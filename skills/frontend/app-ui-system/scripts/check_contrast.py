#!/usr/bin/env python3
"""
check_contrast.py - Deterministic WCAG 2.2 AA Contrast Ratio Calculator.
Calculates relative luminance according to W3C specifications.
"""

import sys
import argparse
import re

def hex_to_rgb(hex_str: str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join(c * 2 for c in hex_str)
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: {hex_str}")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def channel_luminance(val: int) -> float:
    c = val / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def relative_luminance(rgb) -> float:
    r, g, b = (channel_luminance(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = relative_luminance(hex_to_rgb(hex1))
    l2 = relative_luminance(hex_to_rgb(hex2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def main():
    parser = argparse.ArgumentParser(description="Calculate WCAG 2.2 contrast ratio between two hex colors.")
    parser.add_argument("--fg", required=True, help="Foreground HEX color (e.g. #94a3b8)")
    parser.add_argument("--bg", required=True, help="Background HEX color (e.g. #0f172a)")
    parser.add_argument("--target", choices=["normal", "large", "ui"], default="normal",
                        help="Target element type: normal text (4.5:1), large text (3.0:1), ui component (3.0:1)")
    args = parser.parse_args()

    try:
        ratio = contrast_ratio(args.fg, args.bg)
    except Exception as e:
        print(f"[FAIL] Error parsing colors: {e}", file=sys.stderr)
        sys.exit(1)

    threshold = 4.5 if args.target == "normal" else 3.0
    passed = ratio >= threshold

    status = "PASS" if passed else "FAIL"
    print(f"[{status}] Contrast Ratio: {ratio:.2f}:1 (Required: {threshold}:1 for {args.target})")
    print(f"       FG: {args.fg} | BG: {args.bg}")

    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
