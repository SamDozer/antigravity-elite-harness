---
name: scientific-figures
description: Publication-grade scientific figure design and formatting for peer-reviewed journals (Nature, Cell, Science, PNAS). Use when generating static publication plots, vector figures (PDF/SVG), high-resolution rasters (>= 300 DPI), exact column-width figures (85mm single-column, 178mm double-column), colorblind-safe palettes, sample size annotations (n=...), and explicit error bar labeling (SD, SEM, or 95% CI). Do NOT use when designing interactive web dashboard charts (use data-viz-ui instead) or styling web UI components.
---

# Scientific Figures Skill (Publication Grade)

Create journal-ready scientific figures that meet the rigorous standards of Nature, Science, Cell, and PNAS.

## Non-Negotiable Publication Standards

1. **Resolution & Formats:**
   - Vector format (`.pdf` or `.svg`) is mandatory for line plots, bar charts, scatter plots, and schematics.
   - Raster format (`.png` or `.tiff`) for microscopy, heatmaps, or gel blots must be at least **300 DPI** (600 DPI for line art).
2. **Standard Column Widths:**
   - Single column: `85 mm` to `89 mm` (~3.35 to 3.5 inches).
   - 1.5 column: `120 mm` to `130 mm` (~4.7 to 5.1 inches).
   - Double column (full page width): `174 mm` to `183 mm` (~6.85 to 7.2 inches).
3. **Mandatory Sample Size & Error Bar Declarations:**
   - Every figure panel showing statistics MUST state the sample size (e.g., `n = 8 mice per group`).
   - Every error bar MUST be explicitly labeled in the caption and legend (e.g., "Data represent mean ± s.e.m." or "mean ± s.d."). Never display unexplained error bars.
4. **Colorblind-Safe Palettes:**
   - Use Okabe-Ito, Viridis, or Cividis. Never combine pure red and pure green in the same panel for comparison.
5. **Clean Typography:**
   - Arial or Helvetica; 7–8 pt for axis titles, 6–7 pt for tick labels, 8–9 pt bold for panel identifiers (A, B, C).

## Workflow

### 1. Apply Matplotlib Publication Style
Load the stylesheet before generating figures:
```python
import matplotlib.pyplot as plt
plt.style.use('skills/comp-bio/scientific-figures/assets/pub_style.mplstyle')
```

### 2. Dimension Specification
Set figure dimensions to exact journal widths:
```python
# Single column width (85 mm = 3.35 inches), height 3.0 inches
fig, ax = plt.subplots(figsize=(3.35, 3.0))
```

### 3. Automated Figure Verification
Verify resolution and dimensions before submitting:
```bash
python skills/comp-bio/scientific-figures/scripts/check_figure.py --figure figure1.png
```

## Hard Constraints
- Never save figures at the default 72 or 100 DPI.
- Never omit sample size ($n$) annotations.
