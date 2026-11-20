---
name: web-editorial-design
description: Expressive typography, narrative editorial layout, and orchestrated motion for websites, marketing landing pages, and long-form publications. Use when designing promotional websites, product landing pages, editorial essays, documentation hubs, or marketing hero layouts requiring dramatic typographic scale jumps (3x+ hero-to-body), distinctive serif/grotesque pairings, intentional whitespace, and staggered entrance reveals. Do NOT use when building high-density software dashboards, desktop Electron settings windows, data-entry forms, or scientific workbench tables (use app-ui-system instead).
---

# Web Editorial Design Skill

Create distinctive, high-end editorial layouts and marketing pages that avoid AI-generated visual convergence.

## Core Tenets
- **Dramatic Typographic Scale:** Hero display headlines must feature at least a 3.0x scale jump over body copy (e.g. 56px - 72px display vs. 18px body).
- **Curated Distinctive Pairings:** Pair high-character display typefaces (Editorial Serifs, Sculptural Grotesks) with crisp neutral body copy. Ban generic Space Grotesk + purple-blue gradient clichés.
- **Intentional Negative Space:** Generous vertical rhythm (`80px` to `140px` section margins) allowing ideas room to breathe.
- **Orchestrated Load Motion:** Subtle staggered load entrance animations (100ms - 150ms intervals, 400ms duration, `cubic-bezier(0.16, 1, 0.3, 1)`) rather than hyperactive hover vibrations.

## Workflow

### 1. Typographic Selection
- Consult `references/editorial_pairings.md` to select a display + body combination matching the subject voice.
- Set up fluid type scaling using `clamp()` baselines from `assets/editorial_baseline.css`.

### 2. Reading Ergonomics
- Constrain prose reading containers to `max-width: 65ch` with `line-height: 1.6` to `1.7`.
- Use hanging punctuation or optical alignment on large display quotes.

### 3. Motion Orchestration
- Apply staggered reveal classes from `references/motion_patterns.md`.
- Ensure all keyframe and transition effects are wrapped in `@media (prefers-reduced-motion: no-preference)`.

### 4. Automated Typography & Motion Audit
- Run the typography audit script against your styles:
  ```bash
  python skills/frontend/web-editorial-design/scripts/audit_typography.py --file styles.css
  ```

## Hard Constraints
- Must include `@media (prefers-reduced-motion: reduce)` fallbacks disabling motion.
- Never use pure black (`#000000`) text on pure white (`#ffffff`) paper—use softened charcoal (`#111827` on `#fafaf9`).
