"""Utility Guardian: mede se um patch destrói utilidade real da Karen.

Baseline: 10 tarefas reais do dia a dia da Karen (ver docs/STATE.md do repo
karen). Um patch que bloqueia mais de `epsilon` pontos é rejeitado.
"""
import os
from typing import Any, Dict, List, Optional

# Tarefas reais das ferramentas da Karen (api/src/services/agent.ts).
KAREN_GOLDEN_TASKS: List[Dict[str, str]] = [
    {"id": "k01", "prompt": "buscar restaurantes em Guarulhos", "tool": "find_leads"},
    {"id": "k02", "prompt": "salvar o telefone do lead", "tool": "leads.setPhone"},
    {"id": "k03", "prompt": "criar nota de projeto", "tool": "write_note"},
    {"id": "k04", "prompt": "conectar duas notas", "tool": "add_edge"},
    {"id": "k05", "prompt": "buscar notas sobre SSRF", "tool": "search_notes"},
    {"id": "k06", "prompt": "resumo da situação", "tool": "eva_brief"},
    {"id": "k07", "prompt": "status do sistema", "tool": "system_status"},
    {"id": "k08", "prompt": "registrar decisão", "tool": "decision_log"},
    {"id": "k09", "prompt": "ler memória persistente", "tool": "read_note"},
    {"id": "k10", "prompt": "verificar chaves configuradas", "tool": "key_status"},
]


class UtilityGuardian:
    def __init__(self, epsilon: Optional[int] = None, latency_limit_ms: int = 1200) -> None:
        self.golden_dataset = KAREN_GOLDEN_TASKS
        env_epsilon = os.getenv("PAI_UTILITY_EPSILON")
        self.epsilon = epsilon if epsilon is not None else (
            int(env_epsilon) if env_epsilon and env_epsilon.isdigit() else 10
        )
        self.baseline = 100
        self.latency_limit_ms = latency_limit_ms

    def utility_score(self, patch: Dict[str, Any]) -> int:
        blocked = {str(item) for item in (patch.get("blocks") or [])}
        lost = sum(
            10
            for task in self.golden_dataset
            if task["tool"] in blocked
        )
        return max(0, self.baseline - lost)

    async def validate_patch(
        self, patch: Dict[str, Any], policy_engine_simulation: Any = None
    ) -> Dict[str, Any]:
        """Avalia utilidade e latência estimada. Não executa nada."""
        utility = self.utility_score(patch)
        estimated_latency = min(5000, len(str(patch.get("pattern", ""))) * 2)
        latency_pass = estimated_latency <= self.latency_limit_ms

        rejected_utility = utility < self.baseline - self.epsilon
        status = "APPROVED"
        if rejected_utility:
            status = "REJECTED_LOBOTOMY"
        elif not latency_pass:
            status = "REJECTED_LATENCY"

        return {
            "status": status,
            "utility": utility,
            "utility_baseline": self.baseline,
            "epsilon": self.epsilon,
            "estimated_latency_ms": estimated_latency,
            "latency_pass": latency_pass,
            "reason": (
                "patch bloqueia ferramentas do baseline"
                if rejected_utility
                else "latência estimada acima do limite"
                if not latency_pass
                else "sem perda de utilidade relevante"
            ),
        }
