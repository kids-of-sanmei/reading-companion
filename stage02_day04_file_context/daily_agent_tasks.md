# 2026-05-16 Stage 2 Day 4

Stage: 第 2 阶段 - OpenAI API 基础
Goal: 学会读取本地文件，并把文件内容整理成结构化上下文传给模型。
Estimated time: 90 到 120 分钟
Task directory: `stage02_day04_file_context/`

### Learn
- 理解“上下文输入”和普通 user prompt 的区别。
- 理解为什么不能把所有文件无脑塞进 prompt。
- 理解给模型传文件内容时需要包含来源、标题、正文和任务要求。

### Build
- 阅读并运行 `file_context_demo.py`。
- 从 `sample_docs/` 读取 `.md` 和 `.txt` 文件。
- 把文件内容转换成结构化 context block。
- 用一个 user question 询问这些文件的内容。
- 将模型回答或 dry-run 输出记录到 `answers.md`。

### Verify
- 无 API key 时，运行：

```powershell
python file_context_demo.py --dry-run --question "这些文档主要讲了什么？"
```

- 有 API key 时，运行：

```powershell
python file_context_demo.py --question "根据文档，总结 Agent 学习的下一步重点。"
```

- 修改 `sample_docs/notes.md` 后再次运行，观察回答是否变化。

### Deliverable
- `file_context_demo.py`
- `sample_docs/notes.md`
- `sample_docs/todo.txt`
- `answers.md`
- `run_log.md`

### Completion Criteria
- 能解释 context block 为什么要标注文件来源。
- 能说清楚“读取文件”和“RAG 检索”的区别。
- 脚本能在 `--dry-run` 模式下运行。
- 有 API key 时，脚本能基于文件内容回答问题。
- `answers.md` 至少记录 2 次运行结果或观察。

### If Stuck
- 如果 API key 报错，先只运行 `--dry-run`。
- 如果读不到文件，确认命令在 `stage02_day04_file_context/` 目录下执行。
- 如果回答没有引用文件内容，检查 prompt 中是否真的包含了 context block。
