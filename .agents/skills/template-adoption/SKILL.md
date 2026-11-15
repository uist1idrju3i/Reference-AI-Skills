---
name: template-adoption
description: エージェント規約・スキル・検査基盤を別のリポジトリへ導入するときに、深い調査と計画を行いユーザー承認後に適用する。
---

# テンプレートの導入

1. 導入先の目的、コード、既存規約、スキル、CI、権限、文書の配置を深く調べる。統治文書を追加する作業として、採用・変更・除外、競合の解消方法、検証方法を深く計画し、ユーザー承認を得るまで変更しない。
2. 承認後に作業ブランチを作る。テンプレートの`AGENTS.md`の1〜12節をコピーし、13節を導入先の事実で書き直す。確認コマンドも導入先に合わせる。既存規約と黙って置換・矛盾させない。
3. `CLAUDE.md`を`@AGENTS.md`だけの参照にする。個人用設定、`AGENTS.override.md`、`.yomiyasu/`、`__pycache__/`などを`.gitignore`に反映し、既存の除外を保つ。
4. `vendor-update`で各submoduleの最新安定タグ、必要なスキルの実在、変更履歴、ライセンスを再確認する。古い固定値を無条件にコピーせず、承認した版をshallow submoduleとして追加し、タグ・監視系列を記録する。
5. 外部スキルは`.agents/skills/<name>`から`../../vendor/...`へリンクする。自作スキルは実ディレクトリに置き、どちらも`.claude/skills/<name>`から`../../.agents/skills/<name>`へリンクする。名前はfrontmatterと一致させ、固有の前提を除く。
6. 検査スクリプトと負例テスト、workflows、Dependabot、actionlint設定を導入先に合わせる。`github-actions-ci`で最新版・固定SHA・hash、runner、権限、キャッシュ、並列化を再確認する。固定タグ監視とbranch追従の対象を同期する。
7. READMEのスキル表へ全スキルを一度ずつ登録する。例として先頭列は「[`name`](.agents/skills/name/SKILL.md)」、種類は実ディレクトリなら自作、vendorへのリンクなら外部とする。出所・版・ライセンス・利用条件を示す。
8. `deepwiki-config`に従い、導入先を深く調べて`.devin/wiki.json`を新しく設計する。テンプレートの製品名・ページ・ノートを残さず、文書の配置規約も適用する。
9. 日本語をyomiyasuで推敲し、スキル・Wiki検査、全対象unittest、actionlint、zizmor、`git diff --check`を実行する。更新監視はdry-runで確かめ、外部書き込みは別途許可を得る。
10. 差分、ライセンス、個人設定の混入、CI結果を確認する。採否、検証、未確認を報告し、依頼されたcommit・pushだけを行う。Template repository設定、保護設定、マージ、Wiki再生成は別の操作として扱う。
