# スキル（Codex / Claude Code / Cursor 共通）

このフォルダが手順の正本です。ツール別の `SKILL.md` は正本を読むための入口だけを持ちます。

| ファイル | 役割 | 読むタイミング |
| --- | --- | --- |
| [technews.md](technews.md) | 国内外のテック情報を収集・検証・要約する | スキル実行時 |
| [references/sources.md](references/sources.md) | 分野別の情報源、人物発言の探索先、新しい情報源の選び方 | 収集先を選ぶとき |
| [references/output-format.md](references/output-format.md) | 日付、要約、反応の根拠、リンクを含む出力例 | ダイジェストを編集するとき |

`technews.md` の frontmatter を変更したら、`python3 scripts/manage_skill.py sync` で3つの入口へ反映します。
