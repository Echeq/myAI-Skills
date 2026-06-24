# myAI-Skills

Modular, reusable skill packages for AI-assisted development. Each skill is a self-contained OpenCode agent with its own documentation and conventions.

## Quick Start

Browse the available skills below, or read the [Skill Index](docs/README.md) for full documentation.

| Skill | Trigger | Description |
|-------|---------|-------------|
| [ai-commit](docs/skills/ai-commit.md) | `@ai-commit` | Stage all changes and create a conventional commit |
| [ai-docs](docs/skills/ai-docs.md) | `@ai-docs` | Doc generation, update, and audit |
| [ai-log-generate](docs/skills/ai-log-generate.md) | `@ai-log` | Log every AI interaction |
| [ai-orchestrator](docs/skills/ai-orchestrator.md) | `@ai-orchestrator` | Intelligent task router with 4-tier auto-pipeline, memory system, adaptive planning, and hybrid confidence scoring |
| [ai-release](docs/skills/ai-release.md) | `@ai-release` | Changelog generation, SemVer bump, git tagging, and GitHub releases |
| [ai-env](docs/skills/ai-env.md) | `@ai-env` | Environment config manager, .env.example generation, secret auditing |
| [central-skills-hub-builder](docs/skills/central-skills-hub-builder.md) | — | Build skills hub repo from scratch |
| [auto-report](docs/skills/auto-report.md) | `@auto-report` | Interactive report generator with figure/table placeholders |
| [ai-audit](docs/skills/ai-audit.md) | `@ai-audit` | Code quality auditor with health scoring |

## Repository Structure

```
.agents/
  memory/             Session memory & token tracking (gitignored)
  plan/               Generated plans (gitignored)
  skills/             OpenCode agent/skill definitions
    <name>/SKILL.md   Skill package (frontmatter + instructions)
docs/                 Documentation
  README.md           Skill index
  guides/             Usage and creation guides
  reference/          Conventions and architecture
  skills/             Per-skill documentation pages
  audit/              Audit reports
```

## How It Works (ai-orchestrator)

The orchestrator follows a 5-phase workflow for every task:

1. **Pre-flight** — Reads session memory (`.agents/memory/orchestrator/`) and checks token budget. Injects previous context into the prompt. Warns if daily tokens are below 30%.
2. **Planning** — Generates a structured plan saved to `.agents/plan/`. Plan depth adapts to the tier (inline for SIMPLE, detailed with risks for VERY COMPLEX). User can review before execution.
3. **Execution** — Routes through the optimal pipeline tier (SIMPLE/MEDIUM/COMPLEX/VERY COMPLEX) using Flash and Deep subagents.
4. **Quality Assurance** — Runs hybrid confidence scoring using objective data: git diff analysis, static analysis (tsc, eslint, ruff if available), and pattern grep. Self-healing loop if score < 70.
5. **Post-flight** — Updates memory files (context rotation, token usage, decision log).

## Documentation

- [Skill Index](docs/README.md) — full index of all skills
- [Usage Guide](docs/guides/usage.md) — how to consume skills from external projects
- [Creating Skills](docs/guides/creating-skills.md) — how to create new skills
- [Conventions](docs/reference/conventions.md) — coding standards and technology choices
- [Architecture](docs/reference/ARCHITECTURE.md) — ADRs, complexity analysis, edge cases
