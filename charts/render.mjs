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
