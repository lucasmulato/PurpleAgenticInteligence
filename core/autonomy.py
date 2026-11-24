"""Modo de autonomia do PAI.

Padrão é `propose_only`: o Blue propõe um patch, um humano aprova. Modos
autônomos são experimentais e devem ser explícitos em config/autonomy.yaml.
"""
import os
from pathlib import Path
from typing import Literal

MODES = ("propose_only", "auto_with_rollback", "auto")
Mode = Literal["propose_only", "auto_with_rollback", "auto"]

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "config" / "autonomy.yaml"


def load_mode(config_path: str | None = None) -> Mode:
    """Lê `autonomy:` do YAML; qualquer valor desconhecido volta ao padrão."""
    path = Path(config_path or os.getenv("PAI_AUTONOMY_CONFIG", str(DEFAULT_CONFIG)))
    raw = ""
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("autonomy:"):
                raw = line.split(":", 1)[1].strip().strip("'\"")
                break
    return raw if raw in MODES else "propose_only"  # type: ignore[return-value]


def is_autonomous(mode: Mode) -> bool:
    """Só os modos explícitos auto_with_rollback e auto aplicam patches."""
    return mode in ("auto_with_rollback", "auto")
