# 2026-05-18 Stage 3 Day 1

Stage: 第 3 阶段 - RAG 检索增强生成
Goal: 跑通一个最小 RAG 问答 CLI：检索相关 chunks，组装上下文，并生成带引用的回答。
Estimated time: 120 到 150 分钟
Task directory: `stage03_day01_min_rag_qa/`

### Learn
- 理解 RAG 的完整最小链路：query -> query embedding -> vector search -> context -> answer。
- 理解 RAG 的第一版可以先用本地离线回答验证链路，再接真实模型。
- 理解 `trace` 的重要性：记录检索结果、prompt 和回答，方便之后排错。
- 理解“资料不足”处理是 RAG 的基本能力，不是额外功能。

### Build
- 阅读并运行 `rag_qa_demo.py`。
- 从 `../stage02_day06_embeddings/embeddings.jsonl` 读取本地向量记录。
- 对用户问题生成 query embedding。
- 检索 top-k chunks。
- 默认用本地 extractive 模式生成答案摘要和引用。
- 可选使用 `--api` 调用真实 OpenAI API 生成回答。
- 输出 `answer.md` 和 `rag_trace.json`。

### Verify
- 默认离线运行：

```powershell
python rag_qa_demo.py "为什么长文档不能直接放进 prompt？"
```

- 调整 top-k：

```powershell
python rag_qa_demo.py "RAG 的基本流程是什么？" --top-k 5
```

- 可选真实 API：

```powershell
python rag_qa_demo.py "RAG 的基本流程是什么？" --api
```

- 检查 `answer.md` 是否包含回答和引用。
- 检查 `rag_trace.json` 是否包含 query、retrieved_context、prompt 和 answer。

### Deliverable
- `rag_qa_demo.py`
- `answer.md`
- `rag_trace.json`
- `.env.example`
- `notes.md`
- `run_log.md`

### Completion Criteria
- 能解释 RAG 的完整最小流程。
- 能解释为什么要保存 `rag_trace.json`。
- 脚本能从本地 embeddings 检索 chunks，并生成带引用的回答。
- 至少运行 2 个不同问题，并把观察写进 `notes.md`。
- 能说出当前离线 hash embedding 和真实 embedding 的差异。

### If Stuck
- 如果找不到 `embeddings.jsonl`，先回到 Day 6 目录运行 `python embedding_demo.py`。
- 如果检索结果不理想，先降低或提高 `--top-k` 做对比。
- 如果没有 API key，先完成默认离线模式；真实 API 是可选项。
