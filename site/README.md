# Site estático — auditoria de agentes + Climara

Site de uma página, sem backend, gerado a partir de JSON. PT-BR primeiro, EN
depois. Páginas: `/`, `/en/`, `/pai/` (escondida, sem link no menu) e
`/en/pai/`.

## Desenvolver

```bash
npm run build
npm test
npm run build   # gera dist/
```

Sirva `dist/` com qualquer servidor estático, por exemplo:
`python3 -m http.server --directory dist`.

## Editar textos

- `content/site.pt.json` — todos os textos e preços em português.
- `content/site.en.json` — versão em inglês.
- `content/demo-transcript.txt` — transcrição real do `scripts/demo.py`
  do SAFE-AI (não há vídeo; não inventar link).

O HTML é gerado pelo `scripts/build.mjs`. Não edite `dist/` à mão.

## Antes de publicar

- Definir `SITE_URL` para gerar `sitemap.xml` com a URL real:
  `SITE_URL=https://seu-dominio npm run build`. Sem isso o sitemap usa
  `https://example.invalid` como placeholder.
- Definir o e-mail oficial em `contact.email` nos dois JSON (hoje vazio;
  o site mostra "a definir").
- O WhatsApp usa `+5511988869469` (número pessoal provisório do Lucas).
- Publicar é Tier 2: precisa de aprovação. Nenhum deploy foi feito aqui.

## Verificação

`npm test` valida: páginas PT/EN geradas dos JSON, `/pai` fora da navegação,
preço da auditoria sem número inventado, nenhuma frase de garantia de
conformidade, arquivos estáticos, robots, sitemap e ausência de analytics.

**Lighthouse mobile não foi medido** — não há Chrome/Lighthouse nesta máquina.
O layout usa sistema de fontes, CSS mínimo e JS apenas para o tema claro/escuro,
mas o número de Lighthouse permanece "não medido" até execução real.
