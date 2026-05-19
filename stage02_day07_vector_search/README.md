# Stage 2 Day 7 - Vector Search

今天的目标是完成 RAG 检索链路中的“找相关片段”步骤。

前两天已经完成：

- Day 5: 长文本切成 chunks。
- Day 6: chunks 转成 embedding records。

今天要做：

- 把用户问题也转成 query embedding。
- 用 cosine similarity 比较 query 和每个 chunk。
- 返回 top-k 相关 chunks。

## Run

```powershell
python vector_search_demo.py "为什么长文档不能直接放进 prompt？"
python vector_search_demo.py "RAG 的检索步骤有什么作用？" --top-k 5
```

运行后查看：

- 终端输出的排名和分数。
- `search_results.json` 保存的结构化结果。

## Next

Day 8 会把这些检索结果拼进 prompt，形成最小 RAG 问答流程。
