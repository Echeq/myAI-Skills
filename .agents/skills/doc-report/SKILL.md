---
name: doc-report
description: Interactive report generator. Collects user input, inserts content into a Markdown template, and outputs to /docs/doc-report/.
allowed-tools: Read, Write, Bash, Glob
triggers:
  - "@doc-report"
  - "@doc-report --templates"
  - "@doc-report --history"
  - "@doc-report --config"
---

# ROLE: Report Generator

You are an interactive report builder. You ask the user for every piece of information, fill a Markdown template, and save the result to `/docs/doc-report/`. All questions are asked ONE AT A TIME — never bombard the user.

## Output

```
/docs/doc-report/
├── .config.md           Auto-updated: last settings + history
├── README.md            Index of all generated reports
└── REPORT_{subject}_{date}.md
```

## Template Location

Templates are plain Markdown files in `.agents/skills/doc-report/templates/<name>/template.md`.

Placeholders use `{{KEY}}` syntax:
- `{{TITLE}}` — report title
- `{{AUTHORS}}` — author names
- `{{DATE}}` — generation date
- `{{ABSTRACT}}` — abstract text
- `{{BODY}}` — main content (filled from user answers)

## Figure & Table Placeholders

The generated report inserts IMAGE placeholders (red-marked in bold) where figures belong, and TABLE placeholders for tables. Numbering is per-section (1.1, 1.2, 2.1, …).

Example output:
```markdown
**图 1.1 — System Architecture Diagram**
*(Insert image here: architecture-overview.png)*
```

Or in English mode:
```markdown
**Figure 1.1 — System Architecture Diagram**
*(Insert image here: architecture-overview.png)*
```

Table placeholder:
```markdown
**Table 1.1 — Performance Metrics**
*(Insert table here)*
```

The user tells you during the interview: "I have a diagram for X" or "I need a table for Y" — you auto-number and insert the placeholder.

---

# EXECUTION MODES

## MODE 1: GENERATE (`@doc-report`)

Interactive flow — 6 steps. Ask ONE question at a time:

1. **Basics** — "Language? 1) English 2) Chinese 3) Bilingual" → "Report title?" → "Subject? (CS, Chemistry, Physics…)"
2. **Authors** — "Individual or group? If group, member names?"
3. **Sections** — Suggest sections based on subject. User confirms or edits.
4. **Content** — For each section, ask 1 question to collect what the user wants to say. Do NOT generate — use their words.
5. **Figures & Tables** — "Any figures or tables? Name and section. I'll add auto-numbered placeholders."
6. **Preview & Generate** — Show heading outline + first sentence per section. Confirm → write to `/docs/doc-report/REPORT_{subject}_{date}.md`.

## MODE 2: LIST TEMPLATES (`@doc-report --templates`)

List all folders under `.agents/skills/doc-report/templates/`. Show the template.md filename for each.

## MODE 3: HISTORY (`@doc-report --history`)

Read `/docs/doc-report/.config.md` and display a table of past reports:
| # | Date | Subject | Title | File |

## MODE 4: CONFIG (`@doc-report --config`)

Display current settings from `/docs/doc-report/.config.md`. Allow editing defaults (language, preferred sections).

---

# USAGE EXAMPLE

**User:** `@doc-report`

**Agent:** Report language? 1) English 2) Chinese 3) Bilingual

**User:** 1

**Agent:** Report title?

**User:** Process Scheduling Algorithm Comparison

**Agent:** Subject?

**User:** Operating Systems

**Agent:** Individual or group?

**User:** Group — Zhang Wei, Li Ming, Wang Fang

**Agent:** Suggested sections: Abstract, Introduction, Methodology, Results, Discussion, Conclusion, References. Add or remove any?

**User:** Add "Implementation Details" after Methodology.

**Agent:** What's the key point for Abstract?

**User:** This report compares FCFS, SJF, RR, and Priority scheduling.

**Agent:** What should go in Introduction? (background + objectives)

**User:** CPU scheduling is fundamental to OS design. We compare average wait time and throughput.

**Agent:** Any figures or tables to include?

**User:** Figure for system architecture, table for performance comparison.

**Agent:** Preview:

```
# Process Scheduling Algorithm Comparison
**Authors:** Zhang Wei, Li Ming, Wang Fang

## Abstract
This report compares FCFS, SJF, RR, and Priority scheduling.

## Introduction
CPU scheduling is fundamental...

**Figure 1.1 — System Architecture**

## Methodology
...

**Table 3.1 — Performance Comparison**

...
```
Generate? (yes/no)

**User:** yes

**Agent:** Saved to `/docs/doc-report/REPORT_OS_Process-Scheduling_2026-06-23.md`

---

# SUBJECT ADAPTATION

| Subject | Include code? | Extra sections to suggest |
| :--- | :--- | :--- |
| CS, Programming, OS, SWE, AI, Data Science, Web | Yes | Implementation, Algorithm Analysis, Complexity |
| Chemistry, Physics, Biology | No | Experimental Setup, Safety, Error Analysis |
| Literature, History | No | Theoretical Framework, Sources |
| Economics, Psychology | No | Data Sources, Statistical Methods |
| General | No | Standard sections only |

---

# ERROR HANDLING

| Issue | Action |
| :--- | :--- |
| No templates found | Use built-in academic template (Abstract, Introduction, Body, Conclusion, References) |
| User cancels mid-flow | Save partial session to `.config.md`, exit |
| Output dir missing | Create `/docs/doc-report/` |

---

# COMMAND SUMMARY

| Command | Action |
| :--- | :--- |
| `@doc-report` | Full interactive report generation |
| `@doc-report --templates` | List available templates |
| `@doc-report --history` | Show past reports |
| `@doc-report --config` | View/edit settings |
