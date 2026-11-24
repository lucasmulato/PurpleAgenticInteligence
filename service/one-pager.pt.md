# Auditoria de Ações de Agentes de IA

**Problema.** Agentes de IA sugerem e executam ações. Uma injeção de prompt ou
uma permissão larga demais pode causar dano antes de alguém perceber.

**Abordagem.** Cinco etapas de escopo fechado: inventário das ações, mapa de
riscos, política executável, testes adversariais (incluindo injeção por
conteúdo externo) e relatório em português. Ver [AUDITORIA.md](AUDITORIA.md).

**Demo.** O gateway determinístico SAFE-AI decide `PERMIT`, `REJECT` ou
`ASK_HUMAN` e registra tudo em `/audit`. Roteiro de 90 segundos:
[DEMO-SCRIPT.md](../docs/DEMO-SCRIPT.md).

**Entregáveis.** Relatório, arquivo de política no formato do SAFE-AI,
evidências dos testes e registro de limites conhecidos.

**Oferta.** Escopo fixo, sem mensalidade obrigatória e sem plataforma para
comprar. Valor e prazo são definidos no documento de escopo, caso a caso —
não publicamos número sem decisão do Lucas.

**Contato.** [canal oficial a definir pelo Lucas].

Não garantimos conformidade com LGPD nem com marco legal de IA. O serviço
entrega evidências e limites explícitos.
