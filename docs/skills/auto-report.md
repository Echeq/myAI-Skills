# auto-report

> **Trigger:** `@auto-report` | **Tools:** Read, Write, Bash, Glob | **Category:** Reporting

[📂 Skill Index](/docs/README.md) → **auto-report**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Wizard | `@auto-report` | Interactive 8-step: format → language → subject → title → authors → sections → content → figures |
| Templates | `@auto-report --templates` | List available template folders |
| History | `@auto-report --history` | Show past reports table with dates and subjects |
| Config | `@auto-report --config` | View saved settings and preferences |

> [!TIP]
> Use `@auto-report --templates` first to see available templates before starting the wizard.

## Overview

Interactive report generator. Asks one question at a time, fills a template, checks export dependencies, and saves the result to `/docs/auto-report/`. Supports 5 output formats: Markdown, DOCX, PDF, HTML, and LaTeX (via pandoc).

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Start the 8-step wizard: format → language → subject → title → authors → sections → content → figures/tables |
| `--templates` | List available template folders in `.agents/skills/auto-report/templates/` |
| `--history` | Show a table of past reports with dates and subjects |
| `--config` | View saved user settings and preferences |

## Generation Flow

1. **Format** — md / docx / pdf / html / tex
2. **Language** — English / Chinese / Bilingual
3. **Subject** — e.g., "Operating Systems", "Machine Learning"
4. **Title** — report title
5. **Authors** — individual or group
6. **Sections** — AI suggests sections based on subject; user confirms/edits
7. **Content** — user provides content for each section (no AI generation)
8. **Figures/Tables** — name and section; auto-numbered placeholders

> [!NOTE]
> If the chosen export format's dependency (pandoc) is missing, the skill falls back to Markdown output and prints the install command. Mermaid diagrams in reports must include the `%%{init}%%` sizing directive.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
