---
name: ai-orchestrator
description: >-
  Intelligent task orchestrator. Classifies requests by intent, decomposes
  them into subtasks, routes each subtask to the best available agent or
  skill, and reviews results with task-adaptive criteria.
triggers:
  - "@ai-orchestrator"
  - "@ai-orchestrator --init"
  - "@ai-orchestrator --quick"
  - "@ai-orchestrator --plan"
  - "@ai-orchestrator --debug"
  - "@ai-orchestrator --cancel <id>"
  - "@ai-orchestrator --cancel-all"
  - "@ai-orchestrator --status"
---

# AI Orchestrator Skill

Intelligent task orchestrator. Unlike `ai-router` (fixed 3-mode pipeline),
ai-orchestrator uses **dynamic classification** and a **capability registry**
to route work to the right agent or skill.

```
User → Classifier → [intent + capabilities] → Registry lookup →
  → Planner → [subtasks with skill hints] →
  → Auto-route to skill or executor → Review → Fix loop
```

## Quick Start

```
@ai-orchestrator --init          # Interactive setup (models + capabilities)
@ai-orchestrator                 # Auto-classify and route
@ai-orchestrator --quick "..."   # Force quick mode
@ai-orchestrator --plan "..."    # Force plan mode
@ai-orchestrator --debug "..."   # Force debug mode
```

## Initialization

If the user's message contains `--init`, run the initialization procedure from
`references/init.md` and stop. Do not run the normal pipeline.

## Prerequisites

Requires four sub-agents configured in `opencode.json`:
- `ai-orchestrator-planner` — strategic planning (prompt: `references/manager.md`)
- `ai-orchestrator-executor` — code/task execution (prompt: `references/worker.md`)
- `ai-orchestrator-reviewer` — full review (prompt: `references/supervisor.md`, model: pro)
- `ai-orchestrator-reviewer-flash` — lightweight review (prompt: `references/supervisor-lite.md`, model: flash)

Run `@ai-orchestrator --init` to generate the configuration interactively.

## Dynamic Classification

Replaces ai-router's 3 hardcoded keyword modes with a structured prompt
that outputs:

```yaml
mode: plan                    # quick | plan | debug
confidence: 0.85              # 0.0 - 1.0
capabilities_needed:          # what this task needs
  - code-generation
  - testing
suggested_skills:             # skills that can help
  - ai-git
```

**Classification prompt rules:**
- If confidence < 0.6 → escalate to user: "I'm not sure how to route this.
  Is it quick (simple), plan (multi-step), or debug (fix something)?"
- If the request mentions an existing skill by trigger (e.g. "audit this code")
  → auto-route to that skill directly, skip the pipeline.
- If the request spans multiple domains (e.g. "audit and document")
  → break into parallel tracks.

## Capability Registry

Each installed skill declares its capabilities in frontmatter.
The orchestrator discovers them at runtime:

```yaml
# Example from ai-audit/SKILL.md
capabilities:
  domains: [code-review, security, performance, documentation]
  environments: [python, javascript, typescript, shell, markdown]
```

**Built-in taxonomy** (see `references/config.md` for full list):

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
1. Classifier extracts `capabilities_needed` from the request
2. Registry matches against all installed skills' `capabilities`
3. Best match (highest overlap) gets routed via `skill()` before execution
4. If no match → use generic executor

## Pipeline Flow

### Quick Mode (simple tasks)
1. Delegate to **ai-orchestrator-executor** via `task`
2. If trivial (read-only, single edit) → skip review, log and return
3. Otherwise → review with **ai-orchestrator-reviewer-flash**
4. If REJECTED → fix and re-run (up to `max_iterations`)

### Plan Mode (multi-step tasks)
1. **Dynamic classification** → extract intent + capabilities
2. **Registry lookup** → identify which skills/agents can help
3. Send to **ai-orchestrator-planner** with classification context
4. Planner returns structured subtasks with skill hints
5. For each subtask:
   - If a skill hint matches → `skill("name")` to load it, delegate
   - Otherwise → **ai-orchestrator-executor**
6. Review with **ai-orchestrator-reviewer** (task-adaptive criteria)
7. If REJECTED → severity-based fix loop (minor→flash, major→pro)
8. Log to `assets/state/history.md`

### Debug Mode (fixing errors)
1. Read relevant files / search
2. Delegate to **ai-orchestrator-executor** with error context
3. Review with **ai-orchestrator-reviewer-flash**
4. Apply fix, log to `history.md`

## DAG Execution Engine

For **plan mode**, the orchestrator uses a formal Directed Acyclic Graph (DAG)
execution engine with an 8-state machine per subtask. See full design in
`assets/plan/Plan_task_lifecycle.md`.

### Pipeline (Phase 1 — DAG only, no priorities)

1. **Plan** — Planner returns Markdown plan with subtasks, dependencies, and dep types
2. **Parse** — Orchestrator converts Markdown plan to `plan_input.json` (see `references/parse_plan.md`)
3. **Init DAG** — `bash: python dag.py init plan_input.json` — validates DAG (cycle detection), builds graph
4. **Execute loop** — Repeatedly call `bash: python dag.py run`:
   - `NEXT <id> "<label>"` — delegate to executor sub-agent, then report `dag.py complete <id>` or `dag.py fail <id> "<error>"`
   - `WAIT` — tasks are RUNNING, poll again shortly
   - `DEADLOCK <ids>` — tasks auto-failed (dependency was CANCELLED/FAILED — cannot proceed)
   - `ALL_DONE` — execution complete
5. **Review** — Each executor output reviewed per task-adaptive criteria
6. **Cascade** — On `fail`, `dag.py` automates transitive cascade failure to dependents
7. **Cancel** — `@ai-orchestrator --cancel <id>` calls `dag.py cancel <id>` (NO cascade)
8. **Cancel all** — `@ai-orchestrator --cancel-all` — cancels all non-terminal tasks
9. **Status** — `@ai-orchestrator --status` calls `dag.py status` — displays current state table
10. **Log** — Results appended to `assets/state/history.md`

### State Machine

8 states: READY, RUNNING, BLOCKED, COMPLETED, FAILED, CANCELLED, SKIPPED, PAUSED.
All transitions validated by guard function. See `Plan_task_lifecycle.md` §2 for details.

Key rules:
- **FAILED is retryable** (not terminal). Enters terminal only when retries exhausted.
- **CANCELLED does NOT cascade.** But dependents may deadlock (all deps terminal, not all COMPLETED).
- **Cascade is transitive BFS** through all dependents. COMPLETED/CANCELLED/SKIPPED never reverted.
- **Deadlock detection** auto-fails BLOCKED tasks whose ALL dependencies are terminal but NOT all COMPLETED. Prevents infinite waiting loops.

### Plan JSON Format

The orchestrator converts the planner's Markdown into this format for `dag.py init`:

```json
{
  "plan_id": "2026-07-07-plan-001",
  "objective": "Add user authentication to the app",
  "tasks": [
    {
      "id": "1",
      "label": "Design auth schema",
      "description": "Design the database schema for user accounts.",
      "dependencies": [],
      "dep_types": {}
    },
    {
      "id": "2",
      "label": "Implement auth middleware",
      "description": "Implement middleware that checks session tokens.",
      "dependencies": ["1"],
      "dep_types": {"1": "data"}
    }
  ]
}
```

## Task-Adaptive Review

The reviewer uses different criteria based on task type:

| Task type | Review focus |
|-----------|-------------|
| `code-generation` | Correctness, style, edge cases |
| `security` | Injection flaws, secrets, auth |
| `documentation` | Completeness, formatting, links |
| `debugging` | Root cause addressed, no regressions |
| `configuration` | Syntax, path correctness, security |

Selected automatically from the classifier's `capabilities_needed`.

## Delegating to Sub-Agents

```yaml
task:
  description: "Plan: <user request>"
  prompt: "<request + classification context>"
  subagent_type: ai-orchestrator-planner
```

Same pattern for executor, reviewer, and reviewer-flash.

## Invoking Other Skills

```yaml
# Auto-routing (Phase 1): before delegating a subtask, check registry
if skill_match:
  skill("<matched_skill>")
  task:
    description: "<subtask>"
    prompt: "<task details>"
    subagent_type: ai-orchestrator-executor
```

## State & History

- **`assets/state/task_states.json`** — machine-readable state persistence. Source of truth for the DAG engine. Written atomically after every transition.
- **`assets/state/current_plan.md`** — active plan (or "No active plan." if idle)
- **`assets/state/history.md`** — append-only log with ISO timestamp, mode, outcome
- **`assets/plan/`** — archived plans with dated filenames

## Example Flow

**User:** "Audit this repo for security issues and generate a report."

1. **Classifier** → `{mode: plan, confidence: 0.9, capabilities: [security, documentation], skills: [ai-audit, ai-docs]}`
2. **Registry** → matches `ai-audit` (security), `ai-docs` (documentation)
3. **Planner** → subtask 1: "Run security audit" (skill: ai-audit), subtask 2: "Generate report" (skill: ai-docs)
4. **Execute** → `skill("ai-audit")` for subtask 1, `skill("ai-docs")` for subtask 2
5. **Review** → security-adaptive criteria
6. **Log** → success to `history.md`

---

*ai-orchestrator v1 — Phase 1: Smart Router. Forked from ai-router.*
