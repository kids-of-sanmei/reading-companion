# Agent 每日任务

本文档是每日学习任务的追加索引，由 `daily-agent-learning-plan` skill 生成和维护。

## 2026-05-14 第 1 阶段结尾验收

Stage: 第 1 阶段 - Python 与项目基础
Goal: 通过一个小型但完整的 Python 命令行项目，验收第 1 阶段要求的工程基础能力。
Task directory: `stage01_final_acceptance/`
Task file: `stage01_final_acceptance/acceptance_task.md`
Estimated time: 2 到 4 小时
Next step: 通过后进入第 2 阶段 - OpenAI API 基础。

## 2026-05-14 Stage 2 Day 1

Stage: 第 2 阶段 - OpenAI API 基础
Goal: 编写第一个直接调用 OpenAI API 的命令行脚本，理解一次模型调用从输入到输出的基本过程。
Task directory: `stage02_day01_openai_api_call/`
Task file: `stage02_day01_openai_api_call/daily_agent_tasks.md`
Estimated time: 60 到 120 分钟
Next step: 为脚本增加 system prompt。

## 2026-05-14 Stage 2 Day 2

Stage: 第 2 阶段 - OpenAI API 基础
Goal: 为 API 调用脚本增加 system prompt，并用同一个用户问题对比不同 system prompt 对输出的影响。
Task directory: `stage02_day02_system_prompt/`
Task file: `stage02_day02_system_prompt/daily_agent_tasks.md`
Estimated time: 60 到 120 分钟
Next step: 多轮对话历史与 prompt 结构。

## 2026-05-16 Stage 2 Day 3

Stage: 第 2 阶段 - OpenAI API 基础
Goal: 理解多轮对话中的 `messages` 结构，并把聊天历史保存为 JSONL。
Task directory: `stage02_day03_chat_history/`
Task file: `stage02_day03_chat_history/daily_agent_tasks.md`
Estimated time: 90 到 120 分钟
Status: 已完成
Next step: 文件读取与结构化上下文输入。

## 2026-05-16 Stage 2 Day 4

Stage: 第 2 阶段 - OpenAI API 基础
Goal: 学会读取本地文件，并把文件内容整理成结构化上下文传给模型。
Task directory: `stage02_day04_file_context/`
Task file: `stage02_day04_file_context/daily_agent_tasks.md`
Estimated time: 90 到 120 分钟
Status: 已分配，完成状态未确认
Next step: 完成后进入“文本切分基础”，为 embeddings 和 RAG 检索做准备。

## 2026-05-18 Stage 2 Day 5

Stage: 第 2 阶段 - OpenAI API 基础到 RAG 前置能力
Goal: 学会把长文本切分成适合后续 embedding 和 RAG 检索的小块。
Task directory: `stage02_day05_text_chunking/`
Task file: `stage02_day05_text_chunking/daily_agent_tasks.md`
Estimated time: 90 到 120 分钟
Status: 已生成输出，完成状态待用户自检确认
Next step: 完成后进入 embeddings 基础，把 chunks 转换成向量表示。

## 2026-05-18 Stage 2 Day 6

Stage: 第 2 阶段 - OpenAI API 基础到 RAG 前置能力
Goal: 理解 embedding 的作用，并把 Day 5 生成的 chunks 转换成可保存、可检查的向量记录。
Task directory: `stage02_day06_embeddings/`
Task file: `stage02_day06_embeddings/daily_agent_tasks.md`
Estimated time: 90 到 120 分钟
Status: 已生成输出，完成状态待用户自检确认
Next step: 完成后进入向量相似度搜索，用 query embedding 从本地向量记录中找出相关 chunks。

## 2026-05-18 Stage 2 Day 7

Stage: 第 2 阶段 - RAG 检索前置能力
Goal: 学会用 query embedding 和 cosine similarity 从本地向量记录中找出最相关的 chunks。
Task directory: `stage02_day07_vector_search/`
Task file: `stage02_day07_vector_search/daily_agent_tasks.md`
Estimated time: 90 到 120 分钟
Status: 已分配，完成状态待用户自检确认
Next step: 完成后进入 RAG prompt assembly，把 top-k 检索结果组织成上下文并生成回答。

## 2026-05-18 Stage 2 Day 8

Stage: 第 2 阶段 - RAG 前置能力收尾
Goal: 学会把 top-k 检索结果组织成可交给模型的 RAG prompt。
Task directory: `stage02_day08_rag_prompt_assembly/`
Task file: `stage02_day08_rag_prompt_assembly/daily_agent_tasks.md`
Estimated time: 90 到 120 分钟
Status: 已分配
Next step: 完成后进入第 3 阶段第 1 天，跑通最小 RAG 问答 CLI。

## 2026-05-18 Stage 3 Day 1

Stage: 第 3 阶段 - RAG 检索增强生成
Goal: 跑通一个最小 RAG 问答 CLI：检索相关 chunks，组装上下文，并生成带引用的回答。
Task directory: `stage03_day01_min_rag_qa/`
Task file: `stage03_day01_min_rag_qa/daily_agent_tasks.md`
Estimated time: 120 到 150 分钟
Status: 今日任务
Next step: 完成后继续做文档导入增强或接入真实 embedding/vector database。
