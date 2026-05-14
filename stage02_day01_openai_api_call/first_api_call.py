from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# ── 提示词统一管理 ──────────────────────────────────────────
# 所有提示词放在一起，修改时不用翻业务逻辑代码。

PROMPTS = {
    "translator": "你是一个专业翻译，把用户输入翻译成{target_lang}，只输出译文。",
    "summarizer": "用一句话总结以下内容，不超过 50 个字。",
    "qa": "你是一个有帮助的助手，用中文回答。",
}


class LLMClient:
    def __init__(self):
        try:
            self.api_key = os.getenv("API_KEY")
            self.model = os.getenv("MODEL", "gpt-5.5")
            self.base_url = os.getenv("BASE_URL", "https://api.openai.com/v1")
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except Exception as e:
            print(f"请你检查你的配置: {e}")
            raise

    def chat(self, system: str, user: str, temperature=0.7, max_tokens=150) -> str:
        """发送 system + user 消息，返回模型回复。"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    llm = LLMClient()

    # 1) 简单问答 — 直接用预定义的 system prompt
    answer = llm.chat(PROMPTS["qa"], "法国的首都是哪里？")
    print(f"问答: {answer}")

    # 2) 翻译 — 模板变量填充
    system = PROMPTS["translator"].format(target_lang="英语")
    answer = llm.chat(system, "今天天气真好")
    print(f"翻译: {answer}")

    # 3) 摘要 — 不填变量的模板
    text = "Python 的 argparse 模块用于解析命令行参数..."
    answer = llm.chat(PROMPTS["summarizer"], text)
    print(f"摘要: {answer}")
