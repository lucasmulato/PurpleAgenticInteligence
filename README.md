# PAI — Purple Agentic Intelligence

Loop vermelho/azul para agentes de IA, com **portão humano por padrão**.
Nome único: **PAI**. O repositório continua `PurpleAgenticInteligence` (renome
depende de aprovação do Lucas).

> Status "AI Safety Residency 2026" e "Private R&D" apareciam na versão anterior
> do README. **A verificar com o Lucas** — não são apresentados aqui como fato.

## O que funciona hoje

Só o que os testes provam:

- **Utility Guardian** — baseline de 10 tarefas reais da Karen; um patch que
  bloqueia mais de `epsilon` pontos é rejeitado. Evidência:
  `tests/test_utility_guardian.py`.
- **Trava de profundidade** — no máximo 3 patches por 24h, com log append-only
  e lock de arquivo. Evidência: `tests/test_fase2.py`.
- **Rollback testado** — `rollback.sh` tem modo `PAI_DRY_RUN=1` que restaura o
  manifesto em diretório descartável, sem matar processos. Evidência:
  `tests/test_fase2.py`.
- **Policy-as-Code** — um patch aprovado gera uma política no formato que o
  SAFE-AI carrega (`permit` / `ask_human` / `reject`). Evidência:
  `tests/test_fase2.py`.
- **Modo padrão `propose_only`** — o orchestrator propõe o patch e para; não
  grava manifesto sem aprovação. Evidência: `tests/test_fase2.py`.

Os servidores MCP em `agents/` são **stubs**: produzem payloads e patches de
demonstração. Não há red team evolutivo real, nem benchmarks medidos.

## Pesquisa em andamento

Não são funcionalidades entregues:

- **Async Shield** — auditoria assíncrona após a ação (janela de detecção).
- **Pareto Utility–Security** — escolher patches preservando utilidade.
- **Auto-patch** — proposto como PR, revisado por humano no modo padrão.
- **Nash Equilibrium** — objetivo de pesquisa, **não um resultado medido**.

## Autonomia

`config/autonomy.yaml`:

- `propose_only` — **padrão**. Blue propõe patch; humano aprova.
- `auto_with_rollback` — experimental: aplica com snapshot prévio.
- `auto` — experimental: aplica sem rollback. Não recomendado em produção.

Modos autônomos não foram validados em ambiente regulado. Não use para
"corrigir em 1 minuto sem assinatura humana" — isso contradiz o portão da
Karen e a expectativa de clientes regulados.

## Rodar

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python3 core/orchestrator.py        # demo local, modo propose_only
```

## Referências

Verificadas em 2026-11-24:

- arXiv:2601.13518 — *AgenticRed: Evolving/Optimizing Agentic Systems for
  Red-Teaming*.
- arXiv:2512.13526 — *Async Control: Stress-testing Asynchronous Control
  Measures for LLM Agents* (código em `github.com/UKGovernmentBEIS/async-control`).

A verificar: a afiliação "UK AISI" do segundo artigo (inferida do repositório
de código, não explicitada no resumo).

## Limites

1. Matching é estrutural, não semântico; patches são avaliados contra o
   baseline, não contra um modelo de ameaças completo.
2. Servidores MCP são stubs; não há geração evolutiva de ataques.
3. Nenhum benchmark de segurança ou utilidade foi publicado — números aqui são
   de teste unitário, não resultados de produto.
4. Não substitui revisão humana nem a trilha do SAFE-AI.
5. Sem promessa de conformidade com LGPD ou com marco legal de IA.

Ver `docs/THREAT-MODEL.md` e `docs/RESEARCH-QUESTION.md`.
