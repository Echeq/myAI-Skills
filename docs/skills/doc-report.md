# doc-report

Interactive report generator with figure/table placeholder auto-numbering.

> **Trigger:** `@doc-report` | `@doc-report --templates` | `@doc-report --history` | `@doc-report --config`

---

## File Map

```
.agents/skills/doc-report/           ← Skill definition & templates
  SKILL.md                           ← Agent instructions (this skill)
  templates/                         ← Read-only template library
    README.md                        ← How to create templates
    default/
      template.md                    ← Built-in academic template

docs/doc-report/                     ← Generated output (created on first use)
  README.md                          ← Output index
  .config.md                         ← Session history & defaults
  REPORT_{subject}_{date}.md         ← Generated reports

docs/skills/doc-report.md            ← This documentation page
```

---

## ADR-001: Markdown-Only Template Engine

**Status:** Adopted

**Context:** OpenCode agents operate in a text-only environment. Claims of DOCX, PDF, or LaTeX processing are non-executable.

**Decision:** Restrict template processing to Markdown (`.md`). Templates use `{{KEY}}` placeholder syntax replaced via string interpolation. No external tools required.

**Alternatives rejected:** Pandoc conversion, python-docx, LaTeX compilation — all require runtime environments not guaranteed in OpenCode sessions.

---

## ADR-002: Figure/Table Placeholder Auto-Numbering

**Status:** Adopted

**Context:** Academic reports require numbered figures (`Figure 1.1`) and tables (`Table 2.3`). The skill must insert these without the user manually tracking numbering.

**Decision:** Auto-number per-section. Section 1 = `1.1, 1.2, …`. Section 2 = `2.1, 2.2, …`. User provides name/description; skill assigns number and inserts bold placeholder.

**Format by language:**
| Language | Figure | Table |
| :--- | :--- | :--- |
| English | `**Figure 1.1 — Description**` | `**Table 1.1 — Description**` |
| Chinese | `**图 1.1 — Description**` | `**表 1.1 — Description**` |

---

## Complexity Analysis

**Generation pipeline (per session):**
1. Template scan: O(t) — list t template folders
2. Interactive Q&A: O(s × q) — s sections × q questions per section, bounded by ~20 interactions
3. Placeholder replacement: O(p) — p placeholders in template
4. Write output: O(1) — single file write

**Overall:** Linear in user input, no loops or recursion.

---

## Dependency Graph

```
@doc-report
  ├── Reads  → .agents/skills/doc-report/templates/<name>/template.md
  ├── Reads  → docs/doc-report/.config.md (if exists)
  ├── Writes → docs/doc-report/REPORT_{subject}_{date}.md
  └── Writes → docs/doc-report/.config.md
```

**External dependencies:** None. Self-contained within the repo.

---

## Stress / Edge Cases

| Case | Handling |
| :--- | :--- |
| Zero templates exist | Falls back to built-in academic template (Abstract, Introduction, Body, Conclusion, References) |
| User cancels mid-flow | Partial session saved to `.config.md`; prompt to resume |
| Same filename collision | Appends `-2`, `-3` suffix to avoid overwrite |
| Chinese characters in filenames | Transcribes subject to pinyin for safe filenames |
| `.config.md` corruption | Regenerates from defaults if unreadable |
| Very long user input | Truncated to reasonable paragraph size; warns user |

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
