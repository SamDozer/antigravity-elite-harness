# Ghost-QA 8-Trap Verification Matrix

1. **Console & Page Exceptions:** Uncaught `TypeError`, `ReferenceError`, or unhandled promise rejections.
2. **Hydration Mismatches:** Server vs. client DOM tree divergence in Next.js/React.
3. **Network Failures:** `4xx` or `5xx` responses on critical assets or API calls.
4. **Horizontal Viewport Overflow:** `document.documentElement.scrollWidth > window.innerWidth` at `375px`, `768px`, `1440px`.
5. **Bounding-Box Collisions:** Interactive buttons or sticky headers overlapping sibling controls.
6. **Dead Interactions:** Clickable elements (`button`, `a`) with zero dimensions or obscured hit targets.
7. **Accessibility Violations:** Missing `alt`, unlabeled form inputs, or broken heading hierarchy.
8. **Contrast Failures:** Text or interactive marks falling below WCAG 2.2 AA contrast thresholds.
