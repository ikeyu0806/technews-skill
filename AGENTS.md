# AGENTS.md

国内外のテック情報を調査する `technews` スキルを管理するリポジトリです。

Claude Code・Codex・Cursor 共通のプロジェクト指示は、このファイルを正本とします。

## スキルの配置

- 手順の正本: `docs/skills/technews.md`
- 情報源と出力例: `docs/skills/references/`
- ツール別の入口: `.agents/skills/technews/`、`.claude/skills/technews/`、`.cursor/skills/technews/`

情報収集を依頼されたら、正本を読んで実行してください。スキル自体の修正では、正本と関連する参照資料を編集し、入口に手順を複製しないでください。

## 変更の確認

正本のメタデータを変更したら、入口を同期します。

```sh
python3 scripts/manage_skill.py sync
python3 scripts/manage_skill.py sync --check
python3 -m unittest discover -s tests -v
git diff --check
```

実行環境で利用できる Web 検索・URL 取得機能を使うスキルです。特定の MCP、API キー、個人の絶対パスには依存させないでください。記事や反応数は実行時に取得し、過去の調査結果を最新情報として埋め込まないでください。

依頼と無関係な変更をコミットに混ぜず、push・公開・定期実行の設定は、それぞれユーザーから依頼があったときに行ってください。
