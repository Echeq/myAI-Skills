# ai-orchestrator

DAG-based task orchestration engine. Implements dynamic classification, capability registry lookup, 8-state task lifecycle, cascade failure propagation, and deadlock detection. Called by the ORCHESTRATOR agent via `skill("ai-orchestrator")`. Not user-facing.

> **Trigger:** `@ai-orchestrator` | `@ai-orchestrator --init` | `@ai-orchestrator --quick` | `@ai-orchestrator --plan` | `@ai-orchestrator --debug` | `@ai-orchestrator --cancel <id>` | `@ai-orchestrator --cancel-all` | `@ai-orchestrator --status`

## Quick Start

1. Run `@ai-orchestrator --init` to configure models for planner, executor, and reviewer roles.
2. Type `@ai-orchestrator <task>` — the skill dynamically classifies the request into **quick**, **plan**, or **debug** mode.
3. For **plan** mode: decomposes into a formal DAG → delegates subtasks → reviews with task-adaptive criteria → fix loop on rejection.
4. For **quick** mode: delegates directly to executor; always reviewed by flash reviewer.
5. For **debug** mode: reads files, delegates to executor, reviews, applies fix.

**Example:** `@ai-orchestrator audit this repo for security issues and generate a report` → classified as **plan** (confidence 0.9) → registry matches `ai-audit` (security) and `ai-docs` (documentation) → planner decomposes → DAG executes → review passes → logs to `history.md`.

## Description

Unlike `ai-router` (fixed 3-mode keyword pipeline), ai-orchestrator uses **dynamic classification** via a structured prompt that outputs `{mode, confidence, capabilities_needed, suggested_skills}`. A **capability registry** maps task requirements to installed skills, enabling automatic routing without hardcoded triggers.

The orchestrator builds a formal **Directed Acyclic Graph (DAG)** for plan-mode tasks, managed by a Python CLI engine (`dag.py`, stdlib only). Each subtask progresses through an 8-state machine (READY → RUNNING → BLOCKED → COMPLETED → FAILED → CANCELLED → SKIPPED → PAUSED) with deadlock detection and transitive cascade failure propagation.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-orchestrator` | Auto-classify and route |
| `@ai-orchestrator --init` | Interactive setup (models + sub-agents) |
| `@ai-orchestrator --quick "..."` | Force quick mode |
| `@ai-orchestrator --plan "..."` | Force plan mode |
| `@ai-orchestrator --debug "..."` | Force debug mode |
| `@ai-orchestrator --cancel <id>` | Cancel a task (NO cascade) |
| `@ai-orchestrator --cancel-all` | Cancel all non-terminal tasks |
| `@ai-orchestrator --status` | Show current DAG state table |

### DAG Engine Commands

| Command | Purpose |
| :--- | :--- |
| `python dag.py init plan_input.json` | Load plan, validate DAG, build state machine |
| `python dag.py run` | Pop next READY task or signal done/deadlock |
| `python dag.py complete <id>` | Mark task COMPLETED, unblock dependents |
| `python dag.py fail <id> "<error>"` | Mark task FAILED, cascade to dependents |
| `python dag.py cancel <id>` | Cancel task (deadlock detection, no cascade) |
| `python dag.py cancel-all` | Cancel all non-terminal tasks |
| `python dag.py retry <id>` | Retry FAILED task, revert cascade dependents |
| `python dag.py status` | Human-readable state table |
| `python dag.py dump` | Full JSON state dump to stdout |

## Configuration

### Prerequisites

Requires four subagents configured in `opencode.json` (run `@ai-orchestrator --init` to generate):

| Subagent | Role | Model | Permission |
| :--- | :--- | :--- | :--- |
| `ai-orchestrator-planner` | Strategic planning, dep types | Pro | Full access |
| `ai-orchestrator-executor` | Code/task execution | Flash | Full access |
| `ai-orchestrator-reviewer` | Full review (plan mode) | Pro | Read-only + task |
| `ai-orchestrator-reviewer-flash` | Lightweight review (quick/debug) | Flash | Read-only + task |

### State & History

| Path | Purpose |
| :--- | :--- |
| `.agents/memory/ai-orchestrator/assets/state/task_states.json` | Machine-readable state (source of truth for DAG engine) |
| `.agents/memory/ai-orchestrator/assets/state/current_plan.md` | Active plan |
| `.agents/memory/ai-orchestrator/assets/state/history.md` | Append-only execution log |
| `.agents/memory/ai-orchestrator/assets/plan/` | Archived plans with dated filenames |

### Task-Adaptive Review

| Task type | Review focus |
| :--- | :--- |
| `code-generation` | Correctness, style, edge cases |
| `security` | Injection flaws, secrets, auth |
| `documentation` | Completeness, formatting, links |
| `debugging` | Root cause addressed, no regressions |
| `configuration` | Syntax, path correctness, security |

> [!NOTE]
> Unlike `ai-router`, the orchestrator supports parallel subtask execution (independent tasks run concurrently) and automatic capability-based skill routing. The DAG engine provides formal guarantees against deadlocks and cascading failures.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-10 via @ai-docs update -->
