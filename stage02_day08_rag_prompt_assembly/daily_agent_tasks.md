# 2026-05-18 Stage 2 Day 8

Stage: 第 2 阶段 - RAG 前置能力收尾
Goal: 学会把 top-k 检索结果组织成可交给模型的 RAG prompt。
Estimated time: 90 到 120 分钟
Task directory: `stage02_day08_rag_prompt_assembly/`

### Learn
- 理解 RAG prompt 需要包含：任务说明、回答约束、检索上下文、用户问题。
- 理解为什么 context block 要保留来源、chunk_id 和相似度分数。
- 理解“只能基于资料回答”和“资料不足时说明不足”的提示词约束。
- 理解 prompt assembly 是从检索到生成之间的桥梁。

### Build
- 阅读并运行 `rag_prompt_demo.py`。
- 从 `../stage02_day07_vector_search/search_results.json` 读取检索结果。
- 将 top-k chunks 组装成带引用编号的 context blocks。
- 生成 `assembled_prompt.md` 和 `rag_prompt_payload.json`。
- 在 `notes.md` 记录 prompt 结构设计和你认为容易出错的地方。

### Verify
- 默认运行：

```powershell
python rag_prompt_demo.py
```

- 指定一个新问题：

```powershell
python rag_prompt_demo.py --query "RAG 为什么要先检索再回答？"
```

- 检查 `assembled_prompt.md` 是否包含 system 指令、context blocks 和 user question。
- 检查 `rag_prompt_payload.json` 是否是合法 JSON。

### Deliverable
- `rag_prompt_demo.py`
- `assembled_prompt.md`
- `rag_prompt_payload.json`
- `notes.md`
- `run_log.md`

### Completion Criteria
- 能解释 RAG prompt 里 system 指令、context、question 各自的作用。
- 能解释为什么引用来源对 RAG 很重要。
- 脚本能从 Day 7 检索结果生成结构化 prompt。
- `assembled_prompt.md` 至少包含 2 个 context block。
- `notes.md` 至少写出 3 条 prompt assembly 的注意点。

### If Stuck
- 如果找不到 `search_results.json`，先回到 Day 7 目录运行一次 `python vector_search_demo.py "为什么长文档不能直接放进 prompt？"`。
- 如果 prompt 太长，降低 Day 7 的 `--top-k`。
- 如果 context 内容混乱，先检查 Day 5 的 chunk 是否切得太碎。
