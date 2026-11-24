"""Converte um patch aprovado em Policy-as-Code legível pelo SAFE-AI.

O formato é o mesmo de `config/allowlist.yaml` do SAFE-AI: permit / ask_human /
reject. Escrevemos sintaxe JSON (subconjunto válido de YAML) para evitar
dependência de biblioteca YAML na geração.
"""
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def render_safe_ai_policy(patch: Dict[str, Any]) -> str:
    """Devolve o conteúdo YAML de uma política para o SAFE-AI."""
    action = str(patch.get("action", "FLAG")).upper()
    target_bucket = {
        "PERMIT": "permit",
        "FLAG": "ask_human",
        "ASK_HUMAN": "ask_human",
        "BLOCK": "reject",
        "REJECT": "reject",
    }.get(action, "reject")

    buckets: Dict[str, list] = {"permit": [], "ask_human": [], "reject": []}
    commands: Iterable[Any] = patch.get("commands") or []
    if not commands:
        pattern = str(patch.get("pattern", "")).strip()
        commands = [pattern] if pattern else []

    for command in commands:
        value = str(command).strip()
        if value and value not in buckets[target_bucket]:
            buckets[target_bucket].append(value)

    return (
        "# Política gerada pelo PAI — revisar antes de aplicar\n"
        + "".join(
            f"{name}: {json.dumps(values, ensure_ascii=False)}\n"
            for name, values in buckets.items()
        )
    )


def write_safe_ai_policy(patch: Dict[str, Any], path: str) -> Path:
    """Escreve a política em `path` e devolve o caminho."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_safe_ai_policy(patch), encoding="utf-8")
    return target
