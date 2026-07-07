"""
ai-orchestrator DAG Execution Engine — Phase 1 (no priorities).

A CLI-driven Directed Acyclic Graph executor with a formal 8-state machine,
transitive cascade failure propagation, deadlock detection, and atomic state
persistence.

Usage (from orchestrator SKILL.md via bash tool):
  python dag.py init <plan.json>              # Load plan, validate, write state
  python dag.py run                           # Pop next READY task or signal done
  python dag.py complete <task_id>            # Mark task COMPLETED, unblock deps
  python dag.py fail <task_id> "<reason>"     # Mark task FAILED, cascade
  python dag.py cancel <task_id>              # Cancel task (NO cascade, but deadlock detection)
  python dag.py retry <task_id>               # Retry a FAILED task (revert cascade)
  python dag.py status                        # Print human-readable state table
  python dag.py dump                          # Print full task_states.json
"""

import json
import sys
import os
from datetime import datetime, timezone
from collections import deque
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── Constants ────────────────────────────────────────────────

STATE_FILE = ".agents/skills/ai-orchestrator/assets/state/task_states.json"

STATES = {"READY", "RUNNING", "BLOCKED", "COMPLETED", "FAILED", "CANCELLED", "SKIPPED", "PAUSED"}
TERMINAL_STATES = {"COMPLETED", "CANCELLED", "SKIPPED"}  # FAILED is retryable, NOT terminal

VALID_TRANSITIONS = {
    ("READY", "RUNNING"), ("READY", "CANCELLED"), ("READY", "SKIPPED"),
    ("RUNNING", "COMPLETED"), ("RUNNING", "FAILED"), ("RUNNING", "CANCELLED"), ("RUNNING", "PAUSED"),
    ("BLOCKED", "READY"), ("BLOCKED", "FAILED"), ("BLOCKED", "CANCELLED"), ("BLOCKED", "SKIPPED"),
    ("FAILED", "READY"), ("FAILED", "CANCELLED"),
    ("PAUSED", "READY"), ("PAUSED", "RUNNING"), ("PAUSED", "CANCELLED"), ("PAUSED", "FAILED"),
}

DEP_TYPE_TAXONOMY = {"code", "data", "config", "external", "knowledge", "decision"}

# ── Data Model ───────────────────────────────────────────────

@dataclass
class TaskNode:
    id: str
    label: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    dep_types: dict[str, str] = field(default_factory=dict)
    state: str = "BLOCKED"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    attempts: int = 0
    max_attempts: int = 1
    timeout_seconds: int = 60
    executor_model: str = "flash"
    reviewer_model: str = "flash"
    executor_task_id: Optional[str] = None
    paused_from_running: bool = False


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── JSON serialisation helpers ───────────────────────────────

def _serialize(node: TaskNode) -> dict:
    return asdict(node)


def _deserialize(data: dict) -> TaskNode:
    return TaskNode(**data)


# ── State persistence ────────────────────────────────────────

def _state_path() -> str:
    """Return the state file path. Resolve relative to repo root or env override."""
    env_path = os.environ.get("AI_ORCHESTRATOR_STATE_FILE")
    if env_path:
        return env_path
    return STATE_FILE


def load_state() -> tuple[dict, list, dict[str, TaskNode]]:
    """Load task_states.json → (metadata, transition_log, nodes dict)."""
    path = _state_path()
    if not os.path.exists(path):
        return {"plan_id": None, "plan_status": "IDLE", "created_at": None, "updated_at": None}, [], {}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    metadata = {k: data[k] for k in ("plan_id", "plan_status", "created_at", "updated_at")}
    transition_log = data.get("transition_log", [])
    nodes = {}
    for tid, tdata in data.get("tasks", {}).items():
        nodes[tid] = _deserialize(tdata)

    return metadata, transition_log, nodes


def save_state(metadata: dict, transition_log: list, nodes: dict[str, TaskNode]) -> None:
    """Atomic write to task_states.json."""
    path = _state_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    metadata["updated_at"] = _now()

    state = {
        "plan_id": metadata["plan_id"],
        "plan_status": metadata["plan_status"],
        "created_at": metadata["created_at"],
        "updated_at": metadata["updated_at"],
        "tasks": {tid: _serialize(n) for tid, n in sorted(nodes.items())},
        "transition_log": transition_log[-500:],  # Keep last 500 entries
    }

    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)


# ── Transition guard ─────────────────────────────────────────

def _transition(node: TaskNode, to_state: str, trigger: str,
                nodes: dict[str, TaskNode], metadata: dict, transition_log: list) -> tuple[bool, str]:
    """Attempt a state transition. Validates via guard, logs on success."""
    ok, msg = _guard(node, node.state, to_state, nodes)
    if not ok:
        return False, msg

    from_state = node.state
    node.state = to_state

    if to_state == "RUNNING":
        node.started_at = _now()
        node.error = None
    elif to_state == "COMPLETED":
        node.completed_at = _now()
    elif to_state == "FAILED":
        if not node.started_at:
            node.started_at = _now()

    transition_log.append({
        "task_id": node.id,
        "from": from_state,
        "to": to_state,
        "at": _now(),
        "trigger": trigger,
        "by": "dag.py",
    })

    save_state(metadata, transition_log, nodes)
    return True, f"{node.id} -> {to_state}"


def _guard(node: TaskNode, from_state: str, to_state: str,
           nodes: dict[str, TaskNode]) -> tuple[bool, str]:
    """Validate a transition. Returns (is_valid, reason)."""
    tid = node.id

    # No-op
    if from_state == to_state:
        return False, f"Task {tid}: no-op ({from_state} -> {from_state})"

    # Terminal states are frozen
    if from_state in TERMINAL_STATES:
        return False, f"Task {tid}: cannot transition from terminal state '{from_state}'"

    # Must be a valid transition pair
    if (from_state, to_state) not in VALID_TRANSITIONS:
        return False, f"Task {tid}: invalid transition {from_state} -> {to_state}"

    # --- Guards ---

    if from_state == "READY" and to_state == "RUNNING":
        unmet = [d for d in node.dependencies if nodes[d].state != "COMPLETED"]
        if unmet:
            return False, f"Task {tid}: cannot RUN — unmet dependencies: {unmet}"

    if from_state == "BLOCKED" and to_state == "READY":
        unmet = [d for d in node.dependencies if nodes[d].state != "COMPLETED"]
        if unmet:
            return False, f"Task {tid}: cannot unblock — unmet dependencies: {unmet}"

    if from_state == "FAILED" and to_state == "READY":
        if node.attempts >= node.max_attempts:
            return False, f"Task {tid}: no retries remaining ({node.attempts}/{node.max_attempts})"

    if from_state == "PAUSED" and to_state == "RUNNING":
        if not node.paused_from_running:
            return False, f"Task {tid}: was paused from READY, resume goes to READY not RUNNING"

    if from_state == "BLOCKED" and to_state == "SKIPPED":
        # Phase 1: SKIPPED cannot trigger automatically, but allow it manually
        pass

    # Fail→READY guard: if dependents are RUNNING, reject retry
    if from_state == "FAILED" and to_state == "READY":
        running_deps = [d for d in _transitive_dependents(node.id, nodes)
                        if nodes[d].state == "RUNNING"]
        if running_deps:
            return False, f"Task {tid}: cannot retry — dependents {running_deps} are still RUNNING"

    return True, "ok"


# ── DAG construction ─────────────────────────────────────────

def build_dag(tasks_data: list[dict]) -> dict[str, TaskNode]:
    """Parse JSON task list → TaskNode dict with dependents derived."""
    nodes = {}

    for t in tasks_data:
        tid = str(t["id"])
        if tid in nodes:
            raise ValueError(f"Duplicate task ID: {tid}")
        nodes[tid] = TaskNode(
            id=tid,
            label=t.get("label", ""),
            description=t.get("description", ""),
            dependencies=[str(d) for d in t.get("dependencies", [])],
            dep_types={str(k): v for k, v in t.get("dep_types", {}).items()},
        )

    # Build reverse edges (dependents)
    for tid, node in nodes.items():
        for dep_id in node.dependencies:
            if dep_id not in nodes:
                raise ValueError(f"Task {tid}: orphan dependency '{dep_id}' not found in plan")
            if dep_id == tid:
                raise ValueError(f"Task {tid}: self-dependency")
            nodes[dep_id].dependents.append(tid)

    # Validate DAG (cycle detection)
    _validate_dag(nodes)

    # Set initial states
    for tid, node in nodes.items():
        if not node.dependencies:
            node.state = "READY"
        else:
            node.state = "BLOCKED"
        node.dep_types = _validate_dep_types(node, nodes)

    return nodes


def _validate_dag(nodes: dict[str, TaskNode]) -> None:
    """DFS cycle detection. Raises ValueError on cycle."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in nodes}
    parent = {}

    def dfs(tid: str) -> None:
        color[tid] = GRAY
        for dep_id in nodes[tid].dependencies:
            if color[dep_id] == GRAY:
                # Cycle found — trace it
                cycle = [dep_id, tid]
                cur = tid
                while cur != dep_id:
                    cur = parent.get(cur)
                    if cur is None:
                        break
                    cycle.append(cur)
                cycle.reverse()
                raise ValueError(f"DAG cycle detected: {' -> '.join(cycle)}")
            if color[dep_id] == WHITE:
                parent[dep_id] = tid
                dfs(dep_id)
        color[tid] = BLACK

    for tid in nodes:
        if color[tid] == WHITE:
            dfs(tid)


def _validate_dep_types(node: TaskNode, nodes: dict[str, TaskNode]) -> dict[str, str]:
    """Validate dep_types against taxonomy. Fill missing with 'code'."""
    validated = {}
    for dep_id in node.dependencies:
        dtype = node.dep_types.get(dep_id, "code")
        if dtype not in DEP_TYPE_TAXONOMY:
            dtype = "code"
        validated[dep_id] = dtype
    return validated


# ── Cascade failure propagation ──────────────────────────────

def propagate_cascade(failed_tid: str, nodes: dict[str, TaskNode],
                       metadata: dict, transition_log: list) -> list[str]:
    """
    BFS from failed task through all dependents (transitive).
    COMPLETED/CANCELLED/SKIPPED tasks are NEVER reverted.
    RUNNING tasks are FAILED (mid-execution cascade).
    Returns list of all cascaded task IDs.
    """
    cascaded = []
    visited = set()
    queue = deque([failed_tid])

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        for dep_id in nodes[current].dependents:
            dep_node = nodes[dep_id]
            if dep_node.state in TERMINAL_STATES:
                continue
            if dep_node.state == "FAILED":
                queue.append(dep_id)
                continue

            if dep_node.state == "RUNNING":
                dep_node.error = f"cascade: dependency {current} failed mid-execution"
            else:
                dep_node.error = f"cascade: dependency {current} failed"

            ok, msg = _transition(dep_node, "FAILED", "cascade_failure", nodes, metadata, transition_log)
            if ok:
                cascaded.append(dep_id)
            queue.append(dep_id)

    return cascaded


def retry_reversal(tid: str, nodes: dict[str, TaskNode],
                   metadata: dict, transition_log: list) -> tuple[bool, str]:
    """
    Retry a FAILED task: FAILED → READY (if attempts remain).
    Revert cascade-failed dependents: FAILED(cascade) → BLOCKED.
    Does NOT touch COMPLETED/SKIPPED/CANCELLED or non-cascade FAILED.
    """
    node = nodes[tid]
    if node.state != "FAILED":
        return False, f"Task {tid}: not FAILED (current: {node.state})"

    node.attempts += 1
    ok, msg = _transition(node, "READY", "user_retry", nodes, metadata, transition_log)
    if not ok:
        return False, msg

    # Revert cascade-failed dependents
    for dep_id in _transitive_dependents(tid, nodes):
        dep_node = nodes[dep_id]
        if dep_node.state == "FAILED" and dep_node.error and dep_node.error.startswith("cascade:"):
            dep_node.error = None
            _transition(dep_node, "BLOCKED", "retry_reversal", nodes, metadata, transition_log)

    return True, f"Task {tid} retried (attempt {node.attempts}/{node.max_attempts})"


def _transitive_dependents(tid: str, nodes: dict[str, TaskNode]) -> set[str]:
    """BFS to find all descendants."""
    result = set()
    queue = deque([tid])
    while queue:
        current = queue.popleft()
        for dep_id in nodes[current].dependents:
            if dep_id not in result:
                result.add(dep_id)
                queue.append(dep_id)
    return result


# ── Deadlock detection ───────────────────────────────────────

def find_deadlocked_tasks(nodes: dict[str, TaskNode]) -> list[str]:
    """
    Find BLOCKED tasks whose ALL dependencies are terminal but NOT all COMPLETED.
    These tasks can NEVER become READY.
    """
    deadlocked = []
    for tid, node in nodes.items():
        if node.state != "BLOCKED":
            continue
        if not node.dependencies:
            continue
        all_terminal = all(nodes[d].state in TERMINAL_STATES | {"FAILED"} for d in node.dependencies)
        all_completed = all(nodes[d].state == "COMPLETED" for d in node.dependencies)
        if all_terminal and not all_completed:
            deadlocked.append(tid)
    return deadlocked


def resolve_deadlocks(nodes: dict[str, TaskNode],
                      metadata: dict, transition_log: list) -> list[str]:
    """
    Find deadlocked tasks and mark them FAILED.
    Returns list of resolved task IDs.
    """
    resolved = []
    for tid in find_deadlocked_tasks(nodes):
        node = nodes[tid]
        # Find which non-COMPLETED terminal dep is blocking
        blockers = [d for d in node.dependencies if nodes[d].state != "COMPLETED"]
        blocker_states = {d: nodes[d].state for d in blockers}
        node.error = (f"deadlock: dependencies {blocker_states} are not COMPLETED"
                      f" — task cannot proceed")
        ok, msg = _transition(node, "FAILED", "deadlock_detected", nodes, metadata, transition_log)
        if ok:
            resolved.append(tid)
    return resolved


# ── Dependency resolver (called when any task enters terminal) ─

def _resolve_dependents(terminal_tid: str, nodes: dict[str, TaskNode],
                         metadata: dict, transition_log: list) -> list[str]:
    """
    Called when a task enters any terminal state (COMPLETED, FAILED, CANCELLED, SKIPPED).
    For each dependent:
      - ALL deps COMPLETED → BLOCKED → READY (unblock)
      - ALL deps terminal, but NOT all COMPLETED → BLOCKED → FAILED (deadlock)
      - Some deps still non-terminal → stay BLOCKED
    Returns list of task IDs that changed state.
    """
    changed = []
    terminal_node = nodes[terminal_tid]

    for dep_id in terminal_node.dependents:
        dep_node = nodes[dep_id]
        if dep_node.state != "BLOCKED":
            continue

        all_terminal = all(nodes[d].state in TERMINAL_STATES | {"FAILED"} for d in dep_node.dependencies)
        all_completed = all(nodes[d].state == "COMPLETED" for d in dep_node.dependencies)

        if all_completed:
            ok, msg = _transition(dep_node, "READY", "dependencies_resolved",
                                  nodes, metadata, transition_log)
            if ok:
                changed.append(dep_id)
        elif all_terminal:
            blockers = {d: nodes[d].state for d in dep_node.dependencies if nodes[d].state != "COMPLETED"}
            dep_node.error = (f"deadlock: dependencies {blockers} are not COMPLETED"
                              f" — task cannot proceed")
            ok, msg = _transition(dep_node, "FAILED", "deadlock_detected",
                                  nodes, metadata, transition_log)
            if ok:
                changed.append(dep_id)
        # else: still waiting — do nothing

    return changed


# ── Execution scheduler ──────────────────────────────────────

def find_ready_tasks(nodes: dict[str, TaskNode]) -> list[str]:
    """Return all READY task IDs in insertion order (FIFO)."""
    return [tid for tid in sorted(nodes.keys()) if nodes[tid].state == "READY"]


def has_running_tasks(nodes: dict[str, TaskNode]) -> bool:
    """Check if any task is RUNNING."""
    return any(n.state == "RUNNING" for n in nodes.values())


def all_terminal(nodes: dict[str, TaskNode]) -> bool:
    """Check if all tasks are in terminal states."""
    if not nodes:
        return True
    for n in nodes.values():
        if n.state not in TERMINAL_STATES | {"FAILED"}:
            # FAILED is not in TERMINAL_STATES but the loop can continue if there's
            # a retry. However, with max_attempts=1, FAILED is effectively terminal.
            # For the scheduler loop: if there are READY tasks, run them.
            # If only FAILED tasks remain with no retries, they're effectively done.
            pass
    # More precise: check if any task can still make progress
    has_ready = bool(find_ready_tasks(nodes))
    has_running = has_running_tasks(nodes)
    has_blocked_waiting = any(
        n.state == "BLOCKED" and not all(
            nodes[d].state in TERMINAL_STATES | {"FAILED"}
            for d in n.dependencies
        )
        for n in nodes.values() if n.state == "BLOCKED"
    )
    return not (has_ready or has_running or has_blocked_waiting)


# ── CLI Commands ─────────────────────────────────────────────

def cmd_init(plan_path: str) -> str:
    """Load plan JSON, build DAG, write task_states.json."""
    if not os.path.exists(plan_path):
        return f"ERROR Plan file not found: {plan_path}"

    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    try:
        nodes = build_dag(plan.get("tasks", []))
    except ValueError as e:
        return f"ERROR {e}"

    now = _now()
    metadata = {
        "plan_id": plan.get("plan_id", "unknown"),
        "plan_status": "EXECUTING",
        "created_at": now,
        "updated_at": now,
    }
    transition_log = []

    save_state(metadata, transition_log, nodes)

    ready_count = len(find_ready_tasks(nodes))
    blocked_count = sum(1 for n in nodes.values() if n.state == "BLOCKED")
    return f"OK Plan loaded: {len(nodes)} tasks ({ready_count} READY, {blocked_count} BLOCKED)"


def cmd_run() -> str:
    """Pop next READY task or signal completion."""
    metadata, transition_log, nodes = load_state()

    if not nodes:
        return "ALL_DONE"

    if metadata.get("plan_status") != "EXECUTING":
        metadata["plan_status"] = "EXECUTING"

    # 1. Check for deadlocked BLOCKED tasks
    deadlocked = resolve_deadlocks(nodes, metadata, transition_log)
    if deadlocked:
        return f"DEADLOCK {' '.join(deadlocked)}"

    # 2. Find READY tasks
    ready = find_ready_tasks(nodes)
    if ready:
        tid = ready[0]
        node = nodes[tid]
        ok, msg = _transition(node, "RUNNING", "start_execution", nodes, metadata, transition_log)
        if ok:
            return f"NEXT {tid} \"{node.label}\""
        return f"ERROR {msg}"

    # 3. Check if any task is still RUNNING
    if has_running_tasks(nodes):
        return "WAIT"

    # 4. Check if there are BLOCKED tasks legitimately waiting
    blocked_waiting = any(
        n.state == "BLOCKED" and not all(
            nodes[d].state in TERMINAL_STATES | {"FAILED"}
            for d in n.dependencies
        )
        for n in nodes.values() if n.state == "BLOCKED"
    )
    if blocked_waiting:
        return "WAIT"

    # 5. All tasks terminal
    metadata["plan_status"] = "COMPLETED"
    save_state(metadata, transition_log, nodes)
    return "ALL_DONE"


def cmd_complete(tid: str) -> str:
    """Mark a task as COMPLETED. Unblock dependents."""
    metadata, transition_log, nodes = load_state()

    if tid not in nodes:
        return f"ERROR Task {tid} not found"

    node = nodes[tid]
    ok, msg = _transition(node, "COMPLETED", "execution_success", nodes, metadata, transition_log)
    if not ok:
        return f"ERROR {msg}"

    # Resolve dependents
    changed = _resolve_dependents(tid, nodes, metadata, transition_log)
    return f"OK {tid} COMPLETED unblocked={changed}"


def cmd_fail(tid: str, reason: str) -> str:
    """Mark a task as FAILED. Cascade to dependents."""
    metadata, transition_log, nodes = load_state()

    if tid not in nodes:
        return f"ERROR Task {tid} not found"

    node = nodes[tid]
    node.error = reason
    ok, msg = _transition(node, "FAILED", "execution_error", nodes, metadata, transition_log)
    if not ok:
        return f"ERROR {msg}"

    # Cascade
    cascaded = propagate_cascade(tid, nodes, metadata, transition_log)
    return f"OK {tid} FAILED cascaded={cascaded}"


def cmd_cancel(tid: str) -> str:
    """Cancel a task. NO cascade, but deadlock detection will handle dependents."""
    metadata, transition_log, nodes = load_state()

    if tid not in nodes:
        return f"ERROR Task {tid} not found"

    node = nodes[tid]
    if node.state in TERMINAL_STATES | {"FAILED"}:
        return f"ERROR Task {tid}: cannot cancel from state '{node.state}'"

    ok, msg = _transition(node, "CANCELLED", "user_cancel", nodes, metadata, transition_log)
    if not ok:
        return f"ERROR {msg}"

    # Resolve dependents (this will detect deadlocks)
    changed = _resolve_dependents(tid, nodes, metadata, transition_log)

    return f"OK {tid} CANCELLED unresolved_dependents={changed}"


def cmd_retry(tid: str) -> str:
    """Retry a FAILED task with cascade reversal."""
    metadata, transition_log, nodes = load_state()

    if tid not in nodes:
        return f"ERROR Task {tid} not found"

    ok, msg = retry_reversal(tid, nodes, metadata, transition_log)
    if ok:
        return f"OK {msg}"
    return f"ERROR {msg}"


def cmd_cancel_all() -> str:
    """Cancel all non-terminal, non-FAILED tasks."""
    metadata, transition_log, nodes = load_state()
    cancelled = []
    for tid in sorted(nodes.keys()):
        node = nodes[tid]
        if node.state not in TERMINAL_STATES | {"FAILED"}:
            _transition(node, "CANCELLED", "user_cancel_all", nodes, metadata, transition_log)
            cancelled.append(tid)
    return f"OK Cancelled {len(cancelled)} tasks: {cancelled}"


def cmd_status() -> str:
    """Print human-readable task state table."""
    metadata, transition_log, nodes = load_state()
    lines = []
    lines.append(f"Plan: {metadata.get('plan_id', 'N/A')} | Status: {metadata.get('plan_status', 'N/A')}")
    lines.append(f"{'ID':<6} {'Label':<30} {'State':<12} {'Attempts':<9} {'Error'}")
    lines.append("-" * 80)
    for tid in sorted(nodes.keys()):
        n = nodes[tid]
        err = (n.error or "-")[:40]
        lines.append(f"{tid:<6} {n.label:<30} {n.state:<12} {n.attempts}/{n.max_attempts:<5} {err}")
    lines.append(f"\nTasks: {len(nodes)} | Transition log entries: {len(transition_log)}")
    return "\n".join(lines)


def cmd_dump() -> str:
    """Print full task_states.json."""
    path = _state_path()
    if not os.path.exists(path):
        return "{}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ── Main ─────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) < 3:
            print("Usage: python dag.py init <plan.json>")
            return
        print(cmd_init(sys.argv[2]))

    elif command == "run":
        print(cmd_run())

    elif command == "complete":
        if len(sys.argv) < 3:
            print("Usage: python dag.py complete <task_id>")
            return
        print(cmd_complete(sys.argv[2]))

    elif command == "fail":
        if len(sys.argv) < 4:
            print("Usage: python dag.py fail <task_id> \"<reason>\"")
            return
        print(cmd_fail(sys.argv[2], sys.argv[3]))

    elif command == "cancel":
        if len(sys.argv) < 3:
            print("Usage: python dag.py cancel <task_id>")
            return
        print(cmd_cancel(sys.argv[2]))

    elif command == "cancel-all":
        print(cmd_cancel_all())

    elif command == "retry":
        if len(sys.argv) < 3:
            print("Usage: python dag.py retry <task_id>")
            return
        print(cmd_retry(sys.argv[2]))

    elif command == "status":
        print(cmd_status())

    elif command == "dump":
        print(cmd_dump())

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
