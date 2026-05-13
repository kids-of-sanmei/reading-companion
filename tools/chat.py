from __future__ import annotations

import argparse

from core.agent import ReadingAssistant
from core.config import load_settings
from core.embeddings import build_embedder
from core.llm import ChatLLM
from core.memory import MemoryStore
from core.vector_store import MilvusBookStore


def build_assistant() -> ReadingAssistant:
    # 读取 .env 里的配置，比如 OpenAI key、Milvus 地址等。
    settings = load_settings()

    # embedder 负责把文字变成向量。
    # 向量可以理解成：让电脑比较“这两段话意思像不像”的数字表示。
    embedder = build_embedder(settings)

    # store 负责连接 Milvus，后面聊天时会用它检索书籍片段。
    store = MilvusBookStore(
        uri=settings.milvus_uri,
        token=settings.milvus_token,
        collection_name=settings.milvus_collection,
        dimension=embedder.dimension,
    )

    # 把配置、向量工具、Milvus、记忆、大模型拼装成一个完整助手。
    return ReadingAssistant(
        settings=settings,
        embedder=embedder,
        store=store,
        memory=MemoryStore(settings.memory_path),
        llm=ChatLLM(settings),
    )


def main() -> None:
    # argparse 用来读取命令行参数。
    # 例如：python -m tools.chat --book-title "原则"
    parser = argparse.ArgumentParser(description="Chat with your reading assistant.")
    parser.add_argument("--book-title", help="Limit retrieval to one book title.")
    parser.add_argument("--limit", type=int, default=5, help="Number of book chunks to retrieve.")
    args = parser.parse_args()

    assistant = build_assistant()
    print("Reading assistant is ready. Type 'exit' or 'quit' to stop.")
    while True:
        # input 会等待你在终端输入一句话。
        message = input("\nYou: ").strip()
        if message.lower() in {"exit", "quit"}:
            break
        if not message:
            continue

        # 这里是真正的一轮聊天：
        # 1. 把你的问题变成向量
        # 2. 去 Milvus 找相关书籍片段
        # 3. 把片段和记忆交给大模型
        # 4. 保存这轮对话为长期记忆
        reply = assistant.ask(message, book_title=args.book_title, limit=args.limit)
        print(f"\nAssistant:\n{reply.answer}")

        if reply.references:
            # 显示引用来源，方便你知道回答主要参考了哪些书籍片段。
            print("\nReferences:")
            for index, reference in enumerate(reply.references, start=1):
                print(
                    f"  [{index}] {reference.book_title} "
                    f"chunk={reference.chunk_index} score={reference.score:.4f}"
                )


if __name__ == "__main__":
    main()
