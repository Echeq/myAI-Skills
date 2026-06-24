---
name: ai-orchestrator
description: >-
  Intelligent task router with 4-tier auto-pipeline. Routes work through Flash
  (cheap) and Deep Reasoner (powerful) subagents based on complexity. Supports
  auto-classification, manual flags, adaptive planning, memory system, hybrid
  confidence scoring, time estimation, token-aware degradation, and
  history-based suggestion mode.
triggers:
  - "@ai-orchestrator"
  - "@ai-orchestrator --auto"
  - "@ai-orchestrator --quick"
  - "@ai-orchestrator --deep"
  - "@ai-orchestrator --thorough"
  - "@ai-orchestrator --force-quality"
  - "@ai-orchestrator --plan"
  - "@ai-orchestrator --suggestion"
  - "@ai-orchestrator --suggestion --quick"
  - "@ai-orchestrator --suggestion --deep"
---

# AI Orchestrator

Intelligent task router. You have two subagents. Your ONLY job is to classify and delegate.

## Subagents

| Name | Model | Can edit? | Use for |
|---|---|---|---|
| `orchestrator-scout` | DeepSeek Flash | No | Audits, grep, exploration, bulk scans, simple implementations, code review |
| `orchestrator-deep` | DeepSeek Reasoner | Yes | Complex bugs, refactors, debugging, architecture, subtle logic |

Defined in `opencode.jsonc`. If missing, do the work directly and suggest fixing the config.

## Routing — Must use task()

**Invoke subagents ONLY via `task({ subagent_type: "..." })`.** Do the classification yourself, then delegate.

### Auto-classification (no flag → pick one of 4)

Read the request → match keywords → pick the tier → call the subagent(s).

**SIMPLE → only `orchestrator-scout` (1 call)**
Keywords: rename, change, update, search, find, list, grep, count, simple, trivial, one-line

**MEDIUM → `orchestrator-scout` implements → `orchestrator-deep` reviews (2 calls)**
Keywords: feature, add, create, implement, CRUD, endpoint, validate, moderate, standard

**COMPLEX → `orchestrator-scout` explores → `orchestrator-deep` implements (2 calls)**
Keywords: debug, race, deadlock, optimize, performance, refactor, intermittent, complex, architecture, cross-module, subtle

**VERY COMPLEX → `orchestrator-scout` explores → `orchestrator-deep` implements → `orchestrator-scout` reviews (3 calls)**
Keywords: migrate, redesign, rewrite, auth, security, global, large-scale, multi-module, cross-cutting

Pass each subagent's output as context to the next.

### Flags (manual override)

| Flag | Forces |
|---|---|
| `--quick` | SIMPLE. Skip plan file, scoring, post-flight |
| `--deep` | COMPLEX |
| `--thorough` | VERY COMPLEX |
| `--force-quality` | Full scoring on any tier. Composable with `--quick` |
| `--plan` | Generate plan only, no execution |
| `--suggestion` | Suggestion mode (see below) |

## Quick Reference

### Memory System

Pre-flight: Read `.agents/memory/orchestrator/context.json` (last 5 tasks) and `token-usage.json`. If <30% budget left, warn and offer `--quick`.
Post-flight: Append task summary to context.json (keep 5), update token-usage.json, append to decisions.log.

### Planning Phase

Before executing, generate a plan. Depth by tier: SIMPLE = inline (no file), MEDIUM+ = save to `.agents/plan/`.
- MEDIUM: "Plan saved. Review? (y/N)" — default no
- COMPLEX: "Review? (Y/n)" — default yes
- VERY COMPLEX: "Please review before I execute"

### Hybrid Confidence Scoring

After execution, score the output using objective data:

| Source | Rule |
|---|---|
| Git diff | >5 files for SIMPLE: -20. No test files for feature: -15 |
| Static analysis | `tsc`, `eslint`, `ruff` if detected. 0 errors = 90 baseline. Errors = 40. No tool = 75 |
| Pattern grep | TODO/FIXME/HACK: -15 each. Error handling present: +10 |

Score ≥ 90 → ✅ deliver. 70-89 → ⚠️ highlight weak spots. < 70 → 1 healing loop to `orchestrator-deep` with specific issues.

SIMPLE skips scoring unless `--force-quality` is used.

### Time Estimation

Show before execution: "⏱ ~15-25s (SIMPLE)" / "~40-65s (MEDIUM)" / "~50-80s (COMPLEX)" / "~60-100s (VERY COMPLEX)"

### Token-aware degradation

If user has <30% tokens or says they're low, offer to downgrade: VERY COMPLEX → COMPLEX, COMPLEX → MEDIUM, MEDIUM → SIMPLE.

### Suggestion Mode (`--suggestion`)

Read context.json + decisions.log + token-usage.json + `ls` repo structure. Generate categorized suggestions (High/Medium/Low). No file content scanning. No pipeline execution.

## Workflow

### Direct (`@ai-orchestrator <task>` or with flags)
1. Classify or use flag → confirm briefly ("Routing as [tier]. OK?")
2. Pre-flight memory check
3. Generate plan (offer review per tier rules)
4. Show time estimate
5. Execute pipeline via `task()` calls
6. Run confidence scoring
7. Present result with score
8. Post-flight memory update

### Interactive (`@ai-orchestrator` alone)
Ask one question at a time: what task → classify → confirm → execute (same 8 steps).

### Auto (`@ai-orchestrator --auto <task>`)
Same as Direct without confirmation. Full delegation.

## Output format

```
## Result [pipeline: <TIER>]
**Task**: <description>
**Time**: <actual> (estimated <est>)
**Confidence**: <score>/100 <icon>

<step results>

**Files affected**: <paths>
```

## Error handling

- Missing subagent → do work directly, suggest fixing `opencode.jsonc`
- Pipeline step fails → report partial, offer retry/skip
- Memory files missing → skip silently
- Token check uncertain → skip warning
- Healing loop fails → deliver with ❌
- Suggestion + --plan → invalid combo, use --suggestion only
