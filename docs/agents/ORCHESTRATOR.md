# ORCHESTRATOR

Intelligent task orchestrator. Classifies requests by intent, decomposes them into a DAG of subtasks with dependency resolution, executes via a formal state machine, and auto-routes to the best available skill or agent.

> **File:** `agent/ORCHESTRATOR.md`

## Quick Start

1. Copy `agent/ORCHESTRATOR.md` to `~/.config/opencode/agents/ORCHESTRATOR.md`
2. Run `@ai-orchestrator --init` to write `opencode.json` with the 4 required sub-agents
3. Restart OpenCode

## Description

ORCHESTRATOR uses **dynamic classification** via a structured LLM prompt that outputs `{mode, confidence, capabilities_needed, suggested_skills}`. It maintains a **capability registry** of all installed skills for automatic routing. For plan-mode, it builds a formal Directed Acyclic Graph (DAG) with an 8-state task machine, cascade failure propagation, and deadlock detection — all managed by a Python CLI engine (`dag.py`, stdlib only).

## Pipeline Modes

| Mode | Trigger | Execution |
|---|---|---|
| **quick** | Default for short requests | executor(flash) → review(flash or skip) |
| **plan** | Classifier (intent-based) | classifier → registry → planner → DAG engine → executor/skill → review(adaptive) → fix loop |
| **debug** | "error", "fail", "bug" | read → executor → review(flash) → fix → log |

## Key Features

- **Dynamic classification**: LLM-based intent detection (not keyword heuristics)
- **Capability registry**: Auto-discovers installed skills and routes subtasks accordingly
- **DAG engine**: Formal Directed Acyclic Graph with 8-state machine
- **Cascade propagation**: If task A fails, all tasks depending on A (transitively) also fail
- **Deadlock detection**: If a dependency is CANCELLED, dependents auto-fail instead of blocking forever
- **Cancel without cascade**: `cancel <id>` stops a task without cascading (dependents become deadlock-detected)
- **Retry with reversion**: Failed tasks can be retried, reverting cascade-failed dependents back to BLOCKED

## Differences from ROUTER

| Aspect | ROUTER | ORCHESTRATOR |
|---|---|---|
| Mode detection | Keyword heuristics | LLM-based + fallback |
| Execution model | Linear pipeline | DAG with dependency resolution |
| Skill routing | Manual via subtask hints | Auto via capability registry |
| State machine | None (sequential) | 8-state FSM + cascade + deadlock |
| Parallel execution | No | Yes (independent subtasks) |

## DAG Engine

The Python CLI engine (`dag.py`) manages the task lifecycle:

```
python dag.py init <plan.json>   # Load plan, validate, write state
python dag.py run                # Pop next READY task or signal done
python dag.py complete <id>      # Mark task COMPLETED, unblock deps
python dag.py fail <id> <reason> # Mark task FAILED, cascade
python dag.py cancel <id>        # Cancel task (NO cascade)
python dag.py retry <id>         # Retry a FAILED task
python dag.py status             # Print human-readable state table
python dag.py dump               # Print full task_states.json
```

States: READY, RUNNING, BLOCKED, COMPLETED, FAILED, CANCELLED, SKIPPED, PAUSED

---

**[⬆ Back to Top](#)** | **[📂 Agent Index](/docs/agents/README.md)**
