"""Core trajectory distiller turning raw agent logs into compact episodic lessons."""
import hashlib
from typing import Any, Dict, List, Optional


class EpisodicTraceDistiller:
    """Extracts (trigger, mistake, verified_fix) lessons from multi-turn execution traces."""

    def distill(self, steps: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not steps:
            return None

        first_error = None
        error_idx = -1
        for i, st in enumerate(steps):
            if st.get("status") == "error":
                first_error = st
                error_idx = i
                break

        if first_error is None:
            return {
                "lesson_id": hashlib.sha256(str(len(steps)).encode("utf-8")).hexdigest()[:10],
                "kind": "clean_run",
                "trigger": steps[0].get("tool", "start"),
                "verified_fix": "completed_without_errors",
                "steps_compressed": len(steps),
            }

        recovery_steps = [
            f"{s.get('tool')}({s.get('args', {})})"
            for s in steps[error_idx + 1:]
            if s.get("status") == "ok"
        ]
        resolved = len(recovery_steps) > 0 and steps[-1].get("status") == "ok"
        trigger = f"{first_error.get('tool')}: {first_error.get('error', 'unknown_error')}"
        fix = " -> ".join(recovery_steps) if resolved else "unresolved"
        lid = hashlib.sha256(f"{trigger}|{fix}".encode("utf-8")).hexdigest()[:12]

        return {
            "lesson_id": lid,
            "kind": "recovery_lesson" if resolved else "failure_warning",
            "trigger": trigger,
            "verified_fix": fix,
            "resolved": resolved,
            "steps_compressed": len(steps),
        }
