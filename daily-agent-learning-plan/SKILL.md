---
name: daily-agent-learning-plan
description: Use when the user asks for a long-term learning roadmap, daily learning task, next learning step, stage acceptance task, learning progress update, study state recovery, or continuity after context loss.
---

# Structured Learning Roadmap And Task System

## Purpose

Use this skill to turn a user's learning topic, learning goal, current level, and mastery requirements into a long-term, executable, trackable, and verifiable learning system.

This skill is not only a daily task generator. It must manage the full learning loop:

1. Create or update a long-term learning roadmap.
2. Break the roadmap into stages, weeks, daily tasks, and stage acceptance tasks.
3. Maintain persistent learning state.
4. Create complete task directories with task files and deliverable placeholders.
5. Keep an append-only task log.
6. Advance, pause, recover, or jump stages based on user instructions.

Do not rely on chat history when local state files exist. The local Markdown files are the source of truth.

## Required Inputs

When the user starts a new learning plan, gather or infer:

- Learning topic: what the user wants to learn.
- Learning goal: what the user wants to be able to build, explain, pass, or do.
- Current level: beginner, intermediate, advanced, or user-described background.
- Mastery requirement: basic understanding, practical project ability, interview readiness, production ability, exam readiness, or another concrete standard.
- Time budget if provided: daily study time, total duration, deadline, or weekly rhythm.

If the user does not provide all fields, make conservative assumptions and write them into the roadmap. Ask only when the missing detail would materially change the plan.

## Required Markdown Files

Use these files relative to the user's current workspace.

### Must Create If Missing

If any of the following files do not exist, you must create them before or during task generation:

- `agent_developer_roadmap.md`: long-term learning roadmap.
- `agent_learning_state.md`: persistent learning state.
- `daily_agent_tasks.md`: append-only task log and index.

The file names are kept for compatibility with the existing workspace. If the user is learning a non-Agent topic, still use these file names unless the user explicitly asks for different names.

### File Responsibilities

`agent_developer_roadmap.md` must contain:

- Learning topic.
- Learning goal.
- Current level assumptions.
- Mastery requirement.
- Suggested duration and weekly rhythm.
- Stage list in order.
- Goals for each stage.
- Core concepts for each stage.
- Practice tasks for each stage.
- Stage acceptance criteria.
- Final project or final verification target.

`agent_learning_state.md` must contain:

- Current stage.
- Current week.
- Last completed task.
- Today's assigned task.
- Blockers.
- Next suggested task.
- Notes for future Codex sessions.

`daily_agent_tasks.md` must contain:

- Append-only list of assigned tasks.
- For each task: date, stage, goal, task directory, task file, estimated time, and next step.

## Roadmap Creation Rules

If `agent_developer_roadmap.md` is missing or clearly empty:

1. Create a long-term roadmap from the user's learning topic, goal, level, and mastery requirement.
2. Split the roadmap into ordered stages.
3. Each stage must have concrete acceptance criteria.
4. Include at least one final project or final verification task.
5. Write the roadmap to `agent_developer_roadmap.md`.

If the user only says "I want to learn X", create a sensible default roadmap and record assumptions.

If the user asks to revise the learning goal or mastery level, update the roadmap and state rather than creating an unrelated duplicate plan.

## Task Directory Rules

Every assigned task must create a complete task directory. A task is incomplete if it only appears in `daily_agent_tasks.md`.

Use stable directory names:

- Daily task: `stageNN_dayNN_short_topic/`
- Stage acceptance task: `stageNN_final_acceptance/`
- Recovery task: `stageNN_recovery_short_topic/`

Each task directory must include at least:

- `daily_agent_tasks.md`: task-specific instructions.
- `README.md`: how to run, study, verify, or submit the task.
- `run_log.md`: command outputs, observations, or completion evidence.

Add deliverable placeholders based on the task, such as:

- Python task: `main.py`, `notes.md`, `requirements.txt`, sample data.
- API task: script file, `.env.example`, request/response notes.
- Writing task: `notes.md`, `summary.md`, `examples.md`.
- Project task: source files, tests, README, sample input.

Do not create vague task directories with only a README. The directory must contain the files the learner is expected to edit or fill in.

## Daily Task Format

Each generated daily task must include:

```markdown
## YYYY-MM-DD Stage N Day M

Stage:
Goal:
Estimated time:
Task directory:

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

Prefer build-heavy tasks. Each day should produce a file, script, command output, note, small feature, or testable artifact.

## Stage Acceptance Rules

At the end of every stage, create a stage acceptance directory:

```text
stageNN_final_acceptance/
  acceptance_task.md
  README.md
  run_log.md
  sample files or starter files
```

The acceptance task must include:

- Stage goal.
- Skills being verified.
- Project or exercise requirements.
- Required commands or verification steps.
- Deliverables.
- Passing criteria.
- Not-passing criteria.
- Suggested next stage after passing.

Do not advance to the next stage unless:

- the user reports completion,
- the user explicitly asks to skip ahead,
- or the user asks to force progress forward.

When skipping ahead, record that the stage was skipped or treated as passed in `agent_learning_state.md`.

## Workflow

When the user asks for a roadmap, current task, next task, progress update, or stage jump:

1. Read `agent_learning_state.md` if it exists; create it if missing.
2. Read `daily_agent_tasks.md` if it exists; create it if missing.
3. Read `agent_developer_roadmap.md` if it exists; create it if missing from user inputs or fallback assumptions.

Then choose the correct mode:

- Progress check: if the user asks to view current progress, inspect current state, or ask where they are, do not create or edit files unless required files are missing. Summarize the current stage, current task, last completed task, blockers, whether the current task appears complete, and the next suggested task.
- Current task: if the user asks what to do today and today's assigned task already exists, summarize the existing task and link to its directory. Do not create a duplicate task.
- Next task: if the user asks for the next task after completing the current one, or explicitly asks to advance, generate exactly one task unless they ask for multiple tasks or a full roadmap.
- Roadmap: if the user asks for a roadmap or the roadmap is missing, create or update the full roadmap before assigning tasks.
- Stage jump: if the user asks to jump forward or backward, update state to the requested stage and record what was skipped or revisited.

When generating a new task:

1. Determine the next task from the current state and roadmap.
2. Create the complete task directory and all required placeholder files.
3. Update `agent_learning_state.md`.
4. Append the task to `daily_agent_tasks.md`.
5. In the final response, summarize the new task and link to the roadmap, state file, root task log, and task directory.

## State Update Rules

When the user says a task is complete:

- Update `Last completed task`.
- Clear or revise blockers.
- Set `Today's assigned task` to the next task you create.
- Set `Next suggested task` to the likely following task.
- Append the new task to `daily_agent_tasks.md`.
- Create the new task directory.

When the user says they did not finish:

- Keep the same stage.
- Create a smaller recovery task.
- Record the blocker.

When the user asks to jump forward:

- Update state to the requested stage.
- Record what was skipped.
- Create the appropriate next task or stage acceptance task.

## Task Sizing

For beginners:

- One new concept per day.
- One small coding or writing exercise per day.
- One explicit deliverable per day.
- Avoid assigning multiple frameworks or major concepts on the same day.

For intermediate learners:

- Combine one concept with one realistic implementation slice.
- Require a short note explaining tradeoffs or errors.

For project days:

- Focus on one feature slice: API call, chat loop, memory, retrieval, tool call, logging, testing, or deployment.

For review days:

- Ask the user to run prior work.
- Identify one weakness.
- Assign one focused fix or refactor.

## Existing Agent Developer Curriculum

When the user's learning target is Agent development, follow this order unless the roadmap or state says otherwise:

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

Use `references/roadmap-outline.md` only as a fallback seed. If `agent_developer_roadmap.md` is missing, create the full roadmap file instead of only reading the fallback.

## Output Discipline

Do not produce only a broad study plan when the user asks for today's task.

Do not create a new task when the user only asks to view learning progress.

Do not create duplicate daily task entries when today's assigned task already exists.

Do not create a task without a task directory.

Do not create a task directory without task-specific instructions and deliverable placeholders.

Do not skip file creation when a required Markdown file is missing.

Do not skip ahead because a topic sounds more interesting.

Do not depend on previous chat context when local state files are available.

Do not create vague tasks like "learn LangChain." Convert them into concrete actions such as "write a script that calls ChatOpenAI with a system prompt and records the response."

Default to Chinese for learner-facing Markdown in this workspace, while keeping commands, filenames, code identifiers, and API names in English.
