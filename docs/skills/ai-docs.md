# ai-docs

Generates, updates, and audits Markdown documentation in `/docs/`. Also
handles AI interaction logs via the `--log` sub-module.

> **Trigger:** `@ai-docs` | `@ai-docs pro` | `@ai-docs update` | `@ai-docs audit` | `@ai-docs --log`

## Quick Start

| Mode | Trigger | What happens |
| :--- | :--- | :--- |
| Generate | `@ai-docs` | Rebuilds skill index + all per-skill pages from `.agents/skills/` |
| Deep-dive | `@ai-docs pro <dir>` | Architectural doc with ADR, complexity, edge cases |
| Update | `@ai-docs update <name>` | Incremental update of one skill page (preserves manual edits) |
| Audit | `@ai-docs audit` | Compliance check with weighted score, saved to `/docs/audit/` |
| Log | `@ai-docs --log` | Log AI interaction to `docs/log/AI-LOG-*.md` |

**Example:** `@ai-docs` → all docs regenerated in ~10s. `@ai-docs audit` → score report generated.

## Description

Documentation lifecycle agent with 5 modes: full generation, professional deep-dive, incremental update, compliance audit, and AI interaction logging. Operates entirely in `/docs/`. Reads skill definitions from `.agents/skills/<name>/SKILL.md`.

## Architecture

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
stateDiagram-v2
    [*] --> Standard: @ai-docs
    [*] --> Professional: @ai-docs pro &lt;dir&gt;
    [*] --> Update: @ai-docs update &lt;name&gt;
    [*] --> Audit: @ai-docs audit
    [*] --> Log: @ai-docs --log

    Standard --> GenerateIndex: Glob .agents/skills/*/SKILL.md
    GenerateIndex --> GeneratePages: Per-skill template
    GeneratePages --> [*]

    Professional --> DeepDive: Read dir files
    DeepDive --> AddADR: Why this approach
    AddADR --> AddComplexity: Big-O analysis
    AddComplexity --> AddDeps: Mermaid dependency graph
    AddDeps --> AddEdgeCases: Concurrency + failure modes
    AddEdgeCases --> [*]

    Update --> CompareSources: Diff SKILL.md vs docs page
    CompareSources --> PreserveManual: Keep &lt;!-- MANUAL --&gt; blocks
    PreserveManual --> SyncMissing: Update only stale sections
    SyncMissing --> [*]

    Audit --> CheckCritical: 40% weight
    CheckCritical --> CheckWarning: 30% weight
    CheckWarning --> CheckSuggestion: 30% weight
    CheckSuggestion --> Score: PASS if &#8805; 80%
    Score --> [*]

    Log --> ReadLogModule: Load log.md sub-module
    ReadLogModule --> WriteLog: Write docs/log/AI-LOG-*.md
    WriteLog --> [*]
```

**Why five modes?** Each mode targets a different documentation need — fresh generation, deep architecture dives, incremental updates, compliance audits, and interaction logging. The state machine keeps them isolated so they never interfere.

## Usage

| Mode | Trigger | Output |
| :--- | :--- | :--- |
| Standard | `@ai-docs` | `/docs/README.md` + `/docs/skills/<name>.md` |
| Professional | `@ai-docs pro <dir>` | Single deep-dive `.md` with ADR, complexity, deps, edge cases. Includes `%%{init}%%` sizing directive per diagram conventions. |
| Update | `@ai-docs update <name>` | Updated `/docs/skills/<name>.md` |
| Audit | `@ai-docs audit` | `/docs/audit/DOCS_AUDIT_REPORT.md` (score 0-100%) |
| Log | `@ai-docs --log` | `docs/log/AI-LOG-{date}-{time}-{pc}.md` |

## Configuration

| Path | Purpose |
| :--- | :--- |
| `.agents/skills/<name>/SKILL.md` | Source of truth — frontmatter drives doc generation |
| `/docs/README.md` | Skill index (auto-generated) |
| `/docs/skills/<name>.md` | Per-skill doc pages (auto-generated) |
| `/docs/audit/` | Audit reports |

Use `<!-- MANUAL -->` comments in doc pages to preserve custom edits on update.

> [!NOTE]
> Standard mode regenerates ALL skill pages. Manual edits are overwritten unless protected with `<!-- MANUAL -->`.
> Audit compliance scoring: Critical 40%, Warnings 30%, Suggestions 30%. PASS if ≥ 80%.

> [!TIP]
> Use `@ai-docs pro <dir>` for deep-dive architecture docs with ADRs and dependency graphs.

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-07 via @ai-docs update -->
