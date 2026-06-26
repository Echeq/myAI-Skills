# myAI-Skills

Modular, reusable skill packages for AI-assisted development. Each skill is a self-contained OpenCode agent with its own documentation and conventions.

## Quick Start

Browse the available skills below, or read the [Skill Index](docs/README.md) for full documentation.

| Skill | Trigger | Description |
|-------|---------|-------------|
| [ai-docs](docs/skills/ai-docs.md) | `@ai-docs` | Doc generation, update, audit, and AI interaction logging |
| [ai-env](docs/skills/ai-env.md) | `@ai-env` | Environment config manager, `.env.example` generation, secret auditing |
| [ai-git](docs/skills/ai-git.md) | `@ai-git` | Git/GitHub skill hub with sub-modules: commit, release, branch, PR |
| [ai-orchestrator](docs/skills/ai-orchestrator.md) | `@ai-orchestrator` | Intelligent task router with 4-tier auto-pipeline, memory system, adaptive planning, and hybrid confidence scoring |
| [auto-report](docs/skills/auto-report.md) | `@auto-report` | Interactive report generator with figure/table placeholders |
| [ai-audit](docs/skills/ai-audit.md) | `@ai-audit` | Code quality auditor with health scoring |
| [central-skills-hub-builder](docs/skills/central-skills-hub-builder.md) | — | Build skills hub repo from scratch |

## Repository Structure

```
.agents/
  memory/             Session memory & token tracking
  plan/               Generated plans by date subdirectories
  skills/             OpenCode agent/skill definitions
    <name>/SKILL.md   Skill package (frontmatter + instructions)
    ai-git/           Git/GitHub skill hub (router + sub-modules)
docs/                 Documentation
  README.md           Skill index
  guides/             Usage and creation guides
  reference/          Conventions and architecture
  skills/             Per-skill documentation pages
  audit/              Audit reports
  log/                AI interaction logs (gitignored)
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
