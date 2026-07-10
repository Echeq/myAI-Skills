# Agent Index

> Standalone OpenCode agents. Unlike skills (invoked via `@` triggers), agents are installed by copying the `.md` file to `~/.config/opencode/agents/` and they monitor incoming requests to route them to the appropriate pipeline.

[📂 Welcome](/docs/WELCOME.md) • [📂 Skill Index](/docs/README.md) • [📂 Guides](/docs/guides/usage.md)

---

## Agent vs Skill

| Layer | What | Who |
|:------|:-----|:----|
| **Agent** | Conversational, user-facing interface. Talks to you, decides what to do. | `agent/ROUTER.md`, `agent/ORCHESTRATOR.md`, `agent/DELLA.md` |
| **Skill** | Technical engine. Called by agents via `skill("name")`. Does the heavy lifting. | `.agents/skills/<name>/SKILL.md` |

Agents are **conversational** — they explain, decide, and delegate. Skills are **technical** — they contain precise step-by-step execution logic. This separation keeps agents readable and skills maintainable.

---

## Available Agents

| Agent | File | Role | When to Use |
|:------|:-----|:-----|:------------|
| **DELLA** | `agent/DELLA.md` | Strategic planning consultant | Before starting: decides ROUTER vs ORCHESTRATOR, designs workflows |
| **ROUTER** | `agent/ROUTER.md` | Lightweight daily task agent | Default for most work: fast, direct, pipeline-only when needed |
| **ORCHESTRATOR** | `agent/ORCHESTRATOR.md` | Complex multi-step orchestrator | Multi-step with dependencies, cascade risk, parallel execution |

---

## Choosing the Right Agent

| If you need... | Use |
|:---------------|:----|
| A quick edit, a question answered, a single command | **ROUTER** (or just answer directly) |
| A multi-step task that's linear (plan → build → review) | **ROUTER** with `skill("ai-router")` |
| A complex task with dependencies (A must finish before B) | **ORCHESTRATOR** with `skill("ai-orchestrator")` |
| Parallel work or cascade failure handling | **ORCHESTRATOR** |
| A strategic plan before any coding starts | **DELLA** |

---

## Installation

All agents follow the same pattern:

```bash
# Windows:
copy agent\<AGENT>.md %USERPROFILE%\.config\opencode\agents\<AGENT>.md

# macOS / Linux:
cp agent/<AGENT>.md ~/.config/opencode/agents/<AGENT>.md
```

After installation, each agent may need its corresponding skill configured:

| Agent | Configuration command | Skill |
|:------|:---------------------|:------|
| ROUTER | `@ai-router --init` | `skill("ai-router")` — 3-mode pipeline |
| ORCHESTRATOR | `@ai-orchestrator --init` | `skill("ai-orchestrator")` — DAG engine |
| DELLA | None (no sub-agents needed) | — |

---

## Relationship with Skills

```
User → DELLA (plan) → decides: ROUTER or ORCHESTRATOR?
  ├── ROUTER Agent (conversational, fast)
  │     └── Calls skill("ai-router") for pipeline
  │     └── Or calls individual skills: skill("ai-audit"), skill("ai-docs")
  │
  └── ORCHESTRATOR Agent (strategic, powerful)
        └── Calls skill("ai-orchestrator") for DAG engine
        └── Auto-routes to skills via capability registry
```

Each agent doc below details its specific workflow, installation, and usage.

---

| Agent | Read more |
|:------|:----------|
| DELLA | [📄 DELLA Agent](DELLA.md) |
| ROUTER | [📄 ROUTER Agent](ROUTER.md) |
| ORCHESTRATOR | [📄 ORCHESTRATOR Agent](ORCHESTRATOR.md) |

---

> [!NOTE]
> If you're new here, start with ROUTER — it's simpler to set up and covers most daily tasks.

[⬆ Back to Top](#) | [📂 Skill Index](/docs/README.md) | [📂 Welcome](/docs/WELCOME.md)
