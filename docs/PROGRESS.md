# Progress

## Fase 4 — 2026-11-24

Branch `feat/fase4` (sem push, sem deploy).

Site estático em `site/`: uma página PT-BR e EN gerada dos JSON em
`site/content/`, `/pai` como página separada sem link no menu, tema claro/escuro,
acessibilidade básica, robots/sitemap, sem analytics e sem backend. Transcrição
real do demo do SAFE-AI em vez de vídeo inventado.

Como testar:

```
cd /home/admin/PAI/site
npm run build
npm test
# 5 tests pass
```

Pendente: definir `SITE_URL` real antes do sitemap; definir e-mail oficial
(hoje vazio); Lighthouse mobile **não medido** (sem Chrome/Lighthouse na
máquina); publicar é Tier 2 e depende de aprovação.
