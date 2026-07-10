# auto-report

Interactive report generator. Asks one question at a time, fills a Markdown template, checks export dependencies, and saves the result to `/docs/auto-report/`.

> **Trigger:** `@auto-report` | `@auto-report --templates` | `@auto-report --history` | `@auto-report --config`

## Quick Start

1. Type `@auto-report` to start the wizard.
2. Answer: format → language → subject → title → authors → sections → content.
3. Skill checks dependencies, generates the report, and saves to `/docs/auto-report/`.

**Example:** `@auto-report` → .docx → English → "AI Ethics" → 3 authors → sections confirmed → pandoc found → saved as `edited_default_2026-06-30.docx`.

## Description

Interactive report builder that asks one question at a time, reducing cognitive load and allowing mid-session cancellation. Adapts sections to the subject dynamically (CS → Implementation, Algorithm Analysis; Science → Experimental Setup, Results; Humanities → Theoretical Framework, Sources). Supports 5 export formats. Templates stored in `.agents/skills/auto-report/templates/`. No external dependencies required for Markdown output.

## Usage

| Command | Action |
| :--- | :--- |
| `@auto-report` | Full wizard: format → language → subject → title → authors → sections → content → export |
| `@auto-report --templates` | List available template folders |
| `@auto-report --history` | Show past reports table |
| `@auto-report --config` | View/edit saved settings |

## Configuration

### Supported Formats

| Format | Ext | Dependency | Fallback |
| :--- | :--- | :--- | :--- |
| Markdown | `.md` | None | — |
| Word | `.docx` | pandoc | .md |
| PDF | `.pdf` | pandoc + pdf-engine | .md |
| HTML | `.html` | pandoc | .md |
| LaTeX | `.tex` | pandoc | .md |

### Templates

Located in `.agents/skills/auto-report/templates/<name>/template.md`. Built-in:

| Template | Use |
| :--- | :--- |
| `default` | Standard academic reports |
| `chinese-university` | Chinese university reports (GB/T 7714-2015) |

If the subject matches a template folder, it is used. Otherwise, the default template is adapted to the subject dynamically.

### Output

All reports saved to `/docs/auto-report/edited_{template}_{date}.{ext}`. Past session data persisted to `/docs/auto-report/.config.md`.

> [!NOTE]
> The skill always generates Markdown with zero dependencies. Other formats require pandoc (and a PDF engine for `.pdf`). If the chosen format's dependency is missing, the skill falls back to `.md` and prints install instructions.

> [!TIP]
> No external deps needed for Markdown output. Only install pandoc if you need .docx/.pdf/.html/.tex. If your report includes Mermaid diagrams, include the `%%{init}%%` sizing directive per `docs/diagrams/README.md` to prevent oversized rendering.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-10 via @ai-docs update -->
