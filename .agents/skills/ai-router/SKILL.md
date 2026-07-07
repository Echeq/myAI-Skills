---
name: ai-router
description: Routes complex tasks by planning, delegating to specialised sub-agents, and reviewing results. Supports custom model selection for each role.
---

# AI Router Skill

Routes complex tasks by planning, delegating to specialised sub-agents (`ai-router-planner`, `ai-router-executor`, `ai-router-reviewer`), and reviewing results.

## Initialization

If the user's message contains `--init`, run the initialization procedure from `references/init.md` and stop. Do not run the normal pipeline.

## Prerequisites

This skill requires four subagents configured in `opencode.json`:
- `ai-router-planner` — strategic planning (system prompt: `references/manager.md`)
- `ai-router-executor` — fast code execution (system prompt: `references/worker.md`)
- `ai-router-reviewer` — full review for plan mode (system prompt: `references/supervisor.md`, model: pro)
- `ai-router-reviewer-flash` — lightweight review for quick/debug (system prompt: `references/supervisor-lite.md`, model: flash)

Run `@ai-router --init` to generate the configuration interactively.

The `external_directory: deny` permission on each agent restricts all file access to within the repository.

## Available Tools

- `read`, `write`, `edit` — file operations
- `task` — delegate to sub-agents (planner, reviewer, executor)
- `skill` — invoke other installed skills
- `grep`, `glob` — search files
- `bash` — run shell commands

## Configuration

Read `references/config.md` for auto-classification rules, timeouts, and iteration limits.

## Query Classification

Use the rules in `references/config.md` to classify the incoming query into one of three modes:

| Mode | Trigger | Behaviour |
|------|---------|-----------|
| **debug** | query contains "error", "fail", "bug" | Direct fix → executor → review(flash) |
| **plan** | action verbs (build/create/implement/design/refactor/generate/develop/system/architecture), or length > 150 | Planner(pro) → executor → review(pro) → [minor→flash fix \| major→pro fix] |
| **quick** | default | Execute(flash) → review(flash or skip for trivial) |

## Pipeline Modes

### Quick Mode
1. Delegate to **ai-router-executor** via `task` with the user request as `prompt`.
2. **If the request is trivial** (read-only info, simple question, single edit): skip review entirely, log and return.
3. **Otherwise**: delegate output to **ai-router-reviewer-flash** via `task` for lightweight review.
4. If REJECTED, classify severity (same as plan mode) then fix and re-run (up to `max_iterations` from config).
5. Log outcome to `assets/state/history.md`.

### Plan Mode
1. Send to **ai-router-planner** via `task` with the user request as `prompt`. The planner returns a structured Markdown plan **only** — it does NOT write any files.
2. **Write the plan directly** using the `write` tool:
   - Save to `assets/plan/Plan_<date>_<nnn>.md`.
   - Update `assets/state/current_plan.md` with the subtask list.
3. For each subtask in order:
   - Send to **ai-router-executor** with the subtask description as `prompt`.
   - Collect result.
4. Review with **ai-router-reviewer** (pro).
5. If REJECTED, the reviewer classifies severity:
   - **[minor]** naming, style, edge cases, formatting → send fix to **ai-router-executor** (flash) → re-review with **ai-router-reviewer** (pro)
   - **[major]** architecture, security, logic flaws → send fix to **ai-router-executor** (pro) → re-review with **ai-router-reviewer** (pro)
6. If still rejected after the fix pass, escalate: send fix to **ai-router-executor** (pro) regardless of severity (up to `max_iterations` from config).
7. Mark completion in `current_plan.md`, append summary to `history.md`.

### Debug Mode
1. Read relevant files with `read` or search with `grep`/`glob`.
2. Delegate to **ai-router-executor** with the error context as `prompt`.
3. Review with **ai-router-reviewer-flash** (lightweight).
4. Apply fix with `edit` or `write`.
5. Log to `history.md`.

## Delegating to Sub-Agents

Use the `task` tool to call sub-agents. Each subagent already has its system prompt loaded from its `opencode.json` config. Pass only the task-specific request as `prompt`:

```yaml
# Invoke planner
task:
  description: "Plan: <user request>"
  prompt: "<user request>"
  subagent_type: ai-router-planner

# Invoke executor
task:
  description: "Execute: <subtask>"
  prompt: "<task details>"
  subagent_type: ai-router-executor

# Invoke reviewer (pro — for plan mode)
task:
  description: "Review: <output>"
  prompt: "<code or plan to review>"
  subagent_type: ai-router-reviewer

# Invoke reviewer (flash — for quick/debug modes)
task:
  description: "Review: <output>"
  prompt: "<code to review>"
  subagent_type: ai-router-reviewer-flash
```

## Invoking Other Skills

Use the `skill` tool to load another skill when a subtask matches its description:

```
skill <skill_name>
```

## State & History

- **`assets/state/current_plan.md`** — always contains the active plan (or "No active plan." if idle).
- **`assets/state/history.md`** — append-only log. Each entry must have an ISO timestamp, mode, outcome, and a brief summary.
- **`assets/plan/`** — saved plans with dated filenames for reference.

## Example Flow

**User:** "Build a CLI tool that fetches weather data for a given city."

1. Query triggers **plan** mode (contains "build").
2. Send to `ai-router-planner`; receive a structured plan.
3. Write the plan directly: `assets/plan/Plan_2026-07-07_001.md` and `assets/state/current_plan.md` via `write` tool.
4. For each subtask (e.g. "parse CLI args", "fetch weather API", "format output"), send to `ai-router-executor`.
5. Review with `ai-router-reviewer` (pro).
6. If REJECTED, the reviewer classifies severity (minor→flash fix, major→pro fix) and re-runs the fix loop.
7. If APPROVED, write final code with `write` tool, log success to `history.md`.
8. Mark plan complete in `current_plan.md`.
