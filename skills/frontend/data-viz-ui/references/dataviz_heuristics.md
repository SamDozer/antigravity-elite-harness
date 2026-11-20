# Data Visualization Heuristics & Standards

### 1. Dual Y-Axis Prohibition
Never put two different metrics on opposing left and right Y-axes. Users misattribute trends and assume intersection points have physical meaning. Instead:
- Split into two vertical charts sharing the same synchronized X-axis (e.g. time or genomic coordinate).

### 2. High-Density Tables
- Rows: `32px` height for compact inspection, `44px` for touch screens.
- Alignment: Numbers right-aligned with monospace font features (`font-variant-numeric: tabular-nums;`). Text left-aligned. Status badges centered.
- Sort indicators: Visual arrows on column headers with ARIA sort attributes (`aria-sort="ascending"`).

### 3. Tooltip Architecture
- Never let tooltips jitter or follow the pointer with 0ms delay. Apply a 50ms smooth transition or anchor to the active data bar/point.
- Invert position when near viewport edges (flip above if near bottom; flip left if near right).
