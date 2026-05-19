# Stage 2 Day 5 - Text Chunking

本任务练习 RAG 前的关键步骤：把长文本切成适合 embedding 和检索的小块。

## Files

- `chunking_demo.py`: 文本切分脚本。
- `sample_docs/long_note.md`: 示例长文本。
- `chunks.jsonl`: 脚本输出的 chunk 结果。
- `notes.md`: 参数观察和学习总结。
- `run_log.md`: 运行命令和结果记录。

## Run

```powershell
python chunking_demo.py
python chunking_demo.py --chunk-size 180 --overlap 40
```

完成后查看 `chunks.jsonl`，并把观察写入 `notes.md`。
