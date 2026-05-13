from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Settings 是整个项目的“配置盒子”。
# 它把 .env 里的配置统一读出来，后面其他文件就不用到处读环境变量。
@dataclass(frozen=True)
class Settings:
    # OpenAI API key，用来调用大模型和 embedding。
    openai_api_key: str
    # 如果你用的是兼容 OpenAI 的第三方服务，可以在这里填 base url。
    openai_base_url: str | None
    # 聊天模型名称。
    openai_chat_model: str
    # 向量来源：openai 或 local_hash。
    embedding_provider: str
    # OpenAI embedding 模型名称。
    openai_embedding_model: str
    # 向量维度。text-embedding-3-small 常用 1536。
    embedding_dimension: int
    # Milvus 地址。
    milvus_uri: str
    # Milvus token。你本地 docker 启动时一般可以空着。
    milvus_token: str | None
    # Milvus 里保存书籍切片的 collection 名称。
    milvus_collection: str
    # 本地长期记忆文件的位置。
    memory_path: Path


def load_settings() -> Settings:
    # load_dotenv 会读取当前目录下的 .env 文件。
    load_dotenv()

    # os.getenv("名字", "默认值") 的意思是：
    # 先从 .env 里找这个名字；找不到就用默认值。
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_base_url=os.getenv("OPENAI_BASE_URL") or None,
        openai_chat_model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "openai").lower(),
        openai_embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        embedding_dimension=int(os.getenv("EMBEDDING_DIMENSION", "1536")),
        milvus_uri=os.getenv("MILVUS_URI", "http://localhost:19530"),
        milvus_token=os.getenv("MILVUS_TOKEN") or None,
        milvus_collection=os.getenv("MILVUS_COLLECTION", "reading_book_chunks"),
        memory_path=Path(os.getenv("MEMORY_PATH", "data/memory.jsonl")),
    )
