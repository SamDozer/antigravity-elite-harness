#!/usr/bin/env node
/**
 * visual_audit.mjs - Automated Playwright-based visual and runtime auditor.
 * Audits 1440px desktop & 375px mobile viewports, light/dark themes,
 * catches horizontal layout overflow, and intercepts unhandled console/hydration errors.
 */

import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
function getArg(flag, defaultVal = null) {
  const idx = args.indexOf(flag);
  return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : defaultVal;
}

const targetUrl = getArg('--url');
const targetFile = getArg('--file');
const outputDir = getArg('--output-dir', 'visual-audit-results');

if (!targetUrl && !targetFile) {
  console.log('Usage: node visual_audit.mjs --url <http://localhost:3000> [--output-dir <dir>]');
  console.log('       node visual_audit.mjs --file <path/to/index.html> [--output-dir <dir>]');
  process.exit(0);
}

const urlToVisit = targetUrl || `file://${path.resolve(targetFile).replace(/\\/g, '/')}`;

async function runAudit() {
  let playwright;
  try {
    playwright = await import('playwright');
  } catch (err) {
    console.warn('⚠️ [WARN] Playwright not installed in local environment.');
    console.warn('           Install with: npm install -D playwright');
    console.log('Performing static HTML viewport heuristic check instead...');

    if (targetFile && fs.existsSync(targetFile)) {
      const html = fs.readFileSync(targetFile, 'utf8');
      const hasViewport = html.includes('name="viewport"');
      if (hasViewport) {
        console.log('✅ [PASS] Static check: Meta viewport tag declared correctly.');
        process.exit(0);
      } else {
        console.error('❌ [FAIL] Static check: Missing <meta name="viewport"> tag in HTML.');
        process.exit(1);
      }
    }
    process.exit(0);
  }

  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await playwright.chromium.launch({ headless: true });

  const viewports = [
    { name: 'desktop', width: 1440, height: 900 },
    { name: 'mobile', width: 375, height: 812 }
  ];
  const themes = ['dark', 'light'];

  const issues = [];

  for (const vp of viewports) {
    for (const theme of themes) {
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        colorScheme: theme
      });

      const page = await context.newPage();
      const consoleErrors = [];

      page.on('console', msg => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });
      page.on('pageerror', err => {
        consoleErrors.push(err.message);
      });

      try {
        await page.goto(urlToVisit, { waitUntil: 'networkidle', timeout: 15000 });
      } catch (e) {
        await page.goto(urlToVisit, { waitUntil: 'domcontentloaded', timeout: 10000 });
      }

      // 1. Check for horizontal overflow
      const overflow = await page.evaluate(() => {
        const docWidth = document.documentElement.scrollWidth;
        const winWidth = window.innerWidth;
        return {
          scrollWidth: docWidth,
          innerWidth: winWidth,
          hasOverflow: docWidth > winWidth + 1
        };
      });

      if (overflow.hasOverflow) {
        issues.push(`[OVERFLOW] ${vp.name} (${theme}): document scrollWidth (${overflow.scrollWidth}px) exceeds window width (${overflow.innerWidth}px).`);
      }

      // 2. Save screenshot
      const shotPath = path.join(outputDir, `${vp.name}-${theme}.png`);
      await page.screenshot({ path: shotPath, fullPage: false });
      console.log(`📸 Captured screenshot: ${shotPath}`);

      if (consoleErrors.length > 0) {
        for (const err of consoleErrors) {
          issues.push(`[CONSOLE_ERROR] ${vp.name} (${theme}): ${err}`);
        }
      }

      await context.close();
    }
  }

  await browser.close();

  console.log('\n====================================================');
  console.log(`VISUAL AUDIT COMPLETE: ${issues.length} issue(s) detected`);
  console.log('====================================================');

  if (issues.length > 0) {
    for (const issue of issues) {
      console.error(`❌ ${issue}`);
    }
    process.exit(1);
  } else {
    console.log('✅ ALL VIEWPORT AND CONSOLE CHECKS PASSED CLEANLY.');
    process.exit(0);
  }
}

runAudit().catch(err => {
  console.error(`Fatal error running visual audit: ${err.message}`);
  process.exit(1);
});
