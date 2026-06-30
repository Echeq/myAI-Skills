# Skill Index

Welcome to the myAI-Skills documentation.

## Skills

| Skill | Trigger | Description |
| :--- | :--- | :--- |
| [ai-audit](skills/ai-audit.md) | `@ai-audit` | Code quality auditor: security, performance, best practices |
| [ai-config](skills/ai-config.md) | `@ai-config` | Config manager: validate opencode.jsonc, skills frontmatter, .gitignore |
| [ai-diagram](skills/ai-diagram.md) | `@ai-diagram` | Diagram generator: flowcharts, sequence, class, Gantt, charts as Mermaid |
| [ai-docs](skills/ai-docs.md) | `@ai-docs` | Doc generation, update, audit, and AI interaction logging |
| [ai-env](skills/ai-env.md) | `@ai-env` | Environment config: .env.example, secret auditing, gitignore |
| [ai-git](skills/ai-git.md) | `@ai-git` | Git/GitHub hub: commit, release, branch, PR |
| [ai-orchestrator](skills/ai-orchestrator.md) | `@ai-orchestrator` | Task router with 4-tier pipeline and mandatory plan files |
| [auto-report](skills/auto-report.md) | `@auto-report` | Interactive report generator with multi-format export |
| [skill-search](skills/skill-search.md) | `@skill-search` | Skill package manager: browse, install, update from GitHub |

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

## Diagrams

Generated diagrams are saved as Mermaid blocks in `/docs/diagrams/`. They render natively on GitHub.

| Diagram | Source |
|---------|--------|
| [ai-diagram flow](diagrams/ai-diagram.md) | `@ai-diagram` self-diagram |
| [orchestrator 4-tier pipeline](diagrams/orchestrator-pipeline.md) | `@ai-orchestrator` routing |

---

**[⬆ Back to Top](#)** | **[📂 Root README](/README.md)**

<!-- Generated via @ai-docs on 2026-06-30 -->
