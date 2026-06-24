---
name: auto-report
description: Interactive report generator. Collects user input, inserts content into a Markdown template, checks export dependencies, and outputs to /docs/auto-report/.
allowed-tools: Read, Write, Bash, Glob
triggers:
  - "@auto-report"
  - "@auto-report --templates"
  - "@auto-report --history"
  - "@auto-report --config"
---

# ROLE: Report Generator

Interactive report builder. Ask ONE question at a time. Fill a template, check dependencies for the target format, and save the result.

## Quick Start

| Mode | Trigger | What happens |
|---|---|---|
| Generate | `@auto-report` | 6-step wizard → choose format → dependency check → save as `edited_{template}.{ext}` |
| Templates | `@auto-report --templates` | List available template folders |
| History | `@auto-report --history` | Show past reports table |
| Config | `@auto-report --config` | View/edit saved settings |

## Output

```
/docs/auto-report/
├── .config.md                    Session history + defaults
├── README.md                     Report index
└── edited_{template}_{date}.{ext}  Generated reports
```

### Supported formats

| Format | Extension | Dependency | Fallback |
|---|---|---|---|
| Markdown | `.md` | None (native) | — |
| Word | `.docx` | `pandoc --version` | Warn + offer .md |
| PDF | `.pdf` | `pandoc --version` + pdf-engine | Warn + offer .md |
| HTML | `.html` | `pandoc --version` | Warn + offer .md |
| LaTeX | `.tex` | `pandoc --version` | Warn + offer .md |

The filename uses the template folder name (e.g., `default`) + date + extension:
`edited_default_2026-06-24.docx`

## Template Location

Templates are plain Markdown files in `.agents/skills/auto-report/templates/<name>/template.md`. Placeholders use `{{KEY}}` syntax: `{{TITLE}}`, `{{AUTHORS}}`, `{{DATE}}`, `{{ABSTRACT}}`, `{{BODY}}`.

## Dependency Detection

After the user chooses a format, run:

```
# Check pandoc (for docx, pdf, html, tex)
pandoc --version

# Check pdf engine (if format is pdf and pandoc exists)
pandoc --version | findstr "pdf"  # Windows
# OR on Linux/Mac:
pandoc --version | grep pdf
```

**If all dependencies found**: Proceed with conversion after generating .md.
**If missing**: "Required tool not found (pandoc). Generating in Markdown instead. To convert manually: `pandoc edited_default.md -o edited_default.docx`"

## Generation Flow (6 steps)

Ask ONE question at a time:

1. **Format** — "Output format? 1) Markdown .md  2) Word .docx  3) PDF  4) HTML  5) LaTeX .tex"
2. **Language** — "Language? 1) English 2) Chinese 3) Bilingual"
3. **Subject & Title** — "Subject? (CS, Chemistry, Physics…)" → "Report title?"
4. **Authors** — "Individual or group? If group, member names?"
5. **Sections** — Suggest sections based on subject (see Subject Adaptation). User confirms or edits.
6. **Content** — For each section, ask 1 question. Use their words, do not generate.

After content: "Any figures or tables? Name and section. I'll add auto-numbered placeholders."

Then run Dependency Detection. If okay, generate → convert → save as `edited_{template}_{date}.{ext}`.

### Output file
```markdown
# edited_{template}_{date}.{ext}
## Section 1
Content from user...

**Figure 1.1 — Description** *(Insert image)*
```

## Subject Adaptation

| Subject | Includes code? | Extra sections to suggest |
|---|---|---|
| CS, Programming, OS, AI, Web | Yes | Implementation, Algorithm Analysis, Complexity |
| Chemistry, Physics, Biology | No | Experimental Setup, Safety, Error Analysis |
| Literature, History | No | Theoretical Framework, Sources |
| Economics, Psychology | No | Data Sources, Statistical Methods |
| General | No | Standard sections only |

## Figure & Table Placeholders

Auto-number per section (1.1, 1.2, …). User says "I have a diagram" during the interview → skill inserts:

```markdown
**Figure 1.1 — Description** *(Insert image here)*
**Table 1.1 — Description** *(Insert table here)*
```

Language adapts label: English → "Figure/Table", Chinese → "图/表".

## Error Handling

| Issue | Action |
|---|---|
| No templates found | Use built-in academic template (Abstract, Introduction, Body, Conclusion, References) |
| User cancels mid-flow | Save partial session to `.config.md`, exit |
| Output dir missing | Create `/docs/auto-report/` |
| Dependency not found | Generate .md, print conversion command for user |
| Format unsupported | Fall back to .md |
