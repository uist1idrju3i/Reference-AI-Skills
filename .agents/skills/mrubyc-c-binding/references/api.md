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

### keywordの失敗経路と後始末

推奨形は[公式のkeyword引数例](https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/doc/c_KeywordArgument.md#L1-L21)と同じく、失敗時に`goto RETURN;`で関数末尾の`RETURN:`へ飛ぶ形です。driver呼出しや`SET_RETURN`などの正常処理はlabelより前に置き、label以降には`MRBC_KW_DELETE`などの後始末だけを置きます。後始末の後ろに処理を置かず、そのまま関数からreturnします。[実行fixtureのkeyword_guard](../scripts/binding.c)もこの形です。

Symbolを期待する引数に別の型が渡った場合は、黙ってbreakせず、`mrbc_raise(vm, MRBC_CLASS(TypeError), ...)`で例外を設定してから`goto RETURN;`で後始末へ進みます。[型検査][MTAGS]・[raise][MRAISE]

`do { … break; } while (0)`を使う場合は、driver呼出しや成功値の設定など、副作用のある正常処理をloop内に置き、loopの後ろは後始末だけにします。`MRBC_KW_MANDATORY`や`MRBC_KW_END`がraiseしてもC関数は中断されず、breakはloopから抜けるだけなので、loopの後ろの処理も実行されるためです。[keyword macros][MKW]・[raise][MRAISE]

fixtureは不足・未知keyword・型違いの例外をRubyでrescueし、各失敗直後に副作用カウンタが0であることを確認します。正常時にはカウンタが1になることも検査し、常に0を返すだけの実装を成功としません。[契約テスト](../scripts/contract.rb)・[期待値](../scripts/expected.json)

## 型ごとの受け渡し

型名は固定版の公開tag一覧に合わせます。`MRBC_TT_FIXNUM`はINTEGERと同じ値です。EMPTYはkeyword省略の判定だけに使い、Rubyへ返すnilとは区別します。次の読出しは、先にtagを検査した値へ適用します。[tag一覧][VTYPES]・[payloadと生成][VBOX]・[keyword macros][MKW]

| 型 | 判定 | 読み出し | 生成 | 所有権・注意 |
|---|---|---|---|---|
| `MRBC_TT_NIL` / `MRBC_TT_TRUE` / `MRBC_TT_FALSE` | mrbc_typeで各tagを区別 | tag自体。0・空Stringとは別 | mrbc_nil_value / mrbc_true_value / mrbc_false_value / mrbc_bool_value | 即値。strict boolはTRUE/FALSEだけを受ける。[boxing][VBOX]・[bool helper][VARGB] |
| `MRBC_TT_INTEGER` | tag、必要ならkind_of | mrbc_integer | mrbc_integer_value、SET_INT_RETURN | 即値。mrbc_int_tの幅と出力C型の両方を検査。[boxing][VBOX]・[数値型][MNUMTYPES] |
| `MRBC_TT_FLOAT` | tag。Float有効設定を確認 | mrbc_float | mrbc_float_value(vm, n)、SET_FLOAT_RETURN | 即値。整数化前に有限・範囲・小数部の方針を決める。[boxing][VBOX]・[設定][MCFG]・[変換][VCONV] |
| `MRBC_TT_SYMBOL` | tagと許可sym_id集合 | mrbc_symbol、mrbc_symbol_cstr（借用文字列） | mrbc_symbol_new、既知IDからmrbc_symbol_value | 即値だがintern表の容量は有限。str_to_symidへ渡す名前は寿命のある固定文字列とし、動的文字列の生成はコピーを行うsymbol_newの契約を確認。[symbol][VSYMBOL]・[名前登録][VSYMID]・[読出し][VSYMGET]・[boxing][VBOX] |
| `MRBC_TT_CLASS` / `MRBC_TT_MODULE` | tagとcls identity。find_class_by_object、mrbc_obj_is_kind_ofも目的を区別して使う | cls、class探索結果 | mrbc_define_class/module、*_under。戻るclass pointerとRuby値の表現を混同しない | refcount増減対象外。fixtureのvalue_makeは固定版の内部即値表現を使う検査用adapterで、汎用のpublic constructorではない。[登録][MCLASS]・[lookup][MLOOKUP]・[kind_of][VKIND]・[tag境界][VTYPES]・[表現][VBOX] |
| `MRBC_TT_OBJECT` | tag→class→登録済みinstance identity→data | instance->data。sizeを保証した生成元だけが読む | mrbc_instance_new(vm, cls, extra_size) | refcount対象。classが同じでも追加dataが同じlayoutとは限らない。fixtureは専用constructorと生存中のregistry ownerを使う。[instance][MINSTANCE]・[class構造][VOBJECT]・[fixture](../scripts/value_contract.c) |
| `MRBC_TT_PROC` | tag、必要ならkind_of | Procの保持・受渡し。Cからの同期yieldとは別 | mrbc_proc_newには有効なVM/IREP/callinfoが必要。通常のcallbackはRubyのProc.new/blockを受ける | 保存・返却分をretain。objectだけを延命してframe/IREP寿命を保証しない。[Proc][MPROCNEW]・[call][MPROCCALL]・[fixture](../scripts/contract.rb) |
| `MRBC_TT_ARRAY` | tag→長さ→全要素のtag/範囲 | mrbc_array_size / mrbc_array_get | mrbc_array_new、set/push | getは借用、成功時set/pushは移譲。全件検査後にC bufferへコピー。[Array][VARRAY]・[set][MASET]・[get][MAGET] |
| `MRBC_TT_STRING` | tag→byte長上限→NUL等 | mrbc_string_cstr / mrbc_string_size | mrbc_string_newは指定長をコピー、new_cstrはNUL終端入力 | cstrは借用。保持元の解放・変更をまたがせない。C sizeはbufferのbyte長で、RubyのUTF-8文字数と混同しない。[生成][MSTRNEW]・[accessor][VSTRING]・[UTF-8設定][MCFG] |
| `MRBC_TT_RANGE` | tag→両端のtag/範囲→順序・exclude_end | mrbc_range_first/last/exclude_end | mrbc_range_new(vm, &first, &last, exclude) | newは両端をincrefせず移譲、getは借用。借りた端点から新Rangeを作るなら返却分を先にretain。new自体が端点の型・順序を検査するとは仮定しない。[new/delete][VRANGE]・[get][VRANGEGET] |
| `MRBC_TT_HASH` | tag→長さ→全key/value | hash_size、hash_get、mrbc_hash_iterator_new / i_has_next / i_next | mrbc_hash_new / hash_set | getとiteratorのpairは借用。走査中にHashを変更しない。setはkey/valueを移譲するが、追加時にkeyだけが入る失敗もあり得るため一括成功とみなさない。[set][MHSET]・[iterator][VHASHIT]・[new][VHASHNEW] |
| `MRBC_TT_EXCEPTION` | tag、kind_ofで許す例外classを確認 | exception->cls / message / message_size | mrbc_exception_new、mrbc_exception_new_alloc | newはlen>0ならmessageをコピー、len=0ならROM文字列を借用。new_allocは渡したbufferを保持し、正のmessage_sizeならdelete時にfreeする。VMへのraise設定とは別。[例外生成・破棄][VEXCEPTION]・[構造][VEXSTRUCT]・[kind_of][VKIND] |

### 検査順序とcontainerの例

1. argcを確認してからslotを読みます。次にtag、全要素・key・endpointの型と中身を検査し、すべて通ってからC型へ変換し、副作用を起こします。payload getterやcastは型検査の代わりになりません。[getter][VBOX]・[argc helper][MARG]
2. Integerはmrbc_int_tのままint16_t等の出力範囲と比較し、その後castします。Floatを整数として扱う契約ではNaN/Inf、出力範囲、小数部を先に検査します。fixtureは小数部を拒否し、betaの整数helperは有限かつ表現可能な値を0方向へ切り捨てる、という違いを検査します。[数値型][MNUMTYPES]・[helper][VARGI]・[fixture](../scripts/value_contract.c)
3. Stringのbyte長上限、埋込みNULの許否、UTF-8設定を決めます。fixtureの上限8byte・NUL拒否は導入先の契約例です。Symbolは型検査後に`mrbc_str_to_symid("write")`等の固定名とIDを比較し、許可集合へ写像します。未知の文字列を無制限にinternしません。[String][VSTRING]・[設定][MCFG]・[symbol][VSYMBOL]・[fixture](../scripts/value_contract.c)
4. Objectはclass判定だけでnative pointerをcastしません。登録された生存instanceとのidentityを確認してから、自分が確保したdataを読みます。HashもkeyがSymbolというだけで許可済みとはせず、key集合とvalueを検査します。[class/instance][VOBJECT]・[kind_of][VKIND]・[fixture](../scripts/value_contract.c)

[value_contract.c](../scripts/value_contract.c)の`array_values` / `typed`は、最大4要素と全Integer/int16範囲を検査した後でC bufferへ写します。`nested`は最大4行×4列の全件を先に検査し、後のloopでコピーします。`hash_values`はiteratorで全keyの型・許可集合とvalueを確認します。一部だけを検査してdriverを呼ぶ例にはしていません。[契約テスト](../scripts/contract.rb)

同fixtureの`build_pair`はArrayとHashを先に必要容量で確保し、子objectを格納してから失敗を注入します。失敗時は作りかけをreleaseし、正常時はHashへArrayを移譲して返します。destructor回数と、最後にregistry以外のownerが残っていないことを検査します。これは部分構築失敗の検査であり、allocatorのOOMやHash拡張途中の全失敗を網羅する試験ではありません。[生成・setter][VARRAY]・[Hash追加][MHSET]・[fixture](../scripts/value_contract.c)

nilは独立した正常値です。boolやClass等に「範囲外」「空」の定義がなければ作り足さず、型違い・nil・identityを検査します。空Array/Hash/String/Range/Proc、数値の0、意味のある型の境界値を別に検査します。[tag][VTYPES]・[契約テスト](../scripts/contract.rb)

### beta helperの契約

この群はheader上betaです。macroはC callback内のvm/v/argcを使います。1始まりの正の引数番号を指定し、型・範囲検査を省略するために使いません。raiseしたhelperも0やNULLを返してC処理を続けるため、直後に`mrbc_israised(vm)`を確認してreturnまたは後始末へ進みます。0/NULLだけで成功・失敗を判定しません。[macros][VHELPERMACRO]・[helper実装][VARGI]・[例外][MRAISE]

| APIとmacro | 受理値・default・失敗 |
|---|---|
| mrbc_arg / MRBC_ARG | argc不足はArgumentErrorとNULL。それ以外はslot pointerで、値の型は検査しない。[実装][MARG] |
| mrbc_arg_i,i2 / MRBC_ARG_I | Integer/Float。Floatは0方向へ整数化。不足はiがArgumentError+0、i2だけdefault。指定済みnilはTypeError+0で、defaultではない。NaN/Inf・表現範囲は先に検査する。[実装][VARGI] |
| mrbc_arg_f,f2 / MRBC_ARG_F | Integer/Float。不足はfがArgumentError+0、f2だけdefault。nilや他型はTypeError+0。[実装][VARGF] |
| mrbc_arg_s,s2 / MRBC_ARG_S | Stringのみ、借用cstr。不足はsがArgumentError+NULL、s2だけdefault。nilやSymbolはTypeError+NULL。[実装][VARGS] |
| mrbc_arg_b,b2 / MRBC_ARG_B | TRUE/FALSEのみを1/0へ。不足はbがArgumentError+0、b2だけdefault。nilやIntegerの0はTypeError+0。[実装][VARGB] |
| mrbc_val_i,i2 / MRBC_VAL_I | Integer/Float。NULL pointerはiがraiseせず0、i2がdefault。i2はEMPTYもdefaultにするが、nilはどちらもTypeError+0。[実装][VVAL] |
| mrbc_val_f,f2 / MRBC_VAL_F | Integer/Float。NULL pointerはfがraiseせず0、f2がdefault。f2はEMPTYもdefault、nilはTypeError+0。[実装][VVAL] |
| mrbc_val_s,s2 / MRBC_VAL_S | Stringの借用cstr。NULL pointerはsがraiseせずNULL、s2がdefault。s2はEMPTYもdefault、nilはTypeError+NULL。VAL_Bはこのheaderにない。[実装][VVAL]・[macro一覧][VHELPERMACRO] |
| mrbc_to_i/f/s / MRBC_TO_I/F/S | valを書き換える変換。NULL pointerはraiseせず0/NULL、EMPTYはTypeError。数値の直接変換以外はto_i/to_f/to_sをmrbc_sendし、成功時に旧valをreleaseして結果へ置換。送信先の制約や変換後の型を別途確認する。nilはこの版のC実装により0/0.0/空Stringへ変換され、上のstrict helperとは異なる。[変換][VCONV]・[NilClass][VNILCONV]・[send][MSEND] |
| 旧GET_*_ARG、MRBC_TO_INT/FLOAT | headerで非推奨。GETはslot/payloadを読むだけで型を保証しない。旧MRBC_TO_INT/FLOATは非数値ならraiseせず0を返す。新しいMRBC_TO_I/Fとは別物。[旧macros][VLEGACY] |

converterは一般のRuby変換methodが安全に同期実行できるという保証ではありません。fixtureのhelper facadeは、各getter後の例外確認、負のFloatの切り捨て、不足default、nilとNULLの差、既知のC変換methodを検査します。未知のto_*返却型やRuby定義to_*まで検証済みとはしません。[変換][VCONV]・[send][MSEND]・[fixture](../scripts/value_contract.c)・[契約テスト](../scripts/contract.rb)

Exceptionの同一性はCのexception pointerで検査します。この版のmrbc_compareにはException用caseがなくdefaultで1を返すため、fixtureの受け渡し検査をRubyの`==`だけに依存させません。[比較][VCOMPARE]・[fixture](../scripts/value_contract.c)

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
refcount/destructor、self返却、kwargs/block、保存したblock、raise後のreturnと副作用、mrbc_sendのC限定、全公開値tag、beta helper、containerの検査・部分構築失敗を自己検査します。[C fixture](../scripts/binding.c)・[値のfixture](../scripts/value_contract.c)・[Ruby fixture](../scripts/contract.rb)

2026-11-22に上記固定版とmrbc 4.0.0で5回実行し、5/5で全71検査群と完了markerが各1回一致しました。全回exit=0、timeoutなし、stderr空、status/exit/diagnostic一致、source tree unchanged=YESです。実測configはInteger32、Float64、UTF-8無効、pool 1MiB、MAX_REGS110、MAX_SYMBOLS255でした。結果は保存先のmetadata.json、run-1.run.stdout等で確認できます。compile/runのraw出力、各回のbytecode、sourceのcommit・設定、compiler/mrbc版、flags、入力hashを保存します。このfixtureは固定入力の実験であり、一般入力を受けるproduction-ready libraryではありません。
未検証は実機IRQ/thread競合、長いC callbackの2 task遅延、OOM、全VMID設定、捕捉frame終了後のProc、destructor inheritanceです。トップレベルblockの同一VM内保存だけを、任意のclosureの寿命保証に拡張しません。[Procの参照先][MPROCNEW]

[MCFG]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/vm_config.h#L18-L66
[VTYPES]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L76-L105
[VBOX]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/boxing_no.h#L17-L75
[VCOMPARE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L76-L161
[VKIND]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.c#L385-L404
[VOBJECT]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/class.h#L173-L189
[VSYMBOL]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/symbol.c#L331-L362
[VSYMID]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/symbol.c#L207-L239
[VSYMGET]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/symbol.h#L55-L61
[VARRAY]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_array.c#L38-L106
[VSTRING]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_string.h#L84-L137
[VRANGE]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_range.c#L33-L69
[VRANGEGET]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_range.h#L60-L103
[VHASHIT]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_hash.h#L114-L148
[VHASHNEW]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_hash.c#L72-L110
[VEXCEPTION]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.c#L32-L134
[VEXSTRUCT]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/error.h#L42-L75
[VARGI]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L549-L615
[VARGF]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L630-L672
[VARGS]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L687-L726
[VARGB]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L741-L783
[VVAL]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L283-L414
[VCONV]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.c#L429-L533
[VNILCONV]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/c_object.c#L861-L946
[VHELPERMACRO]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L301-L415
[VLEGACY]: https://github.com/mrubyc/mrubyc/blob/434bccd609f2a3e90d6bb95c458621898bc6a508/src/value.h#L254-L297
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
