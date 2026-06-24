# ai-docs

Generates, updates, and audits Markdown documentation in `/docs/`.

> **Trigger:** `@ai-docs` | `@ai-docs pro` | `@ai-docs update` | `@ai-docs audit`

## Quick Start

| Mode | Trigger | What happens |
| :--- | :--- | :--- |
| Generate | `@ai-docs` | Rebuilds skill index + all per-skill pages from `.agents/skills/` |
| Deep-dive | `@ai-docs pro src/` | Architectural doc with ADR, complexity, edge cases |
| Update | `@ai-docs update ai-commit` | Incremental update of one skill page (preserves manual edits) |
| Audit | `@ai-docs audit` | Compliance check with weighted score, saved to `/docs/audit/` |

**Example:** `@ai-docs` → all docs regenerated in ~10s. `@ai-docs audit` → score report generated.

## Description

Documentation lifecycle agent with 4 modes: full generation, professional deep-dive, incremental update, and compliance audit. Operates entirely in `/docs/`. Reads skill definitions from `.agents/skills/<name>/SKILL.md`.

## Usage

| Mode | Trigger | Output |
| :--- | :--- | :--- |
| Standard | `@ai-docs` | `/docs/README.md` + `/docs/skills/<name>.md` |
| Professional | `@ai-docs pro <dir>` | Single deep-dive `.md` with ADR, complexity, deps, edge cases |
| Update | `@ai-docs update <name>` | Updated `/docs/skills/<name>.md` |
| Audit | `@ai-docs audit` | `/docs/audit/DOCS_AUDIT_REPORT.md` (score 0-100%) |

## Configuration

| Path | Purpose |
| :--- | :--- |
| `.agents/skills/<name>/SKILL.md` | Source of truth — frontmatter drives doc generation |
| `/docs/README.md` | Skill index (auto-generated) |
| `/docs/skills/<name>.md` | Per-skill doc pages (auto-generated) |
| `/docs/audit/` | Audit reports |

Use `<!-- MANUAL -->` comments in doc pages to preserve custom edits on update.

> [!NOTE]
> Standard mode regenerates ALL skill pages. Manual edits are overwritten unless protected with `<!-- MANUAL -->`.
> Audit compliance scoring: Critical 40%, Warnings 30%, Suggestions 30%. PASS if ≥ 80%.

> [!TIP]
> Use `@ai-orchestrator --plan` before writing docs to get a structured outline first.

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
