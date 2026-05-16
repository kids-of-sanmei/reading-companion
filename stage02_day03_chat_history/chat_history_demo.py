"""Run a small multi-turn chat and persist each turn to JSONL."""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


SYSTEM_PROMPT = "你是一个耐心的 Agent 开发教练。用中文回答，优先解释工程实现思路。"
HISTORY_FILE = Path("conversations.jsonl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="多轮对话与 JSONL 聊天记录演示。")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="不调用 API，用本地模拟回复验证聊天历史和 JSONL 写入逻辑。",
    )
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def call_model(client: OpenAI, model: str, messages: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()


def fake_reply(messages: list[dict[str, str]]) -> str:
    user_turns = [message["content"] for message in messages if message["role"] == "user"]
    if len(user_turns) == 1:
        return "这是 dry-run 回复：我已收到第一轮问题。"
    return f"这是 dry-run 回复：当前共有 {len(user_turns)} 轮用户输入，我会参考前文回答。"


def main() -> int:
    args = parse_args()
    load_dotenv()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    client = None
    model = os.getenv("MODEL_NAME", "gpt-4.1-mini")

    if not args.dry_run:
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise RuntimeError("缺少 API_KEY。没有 key 时请先运行：python chat_history_demo.py --dry-run")
        client = OpenAI(api_key=api_key, base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"))

    print("输入 exit 或 quit 结束。")
    while True:
        user_input = input("user> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        assistant_reply = fake_reply(messages) if args.dry_run else call_model(client, model, messages)
        messages.append({"role": "assistant", "content": assistant_reply})

        print(f"assistant> {assistant_reply}")
        append_jsonl(
            HISTORY_FILE,
            {
                "timestamp": now_iso(),
                "user": user_input,
                "assistant": assistant_reply,
                "mode": "dry-run" if args.dry_run else "api",
            },
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
