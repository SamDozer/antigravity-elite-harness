#!/usr/bin/env python3
"""
diff_exp_template.py - Minimal, leak-free template for differential gene expression analysis.
Demonstrates deterministic FDR adjustment and volcano plot data preparation.
"""

import math

def calculate_diff_exp(gene_data: list, alpha: float = 0.05):
    """
    Input: list of dicts: [{'gene': 'TP53', 'log2fc': 2.3, 'raw_p': 0.0001}, ...]
    Applies Benjamini-Hochberg FDR correction and assigns significance status.
    """
    n = len(gene_data)
    if n == 0:
        return []

    # Sort by p-value
    sorted_genes = sorted(gene_data, key=lambda x: x['raw_p'])

    cum_min = 1.0
    for rank in range(n, 0, -1):
        p = sorted_genes[rank - 1]['raw_p']
        fdr = min(cum_min, (p * n) / rank)
        cum_min = fdr
        sorted_genes[rank - 1]['padj'] = min(fdr, 1.0)
        sorted_genes[rank - 1]['neg_log10_padj'] = -math.log10(max(sorted_genes[rank - 1]['padj'], 1e-300))

        # Significance flag: padj < alpha and abs(log2fc) >= 1.0
        is_sig = sorted_genes[rank - 1]['padj'] <= alpha and abs(sorted_genes[rank - 1]['log2fc']) >= 1.0
        sorted_genes[rank - 1]['significant'] = is_sig

    return sorted_genes

if __name__ == "__main__":
    sample_genes = [
        {'gene': 'BRCA1', 'log2fc': 2.4, 'raw_p': 0.00001},
        {'gene': 'EGFR', 'log2fc': -1.8, 'raw_p': 0.0003},
        {'gene': 'GAPDH', 'log2fc': 0.05, 'raw_p': 0.85},
        {'gene': 'ACTB', 'log2fc': -0.12, 'raw_p': 0.72}
    ]
    results = calculate_diff_exp(sample_genes)
    for r in results:
        print(f"Gene: {r['gene']:<8} | Log2FC: {r['log2fc']:>5.2f} | Raw P: {r['raw_p']:.2e} | Padj: {r['padj']:.2e} | Significant: {r['significant']}")
