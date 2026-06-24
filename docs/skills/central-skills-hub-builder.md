# Central Skills Hub Builder

Architect for building a repository of modular, reusable, self-contained skills.

> **Trigger:** No trigger (meta-skill, invoked by context)

## Quick Start

1. This skill defines the architecture for building new skills in this repo.
2. When creating a new skill, your agent follows the structure: `.agents/skills/<name>/SKILL.md`.
3. Each skill is self-contained with its own SKILL.md, README, and (when applicable) `src/`, `tests/`, `package.json`.
4. Default tech: TypeScript. Config injected via parameters. SemVer starting at `1.0.0`.

**Example:** New skill request → agent creates `.agents/skills/my-skill/SKILL.md` following the hub builder rules.

## Description

Defines the architecture, principles, and workflow for building new skills in this repository. Not a triggerable agent but a specification loaded when building skills from scratch.

## Usage

When creating a new skill, follow the structure and rules defined in `.agents/skills/central-skills-hub-builder/SKILL.md`.

## Configuration / Principles

- Self-contained packages with own deps, tests, docs
- Config injection over global env vars
- SemVer starting at `1.0.0`
- TypeScript by default, Python for data skills

> [!NOTE]
> This skill has no trigger command — it is loaded automatically when the agent detects a skill-building task.

> [!TIP]
> See [creating-skills.md](../guides/creating-skills.md) for the step-by-step guide on building new skills.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
