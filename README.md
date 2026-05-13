# 读书助手

这是一个本地 Python 读书助手骨架：把 PDF/TXT/Markdown 书籍切片后写入 Milvus，聊天时检索相关片段，并保存每天交流形成的长期记忆。

## 快速开始

1. 安装依赖：

```powershell
pip install -r requirements.txt
```

2. 启动 Milvus：

```powershell
docker compose up -d
```

3. 配置环境变量：

```powershell
Copy-Item .env.example .env
```

编辑 `.env`，填入 `OPENAI_API_KEY`。如果只是测试入库流程，可以把 `EMBEDDING_PROVIDER=local_hash`，此时不需要 API key，但检索语义质量会弱很多。

4. 导入一本书：

```powershell
python -m tools.ingest_book "books/example.pdf" --title "示例书名"
```

5. 开始聊天：

```powershell
python -m tools.chat
```

## 目录

- `core/config.py`：读取 `.env` 配置。
- `core/chunking.py`：解析书籍并切片。
- `core/embeddings.py`：OpenAI 或本地 hash embedding。
- `core/vector_store.py`：Milvus collection 创建、写入和检索。
- `core/memory.py`：本地 JSONL 长期记忆。
- `core/llm.py`：LLM 调用和离线兜底回复。
- `core/agent.py`：读书助手编排逻辑。
- `tools/ingest_book.py`：书籍入库命令。
- `tools/chat.py`：日常交流命令。

## 推荐工作流

每天打开 `python -m tools.chat`，围绕当天想读的章节提问、复盘、写行动计划。助手会自动检索书籍片段，并把对话摘要追加到 `data/memory.jsonl`，后续交流会带上最近的记忆。
