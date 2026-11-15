---
name: crc-polynomial
description: CRC多項式を選定・変更するときに、Koopmanの一次資料でデータ長・要求HD・誤りモデルに合う候補と表記を検証する。
---

# CRC多項式を根拠から選ぶ

1. 最大dataword長をbit単位で決め、CRCを足したcodeword長と区別する。要求HD、許容する未検出誤り率、CRC幅、計算・通信の制約を記録する。
2. 誤りモデルを確かめる。Koopmanの「Best」は低く一定のランダム・独立BERが前提。高BER（例：10万bitに1bitを超える）、非定常・相関・バースト等では表だけで決めず、モデルと検証を掘り下げる。
3. [公式サイト](https://users.ece.cmu.edu/~koopman/crc/)の現行値と取得日を毎回確認する。転載後に更新され得るため、同梱表だけで実装値を確定しない。[Best表](references/best-crcs.md)から長さとHDに合う候補を選び、[Selection索引](references/details.md)とHD3〜6・6sub8の表で副次特性も比較する。
4. Zooの[3〜16bit](references/zoo-03-16.md)・[17〜32bit](references/zoo-17-32.md)・[33〜64bit](references/zoo-33-64.md)で候補のHD長リスト、名称、gold、括弧情報、(*p)・(*o)・(*op)属性を照合する。意味は[Notation原文](references/notes.md)で確かめる。
5. 表記を混同しない。implicit +1の0x247はx^10+x^7+x^3+x^2+x+1で、explicit +1では0x48f。reversedの値も原文で照合し、実装のbit方向、幅、refin/refoutとの対応を確かめる。幅を省いた定数だけを渡さない。
6. (**)は暫定結果で、より長いHD保証長や同長で低い重みの候補が後から見つかり得る。?や>=、未掲載の表記を確定値へ補完しない。Selectionの「Published source anomalies」に挙げた原文の表記異常は勝手に修正せず、一次資料で解決するまで実装値に使わない。
7. 多項式の選択とCRC方式全体を分ける。初期値、xorout、反射、送信順を定め、既知のcheck値・テストベクトルと照合する。空入力、既知メッセージ、長さ境界も試し、用途に必要な誤り検出を検証する。
8. 選んだ多項式の全表記、幅、最大dataword長、要求HD、誤りモデル、初期値等、採否の理由、原文URL、取得日、検証結果と未確認事項を導入先の配置規約に従って残す。
9. 引用データはPhilip Koopman, Carnegie Mellon UniversityのCC BY 4.0。コピー時は著作者・出典URL・ライセンスURL・変更内容の表示を保つ。表はHTMLを整形した引用で、値を再計算していない。個別の重みデータファイルは取得しない。
10. スキルのルートで`python3 scripts/fetch_koopman.py`を実行するとオンラインで表を再生成する。最新HTMLとの照合は`--check`、保存HTMLとの照合は`--check --html-dir <保存先>`を付ける。再生成時の`--save-html-dir <保存先>`は原文をgzipで保存する。取得・解析・件数・一致検査の失敗を成功扱いせず、更新差分とオフラインのtests/crc-polynomial/を確認する。
