# OpenCode Agents

Standalone agent files in `agent/` that you copy into OpenCode's agent directory to install. Each agent monitors incoming requests and routes them to the appropriate skill or sub-agent pipeline.

Both agents follow the same pattern:
1. Copy the `.md` file to `~/.config/opencode/agents/`
2. Run `--init` to write `opencode.json` with required sub-agents
3. Restart OpenCode

---

## ROUTER — Adaptive Route Agent

Routes complex tasks by classifying requests into three fixed modes (quick/plan/debug) and delegating to specialised sub-agents via `skill("ai-router")`.

**File:** `agent/ROUTER.md`

### Installation

```bash
# Windows
copy agent\ROUTER.md %USERPROFILE%\.config\opencode\agents\ROUTER.md

# macOS / Linux
cp agent/ROUTER.md ~/.config/opencode/agents/ROUTER.md
```

### Setup

```text
@ai-router --init
```

This asks which models to use for each role and writes `opencode.json` with four sub-agents:

| Sub-agent | Role |
|-----------|------|
| `ai-router-planner` | Strategic planning, task breakdown |
| `ai-router-executor` | Code execution, applying changes |
| `ai-router-reviewer` | Full review (plan mode) |
| `ai-router-reviewer-flash` | Lightweight review (quick/debug mode) |

### Pipeline

| Mode | Trigger | Execution |
|------|---------|-----------|
| **quick** | Default for short requests | executor(flash) → review(flash or skip) |
| **plan** | Action verbs or > 150 chars | planner(pro) → executor × N → review(pro) → fix loop |
| **debug** | "error", "fail", "bug" | read → executor → review(flash) → fix → log |

> **Cardinal rule:** load the full `@ai-router` skill only when the request needs the formal pipeline. For trivial or single-edit tasks, answer directly.

---

## ORCHESTRATOR — Intelligent Orchestrator Agent

Classifies requests by intent, decomposes them into a DAG of subtasks with dependency resolution, executes via an 8-state machine, and auto-routes to the best available skill or agent.

**File:** `agent/ORCHESTRATOR.md`

### Installation

```bash
# Windows
copy agent\ORCHESTRATOR.md %USERPROFILE%\.config\opencode\agents\ORCHESTRATOR.md

# macOS / Linux
cp agent/ORCHESTRATOR.md ~/.config/opencode/agents/ORCHESTRATOR.md
```

### Setup

```text
@ai-orchestrator --init
```

Writes `opencode.json` with four sub-agents:

| Sub-agent | Role |
|-----------|------|
| `ai-orchestrator-planner` | Strategic planning, dep types |
| `ai-orchestrator-executor` | Code/task execution |
| `ai-orchestrator-reviewer` | Full review (plan mode) |
| `ai-orchestrator-reviewer-flash` | Lightweight review (quick/debug) |

### Pipeline

| Mode | Trigger | Execution |
|------|---------|-----------|
| **quick** | Default for short requests | executor(flash) → review(flash or skip) |
| **plan** | Classifier (intent-based) | classifier → registry → planner → DAG engine → executor/skill → review(adaptive) → fix loop |
| **debug** | "error", "fail", "bug" | read → executor → review(flash) → fix → log |

Unlike ROUTER (fixed keyword mode detection), ORCHESTRATOR uses **dynamic classification** via a structured LLM prompt that outputs `{mode, confidence, capabilities_needed, suggested_skills}`. It also maintains a **capability registry** of all installed skills for automatic routing.

For plan-mode, it builds a formal Directed Acyclic Graph (DAG) with an 8-state task machine (READY/RUNNING/BLOCKED/COMPLETED/FAILED/CANCELLED/SKIPPED/PAUSED), cascade failure propagation, and deadlock detection — all managed by a Python CLI engine (`dag.py`, stdlib only).

### Key differences from ROUTER

| Aspect | ROUTER | ORCHESTRATOR |
|--------|--------|--------------|
| Mode detection | Keyword heuristics | LLM-based + fallback |
| Execution model | Linear pipeline | DAG with dependency resolution |
| Skill routing | Manual via subtask hints | Auto via capability registry |
| State machine | None (sequential) | 8-state FSM + cascade + deadlock |
| Parallel execution | No | Yes (independent subtasks) |

---

## Choosing an agent

| Use case | Agent |
|----------|-------|
| Fixed pipeline, simple multi-step tasks | ROUTER |
| Complex dependency chains, cross-skill orchestration | ORCHESTRATOR |
| First time setting up OpenCode agents | Either (ROUTER is simpler to understand) |

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
