# Conventions

## Skill Structure

Every skill lives in `.agents/skills/<name>/` and consists of a single `SKILL.md` file with YAML frontmatter. No runtime code, no `src/`, no `package.json`.

```
.agents/skills/<name>/
├── SKILL.md          # YAML frontmatter + Markdown instructions
└── ...               # Optional sub-modules (ai-git hub, ai-router references/)
```

## Frontmatter Rules

| Field | Rule | Example |
| :--- | :--- | :--- |
| `name` | kebab-case, lowercase | `ai-git`, `auto-report` |
| `description` | One line, imperative tone | "Generates and audits Markdown documentation" |
| `triggers` | `@skill-name` with `@` prefix, kebab-case | `@ai-docs`, `@ai-git --commit` |
| `allowed-tools` | Comma-separated tool names | `Read, Write, Bash, Glob, Grep` |

## Trigger Convention

- All triggers use `@` prefix: `@ai-audit`, `@ai-env --scan`
- Flags use `--` prefix: `--full`, `--fix`, `--list`
- Trigger naming is kebab-case: `skill-search`, not `skillSearch` or `skill_search`
- Each trigger must be unique across all skills (ambiguous routing breaks the skill system)

## Diagram Standards

All generated Mermaid diagrams must include a `%%{init}%%` block constraining max-width and font size. See [Diagram Conventions](/docs/diagrams/README.md) for the exact directive pattern.

Place the directive as the **first line** of every Mermaid fenced code block, before any diagram content.

## Skill Creation Lifecycle

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart LR
    A[Create .agents/skills/&lt;name&gt;/] --> B[Write SKILL.md with frontmatter]
    B --> C[Add name, description, triggers]
    C --> D[Write agent instructions in Markdown]
    D --> E[Run @ai-config --check to validate]
    E --> F{Frontmatter valid?}
    F -->|No| G[Fix frontmatter]
    G --> E
    F -->|Yes| H[Run @ai-docs to generate doc page]
    H --> I[Skill is indexed and discoverable]
```

## Language

All instructions, comments, and documentation must be in professional English.

## Agent Setup

The file `agent/ROUTER.md` defines a standalone adaptive orchestrator agent. It should be installed to OpenCode's agent PATH so it's available as a subagent in other projects. Add it to your OpenCode configuration's agent paths or reference it via `{file:agent/ROUTER.md}` in `opencode.jsonc`.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
