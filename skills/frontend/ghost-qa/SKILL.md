---
name: ghost-qa
description: "Runs autonomous headless Playwright browser QA across Desktop, Tablet, and Mobile viewports to catch hydration, layout overflow, and accessibility bugs. Use when verifying rendered frontend UI pages across responsive viewports on local dev servers. Do NOT use when targeting unauthorized third-party production websites or testing pure backend logic."
source_repo: sickn33/agentic-awesome-skills
risk: safe
---



# Ghost-QA — Autonomous Headless Playwright Browser QA Skill

## Overview

`ghost-qa` is a local headless Playwright browser verification CLI and MCP server that inspects running web applications across Desktop (`1440x900`), Tablet (`768x1024`), and Mobile (`375x812`) viewports. Its 8-Trap Engine detects console exceptions, React/Next.js hydration mismatches, failed network requests (`4xx`/`5xx`), dead interactions, horizontal viewport overflow, bounding-box element collisions, accessibility violations, and dark-mode contrast failures.

## When to Use This Skill

- Use this skill after building or modifying frontend pages, layouts, or interactive components to verify real browser rendering before deployment.
- Use this skill when diagnosing mobile `375px` overflow, overlapping sticky headers, or client-side hydration errors.
- Do not use this skill against third-party production websites without authorization; run it against local development servers (`http://localhost:3000`, `http://localhost:5173`, etc.).

## Prerequisites and side effects

Use an authorized disposable localhost application with test data. The browser can navigate and interact with controls and forms, and the CLI writes reports. Keep production services, credentials, and webhooks disconnected. Review the pinned package and get authorization before installing dependencies or running the browser interactions. Install Chromium separately if required, following the upstream setup guide.

## Workflow & Commands

### 1. Run Autonomous Multi-Viewport Browser QA

~~~bash
npx -y ghost-qa@2.1.2 test http://localhost:3000 --out-dir ghost-qa-out
~~~

### 2. Inspect Findings & Health Score

- Review the generated `0-100` QA Health Score, per-viewport trap breakdown, and `report.html` artifact.
- Fix any reported `scrollWidth > clientWidth` overflow, bounding-box overlaps, console errors, or missing ARIA labels.

### 3. Re-Verify Fix

~~~bash
npx -y ghost-qa@2.1.2 test http://localhost:3000 --out-dir ghost-qa-out
~~~

## Verification Checklist

1. Confirm `ghost-qa` reports 0 uncaught console/page errors and 0 hydration mismatches.
2. Confirm Desktop (`1440x900`), Tablet (`768x1024`), and Mobile (`375x812`) viewports have zero horizontal overflow or overlapping interactive elements.

## Examples

For a disposable local dashboard with a mobile overflow report, run the viewport check, inspect the first overflow finding in the HTML report, then rerun after correcting the responsible component.

## Limitations

- An automated crawl cannot establish coverage of signed-in flows or accessibility conformance.
- The interaction filter cannot guarantee that a control is harmless. Restrict the run to a disposable fixture even when a button appears safe.
- Browser artifacts may contain application content. Review them before sharing.

## Sources

- [Ghost-QA project and setup](https://github.com/avivgerz-hue/ghost-qa)

## Local Responsive Pre-Check
Run `scripts/check_responsive_css.py` using `assets/viewports.config.json` and consult `references/eight_trap_engine.md`.

## Local Responsive Pre-Check
Run `scripts/check_responsive_css.py` using `assets/viewports.config.json` and consult `references/eight_trap_engine.md`.
