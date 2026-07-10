# skill-search

> **Trigger:** `@skill-search` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Package Management

[📂 Skill Index](/docs/README.md) → **skill-search**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Interactive | `@skill-search` | Browse all available remote skills |
| List | `@skill-search --list` | List all installed local skills |
| Search | `@skill-search --search <query>` | Search remote repository by name or keyword |
| Install | `@skill-search --install <name>` | Download a skill to `.agents/skills/<name>/` |
| Update | `@skill-search --update <name>` | Re-download and overwrite an installed skill |
| Info | `@skill-search --info <name>` | Show detailed info about a remote skill |

> [!TIP]
> After installing a new skill, run `@ai-docs` to regenerate the documentation index so the new skill appears in the skill index.

## Overview

Package manager for OpenCode skills. Fetches skills from the [Echeq/myAI-Skills](https://github.com/Echeq/myAI-Skills) GitHub repository and installs them locally into `.agents/skills/<name>/`. Browse, search, install, update, and get info on available skills.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Browse all available remote skills from the GitHub repository |
| `--list` | List all locally installed skills |
| `--search <query>` | Search remote skills by name or keyword |
| `--install <name>` | Download and install a skill to `.agents/skills/<name>/` |
| `--update <name>` | Re-download and overwrite an already-installed skill |
| `--info <name>` | Show detailed information about a remote skill (description, triggers, version) |

> [!NOTE]
| Skills are fetched from the `Echeq/myAI-Skills` GitHub repository. After installing or updating a skill, run `@ai-docs` to regenerate the documentation index. After installing, you may also need to run `@ai-config --check` to validate the new skill's frontmatter.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
