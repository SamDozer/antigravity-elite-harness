---
name: frontend-interaction-states
description: Production component state handling covering loading skeletons, empty zero-data states, optimistic UI rollbacks, accessible error boundaries, keyboard shortcuts, focus rings, and responsive viewport collapse (1440px down to 375px). Use when implementing interactive frontend views, form components, async data-fetching screens, dialogs, and navigation drawers that require comprehensive state resilience. Do NOT use when writing backend business logic, database migrations, CLI tools, or non-visual pipelines.
---

# Frontend Interaction States Skill

Eliminate "happy-path only" bias by enforcing complete coverage across all 5 interaction states: Loading, Empty, Error, Success, and Disabled/Offline.

## The 5 Interaction States

| State | Production Requirement | Anti-Pattern to Avoid |
| :--- | :--- | :--- |
| **Loading** | Content-shaped layout skeleton with subtle pulse; maintain container height. | Full-screen blocking spinners that cause layout shift. |
| **Empty** | Helpful illustration or icon, explanatory copy, and a primary CTA to create the first record. | A blank empty card or silent blank table. |
| **Error** | Actionable error message, inline retry button, preserved user inputs, `role="alert"`. | Generic "Something went wrong" without retry or code. |
| **Success / Optimistic** | Immediate UI update; background sync; automatic rollback on network failure. | Freezing UI for 800ms awaiting server roundtrip. |
| **Focus & Keyboard** | Visible high-contrast focus rings (`:focus-visible`), Escape to close, Tab trapping. | Mouse-only click targets, invisible tab focus. |

## Workflow

### 1. State Matrix Audit
- For every async component, declare state representations for `idle`, `loading`, `empty`, `error`, and `success`.
- Copy or import starter classes from `assets/skeleton_patterns.css`.

### 2. Keyboard & Focus Ergonomics
- Modals, drawers, and popovers MUST trap focus within their container while open.
- Pressing `Escape` must immediately close open overlays and return focus to the trigger element.

### 3. Responsive Collapse Discipline
- Design must reflow gracefully from `1440px` (desktop multi-column) down to `375px` (single-column mobile).
- Ensure no horizontal page scrollbar is triggered at `375px` viewport width.

### 4. Deterministic Coverage Check
- Scan component code for state handlers before opening a PR:
  ```bash
  python skills/frontend/frontend-interaction-states/scripts/check_state_coverage.py --file src/components/DataView.tsx
  ```

## Hard Constraints
- Never discard form inputs when a submission error occurs.
- Screen readers must be notified of async status changes via `aria-live="polite"` or `role="status"`.
