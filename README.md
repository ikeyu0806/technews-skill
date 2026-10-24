# technews-skill

国内外の「いま面白いテック情報」を、参照リンク付きで日本語にまとめる Agent Skill です。人気記事、開発者の実録、業界人物の発言、作品・デモ、面白いサービス、研究、重要なリリースを収集します。

AI・Web／アプリ開発に加え、Blender、ゲーム開発、VR／AR／MR、ガジェット、電子工作、フィジカルAIを扱います。ゲームエンジンやプラットフォームは限定しません。

## このリポジトリで使う

このディレクトリを各ツールの作業ディレクトリとして開いてください。

| ツール | 検出する入口 | 明示的な呼び出し |
| --- | --- | --- |
| Codex | `.agents/skills/technews/SKILL.md` | `$technews` |
| Claude Code | `.claude/skills/technews/SKILL.md` | `/technews` |
| Cursor | `.cursor/skills/technews/SKILL.md` | `/` メニューから `technews` を選択 |

```text
国内外で話題になっているテック情報を10件集めて。
人気記事や有名人の発言も含め、ゲーム開発、VR、ガジェット、フィジカルAIも拾って。
内容の要約、話題性の根拠、元記事と議論へのリンクを日本語で教えて。
```

期間、件数、分野を指定できます。たとえば「直近1週間、海外中心、BlenderとXRを多めに」「直近24時間のHacker NewsとはてなITから5件」「ロボティクスで新しく注目されている研究やデモを探して」などです。

調査結果は会話内で届けるとともに、作業ディレクトリの `docs/research/YYYY-MM-DD.md` に記録します。同日に別の調査を行う場合は連番を付けます。保存先の変更や保存しない指定もできます。commit・pushは依頼があった場合に行います。

Web 検索・URL 取得が使えるセッションで実行してください。特定の検索プロバイダーや MCP は必須ではありません。Web アクセスが使えない場合は、その制約を伝え、最新ニュースを作り話で補わない手順になっています。

## ほかのプロジェクトでも使う

ツール別の入口はこのリポジトリの正本を参照するため、入口ファイルだけをコピーしないでください。書き出しコマンドは、正本と参照資料を含む単独スキルを生成します。Python 3.9 以上、追加ライブラリ不要です。

使いたいツールのコマンドを実行します。

```sh
# Codex のユーザースキル
python3 scripts/manage_skill.py export --output "$HOME/.agents/skills/technews"

# Claude Code のユーザースキル
python3 scripts/manage_skill.py export --output "$HOME/.claude/skills/technews"

# Cursor のユーザースキル
python3 scripts/manage_skill.py export --output "$HOME/.cursor/skills/technews"
```

別プロジェクトだけで使う場合は、書き出し先をそのプロジェクトの `.agents/skills/technews`、`.claude/skills/technews`、または `.cursor/skills/technews` にしてください。更新時に既存の内容と異なる場合は停止します。内容を確認して更新するには、同じコマンドに `--overwrite` を付けます。書き出し先の無関係なファイルは削除しません。

スキルが一覧に出ない場合は、セッションを開き直すか、ツールのスキル再読み込み機能を使ってください。複数の対応ディレクトリを検出するツールでは同名の入口が表示される場合があります。書き出し版は利用する入口を1つ選んで配置できます。

## 構成と変更方法

[threejs-worlds](https://github.com/ikeyu0806/threejs-worlds) の構成に合わせ、手順の正本とツール別の入口を分けています。

```text
AGENTS.md                         共通のプロジェクト指示
CLAUDE.md                         AGENTS.md を読み込む入口
docs/skills/
  technews.md                     スキル本文・メタデータの正本
  references/sources.md           分野別の情報源と人物の探索先
  references/output-format.md     要約の形式と話題性の示し方
docs/research/                    日付付きの調査記録
.agents/skills/technews/SKILL.md   Codex の入口
.claude/skills/technews/SKILL.md   Claude Code の入口
.cursor/skills/technews/SKILL.md   Cursor の入口
scripts/manage_skill.py           入口の同期・検証・単独スキルの書き出し
```

編集後は次を実行してください。

```sh
python3 scripts/manage_skill.py sync
python3 scripts/manage_skill.py sync --check
python3 -m unittest discover -s tests -v
git diff --check
```

配置と呼び出し方法は、[Codex公式ドキュメント](https://learn.chatgpt.com/docs/build-skills)、[Claude Code公式ドキュメント](https://code.claude.com/docs/en/skills)、[Cursor公式ドキュメント](https://cursor.com/docs/skills) を確認しています。プロジェクトスキルとローカルのユーザースキルの構成で、クラウドへの同期やプラグイン公開は行いません。
