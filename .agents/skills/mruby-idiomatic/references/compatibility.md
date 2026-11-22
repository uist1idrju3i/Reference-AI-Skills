# CRuby idiom と mruby/c の可否

この表を可否判断の正本とします。結果はfixtureで検査した範囲だけを表し、機能全体への対応を保証しません。

## 測定条件と再現

| 項目 | 条件 |
|---|---|
| mruby/c | [release4.0.0](https://github.com/mrubyc/mrubyc/tree/release4.0.0)、commit `434bccd609f2a3e90d6bb95c458621898bc6a508` |
| mrbc | mruby 4.0.0、表示は `mruby 4.0.0 (2026-04-20)` |
| HAL | POSIX |
| vm_config | 既定、Integer 32bit、Float 64bit、UTF-8 off |
| host | Ubuntu、GCC 11.4.0、Ruby 3.0.2、GNU Make 4.3 |
| build | `-Wall -g -O0 -I../hal/posix`、linkは `-lm`、poolは1 MiB |
| 実行日 | 2026-11-22 |
| 反復 | 5回、status・終了コード・診断行が全回一致 |
| 内訳 | 元の129件、代替60件、Symbol切り分け3件、計192件 |

以下の作業ディレクトリはスキルのルートです。Python 3、C compiler、make、Rubyとmrubyのビルド依存を用意します。
作業用ソースとmrbcを下記の相対パスに用意し、生成したディレクトリと結果はコミットしません。

```sh
mkdir -p .toolchains
git clone --depth 1 --branch release4.0.0 https://github.com/mrubyc/mrubyc .toolchains/mrubyc-release4.0.0
git clone --depth 1 --branch 4.0.0 https://github.com/mruby/mruby .toolchains/mruby-4.0.0
make -C .toolchains/mruby-4.0.0
python3 scripts/probe_mrubyc.py \
  --mrubyc .toolchains/mrubyc-release4.0.0 \
  --mrbc .toolchains/mruby-4.0.0/bin/mrbc \
  --out results/release4.0.0.csv --repeat 5 \
  --expected scripts/expected.csv
```

runnerはソースの一時コピーでmrblib・生成ヘッダー・POSIX HALをビルドします。各probeをcompileしてtimeout付きで実行し、CSV、生のstdout/stderr、終了コード、コマンド、版・設定・SHA-256を含むJSONを結果の隣に保存します。既存の出力名は拒否します。[expected.csv](../scripts/expected.csv)はこの実測から作ったstatusの期待値であり、FAILを成功に読み替えるものではありません。期待値との比較はstatus、5回の比較はstatus・終了コード・診断行が対象です。

異なるバージョン・vm_config・HALでは結果が変わります。採用する環境で再実行してください。現在のrunnerはmrbc 4.0.0を要求するため、別のmrbcを採用する場合は版の検査とbytecode互換性も見直します。表を更新するときは、正常・空・nil・不正入力をfixtureで検査し、期待値を単に合わせず差分の意味を確認します。

## 結果の読み方

- 「使える」はfixtureのPASSです。「使えない」は検査した操作の実行エラーです。「CRubyと意味が違う」は自己検査のFAIL、または通常例は通るものの境界条件が異なる場合です。
- 存在確認の2件では「使えない」はrespondによる検査手順に掛かります。sleep・sleep_ms・Taskの不存在を意味しません。
- 代替リンクはすべて同じ条件で5回PASSしたprobeです。同一機能の再実装とは限りません。対象の入力や戻り値を狭めたものは、その制限を代替欄とコードで確認します。

## 制御構造

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`guard clause / 修飾if・unless`](../scripts/probes/guard-clause.rb) | 使える | 自己検査PASS | — |
| [`case-when`](../scripts/probes/case-when.rb) | 使える | 自己検査PASS | — |
| [`case-in-array`](../scripts/probes/case-in-array.rb) | CRubyと意味が違う | 通常例は通過。nil非一致でdeconstruct例外 | [alt-case-in-array](../scripts/probes/alt-case-in-array.rb)：型・長さ・タグを明示検査 |
| [`case-in-hash`](../scripts/probes/case-in-hash.rb) | CRubyと意味が違う | 通常例は通過。nil非一致でdeconstruct_keys例外 | [alt-case-in-hash](../scripts/probes/alt-case-in-hash.rb)：has_key? で明示検査 |
| [`case-in-find`](../scripts/probes/case-in-find.rb) | CRubyと意味が違う | 通常例は通過。nil非一致でdeconstruct例外 | [alt-case-in-find](../scripts/probes/alt-case-in-find.rb)：限定したタグ列を明示検査 |
| [`case-in-pin`](../scripts/probes/case-in-pin.rb) | CRubyと意味が違う | 通常例は通過。nil非一致でdeconstruct例外 | [alt-case-in-pin](../scripts/probes/alt-case-in-pin.rb)：限定した値を明示比較 |
| [`while-until`](../scripts/probes/while-until.rb) | 使える | 自己検査PASS | — |
| [`times-block`](../scripts/probes/times-block.rb) | 使える | 自己検査PASS | — |
| [`times-no-block`](../scripts/probes/times-no-block.rb) | 使えない | blockなしのyieldで例外 | [alt-times-no-block](../scripts/probes/alt-times-no-block.rb)：times に直接block |
| [`loop-break`](../scripts/probes/loop-break.rb) | 使える | 自己検査PASS | — |
| [`&&=`](../scripts/probes/and-assign.rb) | 使える | 自己検査PASS | — |
| [`\|\|=`](../scripts/probes/or-assign.rb) | 使える | 自己検査PASS | — |
| [`&.`](../scripts/probes/safe-navigation.rb) | 使える | 自己検査PASS | — |

## block/Proc

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`lambda`](../scripts/probes/lambda.rb) | 使えない | lambda 未定義 | [alt-lambda](../scripts/probes/alt-lambda.rb)：Proc.new（lambdaとは意味が異なる） |
| [`->`](../scripts/probes/arrow-lambda.rb) | 使えない | 未実装opcode 0x61 | [alt-arrow-lambda](../scripts/probes/alt-arrow-lambda.rb)：Proc.new（lambdaとは意味が異なる） |
| [`proc-new`](../scripts/probes/proc-new.rb) | 使える | 自己検査PASS | — |
| [`yield`](../scripts/probes/yield.rb) | 使える | 自己検査PASS | — |
| [`block-given`](../scripts/probes/block-given.rb) | 使える | 自己検査PASS | — |
| [`explicit-block-param`](../scripts/probes/explicit-block-param.rb) | 使える | 自己検査PASS | — |
| [`block-with-ensure`](../scripts/probes/block-with-ensure.rb) | 使える | 自己検査PASS | — |
| [`&:sym`](../scripts/probes/symbol-to-proc.rb) | 使えない | blockなしのyieldで例外 | [alt-symbol-to-proc](../scripts/probes/alt-symbol-to-proc.rb)：明示block |
| [`each-with-index-chain`](../scripts/probes/each-with-index-chain.rb) | 使えない | blockなしのyieldで例外 | [alt-each-with-index-chain](../scripts/probes/alt-each-with-index-chain.rb)：each_with_index に直接block |
| [`map-with-index-chain`](../scripts/probes/map-with-index-chain.rb) | 使えない | blockなしのyieldで例外 | [alt-map-with-index-chain](../scripts/probes/alt-map-with-index-chain.rb)：each_with_index で組を作る |
| [`to-enum`](../scripts/probes/to-enum.rb) | 使えない | to_enum 未定義 | [alt-to-enum](../scripts/probes/alt-to-enum.rb)：block付き反復へ設計変更 |
| [`_1 block引数`](../scripts/probes/numbered-params.rb) | 使える | 自己検査PASS | — |
| [`it block引数`](../scripts/probes/it-block-param.rb) | 使えない | it 未定義 | [alt-it-block-param](../scripts/probes/alt-it-block-param.rb)：明示block引数 |

## Enumerable/Array

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`each`](../scripts/probes/each.rb) | 使える | 自己検査PASS | — |
| [`map`](../scripts/probes/map.rb) | 使える | 自己検査PASS | — |
| [`select`](../scripts/probes/select.rb) | 使える | 自己検査PASS | — |
| [`reject`](../scripts/probes/reject.rb) | 使える | 自己検査PASS | — |
| [`each-with-index`](../scripts/probes/each-with-index.rb) | 使える | 自己検査PASS | — |
| [`any?`](../scripts/probes/any.rb) | 使える | 自己検査PASS | — |
| [`all?`](../scripts/probes/all.rb) | 使える | 自己検査PASS | — |
| [`none?`](../scripts/probes/none.rb) | 使える | 自己検査PASS | — |
| [`find`](../scripts/probes/find.rb) | 使えない | find 未定義 | [alt-find](../scripts/probes/alt-find.rb)：each と break |
| [`sort-by`](../scripts/probes/sort-by.rb) | 使えない | sort_by 未定義 | [alt-sort-by](../scripts/probes/alt-sort-by.rb)：長さをキーに手動挿入ソート |
| [`min-by`](../scripts/probes/min-by.rb) | 使えない | min_by 未定義 | [alt-min-by](../scripts/probes/alt-min-by.rb)：長さをキーに並べ先頭を取る |
| [`sum`](../scripts/probes/sum.rb) | 使えない | sum 未定義 | [alt-sum](../scripts/probes/alt-sum.rb)：each と初期値で合計 |
| [`group-by`](../scripts/probes/group-by.rb) | 使えない | group_by 未定義 | [alt-group-by](../scripts/probes/alt-group-by.rb)：Hashへ明示集計 |
| [`each-slice`](../scripts/probes/each-slice.rb) | 使えない | each_slice 未定義 | [alt-each-slice](../scripts/probes/alt-each-slice.rb)：幅を検査し手動分割 |
| [`zip`](../scripts/probes/zip.rb) | 使えない | zip 未定義 | [alt-zip](../scripts/probes/alt-zip.rb)：添字で組を作る |
| [`flat-map`](../scripts/probes/flat-map.rb) | 使えない | flat_map 未定義 | [alt-flat-map](../scripts/probes/alt-flat-map.rb)：1段だけ手動展開 |
| [`partition`](../scripts/probes/partition.rb) | 使えない | partition 未定義 | [alt-partition](../scripts/probes/alt-partition.rb)：2個のArrayへ分配 |
| [`tally`](../scripts/probes/tally.rb) | 使えない | tally 未定義 | [alt-tally](../scripts/probes/alt-tally.rb)：Hashへ明示集計 |
| [`reduce`](../scripts/probes/reduce.rb) | 使えない | reduce 未定義 | [alt-reduce](../scripts/probes/alt-reduce.rb)：each と初期値で合計 |
| [`inject`](../scripts/probes/inject.rb) | 使えない | inject 未定義 | [alt-inject](../scripts/probes/alt-inject.rb)：each と初期値で合計 |
| [`count-value`](../scripts/probes/count-value.rb) | CRubyと意味が違う | 指定値の一致件数にならない | [alt-count-value](../scripts/probes/alt-count-value.rb)：手動カウンタ |
| [`count-block`](../scripts/probes/count-block.rb) | CRubyと意味が違う | block条件を反映した件数にならない | [alt-count-block](../scripts/probes/alt-count-block.rb)：手動カウンタ（nil以外） |
| [`Array#dig`](../scripts/probes/array-dig.rb) | 使えない | Array#dig 未定義 | [alt-array-dig](../scripts/probes/alt-array-dig.rb)：固定構造を明示探索 |
| [`Array#sum`](../scripts/probes/array-sum.rb) | 使えない | Array#sum 未定義 | [alt-array-sum](../scripts/probes/alt-array-sum.rb)：each と初期値で合計 |
| [`Array#join`](../scripts/probes/array-join.rb) | 使える | 自己検査PASS | — |
| [`Array#compact`](../scripts/probes/array-compact.rb) | 使えない | Array#compact 未定義 | [alt-array-compact](../scripts/probes/alt-array-compact.rb)：reject でnil除去 |
| [`Array#uniq`](../scripts/probes/array-uniq.rb) | 使える | 自己検査PASS | — |
| [`Array#flatten`](../scripts/probes/array-flatten.rb) | 使えない | Array#flatten 未定義 | [alt-array-flatten](../scripts/probes/alt-array-flatten.rb)：1段だけ手動展開 |
| [`range-step`](../scripts/probes/range-step.rb) | 使えない | Range#step 未定義 | [alt-range-step](../scripts/probes/alt-range-step.rb)：正のstepに限定したwhile |
| [`range-each`](../scripts/probes/range-each.rb) | 使える | 自己検査PASS | — |

## Hash

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`hash-fetch-default`](../scripts/probes/hash-fetch-default.rb) | 使える | 自己検査PASS | — |
| [`hash-fetch-key-error`](../scripts/probes/hash-fetch-key-error.rb) | 使えない | KeyError未定義 | [alt-hash-fetch-key-error](../scripts/probes/alt-hash-fetch-key-error.rb)：has_key? と独自例外 |
| [`hash-each`](../scripts/probes/hash-each.rb) | 使える | 自己検査PASS | — |
| [`hash-map`](../scripts/probes/hash-map.rb) | 使える | 自己検査PASS | — |
| [`hash-select`](../scripts/probes/hash-select.rb) | 使えない | Hash#select 未定義 | [alt-hash-select](../scripts/probes/alt-hash-select.rb)：each でHashを構築 |
| [`hash-to-a`](../scripts/probes/hash-to-a.rb) | 使えない | Hash#to_a 未定義 | [alt-hash-to-a](../scripts/probes/alt-hash-to-a.rb)：each で組を構築 |
| [`hash-dig`](../scripts/probes/hash-dig.rb) | 使えない | Hash#dig 未定義 | [alt-hash-dig](../scripts/probes/alt-hash-dig.rb)：固定構造を明示探索 |

## String/byte

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`string-interpolation`](../scripts/probes/string-interpolation.rb) | 使える | 自己検査PASS | — |
| [`string-append`](../scripts/probes/string-append.rb) | CRubyと意味が違う | nilをTypeErrorで拒否しない | [alt-string-append](../scripts/probes/alt-string-append.rb)：Stringを事前検査 |
| [`string-bytesize`](../scripts/probes/string-bytesize.rb) | 使える | 自己検査PASS | — |
| [`string-each-byte`](../scripts/probes/string-each-byte.rb) | 使える | 自己検査PASS | — |
| [`string-getbyte`](../scripts/probes/string-getbyte.rb) | 使える | 自己検査PASS | — |
| [`string-bytes`](../scripts/probes/string-bytes.rb) | 使える | 自己検査PASS | — |
| [`string-unpack`](../scripts/probes/string-unpack.rb) | 使えない | String#unpack 未定義 | [alt-string-unpack](../scripts/probes/alt-string-unpack.rb)：u16 big-endianだけ手動変換 |
| [`array-pack`](../scripts/probes/array-pack.rb) | 使えない | Array#pack 未定義 | [alt-array-pack](../scripts/probes/alt-array-pack.rb)：u16 big-endianだけ手動変換 |
| [`sprintf`](../scripts/probes/sprintf.rb) | 使える | 自己検査PASS | — |
| [`format`](../scripts/probes/format.rb) | 使えない | format 未定義 | [alt-format](../scripts/probes/alt-format.rb)：sprintf |
| [`percent-w`](../scripts/probes/percent-w.rb) | 使える | 自己検査PASS | — |
| [`percent-i`](../scripts/probes/percent-i.rb) | 使える | 自己検査PASS | — |
| [`heredoc`](../scripts/probes/heredoc.rb) | 使える | 自己検査PASS | — |
| [`symbol`](../scripts/probes/symbol.rb) | 使えない | 空文字列のto_symでSIGSEGV（-11） | [alt-symbol](../scripts/probes/alt-symbol.rb)：空・nilを拒否してto_sym |
| [`string-each-char`](../scripts/probes/string-each-char.rb) | CRubyと意味が違う | UTF-8 offでは「あ」を1文字として返さない | [alt-string-each-char](../scripts/probes/alt-string-each-char.rb)：byte契約に変更しeach_byte |
| [`string-center`](../scripts/probes/string-center.rb) | 使えない | String#center 未定義 | [alt-string-center](../scripts/probes/alt-string-center.rb)：ASCII・空白paddingのみ手動処理 |
| [`string-ljust`](../scripts/probes/string-ljust.rb) | 使える | 自己検査PASS | — |
| [`string-rjust`](../scripts/probes/string-rjust.rb) | 使える | 自己検査PASS | — |

## 数値

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`integer-overflow`](../scripts/probes/integer-overflow.rb) | CRubyと意味が違う | 2147483647 + 1 が -2147483648 にwrap | [alt-integer-overflow](../scripts/probes/alt-integer-overflow.rb)：Floatで範囲検査後に加算 |
| [`large-integer-literal`](../scripts/probes/large-integer-literal.rb) | 使えない | int64未対応の実行時エラー | [alt-large-integer-literal](../scripts/probes/alt-large-integer-literal.rb)：int32の範囲に制約（任意精度ではない） |
| [`float-ops`](../scripts/probes/float-ops.rb) | 使える | 自己検査PASS | — |
| [`integer-digits`](../scripts/probes/integer-digits.rb) | 使えない | Integer#digits 未定義 | [alt-integer-digits](../scripts/probes/alt-integer-digits.rb)：非負整数の十進桁を手動抽出 |
| [`integer-clamp`](../scripts/probes/integer-clamp.rb) | 使える | 自己検査PASS | — |
| [`comparable-clamp`](../scripts/probes/comparable-clamp.rb) | 使えない | Comparable未定義 | [alt-comparable-clamp](../scripts/probes/alt-comparable-clamp.rb)：自作moduleで値の範囲を制約 |

## class/module/可視性

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`keyword-required`](../scripts/probes/keyword-required.rb) | 使える | 自己検査PASS | — |
| [`keyword-default`](../scripts/probes/keyword-default.rb) | 使える | 自己検査PASS | — |
| [`keyword-unknown-error`](../scripts/probes/keyword-unknown-error.rb) | 使える | 自己検査PASS | — |
| [`keyword-rest`](../scripts/probes/keyword-rest.rb) | 使える | 自己検査PASS | — |
| [`splat-multiple-assignment`](../scripts/probes/splat-multiple-assignment.rb) | 使える | 自己検査PASS | — |
| [`default-args`](../scripts/probes/default-args.rb) | 使える | 自己検査PASS | — |
| [`attr-reader`](../scripts/probes/attr-reader.rb) | 使える | 自己検査PASS | — |
| [`attr-accessor`](../scripts/probes/attr-accessor.rb) | 使える | 自己検査PASS | — |
| [`include-module`](../scripts/probes/include-module.rb) | 使える | 自己検査PASS | — |
| [`comparable`](../scripts/probes/comparable.rb) | 使えない | Comparable未定義 | [alt-comparable](../scripts/probes/alt-comparable.rb)：自作moduleで必要な演算のみ |
| [`super`](../scripts/probes/super.rb) | 使える | 自己検査PASS | — |
| [`private`](../scripts/probes/private.rb) | CRubyと意味が違う | 外部からの呼出しが成功 | 内部用の命名と文書で境界を示す。アクセス制御の代替ではない |
| [`protected`](../scripts/probes/protected.rb) | CRubyと意味が違う | 外部からの呼出しが成功 | 内部用の命名と文書で境界を示す。アクセス制御の代替ではない |
| [`is_a? / kind_of?`](../scripts/probes/is-a-kind-of.rb) | 使える | 自己検査PASS | — |
| [`== / eql?`](../scripts/probes/equality-eql.rb) | 使えない | eql? 未定義 | [alt-equality-eql](../scripts/probes/alt-equality-eql.rb)：Integerに限定し型と値を比較 |
| [`class-variable`](../scripts/probes/class-variable.rb) | 使えない | 未実装opcode 0x1c | [alt-class-variable](../scripts/probes/alt-class-variable.rb)：共有ownerを明示的に渡す |
| [`outer-constant-assignment`](../scripts/probes/outer-constant-assignment.rb) | 使えない | 未実装opcode 0x20 | [alt-outer-constant-assignment](../scripts/probes/alt-outer-constant-assignment.rb)：所有module内で定義 |
| [`freeze / frozen?`](../scripts/probes/freeze-frozen.rb) | 使えない | frozen? 未定義（凍結操作には未到達） | 凍結の強制を保証する代替は未検証 |

## 例外

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`begin-rescue-else-ensure`](../scripts/probes/begin-rescue-else-ensure.rb) | 使える | 自己検査PASS | — |
| [`retry`](../scripts/probes/retry.rb) | 使える | 自己検査PASS | — |
| [`custom-standard-error`](../scripts/probes/custom-standard-error.rb) | 使える | 自己検査PASS | — |
| [`raise-class-message`](../scripts/probes/raise-class-message.rb) | 使える | 自己検査PASS | — |
| [`rescue-modifier`](../scripts/probes/rescue-modifier.rb) | 使える | 自己検査PASS | — |
| [`catch-throw`](../scripts/probes/catch-throw.rb) | 使えない | catch 未定義 | [alt-catch-throw](../scripts/probes/alt-catch-throw.rb)：methodのreturnで早期終了 |

## 動的機能

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`respond_to?`](../scripts/probes/respond-to.rb) | 使えない | respond_to? 未定義 | 内省の代替は未検証。対象APIの小さい直接実行probeを別途作る |
| [`method-missing`](../scripts/probes/method-missing.rb) | 使える | 自己検査PASS | — |
| [`define-method`](../scripts/probes/define-method.rb) | 使えない | define_method 未定義 | [alt-define-method](../scripts/probes/alt-define-method.rb)：通常のmethod定義 |
| [`send`](../scripts/probes/send.rb) | 使えない | send 未定義 | [alt-send](../scripts/probes/alt-send.rb)：許可した操作だけcase分岐 |
| [`public-send`](../scripts/probes/public-send.rb) | 使えない | public_send 未定義 | [alt-public-send](../scripts/probes/alt-public-send.rb)：許可した操作だけcase分岐 |
| [`struct`](../scripts/probes/struct.rb) | 使えない | Struct未定義 | [alt-struct](../scripts/probes/alt-struct.rb)：通常のclassとaccessor |
| [`__method__`](../scripts/probes/method-name.rb) | 使えない | __method__ 未定義 | [alt-method-name](../scripts/probes/alt-method-name.rb)：明示したSymbolラベル（内省ではない） |
| [`object-id`](../scripts/probes/object-id.rb) | CRubyと意味が違う | nil.object_id の安定性検査に不一致 | nilを含む同一性の代替は未検証 |

## その他

| idiom | 結果 | 症状 | 代替 |
|---|---|---|---|
| [`then`](../scripts/probes/then.rb) | 使えない | then 未定義 | [alt-then](../scripts/probes/alt-then.rb)：名前付き中間値 |
| [`yield-self`](../scripts/probes/yield-self.rb) | 使えない | yield_self 未定義 | [alt-yield-self](../scripts/probes/alt-yield-self.rb)：名前付き中間値 |
| [`tap`](../scripts/probes/tap.rb) | 使えない | tap 未定義 | [alt-tap](../scripts/probes/alt-tap.rb)：名前付き中間値 |
| [`endless-method`](../scripts/probes/endless-method.rb) | 使える | 自己検査PASS | — |
| [`fiber`](../scripts/probes/fiber.rb) | 使えない | Fiber未定義 | 同等の代替は未検証。必要な機能を対象環境で実装・検証 |
| [`time`](../scripts/probes/time.rb) | 使えない | Time未定義 | 同等の代替は未検証。必要な機能を対象環境で実装・検証 |
| [`regexp`](../scripts/probes/regexp.rb) | 使えない | Regexp未定義 | [alt-regexp](../scripts/probes/alt-regexp.rb)：固定文字列abのindexのみ |
| [`object-space`](../scripts/probes/object-space.rb) | 使えない | ObjectSpace未定義 | 同等の代替は未検証。必要な機能を対象環境で実装・検証 |
| [`Kernel#sleep / sleep_ms 存在確認`](../scripts/probes/sleep-existence.rb) | 使えない | respond_to? 未定義のため存在は未判定 | 内省の代替は未検証。対象APIの小さい直接実行probeを別途作る |
| [`Task / rrt0 存在確認`](../scripts/probes/task-rrt0-existence.rb) | 使えない | respond_to? 未定義のため存在は未判定 | 内省の代替は未検証。対象APIの小さい直接実行probeを別途作る |

## 境界条件と代替の制限

pattern matchingはarray・hash・find・pinの通常例を通過しましたが、nilの非一致でdeconstruct / deconstruct_keysの例外になりました。代替はタグ付き2要素Arrayや固定キーのHashに限定した明示検査であり、任意のpattern、探索、pinの再実装ではありません。

lambdaの代替Proc.newはcallbackとしての通常呼出しを検査しただけです。lambda固有の引数個数検査・returnの意味は代替しません。flattenは1段、pack/unpackはu16 big-endian、centerはASCIIと空白、Regexpは固定文字列abの検索だけです。blockなしEnumeratorの代替は遅延列ではなくblock付き反復です。Hashの存在確認にはkey?ではなく、実測で通ったhas_key?を使います。Comparableの全methodやStructの値比較は再現していません。

既定のUTF-8 offではString#each_charが「あ」を1文字として返す検査に失敗します。代替はbyte列の処理へ契約を変えたもので、Unicode文字列処理ではありません。

int32の上限を超える加算はwrapしました。整数比較の実装も差を返すため、両端に近い値どうしの比較には注意します（[value.c](https://github.com/mrubyc/mrubyc/blob/release4.0.0/src/value.c)）。範囲検査の代替は既定64bit Floatでint32入力の和を評価してから整数加算します。Float無効の設定や任意精度演算の代替ではありません。大きい整数が必要なら表現と契約を別に設計します。

## Symbolの切り分け

非空文字列の変換とto_sは[symbol-nonempty](../scripts/probes/symbol-nonempty.rb)でPASSしました。一方、[symbol-empty-conversion](../scripts/probes/symbol-empty-conversion.rb)は空文字列のto_symだけを実行し、後続のPASS表示より前にSIGSEGV（終了コード-11）になりました。[symbol-empty-string](../scripts/probes/symbol-empty-string.rb)も同じ結果でした。したがって元のprobeのクラッシュはto_sを呼ぶ前の空文字列変換だけで再現します。内部原因は未調査です。Symbol全般が使えないとは結論しません。

## 期待値と単体テスト

最終実測はPASS=120、FAIL=8、RUNTIME_ERROR=64、COMPILE_ERROR=0、TIMEOUT=0でした。代替60件はすべてPASSです。FAILや実行エラーも固定版の観測値として期待値に残しています。存在未判定や未調査を、API不存在や原因解明として扱いません。

runnerの単体テストはリポジトリルートで `python3 -m unittest discover -s tests/mruby-idiomatic` を実行します。CIはPythonだけで分類・timeout・期待値比較・fixture一覧を検査し、mruby/cでの実測は行いません。
