from __future__ import annotations

import argparse
from pathlib import Path

from core.chunking import build_book_chunks
from core.config import load_settings
from core.embeddings import build_embedder
from core.vector_store import MilvusBookStore, batched


def main() -> None:
    # 这个脚本负责“把一本书导入 Milvus”。
    # 使用方式示例：
    # python -m tools.ingest_book "books/example.pdf" --title "示例书"
    parser = argparse.ArgumentParser(description="Ingest a book into Milvus.")
    parser.add_argument("path", type=Path, help="Path to a PDF, TXT, or Markdown book.")
    parser.add_argument("--title", help="Book title. Defaults to the file name.")
    parser.add_argument("--chunk-size", type=int, default=1200)
    parser.add_argument("--overlap", type=int, default=180)
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()

    if not args.path.exists():
        raise FileNotFoundError(args.path)

    # 读取 .env 配置。
    settings = load_settings()

    # 准备文字转向量工具。
    embedder = build_embedder(settings)

    # 准备 Milvus 存储工具。
    store = MilvusBookStore(
        uri=settings.milvus_uri,
        token=settings.milvus_token,
        collection_name=settings.milvus_collection,
        dimension=embedder.dimension,
    )

    # 读取书籍文件，然后切成很多小段。
    # 大模型不适合一次读完整本书，所以需要切片。
    chunks = build_book_chunks(
        path=args.path,
        title=args.title,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    if not chunks:
        print("No text chunks were found.")
        return

    inserted = 0
    for batch in batched(chunks, args.batch_size):
        # 每一批切片先转成向量，再写入 Milvus。
        vectors = embedder.embed([chunk.text for chunk in batch])
        inserted += store.upsert_chunks(batch, vectors)
        print(f"Ingested {inserted}/{len(chunks)} chunks...")

    print(f"Done. Book '{chunks[0].book_title}' ingested with {inserted} chunks.")


if __name__ == "__main__":
    main()
