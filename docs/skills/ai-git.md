# ai-git

> **Trigger:** `@ai-git` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Version Control

[📂 Skill Index](/docs/README.md) → **ai-git**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Help | `@ai-git` | Show available sub-commands and usage |
| Commit | `@ai-git --commit` | Stage all changes, create a conventional commit |
| Release | `@ai-git --release` | Create a GitHub Release with auto-generated notes |
| Branch | `@ai-git --branch` | Create or switch branches with naming conventions |
| Pull Request | `@ai-git --pr` | Create a GitHub Pull Request with template |

> [!TIP]
> Always run `@ai-git --commit` before `@ai-git --release` to ensure all changes are committed first.

## Overview

Git/GitHub skill hub. Routes each sub-command (`--commit`, `--release`, `--branch`, `--pr`) to a lightweight sub-skill file in its own directory. Only the requested module is loaded, saving tokens.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Show help with all available sub-commands |
| `--commit` | Stage all changes, create a conventional commit (loads `commit.md`) |
| `--release` | Create a GitHub Release with auto-generated release notes (loads `release.md`) |
| `--branch` | Create or switch branches following naming conventions (loads `branch.md`) |
| `--pr` | Create a GitHub Pull Request with template (loads `pr.md`) |

> [!NOTE]
> Each sub-command loads its instructions from a separate `.md` file in `.agents/skills/ai-git/`. This keeps the skill token-efficient — only the module you need is loaded. The `--release` and `--pr` commands require GitHub CLI (`gh`) to be authenticated.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
