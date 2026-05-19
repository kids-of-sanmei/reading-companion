# 2026-05-18 Stage 2 Day 7

Stage: 第 2 阶段 - RAG 检索前置能力
Goal: 学会用 query embedding 和 cosine similarity 从本地向量记录中找出最相关的 chunks。
Estimated time: 90 到 120 分钟
Task directory: `stage02_day07_vector_search/`

### Learn
- 理解向量检索的核心不是“关键词匹配”，而是比较 query 向量和 chunk 向量的相似度。
- 理解 cosine similarity 的含义：两个向量方向越接近，分数越高。
- 理解 top-k 的作用：只取最相关的几个片段进入后续 prompt。
- 理解检索结果需要保留 `chunk_id`、`source`、`score` 和原文片段，方便后续回答附引用。

### Build
- 阅读并运行 `vector_search_demo.py`。
- 从 `../stage02_day06_embeddings/embeddings.jsonl` 读取 embedding 记录。
- 把用户问题转换成同维度 query embedding。
- 计算 query 和每个 chunk 的 cosine similarity。
- 输出 top-k 检索结果到终端，并保存到 `search_results.json`。
- 在 `notes.md` 记录不同问题和不同 `--top-k` 的观察。

### Verify
- 默认查询：

```powershell
python vector_search_demo.py "为什么长文档不能直接放进 prompt？"
```

- 调整 top-k：

```powershell
python vector_search_demo.py "RAG 的检索步骤有什么作用？" --top-k 5
```

- 检查 `search_results.json` 是否包含 `query`、`top_k`、`results`，每个 result 是否包含 `score` 和 `text`。

### Deliverable
- `vector_search_demo.py`
- `search_results.json`
- `notes.md`
- `run_log.md`
- `README.md`

### Completion Criteria
- 能解释 cosine similarity 为什么能用于向量检索。
- 能解释 top-k 太大或太小分别有什么影响。
- 脚本能读取 Day 6 的 `embeddings.jsonl` 并返回排序后的检索结果。
- `search_results.json` 至少保存 1 次查询结果。
- `notes.md` 至少记录 2 个不同问题的检索观察。

### If Stuck
- 如果找不到 `embeddings.jsonl`，先回到 Day 6 目录运行 `python embedding_demo.py`。
- 如果结果看起来不稳定，先记住当前是离线 hash embedding，真实 embedding 效果会更接近语义检索。
- 如果 top-k 返回太多无关内容，降低 `--top-k`；如果上下文不够，增加 `--top-k`。
