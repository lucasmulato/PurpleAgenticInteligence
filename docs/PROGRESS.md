# Progress

## Fase 2 — 2026-11-24

Branch `feat/fase2` (sem push).

Mudou: README reescrito em "O que funciona hoje" / "Pesquisa em andamento",
sem claim sem teste; nome único PAI; modo padrão `propose_only` com modos
autônomos experimentais; Utility Guardian com 10 tarefas reais da Karen e
`epsilon`; trava de patches por 24h com lock e log; `rollback.sh` com
`PAI_DRY_RUN=1` testado em diretório descartável; Policy-as-Code no formato do
SAFE-AI; referências verificadas e demais marcadas "a verificar";
`docs/THREAT-MODEL.md` e `docs/RESEARCH-QUESTION.md`.

Como testar:

```
cd /home/admin/PAI
/tmp/opencode/pai-venv/bin/python -m pytest -q
# 10 passed
python3 core/orchestrator.py
# termina em "Modo propose_only: patch proposto como PR; humano aprova."
```

Pendente: confirmar "AI Safety Residency 2026"/"Private R&D"; medir `S`
(suíte adversarial) — hoje é "não medido"; validar a política gerada com o
SAFE-AI em CI entre repos; renomear o repo depende de aprovação do Lucas.
