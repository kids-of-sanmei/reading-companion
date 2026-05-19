# Stage 3 Day 1 - Minimal RAG QA

今天正式进入第 3 阶段：RAG 检索增强生成。

目标不是一上来接向量数据库或复杂框架，而是先用本地文件跑通最小闭环：

1. 用户提问。
2. 问题转成 query embedding。
3. 在本地 embeddings 中检索 top-k chunks。
4. 把 chunks 组装成上下文。
5. 生成带引用的回答。
6. 保存 trace 方便排错。

## Run

```powershell
python rag_qa_demo.py "为什么长文档不能直接放进 prompt？"
python rag_qa_demo.py "RAG 的基本流程是什么？" --top-k 5
```

可选真实 API：

```powershell
pip install openai python-dotenv
python rag_qa_demo.py "RAG 的基本流程是什么？" --api
```

## Outputs

- `answer.md`: 最终回答。
- `rag_trace.json`: 检索、prompt 和回答的完整过程记录。
