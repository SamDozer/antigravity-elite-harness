#!/usr/bin/env python3
"""Scans CSS/TSX files for responsive overflow traps (100vw horizontal scroll, fixed widths > 400px)."""
import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser(description="Check CSS/TSX for responsive viewport traps.")
    parser.add_argument("--file", required=True, help="Path to CSS/TSX file")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    warnings = []
    if re.search(r"width\s*:\s*100vw", text):
        warnings.append("Found 'width: 100vw' which causes horizontal overflow when vertical scrollbar is present (prefer 100%).")
    for m in re.finditer(r"(?:min-width|width)\s*:\s*(\d+)px", text):
        px = int(m.group(1))
        if px > 375:
            warnings.append(f"Fixed width {px}px exceeds 375px mobile viewport budget; use max-width or clamp().")

    if warnings:
        for w in warnings:
            print(f"[WARN] {w}")
        sys.exit(1)
    print("[PASS] Zero static responsive overflow traps detected.")

if __name__ == "__main__":
    main()
