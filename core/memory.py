from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


# 一条“记忆”长什么样。
# dataclass 可以理解成：帮我们少写很多重复代码的数据盒子。
@dataclass(frozen=True)
class MemoryRecord:
    # 这条记忆产生的时间。
    created_at: str
    # 你当时说的话。
    user_message: str
    # 助手当时回答的话。
    assistant_message: str
    # 这条记忆相关的主题，比如某本书名。
    topics: list[str]


class MemoryStore:
    """负责把聊天记忆保存到本地文件，也负责把最近的记忆读出来。"""

    def __init__(self, path: Path) -> None:
        # path 是记忆文件的位置，默认是 data/memory.jsonl。
        self.path = path
        # 如果 data 文件夹不存在，就自动创建，避免保存时报错。
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, user_message: str, assistant_message: str, topics: list[str] | None = None) -> None:
        # 每次你和助手聊完一轮，就生成一条新的记忆。
        record = MemoryRecord(
            created_at=datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
            user_message=user_message,
            assistant_message=assistant_message,
            topics=topics or [],
        )
        # jsonl 的意思是“一行一个 JSON”。
        # 这样以后即使记忆很多，也可以一行一行追加，不用每次重写整个文件。
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")

    def recent(self, limit: int = 8) -> list[MemoryRecord]:
        # 如果还没有任何聊天记忆，就返回空列表。
        if not self.path.exists():
            return []

        # 只读取最后 limit 条，避免把所有历史都塞给大模型，节省 token。
        lines = self.path.read_text(encoding="utf-8").splitlines()
        records: list[MemoryRecord] = []
        for line in lines[-limit:]:
            if not line.strip():
                continue
            payload = json.loads(line)
            records.append(MemoryRecord(**payload))
        return records

    def format_recent(self, limit: int = 8) -> str:
        # 把最近的记忆整理成一段文字，后面会交给大模型作为上下文。
        records = self.recent(limit=limit)
        if not records:
            return "No previous memory yet."

        parts = []
        for record in records:
            parts.append(
                f"- {record.created_at}: user={record.user_message[:180]} | assistant={record.assistant_message[:220]}"
            )
        return "\n".join(parts)
