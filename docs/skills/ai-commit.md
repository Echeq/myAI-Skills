# ai-commit

Stage all changes and create a conventional commit.

> **Trigger:** `@ai-commit`

## Description

Stages all tracked changes and commits them using conventional commit format. Excludes `.gitignore` entries (`.env`, `node_modules/`, `backend/generated/prisma/`).

## Usage

Invoke `@ai-commit` in any conversation. The agent will:

1. Read the diff of current changes
2. Generate a conventional commit message
3. Stage all files and commit

## Commit Types

`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

## Configuration

No parameters. Uses the repo's `.gitignore` for exclusions.

> [!NOTE]
> Root `package-lock.json` and `.opencode/plans/` are excluded if present.

> [!TIP]
> See the [Conventions](../conventions.md) doc for commit type standards.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
