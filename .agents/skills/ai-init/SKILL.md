---
name: ai-init
description: >-
  Bootstraps foundational project documentation in under 5 minutes. Auto-detects
  stack and tooling, asks minimal questions, generates 4 docs in /docs/ai-init/,
  and updates AGENTS.md. Includes validate sub-command for drift detection.
allowed-tools: Read, Write, Bash, Glob, Grep
triggers:
  - "@ai-init"
  - "@ai-init validate"
  - "@ai-init --types"
  - "@ai-init --features"
  - "@ai-init --screaming"
---

# AI Init

Bootstraps foundational project documentation in under 5 minutes. Auto-detects your stack and tooling, asks the few questions code can't answer, then generates 4 structured docs in `/docs/ai-init/` and updates `AGENTS.md`.

## Commands

| Command | Action |
|---|---|
| `@ai-init` | Full wizard: auto-detect → questions → generate docs → update AGENTS.md |
| `@ai-init validate` | Compare documented info against actual code; report drift |
| `@ai-init --types` | Skip folder-structure question; assume `--types` (controllers/models/services) |
| `@ai-init --features` | Skip folder-structure question; assume `--features` (users/payments/) |
| `@ai-init --screaming` | Skip folder-structure question; assume screaming architecture |

## Flow Overview

```
@ai-init → Phase 1 (auto-detect) → Phase 2 (questions) → Phase 3 (generate) → Phase 4 (AGENTS.md)
```

If the user provides a flag (`--types`, `--features`, `--screaming`), the corresponding folder-structure question is skipped.

## Phase 1: Auto-Detection

Scan the project root and produce a summary. Ask no questions in this phase.

### 1.1 Stack Detection

Scan for these files and infer the stack:

| File(s) | Inferred stack |
|---|---|
| `package.json` | Node.js / JavaScript / TypeScript |
| `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg` | Python |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | Java (Maven/Gradle) |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |
| `go.mod` | Go |
| `composer.json` | PHP |
| `CMakeLists.txt` | C/C++ (CMake) |
| `*.csproj`, `*.sln` | .NET / C# |
| `mix.exs` | Elixir |
| `pubspec.yaml` | Dart / Flutter |

If multiple manifests exist (e.g., `package.json` + `requirements.txt`), list all stacks separated by `+`.

If none found, note **"No manifest detected"** and skip to Phase 2 as a greenfield project.

### 1.2 Tooling Detection

Scan the project root for these files and infer tooling:

| File pattern | Inferred tooling |
|---|---|
| `.eslintrc.*`, `eslint.config.*` | ESLint |
| `.prettierrc.*`, `prettier.config.*` | Prettier |
| `tsconfig.json`, `tsconfig.*.json` | TypeScript |
| `pytest.ini`, `tox.ini`, `conftest.py` | pytest |
| `jest.config.*`, `jest.setup.*` | Jest |
| `vitest.config.*` | Vitest |
| `.editorconfig` | EditorConfig |
| `Dockerfile`, `docker-compose*.yml` | Docker |
| `.github/workflows/` | GitHub Actions |
| `Makefile` | Make |
| `biome.json` | Biome |
| `.oxlintrc.*` | oxlint |
| `tailwind.config.*` | Tailwind CSS |
| `next.config.*` | Next.js |
| `vite.config.*` | Vite |

### 1.3 Structure Detection

Look for these top-level directories and infer structure:

| Directory | Inference |
|---|---|
| `src/` | Source code root (common in Java, C#, TypeScript) |
| `lib/` | Library code (common in Ruby, older JS) |
| `app/` | Application code (common in Next.js, Rails, Laravel) |
| `tests/`, `test/`, `__tests__/`, `spec/` | Test directory present |
| `components/`, `pages/`, `layouts/` | Frontend component structure |
| `controllers/`, `models/`, `services/`, `routes/` | Layered backend (or MVC) |
| `api/`, `db/`, `utils/`, `middleware/` | Structured backend |
| `docs/` | Documentation directory |

If `src/` contains subdirectories, peek inside for further inference (e.g., `src/main/java` → Java Maven/Gradle layout).

### 1.4 Summary Format

After scanning, print this summary (replace bracketed values on one line each):

```
📦 AI Init — Auto-detection Results

  Stack:       [detected stacks, comma-separated]
  Tooling:     [detected tooling, comma-separated]
  Structure:   [detected structure notes, e.g. "src/ + tests/ (layered backend)"]
  Language:    [primary language, e.g. TypeScript, Python]

Is this correct? (y/n/edit)
```

If the user types **`y`** or **`yes`** → proceed to Phase 2.
If the user types **`n`** or **`no`** → ask them to type the corrected values in free text, then re-derive and re-confirm.
If the user types free text → treat it as corrections. Parse the text, update the inferred values, re-print the summary, and ask again.

## Phase 2: Minimum Questions

Cap: 5 questions total. Skip any question whose answer is already known from auto-detection or provided flags. Confirm auto-detected answers rather than re-asking.

### 2.1 Folder Structure (skip if flag provided)

If the user did NOT provide `--types`, `--features`, or `--screaming`:

Show these three visual examples and ask:

```
Which folder structure does your project use?

  1) --types (by layer)
     src/
     ├── controllers/
     ├── models/
     ├── services/
     └── routes/

  2) --features (by domain)
     src/
     ├── users/
     │   ├── controller.ts
     │   ├── model.ts
     │   └── service.ts
     └── payments/
         ├── controller.ts
         ├── model.ts
         └── service.ts

  3) --screaming (screaming architecture)
     src/
     ├── User/
     │   ├── UserController.ts
     │   ├── UserModel.ts
     │   └── UserService.ts
     └── Payment/
         ├── PaymentController.ts
         ├── PaymentModel.ts
         └── PaymentService.ts

  Enter 1, 2, or 3 (or describe your own):
```

If the detected structure already strongly implies one pattern (e.g., `controllers/` and `models/` found), mention it: "Detected structure suggests option 1 (by layer). Confirm or choose another."

### 2.2 Key Decisions (max 3)

Ask these open-ended questions one at a time:

```
1/3 — What is the main data flow of this project?
  (e.g. "REST API → PostgreSQL", "CLI tool → file system", "React SPA → GraphQL → microservices")
```

Wait for answer. Then:

```
2/3 — What design patterns or architectural principles are important here?
  (e.g. "Clean Architecture", "MVC", "Hexagonal / ports & adapters", "event-driven", "none in particular")
```

Wait for answer. Then:

```
3/3 — Are there any important restrictions or constraints?
  (e.g. "must support Node 18+", "no external API calls", "strict 100ms P95 latency budget", "none")
```

If the user answers "none" or "skip" to any question, note that and move on.

### 2.3 Conventions (only if not auto-detected)

Check what auto-detection found. Only ask for items NOT detected:

| If this was NOT auto-detected... | Ask this |
|---|---|
| No linter found | "What naming convention do you follow? (e.g. camelCase, snake_case, PascalCase)" |
| No test framework found | "What testing framework do you use? (e.g. Jest, pytest, RSpec, none yet)" |
| No coverage tool found | "Do you have a code coverage target? (e.g. 80%, not yet)" |

Skip any question already answered by auto-detection. Confirm with the user: "Detected ESLint + Prettier for formatting. OK?"

## Phase 3: File Generation

Create `/docs/ai-init/` directory (using `New-Item -ItemType Directory -Path "docs/ai-init" -Force` on Windows, `mkdir -p docs/ai-init` on macOS/Linux). Then write these 4 files.

### 3.1 ARCHITECTURE.md

```markdown
# Architecture

> Generated by `@ai-init` on {date}.

## Stack
- **Language:** {language}
- **Runtime / Framework:** {framework}
- **Package Manager:** {package_manager}
- **Primary Database:** {database or "none"}

## Data Flow
{data_flow_description from Phase 2.2 question 1}

## Folder Structure
{description of chosen structure with a simple tree diagram}

## Architecture Diagram
```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart LR
    {user_or_external} -->|{protocol}| {entrypoint}
    {entrypoint} --> {business_logic}
    {business_logic} --> {data_layer}
```
```

Fill in the Mermaid diagram from the data flow description. Keep it simple — 3 to 5 nodes.

## Key Restrictions
{restrictions from Phase 2.2 question 3, or "None documented."}

## Tooling
| Tool | Purpose |
|---|---|
{auto-detected tooling rows}

---

**[⬆ Back to Top](#)** | **[📂 AI Init Index](/docs/ai-init/)**
```

### 3.2 CONVENTIONS.md

```markdown
# Conventions

> Generated by `@ai-init` on {date}.

## Naming
- **Files:** {file naming convention, e.g. kebab-case.ts, snake_case.py}
- **Variables / Functions:** {naming, e.g. camelCase, snake_case}
- **Classes / Types:** {naming, e.g. PascalCase}
- **Constants:** {naming, e.g. UPPER_SNAKE_CASE}

## Style
| Aspect | Tool / Rule |
|---|---|
{auto-detected formatter/linter rows. If none: "No formatter configured yet."}

## Testing
- **Framework:** {testing framework or "None configured"}
- **Coverage Target:** {coverage or "Not set"}
- **Test Location:** {test directory or "No test directory found"}
- **Naming Convention:** {e.g. "*.test.ts files co-located with source"}

## Design Patterns
{patterns from Phase 2.2 question 2, or "None specified."}

## Git Conventions
- **Branch naming:** {infer or ask}
- **Commit style:** {infer or "Conventional Commits"}
- **PR workflow:** {infer or "Standard (feature branch → main)"}

---

**[⬆ Back to Top](#)** | **[📂 AI Init Index](/docs/ai-init/)**
```

### 3.3 DECISIONS.md

```markdown
# Key Decisions

> Generated by `@ai-init` on {date}.
>
> Update this file when making important architectural or design decisions.
> Run `@ai-init validate` to check for stale decisions.

| # | Decision | Why | Discarded Options | Status | Date |
|---|----------|-----|-------------------|--------|------|
| 1 | {stack choice} | {why this stack} | {alternatives considered} | Active | {date} |
| 2 | {folder structure choice} | {why this structure} | {other structures considered} | Active | {date} |
| 3 | {data flow choice} | {why this flow} | {alternatives} | Active | {date} |
```

Populate rows from Phase 2 answers and auto-detection. For the "why" column, use the user's answers directly. For "Discarded Options," infer common alternatives (e.g., if using TypeScript, discarded options might be "JavaScript, Flow").

### 3.4 ERRORS.md

```markdown
# Known Errors

> Generated by `@ai-init` on {date}.
>
> Add entries as you encounter and resolve errors.
> Run `@ai-init validate` to flag missing entries.

| # | Symptom | Probable Cause | Solution | Last Seen |
|---|---------|---------------|----------|-----------|
| — | _No errors documented yet._ | — | — | — |
```

Start empty. This file grows over time as the user encounters and documents errors.

## Phase 4: AGENTS.md

### Detection & Merge Strategy

Check if `AGENTS.md` exists in the project root:

**If AGENTS.md does NOT exist:**
Create it with the project name (from `package.json` name field or top-level directory name):

```markdown
# {project_name}

<!-- AI-INIT -->
## AI Context
Project documentation is located at `/docs/ai-init/`:

| File | Contents |
|---|---|
| [ARCHITECTURE.md](docs/ai-init/ARCHITECTURE.md) | Stack, structure, data flow, restrictions |
| [CONVENTIONS.md](docs/ai-init/CONVENTIONS.md) | Style, naming, testing, design patterns |
| [DECISIONS.md](docs/ai-init/DECISIONS.md) | Key decisions and rationale |
| [ERRORS.md](docs/ai-init/ERRORS.md) | Known errors and solutions |

**Suggested workflow:**
1. Read `ARCHITECTURE.md` before starting new work.
2. Update `DECISIONS.md` when making an important decision.
3. Run `@ai-init validate` to check documentation consistency.

> Generated by `@ai-init` on {date}. Re-run `@ai-init` to update.
<!-- /AI-INIT -->
```

**If AGENTS.md exists:**

1. Search for the `<!-- AI-INIT -->...<!-- /AI-INIT -->` marker block.
2. If found → replace ONLY the content between those markers with the refreshed block (above).
3. If NOT found → append the block at the end of the file, preceded by a `---` separator.

**Important**: `AGENTS.md` may be gitignored (it is in this repo). If so, remind the user: "AGENTS.md is gitignored by default. To commit it: `git add -f AGENTS.md`."

## Validation: `@ai-init validate`

Compares documented info in `/docs/ai-init/` against actual project code. Produces a status report.

### Checks

Run these checks in order:

| # | Check | What it does | Severity if failing |
|---|---|---|---|
| 1 | Folder structure | Compare ARCHITECTURE.md structure description against actual top-level directories | ⚠️ Warning |
| 2 | Dependency drift | Scan manifests for new packages not mentioned in ARCHITECTURE.md stack section | ⚠️ Warning |
| 3 | Config drift | Detect new linter/formatter config files not in CONVENTIONS.md | ℹ️ Info |
| 4 | Decisions staleness | Flag any DECISIONS.md entry with status "Active" and date > 90 days ago | ℹ️ Info |
| 5 | ERRORS.md completeness | Note if ERRORS.md is still empty | ℹ️ Info |
| 6 | AGENTS.md presence | Check if AGENTS.md exists and has `<!-- AI-INIT -->` block | ⚠️ Warning |

### Output Format

```
📋 AI Init Validation Report — {date}

  1. Folder Structure  ✅ Matches documented structure
  2. Dependency Drift   ⚠️ 3 new packages since last check:
     - lodash (not in ARCHITECTURE.md)
     - zod (not in ARCHITECTURE.md)
     - vitest (not in ARCHITECTURE.md)
  3. Config Drift       ✅ No new config files detected
  4. Decisions          ℹ️ Decision #1 (JavaScript vs TypeScript) is 95 days old — consider reviewing
  5. Error Tracking     ℹ️ ERRORS.md is empty — document errors as you resolve them
  6. AGENTS.md          ✅ Found with AI-INIT block

  Summary: 2 ⚠️ warnings, 2 ℹ️ info
  Run @ai-init to update documentation.
```

Use these symbols: ✅ pass, ⚠️ warning (should fix), ❌ critical (must fix), ℹ️ info (advisory).

### Optional: `--fix` sub-flag

After the validation report, if issues were found, ask: "Would you like me to fix these? (y/n)?"

If yes → re-run the wizard with existing answers as defaults, updating only the drifted sections. This is equivalent to running `@ai-init` again but with the previous answers pre-filled.

## Edge Cases

### Greenfield Project
No files to scan in Phase 1 → print "No manifest detected — treating as greenfield project." Proceed directly to Phase 2. Mark ARCHITECTURE.md stack as "Not yet determined."

### Conflicting Flags
If user provides multiple structure flags (e.g., `@ai-init --types --features`), the last flag wins. Warn: "Multiple structure flags provided; using --features."

### Existing `/docs/ai-init/`
If the output directory already exists, warn and ask:

```
📁 /docs/ai-init/ already exists. Options:
  1) Overwrite all files
  2) Merge (update only changed sections, preserve user edits)
  3) Abort

Enter 1, 2, or 3:
```

For option 2 (merge), read each existing file and only replace sections that the wizard would generate new content for. Preserve user-added content outside the generated sections.

### Session Resume
If the user cancels mid-wizard or the session is interrupted, save partial answers to `.agents/skills/ai-init/assets/session.json` (gitignored by path). On next `@ai-init` invocation, check for this file and offer to resume:

```
💾 Found saved session from {date}. Resume? (y/n)
```

## Platform Notes

- **Windows (PowerShell):** Use `New-Item -ItemType Directory -Path "docs/ai-init" -Force` for directory creation. Chain commands with `; if ($?) { ... }`.
- **macOS / Linux:** Use `mkdir -p docs/ai-init`. Chain commands with `&&`.

The skill should detect the platform and use appropriate commands.

## Output Summary

After generating everything, print a final summary:

```
✅ AI Init complete — {project_name}

  Created:
    📄 docs/ai-init/ARCHITECTURE.md   — Stack, structure, data flow
    📄 docs/ai-init/CONVENTIONS.md    — Style, naming, testing, patterns
    📄 docs/ai-init/DECISIONS.md      — Key decisions and rationale
    📄 docs/ai-init/ERRORS.md         — Error tracking (start here when you hit issues)

  Updated:
    📄 AGENTS.md                      — Added AI Context block

  Quick start:
    1. Read docs/ai-init/ARCHITECTURE.md before coding
    2. Run @ai-init validate to check for drift
    3. Run @ai-init again to update docs when things change
```
