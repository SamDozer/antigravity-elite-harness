---
name: bio-sequence-stats
description: Sequence analysis, tabular omics, and rigorous biostatistics guard. Use when manipulating genomic coordinates (BED vs GFF/VCF conversions), calculating differential gene expression, applying multiple hypothesis testing corrections (Benjamini-Hochberg FDR), aggregating biological vs technical replicates, and preventing data leakage in ML biomarker models. Do NOT use when simulating molecular dynamics trajectories (use structural-bio-md) or designing web UI frontends.
---

# Bio-Sequence & Statistical Integrity Skill

Guards against coordinate indexing errors, statistical false positives, and machine-learning data leakage in genomics and omics data analysis.

## Core Principles

1. **Strict Coordinate Discipline:**
   - **0-based half-open `[start, end)`:** BED, BAM, Python slices, UCSC database queries. Length = `end - start`.
   - **1-based inclusive `[start, end]`:** GFF3, GTF, VCF, SAM POS column, PDB residue indexing. Length = `end - start + 1`.
   - Converting 1-based inclusive `[1, 100]` to BED: `[0, 100]`.
   - Converting BED `[0, 100]` to 1-based inclusive: `[1, 100]`.
2. **Multiple Hypothesis Testing Correction:**
   - Never report raw p-values when testing hundreds or thousands of genes/variants.
   - Enforce Benjamini-Hochberg False Discovery Rate (FDR / q-value) or Bonferroni correction.
3. **Biological vs. Technical Replicates:**
   - Technical replicates (same sample run across two sequencer lanes) MUST be merged or pooled before statistical modeling.
   - Degrees of freedom in differential expression tools (DESeq2, edgeR, Limma) must equal biological biological subjects ($N$), not number of technical runs.
4. **Machine Learning Data Leakage Prevention:**
   - Preprocessing steps (`StandardScaler`, imputers, PCA, feature selection) MUST be fitted ONLY on the training split, then applied via `.transform()` to validation and test splits.

## Workflow

### 1. Apply Multiple Testing Correction
Run `scripts/stats_guard.py` to calculate Benjamini-Hochberg FDR on raw p-values:
```bash
python skills/comp-bio/bio-sequence-stats/scripts/stats_guard.py --pvalues data/raw_pvals.csv --alpha 0.05
```

### 2. Verify Coordinate Systems
Consult `references/coordinate_systems.md` before performing range overlaps or slicing genomic intervals.

### 3. Template Usage
Start differential expression workflows using `assets/diff_exp_template.py`.

## Hard Constraints
- Reporting uncorrected p-values for omics screening is an automatic rejection.
- Zero feature normalization across the full dataset prior to train/test split.
