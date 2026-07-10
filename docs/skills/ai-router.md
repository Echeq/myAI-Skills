# ai-router

> **Trigger:** `@ai-router` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Orchestration

[📂 Skill Index](/docs/README.md) → **ai-router**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Quick | `@ai-router --quick` | executor(flash) → review(flash or skip) for straightforward tasks |
| Plan | `@ai-router --plan` | planner(pro) → executor × N → review(pro) → fix loop for complex tasks |
| Debug | `@ai-router --debug` | read files → executor → review(flash) → fix → log |
| Init | `@ai-router --init` | Configure sub-agents in opencode.json via interactive setup |

> [!TIP]
> This is a technical engine called by the ROUTER agent. Most users should invoke ROUTER directly rather than this skill.

## Overview

Technical pipeline engine for task routing. Implements a 3-mode pipeline (quick/plan/debug) with planner → executor → reviewer sub-agents. Each role uses a different model tier: Pro for planning and major reviews, Flash for execution and minor fixes. Called by the ROUTER agent via `skill("ai-router")`. Not user-facing.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Auto-classify: routes to quick, plan, or debug based on request content and length |
| `--quick` | Default for short requests: executor(flash) → review(flash or skip for trivial) |
| `--plan` | For complex requests: planner(pro) → executor × N → review(pro) → fix loop |
| `--debug` | For errors/bugs: read context → executor → review(flash) → fix → log |
| `--init` | Interactive setup: choose models for each role, write opencode.json |

## Pipeline Details

- **Model-tier routing**: Pro model for planning and major fixes; Flash for execution and minor fixes
- **Severity-based fix retry**: Minor issues (naming, style) → Flash fix; Major issues (architecture, security) → Pro fix
- **Escalation**: If the reviewer rejects after a fix pass, escalate to Pro regardless of severity

> [!NOTE]
> Requires 4 sub-agents configured in `opencode.json` (run `@ai-router --init` to generate): planner (pro), executor (flash), reviewer (pro), reviewer-flash (flash). State is persisted to `assets/state/history.md` and plans to `assets/plan/`.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
