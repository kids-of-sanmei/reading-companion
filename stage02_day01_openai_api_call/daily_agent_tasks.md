# 2026-05-14 第 2 阶段第 1 天任务

阶段：第 2 阶段 - OpenAI API 基础

目标：编写第一个直接调用 OpenAI API 的命令行脚本。

预计时间：60 到 120 分钟

## 学习

- 理解一次 OpenAI API 调用包含哪些要素：API key、model、input/message、response。
- 理解环境变量 `OPENAI_API_KEY` 的作用，避免把 key 写进代码。
- 理解模型返回结果里最重要的信息：模型生成的文本。
- 理解 Responses API 的最小调用方式：`client.responses.create(...)`。
- 暂时不要使用 LangChain，先掌握直接 API 调用。

## 构建

在本目录中完成 `first_api_call.py`。

脚本需要支持：

```powershell
python first_api_call.py "用一句话解释什么是 AI Agent"
```

最低要求：

- 从命令行读取用户问题。
- 从环境变量读取 `OPENAI_API_KEY`。
- 调用 OpenAI API。
- 打印 `response.output_text` 中的模型回复。
- 如果缺少 API key，给出清晰提示。
- 如果用户没有传入问题，给出使用示例。

## 验证

在本目录运行：

```powershell
python first_api_call.py "用一句话解释什么是 AI Agent"
```

再运行一个错误场景：

```powershell
python first_api_call.py
```

如果你还没有 API key，也要运行脚本确认它能给出清晰的缺 key 提示。

## 交付物

- `first_api_call.py`
- `README.md`
- `run_log.md`

## 完成标准

- 脚本不会把 API key 写死在代码里。
- 有参数时会尝试调用 OpenAI API。
- 没有参数时会显示使用方法。
- 没有 `OPENAI_API_KEY` 时会显示清晰错误提示。
- `README.md` 写清楚如何设置环境变量和运行脚本。
- `run_log.md` 记录至少一次正常运行或缺 key 运行的结果。

## 如果卡住

- 先实现命令行参数读取。
- 再实现缺少参数时的提示。
- 再实现读取 `OPENAI_API_KEY`。
- 最后再接入真实 API 调用。
