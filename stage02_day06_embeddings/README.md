# Stage 2 Day 6 - Embeddings 基础

今天的目标是把文本 chunk 转换成向量记录。后续做 vector search 时，不会直接比较原文字符串，而是比较这些向量之间的相似度。

## Files

- `embedding_demo.py`: 从 chunks JSONL 生成 embeddings JSONL 的脚本。
- `.env.example`: 真实 OpenAI Embeddings API 调用的环境变量示例。
- `notes.md`: 记录观察和学习总结。
- `run_log.md`: 记录运行命令和结果。
- `embeddings.jsonl`: 运行脚本后生成。

## Run

默认离线模式，不需要 API key：

```powershell
python embedding_demo.py
```

调整离线向量维度：

```powershell
python embedding_demo.py --limit 3 --dim 16
```

可选真实 API 模式：

```powershell
pip install openai python-dotenv
python embedding_demo.py --api
```

真实 API 模式需要参考 `.env.example` 配置 `OPENAI_API_KEY`。
