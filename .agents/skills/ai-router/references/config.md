# Router Configuration

## Auto-Classification Rules

```yaml
auto_rules:
  - if "error" in query or "fail" in query or "bug" in query: mode = debug
  - if any(verb in query.lower() for verb in ["build", "create", "implement", "design",
       "refactor", "generate", "develop", "add feature", "system", "architecture"]): mode = plan
  - if len(query) > 150: mode = plan  # fallback for very long requests
  - else: mode = quick
```

## Execution Limits

```yaml
timeout: 60
max_iterations: 3  # After the first fix pass, remaining iterations always use pro executor
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

## Mode Summary

| Mode   | Trigger                                      | Pipeline                          |
|--------|----------------------------------------------|-----------------------------------|
| debug  | "error", "fail", "bug" in query              | executor → review(flash) → fix → log |
| plan   | action verbs (build/create/implement...), or length > 150 | planner(pro) → executor → review(pro) → [minor→flash fix \| major→pro fix] → log |
| quick  | default                                       | executor(flash) → review(flash or skip) → log |
