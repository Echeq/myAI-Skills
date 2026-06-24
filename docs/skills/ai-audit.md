# ai-audit

Lightweight interactive code quality auditor with weighted health scoring.

> **Trigger:** `@ai-audit` | `@ai-audit --security` | `@ai-audit --performance` | `@ai-audit --full` | `@ai-audit --fix` | `@ai-audit --list`

## Quick Start

1. Type `@ai-audit` to start an interactive audit.
2. The agent asks: scope (whole repo or dir) → depth (quick or deep) → categories (all, security, security+perf).
3. The scan runs and returns findings grouped by severity with a health score (A–D).
4. Report saved to `docs/ai-audit/AUDIT_REPORT_{date}.md`.

**Example:** `@ai-audit` → whole repo → deep → all categories → 5 findings found, score 72 (B).

## Description

Reads source files and detects patterns across 5 weighted categories: Security (35%), Performance (20%), Maintainability (20%), Best Practices (15%), Documentation (10%). Assigns severities (Critical/High/Medium/Low) and computes a health score (A–D).

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-audit` | Full interactive audit |
| `@ai-audit --security` | Security-only scan |
| `@ai-audit --performance` | Performance-only scan |
| `@ai-audit --full` | Deep scan, all categories |
| `@ai-audit --fix` | Auto-fix Critical and High findings |
| `@ai-audit --list` | List past audit reports |

## Configuration

Output: `/docs/ai-audit/AUDIT_REPORT_{DATE}.md`. Adapts checks to detected language (TypeScript, JavaScript, Python, Markdown).

> [!NOTE]
> This is a pattern-based static analysis skill. It reads files directly — no external tools needed. It does not execute code.

> [!TIP]
> Run `@ai-orchestrator --suggestion` first to identify which areas need auditing most.

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
