# Reference-AI-Skills

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/uist1idrju3i/Reference-AI-Skills)

## 目的

AIエージェントと人間が使う規約、スキル、検査、依存の更新監視を、新しいリポジトリへ導入するためのテンプレートです。製品固有の設計や判断は導入先で決めます。

説明文書はこのREADMEだけにまとめます。`AGENTS.md`は規約、`SKILL.md`は手順です。このリポジトリには`docs/`を作りません。`research-record`の`docs/`保存手順は導入先向けで、配置規約と衝突する場合は先に判断を求めます。

## テンプレートとして使う

1. 導入先のコード、既存規約、CI、文書の配置を深く調べます。`template-adoption`に沿って導入計画を作り、統治文書の追加についてユーザーの承認を得ます。
2. 作業ブランチで`AGENTS.md`の1〜12節をコピーし、13節と確認コマンドを導入先に合わせます。`CLAUDE.md`は`@AGENTS.md`だけにし、個人設定の除外を`.gitignore`へ反映します。
3. `vendor-update`で最新安定タグ、変更履歴、ライセンス、スキルの実在を再確認します。採用版をshallow submoduleとして追加し、相対リンクと自作スキルを配置します。固定版を無条件に使い回しません。
4. 検査器、テスト、CI、Dependabot、actionlint設定を導入先に合わせます。READMEのスキル表を同期し、`deepwiki-config`で導入先を調べてWiki設定を設計します。
5. 日本語を推敲して検査を実行し、未確認事項を報告します。Template repository設定、マージ、Wiki再生成は別の操作です。GitHubのテンプレート利用やcloneだけで導入完了にはなりません。

このリポジトリを取得するときは、GitとPython 3.10以降を用意し、clone後に次を実行します。

```sh
git submodule update --init --depth 1
```

## ディレクトリ構成

```text
AGENTS.md                       共通規約と、このリポジトリ固有の規約
CLAUDE.md                       AGENTS.mdへの参照
README.md                       使い方と唯一のスキル一覧表
.agents/skills/<name>/           自作スキル、またはvendorへのリンク
.claude/skills/<name>            .agents/skillsへのリンク
vendor/                         タグのcommitで固定した外部submodule
.gitmodules                     出所、shallow指定、固定タグ、監視接頭辞
.devin/wiki.json                DeepWikiのページとノート
.github/scripts/                スキル・Wiki検査、タグ更新監視
.github/workflows/              検査CIと更新通知
.github/dependabot.yml          Actions・pip・submoduleの更新設定
.github/actionlint.yaml         検査器がまだ認識しないGA runnerラベル
.github/zizmor-requirements.txt  ハッシュ固定の監査ツール
.github/pull_request_template.md PRの変更・理由・検証・リスク欄
tests/                          検査器と通知処理の負例・mockテスト
```

## スキル一覧

| スキル | 種類 | 出典と固定版 | ライセンス | 使う場面 |
|---|---|---|---|---|
| [`github-actions-ci`](.agents/skills/github-actions-ci/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | 最新安定版を確認して安全なCIを高速化する |
| [`vendor-update`](.agents/skills/vendor-update/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | 依存の変更履歴・回帰・新機能を確認する |
| [`document-structure`](.agents/skills/document-structure/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | 文書を意味と内容で整理する |
| [`code-structure`](.agents/skills/code-structure/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | コードを機能と責務で整理する |
| [`docs-code-sync`](.agents/skills/docs-code-sync/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | コードを正として文書の更新を計画する |
| [`deepwiki-config`](.agents/skills/deepwiki-config/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | コードを調べWikiのページとノートを設計する |
| [`research-record`](.agents/skills/research-record/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | 導入先のdocs/へ調査・検討・検証を残す |
| [`decision-request`](.agents/skills/decision-request/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | 推奨案を添えて不明点や改善案の判断を求める |
| [`session-retrospective`](.agents/skills/session-retrospective/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | セッション全体を振り返り改善を提案する |
| [`template-adoption`](.agents/skills/template-adoption/SKILL.md) | 自作 | 本リポジトリ | BSD-3-Clause | 深い計画と承認を経て別のリポジトリへ導入する |
| [`grill-with-docs`](.agents/skills/grill-with-docs/SKILL.md) | 外部 | mattpocock/skills v1.3.2 | MIT | 質問で計画と用語を詰める |
| [`grilling`](.agents/skills/grilling/SKILL.md) | 外部 | mattpocock/skills v1.3.2 | MIT | 計画の前提と判断を問い直す |
| [`domain-modeling`](.agents/skills/domain-modeling/SKILL.md) | 外部 | mattpocock/skills v1.3.2 | MIT | 用語と概念の境界を整理する |
| [`wayfinder`](.agents/skills/wayfinder/SKILL.md) | 外部 | mattpocock/skills v1.3.2 | MIT | 大きな不確実性を判断課題に分ける |
| [`handoff`](.agents/skills/handoff/SKILL.md) | 外部 | mattpocock/skills v1.3.2 | MIT | 次の担当へ前提と残件を渡す |
| [`research`](.agents/skills/research/SKILL.md) | 外部 | mattpocock/skills v1.3.2 | MIT | 一次資料を調べ根拠を記録する |
| [`prototype`](.agents/skills/prototype/SKILL.md) | 外部 | mattpocock/skills v1.3.2 | MIT | 捨てられる試作で問いに答える |
| [`source-driven-development`](.agents/skills/source-driven-development/SKILL.md) | 外部 | addyosmani/agent-skills 0.6.16 | MIT | 対象版の公式資料に沿って実装する |
| [`yomiyasu`](.agents/skills/yomiyasu/SKILL.md) | 外部 | nanaism/yomiyasu v3.1.0 | MIT、Unicode-3.0（同梱データ） | 意味を保って日本語を推敲する |
| [`context7-mcp`](.agents/skills/context7-mcp/SKILL.md) | 外部 | upstash/context7 mcpb-v4.7.0 | MIT | 対象版のライブラリ資料を取得する |
| [`analytical-thinking`](.agents/skills/analytical-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 要因と仮説を分解して分析する |
| [`creative-thinking`](.agents/skills/creative-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 多様な案を出して組み合わせる |
| [`critical-thinking`](.agents/skills/critical-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 主張と根拠の弱点を検討する |
| [`design-thinking`](.agents/skills/design-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 利用者の課題から試作を考える |
| [`ethical-thinking`](.agents/skills/ethical-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 関係者への影響と公平性を検討する |
| [`fermi-estimation`](.agents/skills/fermi-estimation/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 不確かな量を分解して概算する |
| [`first-principles-thinking`](.agents/skills/first-principles-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 前提を問い基礎条件から組み立てる |
| [`five-whys`](.agents/skills/five-whys/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 根拠をたどって再発原因を探る |
| [`lateral-thinking`](.agents/skills/lateral-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 発想の枠を変えて別案を探る |
| [`pre-mortem`](.agents/skills/pre-mortem/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 失敗を仮定して対策を考える |
| [`prioritization`](.agents/skills/prioritization/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 制約下で取り組む順序を決める |
| [`six-thinking-hats`](.agents/skills/six-thinking-hats/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 事実・感情・危険・利点・案を分ける |
| [`strategic-thinking`](.agents/skills/strategic-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 方向と集中する選択肢を決める |
| [`swot-analysis`](.agents/skills/swot-analysis/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 内外の条件を整理して行動を選ぶ |
| [`systems-thinking`](.agents/skills/systems-thinking/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 相互作用と循環から問題を捉える |
| [`thinking-method-selector`](.agents/skills/thinking-method-selector/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 問いに合う思考法を選んで使う |
| [`tradeoff-analysis`](.agents/skills/tradeoff-analysis/SKILL.md) | 外部 | ysskrishna/ai-agent-skills v1.5.4 | MIT | 評価軸と感度から選択肢を比較する |
| [`mfg-improvement-frameworks`](.agents/skills/mfg-improvement-frameworks/SKILL.md) | 外部 | yutut-app/mfg-kaizen-skills v1.11.0 | 不明（LICENSEなし、転載・再配布の許諾未確認） | 品質改善の手法と根拠を整理する |

## 外部スキルの前提と注意

- `context7-mcp`はContext7 MCPサーバーへの接続が必要です。このテンプレートはサーバー接続や認証情報を設定しません。
- `wayfinder`は意思決定を整理する計画用スキルです。利用する課題管理の方式を指定する前提があり、未指定時にはセットアップ手順の案内やlocal-markdown trackerへのフォールバックがあります。追加のセットアップ用スキルは同梱していません。READMEだけを文書にする本リポジトリでは、Markdown資料の追加やIssue作成を始める前に配置と権限を確認します。
- `handoff`は会話の引き継ぎ資料をOSの一時ディレクトリへ保存する前提です。次のセッションまで残す必要がある環境では、永続的な保存先を先に決めます。秘密を除き、既存成果物は複製せず参照します。
- `grill-with-docs`は`grilling`と`domain-modeling`を呼び出すため、3件をそろえて使います。ADRや用語集を作る前に導入先の配置規約を確認します。
- `research`と`prototype`も含めています。上流が提案するファイル作成、破棄可能な試作、外部操作は、導入先の規約と承認範囲に従います。スキルの記述は操作の許可ではありません。
- `mfg-improvement-frameworks`は採用していますが、上流にLICENSEがなく、転載・再配布の許諾は未確認です。商用利用や再配布の可否を推定せず、用途ごとに権利者へ確認してください。

## 依存の監視と更新

Dependabotは週次でGitHub Actionsとpipのzizmorを更新します。gitsubmoduleも対象ですが、タグで固定した6件はignoreしています。将来追加するbranch追従のsubmoduleは、個別に除外しなければ対象になります。

固定タグは`.gitmodules`の`pinned-tag`を正本とし、`tag-prefix`で安定版の監視系列を限定します。Context7は`mcpb-v`系列です。タグ固定を意図せずbranch先端へ動かさないため、`vendor-release-watch`が週次・手動でreleaseとtagを照会し、新版候補があればsubmoduleごとの日本語Issueを作成・更新します。自動更新や自動closeはしません。

通知後は`vendor-update`で更新範囲の変更履歴を深く読み、回帰検査と有用な新機能の採否を確認してから更新します。APIエラー時は検知成功と扱わず失敗します。既定と`--dry-run`は書き込みなしで、`--write`だけがこのリポジトリのIssueを書き換えます。

## 検査とコマンド

自前の検査スクリプトとテストはPython標準ライブラリだけで動きます。更新監視には認証済みのGitHub CLI（`gh`）も必要です。actionlintとzizmorの採用版・取得元・hashは`.github/workflows/agent-docs.yml`とrequirementsを参照してください。zizmorのrequirementsはCIと同じLinux x86_64用wheelを固定しています。

```sh
python3 .github/scripts/check-skills.py
python3 .github/scripts/check-wiki.py
python3 -m unittest discover -s tests/check-skills
python3 -m unittest discover -s tests/check-wiki
python3 -m unittest discover -s tests/vendor-release-watch
python3 .github/scripts/vendor_release_watch.py --dry-run
actionlint .github/workflows/*.yml
python3 -m pip install --require-hashes --only-binary=:all: -r .github/zizmor-requirements.txt
zizmor --offline .github/workflows
git diff --check
```

CIはPRとmainへのpushで起動し、pathsによる絞り込みをしません。スキル、Wiki、ワークフローの3jobを並列実行し、古いPR実行は中止します。スキルjobはsubmoduleを浅く取得し、Wiki jobでは更新監視のmockテストも実行します。

日本語の候補検査には`python3 .agents/skills/yomiyasu/scripts/yomiyasu_lint.py <file>`を使います。隠しディレクトリ内のファイルは、その親を作業フォルダにしてファイル名を渡してください。指摘は自動的な不合格や意味保持の保証ではありません。修正前後の照合と通読も必要です。

DeepWiki設定は`deepwiki-config`に従って設計します。[公式仕様](https://docs.devin.ai/work-with-devin/deepwiki)の上限を再確認し、設定のcommitと実際のWiki再生成は区別してください。

### Windowsのシンボリックリンク

clone時に`git -c core.symlinks=true clone <repository-url>`を使い、開発者モードまたはリンク作成に必要な権限を有効にします。既存のcloneでは`git config core.symlinks true`だけでは通常ファイルとして取得済みのリンクは復元されません。未保存の変更を保全して取得し直すなど、リンクの実体を確認してください。

## ライセンス

本リポジトリの規約、自作スキル、検査コードは[LICENSE](LICENSE)のBSD 3-Clause Licenseに従います。外部submoduleはそれぞれの利用条件に従い、ルートのLICENSEで一括して許諾されるわけではありません。上の一覧は固定版の表示であり、ライセンス不明の資材への許諾を意味しません。
