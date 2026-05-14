---
name: daily-agent-learning-plan
description: Generate stable daily learning tasks for becoming an Agent development engineer. Use when the user asks for today's study task, daily execution plan, next learning step, review task, weekly learning task, or wants continuity after context loss while following the Agent developer roadmap.
---

# Daily Agent Learning Plan

## Purpose

Use this skill to generate one concrete daily learning task for the user, based on a persistent roadmap and progress state. The main goal is continuity: do not rely on chat history when state files exist.

## Required Files

Use these files relative to the user's current workspace:

- `agent_developer_roadmap.md`: the long-term roadmap.
- `agent_learning_state.md`: persistent study state. Create it if missing.
- `daily_agent_tasks.md`: append-only daily task log. Create it if missing.

If `agent_developer_roadmap.md` is missing, use `references/roadmap-outline.md` as the fallback curriculum.

## Workflow

1. Read `agent_learning_state.md` if it exists.
2. Read `daily_agent_tasks.md` if it exists.
3. Read `agent_developer_roadmap.md`; if missing, read `references/roadmap-outline.md`.
4. Determine the next task from the current stage, not from conversation memory.
5. Generate exactly one daily task unless the user explicitly asks for multiple days.
6. Keep the task small enough to finish in 60 to 120 minutes.
7. Update `agent_learning_state.md`.
8. Append the task to `daily_agent_tasks.md`.
9. In the final response, summarize today's task and point to both files.

## State Rules

The state file must include:

- Current stage
- Current week
- Last completed task
- Today's assigned task
- Blockers
- Next suggested task
- Notes for future Codex sessions

When the user reports completion, update `Last completed task`, clear or revise blockers, and advance `Next suggested task`.

When the user says they did not finish, keep the same stage and produce a smaller recovery task.

When there is no state file, start at Stage 1 unless the user clearly provides their current level.

## Daily Task Format

Each generated task must include:

```markdown
## YYYY-MM-DD Day N

Stage:
Goal:
Estimated time:

### Learn
- ...

### Build
- ...

### Verify
- ...

### Deliverable
- ...

### Completion Criteria
- ...

### If Stuck
- ...
```

Prefer build-heavy tasks. Each day should produce a file, script, command output, note, or small working feature.

## Task Sizing

For beginners:

- One new concept per day.
- One small coding exercise per day.
- One explicit deliverable per day.
- Avoid assigning multiple frameworks on the same day.

For review days:

- Ask the user to run prior code.
- Identify one weakness.
- Assign one fix or refactor.

For project days:

- Focus on one feature slice: API call, chat loop, memory, retrieval, tool call, logging, or deployment.

## Curriculum Order

Follow this order unless the state file says otherwise:

1. Python project basics
2. Direct OpenAI API calls
3. Chat history and prompt structure
4. File reading and JSONL persistence
5. Text chunking
6. Embeddings
7. Vector search
8. RAG prompt assembly
9. Tool calling
10. LangChain basics
11. LangChain RAG
12. LangGraph workflow
13. Memory system
14. Evaluation and logging
15. FastAPI service
16. Docker and deployment
17. Portfolio project polish

## Output Discipline

Do not produce a broad study plan when the user asks for today's task.

Do not skip ahead because a topic sounds more interesting.

Do not depend on previous chat context when local state files are available.

Do not create vague tasks like "learn LangChain." Convert them into concrete actions such as "write a script that calls ChatOpenAI with a system prompt and prints the response."

## Reference

Use `references/roadmap-outline.md` only when the main roadmap file is missing or incomplete.
