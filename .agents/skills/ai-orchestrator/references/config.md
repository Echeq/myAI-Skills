# Orchestrator Configuration

## Dynamic Classification

The classifier uses a structured prompt instead of keyword heuristics.
It outputs `{mode, confidence, capabilities_needed, suggested_skills}`.

Fallback rules (when the prompt classifier is unavailable or fails):

```yaml
fallback_rules:
  - if "error" in query or "fail" in query or "bug" in query: mode = debug
  - if any(verb in query.lower() for verb in ["build", "create", "implement", "design",
       "refactor", "generate", "develop", "add feature", "system", "architecture"]): mode = plan
  - if len(query) > 150: mode = plan
  - else: mode = quick
```

## Execution Limits

```yaml
timeout: 60
max_iterations: 3
fix_loop:
  attempt_1_model: flash     # Same as original executor
  attempt_2_model: pro       # Escalate — flash likely reproduces same error
  attempt_3_model: pro       # Last attempt with full reasoning
```

## Allowed Imports (executor)

```yaml
allowed_imports:
  - json
  - math
  - datetime
  - re
  - collections
  - itertools
  - typing
```

## Virtual Environment

```yaml
venv_dir: ~/.opencode/venvs/
```

## Capability Taxonomy

Controlled vocabulary for skill/agent capability tags:

```yaml
domains:
  - code-generation      # writing new code
  - code-review          # reviewing existing code
  - debugging            # fixing bugs/errors
  - refactoring          # restructuring existing code
  - testing              # writing/executing tests
  - documentation        # generating docs
  - configuration        # managing config files
  - deployment           # CI/CD, releases
  - data-analysis        # analyzing data, reports
  - research             # investigating, answering questions
  - security             # audits, vulnerability scanning
  - performance          # profiling, optimization
  - architecture         # system design, planning

environments:
  - python
  - javascript
  - typescript
  - html-css
  - shell
  - docker
  - git
  - sql
  - markdown
  - any
```

## DAG Engine Configuration (Phase 1)

```yaml
dag:
  timeout_seconds: 60            # Uniform per-task timeout (no priorities yet)
  max_attempts: 1                # Phase 1: single attempt, no retry logic
  state_file: ".agents/memory/ai-orchestrator/assets/state/task_states.json"
  plan_input: ".agents/memory/ai-orchestrator/assets/plan/plan_input.json"
  checkpoint_timeout: 300        # Default if PAUSED state is triggered
```

## Mode Summary

| Mode   | Trigger                                      | Pipeline                          |
|--------|----------------------------------------------|-----------------------------------|
| debug  | "error", "fail", "bug" in query              | executor → review(flash) → fix → log |
| plan   | dynamic classification output                | classifier → registry → planner → DAG engine → executor/skill → review(adaptive) → fix → log |
| quick  | default or --quick flag                      | executor(flash) → review(flash, always) → log |
