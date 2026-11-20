# Editorial Motion Standards

Editorial motion is orchestrated, calm, and narrative-driven. It guides attention without distracting from reading.

### Rules of Editorial Motion
1. **Staggered Entrance:** Elements enter in a choreographed sequence:
   - Eyebrow label: 0ms delay
   - Headline: 100ms delay
   - Deck paragraph: 200ms delay
   - Action buttons: 300ms delay
2. **Smooth Easing:** Use natural deceleration curves:
   ```css
   transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1); /* expo out */
   ```
3. **Restrained Distance:** Translation distances should be short (`12px` to `24px`), never flying across the whole viewport.
4. **Accessible Disabling:**
   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       transition-duration: 0.01ms !important;
     }
   }
   ```
