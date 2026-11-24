# Pergunta de pesquisa (uma)

**É possível gerar patches de política para agentes de IA que aumentem a
resistência a ataques sem reduzir a utilidade em tarefas reais abaixo de um
limite aceitável, mantendo aprovação humana por padrão?**

Variáveis observáveis: `U` (score no baseline de tarefas), `S` (resultado da
suíte adversarial) e `Δ` (quantidade de patches em 24h). `S` ainda **não está
medido** — este documento não afirma resultado.

## Marcos (artefatos públicos)

| Data | Marco | Artefato público |
|---|---|---|
| 2026-12-15 | Baseline de utilidade e trava de profundidade publicadas com testes | `tests/test_utility_guardian.py`, `tests/test_fase2.py`, `config/autonomy.yaml` |
| 2027-01-31 | Gerador de Policy-as-Code validado contra o SAFE-AI em CI | `core/policy_patch.py` + teste de carga da política no repo SAFE-AI |
| 2027-03-31 | Primeira medição de `S` com suíte adversarial reproduzível | relatório em `reports/` com comando exato e dados brutos |

Nenhum marco afirma "Nash equilibrium" ou "correção em 1 minuto". Ambos são
objetivos, não evidências.

## Uso em candidaturas

Este arquivo alimenta `manifund` e fundos de pesquisa. A submissão é sempre
decidida pelo Lucas (Tier 2). Ver `docs/STATE.md` no repo `karen` para o tracker.
