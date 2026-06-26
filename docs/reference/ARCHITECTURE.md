# Documentation Architecture

> Professional deep-dive into the docs system of myAI-Skills.

## ADR-001: Documentation as a Self-Healing System

**Status:** Adopted 2026-06-23

**Context:** The repo contains 6 OpenCode skills (plain `.md` files) with zero runtime code. Traditional doc generation from source (TSDocs, JSDoc) is inapplicable. Documentation must be authored manually but remain verifiable.

**Decision:** Implement a dual-layer documentation model:

| Layer | Location | Ownership | Mutation Policy |
|-------|----------|-----------|----------------|
| Skill definitions | `.agents/skills/<name>/SKILL.md` | Skill author | Manual |
| Global docs | `docs/` | `@ai-docs` agent | Semi-automated audit |

Cross-references flow one way: skill definitions are the source of truth; `docs/` summarizes and indexes but never duplicates.

**Consequences:**
- Positive: No doc generation pipeline to maintain
- Positive: Audit mode (`@ai-docs audit`) enforces compliance without a build step
- Negative: No automated guard against docs/skill drift; relies entirely on triggered audits

---

## Complexity Analysis

### ai-docs State Machine

The `ai-docs` skill implements a 4-mode deterministic state machine:

```
                  ┌──────────┐
                  │ STANDARD │  (full scan + generate)
                  └────┬─────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
        ┌──────────┐     ┌──────────┐
        │ PROFESS. │     │  UPDATE  │  (incremental, diff-based)
        └──────────┘     └────┬─────┘
                              │
                       ┌──────┴──────┐
                       ▼             ▼
                  ┌─────────┐  ┌──────────┐
                  │  AUDIT  │  │  EXIT    │
                  └─────────┘  └──────────┘
```

**Time Complexity (per mode):**
- STANDARD: O(n) where n = total non-git files
- PROFESSIONAL: O(k) where k = targeted module depth
- UPDATE: O(m) where m = files with stale timestamps
- AUDIT: O(n) scan + O(p) report generation (p = severity categories)

**Space Complexity:** O(d) where d = document count. No intermediate representation is materialized.

---

## Dependency Graph

```
┌──────────────────────────────────────────────────┐
│                   docs/                           │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┐  │
│  │README.md │  │creating-     │  │conventions │  │
│  │ (index)  │  │skills.md     │  │ .md        │  │
│  └────┬─────┘  └──────┬───────┘  └──────┬─────┘  │
│       │               │                 │         │
│       └───────┬───────┴─────────┬───────┘         │
│               ▼                 ▼                  │
│        ┌────────────┐   ┌──────────────┐          │
│        │ usage.md   │   │ARCHITECTURE  │          │
│        │            │   │ .md (this)   │          │
│        └────────────┘   └──────────────┘          │
└──────────────────────────────────────────────────┘
         ▲                              ▲
         │                              │
         │ references                   │ audits
         │                              │
┌────────┴──────────────────────────────┴──────────┐
│              .agents/skills/<name>/                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐ │
│  │ ai-docs  │ │ ai-git   │ │ ai-audit │ │...   │ │
│  │ SKILL.md │ │ SKILL.md │ │ SKILL.md │ │      │ │
│  │          │ │ +commit  │ │          │ │      │ │
│  │          │ │ +release │ │          │ │      │ │
│  │          │ │ +branch  │ │          │ │      │ │
│  │          │ │ +pr      │ │          │ │      │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────┘ │
└───────────────────────────────────────────────────┘
```

**External dependencies:** None. The entire system is self-contained within the repo.

---

## Stress / Edge Cases

### Doc-Skill Drift
A skill's `SKILL.md` is updated but `docs/` is not. Mitigation: `@ai-docs audit` flags uncovered code (Critical). `@ai-docs update` reconciles timestamps.

### Zero-Code Skills
All 6 current skills are prose-only `.md` files. The `src/`, `tests/`, `package.json` structure in `docs/README.md` is aspirational — no CI enforces it. Risk: new contributors may expect executable packages.

### Cross-Link Rot
Hardcoded relative paths (`../.agents/skills/`). If the repo is consumed as a submodule, paths break. Current resolution: document path assumption in `docs/ARCHITECTURE.md`.

### Audit False Positives
The audit checklist requires `/docs/api/`, `/docs/setup/`, etc. These do not exist and may never exist for pure-skill repos. Resolution: the global standard was relaxed from mandatory folder list to "organize as the project grows." Audit critical #1 should be interpreted with context.
