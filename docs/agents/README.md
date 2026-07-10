# Agent Index

Standalone OpenCode agents for AI-assisted development. Unlike skills (invoked via `@` triggers), agents are installed by copying the `.md` file to `~/.config/opencode/agents/` and they monitor incoming requests to route them to the appropriate pipeline.

## Overview

| Agent | File | Role | Execution Model |
|---|---|---|---|
| **ROUTER** | `agent/ROUTER.md` | Adaptive orchestration — routes tasks by complexity | Fixed 3-mode pipeline (planner → executor → reviewer) |
| **ORCHESTRATOR** | `agent/ORCHESTRATOR.md` | Intelligent orchestration — dependency-aware multi-step execution | DAG engine (8-state FSM, cascade, deadlock detection) |
| **DELLA** | `agent/DELLA.md` | Strategic planning consultant — produces adaptive plans | Read-only planning (Discover → Examine → Link → Layout → Assess) |

## Installation

All agents follow the same installation pattern:

```bash
# Windows:
copy agent\<AGENT>.md %USERPROFILE%\.config\opencode\agents\<AGENT>.md

# macOS / Linux:
cp agent/<AGENT>.md ~/.config/opencode/agents/<AGENT>.md
```

Or place the agent file anywhere listed in your `opencode.json` `agent.paths`.

## Choosing an Agent

| Use case | Agent |
|---|---|
| Fixed pipeline, simple multi-step tasks | **ROUTER** |
| Complex dependency chains, cross-skill orchestration | **ORCHESTRATOR** |
| Strategic planning, capability discovery, workflow design | **DELLA** |
| First time setting up OpenCode agents | Either (ROUTER is simpler to understand) |

## Relationship with Skills

Agents orchestrate and plan; skills execute. A typical flow:

```
DELLA (plan) → ROUTER or ORCHESTRATOR (execute) → skills (implement)
```

Each agent doc below details its specific workflow, installation, and usage.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
