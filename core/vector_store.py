from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pymilvus import DataType, MilvusClient

from core.chunking import BookChunk


# Milvus 搜索回来的一条结果。
# 它包含：书里找到的原文、相似度分数、来自哪本书、这是第几个切片。
@dataclass(frozen=True)
class SearchResult:
    text: str
    score: float
    book_title: str
    chunk_index: int
    source_path: str


class MilvusBookStore:
    """负责和 Milvus 向量数据库打交道。"""

    def __init__(
        self,
        uri: str,
        collection_name: str,
        dimension: int,
        token: str | None = None,
    ) -> None:
        self.collection_name = collection_name
        self.dimension = dimension
        # MilvusClient 是官方客户端。
        # 你可以把它理解成：Python 连接 Milvus 的“遥控器”。
        self.client = MilvusClient(uri=uri, token=token)

    def ensure_collection(self) -> None:
        # collection 类似数据库里的“表”。
        # 如果这个表已经存在，就不重复创建。
        if self.client.has_collection(self.collection_name):
            return

        # 下面是在定义 Milvus 表结构：
        # id: 每个切片的唯一编号
        # vector: 文字对应的向量
        # book_title/source_path/text: 方便以后知道这段文字来自哪里
        schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
        schema.add_field("id", DataType.VARCHAR, is_primary=True, max_length=128)
        schema.add_field("vector", DataType.FLOAT_VECTOR, dim=self.dimension)
        schema.add_field("book_id", DataType.VARCHAR, max_length=128)
        schema.add_field("book_title", DataType.VARCHAR, max_length=512)
        schema.add_field("chunk_index", DataType.INT64)
        schema.add_field("source_path", DataType.VARCHAR, max_length=2048)
        schema.add_field("text", DataType.VARCHAR, max_length=65535)

        # 给 vector 字段建索引。
        # 索引的作用是：书很多时，也能较快找到相似内容。
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index("vector", metric_type="COSINE", index_type="AUTOINDEX")

        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params,
        )

    def upsert_chunks(self, chunks: list[BookChunk], vectors: list[list[float]]) -> int:
        # chunks 是书籍文字切片，vectors 是每个切片对应的数字向量。
        # 两者必须一一对应。
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must have the same length.")
        if not chunks:
            return 0

        self.ensure_collection()

        # 把 Python 对象整理成 Milvus 可以写入的一行行数据。
        rows = [
            {
                "id": chunk.id,
                "vector": vector,
                "book_id": chunk.book_id,
                "book_title": _truncate_utf8(chunk.book_title, 512),
                "chunk_index": chunk.chunk_index,
                "source_path": _truncate_utf8(chunk.source_path, 2048),
                "text": _truncate_utf8(chunk.text, 65535),
            }
            for chunk, vector in zip(chunks, vectors)
        ]

        # upsert 的意思是：有就更新，没有就插入。
        self.client.upsert(collection_name=self.collection_name, data=rows)
        # flush 会把数据真正落到 Milvus 里，避免刚写入后搜不到。
        self.client.flush(collection_name=self.collection_name)
        return len(rows)

    def search(self, query_vector: list[float], limit: int = 5, book_title: str | None = None) -> list[SearchResult]:
        self.ensure_collection()
        filters = None
        if book_title:
            # 如果指定了书名，就只在这一本书里搜索。
            escaped = book_title.replace('"', '\\"')
            filters = f'book_title == "{escaped}"'

        # 用“问题的向量”去 Milvus 里找最相似的书籍切片。
        raw_results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            anns_field="vector",
            limit=limit,
            filter=filters,
            output_fields=["text", "book_title", "chunk_index", "source_path"],
        )
        if not raw_results:
            return []

        return [self._to_result(hit) for hit in raw_results[0]]

    def _to_result(self, hit: dict) -> SearchResult:
        # Milvus 返回的是字典，这里把它整理成更好用的 SearchResult。
        entity = hit.get("entity", {})
        return SearchResult(
            text=entity.get("text", ""),
            score=float(hit.get("distance", 0.0)),
            book_title=entity.get("book_title", ""),
            chunk_index=int(entity.get("chunk_index", 0)),
            source_path=entity.get("source_path", ""),
        )


def batched(items: list[BookChunk], size: int) -> Iterable[list[BookChunk]]:
    # 把很多切片分批处理。
    # 比如一本书有 1000 段，不一次性全塞进去，而是 64 段一批。
    for index in range(0, len(items), size):
        yield items[index : index + size]


def _truncate_utf8(value: str, max_bytes: int) -> str:
    # Milvus 的 VARCHAR 限制按字节计算。
    # 中文一个字通常占 3 个字节，所以不能只用 len(value) 判断。
    encoded = value.encode("utf-8")
    if len(encoded) <= max_bytes:
        return value
    return encoded[:max_bytes].decode("utf-8", errors="ignore")
