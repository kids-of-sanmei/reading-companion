# Stage 2 Day 3 - Chat History 与 JSONL 持久化

今天的目标是把前两天的单轮 API 调用升级为多轮对话：程序需要维护 `messages` 列表，并把每轮输入输出追加保存到 `conversations.jsonl`。

## 准备环境

```powershell
pip install openai python-dotenv
```

复制 `.env.example` 的变量到你自己的 `.env`，然后填入 API key。

## 本地演练

无需 API key：

```powershell
python chat_history_demo.py --dry-run
```

## 真实调用

```powershell
python chat_history_demo.py
```

输入 `exit` 或 `quit` 结束对话。

## 验证

- `conversations.jsonl` 每行都是一个 JSON 对象。
- 每条记录包含 `timestamp`、`user`、`assistant`。
- `conversation_notes.md` 写下你对多轮上下文的观察。
- `run_log.md` 记录实际运行命令和输出摘要。
