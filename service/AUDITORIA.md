# Auditoria de Ações de Agentes de IA — escopo fechado

Serviço de escopo fixo. Entrega em português: relatório + política executável.
Não é consultoria aberta, não é plataforma e não é garantia de conformidade legal.

## As cinco etapas

1. **Inventário das ações** — listar o que o agente do cliente pode executar
   (comandos, ferramentas, APIs, dados acessíveis, who pode aprovar).
2. **Mapa de riscos por ação** — para cada ação: o que acontece se for
   executada indevidamente, quem pode acionar, o que limita o dano.
3. **Política executável** — arquivo no formato do SAFE-AI (`permit`,
   `ask_human`, `reject`) com os limites acordados. Nada é aplicado sem
   aprovação do cliente.
4. **Testes adversariais** — inclui injeção de prompt por conteúdo externo
   (resposta de prospect, e-mail, issue, página raspada). Registro das
   decisões `PERMIT` / `REJECT` / `ASK_HUMAN`.
5. **Relatório final** — achados, evidências, limites e próximos passos.
   Modelo em `templates/relatorio.md`.

## O que NÃO está no escopo

- Implementar ou operar os sistemas do cliente.
- Garantir conformidade com LGPD, marco legal de IA ou qualquer norma.
- Red teaming autônomo contínuo nem auto-correção de políticas em produção.
- Acesso a credenciais, pagamentos ou dados pessoais além do necessário para
  o inventário.
- Números de desempenho ou benchmarks sem medição acordada previamente.

## Entradas e saídas

- Entrada: documento de escopo assinado pelo cliente + acesso controlado ao
  mapa de ferramentas/permissões do agente.
- Saída: `relatorio.md`, `politica.yaml`, evidências dos testes e este escopo.

## Contato

Definir canal oficial com o Lucas antes de publicar. Não publicar e-mail ou
telefone inventados.
