from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_SOURCE = Path("sample_docs/long_note.md")
DEFAULT_OUTPUT = Path("chunks.jsonl")


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {path}")
    return path.read_text(encoding="utf-8")


def split_paragraphs(text: str) -> list[str]:
    parts = [part.strip() for part in text.split("\n\n")]
    return [part for part in parts if part]


def chunk_text(text: str, source_path: Path, chunk_size: int, overlap: int) -> list[dict[str, object]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    paragraphs = split_paragraphs(text)
    chunks: list[dict[str, object]] = []
    cursor = 0

    for paragraph in paragraphs:
        start = text.find(paragraph, cursor)
        if start == -1:
            start = cursor
        cursor = start + len(paragraph)

        window_start = 0
        while window_start < len(paragraph):
            window_end = min(window_start + chunk_size, len(paragraph))
            chunk_body = paragraph[window_start:window_end].strip()
            if chunk_body:
                chunks.append(
                    {
                        "chunk_id": f"chunk_{len(chunks) + 1:03d}",
                        "source": str(source_path),
                        "start_char": start + window_start,
                        "end_char": start + window_end,
                        "text": chunk_body,
                    }
                )
            if window_end == len(paragraph):
                break
            window_start = window_end - overlap

    return chunks


def write_jsonl(chunks: list[dict[str, object]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a Markdown document into JSONL chunks.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Source Markdown or text file.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output JSONL file.")
    parser.add_argument("--chunk-size", type=int, default=240, help="Maximum characters per chunk.")
    parser.add_argument("--overlap", type=int, default=50, help="Overlapping characters between chunks.")
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output)
    text = read_text(source_path)
    chunks = chunk_text(text, source_path=source_path, chunk_size=args.chunk_size, overlap=args.overlap)
    write_jsonl(chunks, output_path)

    print(f"source: {source_path}")
    print(f"output: {output_path}")
    print(f"chunk_size: {args.chunk_size}")
    print(f"overlap: {args.overlap}")
    print(f"chunks: {len(chunks)}")


if __name__ == "__main__":
    main()
