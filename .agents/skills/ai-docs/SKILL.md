---
name: ai-docs
description: >-
  Generates, updates, and audits Markdown documentation in /docs/. Also
  handles AI interaction logs via the `--log` sub-module.
allowed-tools: Read, Write, Bash, Glob, Grep
triggers:
  - "@ai-docs"
  - "@ai-docs pro"
  - "@ai-docs update"
  - "@ai-docs audit"
  - "@ai-docs --log"
  - "@ai-docs --log --list"
  - "@ai-docs --log --search"
  - "@ai-docs --log --last"
  - "@ai-docs --log --no-prompt"
  - "@ai-docs --log --compact"
---

# ROLE: DocMaster

Create, maintain, and audit Markdown documentation (English) in `/docs/`. Follow the standards below.

## Standards

| Rule | Detail |
|---|---|
| Language | Professional English |
| Location | `/docs/`. Subdirs: `skills/`, `guides/`, `reference/`, `audit/` |
| Skill Index | `/docs/README.md` — table with every skill as clickable link to `skills/<name>.md` |
| Cross-links | Every page ends with `**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**` |
| Headings | H1 per file, H2 major, H3 subsection, H4 sparingly |
| Tables | Header + alignment: `| :--- | :--- |` |
| Code blocks | Always specify language (typescript, json, mermaid, etc.) |
| Admonitions | Use `> [!NOTE]`, `> [!WARNING]`, `> [!TIP]` |
| Wall-text | Break every ~4 lines into lists, tables, or code blocks |

## Quick Start

| Mode | Trigger | What happens |
|---|---|---|---|
| Generate | `@ai-docs` | Rebuilds `/docs/README.md` + all `/docs/skills/<name>.md` from `.agents/skills/` |
| Deep-dive | `@ai-docs pro <dir>` | Architectural doc with ADR, complexity, edge cases for a module |
| Update | `@ai-docs update <name>` | Incremental update of one skill page. Preserves `<!-- MANUAL -->` blocks |
| Audit | `@ai-docs audit` | Compliance check → `/docs/audit/DOCS_AUDIT_REPORT.md` with weighted score |
| Log | `@ai-docs --log` | Log AI interaction (reads `log.md` sub-module from this directory) |

## Sub-modules

This skill loads sub-module files from its own directory by flag:

| Flag | File loaded |
|---|---|
| `--log` | `log.md` |

When a flag is used, read the corresponding `.md` file and execute its
instructions directly. Each file is self-contained with no frontmatter.

## Modes

### STANDARD (`@ai-docs`)
1. Glob `.agents/skills/*/SKILL.md`
2. Extract `name`, `description`, `triggers`, `allowed-tools` from frontmatter
3. Generate `/docs/README.md` (skill index) using the Index Template below
4. Generate `/docs/skills/<name>.md` per skill using the Skill Page Template below

### PROFESSIONAL (`@ai-docs pro <dir>`)
1. Read files in the specified directory
2. Generate a deep-dive doc adding these sections after Technical Spec:
   - **ADR**: Why this approach over alternatives
   - **Complexity Analysis**: Time & Space (Big-O)
    - **Dependency Graph**: Imports and external services
      - Must include `%%{init}%%` sizing directive per `docs/diagrams/README.md` so diagrams render at readable scale.
    - **Stress / Edge Cases**: Concurrency, failure modes, edge behavior

### UPDATE (`@ai-docs update <name>`)
Incremental — NEVER full regenerate:
1. Compare `.agents/skills/<name>/SKILL.md` vs `/docs/skills/<name>.md`
2. Preserve `<!-- MANUAL -->` and `<!-- CUSTOM -->` sections
3. Sync only outdated/missing parts
4. If skills added/removed, rebuild `/docs/README.md`
5. Append `<!-- Last updated: [DATE] via @ai-docs update -->`
6. Report: "Updated X pages, skipped Y (manual edits), added Z skills"

### AUDIT (`@ai-docs audit`)
Evaluates docs against Standards. Output → `/docs/audit/DOCS_AUDIT_REPORT.md`.

| Severity | Weight | Checks |
|---|---|---|
| 🔴 Critical | 40% | Missing doc page, broken links, non-English, index missing skills |
| 🟡 Warning | 30% | Wrong heading order, missing table alignment, no code lang, paragraphs >5 lines, names not clickable |
| 🔵 Suggestion | 30% | Missing admonitions, missing cross-links |

Score = Critical% + Warning% + Suggestion%. PASS if ≥ 80%.
`--fix` auto-corrects Warnings + Suggestions. Critical issues reported for manual fix.

## Index Template (`/docs/README.md`)

```markdown
# Skill Index — myAI-Skills

> **10 OpenCode skills** for AI-assisted development. Each skill is a self-contained agent invoked via `@trigger` commands.

[📂 Welcome](/docs/WELCOME.md) • [📂 Agent Index](/docs/agents/README.md) • [📂 Guides](/docs/guides/usage.md)

---

## Skills by Category

### 🔧 Orchestration & Routing

| Skill | Trigger | Description |
|:------|:--------|:------------|
| _ai-router_ entries | ... | ... |
| _ai-orchestrator_ entries | ... | ... |

### 📋 Documentation & Configuration

| Skill | Trigger | Description |
|:------|:--------|:------------|
| _ai-docs, ai-config, ai-init_ entries | ... | ... |

### ⚡ Workflow & Productivity

| Skill | Trigger | Description |
|:------|:--------|:------------|
| _ai-git, auto-report_ entries | ... | ... |

### 🛡️ Audit & Security

| Skill | Trigger | Description |
|:------|:--------|:------------|
| _ai-audit, ai-env_ entries | ... | ... |

### 📦 Package Management

| Skill | Trigger | Description |
|:------|:--------|:------------|
| _skill-search_ entries | ... | ... |

## All Skills (Alphabetical)

| Trigger | Description |
|:--------|:------------|
| `@<trigger>` | <description> |
| ... | ... |

## Quick Navigation

| To do this... | Use this |
|:--------------|:---------|
| Browse all available skills | `@skill-search --list` |
| Generate or update docs | `@ai-docs` |
| Audit code quality | `@ai-audit` |
| Validate repo config | `@ai-config --check` |
| Scan for env vars | `@ai-env --scan` |
| Git commit / PR / release | `@ai-git --commit` |
| Create a report | `@auto-report` |
| Bootstrap new project docs | `@ai-init` |
| Route a complex task | `@ai-router` |
| Orchestrate cross-skill work | `@ai-orchestrator` |

---

> **Generated by `@ai-docs`** • Last updated: <current-date>
```

When generating:
- Group skills into categories using keyword matching on the description (same keywords as category_guess for skill pages).
- The "All Skills" table covers every skill in alphabetical order.
- The category tables list skills with a link to their skill page in `docs/skills/<name>.md`.
- Preserve any `<!-- MANUAL -->` or `<!-- CUSTOM -->` blocks if the file already exists.

## Skill Page Template (`/docs/skills/<name>.md`)

```markdown
# <name>

> **Trigger:** `@<primary_trigger>` | **Tools:** `<allowed-tools>` | **Category:** <category_guess>

[📂 Skill Index](/docs/README.md) → **<name>**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Interactive | `<primary_trigger>` | <interactive description> |
| Flag-based | `<secondary_triggers>` | <flag descriptions> |

> [!TIP]
> Use `<primary_trigger> --help` or just `<primary_trigger>` (bare) to get started.

## Overview

<description>

<2-3 sentences: how it works, when to use it, key concepts>

## Commands

| Flag | Description |
|:-----|:------------|
| `<primary_trigger>` | <default behavior> |
| `<trigger --flag>` | <flag behavior> |
| ... | ... |

## Configuration

<parameters, outputs, notable behavior>

> [!NOTE]
> <edge cases, prerequisites, or important notes>

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
```

When generating:
- `category_guess`: Infer from the skill's description. Keywords like "audit", "security", "quality" → **Code Quality**; "doc", "document" → **Documentation**; "config", "env" → **Configuration**; "git", "commit" → **Version Control**; "report", "generate" → **Reporting**; "router", "orchestrat", "pipeline", "dag" → **Orchestration**; "skill", "package", "search" → **Package Management**; "init", "bootstrap" → **Project Setup**.
- `primary_trigger`: The first trigger in the list
- `secondary_triggers`: Join the remaining triggers with ``, ``
- `interactive description`: If `(bare)` is a trigger pattern, describe the interactive flow
- `flag descriptions`: For each trigger with a flag (`--flag`), describe what it does. For bare triggers, describe it as "Interactive mode" or "Default behavior".

Professional mode adds: ADR, Complexity Analysis, Dependency Graph, Stress/Edge Cases after Description.
