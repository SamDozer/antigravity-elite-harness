# Application UI Typography Stacks

Dense software requires maximum legibility at 11px - 14px, exceptional tabular numeral alignment (`tnum`), and distinct punctuation symbols.

### Recommended Stacks

#### 1. Modern Native Clean (Zero Bundle Size)
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```
- **Weights:** 400 (Body), 500 (Labels/Buttons), 600 (Headings/Modals).
- **Features:** `font-feature-settings: "cv02", "cv03", "cv04", "cv11", "tnum";`

#### 2. Geist / Inter Hybrid (Precision SaaS)
- **Primary:** `Geist`, `Inter`, sans-serif
- **Code / Tabular:** `Geist Mono`, `JetBrains Mono`, monospace
- **Body size:** `13px` / `0.8125rem` (Dense dashboards), `14px` / `0.875rem` (General apps)
- **Line height:** `1.4` (Compact lists), `1.5` (Readable text)

#### 3. Technical Monospace Data
```css
font-family: "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;
```
- Ideal for genomic coordinate grids, logs, Hex viewers, and ledger rows.
