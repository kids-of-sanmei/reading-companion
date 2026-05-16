# Stage 2 Day 4 - 文件读取与结构化上下文输入

今天的目标是让脚本读取本地文件，并把文件内容作为清晰的上下文传给模型。这是后续 RAG 的前置能力：RAG 不是直接把所有文件塞给模型，而是先找到相关片段，再组织成上下文。

## 准备环境

```powershell
pip install openai python-dotenv
```

如需真实调用 API，参考 `.env.example` 创建 `.env`。

## 本地演练

```powershell
python file_context_demo.py --dry-run --question "这些文档主要讲了什么？"
```

## 真实调用

```powershell
python file_context_demo.py --question "根据文档，总结 Agent 学习的下一步重点。"
```

## 今日重点

- 文件读取只是“拿到原始材料”。
- 结构化上下文是“让模型知道材料边界和来源”。
- RAG 会在后续增加“只挑相关材料”的检索步骤。
