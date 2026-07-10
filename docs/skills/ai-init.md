# ai-init

Bootstraps foundational project documentation in under 5 minutes. Auto-detects stack and tooling, asks minimal questions, generates 4 docs in `/docs/ai-init/`, and updates AGENTS.md. Includes `validate` sub-command for drift detection.

> **Trigger:** `@ai-init` | `@ai-init validate` | `@ai-init --types` | `@ai-init --features` | `@ai-init --screaming`

## Quick Start

1. Type `@ai-init` to bootstrap your project.
2. The skill auto-detects your stack and tooling — confirm or correct.
3. Answer 3–5 questions about structure, data flow, and conventions.
4. 4 docs are generated in `/docs/ai-init/` and AGENTS.md is updated.

**Example:** `@ai-init` → auto-detects Node.js + ESLint + Jest → asks folder structure → generates ARCHITECTURE.md, CONVENTIONS.md, DECISIONS.md, ERRORS.md → updates AGENTS.md.

## Description

Lays the foundational documentation and memory of a project. Auto-detects language, framework, and tooling from manifest files (`package.json`, `pyproject.toml`, etc.), then asks the few questions code can't answer — folder structure, data flow, design patterns, constraints. Generates 4 markdown files designed to be living documents, not one-time artifacts.

## Usage

| Mode | Trigger | Action |
| :--- | :--- | :--- |
| Full Wizard | `@ai-init` | Auto-detect → interactive questions → generate 4 docs → update AGENTS.md |
| Validation | `@ai-init validate` | Compare documented info against actual code; report drift |
| Types Structure | `@ai-init --types` | Skip folder-structure question; assume by-layer (controllers, models, services) |
| Features Structure | `@ai-init --features` | Skip folder-structure question; assume by-domain (users, payments) |
| Screaming Structure | `@ai-init --screaming` | Skip folder-structure question; assume screaming architecture |

## Configuration

### Auto-Detection Sources

| Source Files | What is Detected |
| :--- | :--- |
| `package.json`, `requirements.txt`, `pyproject.toml`, `pom.xml`, `Cargo.toml`, `Gemfile`, `go.mod`, `composer.json`, `*.csproj`, `mix.exs`, `pubspec.yaml` | Language stack |
| `.eslintrc*`, `.prettierrc*`, `tsconfig.json`, `pytest.ini`, `jest.config.*`, `vitest.config.*`, `.editorconfig`, `Dockerfile`, `Makefile`, `biome.json`, `next.config.*`, `vite.config.*` | Tooling |
| `src/`, `lib/`, `app/`, `tests/`, `components/`, `controllers/`, `models/`, `services/` | Folder structure |

### Generated Files

| File | Contents |
| :--- | :--- |
| `/docs/ai-init/ARCHITECTURE.md` | Stack, data flow, folder structure, restrictions, tooling, Mermaid diagram |
| `/docs/ai-init/CONVENTIONS.md` | Naming, style tools, testing, design patterns, git conventions |
| `/docs/ai-init/DECISIONS.md` | Key decisions with rationale, discarded options, status, date |
| `/docs/ai-init/ERRORS.md` | Known errors: symptom, cause, solution, last seen (starts empty) |

### Validation Checks

| Check | Severity |
| :--- | :--- |
| Folder structure vs documented | ⚠️ Warning |
| New dependencies not in ARCHITECTURE.md | ⚠️ Warning |
| New config files not in CONVENTIONS.md | ℹ️ Info |
| Decisions > 90 days with Active status | ℹ️ Info |
| ERRORS.md missing or empty | ℹ️ Info |
| AGENTS.md missing AI-INIT block | ⚠️ Warning |

> [!NOTE]
> `AGENTS.md` may be gitignored by default. To commit it: `git add -f AGENTS.md`. Generated docs in `/docs/ai-init/` are also gitignored by default — add them to version control explicitly if you want the team to see them.

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-10 via @ai-docs update -->
