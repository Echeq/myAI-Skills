# Initialization Procedure

Run this when the user invokes `@ai-router --init`.

## Step 1: Announce

> "Setting up ai-router. I'll ask which models to use for each role, then write `opencode.json`."

## Step 2: Ask for models

Use the `question` tool for each role. Offer presets + "Custom" as last option.

### Manager (planner)

Strategic planning, breaking down tasks. Recommended: DeepSeek V4 Pro.

```
question:
  header: "Manager model (planner)"
  question: "Which model for the planner?"
  options:
    - label: "DeepSeek V4 Pro (Recommended)"
      description: "Strong reasoning"
    - label: "GPT 5.1 Codex"
      description: "OpenCode Zen"
    - label: "Claude Sonnet 4"
      description: "Balanced"
    - label: "Custom"
      description: "Type any provider/model ID"
```

### Worker (executor)

Code execution, applying fixes. Recommended: DeepSeek V4 Flash.

```
question:
  header: "Worker model (executor)"
  question: "Which model for the executor?"
  options:
    - label: "DeepSeek V4 Flash (Recommended)"
      description: "Fast code generation"
    - label: "GPT 5.1 Codex"
      description: "OpenCode Zen"
    - label: "Claude Haiku 4"
      description: "Lightweight"
    - label: "Custom"
      description: "Type any provider/model ID"
```

### Supervisor (reviewer)

Code/plan review. Recommended: DeepSeek V4 Pro.

```
question:
  header: "Supervisor model (reviewer)"
  question: "Which model for the reviewer?"
  options:
    - label: "DeepSeek V4 Pro (Recommended)"
      description: "Thorough review"
    - label: "GPT 5.1 Codex"
      description: "OpenCode Zen"
    - label: "Claude Sonnet 4"
      description: "Balanced"
    - label: "Custom"
      description: "Type any provider/model ID"
```

## Step 3: Resolve custom models

If any answer was "Custom", ask for the exact model ID:

```
question:
  header: "Custom model ID"
  question: "Enter provider/model ID (e.g. anthropic/claude-sonnet-4-20250514, opencode/deepseek-v4-pro):"
```

## Step 4: Generate opencode.json

Map labels to model IDs:

| Label | Model ID |
|-------|----------|
| DeepSeek V4 Pro | opencode-go/deepseek-v4-pro |
| DeepSeek V4 Flash | opencode-go/deepseek-v4-flash |
| GPT 5.1 Codex | opencode-go/gpt-5.1-codex |
| Claude Sonnet 4 | anthropic/claude-sonnet-4-20250514 |
| Claude Haiku 4 | anthropic/claude-haiku-4-20250514 |
| Custom | user-provided value |

Use `write` to create `opencode.json` at the project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": [".agents/skills"]
  },
  "agent": {
    "ai-router-planner": {
      "description": "Planner sub-agent for ai-router",
      "mode": "subagent",
      "model": "<chosen manager model>",
      "prompt": "{file:.agents/skills/ai-router/references/manager.md}",
      "permission": {
        "read": "allow",
        "write": "allow",
        "edit": "allow",
        "grep": "allow",
        "glob": "allow",
        "bash": "allow",
        "task": "allow",
        "external_directory": "deny"
      }
    },
    "ai-router-executor": {
      "description": "Executor sub-agent for ai-router",
      "mode": "subagent",
      "model": "<chosen worker model>",
      "prompt": "{file:.agents/skills/ai-router/references/worker.md}",
      "permission": {
        "read": "allow",
        "write": "allow",
        "edit": "allow",
        "grep": "allow",
        "glob": "allow",
        "bash": "allow",
        "task": "allow",
        "external_directory": "deny"
      }
    },
    "ai-router-reviewer": {
      "description": "Full reviewer (pro) for plan mode — checks correctness, security, architecture",
      "mode": "subagent",
      "model": "<chosen supervisor model>",
      "prompt": "{file:.agents/skills/ai-router/references/supervisor.md}",
      "permission": {
        "read": "allow",
        "write": "allow",
        "edit": "deny",
        "grep": "allow",
        "glob": "allow",
        "bash": "deny",
        "task": "allow",
        "external_directory": "deny"
      }
    },
    "ai-router-reviewer-flash": {
      "description": "Lightweight reviewer (flash) for quick/debug mode — security + basic correctness only",
      "mode": "subagent",
      "model": "<chosen worker model>",
      "prompt": "{file:.agents/skills/ai-router/references/supervisor-lite.md}",
      "permission": {
        "read": "allow",
        "write": "allow",
        "edit": "deny",
        "grep": "allow",
        "glob": "allow",
        "bash": "deny",
        "task": "allow",
        "external_directory": "deny"
      }
    }
  }
}
```

Replace `<chosen manager model>`, `<chosen worker model>`, `<chosen supervisor model>` with the model IDs from Step 2/3.

**Important**: If `opencode.json` already exists with custom config (e.g., user's own agents, custom providers), warn before overwriting. Ask the user to confirm or suggest they back it up first.

## Step 5: Confirm

> "ai-router is ready. Use `@ai-router` followed by your request to start routing."
