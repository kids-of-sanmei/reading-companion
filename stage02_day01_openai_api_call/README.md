# 第 2 阶段第 1 天：第一次直接调用 OpenAI API

本任务目标是写一个最小命令行脚本，直接调用 OpenAI API，并打印模型回复。

## 安装依赖

```powershell
pip install openai
```

## 设置 API Key

PowerShell：

```powershell
$env:OPENAI_API_KEY="你的 API key"
```

不要把 API key 写进 `first_api_call.py`。

如果要指定模型，可以额外设置：

```powershell
$env:OPENAI_MODEL="gpt-5.5"
```

## 运行

```powershell
python first_api_call.py "用一句话解释什么是 AI Agent"
```

## 验证错误提示

```powershell
python first_api_call.py
```

如果没有设置 `OPENAI_API_KEY`，脚本应该给出清晰提示。

## 今日重点

- 学会从环境变量读取 API key。
- 学会从命令行读取 user prompt。
- 学会使用 Responses API 直接调用 OpenAI API。
- 先理解 API 输入输出，不使用 LangChain。
