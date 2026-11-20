# Computational Biology Data Standards & Reproducibility

### 1. The Reproducibility Contract
Any scientific result delivered by an agent or human scientist must include:
- Checksum of input raw files (SHA-256).
- Exact package versions (`pip list`, `conda list`, or `pyproject.toml` lockfile).
- Random seed explicitly passed to all stochastic methods.
- Dry-run verification on a small toy subset before long-running batch launch.

### 2. Large File Hygiene
- Files > 1 GB must not be read into memory with a naive `open().read()` or `pd.read_csv()`.
- Use generator iterators (`Bio.SeqIO.parse()`, `pysam`, `h5py`, or chunked Pandas iterators).
- Always verify coordinate systems before joining datasets (e.g., BED 0-based vs. GFF 1-based).
