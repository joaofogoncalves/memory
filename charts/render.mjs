#!/usr/bin/env node
// CLI to render a chart template to .webp/.png using Playwright.
//
// Usage:
//   node charts/render.mjs --template bar \
//     --data charts/examples/adoption-gap.json \
//     --output charts/out/adoption-gap.webp \
//     --width 1600 --height 900 --scale 2

import { readFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, resolve, extname, isAbsolute } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { chromium } from 'playwright';
import sharp from 'sharp';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const __dirname = dirname(fileURLToPath(import.meta.url));

const argv = yargs(hideBin(process.argv))
  .option('template', { type: 'string', demandOption: true, describe: 'Template name (bar, stat-compare, quadrant, line) or path to .html' })
  .option('data',     { type: 'string', demandOption: true, describe: 'Path to JSON data file' })
  .option('output',   { type: 'string', demandOption: true, describe: 'Output file (.webp or .png)' })
  .option('width',    { type: 'number', default: 1600 })
  .option('height',   { type: 'number', default: 900 })
  .option('scale',    { type: 'number', default: 2, describe: 'deviceScaleFactor (retina)' })
  .option('transparent', { type: 'boolean', default: false, describe: 'Transparent background (drops the dark surface)' })
  .option('no-signature', { type: 'boolean', default: false, describe: 'Skip the logo + URL signature in bottom-right' })
  .strict()
  .parseSync();

function resolvePath(p) {
  return isAbsolute(p) ? p : resolve(process.cwd(), p);
}

function resolveTemplate(name) {
  if (name.endsWith('.html')) return resolvePath(name);
  return resolve(__dirname, 'templates', `${name}.html`);
}

function outputKind(outPath) {
  const ext = extname(outPath).toLowerCase();
  if (ext === '.webp') return 'webp';
  if (ext === '.png')  return 'png';
  throw new Error(`Unsupported output extension: ${ext} (use .webp or .png)`);
}

async function main() {
  const templatePath = resolveTemplate(argv.template);
  const dataPath = resolvePath(argv.data);
  const outPath = resolvePath(argv.output);

  if (!existsSync(templatePath)) throw new Error(`Template not found: ${templatePath}`);
  if (!existsSync(dataPath))     throw new Error(`Data file not found: ${dataPath}`);

  const htmlRaw = await readFile(templatePath, 'utf8');
  const data = JSON.parse(await readFile(dataPath, 'utf8'));

  // Inject window.__DATA__ before any <script> so templates can read it synchronously.
  const injection = `<script>window.__DATA__ = ${JSON.stringify(data).replace(/</g, '\\u003c')};</script>`;
  let html;
  if (htmlRaw.includes('</head>')) {
    html = htmlRaw.replace('</head>', `${injection}</head>`);
  } else {
    html = injection + htmlRaw;
  }

  await mkdir(dirname(outPath), { recursive: true });

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: argv.width, height: argv.height },
    deviceScaleFactor: argv.scale,
  });
  const page = await context.newPage();

  // Base URL so CDN scripts resolve normally.
  await page.setContent(html, { waitUntil: 'networkidle', baseURL: pathToFileURL(templatePath).href });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  // Let Chart.js complete its render pass.
  await page.waitForTimeout(250);

  if (argv.transparent) {
    await page.addStyleTag({ content: `
      html, body { background: transparent !important; }
      #chart-container { background: transparent !important; }
    `});
  }

  if (!argv['no-signature']) {
    const logoPath = resolve(__dirname, '..', 'web', 'img', 'logo.webp');
    const siteUrl = (process.env.SITE_URL || 'joaofogoncalves.com').replace(/^https?:\/\//, '').replace(/\/$/, '');
    let logoDataUrl = '';
    if (existsSync(logoPath)) {
      const buf = await readFile(logoPath);
      logoDataUrl = `data:image/webp;base64,${buf.toString('base64')}`;
    }
    await page.evaluate(({ logoDataUrl, siteUrl }) => {
      const container = document.getElementById('chart-container');
      if (!container) return;
      const cs = getComputedStyle(container);
      if (cs.position === 'static') container.style.position = 'relative';
      const sig = document.createElement('div');
      sig.setAttribute('data-signature', '');
      sig.style.cssText = [
        'position:absolute', 'right:24px', 'bottom:16px',
        'display:flex', 'align-items:center', 'gap:10px',
        'font-family:"Inter",sans-serif', 'font-size:13px',
        'color:#bbc9cc', 'opacity:0.7', 'pointer-events:none',
        'z-index:10',
      ].join(';');
      if (logoDataUrl) {
        const img = document.createElement('img');
        img.src = logoDataUrl;
        img.style.cssText = 'height:20px;width:auto;display:block;';
        sig.appendChild(img);
      }
      const url = document.createElement('span');
      url.textContent = siteUrl;
      url.style.cssText = 'letter-spacing:0.02em;';
      sig.appendChild(url);
      container.appendChild(sig);
    }, { logoDataUrl, siteUrl });
    await page.waitForTimeout(100);
  }

  const container = await page.$('#chart-container');
  if (!container) throw new Error('#chart-container not found in template');

  const kind = outputKind(outPath);
  const pngBuffer = await container.screenshot({ type: 'png', omitBackground: argv.transparent });
  if (kind === 'png') {
    await sharp(pngBuffer).png({ compressionLevel: 9 }).toFile(outPath);
  } else {
    await sharp(pngBuffer).webp({ quality: 95 }).toFile(outPath);
  }

  await browser.close();
  console.log(`✓ Rendered ${outPath}`);
}

main().catch(err => {
  console.error('✗', err.message);
  process.exit(1);
});
