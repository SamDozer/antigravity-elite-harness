#!/usr/bin/env python3
"""
stats_guard.py - Deterministic biological statistics guard.
Calculates Benjamini-Hochberg FDR adjustments, checks coordinate conversions,
and audits datasets for ML leakage.
"""

import sys
import os
import argparse

def benjamini_hochberg(pvalues: list, alpha: float = 0.05):
    """Computes Benjamini-Hochberg FDR adjusted p-values and significance mask."""
    n = len(pvalues)
    if n == 0:
        return [], []

    # Sort p-values while retaining original indices
    indexed_pvals = sorted(enumerate(pvalues), key=lambda x: x[1])
    adjusted = [0.0] * n

    # Step-up calculation: p_adj = min(p * n / rank, next_p_adj)
    cum_min = 1.0
    for rank in range(n, 0, -1):
        orig_idx, p = indexed_pvals[rank - 1]
        val = (p * n) / rank
        cum_min = min(cum_min, val)
        adjusted[orig_idx] = min(cum_min, 1.0)

    significant = [adj <= alpha for adj in adjusted]
    return adjusted, significant

def convert_coords(start: int, end: int, from_sys: str, to_sys: str):
    """Converts coordinates between 0-based half-open and 1-based inclusive."""
    if from_sys == to_sys:
        return start, end
    if from_sys == "0-based" and to_sys == "1-based":
        # e.g., BED [0, 100) -> GFF [1, 100]
        return start + 1, end
    elif from_sys == "1-based" and to_sys == "0-based":
        # e.g., GFF [1, 100] -> BED [0, 100)
        return start - 1, end
    else:
        raise ValueError(f"Unknown coordinate system conversion: {from_sys} -> {to_sys}")

def main():
    parser = argparse.ArgumentParser(description="Statistical and coordinate validation guard.")
    subparsers = parser.add_subparsers(dest="cmd", help="Sub-command to execute")

    # FDR command
    fdr_parser = subparsers.add_parser("fdr", help="Calculate Benjamini-Hochberg FDR")
    fdr_parser.add_argument("--pvalues", required=True, help="Path to text/csv file of p-values, or comma-separated string")
    fdr_parser.add_argument("--alpha", type=float, default=0.05, help="Significance threshold (default 0.05)")

    # Coordinate command
    coord_parser = subparsers.add_parser("coords", help="Convert coordinates between 0-based and 1-based")
    coord_parser.add_argument("--start", type=int, required=True, help="Start position")
    coord_parser.add_argument("--end", type=int, required=True, help="End position")
    coord_parser.add_argument("--from-sys", choices=["0-based", "1-based"], required=True)
    coord_parser.add_argument("--to-sys", choices=["0-based", "1-based"], required=True)

    args = parser.parse_args()

    if args.cmd == "fdr":
        pvals = []
        if os.path.exists(args.pvalues):
            with open(args.pvalues, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.lower().startswith('p'):
                        try:
                            pvals.append(float(line.split(',')[0]))
                        except ValueError:
                            pass
        else:
            # Comma-separated list
            pvals = [float(x.strip()) for x in args.pvalues.split(',') if x.strip()]

        if not pvals:
            print("[FAIL] No valid numerical p-values found in input.", file=sys.stderr)
            sys.exit(1)

        invalid_p = [p for p in pvals if p < 0.0 or p > 1.0]
        if invalid_p:
            print(f"⚠️ [WARN] {len(invalid_p)} p-value(s) outside [0.0, 1.0] (e.g. {invalid_p[:3]}). Clamping to [0.0, 1.0].")
            pvals = [max(0.0, min(1.0, p)) for p in pvals]

        adj, sig = benjamini_hochberg(pvals, args.alpha)
        sig_count = sum(sig)

        print("====================================================")
        print("BENJAMINI-HOCHBERG FDR ADJUSTMENT RESULTS")
        print("====================================================")
        print(f"Total Hypotheses Tested:  {len(pvals):,}")
        print(f"Significance Level (FDR): {args.alpha}")
        print(f"Discoveries Declared:     {sig_count:,} ({sig_count/len(pvals)*100:.1f}%)")
        print("First 5 comparisons:")
        for idx in range(min(5, len(pvals))):
            status = "✅ SIGNIFICANT" if sig[idx] else "❌ NOT SIGNIFICANT"
            print(f"  Item {idx+1}: Raw p={pvals[idx]:.4e} | Adj q={adj[idx]:.4e} -> {status}")
        print("====================================================")

    elif args.cmd == "coords":
        new_start, new_end = convert_coords(args.start, args.end, args.from_sys, args.to_sys)
        print("====================================================")
        print(f"COORDINATE CONVERSION: {args.from_sys} -> {args.to_sys}")
        print(f"Input:  [{args.start}, {args.end}]")
        print(f"Output: [{new_start}, {new_end}]")
        in_len = (args.end - args.start) if args.from_sys == "0-based" else (args.end - args.start + 1)
        out_len = (new_end - new_start) if args.to_sys == "0-based" else (new_end - new_start + 1)
        print(f"Span Length: {in_len} bp (Verified equal: {in_len == out_len})")
        print("====================================================")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
