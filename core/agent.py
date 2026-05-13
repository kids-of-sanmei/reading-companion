from __future__ import annotations

from dataclasses import dataclass

from core.config import Settings
from core.embeddings import Embedder
from core.llm import ChatLLM
from core.memory import MemoryStore
from core.vector_store import MilvusBookStore, SearchResult


# 助手回答给你时，除了 answer 正文，也会带上 references。
# references 是本次回答参考过的书籍片段。
@dataclass(frozen=True)
class AgentReply:
    answer: str
    references: list[SearchResult]


class ReadingAssistant:
    """读书助手的总调度器。

    你可以把它理解成一个“管家”：
    - embedder：把你的问题变成向量
    - store：去 Milvus 找相关书籍内容
    - memory：读取和保存长期记忆
    - llm：让大模型组织最终回答
    """

    def __init__(
        self,
        settings: Settings,
        embedder: Embedder,
        store: MilvusBookStore,
        memory: MemoryStore,
        llm: ChatLLM,
    ) -> None:
        self.settings = settings
        self.embedder = embedder
        self.store = store
        self.memory = memory
        self.llm = llm

    def ask(self, message: str, book_title: str | None = None, limit: int = 5) -> AgentReply:
        # 第一步：把你输入的话变成向量。
        # 这样 Milvus 才能用“意思相近”来搜索书籍内容。
        query_vector = self.embedder.embed([message])[0]

        # 第二步：拿这个向量去 Milvus 找最相关的书籍切片。
        references = self.store.search(query_vector=query_vector, limit=limit, book_title=book_title)

        # 第三步：把你的问题、历史记忆、书籍片段交给大模型，让它生成回答。
        answer = self._answer(message, references)

        # 第四步：把这轮聊天保存下来，形成长期记忆。
        self.memory.append(user_message=message, assistant_message=answer, topics=[book_title] if book_title else [])
        return AgentReply(answer=answer, references=references)

    def _answer(self, message: str, references: list[SearchResult]) -> str:
        # system_prompt 是给大模型看的“角色设定”。
        # 它告诉模型：你不是普通聊天机器人，而是长期陪伴用户读书的助手。
        system_prompt = (
            "你是用户的长期读书助手。你的目标是陪用户每天理解书籍、复盘观点、"
            "提出可执行的学习行动，并根据历史记忆持续跟进。回答要真诚、具体、"
            "以书籍证据为基础；如果检索片段不足，就明确说明不足，不要编造。"
        )

        # context 是本次从书籍中检索到的内容。
        context = self._format_references(references)

        # memory 是最近几轮聊天记录，帮助助手记住你之前关注过什么。
        memory = self.memory.format_recent(limit=8)

        # user_prompt 是这次真正发给大模型的完整问题。
        # 它包含：最近记忆 + 书籍片段 + 你今天的问题。
        user_prompt = (
            f"最近记忆：\n{memory}\n\n"
            f"检索到的书籍片段：\n{context}\n\n"
            f"用户今天的问题或想法：\n{message}\n\n"
            "请用中文回答。结构建议：先回应用户，再结合书中片段解释，最后给一个今天可执行的小练习或反思问题。"
        )
        return self.llm.complete(system_prompt=system_prompt, user_prompt=user_prompt)

    def _format_references(self, references: list[SearchResult]) -> str:
        # 如果没有搜到相关片段，也要明确告诉大模型“没有资料”，避免它乱编。
        if not references:
            return "No book chunks were retrieved."

        parts = []
        for index, item in enumerate(references, start=1):
            # 只截取前 1600 个字符，避免一次给大模型塞太多内容。
            parts.append(
                f"[{index}] {item.book_title} chunk={item.chunk_index} score={item.score:.4f}\n{item.text[:1600]}"
            )
        return "\n\n".join(parts)
