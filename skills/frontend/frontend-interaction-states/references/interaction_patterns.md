# Production Interaction State Patterns

### 1. Optimistic UI with Immediate Rollback
When a user toggles a switch or favorites an item:
1. Immediately render the new state in local memory.
2. Dispatch async request to server.
3. If the server returns an error:
   - Rollback local state to previous snapshot.
   - Display a non-blocking toast/banner with retry capability: `role="alert"`.

### 2. Dialog Keyboard Focus Trap
- Store active element reference on open (`document.activeElement`).
- Shift focus to the first interactive field inside the modal.
- Listen for `KeyDown`:
  - `Escape`: Close modal and restore focus to trigger button.
  - `Tab`: If on last element, cycle back to first element; if `Shift+Tab` on first element, cycle to last.

### 3. Accessible Empty States
```html
<div class="empty-state-container" role="region" aria-label="No projects found">
  <svg class="empty-icon" aria-hidden="true" ...></svg>
  <h3 class="empty-title">No projects yet</h3>
  <p class="empty-description">Get started by creating your first analysis project.</p>
  <button class="btn btn-primary">Create Project</button>
</div>
```
