# Visual QA Verification Checklist

Before approving any UI deliverable, verify that all items pass on the rendered page:

- [ ] **No Mobile Horizontal Scroll:** At 375px width, the page horizontal scrollbar does not exist.
- [ ] **Zero Console Exceptions:** DevTools console has 0 unhandled exceptions or React hydration mismatch warnings.
- [ ] **Touch Target Sizing:** Interactive buttons and links meet at least 44x44px clickable area on mobile.
- [ ] **Accessible Focus Indication:** Pressing `Tab` reveals visible high-contrast focus rings around all interactive elements.
- [ ] **Dark & Light Mode Parity:** Text remains readable with >= 4.5:1 contrast in both color schemes; no unreadable white-on-white or dark-on-dark blocks.
- [ ] **No Content Clipping:** Long labels or localized text strings do not get truncated or overflow outside their containers.
