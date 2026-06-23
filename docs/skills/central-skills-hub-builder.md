# Central Skills Hub Builder

Architect for building a repository of modular, reusable, self-contained skills.

> **Trigger:** No trigger (meta-skill, invoked by context)

## Description

Defines the architecture, principles, and workflow for building new skills in this repository. Not a triggerable agent but a specification loaded when building skills from scratch.

## Usage

When creating a new skill, follow the structure and rules defined in `.agents/skills/central-skills-hub-builder/SKILL.md`.

## Principles

- Self-contained packages with own deps, tests, docs
- Config injection over global env vars
- SemVer starting at `1.0.0`
- TypeScript by default, Python for data skills

> [!TIP]
> See [creating-skills.md](../creating-skills.md) for the step-by-step guide on building new skills.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
