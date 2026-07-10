# ai-audit

> **Trigger:** `@ai-audit` | **Tools:** Read, Glob, Grep, Bash, Write | **Category:** Code Quality

[📂 Skill Index](/docs/README.md) → **ai-audit**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Interactive | `@ai-audit` | 6-step interview: scope → depth → categories → scan → findings → report |
| Full | `@ai-audit --full` | Deep scan all categories, no questions, with regression check |
| Auto-fix | `@ai-audit --fix` | Auto-corrects High + Critical findings from last report |
| Diff | `@ai-audit --diff` | Compare last 2 reports, show what changed (new/fixed/regressed) |
| List | `@ai-audit --list` | Show past audits with date, score, grade |

> [!TIP]
> Run `@ai-audit` (bare) for the full interactive wizard. Use `--full` for a quick no-questions scan.

## Overview

Lightweight interactive code quality auditor. Scans files for security, performance, maintainability, best practices, and documentation issues with regression tracking and confidence scoring. Each audit saves a baseline to `.agents/memory/ai-audit/` so subsequent runs can detect improvement or regression.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Interactive 6-step wizard: scope, depth, categories, language, scan, findings |
| `--full` | Deep scan all categories, no interaction, with automatic regression check |
| `--fix` | Auto-fix High and Critical findings from the most recent report |
| `--list` | Display history of past audits with date, score, and grade |
| `--diff` | Compare the two most recent audit reports for changes |

## Audit Categories

| Category | Weight | Severity scale |
|:---------|-------:|:---------------|
| Security | 35% | 🔴 Critical 10 / 🟠 High 5 / 🟡 Medium 2 / 🔵 Low 1 |
| Performance | 20% | Same scale |
| Maintainability | 20% | Same scale |
| Best Practices | 15% | Same scale |
| Documentation | 10% | Same scale |

Score = Security×.35 + Perf×.20 + Maint×.20 + BestP×.15 + Docs×.10. Grade: A ≥ 90, B ≥ 70, C ≥ 50, D < 50.

> [!NOTE]
> After each audit, the last score and finding count are saved to `.agents/memory/ai-audit/last-audit.json` for regression comparison. Reports are written to `/docs/ai-audit/AUDIT_REPORT_{DATE}.md`.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
