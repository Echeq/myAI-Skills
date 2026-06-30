# Creating Skills

Guide to creating a new skill in this repository.

## Minimum Structure

```
.agents/skills/<skill-name>/
├── SKILL.md          # Frontmatter (name, description, triggers) + instructions
```

## SKILL.md

YAML frontmatter file that defines the skill as an OpenCode agent:

```yaml
---
name: my-skill
description: Brief description of what it does
triggers:
  - "@my-skill"
allowed-tools: Read, Write, Bash  # optional
---
```

## Requirements

1. **Prose-only**: Skills are plain `.md` files with YAML frontmatter. No executable code.
2. **Frontmatter**: Must include `name` (kebab-case) and `description`. `triggers` and `allowed-tools` are optional but recommended.
3. **Trigger convention**: `@skill-name` — kebab-case with `@` prefix.

> [!NOTE]
> All current skills in this repo are plain `.md` files with no `src/`, `tests/`, or `package.json`. The old executable-package model is aspirational and not used.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
