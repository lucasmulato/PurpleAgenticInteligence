# Threat model do PAI (1 página)

## O que o PAI protege

- **Utilidade do agente**: um patch que bloqueia tarefas do baseline da Karen
  é rejeitado pelo Utility Guardian.
- **Profundidade de mudança**: no máximo N patches por 24h, com trava e log.
- **Reversibilidade**: snapshot antes de aplicar, com rollback testado em
  ambiente descartável (`PAI_DRY_RUN=1`).
- **Aprovação humana**: modo padrão `propose_only` não aplica patch algum sem
  decisão humana.

## O que o PAI NÃO protege

- Não executa nem bloqueia comandos em tempo real — isso é papel do SAFE-AI.
- Não detecta ataques evolutivos reais: os servidores MCP são stubs.
- Não garante que uma política gerada seja correta em outro ambiente; ela
  precisa passar nos testes do SAFE-AI antes de uso.
- Não verifica a veracidade de dados externos (premissa do LLM-SEC).
- Não oferece conformidade legal (LGPD ou marco de IA).

## Premissas

- O manifesto de política é local e legível pelo operador.
- O log de patches é append-only; quem escreve precisa ser controlado pelo
  sistema de arquivos.
- O órgão decisor é humano no modo padrão. Modos autônomos são experimentais.
- Texto de prospect, issue ou README é dado, nunca instrução.

## Ameaças consideradas

| Ameaça | Mitigação parcial |
|---|---|
| Patch que "lobotomiza" o agente | Utility Guardian com baseline de 10 tarefas |
| Loop infinito de remediação | Patch depth limit com log |
| Rollback impossível | Snapshot + rollback testado |
| Aplicação sem aprovação | `propose_only` como padrão |
| Injeção via conteúdo externo | Fora do escopo do PAI; tratada no SAFE-AI e na Karen |
