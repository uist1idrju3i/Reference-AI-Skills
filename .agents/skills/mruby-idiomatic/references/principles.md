# Rubyらしさの原則と出典

Matz（まつもとゆきひろ）氏のインタビュー、講演、日記、Issue での判断と、氏が書いた mruby の Ruby コードを読み、Rubyらしさを12の原則にまとめた。各原則は本スキルの解釈であり、発言の引用でも、氏の公式見解でもない。原文は出典表の URL で確かめる。

## 原則

| # | 原則 | コードでの表れ | 主な出典 |
|---|---|---|---|
| 1 | 機械の都合ではなく、人間（書き手と読み手）の労力を減らす | 利用者の語彙で method と引数を設計する。実装の都合をそのまま API にしない | A1, A4 |
| 2 | 簡潔さを目指すが、単純さや最短とは別物。後で読んで分かる保守性を損なう短縮はしない | 1行の guard は使い、複数条件や副作用を1行へ詰め込まない | J7, E1 |
| 3 | 名前は重要。振る舞いではなく意図を名付ける | `high?` のような問い合わせ名、単位付きの定数名、`?`・`!` の慣習 | J1, J2, E5 |
| 4 | 直交性より調和。機能の組合せで読み手が規則を推測しなければならない形を避ける | 排他的な引数や不正な組合せは入口で `ArgumentError` にし、暗黙の優先順位を作らない | A1 |
| 5 | 「驚き最小」は Ruby に習熟した人の基準。他言語の癖ではなく Ruby の慣習に合わせる（氏自身はこの原則を掲げていないと述べている） | `each`・`map`・`to_s`・`?`/`!`・`nil` の扱いを core の慣習にそろえる | A1 |
| 6 | block はループと手続きの抽象。反復や後始末の詳細は提供側が持ち、利用側は「何をするか」だけを書く | `each` を提供して Enumerable を活かす。資源は `open { }` 形式で `ensure` により解放する | A3 |
| 7 | 動的機能はライブラリが環境に適応するための道具で、日常のコードで多用しない | `method_missing`・`define_method`・再オープンを通常の設計に使わない | A2 |
| 8 | 書き方の多様性は合理的な場合だけ認め、混乱を招く多様性は求めない | 同じ処理に複数の書き方を混在させない。読み手が迷う新奇な構文を避ける | E7, E4 |
| 9 | 型注釈はコードに書かない。型は RBS などの別ファイルや推論で扱い、duck typing を保つ | クラス判定より、必要な method を呼べることを前提にする。型は `sig/` に置く | E2, E3, E6, E8, E9, J6 |
| 10 | 生産性は言語単体ではなく、ライブラリと開発者のモチベーションを含めて生まれる | 既存の標準 API（MPIG、core の method 名）に合わせ、利用者の学習量を減らす | J3, J4, J5 |
| 11 | Ruby の価値の多くは、昔からある強力な考えを普通の人に手が届く形で提供すること | 高度な抽象より、読み手が追える素直な構造を選ぶ | J8 |
| 12 | 小さいコンピュータ向けの Ruby はサブセット。制約を隠さず、別の処理系として扱う | mruby/c で使えない機能を CRuby の感覚で使わず、代替と理由を明示する | J9, J10, J11, J12 |

## Matz 氏のコードに見える書き方

mruby の `mrblib/` と `mrbgems/*/mrblib/`（git blame で Matz 氏が主著者の Array・Hash・Numeric・Range・String と enum-ext・array-ext・string-ext）、および氏が追加した周辺機器 gem の Ruby 部分（`mrbgems/hw-*/mrblib/`）から、次の型が読み取れる。参照版は mruby 4.1.0-rc2（`c17ffcc24190b71682bc611fa80053bb252ad482`、MIT）。

- 引数の検査は method の先頭で行い、`raise ArgumentError, "..." if 条件` の1行 guard で早期に失敗させる。
- block を省略した呼出しには `return to_enum(:name) unless block` で応じ、block 付きの経路を通常系として読み下せる形にする。
- 結果の Array は空で初期化し、`each` の中で `<<` して最後に返す。件数で止める処理は `break` で明示する。
- 単位は定数名とコメントで示す（例: `DEFAULT_FREQUENCY = 100_000 # Hz`）。数値 literal に `_` 区切りを使う。
- 設定系の method は `nil` または `self` を明示的に返し、戻り値の意味を曖昧にしない。
- 資源の確保と解放は block と `ensure` で対にする（例: SPI の chip select を `select { }` で囲み、例外時も解除する）。
- 内部用の native method は `__init` のような接頭辞で公開 API と区別し、公開 API は利用者の語彙で Ruby 側に薄く書く。
- 公開 method には `call-seq` 形式のコメントで呼出し形と戻り値を書く。

これらは mruby 本体のコードであり、mruby/c では `to_enum` や一部の構文が使えない。mruby/c での可否は [可否表](compatibility.md) で確かめる。

## 出典

日付が不明なものは「—」とした。取得日はすべて 2026-11-22。

| ID | 種別 | 日付 | 出典 |
|---|---|---|---|
| A1 | インタビュー（英） | 2003-09-29 | [The Philosophy of Ruby（Artima）](https://www.artima.com/articles/the-philosophy-of-ruby) |
| A2 | インタビュー（英） | 2003 | [Dynamic Productivity with Ruby（Artima）](https://www.artima.com/articles/dynamic-productivity-with-ruby) |
| A3 | インタビュー（英） | 2003 | [Blocks and Closures in Ruby（Artima）](https://www.artima.com/articles/blocks-and-closures-in-ruby) |
| A4 | インタビュー（英） | 2003-12-29 | [Matz on Craftsmanship（Artima）](https://www.artima.com/articles/matz-on-craftsmanship) |
| E1 | インタビュー（英） | 2012-01-23 | [gihyo.jp Software Designers #34](https://gihyo.jp/dev/serial/01/software_designers/0034) |
| E2 | Issue 判断 | — | [Feature #9999 Type Annotations](https://bugs.ruby-lang.org/issues/9999) |
| E3 | Issue 判断 | — | [Feature #17848 inline rbs](https://bugs.ruby-lang.org/issues/17848) |
| E4 | Issue 判断 | — | [Feature #15799 pipeline operator](https://bugs.ruby-lang.org/issues/15799) |
| E5 | Issue 判断 | — | [Feature #14594 Rethink yield_self's name](https://bugs.ruby-lang.org/issues/14594) |
| E6 | インタビュー（英） | 2019 | [Evrone interview](https://evrone.com/blog/yukihiro-matsumoto-interview) |
| E7 | メーリングリスト | 2010-11-24 | [ruby-talk: More than one way to do things](https://rubytalk.org/t/rubys-more-than-one-way-to-do-things/60944) |
| E8 | 対談（英） | 2016-11-10 | [Ruby 3x3（Heroku）](https://www.heroku.com/blog/ruby-3-by-3/) |
| E9 | 講演（英） | 2016-06-23 | [Keynote: Ruby Typing（RubyEvents）](https://www.rubyevents.org/talks/keynote-ruby-typing) |
| J1 | インタビュー | 2004-09-10 | [Rubyist Hotlinks 第1回](https://magazine.rubyist.net/articles/0001/0001-Hotlinks.html) |
| J2 | 日記 | 2004-06-28 | [Matzにっき 2004-06-28](https://matz.rubyist.net/20040628.html) |
| J3 | 講演記事 | 2022-09-28 | [Rubyの価値（Re:vent）](https://revent.8card.net/columns/f0jovotwc1) |
| J4 | 講演記事 | 2022-10-06 | [ベロシティの重要性（Re:vent）](https://revent.8card.net/columns/014rlivdnm) |
| J5 | 講演記事 | 2022-09-28 | [開発者のモチベーション（Re:vent）](https://revent.8card.net/columns/ucxvbslmzi) |
| J6 | 講演記事 | 2022-10-04 | [Rubyに型宣言を入れない理由（Re:vent）](https://revent.8card.net/columns/7bls5l96vg) |
| J7 | 講演記事 | — | [Rubyの未来（Re:vent）](https://revent.8card.net/columns/u3zmcwyion) |
| J8 | Podcast | 2013-03-13 | [Rebuild #5 Ruby 2.0](https://rebuild.fm/5/) |
| J9 | インタビュー | 2010-11-30 | [使う人をハッピーにする（TECH+）](https://news.mynavi.jp/techplus/article/20101130-matz/) |
| J10 | 講演記事 | 2022-11-01 | [mruby の特徴（Re:vent）](https://revent.8card.net/columns/eyfjrsvke0) |
| J11 | 講演記事 | — | [mruby/c の特徴（Re:vent）](https://revent.8card.net/columns/ugxkikzq6m) |
| J12 | インタビュー | 2014-02-24 | [mruby に挑戦（doda、Internet Archive）](https://web.archive.org/web/20240000000000/https://doda.jp/engineer/guide/yosoku/07_3.html) |

未確認: 『Beautiful Code』29章「Treating Code As an Essay」と『まつもとゆきひろ コードの世界』『言語のしくみ』は原文を確認していないため、根拠に使っていない。
