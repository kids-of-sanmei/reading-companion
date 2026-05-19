# Run Log

## 2026-05-18

### Commands

```powershell
python chunking_demo.py
python chunking_demo.py --chunk-size 180 --overlap 40
```

### Observations

- `python chunking_demo.py` 已运行成功，输出 `chunks.jsonl`，默认参数为 `chunk_size=240`、`overlap=50`，生成 7 条 chunk。
- `python chunking_demo.py --chunk-size 180 --overlap 40 --output chunks_alt.jsonl` 已运行成功，生成 7 条 chunk；该输出只用于参数验证。
- `chunks.jsonl` 已通过 PowerShell `ConvertFrom-Json` 逐行解析，确认每行是合法 JSON。

### Issues

- 暂无。
