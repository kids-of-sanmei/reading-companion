# Run Log

在这里记录你运行过的命令、输出摘要、遇到的问题和修复方式。

## Commands

```powershell
python rag_qa_demo.py "为什么长文档不能直接放进 prompt？"
```

## Results

- 2026-05-18 已运行默认离线命令。
- 输出摘要：
  - Query: 为什么长文档不能直接放进 prompt？
  - Retrieved chunks: 3
  - Mode: offline
  - Wrote answer: answer.md
  - Wrote trace: rag_trace.json
- 已用 `ConvertFrom-Json` 校验 `rag_trace.json`，结果：`rag_trace json ok`。
