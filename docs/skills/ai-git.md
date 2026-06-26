# ai-git

Git/GitHub skill hub. Routes `--commit`, `--release`, `--branch`, and `--pr` to lightweight sub-skill files. Keeps each module small and token-efficient — only the requested module is loaded.

> **Trigger:** `@ai-git` | `@ai-git --commit` | `@ai-git --release` | `@ai-git --branch` | `@ai-git --pr`

## Quick Start

1. Type `@ai-git --commit` to stage and commit changes.
2. Type `@ai-git --release` to generate changelog, bump version, and create a GitHub release.
3. Type `@ai-git --branch` to create, switch, rename, or delete branches.
4. Type `@ai-git --pr` to create a GitHub PR from the current branch.
5. Type `@ai-git` (bare) to list available modules.

**Example:** `@ai-git --branch` → create a new branch `feature/xyz` from current HEAD.

## Description

A modular router for common Git and GitHub operations. Each sub-command (`--commit`, `--release`, `--branch`, `--pr`) loads its own instruction file from `.agents/skills/ai-git/`. This keeps the router lightweight and prevents token waste — only the module you actually use is read into context.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-git --commit` | Stage all changes and create a conventional commit |
| `@ai-git --release` | Changelog, SemVer bump, git tags, GitHub releases |
| `@ai-git --branch` | Create, switch, rename, delete branches |
| `@ai-git --pr` | Create GitHub PR from current branch (no auto-release) |
| `@ai-git` (bare) | Show help + list available modules |

## Configuration

No configuration needed. Relies on the repo's `.gitignore` for commit exclusions and `gh` CLI for PR/release operations.

> [!TIP]
> To add a new module: create `<name>.md` in `.agents/skills/ai-git/` and add the trigger to the SKILL.md frontmatter.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
