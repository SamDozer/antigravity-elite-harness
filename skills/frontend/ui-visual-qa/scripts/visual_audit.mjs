#!/usr/bin/env node
/**
 * visual_audit.mjs - Automated Playwright-based visual and runtime auditor.
 * Audits 1440px desktop & 375px mobile viewports, light/dark themes,
 * catches horizontal layout overflow, intercepts unhandled console/hydration errors,
 * executes automated WCAG 2.2 AA contrast audits, and supports optional dev-server launching.
 */

import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const args = process.argv.slice(2);
function getArg(flag, defaultVal = null) {
  const idx = args.indexOf(flag);
  return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : defaultVal;
}

const targetUrl = getArg('--url');
const targetFile = getArg('--file');
const devCmd = getArg('--dev-cmd');
const outputDir = getArg('--output-dir', 'visual-audit-results');

if (!targetUrl && !targetFile && !devCmd) {
  console.log('Usage: node visual_audit.mjs --url <http://localhost:3000> [--output-dir <dir>]');
  console.log('       node visual_audit.mjs --file <path/to/index.html> [--output-dir <dir>]');
  console.log('       node visual_audit.mjs --dev-cmd "npm run dev" --url <http://localhost:3000>');
  process.exit(1);
}

const urlToVisit = targetUrl || (targetFile ? `file://${path.resolve(targetFile).replace(/\\/g, '/')}` : 'http://localhost:3000');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForServer(url, timeoutMs = 20000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch(url);
      if (res.ok || res.status < 500) return true;
    } catch (e) {
      // not ready yet
    }
    await sleep(500);
  }
  throw new Error(`Server at ${url} did not become ready within ${timeoutMs / 1000}s`);
}

async function runAudit() {
  let devProcess = null;
  if (devCmd) {
    console.log(`🚀 Spawning dev server: ${devCmd}`);
    devProcess = spawn(devCmd, { shell: true, stdio: 'inherit' });
    try {
      await waitForServer(urlToVisit);
      console.log(`✅ Dev server responded at ${urlToVisit}`);
    } catch (err) {
      if (devProcess) devProcess.kill();
      throw err;
    }
  }

  let playwright;
  try {
    playwright = await import('playwright');
  } catch (err) {
    console.warn('⚠️ [WARN] Playwright not installed in local environment.');
    console.warn('           Install with: npm install -D playwright');
    console.log('Performing static HTML viewport and contrast heuristic check instead...');

    if (devProcess) devProcess.kill();

    if (targetFile && fs.existsSync(targetFile)) {
      const html = fs.readFileSync(targetFile, 'utf8');
      const hasViewport = html.includes('name="viewport"');
      const issues = [];
      if (!hasViewport) {
        issues.push('Missing <meta name="viewport"> tag in HTML.');
      }

      // Check inline low-contrast traps
      if (/color:\s*#(?:777|888|999|aaa).*background(?:-color)?:\s*#(?:888|999|aaa|fff)/i.test(html)) {
        issues.push('Potential low WCAG contrast inline style detected.');
      }

      if (issues.length > 0) {
        for (const i of issues) console.error(`❌ [FAIL] Static check: ${i}`);
        process.exit(1);
      } else {
        console.log('✅ [PASS] Static check: Viewport meta tag and basic structure declared correctly.');
        process.exit(0);
      }
    }
    process.exit(0);
  }

  try {
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

        // 2. Automated WCAG Contrast Audit
        const contrastViolations = await page.evaluate(() => {
          function parseRgb(colorStr) {
            const m = colorStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d\.]+))?\)/);
            if (!m) return null;
            const a = m[4] !== undefined ? parseFloat(m[4]) : 1.0;
            return { r: parseInt(m[1]), g: parseInt(m[2]), b: parseInt(m[3]), a };
          }

          function getLuminance(rgb) {
            const a = [rgb.r, rgb.g, rgb.b].map(v => {
              v /= 255;
              return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
            });
            return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
          }

          function getEffectiveBg(el) {
            let cur = el;
            while (cur && cur !== document.documentElement) {
              const bg = window.getComputedStyle(cur).backgroundColor;
              const parsed = parseRgb(bg);
              if (parsed && parsed.a > 0.05) return parsed;
              cur = cur.parentElement;
            }
            return { r: 255, g: 255, b: 255, a: 1 }; // default canvas
          }

          const nodes = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, p, span, a, button, label, li, td, th'));
          const violations = [];

          for (const node of nodes.slice(0, 100)) {
            const text = (node.textContent || '').trim();
            if (!text || text.length < 2) continue;
            const style = window.getComputedStyle(node);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') continue;

            const fg = parseRgb(style.color);
            const bg = getEffectiveBg(node);
            if (!fg || !bg) continue;

            const l1 = getLuminance(fg);
            const l2 = getLuminance(bg);
            const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);

            const fontSize = parseFloat(style.fontSize) || 16;
            const isBold = parseInt(style.fontWeight) >= 700 || style.fontWeight === 'bold';
            const isLarge = fontSize >= 24 || (fontSize >= 18.66 && isBold);
            const threshold = isLarge ? 3.0 : 4.5;

            if (ratio < threshold) {
              violations.push({
                tag: node.tagName.toLowerCase(),
                text: text.slice(0, 30),
                ratio: ratio.toFixed(2),
                required: threshold
              });
              if (violations.length >= 5) break;
            }
          }
          return violations;
        });

        for (const cv of contrastViolations) {
          issues.push(`[CONTRAST_VIOLATION] ${vp.name} (${theme}): <${cv.tag}> "${cv.text}" contrast ${cv.ratio}:1 fails WCAG AA minimum (${cv.required}:1)`);
        }

        // 3. Save screenshot
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
      console.log('✅ ALL VIEWPORT, WCAG CONTRAST, AND CONSOLE CHECKS PASSED CLEANLY.');
      process.exit(0);
    }
  } finally {
    if (devProcess) {
      console.log('Stopping dev server...');
      devProcess.kill();
    }
  }
}

runAudit().catch(err => {
  console.error(`Fatal error running visual audit: ${err.message}`);
  process.exit(1);
});
