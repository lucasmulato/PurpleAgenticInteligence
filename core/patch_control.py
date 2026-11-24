"""Trava de profundidade de patches: no máximo N patches por 24h, com log."""
import fcntl
import json
import os
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple


class PatchController:
    def __init__(
        self,
        ledger_path: str = "data/patch_ledger.jsonl",
        max_per_24h: Optional[int] = None,
        now_fn: Optional[Any] = None,
    ) -> None:
        self.ledger_path = Path(
            os.getenv("PAI_PATCH_LEDGER", ledger_path)
        )
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        env_max = os.getenv("PAI_PATCH_DEPTH_MAX_24H")
        self.max_per_24h = max_per_24h or (
            int(env_max) if env_max and env_max.isdigit() else 3
        )
        self._now = now_fn or (lambda: datetime.now(timezone.utc))

    @contextmanager
    def _locked(self) -> Iterator[None]:
        lock_path = Path(str(self.ledger_path) + ".lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with open(lock_path, "a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _recent(self) -> List[Dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        cutoff = self._now() - timedelta(hours=24)
        entries: List[Dict[str, Any]] = []
        for line in self.ledger_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            try:
                when = datetime.fromisoformat(entry["timestamp"])
            except (KeyError, ValueError):
                continue
            if when >= cutoff:
                entries.append(entry)
        return entries

    def status(self) -> Dict[str, Any]:
        used = len(self._recent())
        return {
            "used": used,
            "max": self.max_per_24h,
            "allowed": used < self.max_per_24h,
        }

    def can_patch(self) -> Tuple[bool, str]:
        state = self.status()
        if state["allowed"]:
            return True, "ok"
        return (
            False,
            f"Patch depth atingido: {state['used']}/{state['max']} nas últimas 24h.",
        )

    def record(self, patch_id: str) -> Dict[str, Any]:
        """Registra um patch. Levanta RuntimeError se a trava estiver ativa."""
        with self._locked():
            allowed, reason = self.can_patch()
            if not allowed:
                raise RuntimeError(reason)
            entry = {
                "id": patch_id,
                "timestamp": self._now().isoformat(),
                "approved_by": "human" if os.getenv("PAI_APPROVED_BY") else "pending",
            }
            with open(self.ledger_path, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
            return entry
