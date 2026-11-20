---
trigger: always_on
description: "Mandatory adaptive and responsive UI standards for every website, web app, dashboard, and Electron desktop interface the agent designs or modifies."
---

# Global Rule — Adaptive, Responsive & Window-Aware UI

## Mission / Non-negotiable outcome
Every user interface you create or modify MUST automatically adapt to the actual space and interaction mode available to the user. A beautiful design at one reference resolution is NOT a finished design. It must remain usable, legible, visually balanced, and functional when the viewport, Electron window, browser zoom, device orientation, text size, or input method changes.

Apply this rule to **all user-facing UI work**, including web pages, websites, landing pages, dashboards, portals, admin tools, Electron renderers, forms, dialogs, navigation, and individual components. It applies to UI design/review tasks; do not force UI work into backend-only tasks.

This rule is **independent of visual style**. Respect the project's brand and the existing global modern-CSS rule (including its dark-first preference and expressive animation guidance). Responsiveness is mandatory whether the chosen style is futuristic, minimal, editorial, playful, or anything else.

## 1 — Design for the available space, not for one screen
- Start mobile-first where appropriate, but determine adaptations from **content and available space**, not assumptions about a specific device or brand.
- Use flexible Grid/Flex layouts, intrinsic sizing, `minmax()`, `auto-fit`/`auto-fill`, `clamp()`, relative units, and modern container queries where supported and useful.
- Prefer component/container queries for reusable cards, panels, and widgets; use viewport media queries for page-level changes.
- Use content-driven breakpoints. Typical reference widths (not hard-coded universal breakpoints): 320, 360, 390, 430, 768, 1024, 1280, 1440, and 1920 CSS pixels.
- Use a fluid maximum content width where appropriate; on ultrawide screens, avoid both endless stretched text and tiny centered interfaces with wasted space.
- Make typography, spacing, imagery, controls, and grid density scale appropriately. Keep readable line lengths and text hierarchy. Preserve adequate tap targets and contrast.
- Reflow first; resize second; scroll within a component only if it is the right semantic interaction. **Never** shrink the entire interface with CSS transforms or browser zoom as a substitute for real adaptation.
- Avoid arbitrary fixed widths/heights, fragile absolute positioning, and `100vw`-based overflow. Use `min-width: 0` on flex/grid children when needed and account for overflow deliberately.

## 2 — Adapt the layout meaningfully
- **Compact/narrow:** prioritize primary content; stack columns and cards; transform sidebars into accessible drawers, tabs, or compact navigation; make forms single-column when needed; keep key actions reachable.
- **Medium/tablet:** use available width intelligently; allow two-column regions and context-aware navigation without cramped cards.
- **Large/desktop:** use multi-column layouts, persistent contextual navigation, and useful information density while preserving rhythm, whitespace, and hierarchy.
- **Ultrawide:** constrain reading areas and thoughtfully expand workspaces, charts, or supporting panels rather than stretching everything.
- For data-heavy dashboards, choose context-aware alternatives for wide tables (responsive columns, card representations, controlled horizontal table scrolling with discoverability, or detail views). Never silently discard essential data or actions on mobile.
- Menus, popovers, tooltips, dropdowns, dialogs, date pickers, toasts, side panels, and command palettes must reposition, fit, scroll, or change presentation based on available room; prevent content from being clipped offscreen.
- Images, video, illustrations, code blocks, tables, and charts must not break their containers. Adapt chart legends, labels, axis density, and controls; preserve useful meaning.
- Responsive changes must remain aesthetically intentional, not merely technically fit within the screen.

## 3 — Electron and resizable desktop windows
- An Electron app is NOT exempt from responsive design just because it targets Windows.
- Design for maximized, restored, half-screen/snapped, and narrow resized windows. Use the **renderer viewport/container dimensions** for decisions; do not infer layout solely from physical monitor size.
- Reflow navigation, toolbars, master/detail panes, grids, and dialogs as the window changes. If the user narrows the window, transition to a compact layout rather than hiding buttons under a sidebar or clipping content.
- Recommend a reasonable `minWidth` / `minHeight` only when product requirements justify it; do not hide poor layout behind an unnecessarily large minimum window.
- Handle Windows display scaling/high DPI and multiple monitors using CSS-pixel-based responsive logic, not fragile physical-pixel guesses.
- Ensure custom title bars, draggable regions, window controls, and application menus remain accessible after resizing; draggable areas must not consume interactive controls.
- Prefer independent scrollable content regions where appropriate, without accidental nested-scroll traps or cut-off bottom actions.

## 4 — Interaction, orientation, zoom, and accessibility
- Support mouse, touch, trackpad, keyboard navigation, and focus indication. Avoid hover-only critical interactions; use input-capability queries when needed.
- Consider portrait/landscape transitions, mobile safe areas, onscreen keyboards, browser chrome, and viewport height changes. Use modern viewport units such as `dvh` / `svh` thoughtfully, with fallbacks where required.
- Ensure focusable actions remain reachable and dialogs usable with keyboard and screen-reader semantics.
- Respect `prefers-reduced-motion`. Expressive animation may enhance presentation but must never block actions, obscure content, or prevent use at smaller viewports and weaker devices.
- Support long labels, user-generated text, localization, and Arabic RTL where applicable. Do not hardcode text dimensions or positioning dependent on English-only labels.
- Aim for WCAG 2.2 AA usability where practical. Verify readability at 200% browser zoom and increased system text scaling; avoid fixed containers that clip enlarged text.
- The layout must not introduce unintended page-level horizontal scrolling at typical narrow viewport widths. Intentional scroll regions (e.g., rich data tables) must be obvious and operable.

## 5 — Implementation choices
- Respect the repository's framework and styling conventions. Use CSS, CSS Modules, Tailwind, SCSS, styled components, etc. as appropriate; do NOT introduce a new framework just for responsiveness.
- Define consistent design tokens for fluid spacing, sizing, radii, typography, and component constraints when the project structure benefits from them.
- Prefer native CSS capabilities before adding JavaScript resize listeners. Use `ResizeObserver` only where true component measurement is needed, with proper cleanup and no resize feedback loops.
- Do not use JavaScript to check device model, user agent, or screen width when CSS can solve the problem.
- Avoid layout shift, hydration mismatch, expensive continuous reflows, and resize-triggered animation storms.
- Keep breakpoint and adaptation logic maintainable and reusable rather than scattering conflicting magic numbers.

## 6 — Required quality gate before declaring UI work complete
For every substantial UI creation or layout change, verify as many of these conditions as the available tooling allows:

1. **Viewport widths:** 320 / 375 / 430 / 768 / 1024 / 1440 / 1920 CSS px (or a representative subset justified by the component).
2. **Electron:** maximized, restored, and narrow/snapped resize states when applicable.
3. **Height & orientation:** short-height windows and portrait/landscape transitions where applicable.
4. **Content:** long titles, dense lists/tables, empty/error/loading states, and any relevant RTL text.
5. **Controls:** nav, modal, dropdown, tooltip, forms, and charts never cut off essential content or actions.
6. **Accessibility:** keyboard access, visible focus, touch targets, reduced motion, and 200% zoom when testable.
7. **Integrity:** no unintended horizontal page overflow, overlap, unreadably tiny text, clipped content, inaccessible buttons, or broken scrolling.

Use available browser responsive previews, DevTools, screenshots, automated viewport tests, or Electron window resize checks. **Do not claim testing was performed unless it actually was.** If testing is unavailable, state what could not be verified and leave a concrete manual test checklist.

## 7 — Completion standard
Before delivery, mentally ask: **"If the user opens this exact screen in a smaller window, on a bigger monitor, at 200% zoom, or with longer text, does the layout still look designed and remain fully usable?"**

A UI that only looks correct at the screenshot width fails this global rule. Responsiveness and adaptability are default acceptance criteria, never an optional later polish pass.

