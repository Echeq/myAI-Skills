# Creating Skills

Guide to creating a new skill in this repository.

## Minimum Structure

```
.agents/skills/<skill-name>/
├── SKILL.md          # Metadata: name, description, allowed tools
├── src/index.ts      # Main code (or .py for Python)
├── tests/index.test.ts
├── README.md         # Documentation with usage examples
└── package.json      # Dependencies and scripts (or requirements.txt)
```

## SKILL.md

YAML frontmatter file that defines the skill as an OpenCode agent:

```yaml
---
name: my-skill
description: Brief description of what it does
allowed-tools: Read, Write, Bash
---
```

## Requirements

1. **Tests**: at least one unit test and one integration test in `tests/`.
2. **Documentation**: `README.md` must include at least 2 usage examples.
3. **Inject config**: skill receives configuration via parameters, never from global variables.
4. **Typing**: TypeScript strict types or Python type hints.
5. **SemVer**: initial version `1.0.0`; document versioning in the README.

## Recommended Scripts (package.json)

```json
{
  "scripts": {
    "test": "jest",
    "build": "tsc",
    "lint": "eslint src/"
  }
}
```

> [!NOTE]
> The `src/`, `tests/`, `README.md`, and `package.json` structure is the target for future skills. Current skills are plain `.md` files.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**
