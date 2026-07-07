# Initialization Procedure

Run this when the user invokes `@ai-orchestrator --init`.

## Step 1: Check existing config

Check if `opencode.json` exists. If yes, warn the user:
> "⚠️ `opencode.json` already exists. I recommend backing it up first. Type `continue` to overwrite or `cancel` to abort."

If the user cancels, stop and do nothing.

## Step 2: Announce

> "Setting up ai-orchestrator. I'll ask 3 quick questions (just type the number), then write `opencode.json`."

## Step 3: Ask for models

Ask one question at a time. Present each as a clean numbered list and wait for the user to reply with the number or name. Do NOT use bash/echo — write the question directly in your response.

### 3.1 Manager (planner)

Strategic planning, breaking down tasks. Recommended: DeepSeek V4 Pro.

Present as:
```
**Planner model?** (estratégico, descompone tareas)

1) DeepSeek V4 Pro  (Recomendado) — Razonamiento fuerte
2) GPT 5.1 Codex              — OpenCode Zen
3) Claude Sonnet 4            — Balanceado
4) Custom                     — Escribe tu propio model ID

Responde con el número o nombre:
```

Wait for user input. If they type `4` or `Custom`, follow up for the model ID.

### 3.2 Worker (executor)

Code execution, applying fixes. Recommended: DeepSeek V4 Flash.

Present as:
```
**Executor model?** (ejecuta código, aplica cambios)

1) DeepSeek V4 Flash  (Recomendado) — Generación rápida
2) GPT 5.1 Codex               — OpenCode Zen
3) Claude Haiku 4              — Ligero
4) Custom                      — Escribe tu propio model ID

Responde con el número o nombre:
```

Wait for user input.

### 3.3 Supervisor (reviewer)

Code/plan review. Recommended: DeepSeek V4 Pro.

Present as:
```
**Reviewer model?** (revisa código y planes)

1) DeepSeek V4 Pro  (Recomendado) — Revisión profunda
2) GPT 5.1 Codex             — OpenCode Zen
3) Claude Sonnet 4           — Balanceado
4) Custom                    — Escribe tu propio model ID

Responde con el número o nombre:
```

Wait for user input.

## Step 4: Resolve custom models

If any answer was `4` or `Custom`, ask for the exact model ID:

```
Enter provider/model ID (e.g. anthropic/claude-sonnet-4-20250514, opencode/deepseek-v4-pro):
```

Wait for user input.

## Step 5: Map answers to model IDs

| Answer | Model ID |
|--------|----------|
| `DeepSeek V4 Pro` or `1` | `opencode-go/deepseek-v4-pro` |
| `DeepSeek V4 Flash` or `1` | `opencode-go/deepseek-v4-flash` |
| `GPT 5.1 Codex` or `2` | `opencode-go/gpt-5.1-codex` |
| `Claude Sonnet 4` or `3` | `anthropic/claude-sonnet-4-20250514` |
| `Claude Haiku 4` or `3` | `anthropic/claude-haiku-4-20250514` |
| `Custom` or `4` | user-provided value (from Step 4) |

## Step 6: Generate opencode.json

Use `write` to create `opencode.json` at the project root with this exact structure:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": [".agents/skills"]
  },
  "agent": {
    "ai-orchestrator-planner": {
      "description": "Planner sub-agent for ai-orchestrator",
      "mode": "subagent",
      "model": "<chosen manager model>",
      "prompt": "{file:.agents/skills/ai-orchestrator/references/manager.md}",
      "permission": {
        "read": "allow", "write": "allow", "edit": "allow",
        "grep": "allow", "glob": "allow", "bash": "allow",
        "task": "allow", "external_directory": "deny"
      }
    },
    "ai-orchestrator-executor": {
      "description": "Executor sub-agent for ai-orchestrator",
      "mode": "subagent",
      "model": "<chosen worker model>",
      "prompt": "{file:.agents/skills/ai-orchestrator/references/worker.md}",
      "permission": {
        "read": "allow", "write": "allow", "edit": "allow",
        "grep": "allow", "glob": "allow", "bash": "allow",
        "task": "allow", "external_directory": "deny"
      }
    },
    "ai-orchestrator-reviewer": {
      "description": "Full reviewer (pro) for plan mode — checks correctness, security, architecture",
      "mode": "subagent",
      "model": "<chosen supervisor model>",
      "prompt": "{file:.agents/skills/ai-orchestrator/references/supervisor.md}",
      "permission": {
        "read": "allow", "write": "allow", "edit": "deny",
        "grep": "allow", "glob": "allow", "bash": "deny",
        "task": "allow", "external_directory": "deny"
      }
    },
    "ai-orchestrator-reviewer-flash": {
      "description": "Lightweight reviewer (flash) for quick/debug mode",
      "mode": "subagent",
      "model": "<chosen worker model>",
      "prompt": "{file:.agents/skills/ai-orchestrator/references/supervisor-lite.md}",
      "permission": {
        "read": "allow", "write": "allow", "edit": "deny",
        "grep": "allow", "glob": "allow", "bash": "deny",
        "task": "allow", "external_directory": "deny"
      }
    }
  }
}
```

Replace `<chosen manager model>`, `<chosen worker model>`, `<chosen supervisor model>` with the mapped model IDs.

## Step 7: Confirm

After writing:
1. Validate the JSON is parseable (`python -c "import json; json.load(...)"`)
2. Print confirmation:

> **ai-orchestrator is ready.** ✅
> 
> ```
> opencode.json created with 4 sub-agents:
> ├── ai-orchestrator-planner       → DeepSeek V4 Pro
> ├── ai-orchestrator-executor      → DeepSeek V4 Flash
> ├── ai-orchestrator-reviewer      → DeepSeek V4 Pro
> └── ai-orchestrator-reviewer-flash → DeepSeek V4 Flash
> ```
>
> **Restart OpenCode** then use `@ai-orchestrator` followed by your request.
