---
name: bio-orchestrator
description: Meta-router and scientific reproducibility gate for computational biology workflows. Use when inspecting input biological files (.fasta, .pdb, .gro, .fastq, .h5ad, .csv), logging cryptographic checksums, fixing random seeds, and running toy-subset dry runs before launching full compute pipelines. Do NOT use when designing frontend UI components, styling CSS, or creating promotional landing pages.
---

# Bio-Orchestrator Skill

Ensure computational biology analyses are scientifically valid, reproducible, and guarded against common LLM hallucinations and data leakage.

## Core Rules

1. **Inspect Before Code:** Always inspect file headers, line counts, and coordinate schemas before writing downstream analysis scripts:
   ```bash
   python skills/comp-bio/bio-orchestrator/scripts/inspect_biofile.py --file data/sample.fasta
   ```
2. **Cryptographic Checksumming:** Compute and log SHA-256 hashes of all raw input files before transformations into `assets/provenance_manifest.json`.
3. **Fixed Random Seeds:** Pin explicit seeds for every stochastic algorithm (NumPy, PyTorch, SciPy, UMAP, t-SNE, scikit-learn).
4. **Mandatory Toy-Subset Dry Run:** Before submitting a 10-hour compute job or SLURM task, run a 100-record toy subset locally to verify pipeline syntax and output shape.

## Workflow

### 1. Data Ingestion & Integrity
- Run `inspect_biofile.py` to identify file format, compression, record counts, and potential header corruption.
- Record the output checksum in your workflow manifest (`provenance_manifest.json`).

### 2. Sizing & Scaling Check
- Evaluate memory footprint: if file > 2GB, select chunked/streaming I/O (`pd.read_csv(chunksize=...)`, `Bio.SeqIO.parse()`, or Scanpy backed mode) instead of loading the entire file into RAM.

### 3. Toy-Subset Execution
- Create a test fixture with the first 50-100 records.
- Run the analysis end-to-end on the fixture to confirm that no unexpected shape mismatch or broadcast error occurs.

## Hard Constraints
- Never execute downstream analysis without logging the input file checksum.
- Pure random runs without `seed` parameters are strictly forbidden.
