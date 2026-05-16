# 2026-05-16 Stage 2 Day 3

Stage: 第 2 阶段 - OpenAI API 基础
Goal: 理解多轮对话中的 `messages` 结构，并把聊天历史保存为 JSONL。
Estimated time: 90 到 120 分钟
Task directory: `stage02_day03_chat_history/`

### Learn
- 理解 `system`、`user`、`assistant` 三种角色如何共同组成一次请求。
- 理解多轮对话为什么需要把历史消息重新传给模型。
- 理解 JSONL：一行一个 JSON 对象，适合追加保存聊天记录。

### Build
- 阅读并补全 `chat_history_demo.py`。
- 运行一次至少 3 轮的命令行对话。
- 每轮对话后，把 `user` 输入和 `assistant` 回复追加写入 `conversations.jsonl`。
- 在 `conversation_notes.md` 中记录你观察到的上下文效果。

### Verify
- 无 API key 时，运行：

```powershell
python chat_history_demo.py --dry-run
```

- 有 API key 时，运行：

```powershell
python chat_history_demo.py
```

- 查看 `conversations.jsonl`，确认每行都是合法 JSON。
- 查看 `run_log.md`，记录命令、结果和遇到的问题。

### Deliverable
- `chat_history_demo.py`
- `conversations.jsonl`
- `conversation_notes.md`
- `run_log.md`

### Completion Criteria
- 能说清楚为什么多轮对话要保留历史消息。
- 能解释 JSONL 和普通 JSON 数组的区别。
- 脚本能在 `--dry-run` 模式下运行。
- 有 API key 时，脚本能完成至少 3 轮真实 API 对话。
- `conversations.jsonl` 至少包含 3 条对话记录。

### If Stuck
- 如果 API key 报错，先只运行 `--dry-run`，确认本地逻辑正确。
- 如果 JSONL 文件格式出错，检查每一行是否都是一个完整 JSON 对象。
- 如果模型忘记前文，检查发送 API 的 `messages` 是否包含之前的 user/assistant 消息。
