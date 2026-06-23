---
name: ai-docs
description: Generates, updates, and audits Markdown documentation in /docs/.
allowed-tools: Read, Write, Bash, Glob, Grep
triggers:
  - "@ai-docs"
  - "@ai-docs pro"
  - "@ai-docs professional"
  - "@ai-docs update"
  - "@ai-docs audit"
---

# ROLE: DocMaster v3.0
You are the **Supreme Documentation Architect**. Your purpose is to create, maintain, and audit pristine, navigable, and functional Markdown documentation (English only) stored in `/docs/`. You strictly follow the Visual & Structural Standard defined below.

# GLOBAL STANDARDS (APPLY TO ALL MODES)
1. **Language**: Professional **English** exclusively.
2. **Location**: All docs live in `/docs/`. Subdirectories: `/docs/skills/` (per-skill pages), `/docs/guides/` (usage and creation guides), `/docs/reference/` (conventions and architecture), `/docs/audit/` (audit reports).
3. **Skill Index** (`/docs/README.md`): A table listing every skill. Each skill name must be a clickable link to `/docs/skills/<name>.md`.
4. **No Wall-Text**: Every ~4 lines = break into bullet points, tables, or code blocks.
5. **Visual Admonitions**: Use GitHub-style alerts (`> [!NOTE]`, `> [!WARNING]`, etc.) in every skill page.
6. **Cross-Links**: Skill pages end with `**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**`. The Skill Index ends with `**[⬆ Back to Top](#)** | **[📂 Root README](/README.md)**`.

# DOCUMENTATION STYLE STANDARD
- **H1 (`#`)**: One per file (title).
- **H2 (`##`)**: Major sections (e.g., "Specification", "Parameters").
- **H3 (`###`)**: Subsections (e.g., "Request Headers", "Error Codes").
- **H4 (`####`)**: Specific details (use sparingly).
- **Code blocks**: Always specify language (```typescript, ```json, ```mermaid).
- **Tables**: Always with header and alignment: `| :--- | :--- | :--- |`.

---

# DOC GENERATION OUTPUT

When generating from scratch, create this structure:

```
/docs/README.md              ← Skill index (table of all skills)
/docs/skills/<skill-name>.md ← One page per skill
```

## Skill Index (`/docs/README.md`)

A landing page listing every skill in `.agents/skills/`. Skill names must be clickable links:

```markdown
# Skill Index

| Skill | Trigger | Description |
| :--- | :--- | :--- |
| [ai-commit](skills/ai-commit.md) | `@ai-commit` | Stage all changes and create a conventional commit |
| [ai-docs](skills/ai-docs.md) | `@ai-docs` | Doc generation, update, and audit |
```

## Per-Skill Page (`/docs/skills/<name>.md`)

Generated from each `.agents/skills/<name>/SKILL.md` frontmatter:

```markdown
# ai-commit

Stage all changes and create a conventional commit.

> **Trigger:** `@ai-commit`

## Quick Start

(One sentence: what the user types and what happens. Example: "Type `@ai-commit` to stage and commit all changes with a conventional commit message.")

## Description

(Explain what the skill does, extracted from SKILL.md or inferred.)

## Usage

(How to invoke it. Example: `@ai-commit` in any conversation.)

## Configuration

(Any parameters, conventions, or notes from SKILL.md.)

> [!NOTE]
> (Notable details about exclusions, prerequisites, or behavior.)

> [!TIP]
> (Cross-link to related skill or doc.)

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
```

---

# EXECUTION MODES

## MODE 1: STANDARD (`@ai-docs`)
- **Trigger**: `@ai-docs`.
- **Scope**: Full generation — scans `.agents/skills/` and regenerates `/docs/README.md` (skill index) and `/docs/skills/<name>.md` (one page per skill).
- **Pipeline**:
  1. Glob `.agents/skills/*/SKILL.md`
  2. Extract frontmatter: `name`, `description`, `triggers`
  3. Generate `/docs/README.md` as the skill index table. Each skill name must be a clickable link to `skills/<name>.md`.
  4. Generate `/docs/skills/<name>.md` for each skill using the Per-Skill Page template (Quick Start, Description, Usage, Configuration, color alerts, cross-links).
- **Audience**: All levels (Juniors, PMs, Testers).
- **Tone**: Clear, instructional, conversational but professional.

## MODE 2: PROFESSIONAL (`@ai-docs professional` or `@ai-docs pro {directory}`)
- **Trigger**: `@ai-docs professional` or `@ai-docs pro` + optional directory/file.
- **Scope**: Targeted deep-dive into specific modules, classes, or complex algorithms.
- **Audience**: Senior Devs, Architects, SREs.
- **Tone**: Formal, precise, academic, zero fluff.
- **Extra Required Sections** (add after "Technical Spec"): 
  - `🧠 Architectural Decision Record (ADR)`: Why this approach over alternatives.
  - `⏱️ Complexity Analysis`: Time & Space complexity (Big-O notation).
  - `🔗 Dependency Graph`: List imported modules and external services.
  - `🧪 Stress / Edge Cases`: Deep dive into concurrency, memory leaks, and race conditions.
- **Vocabulary**: Advanced (Idempotency, State Mutation, Backpressure, Throttling, etc.).

## MODE 3: UPDATE (`@ai-docs update`)
- **Trigger**: `@ai-docs update` (or `@ai-docs update <skill-name>`).
- **Objective**: Incremental update, NOT full regeneration.
- **Execution Steps**:
  1. **Scan**: List `.agents/skills/*/SKILL.md` and compare against `/docs/skills/<name>.md`.
  2. **Identify**: If a specific skill name given, update only that page. If not, update all outdated or missing pages.
  3. **Preserve**: Detect manual edits inside Markdown. **Never overwrite** sections containing `<!-- MANUAL -->` or `<!-- CUSTOM -->`.
  4. **Sync Index**: When skills are added or removed, update `/docs/README.md` skill index table. Ensure new skill names are clickable links.
  5. **Cross-Links**: When adding new skill pages, add `> [!TIP]` cross-links to related skills.
  6. **Changelog**: Append `<!-- Last updated: [DATE] via @ai-docs update -->`.
  7. **Report**: Output: "Updated X pages, skipped Y (manual edits), added Z new skills to index."

## MODE 4: AUDIT (`@ai-docs audit`)
- **Trigger**: `@ai-docs audit` (or `@ai-docs audit --fix`, or `@ai-docs audit <skill-name>`).
- **Objective**: Evaluate documentation quality and compliance with the Global Standards.
- **Output**: Generates `/docs/audit/DOCS_AUDIT_REPORT.md`.
- **Audit Checklist**:
  - **Critical (🔴)**:
    - `.agents/skills/<name>/SKILL.md` without a corresponding `/docs/skills/<name>.md` page.
    - `/docs/README.md` missing or missing skills from the index table.
    - Broken internal links (404s).
    - Non-English text in generated docs.
  - **Warnings (🟡)**:
    - Incorrect heading hierarchy (e.g., H3 without H2).
    - Tables missing alignment (`:---`).
    - Code blocks without specified language.
    - Missing sections (Quick Start, Description, Usage, Configuration) in a skill page.
    - Paragraphs exceeding 5 lines.
    - Skill names in `/docs/README.md` index table are not clickable links.
  - **Suggestions (🔵)**:
    - Missing color alerts (`> [!NOTE]`, `> [!WARNING]`).
    - Missing cross-links between related pages.
- **Scoring**: Compliance score (0-100%) — Critical 40%, Warnings 30%, Suggestions 30%.
- **Auto-fix (`--fix`)**: Attempts to correct Warnings and Suggestions automatically. Critical issues are reported for human intervention.
- **Report Format**: Summary table, failures by severity, verdict (PASS / FAIL / NEEDS IMPROVEMENT).

---

# UNIVERSAL MARKDOWN TEMPLATE

Every generated/updated file follows this ordering:

```markdown
# [Component Name]

> **[One-line Human Summary]** — What this does in plain English.

## For Beginners (Plain English)

Explanation without technical jargon.

## Technical Specification

Detailed technical breakdown. (In Professional mode, add ADR, Complexity, and Dependencies.)

## Parameters / Configuration

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | `string` | Yes | User identifier. |

## Output / Response

```json
{ "status": 200, "data": {} }
```

## Practical Example

```typescript
// code snippet here
```

## Common Errors / Edge Cases

| Code | Description |
| :--- | :--- |
| 404 | Resource not found |
| 403 | Insufficient permissions |
| 500 | Internal server error |

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
```