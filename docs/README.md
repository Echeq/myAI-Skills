# Skill Index

Welcome to the myAI-Skills documentation — 8 OpenCode skills for AI-assisted development. Each skill is a self-contained agent that you invoke via `@trigger` commands.

## Ecosystem Overview

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart LR
    subgraph Meta["Maintain the Repo"]
        A[ai-docs] --> D[Generates docs]
        B[ai-config] --> E[Validates config]
        C[skill-search] --> F[Installs skills]
    end
    subgraph Workflow["Get Things Done"]
        G[ai-git] --> H[Git/GitHub ops]
        I[ai-router] --> J[Routes complex tasks]
        K[auto-report] --> L[Generates reports]
    end
    subgraph Quality["Audit & Secure"]
        M[ai-audit] --> N[Code quality scans]
        O[ai-env] --> P[Env var management]
    end
```

> See the full [Skill Ecosystem Diagram](diagrams/skill-ecosystem.md) with cross-skill relationships.

## Skills by Category

### 📋 Meta — Maintain the Repository

| Skill | Trigger | What it does |
| :--- | :--- | :--- |
| [ai-docs](skills/ai-docs.md) | `@ai-docs` | Generates, updates, and audits Markdown documentation. 5 modes: generate, pro deep-dive, incremental update, compliance audit, interaction logging. |
| [ai-config](skills/ai-config.md) | `@ai-config` | Validates skill frontmatter, opencode.jsonc structure, and .gitignore coverage. Catches broken triggers and missing paths. |
| [skill-search](skills/skill-search.md) | `@skill-search` | Browse, install, and update skills from the Echeq/myAI-Skills GitHub repository. Acts as a package manager for OpenCode skills. |

### ⚡ Workflow — Get Things Done

| Skill | Trigger | What it does |
| :--- | :--- | :--- |
| [ai-git](skills/ai-git.md) | `@ai-git` | Git/GitHub hub with 4 sub-modules: commit, release, branch, PR. Each loads independently to save tokens. |
| [ai-router](skills/ai-router.md) | `@ai-router` | Routes complex tasks through a planner → executor → reviewer pipeline with severity-based fix retry (minor→flash, major→pro). |
| [auto-report](skills/auto-report.md) | `@auto-report` | Interactive 8-step wizard for generating reports in 5 formats. Adapts sections to subject. |

### 🛡️ Audit & Quality — Keep Code Healthy

| Skill | Trigger | What it does |
| :--- | :--- | :--- |
| [ai-audit](skills/ai-audit.md) | `@ai-audit` | Pattern-based code quality auditor across 5 weighted categories (Security 35%, Performance 20%, Maintainability 20%, Best Practices 15%, Documentation 10%). Grades A–D with regression tracking. |
| [ai-env](skills/ai-env.md) | `@ai-env` | Full environment lifecycle: scan for env vars, generate .env.example, update .gitignore, validate against .env, audit for hardcoded secrets. |

## Choosing the Right Skill

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart TD
    Q{"What do you need?"}
    Q -->|"Validate repo config"| A[ai-config]
    Q -->|"Scan env vars / secrets"| B[ai-env]
    Q -->|"Audit code quality"| C[ai-audit]
    Q -->|"Generate documentation"| D[ai-docs]
    Q -->|"Install new skills"| E[skill-search]
    Q -->|"Git commit / PR / release"| F[ai-git]
    Q -->|"Complex multi-step task"| G[ai-router]
    Q -->|"Generate a report"| H[auto-report]
```

## Quick Start — Recommended Path

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart LR
    START[New to the repo?] --> CFG[1. @ai-config --check]
    CFG --> ENV[2. @ai-env --scan]
    ENV --> AUDIT[3. @ai-audit]
    AUDIT --> DOCS[4. @ai-docs update]
    DOCS --> DONE[Ready! 🚀]
```

## Guides & Reference

| Guide | Description |
| :--- | :--- |
| [Usage Guide](guides/usage.md) | How to use and chain skills |
| [Creating Skills](guides/creating-skills.md) | How to create new skills with diagrams and validation checklist |
| [Conventions](reference/conventions.md) | Naming, frontmatter, diagram standards |
| [Architecture](reference/ARCHITECTURE.md) | ADRs, complexity analysis, dependency graph |

---

**[⬆ Back to Top](#)** | **[📂 Root README](/README.md)**

<!-- Last updated: 2026-07-07 via @ai-docs update -->
