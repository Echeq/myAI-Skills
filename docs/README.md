# Skill Index

Welcome to the myAI-Skills documentation.

## Skills

| Skill | Trigger | Description |
| :--- | :--- | :--- |
| [ai-docs](skills/ai-docs.md) | `@ai-docs` | Doc generation, update, audit, and AI interaction logging |
| [ai-env](skills/ai-env.md) | `@ai-env` | Environment config manager, `.env.example` generation, secret auditing |
| [ai-git](skills/ai-git.md) | `@ai-git` | Git/GitHub skill hub with sub-modules: commit, release, branch, PR |
| [ai-orchestrator](skills/ai-orchestrator.md) | `@ai-orchestrator` | Intelligent task router with auto-pipeline, memory, planning, scoring, suggestions |
| [auto-report](skills/auto-report.md) | `@auto-report` | Interactive report generator with figure/table placeholders |
| [ai-audit](skills/ai-audit.md) | `@ai-audit` | Code quality auditor with health scoring |
| [ai-config](skills/ai-config.md) | `@ai-config` | Repo config manager: validate opencode.jsonc, skills frontmatter, .gitignore |

## Guides

- [Usage Guide](guides/usage.md) — how to consume skills from external projects
- [Creating Skills](guides/creating-skills.md) — how to create new skills

## Reference

- [Conventions](reference/conventions.md) — coding standards and technology choices
- [Architecture](reference/ARCHITECTURE.md) — ADRs, complexity analysis, edge cases

## Choosing the right audit skill

Three skills scan the repo, but each targets different things:

| If you need to... | Use | What it scans |
|---|---|---|
| Find bugs, security issues, performance problems in code | `@ai-audit` | Source files (entire repo) |
| Validate skill configuration (frontmatter, triggers, opencode.json) | `@ai-config` | `.agents/skills/*/SKILL.md`, `opencode.jsonc`, `.gitignore` |
| Manage environment variables, .env.example, hardcoded secrets | `@ai-env` | `process.env`, `os.getenv`, `.env` files, git history |

**Example workflow:** New to a repo? `@ai-config --check` first (structure), then `@ai-env --scan` (env vars), then `@ai-audit` (code quality).

<!-- Last updated: 2026-06-30 via @ai-docs update -->

---

**[⬆ Back to Top](#)** | **[📂 Root README](/README.md)**
