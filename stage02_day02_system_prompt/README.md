# 第 2 阶段第 2 天：System Prompt 对比

本任务目标是理解 system prompt 如何影响同一个 user prompt 的输出。

## 安装依赖

```powershell
pip install openai
```

## 设置 API Key

```powershell
$env:OPENAI_API_KEY="你的 API key"
```

不要把 API key 写进代码。

## 运行

```powershell
python system_prompt_demo.py --style concise "解释什么是 AI Agent"
python system_prompt_demo.py --style teacher "解释什么是 AI Agent"
python system_prompt_demo.py --style engineer "解释什么是 AI Agent"
```

## 记录

把三次输出摘录到 `prompt_compare.md`，并写下你观察到的差异。
