# Agent Developer Roadmap Outline

Use this fallback outline only when `agent_developer_roadmap.md` is missing.

## Stage 1: Python and Project Basics

Goal: write and run small Python programs with clear file structure.

Tasks:

- Create a Python script and run it from the command line.
- Read and write text files.
- Read and write JSON and JSONL.
- Use functions and classes.
- Handle exceptions.
- Use `requirements.txt`.
- Use Git basics.

## Stage 2: Direct OpenAI API

Goal: understand the model call before using frameworks.

Tasks:

- Call a chat model directly.
- Use system and user messages.
- Add multi-turn history.
- Store conversation logs.
- Load API key from `.env`.
- Handle missing key and API errors.

## Stage 3: RAG Basics

Goal: answer questions using local documents.

Tasks:

- Load TXT, Markdown, and PDF text.
- Split text into chunks.
- Generate embeddings.
- Store vectors.
- Retrieve top-k chunks.
- Build a RAG prompt.
- Return answers with references.

## Stage 4: Tool Calling

Goal: let the model call deterministic functions.

Tasks:

- Define tool schemas.
- Build simple tools: time, calculator, file search.
- Parse tool arguments.
- Return tool results to the model.
- Add tool error handling.

## Stage 5: LangChain

Goal: use a framework without losing sight of the underlying flow.

Tasks:

- Use `ChatOpenAI`.
- Use `ChatPromptTemplate`.
- Use output parsers.
- Use retrievers.
- Build a runnable chain.
- Rebuild the RAG project with LangChain.

## Stage 6: LangGraph

Goal: build controlled multi-step Agent workflows.

Tasks:

- Define graph state.
- Add planner node.
- Add executor node.
- Add checker node.
- Handle retries and failures.

## Stage 7: Memory

Goal: preserve useful long-term context.

Tasks:

- Save raw conversations.
- Summarize long-term memory.
- Retrieve relevant memory.
- Decide when to write memory.

## Stage 8: Evaluation and Logging

Goal: debug Agent behavior with evidence.

Tasks:

- Log prompts, retrieval results, tool calls, and outputs.
- Build a small fixed test set.
- Score RAG answers for citation quality.
- Track regressions after prompt changes.

## Stage 9: Deployment

Goal: expose the Agent as a usable service.

Tasks:

- Wrap the Agent in FastAPI.
- Add request and response schemas.
- Add Docker.
- Configure environment variables.
- Add health checks and error responses.

## Stage 10: Portfolio Project

Goal: produce a complete demo project.

Tasks:

- Build a personal knowledge base Agent.
- Add document ingestion.
- Add RAG.
- Add memory.
- Add tool calling.
- Add logs and evaluation.
- Write a README and demo instructions.
