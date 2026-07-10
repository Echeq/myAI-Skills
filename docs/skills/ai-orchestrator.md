# ai-orchestrator

> **Trigger:** `@ai-orchestrator` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Orchestration

[📂 Skill Index](/docs/README.md) → **ai-orchestrator**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Quick | `@ai-orchestrator --quick` | executor(flash) → review(flash or skip) for simple tasks |
| Plan | `@ai-orchestrator --plan` | Full pipeline: classifier → registry → planner → DAG engine → executor → review → fix loop |
| Debug | `@ai-orchestrator --debug` | read context → executor → review(flash) → fix → log |
| Init | `@ai-orchestrator --init` | Configure sub-agents in opencode.json via interactive setup |

> [!TIP]
> This is a technical engine called by the ORCHESTRATOR agent. Most users should invoke ORCHESTRATOR directly rather than this skill.

## Overview

DAG-based task orchestration engine. Implements dynamic classification (LLM-based intent detection), capability registry lookup (auto-discovers installed skills), 8-state task lifecycle, cascade failure propagation, and deadlock detection. Called by the ORCHESTRATOR agent via `skill("ai-orchestrator")`. Not user-facing.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Auto-classify request — routes to quick, plan, or debug mode |
| `--quick` | Fast execution: executor(flash) → review(flash or skip) |
| `--plan` | Full pipeline: classifier → registry → planner → DAG engine → executor/skill → review → fix |
| `--debug` | Debug mode: read context → executor → review(flash) → fix → log |
| `--init` | Interactive setup: configure sub-agents and write opencode.json |
| `--cancel <id>` | Cancel a task by ID (no cascade — dependents become deadlock-detected) |
| `--cancel-all` | Cancel all running tasks |
| `--status` | Show current DAG status with task states |

## DAG Engine

A Python CLI (`dag.py`, stdlib only) manages the task lifecycle with these states:

```
READY → RUNNING → COMPLETED
                  → FAILED → (retry → READY)
         BLOCKED → READY (when deps complete)
         CANCELLED (no cascade)
         SKIPPED
         PAUSED
```

Commands: `init <plan.json>`, `run`, `complete <id>`, `fail <id> <reason>`, `cancel <id>`, `retry <id>`, `status`, `dump`.

> [!NOTE]
> Requires 4 sub-agents configured in `opencode.json` (run `@ai-orchestrator --init` to generate): planner (pro), executor (flash), reviewer (pro), reviewer-flash (flash).

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
