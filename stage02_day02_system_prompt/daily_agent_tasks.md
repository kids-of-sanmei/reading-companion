# 2026-05-14 第 2 阶段第 2 天任务

阶段：第 2 阶段 - OpenAI API 基础

目标：为 API 调用脚本增加 system prompt，并观察不同 system prompt 对输出的影响。

预计时间：60 到 120 分钟

## 学习

- 理解 system prompt 和 user prompt 的区别。
- 理解 system prompt 用来约束角色、风格、边界和输出格式。
- 理解同一个 user prompt 在不同 system prompt 下可能产生不同结果。
- 继续使用 OpenAI Responses API，不使用 LangChain。

## 构建

在本目录完成 `system_prompt_demo.py`。

脚本需要支持：

```powershell
python system_prompt_demo.py --style concise "解释什么是 AI Agent"
python system_prompt_demo.py --style teacher "解释什么是 AI Agent"
python system_prompt_demo.py --style engineer "解释什么是 AI Agent"
```

最低要求：

- 从命令行读取用户问题。
- 支持至少 3 种 system prompt 风格：
  - `concise`：简洁回答
  - `teacher`：像老师一样逐步解释
  - `engineer`：从工程实现角度解释
- 从环境变量读取 `OPENAI_API_KEY`。
- 调用 OpenAI API 并打印回复。
- 没有参数、style 不存在、缺少 API key 时，都要给出清晰提示。

## 验证

用同一个问题运行 3 次：

```powershell
python system_prompt_demo.py --style concise "解释什么是 AI Agent"
python system_prompt_demo.py --style teacher "解释什么是 AI Agent"
python system_prompt_demo.py --style engineer "解释什么是 AI Agent"
```

再运行错误场景：

```powershell
python system_prompt_demo.py --style unknown "解释什么是 AI Agent"
python system_prompt_demo.py
```

## 交付物

- `system_prompt_demo.py`
- `README.md`
- `prompt_compare.md`
- `run_log.md`

## 完成标准

- 三种 style 都能运行。
- 三种 style 的回复差异能在 `prompt_compare.md` 中说明。
- 脚本没有写死 API key。
- 错误场景有清晰提示。
- 你能解释 system prompt 和 user prompt 分别承担什么作用。

## 如果卡住

- 先实现命令行参数解析。
- 再用字典保存 3 个 system prompt。
- 再打印当前选择的 system prompt，确认选择逻辑正确。
- 最后接入 OpenAI API 调用。
