# Skill Ecosystem

How the 8 skills relate to each other and the repository structure.

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart TD
    subgraph Meta["Meta Skills"]
        AI_DOCS[ai-docs<br/>Doc generator]
        AI_CONFIG[ai-config<br/>Config validator]
        SKILL_SEARCH[skill-search<br/>Package manager]
    end

    subgraph Workflow["Workflow Skills"]
        AI_GIT[ai-git<br/>Git/GitHub hub]
        AI_ROUTER[ai-router<br/>Task router]
        AUTO_REPORT[auto-report<br/>Report generator]
    end

    subgraph Audit["Audit & Quality"]
        AI_AUDIT[ai-audit<br/>Code auditor]
        AI_ENV[ai-env<br/>Env manager]
    end

    AI_CONFIG -- validates --> AI_DOCS
    AI_CONFIG -- validates --> AI_GIT
    AI_CONFIG -- validates --> AI_ROUTER
    AI_CONFIG -- validates --> AUTO_REPORT
    AI_CONFIG -- validates --> AI_AUDIT
    AI_CONFIG -- validates --> AI_ENV
    AI_CONFIG -- validates --> SKILL_SEARCH

    AI_DOCS -- generates docs for --> AI_GIT
    AI_DOCS -- generates docs for --> AI_ROUTER
    AI_DOCS -- generates docs for --> AUTO_REPORT
    AI_DOCS -- generates docs for --> AI_AUDIT
    AI_DOCS -- generates docs for --> AI_ENV
    AI_DOCS -- generates docs for --> AI_CONFIG
    AI_DOCS -- generates docs for --> SKILL_SEARCH

    SKILL_SEARCH -- installs/updates --> AI_GIT
    SKILL_SEARCH -- installs/updates --> AI_ROUTER
    SKILL_SEARCH -- installs/updates --> AI_AUDIT
    SKILL_SEARCH -- installs/updates --> AI_ENV

    AI_ROUTER -- can delegate to --> AI_AUDIT
    AI_ROUTER -- can delegate to --> AI_GIT
    AI_ROUTER -- can delegate to --> AI_DOCS

    AI_AUDIT -- scans --> AI_GIT
    AI_AUDIT -- scans --> AI_ENV
    AI_AUDIT -- scans --> AI_ROUTER

    AI_ENV -- scans code in --> AI_AUDIT
    AI_ENV -- scans code in --> AI_GIT
    AI_ENV -- scans code in --> AI_ROUTER
```

## Skill Categories

| Category | Skills | Purpose |
| :--- | :--- | :--- |
| **Meta** | `ai-docs`, `ai-config`, `skill-search` | Maintain the repository itself — docs, config validation, package management |
| **Workflow** | `ai-git`, `ai-router`, `auto-report` | Get things done — version control, task routing, report generation |
| **Audit & Quality** | `ai-audit`, `ai-env` | Keep code healthy — quality auditing, environment management |

## Typical Workflows

### New to the repo
```
@ai-config --check → @ai-env --scan → @ai-audit → @ai-docs update
```

### Building a feature
```
@ai-router plan → implement → @ai-git --commit → @ai-git --pr
```

### Generating a report
```
@auto-report → @ai-docs pro <dir> → embed diagrams → export
```

---

**[⬆ Back to Top](#)** | **[📂 Skill Index](/docs/README.md)**

<!-- Last updated: 2026-07-07 via @ai-docs update -->
