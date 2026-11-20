#!/usr/bin/env python3
"""
inspect_biofile.py - Rapid header, format, and checksum inspector for biological files.
Inspects FASTA, FASTQ, PDB, GRO, XTC, H5AD, NPY, BED, VCF, CSV, and TSV files without reading full gigabytes into memory.
"""

import sys
import os
import hashlib
import gzip
import struct
import ast
import argparse

def compute_sha256(filepath: str, max_bytes: int = 64 * 1024 * 1024) -> str:
    """Computes SHA256 of first max_bytes for speed on huge files."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        chunk = f.read(max_bytes)
        h.update(chunk)
    return h.hexdigest()

def inspect_npy(filepath: str):
    """Inspects NumPy .npy binary header."""
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(6)
            if magic != b'\x93NUMPY':
                return None
            major, minor = struct.unpack('BB', f.read(2))
            if major == 1:
                hlen = struct.unpack('<H', f.read(2))[0]
            else:
                hlen = struct.unpack('<I', f.read(4))[0]
            header_str = f.read(hlen).decode('latin1', errors='replace').strip()
            meta = ast.literal_eval(header_str)
            return {
                "version": f"{major}.{minor}",
                "shape": meta.get("shape"),
                "dtype": meta.get("descr"),
                "fortran_order": meta.get("fortran_order")
            }
    except Exception:
        return None

def inspect_xtc(filepath: str):
    """Inspects GROMACS XTC binary trajectory header."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(16)
            if len(chunk) < 16:
                return None
            magic, natoms, step, time = struct.unpack('>iiif', chunk)
            if magic == 1995:
                return {
                    "natoms": natoms,
                    "first_step": step,
                    "first_time_ps": time
                }
    except Exception:
        return None

def inspect_h5ad(filepath: str):
    """Inspects HDF5/AnnData container signature and structure."""
    try:
        with open(filepath, 'rb') as f:
            sig = f.read(8)
            if sig != b'\x89HDF\r\n\x1a\n':
                return None
        info = {"hdf5_signature": True}
        try:
            import h5py
            with h5py.File(filepath, 'r') as h5:
                info["keys"] = list(h5.keys())
                if 'X' in h5:
                    if hasattr(h5['X'], 'shape'):
                        info["X_shape"] = h5['X'].shape
                    elif 'shape' in h5['X'].attrs:
                        info["X_shape"] = tuple(h5['X'].attrs['shape'])
        except Exception:
            pass
        return info
    except Exception:
        return None

def inspect_file(filepath: str):
    if not os.path.exists(filepath):
        print(f"[FAIL] File not found: {filepath}", file=sys.stderr)
        return False

    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    sha256 = compute_sha256(filepath)

    is_gzipped = filepath.endswith('.gz')
    opener = gzip.open if is_gzipped else open

    ext = os.path.splitext(filepath[:-3] if is_gzipped else filepath)[1].lower()

    detected_format = "Unknown"
    details = []
    header_lines = []

    # Check binary formats first
    if ext == '.npy':
        npy_info = inspect_npy(filepath)
        if npy_info:
            detected_format = "NumPy Binary Array (.npy)"
            details.append(f"Matrix Shape: {npy_info['shape']}")
            details.append(f"Data Type (descr): {npy_info['dtype']}")
            details.append(f"Fortran Order: {npy_info['fortran_order']}")
            details.append(f"NPY Version: {npy_info['version']}")
    elif ext == '.xtc':
        xtc_info = inspect_xtc(filepath)
        if xtc_info:
            detected_format = "GROMACS Compressed Trajectory (.xtc)"
            details.append(f"Declared Atoms: {xtc_info['natoms']:,}")
            details.append(f"Initial Frame Step: {xtc_info['first_step']}")
            details.append(f"Initial Time: {xtc_info['first_time_ps']:.2f} ps")
    elif ext == '.h5ad':
        h5_info = inspect_h5ad(filepath)
        if h5_info:
            detected_format = "AnnData / HDF5 Single-Cell Container (.h5ad)"
            details.append("HDF5 Superblock Signature: Valid (b'\\x89HDF\\r\\n\\x1a\\n')")
            if "X_shape" in h5_info:
                details.append(f"Expression Matrix X Shape: {h5_info['X_shape']}")
            if "keys" in h5_info:
                details.append(f"Top-level HDF5 Groups: {', '.join(h5_info['keys'])}")

    # If not a binary format, read initial text lines safely
    if detected_format == "Unknown":
        total_lines = 0
        try:
            with opener(filepath, 'rt', encoding='utf-8', errors='replace') as f:
                for idx, line in enumerate(f):
                    if idx < 10:
                        header_lines.append(line.rstrip('\r\n'))
                    total_lines += 1
                    if total_lines > 100000:
                        break
        except Exception as e:
            print(f"[FAIL] Could not read file lines: {e}", file=sys.stderr)
            return False

        first_line = header_lines[0] if header_lines else ""
        if ext in ['.fasta', '.fa', '.fna'] or first_line.startswith('>'):
            detected_format = "FASTA"
            seq_count = sum(1 for line in header_lines if line.startswith('>'))
            details.append(f"Sample header: {first_line[:60]}")
        elif ext in ['.fastq', '.fq'] or first_line.startswith('@'):
            detected_format = "FASTQ"
            details.append(f"First read ID: {first_line[:60]}")
        elif ext == '.pdb' or any(l.startswith(('ATOM', 'HETATM', 'HEADER')) for l in header_lines):
            detected_format = "PDB (Macromolecular Structure)"
            atom_count = sum(1 for l in header_lines if l.startswith(('ATOM', 'HETATM')))
            details.append(f"Sample ATOM record: {[l for l in header_lines if l.startswith('ATOM')][:1]}")
        elif ext == '.gro':
            detected_format = "GROMACS GRO"
            if len(header_lines) >= 2:
                details.append(f"System Title: {header_lines[0]}; Declared Atoms: {header_lines[1].strip()}")
        elif ext in ['.bed']:
            detected_format = "BED (0-based half-open intervals)"
            cols = first_line.split('\t')
            details.append(f"Columns detected: {len(cols)}")
        elif ext in ['.vcf'] or first_line.startswith('##fileformat=VCF'):
            detected_format = "VCF (1-based inclusive variants)"
        elif ext in ['.csv', '.tsv']:
            sep = '\t' if ext == '.tsv' or '\t' in first_line else ','
            detected_format = f"Delimited Table ({'TSV' if sep == '\t' else 'CSV'})"
            cols = first_line.split(sep)
            details.append(f"Header columns count: {len(cols)}")
            details.append(f"Sample columns: {', '.join(cols[:5])}...")

    print("====================================================")
    print(f"BIOFILE INSPECTION REPORT: {os.path.basename(filepath)}")
    print("====================================================")
    print(f"Format:       {detected_format}")
    print(f"Size:         {size_mb:.2f} MB ({size_bytes:,} bytes)")
    print(f"Compression:  {'Gzip compressed' if is_gzipped else 'Uncompressed'}")
    print(f"SHA-256 (64M): {sha256}")
    if header_lines:
        print(f"Header Preview:")
        for idx, hl in enumerate(header_lines[:5], 1):
            print(f"  {idx}: {hl[:80]}")
    for d in details:
        print(f"Note: {d}")
    print("====================================================")
    return True

def main():
    parser = argparse.ArgumentParser(description="Inspect biological file format, headers, and checksum.")
    parser.add_argument("--file", required=True, help="Path to biological file")
    args = parser.parse_args()

    success = inspect_file(args.file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
