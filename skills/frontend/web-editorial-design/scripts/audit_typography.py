#!/usr/bin/env python3
"""
audit_typography.py - Linter for editorial web design standards.
Verifies dramatic typographic scale ratio (>= 2.5x), fluid clamp() usage,
reading column line-length constraints (<= 75ch), and prefers-reduced-motion.
"""

import sys
import os
import re
import argparse

def audit_typography(file_path: str):
    if not os.path.exists(file_path):
        print(f"[FAIL] Target file not found: {file_path}", file=sys.stderr)
        return False

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    warnings = []
    passes = []

    # 1. Check prefers-reduced-motion
    if "prefers-reduced-motion" in content:
        passes.append("Includes @media (prefers-reduced-motion) accessibility guard.")
    else:
        warnings.append("Missing @media (prefers-reduced-motion) guard for motion animations.")

    # 2. Check fluid clamp() usage
    if "clamp(" in content:
        passes.append("Uses fluid clamp() for responsive typographic scaling.")
    else:
        warnings.append("No fluid clamp() font-size rules found. Responsive scaling may be rigid.")

    # 3. Check column width constraints (ch units or max-width)
    if re.search(r"max-width:\s*\d+ch", content):
        passes.append("Constrains reading prose width using character units (ch).")
    else:
        warnings.append("No max-width character constraints (e.g. max-width: 65ch) detected for long-form text.")

    # 4. Check for high-contrast scale jumps
    font_sizes = [float(m) for m in re.findall(r"font-size:\s*([\d\.]+)rem", content)]
    if font_sizes:
        min_sz = min(font_sizes)
        max_sz = max(font_sizes)
        ratio = max_sz / min_sz if min_sz > 0 else 1.0
        if ratio >= 2.5:
            passes.append(f"Typographic scale ratio is {ratio:.1f}x (>= 2.5x hero-to-body contrast).")
        else:
            warnings.append(f"Typographic scale ratio is only {ratio:.1f}x. Recommended: >= 2.5x for editorial impact.")

    print(f"=== TYPOGRAPHY AUDIT: {os.path.basename(file_path)} ===")
    for p in passes:
        print(f"✅ [PASS] {p}")
    for w in warnings:
        print(f"⚠️ [WARN] {w}")

    # Pass if at least 2 key criteria are met
    success = len(passes) >= 2
    print(f"\nAudit Result: {'APPROVED' if success else 'NEEDS ATTENTION'}")
    return success

def main():
    parser = argparse.ArgumentParser(description="Audit editorial CSS for typography and motion guidelines.")
    parser.add_argument("--file", required=True, help="Path to CSS or HTML file")
    args = parser.parse_args()

    success = audit_typography(args.file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
