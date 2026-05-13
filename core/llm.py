from __future__ import annotations

from openai import OpenAI

from core.config import Settings


class ChatLLM:
    """负责调用聊天大模型。"""

    def __init__(self, settings: Settings) -> None:
        self.model = settings.openai_chat_model
        self.available = bool(settings.openai_api_key)

        # 如果 .env 里没有 OPENAI_API_KEY，就不创建 OpenAI 客户端。
        # 这样项目至少还能启动，并给出离线提示。
        self.client = (
            OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)
            if self.available
            else None
        )

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        # 没配置 key 时，返回一个本地提示，而不是直接崩掉。
        if not self.client:
            return self._offline_reply(user_prompt)

        # messages 是发给模型的对话内容：
        # system：告诉模型要扮演什么角色
        # user：这次真正的问题和上下文
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content or ""

    def _offline_reply(self, user_prompt: str) -> str:
        return (
            "当前没有配置 OPENAI_API_KEY，我只能做离线兜底回答。\n\n"
            "我已经可以把你的问题和检索到的书籍片段组织起来。配置 API key 后，"
            "我会基于这些上下文和长期记忆，和你进行更自然的读书交流。\n\n"
            f"本次输入摘要：{user_prompt[:800]}"
        )
