import { readFile, writeFile, mkdir, cp } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'dist');
const SITE_URL = (process.env.SITE_URL || '').replace(/\/$/, '');

function esc(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function section(id, title, inner, kicker = '') {
  return `<section id="${esc(id)}" class="section"><div class="wrap">${kicker ? `<p class="kicker">${esc(kicker)}</p>` : ''}<h2>${esc(title)}</h2>${inner}</div></section>`;
}

function linkList(items) {
  return `<ul class="list">${items.map(i => `<li>${esc(i)}</li>`).join('')}</ul>`;
}

function render(c, opts) {
  const base = opts.base || '';
  const other = opts.lang === 'pt' ? '/en/' : '/';
  const otherLabel = opts.lang === 'pt' ? 'English' : 'Português';
  const nav = c.nav.map(i => `<a href="${esc(i.href)}">${esc(i.label)}</a>`).join('');
  const steps = c.how.steps.map((s, i) => `<article class="card"><span class="num">0${i + 1}</span><h3>${esc(s.title)}</h3><p>${esc(s.text)}</p></article>`).join('');
  const plans = c.climara.plans.map(p => `<article class="card"><h3>${esc(p.name)}</h3><p class="price">${esc(p.price)}</p><p class="muted">${esc(c.climara.supportLabel)}: ${esc(p.support)}</p><ul class="list">${p.items.map(i => `<li>${esc(i)}</li>`).join('')}</ul></article>`).join('');
  const limits = c.limits.items.map(i => `<li>${esc(i)}</li>`).join('');
  const milestones = c.research.milestones.map(m => `<li>${esc(m)}</li>`).join('');
  const finance = c.finance.items.map(i => `<div><dt>${esc(i.label)}</dt><dd>${esc(i.value)}</dd></div>`).join('');
  const priceLine = c.audit.priceFrom
    ? `<p class="price">${esc(c.audit.priceLabel)} ${esc(c.audit.priceFrom)}</p>`
    : `<p class="muted">${esc(c.audit.priceEmpty)}</p>`;
  const email = c.contact.email
    ? `<a href="mailto:${esc(c.contact.email)}">${esc(c.contact.email)}</a>`
    : `<span class="muted">${esc(c.contact.emailNote)}</span>`;
  const whatsapp = `<a href="https://wa.me/${esc(c.contact.whatsapp)}">${esc(c.contact.whatsappLabel)}</a>`;
  const canonical = SITE_URL ? `${SITE_URL}${opts.path}` : '';

  return `<!doctype html>
<html lang="${esc(c.lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(c.meta.title)}</title>
<meta name="description" content="${esc(c.meta.description)}">
<meta name="theme-color" content="#0b1410">
<meta property="og:title" content="${esc(c.meta.title)}">
<meta property="og:description" content="${esc(c.meta.description)}">
<meta property="og:type" content="website">
${canonical ? `<link rel="canonical" href="${esc(canonical)}">` : ''}
<link rel="alternate" hreflang="pt-BR" href="${base}/index.html">
<link rel="alternate" hreflang="en" href="${base}/en/index.html">
<link rel="stylesheet" href="${base}/styles.css">
<script src="${base}/app.js" defer></script>
</head>
<body>
<a class="skip" href="#conteudo">${opts.lang === 'pt' ? 'Ir ao conteúdo' : 'Skip to content'}</a>
<header class="site-header"><div class="wrap bar">
<a class="brand" href="${base}/index.html">PAI</a>
<nav aria-label="${opts.lang === 'pt' ? 'Seções' : 'Sections'}">${nav}</nav>
<button id="theme" type="button" aria-label="${opts.lang === 'pt' ? 'Alternar tema' : 'Toggle theme'}">◐</button>
<a class="lang" href="${other}">${esc(otherLabel)}</a>
</div></header>
<main id="conteudo">
<section class="hero"><div class="wrap">
<p class="kicker">${esc(c.hero.eyebrow)}</p>
<h1>${esc(c.hero.title)}</h1>
<p class="lead">${esc(c.hero.subtitle)}</p>
<div class="actions"><a class="btn primary" href="${esc(c.hero.primary.href)}">${esc(c.hero.primary.label)}</a><a class="btn" href="${esc(c.hero.secondary.href)}">${esc(c.hero.secondary.label)}</a></div>
<p class="muted small">${esc(c.hero.note)}</p>
</div></section>
${section('demo', c.demo.title, `<p class="lead">${esc(c.demo.text)}</p><h3>${esc(c.demo.transcriptTitle)}</h3><pre class="terminal">${esc(opts.transcript)}</pre>`)}
${section('como-funciona', c.how.title, `<div class="grid">${steps}</div>`)}
${section('auditoria', c.audit.title, `<p class="lead">${esc(c.audit.intro)}</p>${linkList(c.audit.deliverables)}${priceLine}<a class="btn primary" href="#contato">${esc(c.audit.cta)}</a>`)}
${section('financeiro', c.finance.title, `<p class="lead">${esc(c.finance.text)}</p><p class="muted small">${esc(c.finance.exampleLabel)}</p><dl class="facts">${finance}</dl><p class="muted small">${esc(c.finance.note)}</p>`)}
${section('limites', c.limits.title, `<ol class="limits">${limits}</ol>`)}
${section('pesquisa', c.research.title, `<p class="lead">${esc(c.research.question)}</p><ol class="limits">${milestones}</ol><p class="muted small">${esc(c.research.note)}</p>`)}
${section('climara', c.climara.title, `<p class="lead">${esc(c.climara.text)}</p><div class="grid">${plans}</div>`)}
${section('contato', c.contact.title, `<p>${whatsapp}</p><p>${email}</p><p class="muted small">${esc(c.contact.note)}</p>`)}
</main>
<footer class="site-footer"><div class="wrap"><p>${esc(c.footer.privacy)}</p><p class="muted small">${esc(c.footer.note)}</p></div></footer>
</body></html>`;
}

function renderPai(c, opts) {
  const links = c.pai.links.map(l => `<li><a href="${esc(l.href)}" rel="noopener">${esc(l.label)}</a></li>`).join('');
  return `<!doctype html><html lang="${esc(c.lang)}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(c.pai.title)}</title><meta name="description" content="${esc(c.pai.text)}">
<link rel="stylesheet" href="${opts.base}/styles.css"><script src="${opts.base}/app.js" defer></script>
</head><body><a class="skip" href="#conteudo">Skip</a>
<header class="site-header"><div class="wrap bar"><a class="brand" href="${opts.base}/index.html">PAI</a><button id="theme" type="button">◐</button></div></header>
<main id="conteudo"><section class="hero"><div class="wrap"><p class="kicker">${opts.lang === 'pt' ? 'Pesquisa' : 'Research'}</p><h1>${esc(c.pai.title)}</h1><p class="lead">${esc(c.pai.text)}</p><p class="muted">${esc(c.pai.note)}</p><h2>${esc(c.pai.linksLabel)}</h2><ul class="list">${links}</ul></div></section></main>
<footer class="site-footer"><div class="wrap"><p>${esc(c.footer.privacy)}</p></div></footer>
</body></html>`;
}

function sitemap(paths) {
  const base = SITE_URL || 'https://example.invalid';
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${paths.map(p => `  <url><loc>${base}${p}</loc></url>`).join('\n')}\n</urlset>\n`;
}

async function main() {
  const [pt, en, transcript] = await Promise.all([
    readFile(join(ROOT, 'content', 'site.pt.json'), 'utf8'),
    readFile(join(ROOT, 'content', 'site.en.json'), 'utf8'),
    readFile(join(ROOT, 'content', 'demo-transcript.txt'), 'utf8'),
  ]);
  const cPt = JSON.parse(pt);
  const cEn = JSON.parse(en);
  for (const c of [cPt, cEn]) {
    for (const key of ['meta', 'nav', 'hero', 'demo', 'how', 'audit', 'finance', 'limits', 'research', 'climara', 'contact', 'footer', 'pai']) {
      if (!c[key]) throw new Error(`Missing content key: ${key}`);
    }
  }

  await mkdir(OUT, { recursive: true });
  await mkdir(join(OUT, 'en'), { recursive: true });
  await mkdir(join(OUT, 'pai'), { recursive: true });
  await mkdir(join(OUT, 'en', 'pai'), { recursive: true });

  await writeFile(join(OUT, 'index.html'), render(cPt, { lang: 'pt', base: '', path: '/', transcript }));
  await writeFile(join(OUT, 'en', 'index.html'), render(cEn, { lang: 'en', base: '/en', path: '/en/', transcript }));
  await writeFile(join(OUT, 'pai', 'index.html'), renderPai(cPt, { lang: 'pt', base: '..' }));
  await writeFile(join(OUT, 'en', 'pai', 'index.html'), renderPai(cEn, { lang: 'en', base: '..' }));
  await cp(join(ROOT, 'styles.css'), join(OUT, 'styles.css'));
  await cp(join(ROOT, 'app.js'), join(OUT, 'app.js'));
  await cp(join(ROOT, 'content', 'demo-transcript.txt'), join(OUT, 'demo-transcript.txt'));
  await writeFile(join(OUT, 'robots.txt'), 'User-agent: *\nAllow: /\nSitemap: sitemap.xml\n');
  await writeFile(join(OUT, 'sitemap.xml'), sitemap(['/', '/en/']));

  if (!SITE_URL) console.warn('SITE_URL not set: sitemap uses https://example.invalid placeholder.');
  console.log('site built in dist/');
}

main().catch(err => { console.error(err); process.exit(1); });
