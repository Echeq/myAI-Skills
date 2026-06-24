# ai-orchestrator

Intelligent task router with 4-tier auto-pipeline. Routes work through Flash (cheap) and Deep Reasoner (powerful) subagents based on complexity.

> **Trigger:** `@ai-orchestrator` | `@ai-orchestrator --auto` | `@ai-orchestrator --quick` | `@ai-orchestrator --deep` | `@ai-orchestrator --thorough`

## Quick Start

**Direct with auto-pipeline (recommended):**
1. Type `@ai-orchestrator add validation to the login form`.
2. The orchestrator classifies it as MEDIUM.
3. Flash implements the validation. Deep reviews the diff.
4. Summary is presented.

**Direct with flag:**
- `@ai-orchestrator --quick rename this variable` &rarr; forces SIMPLE (Flash only)
- `@ai-orchestrator --deep fix the race condition` &rarr; forces COMPLEX (Flash explores &rarr; Deep implements)
- `@ai-orchestrator --thorough migrate auth to JWT` &rarr; forces VERY COMPLEX (3-step pipeline)

**Interactive (no task given):**
1. Type `@ai-orchestrator`.
2. The skill asks: "What do you need help with? Describe the task."
3. Answer. The skill classifies, confirms the route with you, and executes.

## Description

Routes requests through an optimal pipeline of two subagents — `orchestrator-scout` (DeepSeek Flash, cheap) and `orchestrator-deep` (DeepSeek Reasoner, expensive) — based on task complexity. The pipeline is designed to spend tokens only where they add value:

- **SIMPLE**: Flash alone. Cheap tasks stay cheap.
- **MEDIUM**: Flash implements, Deep reviews. Quality of a powerful model at the cost of a review, not an implementation.
- **COMPLEX**: Flash explores (cheap context gathering), Deep implements (power focused on the actual work, not on grep).
- **VERY COMPLEX**: Full 3-step chain with double validation.

Includes token-aware degradation: if >50% of daily tokens are used, the orchestrator offers to downgrade to a cheaper tier.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-orchestrator <task>` | Auto-pipeline: classify and execute in optimal tier |
| `@ai-orchestrator --auto <task>` | Same as above (explicit auto) |
| `@ai-orchestrator --quick <task>` | Force SIMPLE tier (Flash only) |
| `@ai-orchestrator --deep <task>` | Force COMPLEX tier (Flash explores &rarr; Deep implements) |
| `@ai-orchestrator --thorough <task>` | Force VERY COMPLEX tier (3-step pipeline) |
| `@ai-orchestrator` | Interactive mode: ask &rarr; classify &rarr; confirm &rarr; execute |

## Routing Decision Table

| Tier | Pipeline | Calls | Token cost | Typical tasks |
| :--- | :--- | :--- | :--- | :--- |
| SIMPLE | Flash &rarr; done | 1 cheap | Minimal | Rename, grep, typo fix, one-file change |
| MEDIUM | Flash implements &rarr; Deep reviews | 1 cheap + 1 review | Low | New feature, CRUD, standard bug with stack trace |
| COMPLEX | Flash explores &rarr; Deep implements | 1 cheap + 1 focused expensive | Optimal | Race conditions, perf opt, cross-module refactor |
| VERY COMPLEX | Flash explores &rarr; Deep implements &rarr; Flash reviews | 2 cheap + 1 expensive | Higher, justified | Auth rewrite, DB migration, 5+ module refactor |

## Token-Aware Degradation

If daily tokens exceed 50%, the orchestrator offers to downgrade:

| Original | Degraded to | Savings |
| :--- | :--- | :--- |
| VERY COMPLEX | COMPLEX | Skips final Flash review (1 call saved) |
| COMPLEX | MEDIUM | Deep reviews instead of implements (much cheaper) |
| MEDIUM | SIMPLE | Skips Deep review entirely (1 call saved) |
| SIMPLE | unchanged | Already minimal |

## Configuration

The skill relies on two subagents defined in `opencode.jsonc` at the repo root:

```
opencode.jsonc
  orchestrator-scout    — DeepSeek Flash, read-only + bash, no edits
  orchestrator-deep     — DeepSeek Reasoner, full tool access
```

No additional configuration files are needed. The skill is self-contained in `.agents/skills/ai-orchestrator/SKILL.md`.

---

## File Map

```
.agents/skills/ai-orchestrator/     ← Skill definition
  SKILL.md                          ← Agent instructions (this skill)

opencode.jsonc                       ← Subagent definitions (orchestrator-scout, orchestrator-deep)

docs/skills/ai-orchestrator.md       ← This documentation page
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
- Always-pipeline (all tasks go through 3 steps): wastes tokens on trivial tasks

---

## ADR-002: Token-Aware Degradation

**Status:** Adopted 2026-06-24

**Context:** Users with daily token budgets can exhaust them quickly if every task routes through Deep. The orchestrator has no visibility into the user's remaining budget.

**Decision:** Add an optional degradation step. Before executing, if >50% of daily tokens are consumed, the orchestrator warns and offers to downgrade one tier. The degradation rules are designed to minimize quality impact while maximizing token savings.

**Boundaries:**
- Only warns once per session to avoid nagging
- Degradation is opt-in, not automatic — user choice
- If remaining budget is unknown, skip the warning

---

## Complexity Analysis

### Pipeline execution (per tier)

| Tier | Steps | Subagent calls | Max context passed |
| :--- | :--- | :--- | :--- |
| SIMPLE | 1 | 1x Flash | — |
| MEDIUM | 2 | 1x Flash, 1x Deep | Flash output (~2-5 KB) |
| COMPLEX | 2 | 1x Flash, 1x Deep | Flash exploration (~5-15 KB) |
| VERY COMPLEX | 3 | 2x Flash, 1x Deep | ~10-25 KB accumulated |

**Overall:** Linear in pipeline depth. No loops or recursion.

### Classification complexity

O(1) — keyword matching against the user's task description. No file system access is needed for routing.

---

## Dependency Graph

```
@ai-orchestrator
  ├── Reads     → task description (user input)
  ├── Invokes   → orchestrator-scout (via Task tool)
  │                ├── Read, Glob, Grep, List, Bash
  │                └── No edit/write access
  ├── Invokes   → orchestrator-deep (via Task tool)
  │                ├── Read, Glob, Grep, List, Bash
  │                └── Full edit/write access
  ├── Depends on → opencode.jsonc (subagent definitions)
  └── Outputs   → result summary to user
```

**External dependencies:** None beyond OpenCode's built-in Task tool and the configured LLM provider.

---

## Stress / Edge Cases

| Case | Handling |
| :--- | :--- |
| Subagent not configured (missing `opencode.jsonc`) | Falls back to direct work; suggests verifying the config |
| Pipeline step fails or times out | Reports partial results; offers retry or skip to next step |
| Ambiguous classification | Asks 1-2 clarifying questions; does not guess |
| Token budget unknown | Skips the degradation warning silently |
| User declines degradation | Proceeds with original tier; does not ask again in the same session |
| Very large task (100+ files) | Pipeline still works but context limits may apply; suggests splitting into subtasks |
| Repeated `--quick` on complex tasks | Executes as requested; no override |
| Subagent returns unusable output | Offers to re-run with the other subagent or in direct mode |
| Concurrent sessions share token budget | The degradation check is based on what the user reports; orchestrator cannot enforce cross-session limits |

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
