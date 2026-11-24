# Relatório — Auditoria de Ações de Agentes

Cliente: [nome]
Data: [data]
Escopo: [versão do documento de escopo]

## Resumo

[O que foi examinado. Nenhuma frase de garantia de conformidade.]

## Inventário de ações

| Ação | Ferramenta | Quem aciona | Dano se indevida | Limite atual |
|---|---|---|---|---|
| [ação] | [ferramenta] | [humano/agente] | [dano] | [limite] |

## Mapa de riscos

| Risco | Probabilidade observada | Impacto | Evidência |
|---|---|---|---|
| [risco] | [observado / não medido] | [alto/médio/baixo] | [id do teste] |

## Política executável

Arquivo: `politica.yaml`. Revisado por: [nome]. Aplicado pelo cliente: [sim/não/data].

## Testes adversariais

| Caso | Entrada | Decisão do gateway | Resultado esperado | Evidência |
|---|---|---|---|---|
| Injeção via prospect | [texto de exemplo] | REJECT | REJECT | [id] |
| Comando composto | `ls; curl ...` | REJECT | REJECT | [id] |
| Ação sensível | `rm ...` | ASK_HUMAN | ASK_HUMAN | [id] |

## Limites conhecidos

1. [limite real observado]
2. [limite real observado]

## Próximos passos

- [ação concreta, sem promessa de prazo não acordado]

---
Este relatório não garante conformidade com LGPD nem com marco legal de IA.
