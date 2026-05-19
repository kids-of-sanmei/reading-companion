# Assembled RAG Prompt

## System

你是一个基于资料回答问题的 RAG 助手。
回答必须遵守：
1. 只基于提供的 context 回答。
2. 如果 context 中没有足够信息，明确说“资料不足，无法确定”。
3. 回答后列出使用到的引用编号。
4. 不要编造 context 之外的事实。

## User

请根据以下 context 回答问题。

## Context

[1] chunk_id=chunk_002 source=sample_docs\long_note.md score=0.25
在前面的练习中，我们已经学习了如何读取本地 Markdown 和 TXT 文件，并把文件内容整理成带有来源信息的 context block。这个能力可以让模型基于用户提供的资料回答问题，但它仍然有一个明显限制：当文件很长时，不能把所有内容都一次性放进 prompt。

[2] chunk_id=chunk_003 source=sample_docs\long_note.md score=0.25
大模型的上下文窗口虽然越来越大，但上下文不是无限资源。把整篇文档直接传给模型会增加成本，也会让模型更难关注真正相关的段落。更重要的是，在真实知识库场景中，用户的问题通常只需要文档中的少数片段，不需要整本书或整个项目说明。

[3] chunk_id=chunk_004 source=sample_docs\long_note.md score=0.196116
RAG 的基本思路是先把资料切成小块，然后为每个小块生成 embedding。用户提问时，系统也会把问题转换成 embedding，再从知识库中找出最相似的若干个 chunk。最后，只把这些相关 chunk 拼进 prompt，让模型基于它们回答。

## Question

为什么长文档不能直接放进 prompt？