---
name: app-ui-system
description: Dense application UI design system for dashboards, desktop/Electron interfaces, scientific tools, and SaaS consoles. Use when building or styling high-density web or desktop apps, dashboards, workspace tools, settings panels, and data-entry screens requiring restrained typography (400/500 weights) and dark-first tokens. Do NOT use when designing promotional marketing websites, editorial landing pages, or narrative hero sections that need expressive display typography and dramatic scale jumps (use web-editorial-design instead).
---

# App UI System (Dense Apps & Dashboards)

A production design system optimized for high-information-density workspaces, Electron desktop apps, scientific workbenches, and data dashboards.

## Core Design Principles
- **Restrained Density:** Prioritize compact table rows, 28-36px button heights, and crisp 1px borders over cavernous padding.
- **Controlled Typography:** Default to regular (400) and medium (500) font weights. Reserve bold (600/700) strictly for page titles and active KPI counters.
- **Dark-First Elegance:** Deep dark surfaces (`#0a0b0e`, `#12141a`, `#1a1d26`) paired with low-saturation borders (`rgba(255,255,255,0.08)`). Ban acid neon gradients.
- **Deterministic Color Contrast:** Every text mark must meet WCAG 2.2 AA (4.5:1 for normal text, 3:1 for UI borders and large headings).

## Workflow

### 1. Token Initialization
- Import or copy the CSS token baseline from `assets/tokens.css`.
- Select an application palette from `references/palettes.md`.
- Select an appropriate UI font stack from `references/font-pairings.md`.

### 2. Layout & Surface Hierarchy
- Base surface: `var(--bg-canvas)`
- Panel / Sidebar: `var(--bg-surface-1)`
- Card / Popover: `var(--bg-surface-2)`
- Borders: `1px solid var(--border-subtle)`

### 3. Automated Contrast Gate
- Run the deterministic contrast checker on custom color definitions before shipping:
  ```bash
  python skills/frontend/app-ui-system/scripts/check_contrast.py --fg "#94a3b8" --bg "#0f172a"
  ```

## Hard Constraints
- No font weight above 600 in body text or table cells.
- Zero decorative backdrop blurs that degrade FPS on multi-window desktop setups.
- Form controls must feature unambiguous, high-contrast `:focus-visible` outlines.
