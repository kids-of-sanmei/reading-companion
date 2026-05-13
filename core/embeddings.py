from __future__ import annotations

import hashlib
import math
import re
import warnings
from abc import ABC, abstractmethod

from openai import OpenAI

from core.config import Settings


class Embedder(ABC):
    """文字转向量工具的统一接口。"""

    # dimension 是向量长度。
    # 比如 1536 表示每段文字会变成 1536 个数字。
    dimension: int

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        # 输入多段文字，返回多组向量。
        raise NotImplementedError


class OpenAIEmbedder(Embedder):
    """使用 OpenAI 的 embedding 模型，把文字变成向量。"""

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai.")
        self.model = settings.openai_embedding_model
        self.dimension = settings.embedding_dimension
        self.client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        # 这里是真正调用 OpenAI API 的地方。
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimension,
        )
        return [item.embedding for item in response.data]


class LocalHashEmbedder(Embedder):
    """本地兜底版 embedding。

    它不需要联网，也不需要 API key，适合先测试流程。
    但它不是真正理解语义，只是粗略地把词映射成数字，所以效果不如 OpenAI。
    """

    def __init__(self, dimension: int = 1536) -> None:
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        # 先准备一个全是 0 的向量。
        vector = [0.0] * self.dimension

        # 把文字切成一个个词。这里也兼容中文字符。
        tokens = re.findall(r"[\w\u4e00-\u9fff]+", text.lower())
        for token in tokens:
            # 用 hash 把每个词固定映射到向量里的某个位置。
            digest = hashlib.md5(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        # 归一化：把向量长度调整到 1，方便比较相似度。
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]


def build_embedder(settings: Settings) -> Embedder:
    # 根据 .env 里的 EMBEDDING_PROVIDER 决定用哪种向量工具。
    if settings.embedding_provider == "openai":
        if not settings.openai_api_key:
            warnings.warn(
                "OPENAI_API_KEY is empty; falling back to local_hash embeddings. "
                "Set OPENAI_API_KEY for real semantic retrieval.",
                RuntimeWarning,
                stacklevel=2,
            )
            return LocalHashEmbedder(settings.embedding_dimension)
        return OpenAIEmbedder(settings)

    if settings.embedding_provider == "local_hash":
        return LocalHashEmbedder(settings.embedding_dimension)

    raise ValueError("EMBEDDING_PROVIDER must be either 'openai' or 'local_hash'.")
