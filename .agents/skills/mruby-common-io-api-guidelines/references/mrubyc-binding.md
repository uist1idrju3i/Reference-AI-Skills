# 周辺機器bindingの待機と検証

一般的なC API、引数・kwargs/block、戻り値と所有権、raise、schedulerの動作は[mrubyc-c-bindingの契約表](../../mrubyc-c-binding/references/api.md)へ集約しています。MPIGの規定は[契約表](mpig.md)、mruby側との差は[比較表](mruby-hw.md)を参照します。

## 長い待機とtimeoutの設計

以下は周辺機器向けの設計方針です。転送開始・状態確認・完了取得を短いC methodへ分け、Rubyで期限を確認してsleep_msを挟むか、非同期backendの完了をforegroundで回収します。標準UART.readの「指定長まで呼出しtaskが待つ」という[契約](mpig.md)を保ち、非blockingなnil-returnへ黙って変えません。
sleep/relinquishの一般的な意味とC methodの制約は[taskとHAL](../../mrubyc-c-binding/references/api.md#taskとhal)を確認します。

単調時刻による期限、各C呼出しの最大時間、tickの丸め、Integerの桁あふれ、timeout後の遅延完了、取消し、部分転送とbuffer寿命を決めます。relinquishだけを繰り返すbusy pollingを避け、未完了なら有限時間sleepしてから確認します。

## ISRは通知だけにする

周辺機器driverでは、ISRは固定容量のflag/ring bufferへの通知だけにし、Ruby値への変換と配送はforegroundで行う方針にします。overflow、複数writer、memory ordering、割込み禁止区間は対象HALとCPUで設計します。
一般VM APIとHAL専用tickの区別、thread safetyを一般化できない根拠は[taskとHAL](../../mrubyc-c-binding/references/api.md#taskとhal)を参照します。

GPIO例は型違いにTypeError、fakeのpin範囲外にRangeError、flags違反にArgumentError、writeの0/1以外にRangeErrorを採用しています。MPIGの規定と導入先方針の区別は[契約表](mpig.md)に従います。実機driverのIOError、busy、timeout/cancelはGPIO fakeには実装していません。

## fake GPIO例と再現

[scripts/gpio-example](../scripts/gpio-example/)のbinding.c、fake_hal.c/h、contract.rbを[runner](../scripts/gpio-example/run.py)で実行します。runnerは隣のmruby-idiomaticのprobe_mrubyc.pyから実行・分類・harnessを再利用するので、両スキルを同じskillsディレクトリに置きます。Python標準ライブラリのほか、cc/ar/make/Rubyとmrbcが必要です。

pinは0〜7のInteger、1 pin 1bit、初期levelは0です。方向とpullの排他、不明bitの拒否、class setmodeの方向必須、instance setmodeの方向なし部分更新、方向指定時のpull解除はこの例の採用方針です。複数instanceは同じpinを共有し、所有権を予約せず、releaseもありません。fakeのlevelは入力注入と出力書込みで共有し、pullやHIGH_Zの電気的作用を模擬しません。FakeGPIOとBindingProbeは試験専用の観測・注入APIです。

通常の入出力、空String/nil等の不正入力、必須方向なし、排他flags、範囲外write、classのread_at/write_at/high_at?/low_at?とinstanceのhigh?/low?、拒否時にHAL状態が変わらないことを自己検査します。GPIOの非待機例なのでbusy/timeout/ISR/電気特性は未検証です。採用先の転送APIで別途試験します。

スキルのrootで、未使用の保存先を指定します。ソースは一時コピーにしてPOSIX HALでbuildし、原本を変更しません。

```sh
python3 scripts/gpio-example/run.py \
  --mrubyc "$MRUBYC_SOURCE" --mrbc "$MRBC" \
  --out "$RESULTS_DIR/gpio-release4.0.0" --repeat 5
```

2026-11-22にrelease4.0.0とmrbc 4.0.0で5回実行しました。default vm_configはInteger 32bit、Float 64bit、UTF-8無効です。5/5が `PASS gpio-contract`、終了コード0で、status/exit/diagnosticが全回一致し、source tree unchangedもYESでした。新しい保存先にmetadata.json、compile/runのstdout/stderr/JSON、各回のbytecodeを残します。保存先はリポジトリ外とし、記録にはcommit、compiler、mrbc版、flags、入力hashを含めます。固定版の再実行と、導入先版での適合判定は区別してください。
