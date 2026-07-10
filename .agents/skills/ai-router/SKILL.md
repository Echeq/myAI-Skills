---
name: ai-router
description: >-
  Technical pipeline engine for task routing. Implements a 3-mode pipeline
  (quick/plan/debug) with planner → executor → reviewer sub-agents. Called
  by the ROUTER agent via `skill("ai-router")`. Not user-facing.
triggers:
  - "@ai-router"
  - "@ai-router --init"
  - "@ai-router --quick"
  - "@ai-router --plan"
  - "@ai-router --debug"
allowed-tools: Read, Write, Bash, Glob, Grep
---

# AI Router Skill (Technical Engine)

This is the **technical engine** behind the ROUTER agent. It is not meant to
be called directly by users — the ROUTER agent calls it via `skill("ai-router")`
when a task needs the formal pipeline (planner → executor → reviewer → fix loop).

## Initialization

If the query contains `--init`, run `references/init.md` and stop.
Do NOT run the pipeline.

## Prerequisites

Requires four sub-agents configured in `opencode.json` (run `@ai-router --init`):

| Sub-agent | Role | Prompt file | Recommended model |
|-----------|------|-------------|-------------------|
| `ai-router-planner` | Strategic planning, task breakdown | `references/manager.md` | Pro |
| `ai-router-executor` | Code execution, applying fixes | `references/worker.md` | Flash |
| `ai-router-reviewer` | Full review (plan mode) | `references/supervisor.md` | Pro |
| `ai-router-reviewer-flash` | Lightweight review (quick/debug) | `references/supervisor-lite.md` | Flash |

## Pipeline Modes

### Classification

Use these rules to determine the mode:

| Condition | Mode |
|-----------|------|
| Query contains "error", "fail", "bug" | **debug** |
| Action verbs (build/create/implement/design/refactor/generate/develop/system/architecture) or length > 150 chars | **plan** |
| Default | **quick** |

### Quick Mode (simple tasks)

```
Plan: No (too simple)
Execute: ai-router-executor (flash)
Review: ai-router-reviewer-flash (skip if trivial)
```

1. Delegate to **ai-router-executor** via `task` with the request as `prompt`.
2. If the request is trivial (read-only, simple question, single edit): skip
   review, log to history, and return.
3. Otherwise: delegate output to **ai-router-reviewer-flash** for review.
4. If REJECTED: fix with executor (flash) up to `max_iterations` (config).
5. Log outcome to `.agents/memory/ai-router/assets/state/history.md`.

### Plan Mode (multi-step tasks)

```
Plan: ai-router-planner (pro)
Execute: ai-router-executor (flash) × N subtasks
Review: ai-router-reviewer (pro) → fix loop
```

1. Send to **ai-router-planner** via `task`. Planner returns structured plan
   **only** — does NOT write files.
2. Write the plan: `.agents/memory/ai-router/assets/plan/Plan_<date>_<nnn>.md`
   and update `.agents/memory/ai-router/assets/state/current_plan.md`.
3. For each subtask in order: delegate to **ai-router-executor**, collect result.
4. Review all with **ai-router-reviewer** (pro).
5. If REJECTED:
   - **[minor]** style, naming, edge cases → fix with executor (flash)
   - **[major]** architecture, security, logic → fix with executor (pro)
   - After 2 consecutive rejections → always use pro executor
6. Mark complete in `current_plan.md`, append summary to `history.md`.

### Debug Mode (fixing errors)

```
Read → ai-router-executor → ai-router-reviewer-flash → fix → log
```

1. Read relevant files with `read` or search with `grep`/`glob`.
2. Delegate to **ai-router-executor** with error context.
3. Review with **ai-router-reviewer-flash**.
4. Apply fix with `edit` or `write`.
5. Log to `.agents/memory/ai-router/assets/state/history.md`.

## Sub-Agent Delegation

Use `task()` to delegate. Each sub-agent has its prompt pre-loaded from
`opencode.json`. Pass only the task-specific prompt:

```yaml
# Planner
task:
  description: "Plan: <user request>"
  prompt: "<request>"
  subagent_type: ai-router-planner

# Executor
task:
  description: "Execute: <subtask>"
  prompt: "<task details>"
  subagent_type: ai-router-executor

# Reviewer (pro)
task:
  description: "Review: <output>"
  prompt: "<code or plan>"
  subagent_type: ai-router-reviewer

# Reviewer (flash)
task:
  description: "Review: <output>"
  prompt: "<code>"
  subagent_type: ai-router-reviewer-flash
```

## Calling Other Skills

When a subtask matches another skill's description, load it:
```
skill("ai-audit")    # code audit
skill("ai-docs")     # documentation
skill("ai-git")      # git operations
```

## State & History

- **`.agents/memory/ai-router/assets/state/current_plan.md`** — active plan
- **`.agents/memory/ai-router/assets/state/history.md`** — append-only log
  (ISO timestamp, mode, outcome, summary)
- **`.agents/memory/ai-router/assets/plan/`** — archived plans

## Configuration

See `references/config.md` for:
- Auto-classification rules
- Execution limits (`timeout: 60`, `max_iterations: 3`)
- Allowed imports for executor sub-agent
