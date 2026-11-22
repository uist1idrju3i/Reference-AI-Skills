---
name: mruby-common-io-api-guidelines
description: mruby/c向けGPIO/ADC/PWM/UART/I2C/SPI Ruby APIを追加・変更するとき、MPIG準拠のために使う。標準と拡張、pin、資源、待機、例外の契約を決め、C bindingとfake backendで検証する。
---

# mruby/cのCommon I/O API

MPIGをAPI契約の基準にし、mrubyのhw-*を参考実装として分けます。mrubyのコードをそのまま移して適合したとは判定しません。

## 手順

1. MPIGのcommitを固定し、対象クラスのenとjaを両方読みます。[固定版の契約表](references/mpig.md)から原文へ進み、日英差や未規定の条件を記録します。異なる版を採用する場合は表を更新します。
2. 実装より先に、class/instance method、位置・keyword引数、alias、定数、default、単位、戻り値、例外、待機の契約表を書きます。未規定をnilや成功と解釈せず、「導入先が決める事項」として採用する動作を明記します。
3. 標準API、任意実装のmethod、独自拡張を分けます。追加keywordや便利method、非対応parameterを文書に示し、標準名の意味を変えません。[mruby 4.1.0-rc2との差分](references/mruby-hw.md)は移植時の注意であり、規格ではありません。
4. pinとunitの表現を別々に決めます。受理する型、同じ物理資源への解決、範囲、対応機能、予約済み資源、active-low、未知の名前を定義します。castより先に型と範囲を検査します。
5. 物理資源とbufferのowner、共有・busy、最大長、queue上限、timeout、cancel、部分転送、buffer寿命、releaseの契約を決めます。転送中やtask終了後の解放、取消し後に届く完了通知も含めます。
6. 一般的な登録・引数・所有権・例外は[mrubyc-c-binding](../mrubyc-c-binding/SKILL.md)で確認します。[周辺機器の待機設計](references/mrubyc-binding.md)に従い、開始・状態確認・完了を短い処理へ分け、sleepを挟むか非同期backendを使い、各C処理と待機全体に上限を設けます。
7. 周辺機器ISRは容量と処理時間を制限したflag/ring bufferへの通知にとどめます。VM呼出し、allocation/refcount、raise、一般のtask操作はforegroundで行います。専用HAL tickの経路と混同しません。
8. MPIGに明記されたエラーを保ちます。GPIOの必須方向なし、class write_atの範囲外、ADCのFloat無効時を落としません。型違い、未対応設定、busy、timeout等の未規定部分は例外と副作用を決めます。Cの例外処理は[mrubyc-c-bindingの契約](../mrubyc-c-binding/references/api.md#例外とcからの呼出し)に従います。
9. Ruby層は[mruby-idiomatic](../mruby-idiomatic/SKILL.md)に従い、対象版とvm_configで実行します。RBSを付ける場合も型を補う資料とし、単位・待機・例外・所有権の契約表の代わりにしません。
10. fake backendで受理した設定、転送byte、状態と完了順を観測できるようにし、下記を実行します。[最小GPIO例](scripts/gpio-example/)を出発点にできますが、そこで未検証の通信・待機・ISRを保証したとは扱いません。

## fakeで確認すること

- 通常・空・nil・型違い・範囲外・必須parameter不足と、対応する戻り値・例外を検査する。
- 失敗時に設定やbufferを壊さず、部分転送の件数とbyte列を保つことを検査する。
- I2CのSTART/repeated START/STOP、SPIのzero dummyとGPIO CS、UARTのwrite受付とflush完了の順序を検査する。
- busy、期限到達、cancel、遅延完了、queue満杯、buffer保持とreleaseを検査する。
- 待機中に別Ruby taskが進むことと、各C処理が決めた時間内に戻ることを検査する。
- compileだけでなく実行し、異常系の例外をfixture内で捕捉して種類と副作用をassertする。crashをエラー契約への適合としない。

## 完了確認

- 契約表、実装、標準と拡張の表示、fakeの期待値が一致している。
- 固定版・設定・再現コマンド・実行結果を残し、実機の電気特性や実効速度など未確認事項を分けて報告した。
- 日本語のyomiyasu、skill・link検査と対象テストを実行した。

## 帰属

MPIGはCC BY 4.0です。本スキルの契約要約・比較は翻案として[原資料・固定版・帰属・変更内容](references/mpig.md#帰属とライセンス)を示します。Copyright 2023のmruby forum committee、Kyushu Institute of Technology、Shimane IT Open-Innovation Centerへ帰属します。community libraryのコードは別の利用条件を確認してください。本スキルの独自コードはBSD-3-Clauseです。
