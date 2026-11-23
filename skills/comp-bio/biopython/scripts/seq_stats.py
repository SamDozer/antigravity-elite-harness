#!/usr/bin/env python3
"""Deterministic FASTA sequence statistics calculator (count, total bp, GC%, N50)."""
import argparse
import sys

def parse_fasta(path):
    seqs = []
    curr = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if curr:
                    seqs.append("".join(curr).upper())
                    curr = []
            else:
                curr.append(line)
        if curr:
            seqs.append("".join(curr).upper())
    return seqs

def compute_n50(lengths):
    if not lengths:
        return 0
    sorted_len = sorted(lengths, reverse=True)
    half = sum(sorted_len) / 2.0
    running = 0
    for l in sorted_len:
        running += l
        if running >= half:
            return l
    return sorted_len[-1]

def main():
    parser = argparse.ArgumentParser(description="Compute deterministic FASTA sequence metrics.")
    parser.add_argument("--fasta", required=True, help="Path to FASTA file")
    args = parser.parse_args()

    seqs = parse_fasta(args.fasta)
    if not seqs:
        print("[FAIL] No valid FASTA records found.")
        sys.exit(1)

    lengths = [len(s) for s in seqs]
    total_bp = sum(lengths)
    gc_count = sum(s.count("G") + s.count("C") for s in seqs)
    gc_pct = (gc_count / total_bp * 100.0) if total_bp > 0 else 0.0
    n50 = compute_n50(lengths)

    print(f"[PASS] Records: {len(seqs)} | Total bp: {total_bp} | GC%: {gc_pct:.2f}% | N50: {n50} bp")

if __name__ == "__main__":
    main()
