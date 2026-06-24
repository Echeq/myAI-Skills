# ai-orchestrator

Intelligent task router with 4-tier auto-pipeline. Routes work through Flash (cheap) and Deep Reasoner (powerful) subagents based on complexity. Includes memory system, adaptive planning, hybrid confidence scoring, time estimation, token-aware degradation, and history-based suggestion mode.

> **Trigger:** `@ai-orchestrator` | `@ai-orchestrator --auto` | `@ai-orchestrator --quick` | `@ai-orchestrator --deep` | `@ai-orchestrator --thorough` | `@ai-orchestrator --force-quality` | `@ai-orchestrator --plan` | `@ai-orchestrator --suggestion` | `@ai-orchestrator --suggestion --quick` | `@ai-orchestrator --suggestion --deep`

## Quick Start

**Full delegation (recommended):**
1. Type `@ai-orchestrator add validation to the login form`.
2. The orchestrator runs pre-flight, generates an adaptive plan, classifies as MEDIUM, executes the pipeline, runs confidence scoring, and updates memory.
3. No flags needed. Full result with confidence score.

**Direct with flags:**
- `@ai-orchestrator --quick rename this variable` &rarr; forces SIMPLE (Flash only), skips planning file and scoring.
- `@ai-orchestrator --deep fix the race condition` &rarr; forces COMPLEX (Flash explores &rarr; Deep implements).
- `@ai-orchestrator --thorough migrate auth to JWT` &rarr; forces VERY COMPLEX (3-step pipeline).
- `@ai-orchestrator --force-quality add a button` &rarr; SIMPLE classification but full scoring (git + static + patterns).
- `@ai-orchestrator --quick --force-quality add a button` &rarr; SIMPLE pipeline + full scoring (barato pero verificado).

**Plan only:**
1. Type `@ai-orchestrator --plan redesign scheduling system`.
2. The orchestrator generates a detailed plan and saves it to `.agents/plan/`. No code is executed.

**Interactive (no task given):**
1. Type `@ai-orchestrator`.
2. The skill asks one question at a time, classifies, plans, and executes.

## Description

Routes requests through an optimal pipeline of two subagents — `orchestrator-scout` (DeepSeek Flash, cheap) and `orchestrator-deep` (DeepSeek Reasoner, expensive) — based on task complexity. The full lifecycle of a task:

```
User input
  → Memory pre-flight (context injection + token check)
  → Adaptive planning (plan depth by tier, review optional)
  → Time estimation
  → Pipeline execution (1 of 4 tiers)
  → Hybrid confidence scoring (git + static + patterns)
  → Output with confidence level
  → Memory post-flight (rotate, log, update tokens)
```

Separate modes exist for planning-only (`--plan`) and for generating prioritized improvement suggestions from session history and repo structure (`--suggestion`). Suggestion mode reads memory files and directory listings — it never scans file contents.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-orchestrator <task>` | Full auto-pipeline: classify, plan, execute, score, persist |
| `@ai-orchestrator --auto <task>` | Same as above (explicit full delegation) |
| `@ai-orchestrator --quick <task>` | Force SIMPLE tier: Flash only, no plan file, no scoring, no memory post-flight |
| `@ai-orchestrator --deep <task>` | Force COMPLEX tier: Flash explores &rarr; Deep implements |
| `@ai-orchestrator --thorough <task>` | Force VERY COMPLEX tier: 3-step pipeline with double validation |
| `@ai-orchestrator --force-quality <task>` | Full scoring on any tier (git + static analysis + pattern grep + healing loop) |
| `@ai-orchestrator --quick --force-quality <task>` | SIMPLE execution with full scoring |
| `@ai-orchestrator --plan <task>` | Generate and save plan only, no execution |
| `@ai-orchestrator --suggestion` | Analyze history + repo structure, return prioritized suggestions |
| `@ai-orchestrator --suggestion --quick` | Suggestions from Flash only, no Deep refinement |
| `@ai-orchestrator --suggestion --deep` | Flash suggestions + Deep refinement and prioritization |
| `@ai-orchestrator --suggestion <category>` | Filter suggestions by category (tokens, workflow, docs, architecture, performance, security) |
| `@ai-orchestrator` | Interactive mode: ask &rarr; classify &rarr; plan &rarr; confirm &rarr; execute |

## Routing Decision Table

| Tier | Pipeline | Calls | Estimated time | Typical tasks |
| :--- | :--- | :--- | :--- | :--- |
| SIMPLE | Flash &rarr; done | 1 cheap | ~15-25s | Rename, grep, typo fix, one-file change |
| MEDIUM | Flash implements &rarr; Deep reviews | 1 cheap + 1 review | ~40-65s | New feature, CRUD, standard bug with stack trace |
| COMPLEX | Flash explores &rarr; Deep implements | 1 cheap + 1 focused | ~50-80s | Race conditions, perf opt, cross-module refactor |
| VERY COMPLEX | Flash explores &rarr; Deep implements &rarr; Flash reviews | 2 cheap + 1 expensive | ~60-100s | Auth rewrite, DB migration, 5+ module refactor |

## Memory System

Persistent state across sessions. Files stored in `.agents/memory/orchestrator/` (gitignored):

| File | Purpose |
| :--- | :--- |
| `context.json` | Last 5 completed tasks + project focus |
| `token-usage.json` | Daily token budget tracking |
| `decisions.log` | Append-only routing decisions |

**Pre-flight**: Reads context and injects into the prompt. Checks token budget — warns if <30% remaining and offers to degrade.

**Post-flight**: Rotates the task list (keep last 5), updates token usage estimate, logs the routing decision with timestamp and rationale.

## Planning Phase

Before execution, the orchestrator generates a plan. Plan depth matches the tier:

| Tier | Plan format | File saved | Review required |
| :--- | :--- | :--- | :--- |
| SIMPLE | 1-2 sentence inline | No | No |
| MEDIUM | Bullet-point list | Yes | No (default) |
| COMPLEX | Detailed sections | Yes | Yes (default) |
| VERY COMPLEX | Full plan with risks | Yes | Yes |

Plan files are saved to `.agents/plan/<task-slug>-YYYY-MM-DD.md` (gitignored). The `--plan` flag generates a plan without executing.

## Quality Assurance (Hybrid Confidence Scoring)

Uses objective data sources, not model opinion:

| Source | Data | Cost | Baseline |
| :--- | :--- | :--- | :--- |
| Git diff | Files touched, test files, diff size | 0 tokens | Neutral |
| Static analysis | `tsc --noEmit`, `eslint`, `ruff` if tools detected | 0 tokens | 90 (0 errors) / 40 (errors) / 75 (no tool) |
| Pattern grep | TODO, FIXME, HACK, debugger, error handling | 0 tokens | +/- per finding |
| **Model interpretation** | Combines data into final score | ~100 tokens | — |

**Thresholds:**

| Score | Action |
| :--- | :--- |
| ≥ 90 | ✅ Deliver confidently |
| 70-89 | ⚠️ Deliver with weak spots highlighted |
| < 70 | 🔄 Healing loop (1 pass to Deep subagent). If still < 70, deliver with ❌ warning |

**When scoring applies:**

| Tier | Scoring |
| :--- | :--- |
| SIMPLE | Skipped (unless `--force-quality`) |
| MEDIUM | After Deep review |
| COMPLEX | After Deep implementation (replaces manual review) |
| VERY COMPLEX | Final Flash review includes scoring |

## Suggestion Mode

A special mode that generates prioritized improvement suggestions from session history and repo structure. No file content is scanned — only memory files and directory listings.

| Flag | Behavior |
| :--- | :--- |
| `@ai-orchestrator --suggestion` | Read history + structure, generate suggestions via Flash |
| `@ai-orchestrator --suggestion --quick` | Flash only, no Deep refinement |
| `@ai-orchestrator --suggestion --deep` | Flash suggestions + Deep refinement and prioritization |
| `@ai-orchestrator --suggestion <category>` | Filter by: `tokens`, `workflow`, `docs`, `architecture`, `performance`, `security` |

### Data sources

| Source | What it reveals |
| :--- | :--- |
| `context.json` | Last 5 tasks, project focus |
| `decisions.log` | Routing patterns, degradation history |
| `token-usage.json` | Spending trends |
| Repo directory listing | Skill count, doc coverage, missing patterns |

### Output

Suggestions are presented in a categorized table with priority levels (High/Medium/Low) and actionable reasoning.

## Token-Aware Degradation

Two triggers: memory check (<30% remaining) or user declaration (>50% used). Both follow:

| Original | Degraded to | Time saved | Tokens saved |
| :--- | :--- | :--- | :--- |
| VERY COMPLEX | COMPLEX | ~20s | 1 Flash call |
| COMPLEX | MEDIUM | ~15s | Deep implements &rarr; Deep reviews |
| MEDIUM | SIMPLE | ~30s | 1 Deep call eliminated |
| SIMPLE | unchanged | 0 | Nothing to save |

## Time Estimation

Shown before every execution:

> "⏱ Estimated: ~40-65s (MEDIUM — 1 Flash + 1 Deep review)"

With token warning:

> "⚠️ Daily tokens below 30%. Estimated: ~50-80s. Force --quick to reduce to ~20s? (yes/no)"

## Configuration

The skill relies on two subagents defined in `opencode.jsonc` at the repo root:

```
opencode.jsonc
  orchestrator-scout    — DeepSeek Flash, read-only + bash, no edits
  orchestrator-deep     — DeepSeek Reasoner, full tool access
```

Memory and plan directories are auto-created on first use. No additional configuration needed.

---

## File Map

```
.agents/
  memory/orchestrator/            ← Session memory (gitignored)
    context.json                   Last 5 tasks + project focus
    token-usage.json               Daily token tracking
    decisions.log                  Routing decision archive
  plan/                            ← Generated plans (gitignored)
    <task>-YYYY-MM-DD.md           Per-task plan files
  skills/ai-orchestrator/          ← Skill definition
    SKILL.md                       Agent instructions (this skill)

opencode.jsonc                     ← Subagent definitions (orchestrator-scout, orchestrator-deep)

docs/skills/ai-orchestrator.md     ← This documentation page

.gitignore                         ← Ignores memory/ and plan/ directories
```

---

## ADR-001: 4-Tier Pipeline Over Simple OR Routing

**Status:** Adopted 2026-06-24

**Context:** The original design used OR routing — classify a task as "quick" or "deep" and send it to one subagent exclusively. This meant either overspending (Deep on trivial tasks) or underspending (Flash on tasks needing reasoning).

**Decision:** Replace OR with a 4-tier pipeline where subagents can be chained. Each tier represents a distinct cost-quality trade-off:

| Tier | Why it exists |
| :--- | :--- |
| SIMPLE | Tasks Flash can solve alone should not involve Deep at all |
| MEDIUM | Deep *reviewing* costs ~80% less than Deep *implementing*, but catches similar errors |
| COMPLEX | Deep should not waste tokens on grep — let Flash gather context first |
| VERY COMPLEX | High-risk changes need double validation |

**Key insight:** A review pass (MEDIUM) costs far fewer tokens than a full implementation because it only reads a diff and comments. This is the most efficient way to get Deep-level quality on moderately complex tasks.

**Alternatives rejected:**
- Simple OR: overspends on trivial tasks, underspends on complex ones
- Single model: no cost optimization possible
- Always-pipeline: wastes tokens on trivial tasks

---

## ADR-002: Token-Aware Degradation

**Status:** Adopted 2026-06-24

**Context:** Users with daily token budgets can exhaust them quickly if every task routes through Deep. The orchestrator needs visibility into budget without an API.

**Decision:** Add a two-trigger degradation system (memory file <30% or user declaration >50%). Degradation is opt-in, not automatic. Quality-tuned to minimize impact while maximizing savings.

**Boundaries:**
- Only warns once per session to avoid nagging
- Degradation is opt-in — user choice
- If memory files are missing, skip the warning

---

## ADR-003: Hybrid Confidence Scoring

**Status:** Adopted 2026-06-24

**Context:** Pure self-evaluation (model asks itself 3 questions) is unreliable — LLMs are poor at detecting their own errors. A scoring system needs objective data to be trustworthy.

**Decision:** Use objective data sources (git diff, static analysis tools, pattern grep) and let the model only interpret the results. This moves the model from "opinion" to "analysis of facts."

**Why 3 sources:**
- Git diff: always available, detects scope mismatches instantly
- Static analysis: zero-cost error detection if tools exist
- Pattern grep: catches common red flags (TODO, debugger, missing error handling)

**Why self-healing works now:** The healing loop receives specific, actionable issues ("2 type errors in src/auth.ts", "missing test files"), not vague instructions ("review the code").

**Optimization:**
- Skip entirely on `--quick`
- Force with `--force-quality` on any tier
- Only 1 healing attempt (not 2) to limit cost

---

## ADR-004: Adaptive Planning by Tier

**Status:** Adopted 2026-06-24

**Context:** Adding a planning phase to every task would waste tokens on trivial work and add friction for simple requests.

**Decision:** Plan depth adapts to the classified tier — SIMPLE plans are inline and consumed immediately; VERY COMPLEX plans are detailed files with mandatory review. This keeps planning overhead proportional to task value.

---

## Complexity Analysis

### Pipeline execution (per tier)

| Tier | Steps | Subagent calls | Max context passed | Estimated time |
| :--- | :--- | :--- | :--- | :--- |
| SIMPLE | 1 | 1x Flash | — | ~15-25s |
| MEDIUM | 2 | 1x Flash, 1x Deep | Flash output (~2-5 KB) | ~40-65s |
| COMPLEX | 2 | 1x Flash, 1x Deep | Flash exploration (~5-15 KB) | ~50-80s |
| VERY COMPLEX | 3 | 2x Flash, 1x Deep | ~10-25 KB accumulated | ~60-100s |

### Scoring complexity

O(1) per source. Git diff, grep, and static analysis are single command executions. No loops.

### Memory operations

O(1) file reads and writes. ~50 tokens total overhead.

---

## Dependency Graph

```
@ai-orchestrator
  ├── Reads     → task description (user input)
  ├── Reads     → .agents/memory/orchestrator/context.json (pre-flight)
  ├── Reads     → .agents/memory/orchestrator/token-usage.json (pre-flight)
  ├── Writes    → .agents/plan/<task>-<date>.md (planning phase)
  ├── Invokes   → orchestrator-scout (via Task tool)
  │                ├── Read, Glob, Grep, List, Bash
  │                └── No edit/write access
  ├── Invokes   → orchestrator-deep (via Task tool)
  │                ├── Read, Glob, Grep, List, Bash
  │                └── Full edit/write access
  ├── Executes  → git diff, tsc/eslint/ruff (confidence scoring)
  ├── Writes    → .agents/memory/orchestrator/context.json (post-flight)
  ├── Writes    → .agents/memory/orchestrator/token-usage.json (post-flight)
  ├── Appends   → .agents/memory/orchestrator/decisions.log (post-flight)
  └── Outputs   → result summary with confidence score
```

**External dependencies:** None beyond OpenCode's built-in Task tool and the configured LLM provider.

---

## Stress / Edge Cases

| Case | Handling |
| :--- | :--- |
| Memory files corrupt or missing | Skip pre-flight silently; regenerate defaults on post-flight |
| Plan directory missing | Create `.agents/plan/` on first write |
| Static analysis tools not found | Skip that source; baseline = 75 for that category |
| Subagent not configured | Fall back to direct work; suggest verifying `opencode.jsonc` |
| Pipeline step fails or times out | Report partial results; offer retry or skip |
| Ambiguous classification | Ask 1-2 clarifying questions before committing |
| Token budget unknown (no memory) | Skip degradation warning |
| User declines degradation | Proceed with original tier; do not ask again this session |
| Very large task (100+ files) | Pipeline works but context limits may apply; split suggested |
| Repeated `--quick` on complex tasks | Execute as requested; no override |
| Subagent returns unusable output | Offer to re-run with the other subagent |
| Healing loop fails to improve | Deliver with ❌ warning regardless |
| Concurrent sessions | Token tracking is per-install; orchestrator cannot enforce cross-session limits |
| `--plan` on already completed task | Regenerates plan from scratch; does not reuse cached plans |

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
