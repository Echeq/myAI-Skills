# ai-audit

Lightweight interactive code quality auditor with weighted health scoring.

> **Trigger:** `@ai-audit` | `@ai-audit --security` | `@ai-audit --performance` | `@ai-audit --full` | `@ai-audit --fix` | `@ai-audit --list`

## Quick Start

Type `@ai-audit` to start an interactive audit. The skill asks for scope, depth, and categories, then scans your codebase and generates a scored report.

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

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
