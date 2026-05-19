# Stage 2 Day 8 - RAG Prompt Assembly

今天是第 2 阶段到第 3 阶段之间的收尾任务：把检索结果变成模型可用的 prompt。

前置链路：

- Day 5: 文本切分。
- Day 6: 生成 embeddings。
- Day 7: 用向量相似度检索 top-k chunks。

今天只做一件事：把 top-k chunks 组织成清晰、可引用、带约束的 prompt。

## Run

```powershell
python rag_prompt_demo.py
python rag_prompt_demo.py --query "RAG 为什么要先检索再回答？"
```

运行后查看：

- `assembled_prompt.md`
- `rag_prompt_payload.json`

## Next

第 3 阶段 Day 1 会把检索、prompt assembly、回答生成串成一个最小 RAG 问答 CLI。
