# 固定版C APIと検証

主対象はmruby/c release4.0.0、commit `434bccd609f2a3e90d6bb95c458621898bc6a508`、mrbc mruby 4.0.0、POSIX HALです。既定vm_configはInteger32、Float64、UTF-8無効。以下はソース上の契約と、この設定での実測を区別します。[設定][MCFG]・[数値型][MNUMTYPES]
未検出APIの将来版での不存在や、全portの安全性まで断定しません。

## 初期化とbytecode

| 操作 | 固定版の契約・注意 |
|---|---|
| `mrbc_init(pool, size)` | 初回HAL初期化、allocator/global/class、scheduler関連classを初期化する。独自登録はその後、task開始前に置く。[init][MINIT]・[上流例][MSAMPLE] |
| `mrbc_init_alloc` | poolの4-byte境界、非ゼロsize、サイズ型の範囲をassertし、sizeを4-byte単位へ切り下げる。ヘッダ等の分はobjectに使えない。allocator初期化だけをVM全体の初期化と混同しない。[pool][MPOOL] |
| pool容量 | 「max 64KB」というコメントだけで上限を決めない。既定の型定義は異なり、付属fixtureでは1MiBを使用した。必要量や最小安全容量は導入先で測定する。[型][MPOOLTYPE]・[実行fixture](../scripts/run.py) |
| `mrbc_create_task` | VM open、load、begin、queue登録を行う。既定状態はREADY。load失敗ならVMを閉じてNULLを返すため、戻り値を検査する。[create][MCREATE]・[既定][MDEFAULTSTATE] |
| `mrbc_load_mrb` | IREPは入力buffer内の命令・poolを参照し、symbolも入力を指し得る。task終了だけでなく、Ruby method等の全利用者がなくなるまでbufferを生存・不変に保つ。[load][MLOAD]・[symbol][MLOADSYM]・[method保持][MDEF] |
| IREP解放 | `mrbc_irep_free`はIREP領域を解放するが、元bytecodeを解放しない。C側のbuffer ownerを決める。[free][MIREPFREE] |

## 登録とreceiver

| API | 契約 |
|---|---|
| `mrbc_define_class(vm, name, super)` / `mrbc_define_module` | class/moduleを登録する。`*_under`は親class/module配下の定数へ登録する。登録時にNULL VMを渡す例もある。[登録][MCLASS]・[例][MSAMPLE] |
| `mrbc_define_method(vm, cls, name, callback)` | callbackは `void f(mrbc_vm *vm, mrbc_value v[], int argc)`。登録にarity指定はなく、callbackで検査する。[型][MFUNCTYPE]・[method][MMETHOD] |
| class/instance method | lookupはClass receiverとObject receiverから同じclassのmethod表を探し得る。別のclass-method登録APIを推測せず、専用methodはreceiverの型・identityを検査する。[lookup][MLOOKUP] |
| constructor | Object.newはinstanceを作ってinitializeを呼ぶ。C initializeはreceiverをnilへ置き換えず、必要な状態を設定する。new/callの特別扱いを通常のdispatchと混同しない。[new][MOBJECTNEW]・[initialize][MINITIALIZE]・[dispatch][MDISPATCH] |
| `mrbc_set_const` / `mrbc_set_class_const` | global/class定数を登録する。所有権は下表を参照。[const][MCONST] |
| `mrbc_instance_new(vm, cls, size)` | instance構造体にsize bytesの追加領域を確保。`instance->data`にnative状態を置ける。外部資源のowner・release条件は導入先で決める。[instance][MINSTANCE] |
| destructor | `MRBC_INSTANCE_DESTRUCTOR`は既定で有効。`mrbc_define_destructor`で設定し、非built-in classのinstance削除時に呼ばれる。pool全体の破棄が各objectのdestructorを呼ぶとは仮定しない。[既定][MDTORDEFAULT]・[設定][MDESTRUCTOR]・[削除][MINSTANCE]・[pool cleanup][MPOOLCLEAN] |

## 引数

| 要素 | 配置・検査 |
|---|---|
| receiver / positional | `v[0]`はself、`v[1..argc]`は位置引数。通常dispatchはcallback後に引数をreleaseするので、保存する借用値はretainする。[dispatch][MDISPATCH] |
| kwargs / block | kwargsがあればHashは`v[argc+1]`、blockは`v[argc+2]`。なければblockは`v[argc+1]`、block不在はnil。空のkeyword splatは除かれ得るので、位置を固定して読まない。[dispatch][MDISPATCH] |
| `MRBC_KW_ARG(a, b)` | Hashから値を取り外す。省略はEMPTY、nilは指定済み。`MRBC_KW_ISVALID`で区別する。[macros][MKW] |
| mandatory / unknown | `MRBC_KW_MANDATORY(a)`は不足、`MRBC_KW_END()`は残る未知keywordをArgumentErrorにする。失敗後に処理を続けない。[macros][MKW] |
| rest / cleanup | `MRBC_KW_DICT(rest)`は残余Hashの所有権を取る。`MRBC_KW_DELETE`で取り出した値を全経路でreleaseする。返す値は移譲または別途retainし、二度releaseしない。[macros][MKW]・[使用fixture](../scripts/binding.c) |
| type / string | `mrbc_type`と`MRBC_TT_*`で型を先に確認。`mrbc_integer` / `mrbc_float`はpayload読出しで一般的な変換・検証ではない。Stringは型検査後にcstr/sizeを使い、埋込みNULを許す契約ではstrlenで代用しない。[tag][MTAGS]・[payload][MBOX]・[String][MSTRACCESS] |
| `MRBC_ARG_I` | 不足はArgumentError、nilはTypeError。Integerに加えFloatも受けて整数へ変換する。厳密なInteger契約なら型と範囲を別に検査する。[helper][MARG] |

keywordのcleanupとraise後のreturnは[fixtureのkeyword method](../scripts/binding.c)を参照します。fixtureは固定入力の検査用で、汎用の安全なbinding libraryではありません。

## 戻り値と所有権

ここで「移譲」は、成功後に呼出し元が同じowner分をreleaseしないこと、「借用」は、保存・返却に別のretainが必要なことを意味します。

| 操作 | 所有権・副作用 |
|---|---|
| `SET_RETURN(value)` | 式を一時値に保存→古い`v[0]`をdecref→代入。新しい値をincrefせず、C functionからreturnもしない。[macro][MRETURN] |
| scalar return | `SET_INT_RETURN`、`SET_NIL_RETURN`、`SET_BOOL_RETURN`等も古いreceiverをreleaseする。[macro][MRETURN] |
| 新規String/Array/Hash | newで得たowner分をSET_RETURNへ移譲する。返却後に同じowner分をreleaseしない。[String][MSTRNEW]・[Array][MANEW]・[Hash][MHNEW]・[return][MRETURN] |
| selfの返却 | sole-owned objectの`SET_RETURN(v[0])`は古いselfのreleaseでobjectを破棄し得る。先に返却分をincrefする。fixtureはdestructor回数で危険な場合とretain後を区別し、解放済みobjectは参照しない。[macro][MRETURN]・[refcount][MREF]・[fixture](../scripts/binding.c) |
| `mrbc_incref` / `mrbc_decref` | object型の参照数を増減し、ゼロなら型別destructorを呼ぶ。即値は対象外。`mrbc_decref_empty`はslotもEMPTYにする。[refcount][MREF] |
| Array set / push / get | 成功時set/pushは値を移譲、getは借用。既存slotの置換は旧値をreleaseする。setterの失敗時・部分更新も別途確認する。[set][MASET]・[push][MAPUSH]・[get][MAGET] |
| Hash set / get | setはkey/valueを移譲し、置換時は旧値をrelease。getは借用。[set][MHSET]・[get][MHGET] |
| ivar set / get | 固定版のsetは渡した値をretain、getも返す値をretain。get後の不要なowner分はreleaseする。[ivar][MIVAR] |
| const/global set / get | setは自動retainしない。getは借用。C側でも保持するなら保存分を別にretainする。[const][MCONST]・[global][MGLOBAL]・[内部table][MKV] |
| dup | Array/Hashは浅いdup、Stringも専用dupを持つ。調べた公開headerに汎用`mrbc_dup`は見つからなかった。[Array][MADUP]・[Hash][MHDUP]・[String][MSTRDUP] |
| C staticの保存 | 借用値を保存前にretainし、置換・取消し・shutdownでrelease。Procはcallinfo/IREPも参照するためobjectのretainだけでframeやVMをまたげると仮定しない。[refcount][MREF]・[Proc][MPROCNEW] |
| GC | 調査したrefcount/allocator/VM処理にtracing/cycle GCの公開APIは見つからなかった。循環ownerの自動回収を仮定しない。一方、最後のdecrefで通常のobjectは解放される。[refcount][MREF]・[allocator cleanup][MPOOLCLEAN]・[VM end][MVMEND] |

## 例外とCからの呼出し

| API | 契約・制限 |
|---|---|
| `mrbc_raise` / `mrbc_raisef` | VM例外とpreemption flagを設定してCへ戻る。longjmpしない。cleanupして即returnする。NULL VMでは例外設定ではなく出力になる。[raise][MRAISE] |
| custom exception | StandardError派生classを定義してraiseへ渡せる。fixtureでcustom例外をrescueする。[class][MCLASS]・[raise][MRAISE] |
| 例外の継承 | ArgumentError、RangeError、TypeError、IOErrorはStandardError派生。NotImplementedErrorはException直下なので通常のrescueだけでは捕まらない。[class定義][MERRORCLASSES] |
| 検出 / clear | `mrbc_israised(vm)`で例外状態を検出。`mrbc_clear_exception`は意図的に処理済みにした場合だけ使い、無条件に握りつぶさない。[検出][MISRAISED]・[clear][MCLEAR] |
| `mrbc_send` | beta表記。C methodのみ同期呼出しでき、Ruby IREPはNotImplementedError、未定義はNoMethodError。scratch registerを使うため引数や返却値の所有権を一般的なfuncallから推測しない。[send][MSEND] |
| block/yield | 公開headerに`mrbc_funcall` / `mrbc_call_block`は見つからなかった。Proc#callはVMのcallinfo/IREPを切り替える処理で、C stackの同期yieldではない。C実装という理由だけでProc#callを同期sendの対象にしない。推奨はRuby wrapperでblockを呼ぶこと。[dispatch][MDISPATCH]・[Proc#call][MPROCCALL] |
| `mrbc_run_mrblib` | 新しいVMでbytecodeを同期実行するlibrary登録用の別用途。既存receiverの任意methodを呼ぶAPIではない。[実装][MRUNLIB] |

## taskとHAL

| 操作 | 固定版の契約・設計への帰結 |
|---|---|
| `mrbc_run` | ready taskのVMを同期実行。自然終了はdormantへ移し、非permanentならVM end。scheduler-exit設定とqueue条件によって戻る。[run][MRUN] |
| C methodのblocking | run→VM dispatch→method.funcは同期呼出し。preemption検査はopcode後なのでCが戻るまで同じschedulerの他Ruby taskは動かない。別OS threadや割込み全体の停止という意味ではない。[run][MRUN]・[dispatch][MDISPATCH]・[検査位置][MEXECDONE] |
| tickの反証確認 | tickはtimeslice/preemptionを更新し、POSIX timerもtickを呼ぶ。C stackを保存して別taskを実行する処理ではない。以上はソース確認であり、2 taskの遅延実測ではない。[tick][MTICK]・[timer][MPOSIXTIMER] |
| sleep / relinquish | task状態やpreemptionを変更して戻る。任意のC stackを中断・再開しないため、呼んだC側も速やかにreturnする。[sleep][MSLEEP]・[relinquish][MRELINQUISH] |
| `mrbc_get_tcb` | TCB内のVMからoffsetを引く変換。scheduler管理外の独立VMへ適用しない。[変換][MGETTCB]・[独立VMの例][MRUNLIB] |
| start / suspend / resume / terminate / delete | startはdormantだけをreadyにし、loadやbeginは行わない。suspend/resumeはqueue状態を変更、terminateは保持mutexをunlockしない。deleteはdormantが前提でVM closeする。[start][MSTART]・[state][MSTATE]・[delete][MDELETE] |
| mutex / semaphore | mutexのinit/lock/unlock/trylockがある。調べた公開scheduler APIにsemaphoreは見つからなかった。[mutex][MMUTEX]・[宣言][MRRTAPI] |
| ISR/他thread | 一般VM APIの再入・thread safety保証は確認できない。refcountや共有poolを更新するため、安全側の規約としてVM処理をforegroundへ集約し、producer側は同期した固定容量queueに通知だけを渡す。[refcount][MREF]・[allocator][MPOOL] |
| IRQ制御 | POSIX enable/disableはSIGALRM mask。任意thread間mutexではなく、複数producerの同期・memory orderingは導入先で決める。HAL専用tickを一般ISR-safe APIへ拡大解釈しない。[IRQ][MPOSIXIRQ]・[tick][MPOSIXTIMER] |
| port実装 | write/flush/idle_cpu/enable_irq/disable_irq/init/abort等を提供する。consoleはHAL writeへ出力する。POSIX abortはexit(1)。portごとの契約を確認する。[HAL][MPOSIXHAL]・[console][MCONSOLE]・[abort][MPOSIXABORT] |

## 寿命と版の注意

release4.0.0で`MRBC_ALLOC_VMID`が有効ならVM endがそのVMの割当領域を一括解放する。C staticへincrefしただけでtask終了をまたげるとは限らない。`NULL` VMによるVM非依存割当でも、参照先やpool全体の寿命は別問題です。明示的なcancel/releaseとshutdown順序を決めてください。[VMID][MVMID]・[free_all][MFREEALL]・[end][MVMEND]

master比較は調査時HEAD `5bb8ae6466cc5f8ba87ca8dad4ee4f62b5d4dc14`に限定します。ivarはclass ivar対応に伴い対象・setter戻り値が変わり、allocatorからVMID経路も削除されています。固定版のivar/VMID説明をそのまま移さず、対象commitで確認します。masterで全fixtureを実行した結果ではありません。[ivar][UIVAR]・[allocator][UALLOC]
同HEADの条件付きscheduler hookにも、thread context・sleep禁止・再入禁止等の制約があります。release4.0.0の標準機能として扱いません。[hook][UHOOK]

## POSIXでの再現

[scripts/run.py](../scripts/run.py)は隣のmruby-idiomaticのprobe runnerをimportし、sourceのコピーでbuildします。両スキルを同じskills directoryに配置してください。Python標準ライブラリ、git、make、Ruby、cc、ar、mrbc 4.0.0が必要です。保存先はリポジトリ外の新しいdirectoryを指定します。

スキルrootで実行します。

```sh
python3 scripts/run.py \
  --mrubyc "$MRUBYC_SOURCE" --mrbc "$MRBC" \
  --out "$RESULTS_DIR/binding-release4.0.0" --repeat 5
```

期待する全PASS行は[scripts/expected.json](../scripts/expected.json)が正本です。全行が各1回出ること、未知の出力やstderrがないこと、exit=0、timeoutなしを検査します。完了markerだけの出力は成功としません。C stdioとHAL出力の順序差があるため、PASS行の順序には依存しません。
refcount/destructor、self返却、kwargs/block、保存したblock、raise後のreturnと副作用、mrbc_sendのC限定、数値helperを自己検査します。[C fixture](../scripts/binding.c)・[Ruby fixture](../scripts/contract.rb)

2026-11-22に上記固定版とmrbc 4.0.0で5回実行し、5/5で全39検査群と完了markerが各1回一致しました。全回exit=0、timeoutなし、stderr空、status/exit/diagnostic一致、source tree unchanged=YESです。実測configはInteger32、Float64、UTF-8無効、pool 1MiB、MAX_REGS110、MAX_SYMBOLS255でした。結果は保存先のmetadata.json、run-1.run.stdout等で確認できます。compile/runのraw出力、各回のbytecode、sourceのcommit・設定、compiler/mrbc版、flags、入力hashを保存します。このfixtureは固定入力の実験であり、一般入力を受けるproduction-ready libraryではありません。
未検証は実機IRQ/thread競合、長いC callbackの2 task遅延、OOM、全VMID設定、捕捉frame終了後のProc、destructor inheritanceです。トップレベルblockの同一VM内保存だけを、任意のclosureの寿命保証に拡張しません。[Procの参照先][MPROCNEW]

[MCFG]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm_config.h#L18-L66
[MNUMTYPES]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L39-L55
[MGETTCB]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.h#L140-L150
[MOBJECTNEW]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_object.c#L105-L127
[MINITIALIZE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_object.c#L50-L77
[MERRORCLASSES]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.c#L285-L355
[MINIT]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L1479-L1510
[MSAMPLE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/sample_c/sample_myclass.c#L44-L88
[MPOOL]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/alloc.c#L447-L489
[MPOOLTYPE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/alloc.c#L129-L179
[MCREATE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L228-L253
[MDEFAULTSTATE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.h#L56-L62
[MLOAD]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/load.c#L131-L158
[MLOADSYM]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/load.c#L209-L229
[MDEF]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c#L2941-L3012
[MIREPFREE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/load.c#L347-L361
[MCLASS]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c#L109-L263
[MFUNCTYPE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L61-L64
[MMETHOD]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c#L266-L295
[MLOOKUP]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.h#L250-L279
[MCONST]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/global.c#L50-L112
[MINSTANCE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c#L298-L336
[MDTORDEFAULT]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.h#L34-L38
[MDESTRUCTOR]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.h#L283-L300
[MPOOLCLEAN]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/alloc.c#L492-L505
[MDISPATCH]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c#L53-L162
[MKW]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L427-L453
[MTAGS]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L68-L103
[MBOX]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/boxing_no.h#L23-L70
[MSTRACCESS]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_string.h#L111-L125
[MARG]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L549-L598
[MRETURN]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L221-L252
[MSTRNEW]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_string.c#L56-L100
[MANEW]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_array.c#L76-L97
[MHNEW]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_hash.c#L71-L92
[MREF]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L546-L594
[MASET]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_array.c#L162-L216
[MAPUSH]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_array.c#L236-L254
[MAGET]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_array.c#L200-L215
[MHSET]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_hash.c#L153-L179
[MHGET]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_hash.c#L182-L193
[MIVAR]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c#L339-L367
[MGLOBAL]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/global.c#L146-L168
[MKV]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/keyvalue.c#L228-L290
[MADUP]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_array.c#L479-L501
[MHDUP]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_hash.c#L299-L322
[MSTRDUP]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_string.c#L138-L155
[MPROCNEW]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_proc.c#L34-L74
[MVMEND]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c#L362-L389
[MRAISE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.c#L137-L218
[MISRAISED]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.h#L37-L38
[MCLEAR]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.c#L196-L206
[MSEND]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c#L504-L575
[MPROCCALL]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_proc.c#L109-L131
[MRUNLIB]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c#L587-L613
[MRUN]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L347-L432
[MEXECDONE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm.c#L3301-L3336
[MTICK]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L145-L180
[MPOSIXTIMER]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/hal/posix/hal.c#L41-L115
[MSLEEP]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L503-L525
[MRELINQUISH]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L564-L573
[MSTART]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L323-L339
[MSTATE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L602-L664
[MDELETE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L262-L273
[MMUTEX]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.c#L694-L837
[MRRTAPI]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/rrt0.h#L111-L137
[MPOSIXIRQ]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/hal/posix/hal.c#L119-L144
[MPOSIXHAL]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/hal/posix/hal.h#L54-L111
[MCONSOLE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/console.c#L125-L194
[MPOSIXABORT]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/hal/posix/hal.c#L144-L156
[MVMID]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/alloc.h#L77-L89
[MFREEALL]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/alloc.c#L935-L950
[UIVAR]: https://github.com/mrubyc/mrubyc/blob/5bb8ae6466cc5f8ba87ca8dad4ee4f62b5d4dc14/src/class.c#L358-L413
[UALLOC]: https://github.com/mrubyc/mrubyc/blob/5bb8ae6466cc5f8ba87ca8dad4ee4f62b5d4dc14/src/alloc.h#L59-L110
[UHOOK]: https://github.com/mrubyc/mrubyc/blob/5bb8ae6466cc5f8ba87ca8dad4ee4f62b5d4dc14/src/rrt0.h#L156-L169
