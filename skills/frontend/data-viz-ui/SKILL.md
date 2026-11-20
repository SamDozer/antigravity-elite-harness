---
name: data-viz-ui
description: Interactive web data visualization engineering for scientific datasets, genomics tracks, dashboards, and analytics pipelines. Use when building interactive scatter plots, heatmaps, virtualized data tables (>1,000 rows), SVG/Canvas visualizations, zoom/pan tooltips, and client-side SVG/CSV export handlers. Do NOT use when generating static publication-grade 300+ DPI journal figures (use scientific-figures instead) or designing generic static forms.
---

# Data Visualization UI Skill

Build fast, accessible, and high-density web visualizations for complex analytical and scientific datasets.

## Core Rules

1. **The Single-Axis Rule:** Never combine two independent scales onto a single dual-axis chart (e.g. temperature on left Y-axis, pressure on right Y-axis). Split into two stacked synchronized charts.
2. **Colorblind-Safe Palettes:** Categorical colors must lock to entities, never to changing sorted ranks. Use Okabe-Ito or Viridis palettes from `assets/colorblind_palettes.json`.
3. **Mandatory DOM Virtualization:** Any tabular or list view exceeding 1,000 rows must use windowing / virtualization (e.g. TanStack Virtual, clusterize, or Canvas rendering) to prevent DOM node exhaustion.
4. **Ergonomic Tooltips:** Tooltips must feature 50ms debounce, direct pointer tracking with viewport collision detection, and formatted tabular values.
5. **One-Click Export:** Every interactive chart or table must support immediate client-side SVG download and raw data CSV export.

## Workflow

### 1. Palette & Accessibility Setup
- Load verified color palettes from `assets/colorblind_palettes.json`.
- Verify at least 3:1 contrast for data marks against the canvas surface.

### 2. High-Performance Rendering Selection
- Under 1,000 data marks: Responsive SVG (`<svg viewBox="...">`).
- 1,000 to 50,000 data marks: HTML5 Canvas (`<canvas>`) with offscreen rendering.
- Over 50,000 data marks: WebGL or Deck.gl GPU rendering.

### 3. Export Integration
- Wire up client-side data export using the utility functions in `scripts/export_viz_helper.js`.

## Hard Constraints
- No dual Y-axes under any circumstance.
- Never hardcode fixed pixel widths on SVGs; always declare responsive `viewBox` attributes.
