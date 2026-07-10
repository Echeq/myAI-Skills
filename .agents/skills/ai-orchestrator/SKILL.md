---
name: ai-orchestrator
description: >-
  DAG-based task orchestration engine. Implements dynamic classification,
  capability registry lookup, 8-state task lifecycle, cascade failure
  propagation, and deadlock detection. Called by the ORCHESTRATOR agent
  via `skill("ai-orchestrator")`. Not user-facing.
triggers:
  - "@ai-orchestrator"
  - "@ai-orchestrator --init"
  - "@ai-orchestrator --quick"
  - "@ai-orchestrator --plan"
  - "@ai-orchestrator --debug"
  - "@ai-orchestrator --cancel <id>"
  - "@ai-orchestrator --cancel-all"
  - "@ai-orchestrator --status"
allowed-tools: Read, Write, Bash, Glob, Grep
---

# AI Orchestrator Skill (Technical Engine)

This is the **technical engine** behind the ORCHESTRATOR agent. It implements
the DAG execution engine, capability registry, and 8-state task lifecycle.
Called via `skill("ai-orchestrator")` when a task needs formal dependency
management, parallel execution, cascade failure handling, or deadlock detection.

## Initialization

If the query contains `--init`, run `references/init.md` and stop.
Do NOT run the pipeline.

## Prerequisites

Requires four sub-agents configured in `opencode.json` (run
`@ai-orchestrator --init`):

| Sub-agent | Role | Prompt file | Recommended model |
|-----------|------|-------------|-------------------|
| `ai-orchestrator-planner` | Strategic planning, dep types | `references/manager.md` | Pro |
| `ai-orchestrator-executor` | Code/task execution | `references/worker.md` | Flash |
| `ai-orchestrator-reviewer` | Full review (plan mode) | `references/supervisor.md` | Pro |
| `ai-orchestrator-reviewer-flash` | Lightweight review (quick/debug) | `references/supervisor-lite.md` | Flash |

Also requires `dag.py` at `.agents/skills/ai-orchestrator/dag.py` (stdlib-only
Python CLI, no dependencies).

## Pipeline Modes

### Quick Mode (simple tasks)

```
ai-orchestrator-executor (flash) → ai-orchestrator-reviewer-flash (always)
```

1. Delegate to **ai-orchestrator-executor** via `task`.
2. Review with **ai-orchestrator-reviewer-flash** (always — even trivial tasks
   get a security scan).
3. If REJECTED: fix loop (up to `max_iterations=3`):
   - Attempt 1: same executor (flash)
   - Attempts 2-3: escalate to planner (pro) as executor
4. Log to `.agents/memory/ai-orchestrator/assets/state/history.md`.

### Plan Mode (multi-step with dependencies)

```
Dynamic classifier → Capability registry → Planner → DAG engine →
Executor/skill loop → Adaptive review → Fix loop → Log
```

1. **Dynamic classification**: extract `{mode, confidence, capabilities_needed,
   suggested_skills}`. If confidence < 0.6, escalate to user.
2. **Registry lookup**: match capabilities against installed skills.
3. Send to **ai-orchestrator-planner** with classification context.
4. Planner returns structured plan with subtasks, dependencies, dep types.
5. **Parse plan** → convert to `plan_input.json` (see `references/parse_plan.md`).
6. **Init DAG**: `bash: python dag.py init .agents/memory/ai-orchestrator/assets/plan/plan_input.json`
7. **Execute loop**: repeatedly call `bash: python dag.py run`:
   - `NEXT <id> "<label>"` → delegate to executor or skill, then
     `dag.py complete <id>` or `dag.py fail <id> "<error>"`
   - `WAIT` → tasks running, poll again
   - `DEADLOCK <ids>` → deadlocked tasks auto-failed
   - `ALL_DONE` → execution complete
8. **Review**: each output reviewed with task-adaptive criteria.
9. If REJECTED:
   - [minor] → fix with executor (flash), escalate to pro on 2nd rejection
   - [major] → fix with planner (pro) immediately
10. Log to `.agents/memory/ai-orchestrator/assets/state/history.md`.

### Debug Mode (fixing errors)

```
Read → ai-orchestrator-executor → ai-orchestrator-reviewer-flash → fix → log
```

1. Read relevant files.
2. Delegate to **ai-orchestrator-executor** with error context.
3. Review with **ai-orchestrator-reviewer-flash**.
4. Apply fix.
5. Log to `.agents/memory/ai-orchestrator/assets/state/history.md`.

## Dynamic Classification

Use a structured prompt to classify, not keyword heuristics:

```yaml
mode: plan                    # quick | plan | debug
confidence: 0.85              # 0.0 - 1.0
capabilities_needed:
  - code-generation
  - database
suggested_skills:
  - ai-git
```

**Rules:**
- Confidence < 0.6 → escalate: "I'm not sure how to route this. Is it
  quick (simple), plan (multi-step), or debug (fix something)?"
- Mentions an existing skill trigger → auto-route directly, skip pipeline.
- Spans multiple domains → break into parallel tracks.

**Fallback** (if prompt classifier unavailable):
- "error"/"fail"/"bug" → debug
- action verbs or length > 150 → plan
- otherwise → quick

## Capability Registry

Each installed skill declares capabilities. The orchestrator discovers them
at runtime:

```yaml
# In skill frontmatter:
capabilities:
  domains: [code-review, security, documentation]
  environments: [python, javascript]
```

**Taxonomy** (see `references/config.md` for full list):

| Domain | Examples |
|--------|----------|
| `code-generation` | Writing new code, refactoring |
| `code-review` | Reviewing, auditing |
| `debugging` | Fixing errors, stack traces |
| `documentation` | Generating docs, READMEs |
| `configuration` | Config files, env vars, gitignore |
| `deployment` | CI/CD, releases, git ops |
| `research` | Answering questions, investigating |
| `architecture` | System design, planning |

**Matching logic:**
1. Classifier extracts `capabilities_needed`
2. Registry matches against installed skills' `capabilities`
3. Best match → route via `skill()` before execution
4. No match → use generic executor

## DAG Execution Engine

Powered by `dag.py` (stdlib only, no deps).

### 8-State Machine

```
READY ──→ RUNNING ──→ COMPLETED (terminal)
                  └──→ FAILED ──→ READY (retry)
                  └──→ PAUSED ──→ RUNNING (resume)
BLOCKED ──→ READY (deps resolved)
        └──→ FAILED (cascade or deadlock)
FAILED ──→ READY (retry) ──→ revert cascade dependents to BLOCKED
CANCELLED (terminal, NO cascade)
SKIPPED (terminal)
```

**Key rules:**
- FAILED is retryable (not terminal). Terminal only when retries exhausted.
- CANCELLED does NOT cascade. Dependents may deadlock (all deps terminal,
  not all COMPLETED).
- Cascade is transitive BFS through all dependents.
- Deadlock detection auto-fails BLOCKED tasks whose dependencies are all
  terminal but not all COMPLETED.

### DAG Commands

| Command | Action |
|---------|--------|
| `python dag.py init <plan.json>` | Load plan, validate DAG, write state |
| `python dag.py run` | Pop next READY task or signal done |
| `python dag.py complete <id>` | Mark COMPLETED, unblock dependents |
| `python dag.py fail <id> "<error>"` | Mark FAILED, cascade to dependents |
| `python dag.py cancel <id>` | Cancel (NO cascade) |
| `python dag.py retry <id>` | Retry FAILED, revert cascade |
| `python dag.py status` | Print state table |
| `python dag.py dump` | Full JSON state dump |

### Plan JSON Format

```json
{
  "plan_id": "2026-07-10-plan-001",
  "objective": "Build a CLI tool",
  "tasks": [
    {
      "id": "1",
      "label": "Set up project",
      "description": "Create scaffolding",
      "dependencies": [],
      "dep_types": {}
    },
    {
      "id": "2",
      "label": "Implement feature",
      "description": "Core logic",
      "dependencies": ["1"],
      "dep_types": {"1": "code"}
    }
  ]
}
```

## Task-Adaptive Review

Review criteria adapt to the task type:

| Task type | Review focus |
|-----------|-------------|
| `code-generation` | Correctness, style, edge cases |
| `security` | Injection flaws, secrets, auth |
| `documentation` | Completeness, formatting, links |
| `debugging` | Root cause addressed, no regressions |
| `configuration` | Syntax, path correctness, security |

## Sub-Agent Delegation

```yaml
task:
  description: "Plan: <user request>"
  prompt: "<request + classification context>"
  subagent_type: ai-orchestrator-planner
```

Same pattern for executor, reviewer, and reviewer-flash.

## Skill Routing

When a subtask matches a skill via the registry:

```yaml
if skill_match:
  skill("<matched_skill>")
  task:
    description: "<subtask>"
    prompt: "<task details>"
    subagent_type: ai-orchestrator-executor
```

## State & History

- **`.agents/memory/ai-orchestrator/assets/state/task_states.json`** —
  machine-readable DAG state. Source of truth. Written atomically.
- **`.agents/memory/ai-orchestrator/assets/state/current_plan.md`** — active plan
- **`.agents/memory/ai-orchestrator/assets/state/history.md`** — append-only log
  (ISO timestamp, mode, outcome, summary)
- **`.agents/memory/ai-orchestrator/assets/plan/`** — archived plans

## Configuration

See `references/config.md` for:
- Dynamic classification rules (primary + fallback)
- Execution limits (`timeout: 60`, `max_iterations: 3`, fix loop model escalation)
- Capability taxonomy (full list of domains and environments)
- DAG engine configuration (state paths, timeouts)
