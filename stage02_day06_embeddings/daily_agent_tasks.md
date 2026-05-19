# 2026-05-18 Stage 2 Day 6

Stage: 第 2 阶段 - OpenAI API 基础到 RAG 前置能力
Goal: 理解 embedding 的作用，并把 Day 5 生成的 chunks 转换成可保存、可检查的向量记录。
Estimated time: 90 到 120 分钟
Task directory: `stage02_day06_embeddings/`

### Learn
- 理解 embedding 是“把文本映射成向量”，方便后续用相似度做检索。
- 理解 chunk 文本、embedding 向量、metadata 三者要一起保存。
- 理解为什么真实 RAG 系统需要先 embedding，再做 vector search。
- 区分离线模拟 embedding 和真实 OpenAI Embeddings API 的用途。

### Build
- 阅读并运行 `embedding_demo.py`。
- 默认使用离线 hash embedding，把 `../stage02_day05_text_chunking/chunks.jsonl` 转成 `embeddings.jsonl`。
- 检查每条输出是否包含 `chunk_id`、`source`、`text`、`embedding`、`embedding_dim`、`embedding_model` 字段。
- 如果已有 `OPENAI_API_KEY`，尝试用 `--api` 调用真实 Embeddings API。
- 在 `notes.md` 记录离线 embedding 和真实 API embedding 的区别。

### Verify
- 本地离线运行：

```powershell
python embedding_demo.py
```

- 限制前 3 条 chunk：

```powershell
python embedding_demo.py --limit 3 --dim 16
```

- 可选真实 API 调用：

```powershell
python embedding_demo.py --api
```

- 检查 `embeddings.jsonl` 每一行都是合法 JSON，并确认 `embedding` 是数字数组。

### Deliverable
- `embedding_demo.py`
- `embeddings.jsonl`
- `notes.md`
- `run_log.md`
- `.env.example`

### Completion Criteria
- 能解释 embedding 为什么适合做语义检索。
- 能解释为什么要保留 `chunk_id` 和 `source`。
- 脚本能从 Day 5 的 `chunks.jsonl` 读取输入并输出 `embeddings.jsonl`。
- `embeddings.jsonl` 至少包含 3 条记录。
- `notes.md` 至少写出 3 条观察，包括向量维度、metadata、API 与离线模拟的差异。

### If Stuck
- 如果找不到 `chunks.jsonl`，先回到 Day 5 目录运行 `python chunking_demo.py`。
- 如果缺少 `openai` 包，先运行 `pip install openai python-dotenv`。
- 如果没有 API key，先完成默认离线模式；真实 API 是可选加分项。
