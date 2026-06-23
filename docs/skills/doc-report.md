# doc-report

Interactive report generator. Collects user input, inserts content into a Markdown template, and outputs to `/docs/doc-report/`.

> **Trigger:** `@doc-report` | `@doc-report --templates` | `@doc-report --history` | `@doc-report --config`

## Description

Guides the user through an interactive Q&A session, collects all report details (language, subject, title, authors, sections, figures/tables), and generates a structured Markdown report with auto-numbered figure and table placeholders.

## Usage

| Command | Action |
| :--- | :--- |
| `@doc-report` | Full interactive report generation |
| `@doc-report --templates` | List available templates |
| `@doc-report --history` | Show past reports |
| `@doc-report --config` | View/edit settings |

## Configuration

Output: `/docs/doc-report/REPORT_{subject}_{date}.md`. Templates: `.agents/skills/doc-report/templates/<name>/template.md`. Session data saved to `/docs/doc-report/.config.md`.

> [!NOTE]
> Reports are generated as Markdown. Figures and tables are inserted as auto-numbered placeholders (`**Figure 1.1 — Description**`).

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
