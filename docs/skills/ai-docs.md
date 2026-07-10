# ai-docs

Generates, updates, and audits Markdown documentation in `/docs/`. Also handles AI interaction logs via the `--log` sub-module.

> **Trigger:** `@ai-docs` | `@ai-docs pro` | `@ai-docs update` | `@ai-docs audit` | `@ai-docs --log`

## Quick Start

| Mode | Trigger | What happens |
| :--- | :--- | :--- |
| Generate | `@ai-docs` | Rebuilds skill index + all per-skill pages from `.agents/skills/` |
| Deep-dive | `@ai-docs pro <dir>` | Architectural doc with ADR, complexity, edge cases |
| Update | `@ai-docs update <name>` | Incremental update of one skill page (preserves manual edits) |
| Audit | `@ai-docs audit` | Compliance check with weighted score, saved to `/docs/audit/` |
| Log | `@ai-docs --log` | Log AI interaction to `docs/log/AI-LOG-*.md` |

**Example:** `@ai-docs` → all docs regenerated in ~10s. `@ai-docs audit` → score report generated.

## Description

Documentation lifecycle agent with 5 modes: full generation, professional deep-dive, incremental update, compliance audit, and AI interaction logging. Operates entirely in `/docs/`. Reads skill definitions from `.agents/skills/<name>/SKILL.md`. Follows documentation standards: professional English, consistent heading hierarchy, table alignment, code language labels, Mermaid diagram sizing directives, and cross-links on every page.

## Usage

| Mode | Trigger | Output |
| :--- | :--- | :--- |
| Standard | `@ai-docs` | `/docs/README.md` + `/docs/skills/<name>.md` |
| Professional | `@ai-docs pro <dir>` | Single deep-dive `.md` with ADR, complexity, deps, edge cases |
| Update | `@ai-docs update <name>` | Updated `/docs/skills/<name>.md` (preserves `<!-- MANUAL -->` blocks) |
| Audit | `@ai-docs audit` | `/docs/audit/DOCS_AUDIT_REPORT.md` (score 0–100%) |
| Log | `@ai-docs --log` | `docs/log/AI-LOG-{date}-{time}-{pc}.md` |

## Configuration

| Path | Purpose |
| :--- | :--- |
| `.agents/skills/<name>/SKILL.md` | Source of truth — frontmatter drives doc generation |
| `/docs/README.md` | Skill index (auto-generated) |
| `/docs/skills/<name>.md` | Per-skill doc pages (auto-generated) |
| `/docs/audit/` | Audit reports |
| `/docs/log/` | AI interaction logs |

### Audit Scoring

| Severity | Weight | Checks |
| :--- | :--- | :--- |
| 🔴 Critical | 40% | Missing doc page, broken links, non-English, index missing skills |
| 🟡 Warning | 30% | Wrong heading order, missing table alignment, no code lang, paragraphs > 5 lines, names not clickable |
| 🔵 Suggestion | 30% | Missing admonitions, missing cross-links |

Score = Critical% + Warning% + Suggestion%. PASS if ≥ 80%.

> [!NOTE]
> Standard mode regenerates ALL skill pages. Manual edits are overwritten unless protected with `<!-- MANUAL -->` comment blocks.

> [!TIP]
> Use `@ai-docs pro <dir>` for deep-dive architecture docs with ADRs and dependency graphs. Use `@ai-docs update <name>` for targeted updates without regeneration.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-10 via @ai-docs update -->
