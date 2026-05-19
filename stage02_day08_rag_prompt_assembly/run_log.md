# Run Log

在这里记录你运行过的命令、输出摘要、遇到的问题和修复方式。

## Commands

```powershell
python rag_prompt_demo.py
```

## Results

- 2026-05-18 已运行默认命令。
- 输出摘要：
  - Context blocks: 3
  - Question: 为什么长文档不能直接放进 prompt？
  - Wrote markdown: assembled_prompt.md
  - Wrote json: rag_prompt_payload.json
- 已用 `ConvertFrom-Json` 校验 `rag_prompt_payload.json`，结果：`rag_prompt_payload json ok`。
