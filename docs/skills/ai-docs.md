# ai-docs

> **Trigger:** `@ai-docs` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Documentation

[📂 Skill Index](/docs/README.md) → **ai-docs**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Generate | `@ai-docs` | Rebuilds skill index + all per-skill pages from `.agents/skills/` |
| Deep-dive | `@ai-docs pro <dir>` | Architectural doc with ADR, complexity analysis, and edge cases |
| Update | `@ai-docs update <name>` | Incremental update of one skill page (preserves manual edits) |
| Audit | `@ai-docs audit` | Compliance check with weighted score, saved to `/docs/audit/` |
| Log | `@ai-docs --log` | Log AI interaction to `docs/log/AI-LOG-*.md` |

> [!TIP]
> Use `@ai-docs update <name>` to update a single page without overwriting manual sections marked with `<!-- MANUAL -->`.

## Overview

Documentation lifecycle agent with 5 modes: full generation, professional deep-dive, incremental update, compliance audit, and AI interaction logging. Operates entirely in `/docs/`. Reads skill definitions from `.agents/skills/<name>/SKILL.md`.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Full regenerate: rebuild `/docs/README.md` + all `/docs/skills/<name>.md` |
| `pro <dir>` | Generate a deep-dive architecture doc with ADR, complexity, deps, and edge cases |
| `update <name>` | Incremental update of one skill page. Preserves `<!-- MANUAL -->` and `<!-- CUSTOM -->` blocks |
| `audit` | Compliance audit → `/docs/audit/DOCS_AUDIT_REPORT.md` with weighted score |
| `--log` | Log AI interaction to `docs/log/AI-LOG-{date}-{time}-{pc}.md` |
| `--log --list` | List all AI interaction log files |
| `--log --search <q>` | Search logs for a keyword or phrase |
| `--log --last` | Show the most recent log entry |
| `--log --no-prompt` | Log without asking for context |
| `--log --compact` | Log in compact format (single line) |

## Audit Scoring

| Severity | Weight | Checks |
|:---------|-------:|:-------|
| 🔴 Critical | 40% | Missing doc page, broken links, non-English, index missing skills |
| 🟡 Warning | 30% | Wrong heading order, missing table alignment, no code lang, paragraphs > 5 lines |
| 🔵 Suggestion | 30% | Missing admonitions, missing cross-links |

PASS if score ≥ 80%. `--fix` auto-corrects Warnings and Suggestions.

> [!NOTE]
> `@ai-docs update` is the safe incremental mode — it never overwrites content between `<!-- MANUAL -->` or `<!-- CUSTOM -->` comment blocks. Use full `@ai-docs` only when you want a complete regenerate.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
