# ai-config

Configuration manager for this repo. Reads and validates opencode.json/.jsonc, skill frontmatter across `.agents/skills/`, and `.gitignore` consistency.

> **Trigger:** `@ai-config` | `@ai-config --list` | `@ai-config --check` | `@ai-config --validate-opencode` | `@ai-config --gitignore`

## Quick Start

1. Type `@ai-config --list` to see all skills with triggers.
2. Type `@ai-config --check` to run all consistency checks.
3. Type `@ai-config --validate-opencode` to validate subagent config.

**Example:** `@ai-config --check` → validates 10 skills → reports "✅ All trigger names are kebab-case" → "❌ Missing .gitignore entry".

## Description

Manages and validates this repo's configuration files. Never edits code — only config manifests. Reads SKILL.md frontmatter from all skills, opencode.jsonc structure, and .gitignore coverage. Checks for broken triggers, duplicate triggers, missing allowed-tools, and incomplete .gitignore entries.

## Usage

| Command | Action |
| :--- | :--- |
| `@ai-config` | Interactive: choose mode from list |
| `@ai-config --list` | List all skills with name, description, triggers |
| `@ai-config --check` | Run all consistency checks (triggers, naming, .gitignore) |
| `@ai-config --validate-opencode` | Validate opencode.jsonc structure |
| `@ai-config --gitignore` | Check .gitignore for recommended entries |

## Configuration

| Source | What is validated |
| :--- | :--- |
| `.agents/skills/*/SKILL.md` | Frontmatter: name (kebab-case), description, triggers (@-prefixed, kebab-case, unique), allowed-tools |
| `opencode.jsonc` | Subagent definitions: description, mode ("subagent"), permission (read + glob minimum) |
| `.gitignore` | Coverage for generated paths: `.agents/memory/`, `docs/log/`, `docs/audit/`, `docs/ai-audit/`, `docs/auto-report/` |

> [!NOTE]
> This skill validates but never edits configuration files unless explicitly asked. Run `@ai-config --check` periodically to catch drift.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-10 via @ai-docs update -->
