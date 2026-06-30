# ai-diagram

Generates diagrams as Mermaid code blocks. Supports flowcharts, sequence diagrams, class diagrams, Gantt charts, and bar/line/pie charts. Output is pure Markdown — no external tools needed for rendering in GitHub.

> **Trigger:** `@ai-diagram` | `flowchart` | `sequence` | `class` | `gantt` | `chart` | `--render`

## Quick Start

1. Type `@ai-diagram flowchart login` to start a flowchart interactively.
2. Answer one step at a time. Type "done" when finished.
3. Skill outputs a ` ```mermaid ` block ready to paste into any Markdown file.

**Example:** `@ai-diagram sequence API call` → defines actors (Client, Server, DB) and interactions → generates Mermaid block.

## Description

Interactive diagram generator that asks one question at a time. Covers 5 diagram types, all outputting Mermaid syntax — a widely-supported markup language for diagrams that renders natively on GitHub, GitLab, and many Markdown viewers. Optionally renders to PNG/SVG via `mmdc` (Mermaid CLI).

Diagrams are saved to `/docs/diagrams/<topic>.md` and can be embedded into `auto-report` templates by copying the Mermaid code block.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-diagram` | Interactive: choose type → topic → details → generate |
| `@ai-diagram flowchart <topic>` | Auto-generate flowchart from topic alone |
| `@ai-diagram sequence <topic>` | Auto-generate sequence diagram from topic alone |
| `@ai-diagram class <topic>` | Auto-generate class diagram from topic alone |
| `@ai-diagram gantt <topic>` | Auto-generate Gantt chart from topic alone |
| `@ai-diagram chart <topic>` | Auto-generate chart from topic alone |
| `@ai-diagram --render <file.md>` | Convert Mermaid blocks to PNG (requires `mmdc`) |

## Configuration

| Path | Purpose |
| :--- | :--- |
| `/docs/diagrams/` | Saved diagram Markdown files |
| `.agents/skills/ai-diagram/SKILL.md` | Skill definition |

Optional: `mmdc` (Mermaid CLI) for PNG/SVG export. Install via `npm install -g @mermaid-js/mermaid-cli`.

## ADR: Mermaid Over Image-Based Tools

**Status:** Adopted 2026-06-30

**Context:** The skill could generate diagrams as images (PNG via matplotlib, Graphviz, or PlantUML) or as text-based markup. Images require external tools and don't render in diffs.

**Decision:** Use Mermaid as the primary output format. It is:
- **Text-based**: renders in GitHub/GitLab natively, visible in code review diffs
- **Zero-dependency**: no install needed for Markdown output
- **Portable**: can be copied into any `.md` file, including auto-report templates

**Consequences:**
- Positive: No build step or dependency for basic usage
- Positive: Diagrams are version-controlled and diffable
- Negative: Mermaid has limited styling compared to matplotlib
- Negative: PNG export requires `mmdc` (optional)

## Complexity Analysis

**Time complexity:** O(n) where n = number of user answers. Each answer maps to one element in the diagram (node, edge, actor, message, task). No loops or recursive generation.

**Space complexity:** O(d) where d = diagram size in nodes. The full diagram state is held in conversation context and written once to the output file.

## Dependency Graph

```
@ai-diagram
  ├── Reads     → user answers (interactive, 1 at a time)
  ├── Generates → Mermaid code (text, no external calls)
  ├── Writes    → /docs/diagrams/<topic>.md
  └── Optional  → bash: mmdc for PNG render
```

**External dependencies:** None for Markdown output. Optional: `mmdc` (npm package) for PNG/SVG.

## Stress / Edge Cases

| Case | Handling |
| :--- | :--- |
| User provides vague details | Ask clarifying questions one at a time |
| Chart data includes non-numeric values | Validate and prompt to fix |
| Very large diagram (100+ nodes) | Works, but Mermaid rendering may slow in browser |
| mmdc not installed | Inform user, fall back to Markdown block |
| Same topic name overwrites existing file | Warn and confirm before overwrite |
| User cancels mid-flow | No partial files written |

> [!NOTE]
> Mermaid blocks render natively on GitHub, GitLab, and any Markdown viewer that supports Mermaid. No plugins needed.

> [!TIP]
> Use `@ai-diagram` before `@auto-report` to generate diagrams for your report, then paste the Mermaid block into the report template.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Generated via @ai-docs pro on 2026-06-30 -->
