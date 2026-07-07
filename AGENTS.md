# myAI-Skills

8 prose-only `.md` OpenCode skills — **no runtime code, no src/, no tests,
no CI, no package.json**. No build/test/lint/typecheck commands exist; do
not attempt to run any.

## Truth & drift

| Source | Role | Edit policy |
|---|---|---|
| `.agents/skills/<name>/SKILL.md` | Authoritative skill definition | Manual |
| `docs/` tree | Generated summaries | **Never** edit directly; use `@ai-docs update` or `@ai-docs audit` |

The `docs/` tree frequently drifts from skills. Reconcile via `@ai-docs` before
trusting any doc page. Skills `ai-diagram` and `ai-orchestrator` exist in docs/
index but their `.agents/skills/` directories were deleted — `docs/` is stale.

## Structure

```
opencode.jsonc       2 subagents: orchestrator-scout (deepseek-chat, read-only)
                     & orchestrator-deep (deepseek-reasoner, full access)
agent/ROUTER.md      Standalone adaptive orchestrator agent definition
.agents/
  skills/<name>/SKILL.md   YAML-frontmatter agent instructions
  skills/ai-git/           Hub: commit.md | branch.md | pr.md | release.md
  skills/ai-router/        Hub: SKILL.md + references/ + scripts/ + assets/
docs/                      skills/ | guides/ | reference/ | audit/ | log/ | diagrams/
```

## Skills & trigger matrix

| Skill | Triggers |
|---|---|
| `ai-docs` | `@ai-docs`, `--pro`, `--update`, `--audit`, `--log` (with `--list\|--search\|--last\|--no-prompt\|--compact`) |
| `ai-git` | `@ai-git`, `--commit`, `--release`, `--branch`, `--pr` |
| `auto-report` | `@auto-report`, `--templates`, `--history`, `--config` |
| `ai-audit` | `@ai-audit`, `--full`, `--fix`, `--list`, `--diff` |
| `ai-env` | `@ai-env`, `--scan`, `--init`, `--validate`, `--audit` |
| `ai-config` | `@ai-config`, `--list`, `--check`, `--validate-opencode`, `--gitignore` |
| `skill-search` | `@skill-search`, `--list`, `--search`, `--install`, `--update`, `--info` |
| `ai-router` | `@ai-router` (pipeline: planner → executor → reviewer) |

Trigger convention: `@skill-name` (kebab-case, `@` prefix). Flags declared in
each `SKILL.md` frontmatter `triggers` field.

## Generated & gitignored paths

| Path | Source |
|---|---|
| `.agents/memory/` | `@ai-audit` regression tracking |
| `docs/log/` | `@ai-docs --log` |
| `docs/auto-report/` | `@auto-report` |
| `docs/ai-audit/` | `@ai-audit` |
| `docs/audit/` | `@ai-docs audit` |

## Platform & shell

- **Windows.** Use PowerShell syntax in commands.
- Command chaining: `cmd1; if ($?) { cmd2 }` — `&&` is not supported.
- **AGENTS.md is gitignored.** To commit: `git add -f AGENTS.md` (or remove
  from `.gitignore`).

## `opencode.jsonc` subagent roles

| Subagent | Model | Permissions |
|---|---|---|
| `orchestrator-scout` | `deepseek/deepseek-chat` | Read-only (edit/write denied) |
| `orchestrator-deep` | `deepseek/deepseek-reasoner` | Full access |

`agent/ROUTER.md` defines a third adaptive orchestrator agent that delegates
to these subagents via `task()` based on complexity classification.
