# Run Log

在这里记录你运行过的命令、输出摘要、遇到的问题和修复方式。

## Commands

```powershell
python vector_search_demo.py "为什么长文档不能直接放进 prompt？"
```

## Results

- 2026-05-18 已运行默认查询。
- 输出摘要：
  - Loaded records: 7
  - Saved results: search_results.json
  - Top 1: chunk_002, score=0.25
  - Top 2: chunk_003, score=0.25
  - Top 3: chunk_004, score=0.196116
- 已用 `ConvertFrom-Json` 校验 `search_results.json`，结果：`search_results json ok`。
