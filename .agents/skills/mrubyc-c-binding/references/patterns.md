# 製品実装の比較

これは固定commitの実装観察と採用時の推奨です。mruby/cの一般契約は[API契約表](api.md)、周辺機器の標準契約は[I/Oスキル](../../mruby-common-io-api-guidelines/SKILL.md)を正本にします。

| 観点 | RBOS | OpenBlink | 採用時の判断 |
|---|---|---|---|
| 構成 | shared binding、backend契約、登録入口、native helperに分離。[登録][BREG]・[backend][BBACKEND] | src/api配下の各機能がclass/methodを登録。[LED][OLED]・[I2C][OI2C] | backend交換やfake試験の単位に合わせて分ける |
| error policy | argc/type/status検査helperでRuby例外へ正規化。[helper][BNATIVE] | I2C readは先頭にstatusを置くArray、writeは整数statusを返す。[I2C][OI2C] | 例外とstatusのどちらかをRuby契約として明示し、黙って変更しない |
| receiverと値 | class receiverやinstanceの検査、owned/borrowed returnをhelperに分ける。[登録][BREG]・[instance][BRECEIVER]・[helper][BNATIVE] | keywordをCで取得してbackendへ渡す例がある。[LED][OLED] | helper名で所有権を示す。実例の検査範囲をそのまま十分だとみなさない |
| 長い処理 | ADCのstart/poll/finish、lease、identity検査とRuby wrapperのsleep/ensure。[lease][BLEASE]・[wrapper][BADCWRAP] | Ruby slotがreload要求を見て終了する。[slot][OSLOT1] | native処理は短くし、取消し後や古いrequestの再利用を契約化する |
| event配送 | bounded queue、coalescing、overflow counterをforegroundで回収。lockはruntime wrapper側。[queue][BEVENT]・[IRQ保護][BEVENTIRQ]・[service][BSERVICE] | HALがidle/output等をportへ接続。[HAL][OHAL]・[output][OWRITE] | VM値をISRで作らず、通知queueの容量・同期・overflow方針を決める |
| reload | lease解除等の明示的なservice処理を持つ。[service][BSERVICE] | run終了後にtimer停止、API状態の初期化、cleanupを行い、外側loopでpool/bytecodeを用意して再初期化・再登録する。[reload][ORELOAD]・[VM loop][OVM] | 実行中bufferの上書きではなく、全利用者停止と資源整理を先に行う |
| Symbolの対応 | GPIOはIntegerの範囲、Stringのpin表記、Symbolのbackend label lookupを分けて扱う。[pin変換][BPIN] | led1/led2/led3、sw1〜sw4を登録してID表に保持。LED側は対応IDをGPIO出力へ結び付ける。[Symbol表][OSYMBOL]・[写像][OLEDMAP] | 文字列をその都度解釈せず、許可Symbol集合とnative対象の対応を契約にする |
| boolの受渡し | 引数・例外・owned/borrowedの境界を共通helperに置く。[helper][BNATIVE] | TRUE/FALSEのtagからC boolへ変換する専用helperを使う。[bool][OBOOL] | strict boolとRubyのtruthinessを区別し、受理する値を決める |
| 数値と範囲 | 共有helperでInteger型とstatusを扱う。[helper][BNATIVE] | PWM bindingは数値を周波数・dutyのC引数へ渡し、driver側はduty上限100を確認する。[binding][OPWM]・[driver][OPWMDRV] | Ruby側の単位・出力C型・物理範囲を分けて表す。採用先ではcast前の検査を契約化する |
| Array / String | 値の返却はowned/borrowed helperで区別。[helper][BNATIVE] | sampleはStringの長さ・終端と固定buffer、Arrayの要素数・要素読出しを使う。別sampleはFloat配列を生成して返す。[入力例][OVALUEIN]・[生成例][OVALUEOUT] | 長さ、要素型、byte/文字、NUL、コピーと借用の寿命を個別に決める |
| keywordと戻り値 | temperatureはbackendより前にkeyword終了を検査。[修正版][BFIXKW] | LEDはpart/stateをkeywordとして受け取りboolを返す。I2C readはstatusとdataを並べたArrayを返す。[keyword][OLED]・[I2C][OI2C] | keyword名・default・戻り値のshapeをRuby契約へ記載する。後始末の一般形は[API契約表](api.md#keywordの失敗経路と後始末)に従う |

## 履歴からの確認項目

RBOSのtemperature bindingは、親版では未知keywordの終了検査がなく、修正版でbackend呼出し前の`MRBC_KW_END()`が追加されています。argcが正しくても未知keywordを拒否できるとは限らないため、fixtureで個別に検査します。これは両版の静的diffの確認であり、過去版の動作を再実行した結果ではありません。[親版][BOLDKW]・[修正版][BFIXKW]
owned/borrowed helperとADC leaseの導入も履歴で確認できます。全製品や全版の安全性を保証する修正とは扱いません。[helper導入][BHISTHELP]・[lease導入][BHISTLEASE]

## 帰属

- RBOS: `bce986210380785fc89474f53c3b4e80ea9aed33`、BSD-3-Clause、Copyright (c) 2026, Y.Yamashiro。[LICENSE][BLICENSE]
- OpenBlink/openblink-demo-mdbt50q-db-40: `d6efc07877ebac6bd55519b8458be4629bef80c3`、BSD-3-Clause、Copyright (c) 2025 ViXion Inc. All Rights Reserved.。[LICENSE][OLICENSE]

上記は出所を付けた独自の要約・比較で、製品のbindingコードはコピーしていません。各製品のboard、build、認証等の固有条件は移植対象に含めません。

[BREG]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/bindings.c#L6-L40
[BBACKEND]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/include/rbos/backend.h#L7-L50
[OLED]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/api/led.c#L39-L95
[BNATIVE]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/native.c#L3-L62
[BRECEIVER]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/adc_binding.c#L23-L57
[BLEASE]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/adc_binding.c#L71-L151
[BADCWRAP]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/adc.rb#L1-L24
[BEVENT]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/event_queue.c#L3-L43
[BEVENTIRQ]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/firmware/src/runtime.c#L25-L50
[BSERVICE]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/adc_binding.c#L8-L21
[OHAL]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/lib/mrubyc/hal.c#L21-L54
[OWRITE]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/lib/mrubyc/hal.c#L87-L107
[ORELOAD]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/app/mrubyc_vm.c#L91-L109
[OVM]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/app/mrubyc_vm.c#L121-L189
[BOLDKW]: https://github.com/uist1idrju3i/RBOS/blob/b92c4d2d8a62474e2e6f1c35f49a543d24fddf36/src/rbos/bindings.c#L8-L19
[BFIXKW]: https://github.com/uist1idrju3i/RBOS/blob/5370890caeab8c241670729963cc9d13f0666f21/src/rbos/bindings.c#L8-L20
[BHISTHELP]: https://github.com/uist1idrju3i/RBOS/blob/b4ee26c1c91931b160b6932a4109bf6d701dd45b/src/rbos/native.c#L44-L55
[BHISTLEASE]: https://github.com/uist1idrju3i/RBOS/blob/1f815eb981e85b28f4ba391d9775575a1abf57ac/src/rbos/adc_binding.c#L71-L103
[BLICENSE]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/LICENSE#L1-L28
[OLICENSE]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/LICENSE#L1-L28
[OSYMBOL]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/api/symbol.c#L18-L93
[BPIN]: https://github.com/uist1idrju3i/RBOS/blob/bce986210380785fc89474f53c3b4e80ea9aed33/src/rbos/gpio_binding.c#L20-L51
[OLEDMAP]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/api/led.c#L78-L94
[OBOOL]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/api/api.c#L22-L37
[OPWM]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/api/pwm.c#L39-L54
[OPWMDRV]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/drv/pwm.c#L25-L48
[OVALUEIN]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/api/blink.c#L80-L137
[OVALUEOUT]: https://github.com/OpenBlink/openblink-demo-mdbt50q-db-40/blob/d6efc07877ebac6bd55519b8458be4629bef80c3/src/api/blink.c#L139-L156
