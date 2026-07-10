# ai-init

> **Trigger:** `@ai-init` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Project Setup

[📂 Skill Index](/docs/README.md) → **ai-init**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Full wizard | `@ai-init` | Auto-detect stack → questions → generate 4 docs → update AGENTS.md |
| Validate | `@ai-init validate` | Compare documented info against actual code; report drift |
| Types flag | `@ai-init --types` | Skip folder-structure question; assume controllers/models/services layout |
| Features flag | `@ai-init --features` | Skip folder-structure question; assume users/payments/ feature layout |
| Screaming flag | `@ai-init --screaming` | Skip folder-structure question; assume screaming architecture layout |

> [!TIP]
> Use `@ai-init` when starting a new project or joining an existing one with no documentation. It generates 4 essential docs in under 5 minutes.

## Overview

Bootstraps foundational project documentation in under 5 minutes. Auto-detects stack and tooling, asks minimal questions, generates 4 structured docs in `/docs/ai-init/` (ARCHITECTURE.md, CONVENTIONS.md, DECISIONS.md, ERRORS.md), and updates AGENTS.md. Includes a `validate` sub-command for drift detection against the actual codebase.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Full wizard: auto-detect → questions → generate 4 docs → update AGENTS.md |
| `validate` | Compare documented architecture/conventions against actual code; report drift |
| `--types` | Skip folder-structure question; assume controllers/models/services |
| `--features` | Skip folder-structure question; assume users/payments/ feature-based layout |
| `--screaming` | Skip folder-structure question; assume screaming architecture layout |

> [!NOTE]
> Generated docs go to `/docs/ai-init/`. The `validate` sub-command detects drift by comparing documented assumptions (stack, structure, patterns) against the actual codebase.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
