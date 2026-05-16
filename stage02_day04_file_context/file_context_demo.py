"""Read local files and pass structured context to a chat model."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


DOCS_DIR = Path("sample_docs")
SUPPORTED_SUFFIXES = {".md", ".txt"}
SYSTEM_PROMPT = "你是一个严谨的 Agent 开发教练。只能基于用户提供的文档上下文回答。"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="读取本地文件，并把结构化上下文传给模型。")
    parser.add_argument("--question", required=True, help="要基于文档回答的问题。")
    parser.add_argument("--dry-run", action="store_true", help="不调用 API，只打印将要发送的上下文。")
    return parser.parse_args()


def read_documents(docs_dir: Path) -> list[dict[str, str]]:
    documents = []
    for path in sorted(docs_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            documents.append(
                {
                    "source": str(path.as_posix()),
                    "content": path.read_text(encoding="utf-8").strip(),
                }
            )
    return documents


def build_context(documents: list[dict[str, str]]) -> str:
    blocks = []
    for index, document in enumerate(documents, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[Document {index}]",
                    f"source: {document['source']}",
                    "content:",
                    document["content"],
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def build_user_prompt(context: str, question: str) -> str:
    return f"""请基于下面的文档上下文回答问题。

文档上下文：
{context}

问题：
{question}

回答要求：
- 用中文回答。
- 如果文档中没有答案，请明确说“文档中没有提供”。
- 尽量指出答案来自哪个 source。
"""


def call_model(user_prompt: str) -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("缺少 API_KEY。没有 key 时请先运行 --dry-run。")

    client = OpenAI(api_key=api_key, base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"))
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def main() -> int:
    args = parse_args()
    load_dotenv()

    documents = read_documents(DOCS_DIR)
    if not documents:
        raise RuntimeError(f"没有在 {DOCS_DIR} 中找到 .md 或 .txt 文件。")

    context = build_context(documents)
    user_prompt = build_user_prompt(context, args.question)

    if args.dry_run:
        print(user_prompt)
        return 0

    print(call_model(user_prompt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
