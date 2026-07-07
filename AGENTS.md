# myAI-Skills

8 prose-only Markdown skills for OpenCode — **no runtime code, no `src/`, no tests, no CI, no `package.json`, no build/lint/test commands.** Do not try to run any.

## Source of truth

| What | Trust |
|---|---|
| `.agents/skills/<name>/SKILL.md` | Authoritative. **Edit these.** |
| `docs/` tree | Auto-generated. **Never edit directly.** Use `@ai-docs update` or `@ai-docs audit`. |
| `opencode.json` / `.jsonc` | **Does not exist on disk.** Referenced in docs but absent. |
| `agent/ROUTER.md` | Standalone adaptive-orchestrator agent. Install to your OpenCode agent PATH for use across projects. |

## Skills (8)

| Trigger | Skill | Notes |
|---|---|---|
| `@ai-docs` | Doc generation, update, audit, logging | 5 modes. Sub-module: `log.md`. |
| `@ai-git --commit\|--release\|--branch\|--pr` | Git/GitHub hub | Loads sub-module `.md` by flag. Bare `@ai-git` prints help. |
| `@auto-report` | Interactive 8-step wizard | Formats: md, docx, pdf, html, tex. Falls back to `.md` if pandoc missing. |
| `@ai-audit` | Quality auditor | 5 weighted categories. Regression tracking in `.agents/memory/`. |
| `@ai-env --scan\|--init\|--validate\|--audit` | Env var lifecycle | Scans `process.env`, `os.getenv`, etc. Never reads actual `.env`. |
| `@ai-config --check\|--list\|--validate-opencode\|--gitignore` | Config & frontmatter validator | Validates triggers, naming, `.gitignore`. |
| `@skill-search --list\|--search\|--install\|--update\|--info` | Skill package manager | Fetches from `Echeq/myAI-Skills` GitHub. Rate-limited API + raw fallback. |
| `@ai-router` | Pipeline: planner → executor → reviewer | Requires 4 configured subagents. Has `--init` for setup. |

**Trigger rules:** `@` prefix, kebab-case, unique across repo. Flags use `--` prefix.

**Skills can also be invoked programmatically** via the `skill()` tool from within another skill or agent.

## Agent sub-agent types

Available for `task()` with `subagent_type`:
- `ai-router-planner` — strategic planning
- `ai-router-executor` — code execution / applying changes
- `ai-router-reviewer` — full review (pro model)
- `ai-router-reviewer-flash` — lightweight review (flash model)
- `explore` — fast codebase search, read-only
- `general` — multi-step tasks that don't fit elsewhere

## Structure

```
.agents/skills/<name>/SKILL.md       — YAML frontmatter + Markdown instructions
.agents/skills/ai-git/               — hub: commit.md, branch.md, pr.md, release.md
.agents/skills/ai-router/            — hub: SKILL.md + references/ (config, init, manager, worker, supervisor)
.agents/skills/auto-report/templates/ — subject-specific templates
agent/ROUTER.md                      — standalone adaptive orchestrator agent definition
```

## Platform

- **Windows (PowerShell).** Command chaining: `cmd1; if ($?) { cmd2 }` — `&&` not supported.
- **AGENTS.md is gitignored.** To commit: `git add -f AGENTS.md`.
- **No `opencode.json`/`.jsonc`** exists on disk despite docs references. The `@ai-config --validate-opencode` command will fail.
- **MIT License.** Copyright (c) 2026 CHEN QIU ELVIS ENRIQUE.

## Conventions

- All Mermaid diagrams must include `%%{init}%%` sizing directive as first line. See `docs/diagrams/README.md`.
- `<!-- MANUAL -->` and `<!-- CUSTOM -->` comment blocks in docs are preserved by `@ai-docs update`.
- Professional English only in all instructions, comments, and documentation.

## Generated & gitignored paths

| Path | Source |
|---|---|
| `.agents/memory/` | `@ai-audit` regression tracking |
| `.agents/skills/ai-router/assets/plan/` | `@ai-router` plan artifacts |
| `.agents/skills/ai-router/assets/state/` | `@ai-router` state & history |
| `docs/log/` | `@ai-docs --log` |
| `docs/auto-report/` | `@auto-report` |
| `docs/ai-audit/` | `@ai-audit` |
| `docs/audit/` | `@ai-docs audit` |
