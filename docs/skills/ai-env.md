# ai-env

> **Trigger:** `@ai-env` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Configuration

[📂 Skill Index](/docs/README.md) → **ai-env**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Interactive | `@ai-env` | Scan code for env vars, then offer actions |
| Scan | `@ai-env --scan` | Scan project code for environment variable references |
| Init | `@ai-env --init` | Generate `.env.example` + update `.gitignore` + create `docs/ENVIRONMENT.md` |
| Validate | `@ai-env --validate` | Compare `.env` against `.env.example` for missing or extra vars |
| Audit | `@ai-env --audit` | Scan for hardcoded secrets, tokens, and credentials in code |

> [!TIP]
> Run `@ai-env --init` early in a project to establish the canonical env var list and prevent secret leakage.

## Overview

Environment configuration manager. Scans code for environment variable references, generates `.env.example`, updates `.gitignore`, validates `.env` files against the example, and audits for hardcoded secrets. Never reads or exposes actual `.env` file values.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Interactive: scan code for env vars, then choose next action |
| `--scan` | Scan project code for all `process.env.X`, `os.getenv()`, and `.env` references |
| `--init` | One-step setup: generate `.env.example` + update `.gitignore` + create `docs/ENVIRONMENT.md` |
| `--validate` | Check that `.env` matches `.env.example` (no missing or extra vars) |
| `--audit` | Scan for hardcoded secrets, tokens, API keys, and credentials |

> [!WARNING]
> This skill NEVER reads actual `.env` file values. It only checks that variable names exist. Secret values are never exposed, logged, or stored.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
