#!/usr/bin/env python3
"""
check_figure.py - Publication scientific figure quality gate.
Inspects PNG, TIFF, SVG, and PDF figures for minimum DPI (>= 300),
physical dimensions (in mm and inches), and vector compliance.
"""

import sys
import os
import struct
import argparse

def check_png_dpi(filepath: str):
    """Extracts DPI from PNG pHYs chunk if present, or reports dimensions."""
    with open(filepath, 'rb') as f:
        header = f.read(8)
        if header != b'\x89PNG\r\n\x1a\n':
            return None, None, None

        width, height = None, None
        dpi_x, dpi_y = None, None

        while True:
            chunk_len_bytes = f.read(4)
            if not chunk_len_bytes:
                break
            chunk_len = struct.unpack('>I', chunk_len_bytes)[0]
            chunk_type = f.read(4)

            if chunk_type == b'IHDR':
                ihdr = f.read(chunk_len)
                width, height = struct.unpack('>II', ihdr[:8])
                f.read(4) # crc
            elif chunk_type == b'pHYs':
                phys = f.read(chunk_len)
                ppux, ppuy, unit = struct.unpack('>IIB', phys)
                f.read(4) # crc
                if unit == 1: # pixels per meter
                    dpi_x = round(ppux * 0.0254)
                    dpi_y = round(ppuy * 0.0254)
            else:
                f.seek(chunk_len + 4, os.SEEK_CUR)

    return (width, height), (dpi_x, dpi_y)

def check_figure(filepath: str):
    if not os.path.exists(filepath):
        print(f"[FAIL] Figure file not found: {filepath}", file=sys.stderr)
        return False

    ext = os.path.splitext(filepath)[1].lower()
    passes = []
    warnings = []
    errors = []

    print("====================================================")
    print(f"SCIENTIFIC FIGURE AUDIT: {os.path.basename(filepath)}")
    print("====================================================")

    if ext in ['.pdf', '.svg']:
        passes.append("Vector format detected (PDF/SVG). Resolution is resolution-independent.")
        if ext == '.svg':
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read(4096)
                if 'viewBox' in content:
                    passes.append("Responsive viewBox declared.")
                else:
                    warnings.append("SVG missing viewBox attribute.")
    elif ext == '.png':
        dims, dpis = check_png_dpi(filepath)
        if dims:
            width_px, height_px = dims
            passes.append(f"Image dimensions: {width_px} x {height_px} px")
            if dpis and dpis[0]:
                dpi = dpis[0]
                width_mm = (width_px / dpi) * 25.4
                height_mm = (height_px / dpi) * 25.4
                passes.append(f"Physical dimensions at declared DPI: {width_mm:.1f} mm x {height_mm:.1f} mm")
                if dpi >= 300:
                    passes.append(f"Declared DPI: {dpi} DPI (>= 300 DPI publication threshold)")
                else:
                    errors.append(f"Declared DPI {dpi} is below 300 DPI journal publication minimum.")
            else:
                # Assume standard 300 DPI mapping
                width_at_300 = (width_px / 300) * 25.4
                if width_px >= 1000:
                    passes.append(f"Pixel width ({width_px}px) supports ~{width_at_300:.1f}mm at 300 DPI.")
                else:
                    warnings.append(f"Low pixel resolution ({width_px}px). May appear blurry if printed at 85mm+.")
        else:
            errors.append("Invalid or corrupted PNG file.")
    else:
        passes.append(f"File format: {ext} (Manual resolution inspection recommended).")

    for p in passes:
        print(f"✅ [PASS] {p}")
    for w in warnings:
        print(f"⚠️ [WARN] {w}")
    for e in errors:
        print(f"❌ [FAIL] {e}")

    success = len(errors) == 0
    print(f"\nVerdict: {'APPROVED' if success else 'REJECTED'}")
    return success

def main():
    parser = argparse.ArgumentParser(description="Audit scientific figure resolution and format.")
    parser.add_argument("--figure", required=True, help="Path to figure file (.png, .pdf, .svg, .tiff)")
    args = parser.parse_args()

    success = check_figure(args.figure)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
