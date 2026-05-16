"""Compare how different system prompts affect one user prompt."""

import argparse
import os

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPTS = {
    "concise": "你是一个回答简洁的 AI 助手。用不超过三句话回答用户问题。",
    "teacher": "你是一名耐心的老师。请用循序渐进的方式解释概念，并给一个简单例子。",
    "engineer": "你是一名 Agent 开发工程师。请从工程实现、模块组成和落地注意事项角度回答。",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="用不同 system prompt 调用 OpenAI API，并对比输出差异。"
    )
    parser.add_argument(
        "--style",
        choices=sorted(SYSTEM_PROMPTS),
        required=True,
        help="选择 system prompt 风格。",
    )
    parser.add_argument("prompt", nargs="+", help="用户问题。")
    return parser.parse_args()


def require_api_key() -> str:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("缺少环境变量 API_KEY。请先设置 API key。")
    return api_key


def call_openai(style: str, user_prompt: str, api_key: str) -> str:
    model = os.getenv("MODEL_NAME", "deepseek-v4-flash")
    client = OpenAI(api_key=api_key, base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[style]},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def main() -> int:
    args = parse_args()
    user_prompt = " ".join(args.prompt).strip()

    try:
        api_key = require_api_key()
        answer = call_openai(args.style, user_prompt, api_key)
    except Exception as exc:
        print(f"调用失败: {exc}")
        return 1

    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
