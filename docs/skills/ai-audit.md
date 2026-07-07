# ai-audit

Lightweight interactive code quality auditor with weighted health scoring.

> **Trigger:** `@ai-audit` | `@ai-audit --full` | `@ai-audit --fix` | `@ai-audit --list` | `@ai-audit --diff`

## Quick Start

1. Type `@ai-audit` to start an interactive audit.
2. The agent asks: scope (whole repo or dir) → depth (quick or deep) → categories (all, security, security+perf).
3. The scan runs and returns findings grouped by severity with a health score (A–D).
4. Report saved to `docs/ai-audit/AUDIT_REPORT_{date}.md`.

**Example:** `@ai-audit` → whole repo → deep → all categories → 5 findings found, score 72 (B).

## Description

Reads source files and detects patterns across 5 weighted categories: Security (35%), Performance (20%), Maintainability (20%), Best Practices (15%), Documentation (10%). Tracks regression between audits via `.agents/memory/ai-audit/last-audit.json`. Findings include confidence levels — pattern match (70%), file read confirmed (85%), cross-referenced (95%).

## Architecture

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart TD
    A["@ai-audit triggered"] --> B{Mode?}
    B -->|bare| C[Interactive: scope → depth → categories]
    B -->|--full| D[Deep scan all categories]
    B -->|--fix| E[Auto-fix Critical + High]
    B -->|--diff| F[Compare last 2 reports]
    B -->|--list| G[List past audits]
    C --> H[Pattern scan across 5 weighted categories]
    D --> H
    H --> I[Score: Σ(cat_weight × normalized_score)]
    I --> J{Grade}
    J -->|≥ 90| K[A - Excellent]
    J -->|≥ 70| L[B - Good]
    J -->|≥ 50| M[C - Fair]
    J -->|< 50| N[D - Poor]
    I --> O[Regression Δ vs last-audit.json]
```

**Why weighted scoring?** Security gets 35% weight because a vulnerability is more damaging than poor documentation (10%). The regression delta catches drift before it becomes technical debt.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-audit` | Interactive audit with regression check |
| `@ai-audit --full` | Deep scan, all categories, no questions |
| `@ai-audit --fix` | Auto-fix Critical and High findings from last report |
| `@ai-audit --diff` | Compare last 2 reports: new/fixed changes, score delta |
| `@ai-audit --list` | List past audit reports with date, score, grade |

## Configuration

Output: `/docs/ai-audit/AUDIT_REPORT_{DATE}.md`. Regression memory: `.agents/memory/ai-audit/last-audit.json` (auto-created, gitignored). Adapts checks to detected language (TypeScript, JavaScript, Python, Markdown).

> [!NOTE]
> This is a pattern-based static analysis skill. It reads files directly — no external tools needed. It does not execute code. Low-confidence findings are labeled `[unverified]`.

> [!TIP]
> Run `@ai-config --check` first to validate repo structure, then `@ai-audit` for deeper code quality analysis.

<!-- Last updated: 2026-07-07 via @ai-docs update -->

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
