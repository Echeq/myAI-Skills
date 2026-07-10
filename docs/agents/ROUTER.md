# ROUTER

Adaptive orchestration agent. Classifies requests by complexity and routes them to the appropriate execution path — direct (flash-tier) for quick tasks, or skill-loaded pipeline (pro-tier) for complex work.

> **File:** `agent/ROUTER.md`

## Quick Start

1. Copy `agent/ROUTER.md` to `~/.config/opencode/agents/ROUTER.md`
2. Run `@ai-router --init` to write `opencode.json` with the 4 required sub-agents
3. Restart OpenCode

## Description

ROUTER classifies incoming requests into three modes using keyword heuristics. It delegates strategic planning to the `ai-router-planner` sub-agent (Pro model), execution to `ai-router-executor` (Flash), and review to either `ai-router-reviewer` (Pro) or `ai-router-reviewer-flash` depending on the mode. After execution, it logs outcomes to `assets/state/history.md`.

## Pipeline Modes

| Mode | Trigger | Execution |
|---|---|---|
| **quick** | Default for short requests | executor(flash) → review(flash or skip for trivial) |
| **plan** | Action verbs (build/create/implement) or length > 150 chars | planner(pro) → executor × N → review(pro) → fix loop |
| **debug** | "error", "fail", "bug" | read context → executor → review(flash) → fix → log |

## Key Features

- **Model-tier routing**: Pro model for planning and major fixes; Flash model for execution and minor fixes
- **Severity-based fix retry**: Minor issues (naming, style) → Flash fix; Major issues (architecture, security) → Pro fix
- **Escalation**: If rejected after fix pass, escalate to Pro regardless of severity
- **State persistence**: Plans saved to `assets/plan/`; current state in `assets/state/current_plan.md`; history in `assets/state/history.md`

## Configuration

Requires 4 sub-agents in `opencode.json`:

| Sub-agent | Model | Prompt |
|---|---|---|
| `ai-router-planner` | Pro | `references/manager.md` |
| `ai-router-executor` | Flash | `references/worker.md` |
| `ai-router-reviewer` | Pro | `references/supervisor.md` |
| `ai-router-reviewer-flash` | Flash | `references/supervisor-lite.md` |

---

**[⬆ Back to Top](#)** | **[📂 Agent Index](/docs/agents/README.md)**
