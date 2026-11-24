import test, { before } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const run = promisify(execFile);
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

before(async () => {
  await run(process.execPath, ['scripts/build.mjs'], { cwd: ROOT });
});

async function read(rel) {
  return readFile(join(ROOT, 'dist', rel), 'utf8');
}

test('PT and EN pages are generated from JSON content', async () => {
  const pt = await read('index.html');
  const en = await read('en/index.html');
  const cPt = JSON.parse(await readFile(join(ROOT, 'content/site.pt.json'), 'utf8'));
  const cEn = JSON.parse(await readFile(join(ROOT, 'content/site.en.json'), 'utf8'));
  assert.ok(pt.includes(cPt.hero.title));
  assert.ok(en.includes(cEn.hero.title));
  assert.ok(pt.includes('lang="pt-BR"'));
  assert.ok(en.includes('lang="en"'));
});

test('hidden PAI page exists and is not in the main navigation', async () => {
  const pai = await read('pai/index.html');
  const home = await read('index.html');
  assert.ok(pai.includes('PAI — Purple Agentic Intelligence'));
  assert.ok(!home.includes('/pai/'));
});

test('no invented audit price and no compliance guarantee', async () => {
  const home = await read('index.html');
  assert.ok(home.includes('Valor definido no escopo'));
  assert.ok(!home.includes('garante conformidade'));
  assert.ok(home.includes('R$ 397'));
});

test('static files, robots and sitemap exist', async () => {
  assert.ok((await read('styles.css')).includes('prefers-color-scheme'));
  assert.ok((await read('app.js')).includes('pai-theme'));
  assert.ok((await read('robots.txt')).includes('Sitemap: sitemap.xml'));
  assert.ok((await read('sitemap.xml')).includes('<urlset'));
  assert.ok((await read('demo-transcript.txt')).includes('ASK_HUMAN'));
});

test('no third-party tracking scripts', async () => {
  const home = await read('index.html');
  assert.ok(!home.includes('googletagmanager'));
  assert.ok(!home.includes('gtag'));
});
