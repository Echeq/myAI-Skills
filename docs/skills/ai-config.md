# ai-config

> **Trigger:** `@ai-config` | **Tools:** Read, Write, Bash, Glob, Grep | **Category:** Configuration

[📂 Skill Index](/docs/README.md) → **ai-config**

---

## Quick Reference

| Mode | Trigger | What happens |
|:-----|:--------|:-------------|
| Interactive | `@ai-config` | Choose validation mode from an interactive list |
| List | `@ai-config --list` | List all skills with name, description, and triggers |
| Check | `@ai-config --check` | Validate frontmatter, opencode.json, and .gitignore |
| Validate opencode | `@ai-config --validate-opencode` | Validate opencode.json/jsonc structure |
| Gitignore | `@ai-config --gitignore` | Check .gitignore coverage for generated paths |

> [!TIP]
> Run `@ai-config --check` after creating or editing any SKILL.md to catch frontmatter issues early.

## Overview

Configuration manager for this repository. Reads and validates opencode.json/.jsonc, skill frontmatter across `.agents/skills/`, and `.gitignore` consistency. Never edits code — only configuration manifests.

## Commands

| Flag | Description |
|:-----|:------------|
| `(bare)` | Interactive mode: choose validation from a list |
| `--list` | List all installed skills with name, description, and triggers |
| `--check` | Validate all skill frontmatter, opencode.json structure, and .gitignore |
| `--validate-opencode` | Validate the structure of opencode.json or opencode.jsonc |
| `--gitignore` | Check that .gitignore covers all generated and gitignored paths |

> [!NOTE]
> This skill only validates configuration. It does not modify any files. Use it as a gate before committing changes to skills or config.

---

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
