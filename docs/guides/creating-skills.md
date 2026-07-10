# Creating Skills

> Guide to creating a new OpenCode skill in this repository.

[📂 Welcome](/docs/WELCOME.md) • [📂 Skill Index](/docs/README.md) • [📂 Conventions](/docs/reference/conventions.md)

---

## Why Prose-Only?

Skills in this repo are plain Markdown files with YAML frontmatter — no executable code, no build steps, no package managers:

- **Zero friction** — Write instructions, not code. No TypeScript compilation, no dependency resolution, no CI pipelines.
- **Token-efficient** — The agent reads only what it needs. A 50-line SKILL.md loads instantly.
- **Version-controllable** — Every change is a readable diff, unlike compiled or binary formats.

---

## Creation Flow

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart TD
    A[Create .agents/skills/&lt;name&gt;/ directory] --> B[Write SKILL.md]
    B --> C[Add YAML frontmatter]
    C --> D[Set name: kebab-case]
    D --> E[Set description: one-line imperative]
    E --> F[Add triggers: @skill-name]
    F --> G[Write agent instructions in Markdown]
    G --> H[Run @ai-config --check]
    H --> I{Valid?}
    I -->|No| J[Fix frontmatter issues]
    J --> H
    I -->|Yes| K[Run @ai-docs to generate doc page]
    K --> L[Skill is indexed and discoverable]
    L --> M[Test: type @your-skill in OpenCode]
```

---

## Skill Design Pattern

Skills follow a standard format:

```
my-skill/
├── SKILL.md       # required: name, description, instructions
├── scripts/       # optional: executable code
├── references/    # optional: docs and specs
└── assets/        # optional: templates and data
```

Hubs like `ai-git` and `ai-router` use sub-modules in the same directory for token efficiency: the main `SKILL.md` routes to specialized `.md` files, so only the needed instructions are loaded.

---

## Installation Paths

Skills can be installed in any of these locations (project paths override global ones):

| Tool | Project path | Global path |
|:-----|:-------------|:------------|
| OpenCode | `.opencode/skills/<name>/SKILL.md` | `~/.config/opencode/skills/<name>/SKILL.md` |
| Claude Code | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Compatible | `.agents/skills/<name>/SKILL.md` | `~/.agents/skills/<name>/SKILL.md` |

---

## SKILL.md Anatomy

### Frontmatter

```yaml
---
name: my-skill
description: What this skill does in one line
triggers:
  - "@my-skill"
  - "@my-skill --flag"
allowed-tools: Read, Write, Bash, Glob, Grep
---
```

| Field | Required | Why |
|:------|:---------|:----|
| `name` | Yes | Kebab-case identifier. Must be unique across all skills. Used as the directory name. |
| `description` | Yes | One-liner shown in `@skill-search --list` and the doc index. Imperative tone preferred. |
| `triggers` | Recommended | List of `@trigger` strings. First one is the primary trigger. Must be unique. |
| `allowed-tools` | Optional | Comma-separated tools the agent may use. If omitted, OpenCode's default permissions apply. |

### Instructions

After the frontmatter, write Markdown instructions for the agent. Start with a clear role definition:

```markdown
# ROLE: MySkillName

Do X, Y, and Z. Follow these rules:
```

### Sub-Modules

If your skill has multiple distinct commands, split them into separate `.md` files:

```
.agents/skills/ai-git/
├── SKILL.md          # Router: loads sub-module by flag
├── commit.md         # @ai-git --commit
├── branch.md         # @ai-git --branch
├── pr.md             # @ai-git --pr
└── release.md        # @ai-git --release
```

This saves tokens: the agent only reads the sub-module for the flag you used.

---

## Validation Checklist

Before submitting a new skill:

- [ ] `name` is kebab-case and matches the directory name
- [ ] `description` is a single imperative sentence
- [ ] At least one trigger with `@` prefix
- [ ] No trigger conflicts with existing skills
- [ ] Instructions are in professional English
- [ ] `@ai-config --check` passes
- [ ] `@ai-docs` generates the skill's doc page

> [!TIP]
> Look at existing skills for reference. `skill-search` is a good minimal example (single switchable commands). `ai-router` shows a complex pipeline with sub-modules and references.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
