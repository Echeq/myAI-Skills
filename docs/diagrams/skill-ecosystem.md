# Skill Ecosystem

> Relationship diagram showing how skills interact with each other.

[📂 Skill Index](/docs/README.md) • [📂 Diagrams](README.md)

---

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true }, 'themeCSS': '.mermaid svg { max-width: 100% !important; height: auto !important; }' } }%%
flowchart TB
    subgraph Core["Core Infrastructure"]
        R[ai-router]
        O[ai-orchestrator]
    end
    subgraph Meta["Repository Maintenance"]
        D[ai-docs]
        C[ai-config]
        S[skill-search]
        I[ai-init]
    end
    subgraph Workflow["Daily Work"]
        G[ai-git]
        A[auto-report]
    end
    subgraph Security["Audit & Security"]
        AU[ai-audit]
        E[ai-env]
    end
    R --> D
    R --> G
    R --> AU
    R --> E
    O --> D
    O --> G
    O --> AU
    O --> E
    S -->|installs| D
    S -->|installs| G
    S -->|installs| AU
    C -->|validates| D
    C -->|validates| G
    C -->|validates| AU
```

---

> [!TIP]
> This diagram shows the cross-skill relationships. Skills in the Core and Meta groups maintain the repository; Workflow and Security skills are used in daily operations.

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md)
