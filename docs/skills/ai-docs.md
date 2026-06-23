# ai-docs

Generates, updates, and audits Markdown documentation in `/docs/`.

> **Trigger:** `@ai-docs` | `@ai-docs pro` | `@ai-docs professional` | `@ai-docs update` | `@ai-docs audit`

## Description

Documentation lifecycle agent with 4 modes: standard (full regeneration), professional (deep-dive with ADR), update (incremental), and audit (compliance check).

## Usage

| Mode | Trigger |
| :--- | :--- |
| Standard | `@ai-docs` |
| Professional | `@ai-docs pro <target>` |
| Update | `@ai-docs update <skill-name>` |
| Audit | `@ai-docs audit` |

## Configuration

All docs live in `/docs/`. Generated output: skill index at `/docs/README.md` and per-skill pages at `/docs/skills/<name>.md`.

> [!WARNING]
> This skill regenerates `/docs/skills/` pages. Manual edits to those files may be overwritten. Use `<!-- MANUAL -->` comments to preserve custom content.

> [!TIP]
> See [central-skills-hub-builder](central-skills-hub-builder.md) for the architecture rules that skills should follow.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
