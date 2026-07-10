# DELLA

Strategic planning consultant. Reads project context, analyzes available capabilities, and produces adaptive execution plans with workflow composition, skill chaining, and handoff instructions.

> **File:** `agent/DELLA.md`
> **Acronym:** **D**iscover → **E**xamine → **L**ink → **L**ayout → **A**ssess

## Quick Start

1. Copy `agent/DELLA.md` to `~/.config/opencode/agents/DELLA.md`
2. No setup required — DELLA needs no sub-agents, no `--init`, no `opencode.json` modifications
3. Invoke DELLA with a description of what you need to accomplish

**Example:** `@DELLA` → reads AGENTS.md → scans agents and skills → maps your request → produces a plan at `docs/DELLA_PLAN/plan_2026-07-10_001.md`.

## Description

DELLA is a **read-only, planning-only strategic consultant**. Unlike ROUTER (which executes) and ORCHESTRATOR (which orchestrates execution), DELLA only produces plans. It never writes source code, delegates to sub-agents, or executes tasks. Its sole output is a structured plan document in `docs/DELLA_PLAN/`.

DELLA follows a 5-phase methodology: Discover, Examine, Link, Layout, Assess.

## The D.E.L.L.A. Methodology

### D — Discover

Examines the project's context and constraints.

1. Reads `AGENTS.md` — extracts project rules, conventions, platform info, trigger rules, and generated paths
2. Looks for the `<!-- DELLA-CONTEXT -->` marker for focused context; reads the full file if absent
3. Detects platform: Windows PowerShell (`; if ($?) { }`) vs macOS/Linux (`&&`)

### E — Examine

Builds a complete inventory of available capabilities.

1. Scans `agent/*.md` — reads frontmatter of every standalone agent (ROUTER, ORCHESTRATOR, etc.)
2. Scans `.agents/skills/*/SKILL.md` — reads frontmatter (`name`, `description`, `triggers`, `allowed-tools`) of every installed skill
3. Scans project structure — manifests (`package.json`, `pyproject.toml`), configs (`opencode.json`, `.gitignore`), top-level directories

### L — Link

Maps the user's request against the capability inventory.

1. **Request classification**: Parses the user's request into discrete components (e.g., "audit code", "generate docs", "commit changes")
2. **Capability matching**: For each component, finds the best matching agent or skill using keyword heuristics (e.g., "audit" → ai-audit, "commit" → ai-git)
3. **Gap analysis**: Identifies request components with no matching capability and flags them as manual steps
4. **Confidence scoring**: High (direct match), Medium (partial match), Low (weak match), Gap (no match)

### L — Layout

Designs the workflow structure and plan document.

1. **Workflow composition**: Chains matched capabilities into an optimal sequence
   - Determines natural prerequisites and ordering
   - Identifies parallelizable steps
   - Applies adaptive branching (if/then paths based on intermediate results)
2. **Workflow pattern selection**: Matches the request to a known catalog pattern (Audit→Fix→Document→Commit, Parallel Audit Gate, Bootstrap→Validate→Doc, etc.)
3. **Fallback planning**: For each step, defines what to do if the primary skill/agent is unavailable
4. **Plan template**: Assembles the full document with Objective, Context Summary, Capability Mapping, Workflow Diagram (Mermaid), Subtask Breakdown, Parallel Blocks, Adaptive Branching, Risks, and Handoff Instructions

### A — Assess

Reviews the plan for quality, completeness, and safety.

1. **Self-Review checklist**:
   - Existence: every referenced agent/skill exists
   - Circularity: no circular dependencies
   - Handoff clarity: instructions are concrete, not vague
   - Fallback realism: alternatives are practical
   - Gap honesty: all gaps explicitly flagged
   - Self-reference: DELLA never recommends itself for execution
   - Format: professional English, no emojis
   - Completeness: all template sections present
2. **Risk assessment**: Probability × Impact scoring per risk
3. **Edge case handling**: No AGENTS.md, no skills, vague requests, plan file collisions

## Cardinal Rule

| If you need to... | Use this |
|---|---|
| Understand what's possible in this project | **DELLA** |
| Plan a multi-step workflow chaining multiple skills | **DELLA** |
| Get an adaptive plan with fallback alternatives | **DELLA** |
| Know which agent or skill to use for a given task | **DELLA** |
| Execute a known plan step by step | **ROUTER** |
| Orchestrate complex dependency chains | **ORCHESTRATOR** |
| Audit code, generate docs, commit code | **Specific skill** |

## Plan Output

Plans are saved to `docs/DELLA_PLAN/plan_YYYY-MM-DD_nnn.md` with auto-incrementing sequence numbers.

### Plan Structure

Every plan contains these sections:

| Section | Content |
|---|---|
| **Header** | Date, AI model, version, source request |
| **Objective** | One or two sentences describing what the plan achieves |
| **Context Summary** | Project name, AGENTS.md status, available agents and skills |
| **Capability Mapping** | Table mapping request components → agent/skill → trigger → confidence |
| **Workflow Diagram** | Mermaid flowchart with branching and parallel paths |
| **Subtask Breakdown** | Numbered steps with agent/skill, dependencies, time estimate, complexity, fallback |
| **Parallel Blocks** | Concurrent execution groups |
| **Adaptive Branching** | Conditional paths based on intermediate outcomes |
| **Risks and Considerations** | Probability × Impact table with mitigations |
| **Handoff Instructions** | Concrete invocation commands, expected outputs, and verification steps per subtask |

---

**[⬆ Back to Top](#)** | **[📂 Agent Index](/docs/agents/README.md)**
