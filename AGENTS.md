# myAI-Skills

## Status

Repo de skills OpenCode. Las 5 skills existentes son archivos `.md` sin código, deps, ni tests. No hay `opencode.json`, `package.json`, CI, ni build system.

## Structure

```
.agents/      OpenCode agent/skill definitions
  skills/<name>/SKILL.md  — skill packages
docs/         Usage, creation guides, conventions
```

## Existing Skills

| Directory | Trigger | Purpose |
|-----------|---------|---------|
| `ai-commit` | `@ai-commit` | Stage all changes and create a conventional commit |
| `ai-docs` | `@ai-docs` | Doc generation, update, and audit |
| `ai-log-generate` | `@ai-log` | Log every AI interaction |
| `central-skills-hub-builder` | — | Build skills hub repo from scratch |
| `auto-report` | `@auto-report` | Interactive report generator |
| `ai-audit` | `@ai-audit` | Code quality auditor |

## Key Rules

- **Self-contained skills.** Each `.agents/skills/<name>/` is an independent package with own deps, tests, docs.
- **Config injection.** Skills receive config via parameters, not global env vars.
- **SemVer.** Every skill starts at `1.0.0`.
- **TypeScript** by default; **Python** for data/scripting skills.
- **English** for all code, comments, and variable names.

## Commands

None established yet. When a skill uses a build/test/lint tool, document the exact command here.
