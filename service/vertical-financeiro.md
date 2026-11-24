# Vertical financeiro — exemplo com pacote imobiliário

Este é um **exemplo de política executável**, não uma regra de negócio do
cliente. Os limites reais devem vir do cliente e de fonte oficial verificada.

## O que o LLM-SEC declara (manter palavras exatas)

Do README do LLM-SEC: *"Commercial Real-Estate Underwriting Pack: Production
domain pack enforcing statutory LTV caps, DSCR floors, and Ed25519 dual-human
authorization."*

Conformidade declarada, sem aumentar o claim: **CONF-2 (Reproducible)** overall;
**CONF-3 (Bounded Model Checking)** for core protocol.

## Exemplo de regras

| Controle | Exemplo | Natureza |
|---|---|---|
| Teto de LTV | "até 75%" citado em `docs/CONFORMANCE.md` do LLM-SEC como convenção regulatória | **exemplo**, não regra do cliente |
| Piso de DSCR | limite a definir pelo cliente | **a definir** — não inventar número |
| Dupla autorização | assinatura Ed25519 de duas pessoas | mecanismo do LLM-SEC; quem são as pessoas é decisão do cliente |

## Como isso vira escopo de auditoria

1. Identificar quais ações de underwriting o agente pode executar.
2. Perguntar ao cliente qual é o teto de LTV e o piso de DSCR aplicáveis.
3. Verificar se a dupla autorização é exigida para quais ações.
4. Gerar política executável no formato do SAFE-AI com `ask_human` para
   aprovação e `reject` para operações fora do escopo.
5. Testar injeção de prompt em dados de entrada (laudo, e-mail, proposta).

## Limites

- O gateway aplica regras mecanicamente; **não prova** que os limites são
  economicamente corretos nem que os dados de entrada são verdadeiros.
- Nenhum número de aprovação, precisão ou economia é apresentado sem medição.
- Não há promessa de conformidade com regulamentação financeira.
