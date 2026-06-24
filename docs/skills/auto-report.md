# auto-report

Interactive report generator with multi-format export, dependency detection, and figure/table auto-numbering.

> **Trigger:** `@auto-report` | `@auto-report --templates` | `@auto-report --history` | `@auto-report --config`

## Quick Start

1. Type `@auto-report` to start the interactive wizard.
2. Answer 6 questions: format → language → subject → title → authors → sections → content.
3. Add figures and tables — auto-numbered per section.
4. Skill checks dependencies for your chosen format. If missing, falls back to Markdown.
5. Report saved as `edited_{template}_{date}.{ext}`.

**Example (standard):** `@auto-report` → .docx → English → CS → "Process Scheduling" → Group of 3 → confirm sections → pandoc found → saved as `edited_default_2026-06-24.docx`.

**Example (Chinese University):** `@auto-report` → .pdf → Chinese → Chinese University → "操作系统分析" → "Peking University" → "CS-301" → Group of 3 → generated with GB/T 7714-2015 formatting.

## Description

Interactive report builder that asks step-by-step for format, language, subject, title, authors, sections, and content. Fills a Markdown template (standard academic or Chinese university GB/T 7714-2015), checks export dependencies (pandoc for docx/pdf/html/tex), and outputs to `edited_{template}_{date}.{ext}`. Supports figure/table placeholder auto-numbering per section.

## Usage

| Command | Action |
| :--- | :--- |
| `@auto-report` | Full interactive report generation |
| `@auto-report --templates` | List available templates |
| `@auto-report --history` | Show past reports |
| `@auto-report --config` | View/edit settings |

### Supported formats

| Format | Extension | Dependency | Fallback |
| :--- | :--- | :--- | :--- |
| Markdown | `.md` | None | — |
| Word | `.docx` | `pandoc` | Warn + offer .md |
| PDF | `.pdf` | `pandoc` + pdf-engine | Warn + offer .md |
| HTML | `.html` | `pandoc` | Warn + offer .md |
| LaTeX | `.tex` | `pandoc` | Warn + offer .md |

## Configuration

Output: `/docs/auto-report/edited_{template}_{date}.{ext}`. Templates read from `.agents/skills/auto-report/templates/<name>/template.md`. Session data persisted to `/docs/auto-report/.config.md`. Dependencies checked at generation time via bash.

> [!NOTE]
> Native Markdown generation requires no external tools. Other formats require `pandoc`. If missing, the skill generates a `.flag` file with the OS-specific install command (`winget`, `choco`, `brew`, or `apt`).

> [!WARNING]
> PDF generation requires `pandoc` + a pdf-engine (weasyprint, wkhtmltopdf, or xelatex). If only pandoc is found, the skill warns and offers .md.

> [!TIP]
> Use `@ai-orchestrator --plan` before generating a report to plan the structure first.

## Chinese University Format (GB/T 7714-2015)

When the subject is "Chinese University", the report follows national academic formatting standards:

| Element | Standard |
| :--- | :--- |
| Body font | SimSun (宋体) 12pt (小四) |
| Title | 22pt (二号) bold, centered |
| H1 | 16pt (三号) bold |
| H2 | 14pt (四号) bold |
| Body | SimSun 12pt, 1.5x line spacing, 2em first-line indent |
| Margins | L: 3cm, R: 2.5cm, T/B: 2.5cm |
| Header | Course name (left) / University (right) |
| Footer | Centered page number |
| English/nums | Times New Roman |

The template includes pandoc YAML frontmatter for proper CJK rendering. PDF output requires `xelatex` or `ctex` LaTeX distribution.

## File Map

```
.agents/skills/auto-report/           ← Skill definition & templates
  SKILL.md                           ← Agent instructions (this skill)
  templates/                         ← Read-only template library
    README.md                        ← How to create templates
    default/
      template.md                    ← Built-in academic template

docs/auto-report/                     ← Generated output
  README.md                          ← Output index
  .config.md                         ← Session history & defaults
  edited_{template}_{date}.{ext}     ← Generated reports (format varies)
  install_{tool}.flag                ← Dependency installers (created on demand)

docs/skills/auto-report.md            ← This documentation page
```

---

## ADR-001: Template Engine + Format Detection

**Status:** Adopted 2026-06-24

**Context:** Users requested Word/PDF/HTML export. Direct generation requires runtime tools not guaranteed in OpenCode sessions.

**Decision:** Always generate Markdown first (guaranteed). Then check for `pandoc` at generation time via bash. If found, convert. If not, print the exact pandoc command for manual use. This keeps the skill self-contained while supporting multi-format when tools exist.

**Alternatives rejected:** Bundling pandoc, python-docx scripts — adds dependencies that may not be available.

---

## ADR-002: Figure/Table Placeholder Auto-Numbering

**Status:** Adopted

**Context:** Academic reports require numbered figures (`Figure 1.1`) and tables (`Table 2.3`). The skill must insert these without the user manually tracking numbering.

**Decision:** Auto-number per-section. Section 1 = `1.1, 1.2, …`. Section 2 = `2.1, 2.2, …`. Language adapts: English → "Figure/Table", Chinese → "图/表".

---

## Complexity Analysis

**Generation pipeline (per session):**
1. Format selection: O(1)
2. Dependency check: O(1) bash call
3. Template scan: O(t)
4. Interactive Q&A: O(s × q), bounded ~20 interactions
5. Placeholder replacement: O(p)
6. Write output: O(1)
7. Conversion (if tools found): O(1) bash call

**Overall:** Linear. No loops or recursion.

---

## Dependency Graph

```
@auto-report
  ├── Reads  → .agents/skills/auto-report/templates/<name>/template.md
  ├── Reads  → docs/auto-report/.config.md (if exists)
  ├── Checks → pandoc --version (bash, for non-.md formats)
  ├── Writes → docs/auto-report/edited_{template}_{date}.{ext}
  └── Writes → docs/auto-report/.config.md
```

**External dependencies:** `pandoc` optional (for docx/pdf/html/tex export). Core functionality is self-contained.

---

## Stress / Edge Cases

| Case | Handling |
| :--- | :--- |
| No templates found | Falls back to built-in academic template |
| User cancels mid-flow | Partial session saved to `.config.md` |
| Same filename collision | Appends `-2`, `-3` suffix |
| Chinese characters in filenames | Transcribes subject to pinyin |
| `.config.md` corruption | Regenerates from defaults |
| Very long user input | Truncated, warns user |
| pandoc not installed | Generates .md + writes `install_pandoc.flag` with OS-specific command |
| pandoc found but pdf-engine missing | Generates .md + writes `install_pdf-engine.flag` |
| Flag file already exists | Overwrites with latest command (stale flags are harmless) |

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
