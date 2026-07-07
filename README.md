# myAI-Skills

Modular, reusable skill packages for AI-assisted development. Each skill is a self-contained OpenCode agent with its own documentation and conventions.

## Quick Start

Browse the available skills below, or read the [Skill Index](docs/README.md) for full documentation.

| Skill | Trigger | Description |
|-------|---------|-------------|
| [ai-audit](docs/skills/ai-audit.md) | `@ai-audit` | Code quality auditor with health scoring |
| [ai-config](docs/skills/ai-config.md) | `@ai-config` | Config validator for frontmatter, opencode.jsonc, .gitignore |
| [ai-docs](docs/skills/ai-docs.md) | `@ai-docs` | Doc generation, update, audit, and AI interaction logging |
| [ai-env](docs/skills/ai-env.md) | `@ai-env` | Environment config manager, `.env.example` generation, secret auditing |
| [ai-git](docs/skills/ai-git.md) | `@ai-git` | Git/GitHub skill hub with sub-modules: commit, release, branch, PR |
| [ai-router](docs/skills/ai-router.md) | `@ai-router` | Task router with planner → executor → reviewer pipeline |
| [auto-report](docs/skills/auto-report.md) | `@auto-report` | Interactive report generator with multi-format export |
| [ai-orchestrator](docs/skills/ai-orchestrator.md) | `@ai-orchestrator` | DAG-based task orchestrator with dynamic classification and capability routing |
| [skill-search](docs/skills/skill-search.md) | `@skill-search` | Skill package manager: browse, install, update from GitHub |

## Standalone Agents

Installable OpenCode agents in `agent/` — copy to `~/.config/opencode/agents/`:

| Agent | File | Backed by |
|-------|------|-----------|
| ROUTER | `agent/ROUTER.md` | `@ai-router` (fixed 3-mode pipeline) |
| ORCHESTRATOR | `agent/ORCHESTRATOR.md` | `@ai-orchestrator` (DAG engine) |

See the [Agents Guide](docs/guides/agents.md) for installation and setup.

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

## Documentation

- [Skill Index](docs/README.md) — full index of all 8 skills with architecture diagrams
- [Usage Guide](docs/guides/usage.md) — how to invoke and chain skills
- [Creating Skills](docs/guides/creating-skills.md) — how to create new skills
- [Conventions](docs/reference/conventions.md) — naming, frontmatter, diagram standards
- [Architecture](docs/reference/ARCHITECTURE.md) — ADRs, complexity analysis, dependency graph
