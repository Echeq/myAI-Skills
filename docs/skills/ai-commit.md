# ai-commit

Stage all changes and create a conventional commit.

> **Trigger:** `@ai-commit`

## Quick Start

1. Type `@ai-commit` in any conversation where you have uncommitted changes.
2. The agent reads your `git diff` and generates a conventional commit message.
3. Review the message. Confirm. All files are staged and committed.

**Example:** `@ai-commit` → message generated → commit created.

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
> See the [Conventions](../reference/conventions.md) doc for commit type standards.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
