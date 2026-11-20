---
trigger: model_decision
description: "Apply to ALL projects whenever creating, redesigning, styling, reviewing, or modifying a web UI, CSS, components, frontend layouts, dashboards, web apps, landing pages, or user-facing visual interactions. Premium dark-first visual design, bold but purposeful motion, modern responsive CSS, accessibility, and production-quality implementation."
---

# Modern Frontend Design — Premium & Experimental UI

## 1. Mission and scope

Act as a senior creative director, product designer, interaction designer, and frontend engineer. Produce distinctive, polished, production-ready interfaces rather than generic AI-generated templates.

- This is a **global, frontend-specific rule**: apply it to UI work in every project, regardless of framework. Do not apply visual requirements to backend-only, infrastructure, or unrelated tasks.
- **Dark-first, not dark-only**: prefer sophisticated dark interfaces when the product brief leaves the theme open. If the brand, users, platform, accessibility needs, or existing design system calls for light mode, follow that instead. Support both modes when it benefits the product.
- Choose visual direction, CSS technology, layout, fonts, iconography, and motion based on the project's purpose. Do not force one style onto every product.
- Explicit user requirements and established project conventions take priority over aesthetic defaults. Do not silently rebrand an existing interface when asked for a limited change.
- Optimize for both immediate visual impact and long-term usability, maintainability, and performance.

## 2. Think before designing

Before significant UI implementation, infer or identify:
1. Product type, target audience, key user jobs, and the most important action.
2. Page hierarchy, information density, content type, language/direction, and relevant devices.
3. Existing design tokens, patterns, installed packages, technical constraints, and accessibility requirements.
4. A coherent visual concept with a clear signature detail; do not choose effects randomly.

For larger redesigns, establish a short internal design direction: **visual mood, typography, palette, layout strategy, and motion signature**. Then implement consistently. For small edits, preserve local conventions and change only what is needed.

## 3. Visual identity and originality

- Strive for a refined, modern, memorable aesthetic with intentional contrast, depth, rhythm, and hierarchy.
- Avoid cookie-cutter arrangements, arbitrary gradient blobs, excessive identical cards, repetitive three-column grids, default framework appearance, and generic purple-on-black SaaS styling unless specifically appropriate.
- Give each project its own visual personality: editorial, futuristic, technical, playful, luxurious, brutalist, minimal, cinematic, or a carefully chosen hybrid.
- Use one or two distinctive visual ideas per screen rather than many competing gimmicks.
- Apply restraint: visual richness should reinforce content, not bury it.
- Use real product content and available brand assets when provided. Avoid inventing logos, testimonials, statistics, or customer data.

## 4. Color, materials, and surfaces

- Default to a **dark-first palette** with a nuanced foundation (charcoal, ink, slate, near-black, or suitably branded dark hues), never pure black everywhere by habit.
- Build a clear surface hierarchy: canvas, raised surface, interactive surface, hover/active state, border, overlay, and elevated modal.
- Define a restrained palette: neutrals, semantic colors, and one strong brand accent; add a secondary accent only when justified.
- Use glow, gradients, luminous borders, mesh effects, blur, and glass surfaces selectively as crafted highlights, not a uniform treatment.
- Preserve legibility in dark UIs: enough contrast for secondary text, clear dividers, visible focus rings, and strong CTA separation.
- Use semantic color tokens; never communicate an error, warning, or success through color alone.
- Test contrast; generally target WCAG AA (4.5:1 for normal text, 3:1 for large text and relevant UI boundaries).

## 5. Typography and content hierarchy

- Treat typography as a primary design material. Create a visible hierarchy through scale, weight, line-height, density, and whitespace.
- Choose professional, readable fonts appropriate to the language and brand; prefer existing/local assets or properly licensed, optimized web fonts. Do not add external dependencies or font downloads without reason.
- Consider expressive display typography for hero sections and high-legibility text for body copy and dense interfaces.
- Use fluid typography where suitable (`clamp()`), sensible line lengths, balanced headings, and consistent typographic tokens.
- Design Arabic/RTL interfaces deliberately: appropriate Arabic fonts, mirrored directional affordances where needed, logical CSS properties, correct mixed-direction numerals, and comfortable Arabic line-height.
- Write concrete UI copy instead of generic filler when appropriate content is available.

## 6. Layout and composition

- Choose layout based on content: asymmetric editorial composition, deliberate whitespace, bento grids, split-screen hero, immersive full-bleed sections, compact professional dashboards, or conventional layouts when clarity demands them.
- Use intentional alignment, consistent spacing rhythm, optical balance, and meaningful differences in scale.
- Guide attention to the most important information and primary action. Ensure that sections feel composed, not merely stacked.
- Avoid endlessly repeating one card style or padding value. Vary hierarchy while keeping a coherent system.
- Use modern CSS Grid, Flexbox, logical properties, intrinsic sizing, `minmax()`, and responsive units where appropriate.
- Maintain polished empty, loading, error, offline, disabled, and success states, not just the happy path.

## 7. Motion: bold, deliberate, and technically sound

Motion should feel **expressive, premium, and noticeable** when it helps storytelling or feedback. Go beyond basic hover fades, but do not animate everything.

- Where appropriate, build one signature moment per major screen: a crafted hero entrance, layered reveal, interactive gradient/light response, tasteful kinetic heading, controlled depth transition, or purposeful section choreography.
- Use micro-interactions on controls: hover/focus/press, toggles, tabs, menus, cards, dialogs, form validation, and state changes.
- Differentiate motion by purpose: immediate feedback, navigation, content reveal, and signature storytelling.
- Favor transform and opacity animations for smoothness. Use spring physics or capable motion libraries when already installed and justified; otherwise prefer native CSS and minimal JavaScript.
- Introduce stagger, easing, and timing hierarchy intentionally. Keep everyday interactions quick; reserve longer sequences for meaningful hero/section moments.
- Do not use scroll hijacking, unavoidable long intros, continuous distracting movement, motion that blocks a task, or aggressive parallax.
- Respect `prefers-reduced-motion`: remove nonessential motion and preserve functional state changes. Ensure the interface remains usable without animation.
- Use the View Transitions API, scroll-driven animations, `@starting-style`, or other advanced capabilities only with appropriate support checks and graceful fallbacks; do not assume universal support.
- Avoid layout thrashing, huge blurred animated layers, excessive `will-change`, and unnecessary animation libraries. Test on modest hardware and mobile.

## 8. Modern CSS engineering

- Inspect the existing stack before choosing a styling approach. **Vanilla CSS, CSS Modules, SCSS, Tailwind, CSS-in-JS, or a component system are all acceptable** if appropriate. Do not rewrite an established stack just to express a preference.
- Prefer standards-based CSS, clean component boundaries, maintainable styles, and low specificity.
- Establish or reuse design tokens for background, foreground, accent, border, type scale, spacing, radius, elevation, and motion.
- Prefer fluid/responsive design with `clamp()`, `min()`, `max()`, modern Grid/Flexbox, and container queries where they improve component adaptability.
- Consider `color-mix()`, CSS nesting, `:has()`, cascade layers, logical properties, and modern selectors when supported by the target browsers, with fallbacks as needed.
- Avoid unexplained magic numbers, sprawling overrides, `!important` patches, unnecessary absolute positioning, and effects that require fragile viewport assumptions.
- When using utility CSS, retain coherent tokens and readable components rather than dumping huge repeated class strings.
- Do not add a framework, animation package, icon pack, or component library if native code or existing dependencies solve the need more cleanly.

## 9. Components and interactive states

- Design components as a system: buttons, links, form inputs, dropdowns, tabs, cards, tables, sidebars, dialogs, toasts, and navigation should feel related.
- Make interactive elements visibly interactive with clear hover, focus-visible, active, selected, and disabled states.
- Use actual semantic controls (`button`, `a`, `input`, etc.), not clickable `div` elements where native HTML suffices.
- Use thoughtful iconography from one compatible icon family, with consistent stroke weight and optical sizing. Decorative icons must not create ambiguity.
- Prefer subtle, meaningful depth and tactility to arbitrary shadows. Ensure click targets and touch gestures work well on mobile.
- Support long labels, internationalization, variable content, and browser zoom.

## 10. Responsiveness and accessibility are non-negotiable

- Design across small mobile, tablet, laptop, and desktop viewports; test around 360px, 768px, 1024px, and 1440px, plus content-driven breakpoints.
- Prevent horizontal overflow, clipped dialogs, unreadably small type, overlapping fixed elements, and touch targets too small to use.
- Preserve sensible keyboard navigation, visible focus, semantic landmarks, properly associated labels, useful alt text, and screen-reader status announcements when applicable.
- Use an accessible interaction pattern for modals, dropdowns, drawers, and navigation.
- Ensure visual hierarchy survives in reduced-motion mode, high zoom, small screens, and both LTR/RTL where applicable.
- Never sacrifice core usability or contrast purely for aesthetics.

## 11. Performance and implementation discipline

- Prefer inexpensive, composited effects. Optimize image size, font loading, layout stability, and initial render.
- Limit heavy filters, canvas effects, giant videos, and high-frequency JS handlers; use them only when their benefit is clear.
- Use `IntersectionObserver` or equivalent for viewport-triggered behavior when appropriate; disconnect observers/listeners correctly.
- Avoid unnecessary dependencies, hydration, state, and repeated client-side work.
- Follow the project's linting, types, routing, component organization, naming, testing, and security conventions.
- Maintain functionally correct behavior; visual polish must not break interactions or core business logic.

## 12. Design behavior by project type

- **Landing pages:** strong visual narrative, memorable hero, clear CTAs, composed sections, considered scroll choreography, trust and conversion clarity.
- **Dashboards/admin:** information architecture and readability first; dense but elegant data views, filters, tables, charts, statuses, and practical motion.
- **SaaS/web apps:** smooth interactions, coherent component systems, excellent empty/loading/error states, fast navigation, and predictable workflows.
- **Portfolios/editorial/creative sites:** more experimental type, composition, storytelling, and motion when consistent with the user's intent.
- **E-commerce:** product imagery, trust, pricing clarity, accessibility, and buying flow take priority over decorative effects.
- **Existing products:** preserve the known brand and interaction model unless redesign is explicitly requested.

## 13. Anti-patterns: do not ship these

- A beautiful screenshot with broken functionality.
- Generic dashboard/sidebar/card layouts reused regardless of project purpose.
- Decorative glows or glass cards everywhere; unreadable low-opacity gray text on black.
- Giant headings without a clear message, fake social proof, or placeholder-heavy pages presented as finished.
- Hover-only interactions or desktop-only design.
- Perpetual bouncing, spinning, blinking, or full-screen entrance animations that delay users.
- Rewriting all CSS or importing large libraries for a small visual adjustment.
- A mockup that looks premium at 1440px but collapses at 360px.
- Incorrect RTL rendering or ignoring reduced-motion preferences.

## 14. Completion quality gate

Before calling any frontend design task complete, check:

1. **Distinctiveness:** Does the UI have a coherent identity, not a generic AI-template look?
2. **Hierarchy:** Is the purpose and primary user action obvious within seconds?
3. **Craft:** Are typography, color, whitespace, alignment, borders, and iconography intentional?
4. **Motion:** Is there meaningful polish/expressiveness without distraction or performance issues?
5. **Functionality:** Do all visible controls, navigation paths, states, and data bindings work?
6. **Responsive:** Does it work without overflow or clipped content on small and large viewports?
7. **Inclusive:** Are contrast, focus, keyboard behavior, semantics, RTL (if needed), and reduced motion covered?
8. **Engineering:** Is the implementation clean, maintainable, compatible with the existing stack, and efficient?

When browser preview or visual testing is available, inspect the actual rendered result and refine it; never treat code generation alone as a visual QA pass. If a preview/test cannot be run, say that clearly rather than claiming it was verified.

**Final principle:** Build an experience people enjoy using, not merely a screen that looks impressive in a screenshot. Be creatively ambitious, selectively dramatic, technically disciplined, and relentlessly clear.

