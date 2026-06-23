# myAI-Skills

Modular, reusable skill packages for AI-assisted development. Each skill is a self-contained OpenCode agent with its own documentation and conventions.

## Quick Start

Browse the available skills below, or read the [Skill Index](docs/README.md) for full documentation.

| Skill | Trigger | Description |
|-------|---------|-------------|
| [ai-commit](docs/skills/ai-commit.md) | `@ai-commit` | Stage all changes and create a conventional commit |
| [ai-docs](docs/skills/ai-docs.md) | `@ai-docs` | Doc generation, update, and audit |
| [ai-log-generate](docs/skills/ai-log-generate.md) | `@ai-log` | Log every AI interaction |
| [central-skills-hub-builder](docs/skills/central-skills-hub-builder.md) | — | Build skills hub repo from scratch |
| [doc-report](docs/skills/doc-report.md) | `@doc-report` | Interactive report generator with figure/table placeholders |

## Repository Structure

```
.agents/skills/       OpenCode agent/skill definitions
  <name>/SKILL.md     Skill package (frontmatter + instructions)
docs/                 Documentation
  README.md           Skill index
  guides/             Usage and creation guides
  reference/          Conventions and architecture
  skills/             Per-skill documentation pages
  audit/              Audit reports
```

## Documentation

- [Skill Index](docs/README.md) — full index of all skills
- [Usage Guide](docs/guides/usage.md) — how to consume skills from external projects
- [Creating Skills](docs/guides/creating-skills.md) — how to create new skills
- [Conventions](docs/reference/conventions.md) — coding standards and technology choices
- [Architecture](docs/reference/ARCHITECTURE.md) — ADRs, complexity analysis, edge cases
