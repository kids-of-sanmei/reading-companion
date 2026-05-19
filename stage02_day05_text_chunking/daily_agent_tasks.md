# 2026-05-18 Stage 2 Day 5

Stage: 第 2 阶段 - OpenAI API 基础到 RAG 前置能力
Goal: 学会把长文本切分成适合后续 embedding 和 RAG 检索的小块。
Estimated time: 90 到 120 分钟
Task directory: `stage02_day05_text_chunking/`

### Learn
- 理解为什么不能把整篇长文直接塞进 prompt。
- 理解 `chunk_size`、`overlap`、分隔符对检索效果的影响。
- 理解文本切分和 embedding 的关系：切分决定后续检索的最小语义单位。

### Build
- 阅读并运行 `chunking_demo.py`。
- 从 `sample_docs/long_note.md` 读取长文本。
- 按段落和固定字符长度生成 chunks。
- 给每个 chunk 增加 `chunk_id`、`source`、`start_char`、`end_char`、`text` 字段。
- 将切分结果写入 `chunks.jsonl`。
- 在 `notes.md` 记录不同 `chunk_size` 和 `overlap` 的观察。

### Verify
- 运行默认切分：

```powershell
python chunking_demo.py
```

- 调整 chunk size 和 overlap：

```powershell
python chunking_demo.py --chunk-size 180 --overlap 40
```

- 检查 `chunks.jsonl` 是否每行都是合法 JSON，并确认 chunk 之间存在合理重叠。

### Deliverable
- `chunking_demo.py`
- `sample_docs/long_note.md`
- `chunks.jsonl`
- `notes.md`
- `run_log.md`

### Completion Criteria
- 能解释 `chunk_size` 太大或太小分别会带来什么问题。
- 能解释 overlap 为什么能减少语义断裂。
- 脚本能稳定读取 Markdown 文件并输出 JSONL。
- `chunks.jsonl` 至少包含 3 条 chunk 记录。
- `notes.md` 至少记录 2 组参数的观察结果。

### If Stuck
- 如果输出 chunk 太少，降低 `--chunk-size`。
- 如果 chunk 内容断得太碎，增大 `--chunk-size` 或优先按段落切分。
- 如果 JSONL 无法解析，确认每一行都是独立 JSON，不要在文件外层加数组。
