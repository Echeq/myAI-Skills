# ai-audit

Lightweight interactive code quality auditor. Scans files for security, performance, maintainability, best practices, and documentation issues with regression tracking and confidence scoring.

> **Trigger:** `@ai-audit` | `@ai-audit --full` | `@ai-audit --fix` | `@ai-audit --list` | `@ai-audit --diff`

## Quick Start

1. Type `@ai-audit` to start an interactive audit.
2. The agent asks: scope (whole repo or dir) → depth (quick or deep) → categories (all, security, security+perf).
3. The scan runs and returns findings grouped by severity with a health score (A–D).
4. Report saved to `docs/ai-audit/AUDIT_REPORT_{date}.md`.

**Example:** `@ai-audit` → whole repo → deep → all categories → 5 findings found, score 72 (B).

## Description

Reads source files and detects patterns across 5 weighted categories: Security (35%), Performance (20%), Maintainability (20%), Best Practices (15%), Documentation (10%). Tracks regression between audits via `.agents/memory/ai-audit/last-audit.json`. Findings include confidence levels — pattern match (70%), file read confirmed (85%), cross-referenced (95%). Low-confidence findings are labeled `[unverified]`.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-audit` | Interactive: scope → depth → categories → scan → findings → report |
| `@ai-audit --full` | Deep scan all categories, no questions, with regression check |
| `@ai-audit --fix` | Auto-fix Critical and High findings from the last report |
| `@ai-audit --diff` | Compare last 2 reports: new/fixed changes, score delta |
| `@ai-audit --list` | Show past audits with date, score, grade |

## Configuration

| Item | Details |
| :--- | :--- |
| Report output | `/docs/ai-audit/AUDIT_REPORT_{DATE}.md` |
| Regression memory | `.agents/memory/ai-audit/last-audit.json` (auto-created, gitignored) |
| Language adaptation | TypeScript, JavaScript, Python, Markdown — checks adapt per language |
| Quick mode | Uses grep patterns for fast scanning |
| Deep mode | Reads every file for thorough analysis |

### Scoring

Score = Security × 0.35 + Performance × 0.20 + Maintainability × 0.20 + Best Practices × 0.15 + Documentation × 0.10.

| Grade | Range |
| :--- | :--- |
| A | ≥ 90 |
| B | ≥ 70 |
| C | ≥ 50 |
| D | < 50 |

> [!NOTE]
> This is a pattern-based static analysis skill. It reads files directly — no external tools needed. It does not execute code.

> [!TIP]
> Run `@ai-config --check` first to validate repo structure, then `@ai-audit` for deeper code quality analysis.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-10 via @ai-docs update -->
