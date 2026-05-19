# Run Log

在这里记录你运行过的命令、输出摘要、遇到的问题和修复方式。

## Commands

```powershell
python embedding_demo.py
```

## Results

- 2026-05-18 已运行默认离线模式。
- 输出摘要：
  - Read chunks: 7
  - Wrote embeddings: embeddings.jsonl
  - Embedding dim: 32
  - Embedding model: offline-hash-32
- 已用 `ConvertFrom-Json` 校验 `embeddings.jsonl`，结果：`jsonl ok`。
