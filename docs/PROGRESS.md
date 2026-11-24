# Progress

## Fase 2 — 2026-11-24

Branch `feat/fase2`. README reescrito em "O que funciona hoje" /
"Pesquisa em andamento", sem claim sem teste; nome único PAI; modo padrão
`propose_only` com modos autônomos experimentais; Utility Guardian com 10
tarefas reais da Karen e `epsilon`; trava de patches por 24h com lock e log;
`rollback.sh` com `PAI_DRY_RUN=1` testado em diretório descartável;
Policy-as-Code no formato do SAFE-AI; referências verificadas e demais marcadas
"a verificar"; `docs/THREAT-MODEL.md` e `docs/RESEARCH-QUESTION.md`.

Como testar (branch isolada):

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

## Fase 3 — 2026-11-24

Branch `feat/fase3` (merge de `feat/fase2` para manter os testes verdes).

Pasta `service/` com escopo em 5 etapas, templates de relatório e política,
checklist de inventário (15 perguntas), vertical financeiro com exemplo do
pacote imobiliário do LLM-SEC, one-pagers PT/EN, proposta white-label e
checklist LGPD. Sem números inventados, sem promessa de conformidade, sem nomes
de empresas como clientes.

Como testar (branch isolada):

```
cd /home/admin/PAI
/tmp/opencode/pai-venv/bin/python -m pytest -q
# 16 passed
```

Pendente: definir canal de contato oficial do serviço; preço e prazo case a
case; revisão jurídica do checklist LGPD.

## Fase 4 — 2026-11-24

Branch `feat/fase4` (sem push, sem deploy).

Site estático em `site/`: uma página PT-BR e EN gerada dos JSON em
`site/content/`, `/pai` como página separada sem link no menu, tema claro/escuro,
acessibilidade básica, robots/sitemap, sem analytics e sem backend. Transcrição
real do demo do SAFE-AI em vez de vídeo inventado.

Como testar (branch isolada):

```
cd /home/admin/PAI/site
npm run build
npm test
# 5 tests pass
```

Pendente: definir `SITE_URL` real antes do sitemap; definir e-mail oficial
(hoje vazio); Lighthouse mobile **não medido** (sem Chrome/Lighthouse na
máquina); publicar é Tier 2 e depende de aprovação.

## Integração

Conflitos resolvidos em `integration/pai-fases`: `docs/PROGRESS.md` tinha um
resumo por branch e `.gitignore` tinha entradas diferentes. O progresso foi
concatenado em ordem cronológica (Fases 2, 3 e 4) e o `.gitignore` ficou com a
união das entradas (`__pycache__/`, `*.pyc`, `.pytest_cache/`, `site/dist/`).
Nenhuma `main` foi alterada e nada foi empurrado.

Testes finais da integração:

```
cd /home/admin/PAI
/tmp/opencode/pai-venv/bin/python -m pytest -q
cd site && npm test
```
