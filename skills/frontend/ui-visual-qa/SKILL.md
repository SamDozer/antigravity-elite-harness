---
name: ui-visual-qa
description: Closed-loop browser verification and visual quality assurance using Playwright. Use when testing rendered web interfaces, Electron desktop renderers, and responsive layouts across viewports (1440px desktop, 375px mobile) in light and dark modes, detecting horizontal layout overflows, capturing screenshot artifacts, and catching unhandled console/hydration errors. Do NOT use when verifying pure headless backend APIs, database schemas, non-visual scripts, or reviewing computational biology code.
---

# UI Visual QA Skill (Closed-Loop Browser Verification)

Claude-grade UI confidence requires inspecting the actual rendered browser surface rather than trusting prompt checklists.

## Verification Vectors Checked
1. **Layout Overflow:** Detects whether `document.documentElement.scrollWidth > window.innerWidth` at mobile width (375px).
2. **Hydration & Console Errors:** Catches unhandled JavaScript exceptions, React hydration mismatches, and failed resource loads.
3. **Viewport Matrix:** Captures screenshots across Desktop (`1440x900`) and Mobile (`375x812`) in both light and dark modes.
4. **Z-Index & Clipping:** Visually surfaces clipped modal dialogs, misplaced tooltips, and overlapping buttons.

## Workflow

### 1. Launch Dev / Static Server
Ensure the application is running locally:
```bash
npm run dev
# or: npx serve -p 3000 dist/
```

### 2. Execute Automated Visual Audit
Run the Playwright visual audit tool:
```bash
node skills/frontend/ui-visual-qa/scripts/visual_audit.mjs --url http://localhost:3000 --output-dir audit-artifacts/
```

### 3. Review Rendered Artifacts
Inspect the generated screenshot images in `audit-artifacts/`:
- `desktop-dark.png`
- `desktop-light.png`
- `mobile-dark.png`
- `mobile-light.png`

### 4. Consult Quality Checklist
- Verify against criteria in `references/qa_checklist.md` before approving or submitting a pull request.

## Hard Constraints
- Any unhandled React hydration error or uncaught console exception is a blocking failure.
- A horizontal scrollbar on mobile (375px) is an automatic failure.
