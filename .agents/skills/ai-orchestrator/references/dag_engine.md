# DAG Engine Reference

The DAG engine (`dag.py`) is a Python CLI tool that manages the task lifecycle
state machine. The orchestrator invokes it via `bash` tool.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `python dag.py init <plan.json>` | Load plan, build DAG, write task_states.json | `bash: python .agents/skills/ai-orchestrator/dag.py init assets/plan/plan_input.json` |
| `python dag.py run` | Pop next READY task or signal done | `bash: python .agents/skills/ai-orchestrator/dag.py run` |
| `python dag.py complete <task_id>` | Mark task COMPLETED, unblock dependents | `bash: python .agents/skills/ai-orchestrator/dag.py complete 1` |
| `python dag.py fail <task_id> "<error>"` | Mark task FAILED, cascade to dependents | `bash: python .agents/skills/ai-orchestrator/dag.py fail 2 "syntax error"` |
| `python dag.py cancel <task_id>` | Cancel task (NO cascade, but deadlock detection) | `bash: python .agents/skills/ai-orchestrator/dag.py cancel 3` |
| `python dag.py cancel-all` | Cancel all non-terminal tasks | `bash: python .agents/skills/ai-orchestrator/dag.py cancel-all` |
| `python dag.py retry <task_id>` | Retry a FAILED task, revert cascade dependents | `bash: python .agents/skills/ai-orchestrator/dag.py retry 2` |
| `python dag.py status` | Print human-readable state table | `bash: python .agents/skills/ai-orchestrator/dag.py status` |
| `python dag.py dump` | Full JSON state dump to stdout | `bash: python .agents/skills/ai-orchestrator/dag.py dump` |

## Output Format

### `init`
```
OK Plan loaded: 5 tasks (2 READY, 3 BLOCKED)
ERROR Cycle detected: 1 -> 2 -> 1
ERROR Plan file not found: assets/plan/missing.json
```

### `run`
```
NEXT 1 "Set up project scaffolding"    ← execute this task
WAIT                                     ← tasks are RUNNING, poll again
ALL_DONE                                 ← all tasks terminal
DEADLOCK 3 4                            ← deadlocked tasks auto-failed
```

### `complete`, `fail`, `cancel`, `retry`
```
OK 1 COMPLETED unblocked=['2']     ← success
OK 2 FAILED cascaded=['3', '4']    ← with cascade
OK 3 CANCELLED unresolved_dependents=['5']  ← deadlock detected
ERROR 2: cannot RUN — unmet deps: ['1']     ← guard rejected
```

### `status`
```
Plan: test-3-task-dag | Status: EXECUTING
ID     Label                          State        Attempts  Error
------------------------------------------------------------------------
1      Set up project                 COMPLETED    0/1       -
2      Implement feature              CANCELLED    0/1       user cancelled
3      Write tests                    FAILED       0/1       deadlock: dep 2 is CANCELLED
```

## Plan JSON Format (input to `init`)

```json
{
  "plan_id": "2026-07-07-plan-001",
  "objective": "Build a CLI tool",
  "tasks": [
    {
      "id": "1",
      "label": "Set up project",
      "description": "Create project scaffolding",
      "dependencies": [],
      "dep_types": {}
    },
    {
      "id": "2",
      "label": "Implement feature",
      "description": "Write the core feature",
      "dependencies": ["1"],
      "dep_types": {"1": "code"}
    },
    {
      "id": "3",
      "label": "Write tests",
      "description": "Write unit tests",
      "dependencies": ["2"],
      "dep_types": {"2": "code"}
    }
  ]
}
```

## Error Codes

| Output | Meaning | Action |
|--------|---------|--------|
| `OK ...` | Command succeeded | Continue |
| `ERROR ...` | Command failed (guard rejected, etc.) | Check error, retry |
| `NEXT <id> "<label>"` | Task ready for execution | Delegate to executor, then `complete` or `fail` |
| `WAIT` | No READY tasks, some RUNNING | Poll again after a short delay |
| `ALL_DONE` | All tasks terminal | Generate report |
| `DEADLOCK <ids>` | Deadlocked tasks auto-failed | May need user intervention |

## State Machine (8 states)

```
READY ──→ RUNNING ──→ COMPLETED (terminal)
                  └──→ FAILED ──→ READY (retry, if attempts remain)
                  └──→ PAUSED ──→ RUNNING (resume)
BLOCKED ──→ READY (deps resolved)
        └──→ FAILED (cascade or deadlock)
FAILED ──→ READY (retry) ──→ revert cascade dependents to BLOCKED
CANCELLED (terminal, NO cascade)
SKIPPED (terminal)
```

Key rules:
- FAILED is retryable (not terminal). Only enters terminal when retries exhausted.
- CANCELLED does NOT cascade. But dependents may deadlock (all deps terminal, not all COMPLETED).
- Cascade is transitive BFS through all dependents. COMPLETED/CANCELLED/SKIPPED are never reverted.
- Deadlock detection auto-fails BLOCKED tasks whose all dependencies are terminal but not all COMPLETED.
