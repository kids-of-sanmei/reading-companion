from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


# 一本书会被切成很多小段。
# BookChunk 就是其中一小段，以及它来自哪本书、是第几段等信息。
@dataclass(frozen=True)
class BookChunk:
    id: str
    book_id: str
    book_title: str
    chunk_index: int
    text: str
    source_path: str


def read_book_text(path: Path) -> str:
    # 根据文件后缀判断书籍格式。
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        # PDF 需要一页一页提取文字。
        reader = PdfReader(str(path))
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                # 保留页码，后面检索时更容易知道内容来自哪里。
                pages.append(f"\n\n[Page {index}]\n{text}")
        return "\n".join(pages)

    if suffix in {".txt", ".md", ".markdown"}:
        # TXT/Markdown 是纯文本，直接读取即可。
        return path.read_text(encoding="utf-8")

    raise ValueError(f"Unsupported book format: {suffix}. Use PDF, TXT, MD, or Markdown.")


def normalize_text(text: str) -> str:
    # 做一点文本清理：统一换行、去掉多余空格、合并过多空行。
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 180) -> list[str]:
    # chunk_size 是每个切片大约多少字。
    # overlap 是相邻切片重叠多少字，避免一句话刚好被切断后丢失上下文。
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size.")

    text = normalize_text(text)
    if not text:
        return []

    # 优先按段落切，这样比硬切固定长度更容易保留语义。
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        # 如果单个段落本身就太长，只能再硬切成小块。
        if len(paragraph) > chunk_size:
            if current:
                chunks.append(current.strip())
                current = ""
            chunks.extend(_split_long_text(paragraph, chunk_size, overlap))
            continue

        candidate = paragraph if not current else f"{current}\n\n{paragraph}"
        if len(candidate) <= chunk_size:
            # 当前段落还能放进这一块，就继续合并。
            current = candidate
        else:
            # 放不下了，就先保存当前块，再开启下一块。
            chunks.append(current.strip())
            tail = current[-overlap:] if overlap else ""
            current = f"{tail}\n\n{paragraph}".strip() if tail else paragraph

    if current:
        chunks.append(current.strip())
    return chunks


def build_book_chunks(
    path: Path,
    title: str | None = None,
    chunk_size: int = 1200,
    overlap: int = 180,
) -> list[BookChunk]:
    # 这个函数是“读书 + 切片 + 包装成 BookChunk”的总入口。
    text = read_book_text(path)
    book_title = title or path.stem
    book_id = _stable_id(f"{book_title}:{path.resolve()}")
    raw_chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    return [
        BookChunk(
            id=f"{book_id}-{index:06d}",
            book_id=book_id,
            book_title=book_title,
            chunk_index=index,
            text=chunk,
            source_path=str(path),
        )
        for index, chunk in enumerate(raw_chunks)
    ]


def _split_long_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    # 专门处理超长段落：按固定长度切，同时保留 overlap 重叠。
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def _stable_id(value: str) -> str:
    # 根据书名和路径生成一个稳定 id。
    # 同一本书重复导入时，id 一样，Milvus 会更新而不是重复插入。
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:16]
