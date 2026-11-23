#!/usr/bin/env python3
"""Scans frontend files for hardcoded arbitrary Tailwind hex classes (e.g. bg-[#123456]) instead of semantic tokens."""
import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser(description="Audit Tailwind classes for semantic token compliance.")
    parser.add_argument("--file", required=True, help="Path to TSX/JSX/HTML file")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    arbitrary_hex = re.findall(r"\b(?:bg|text|border|ring)-\[#[0-9a-fA-F]{3,8}\]", text)
    if arbitrary_hex:
        print(f"[FAIL] Found {len(arbitrary_hex)} arbitrary hex classes ({', '.join(arbitrary_hex[:5])}). Use semantic design tokens.")
        sys.exit(1)
    print("[PASS] Tailwind semantic token audit passed.")

if __name__ == "__main__":
    main()
