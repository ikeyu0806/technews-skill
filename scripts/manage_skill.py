#!/usr/bin/env python3
"""Sync repository entry points or export a standalone technews skill."""

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "technews"
ENTRY_ROOTS = (".agents", ".claude", ".cursor")


def canonical_text(root):
    text = (root / "docs/skills/technews.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("正本に YAML frontmatter がありません")
    header, separator, body = text[4:].partition("\n---\n")
    if not separator or not body.strip():
        raise ValueError("正本の frontmatter または本文が不完全です")
    if "name: technews" not in header.splitlines():
        raise ValueError("正本の name は technews にしてください")
    if not any(line.startswith("description: ") for line in header.splitlines()):
        raise ValueError("正本に description がありません")
    return text, header


def entry_text(root):
    _, header = canonical_text(root)
    return (
        "---\n" + header + "\n---\n\n# Technews\n\n"
        "リポジトリの [docs/skills/technews.md](../../../docs/skills/technews.md) "
        "を全文読み、そこに従う。手順と参照資料の正本は `docs/skills/` に置き、"
        "このファイルには複製しない。\n"
    )


def bundle_files(root):
    text, _ = canonical_text(root)
    files = {Path("SKILL.md"): text.encode("utf-8")}
    references = root / "docs/skills/references"
    for path in sorted(references.rglob("*")):
        if path.is_file():
            files[Path("references") / path.relative_to(references)] = path.read_bytes()
    for required in (Path("references/sources.md"), Path("references/output-format.md")):
        if required not in files:
            raise ValueError("参照資料がありません: " + str(required))
    return files


def sync_entries(root, check=False):
    # Read all bundle inputs first so missing references never produce new entries.
    bundle_files(root)
    expected = entry_text(root)
    changed = []
    paths = [root / entry / "skills" / SKILL_NAME / "SKILL.md" for entry in ENTRY_ROOTS]
    for path in paths:
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError("同期先のスキルや入口がシンボリックリンクです: " + str(path))
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            changed.append(path)
    if check:
        if changed:
            for path in changed:
                print("未同期: " + str(path.relative_to(root)), file=sys.stderr)
            return 1
        print("3ツールの入口と参照資料を確認しました")
        return 0
    for path in changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8")
        print("同期: " + str(path.relative_to(root)))
    return 0


def export_skill(root, output, overwrite=False):
    files = bundle_files(root)
    output = output.expanduser().absolute()
    if output.is_symlink():
        raise ValueError("書き出し先自体がシンボリックリンクです: " + str(output))
    resolved_output = output.resolve()
    for entry in ENTRY_ROOTS:
        if resolved_output == (root / entry / "skills" / SKILL_NAME).resolve():
            raise ValueError("このリポジトリの入口へは書き出せません。sync を使ってください")
    if output.exists() and not output.is_dir():
        raise ValueError("書き出し先はディレクトリにしてください: " + str(output))

    # Preflight every destination before writing anything; preserve unrelated files.
    conflicts = []
    for relative, content in files.items():
        destination = output / relative
        for parent in destination.parents:
            if parent == output:
                break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise ValueError("書き出し先の親ディレクトリが不正です: " + str(parent))
        if destination.is_symlink():
            raise ValueError("書き出し先のファイルがシンボリックリンクです: " + str(destination))
        if destination.exists():
            if not destination.is_file():
                raise ValueError("書き出し先にファイル以外が存在します: " + str(destination))
            if destination.read_bytes() != content and not overwrite:
                conflicts.append(str(relative))
    if conflicts:
        raise ValueError(
            "既存ファイルと内容が異なります: " + ", ".join(conflicts)
            + "。確認後に --overwrite を指定してください"
        )

    for relative, content in files.items():
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or destination.read_bytes() != content:
            destination.write_bytes(content)
    print("単独スキルを書き出しました: " + str(output))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    sync = commands.add_parser("sync", help="3ツールの入口を正本に同期")
    sync.add_argument("--check", action="store_true", help="書き込まずに一致を確認")
    export = commands.add_parser("export", help="正本と参照資料を単独スキルに書き出す")
    export.add_argument("--output", type=Path, required=True, help="スキルディレクトリの出力先")
    export.add_argument("--overwrite", action="store_true", help="内容の異なる既存の管理対象ファイルを更新")
    args = parser.parse_args(argv)
    try:
        if args.command == "sync":
            return sync_entries(REPO_ROOT, check=args.check)
        return export_skill(REPO_ROOT, args.output, overwrite=args.overwrite)
    except (OSError, ValueError) as error:
        print("エラー: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
