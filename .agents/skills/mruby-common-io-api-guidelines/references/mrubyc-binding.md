# mruby/cのbindingと待機

対象はmruby/c release4.0.0、commit `434bccd609f2a3e90d6bb95c458621898bc6a508`です。以下のリンクはすべてその固定commitです。MPIGの規定は[契約表](mpig.md)、mruby側との違いは[比較表](mruby-hw.md)に分けます。

## C methodの入口

| 実装すること | 固定版の根拠と扱い |
|---|---|
| classを定義する | [class.c: mrbc_define_class / sub_define_class_or_module](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c)で名前と親classを登録する。初期化後、taskを開始する前に行う |
| methodを定義する | [class.c: mrbc_define_method](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c)、[value.h: mrbc_func_t](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h)。入口は `void f(mrbc_vm *vm, mrbc_value v[], int argc)`。v[0]はreceiver、v[1]以降は位置引数 |
| class/instanceで同名methodを持つ | [class.h: find_class_by_object](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.h)はClassとObjectを同じclassのmethod表へ解決する。[vm.c: op_sdef](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c)も同じ表へ登録する。別のclass-method登録APIがあるとは仮定せず、例のsetmodeはreceiverの型でclass呼出しの2引数とinstance呼出しの1引数を分ける |
| 定数とinstance状態 | [global.c: mrbc_set_class_const](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/global.c)、[class.c: mrbc_instance_setiv / mrbc_instance_getiv](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c)を使う。例はInteger pinのみを保持し、driverやbufferの所有権は持たない |
| constructor | [c_object.c: c_object_new / mrbc_instance_call_initialize](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_object.c)がinstanceを作ってinitializeを呼ぶ。C initializeはreceiverをnilで置き換えず、必要な状態だけ保存する |
| 引数個数 | [vm.c: send_by_name](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c)はargcをCへ渡すが、mrbc_define_methodにarity指定はない。例はvを読む前に位置引数の個数と余分なkeywordを検査する。未設定値を0とみなさない |
| 型と数値範囲 | [value.h: MRBC_ARG / MRBC_ARG_I](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h)、[value.c: mrbc_arg / mrbc_arg_i](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c)。不足引数はArgumentError。mrbc_arg_iはFloatも整数へ変換するため、厳密なInteger契約ならmrbc_typeで先に検査する。pinをuint8_tへcastする前、byte列を確保する前に範囲と長さを検査する |
| 戻り値と参照 | [value.h: SET_RETURN / SET_NIL_RETURN / SET_INT_RETURN / SET_BOOL_RETURN / mrbc_incref / mrbc_decref](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h)を使い、receiverと返す値の参照を管理する。[vm.c: send_by_name](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c)が通常の引数を後始末する。new/callには特別扱いがあるので独自constructorを安易に追加しない |
| 例外 | [error.c: mrbc_raise / mrbc_raisefと例外class定義](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.c)。ArgumentError、RangeError、TypeError、IOErrorはStandardError派生。NotImplementedErrorはException直下なので通常のrescueだけでは捕まらない |

`mrbc_raise(vm, MRBC_CLASS(RangeError), "message")`はCのstackをlongjmpしません。[error.c: mrbc_raise](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.c)はvm->exceptionとflag_preemptionを設定して戻ります。失敗後はC側で後始末してreturnし、HAL操作や戻り値の上書きを続けないでください。[vm.c: mrbc_vm_run](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c)がopcode後に例外handlerへ移します。

MPIGが明記する例外を先に採用し、沈黙する部分は導入先の契約にします。例は型違いにTypeError、fakeのpin範囲外にRangeError、flags違反にArgumentError、writeの0/1以外にRangeErrorを選びます。最後のRangeErrorはMPIGのclass write_atの規定に合わせてinstanceにも採用した方針です。実機driverのIOError、busy、timeout/cancelはGPIO fakeには実装していません。

## keywordはCに届く

届きます。ただしmrubyのmrb_get_argsと同じAPIではありません。[vm.c: send_by_name](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c)がkeywordをHashへまとめ、位置引数argcに含めずv[argc+1]へ置いてC methodを同期呼出しします。引数を普通の位置Hashとして渡した場合とは区別します。

[value.h: MRBC_KW_ARG / MRBC_KW_MANDATORY / MRBC_KW_END / MRBC_KW_DICT / MRBC_KW_DELETE](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h)が取得・必須・未知keyword・残余Hash・参照解放を提供します。MRBC_KW_ARGはHashから値を取り外すので、型違いや必須不足のreturnでもMRBC_KW_DELETEで取得済みの値を解放します。MRBC_KW_ISVALIDで「省略」と「nil指定」を分け、既定値はbindingで与えます。

例のBindingProbe.keywordは位置引数1個とrequired:/optional:をCで受けます。argcが1のままであること、既定値、**による展開、必須不足、未知keyword、位置Hashとの違い、nilの型違いをRubyから実行します。GPIO標準method自体にはkeywordを追加せず、不明keywordを拒否します。空の**Hashは引数なしと同じに扱います。

## Cで待つ間、他taskは実行されるか

通常の単一scheduler上では実行されません。固定版の呼出し経路は次のとおりです。

1. [rrt0.c: mrbc_run](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c)がready queueから1 taskを選び、mrbc_vm_runを呼ぶ。
2. [vm.c: mrbc_vm_run → op_send → send_by_name](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c)がCのmethod.funcを通常の関数呼出しで実行する。
3. [rrt0.c: mrbc_tick](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c)はtimesliceを減らしてflag_preemptionを立てる。[POSIX hal.c: sig_alarm](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/hal/posix/hal.c)もこのtickを呼ぶだけで、別taskのVMを実行しない。
4. [vm.c: mrbc_vm_run](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c)がflagを検査するのはopcode処理の後。Cが戻らなければそこへ到達せず、mrbc_runも次のtaskを選べない。

したがってblocking driverをC methodから呼ぶと、その時間だけ同じschedulerの他のRuby taskも止まります。割込みや別OS threadまで停止すると主張しているのではありません。反証のためtick側の処理とMRBC_NO_TIMER分岐も確認しましたが、いずれもC stackを保存してtaskを切り替える経路はありません。これはソースの同期呼出しとscheduler構造に基づく確認であり、GPIO例で2 taskの遅延を実測した結果ではありません。

## 長い待機とtimeoutの設計

[rrt0.c: mrbc_sleep_ms](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c)はtaskをwaiting queueへ移してpreemption flagを立て、mrbc_relinquishはtimesliceを0にしてflagを立てます。**どちらも呼んだC関数の途中から自動的に切り替える関数ではありません。呼んだ後は速やかにreturnが必要です。** [rrt0.c: c_sleep / c_sleep_ms](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c)も状態変更後に戻ります。mrbc_get_tcbは[rrt0.h](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.h)の変換を使い、scheduler管理外のVMへ適用しません。

ここからの設計方針は導入先が決めます。転送開始・状態確認・完了取得を短いC methodへ分け、Rubyで期限を確認してsleep_msを挟むか、非同期backendの完了をforegroundで回収します。標準UART.readの「指定長まで呼出しtaskが待つ」という契約を保ちながら、他taskへ譲れるwrapperにします。非blockingなnil-returnへ黙って変えません。

待機回数だけでなく単調時刻による期限、各C呼出しの最大時間、tick単位の丸め、Integerの桁あふれ、timeout後の遅延完了、取消し、部分転送とbuffer寿命を決めます。これらは上流が一括して保証するものではありません。relinquishだけを繰り返すbusy pollingを避け、未完了なら有限時間sleepしてから確認します。

## ISRは通知だけにする

周辺機器ISRからRuby/VM呼出し、値のallocation/refcount、raise、一般のtask queue操作を行わず、固定容量のflag/ring bufferへ必要最小限の情報を渡します。overflow、複数writer、memory ordering、割込み禁止区間は対象HALとCPUで設計し、foregroundでVM処理へ変換します。

これは上流文書の一文を引用した禁止規則ではなく、安全側のbinding設計規約です。根拠は[alloc.c: mrbc_raw_alloc / mrbc_raw_free](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/alloc.c)が共有poolのfree listを更新すること、[value.h: mrbc_incref / mrbc_decref](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h)が参照数や解放を変更すること、[error.c: mrbc_raise](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.c)が例外を確保してVM状態を書き換えることです。これらに汎用ISR向けの再入保証は確認していません。

例外はHALが意図してISRから呼ぶ専用のmrbc_tickです。[rrt0.c: mrbc_tick](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c)はtick interrupt handlerとされ、[POSIX hal.c: sig_alarm](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/hal/posix/hal.c)からも呼ばれます。これを根拠に、周辺機器ISRから任意のtask APIを呼べると一般化しないでください。

## fake GPIO例と再現

[scripts/gpio-example](../scripts/gpio-example/)のbinding.c、fake_hal.c/h、contract.rbを[runner](../scripts/gpio-example/run.py)で実行します。runnerは隣のmruby-idiomaticのprobe_mrubyc.pyから実行・分類・harnessを再利用するので、両スキルを同じskillsディレクトリに置きます。Python標準ライブラリのほか、cc/ar/make/Rubyとmrbcが必要です。

pinは0〜7のInteger、1 pin 1bit、初期levelは0です。方向とpullの排他、不明bitの拒否、class setmodeの方向必須、instance setmodeの方向なし部分更新、方向指定時のpull解除はこの例の採用方針です。複数instanceは同じpinを共有し、所有権を予約せず、releaseもありません。fakeのlevelは入力注入と出力書込みで共有し、pullやHIGH_Zの電気的作用を模擬しません。FakeGPIOとBindingProbeは試験専用の観測・注入APIです。

通常の入出力、空String/nil等の不正入力、必須方向なし、排他flags、範囲外write、classのread_at/write_at/high_at?/low_at?とinstanceのhigh?/low?、拒否時にHAL状態が変わらないことを自己検査します。GPIOの非待機例なのでbusy/timeout/ISR/電気特性は未検証です。採用先の転送APIで別途試験します。

スキルのrootで、未使用の保存先を指定します。ソースは一時コピーにしてPOSIX HALでbuildし、原本を変更しません。

```sh
python3 scripts/gpio-example/run.py \\
  --mrubyc "$MRUBYC_SOURCE" --mrbc "$MRBC" \\
  --out "$RESULTS_DIR/gpio-release4.0.0" --repeat 5
```

2026-11-22にrelease4.0.0とmrbc 4.0.0で5回実行しました。default vm_configはInteger 32bit、Float 64bit、UTF-8無効です。5/5が `PASS gpio-contract`、終了コード0で、status/exit/diagnosticが全回一致し、source tree unchangedもYESでした。新しい保存先にmetadata.json、compile/runのstdout/stderr/JSON、各回のbytecodeを残します。保存先はリポジトリ外とし、記録にはcommit、compiler、mrbc版、flags、入力hashを含めます。固定版の再実行と、導入先版での適合判定は区別してください。
