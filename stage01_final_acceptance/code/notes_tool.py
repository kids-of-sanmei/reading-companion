"""笔记资料整理工具 — 扫描、摘要、导出、统计 Markdown 和 TXT 文件。"""

import argparse
import json
import sys
from pathlib import Path


def collect_files(target_dir: Path) -> list[Path]:
    """扫描目录，返回所有 .md 和 .txt 文件的排序列表。"""
    if not target_dir.exists():
        print(f"错误：目录不存在 — {target_dir}")
        print("请确认路径是否正确，例如：python notes_tool.py scan ./samples")
        sys.exit(1)
    if not target_dir.is_dir():
        print(f"错误：路径不是目录 — {target_dir}")
        print("请传入一个目录路径，例如：python notes_tool.py scan ./samples")
        sys.exit(1)

    md_files = sorted(target_dir.glob("*.md"))
    txt_files = sorted(target_dir.glob("*.txt"))
    all_files = md_files + txt_files
    return all_files


def summarize_file(filepath: Path, base_dir: Path) -> dict:
    """读取单个文件，返回摘要字典。"""
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()
    return {
        "name": filepath.name,
        "path": str(filepath.relative_to(base_dir)),
        "lines": len(lines),
        "chars": len(content),
        "preview": content[:80],
    }


def export_json(results: dict, output_path: Path) -> None:
    """将结果写入 JSON 文件。"""
    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"已导出到 {output_path}")


def print_stats(json_path: Path) -> None:
    """读取 export 生成的 JSON 并打印统计信息。"""
    if not json_path.exists():
        print(f"错误：JSON 文件不存在 — {json_path}")
        print("请先运行 export 命令生成 JSON 文件，例如：")
        print("  python notes_tool.py export ./samples output.json")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误：JSON 文件无法解析 — {json_path}")
        print(f"详情：{e}")
        print("请确认文件是合法 JSON，或重新运行 export 生成。")
        sys.exit(1)

    files = data.get("files", [])
    file_count = len(files)
    total_lines = sum(f["lines"] for f in files)
    total_chars = sum(f["chars"] for f in files)

    largest = None
    if files:
        largest = max(files, key=lambda f: f["chars"])

    print(f"文件数量：{file_count}")
    print(f"总行数：{total_lines}")
    print(f"总字符数：{total_chars}")
    if largest:
        print(f"字符数最多的文件：{largest['name']}（{largest['chars']} 字符）")
    else:
        print("没有文件数据。")


def cmd_scan(args: argparse.Namespace) -> None:
    target = Path(args.directory).resolve()
    files = collect_files(target)

    if not files:
        print(f"提示：目录 {target} 中没有找到 .md 或 .txt 文件。")
        return

    print(f"扫描目录：{target}")
    for f in files:
        print(f"  {f.name}")


def cmd_summary(args: argparse.Namespace) -> None:
    target = Path(args.directory).resolve()
    files = collect_files(target)

    if not files:
        print(f"提示：目录 {target} 中没有找到 .md 或 .txt 文件。")
        return

    print(f"摘要目录：{target}\n")
    for f in files:
        info = summarize_file(f, target)
        print(f"文件：{info['name']}")
        print(f"  行数：{info['lines']}")
        print(f"  字符数：{info['chars']}")
        print(f"  预览：{info['preview'][:80]}")
        print()


def cmd_export(args: argparse.Namespace) -> None:
    target = Path(args.directory).resolve()
    files = collect_files(target)

    if not files:
        print(f"提示：目录 {target} 中没有找到 .md 或 .txt 文件，将生成空结果。")

    results = {
        "source_dir": str(target),
        "file_count": len(files),
        "files": [summarize_file(f, target) for f in files],
    }

    output_path = Path(args.output)
    export_json(results, output_path)


def cmd_stats(args: argparse.Namespace) -> None:
    print_stats(Path(args.json_file).resolve())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="笔记资料整理工具 — 扫描、摘要、导出、统计",
    )
    subparsers = parser.add_subparsers(dest="commnad", help="可用命令")

    # scan
    sp_scan = subparsers.add_parser("scan", help="扫描目录下的 .md 和 .txt 文件")
    sp_scan.add_argument("directory", help="要扫描的目录路径")

    # summary
    sp_summary = subparsers.add_parser("summary", help="读取并摘要每个文件")
    sp_summary.add_argument("directory", help="要摘要的目录路径")

    # export
    sp_export = subparsers.add_parser("export", help="将摘要导出为 JSON")
    sp_export.add_argument("directory", help="要扫描的目录路径")
    sp_export.add_argument("output", help="输出的 JSON 文件路径")

    # stats
    sp_stats = subparsers.add_parser("stats", help="从 JSON 文件读取统计信息")
    sp_stats.add_argument("json_file", help="export 生成的 JSON 文件路径")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    commands = {
        "scan": cmd_scan,
        "summary": cmd_summary,
        "export": cmd_export,
        "stats": cmd_stats,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
