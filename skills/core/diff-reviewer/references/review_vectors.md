# The 7+1 Quality Review Vectors

Reviewers and automated agents inspect pull requests against these rigorous vectors:

### Vector 1: Logic Correctness & Edge Cases
- IEEE-754 precision issues (cents/currency floating-point math).
- Off-by-one boundary conditions (`<` vs `<=`, array slicing).
- Unhandled null, undefined, or empty set states.

### Vector 2: Security & Injection Vulnerabilities
- String interpolation in SQL, shell executions, HTML markup (XSS).
- Secret exposure (tokens, private keys, connection strings hardcoded).
- Path traversal vulnerabilities in file system calls.

### Vector 3: Reliability & Memory Leaks
- Unbounded caches (`new Map()`, `new Set()`, Python `dict` growing indefinitely).
- Unclosed sockets, unreleased DB connections, missing `clearTimeout` / `clearInterval`.
- Unhandled Promise rejections and uncatchable background task errors.

### Vector 4: Test Coverage & Invariant Verification
- Mutation resilience: if an operator or sign is inverted, does a test fail?
- Zero deletion or weakening of existing assertions to turn CI green.
- Concurrency and race condition testing.

### Vector 5: Altitude & Root-Cause Depth
- Does the fix eliminate the root cause in the originating system?
- Reject superficial symptom patching (e.g. adding `if (!x) return` in 5 different callers).

### Vector 6: Performance & Latency Bottlenecks
- Synchronous I/O in high-frequency event loops or request paths.
- N+1 database queries; missing indexes on filtered columns.
- Redundant re-renders or un-memoized expensive calculations in UI.

### Vector 7: Minimalism & SLOC Debloat (Ponytail)
- Deletion beats addition: is this feature, configuration, or abstraction actually requested?
- Refuse speculative "for later" architectural wrappers.

### Vector 8: Scientific Integrity (Bio / Data Repos)
- **Unit Consistency:** nm vs. Å (1 nm = 10 Å), kJ/mol vs. kcal/mol (1 kcal = 4.184 kJ), Kelvin vs. Celsius, log2 vs. ln.
- **Coordinate Discipline:** 0-based half-open (Python, BED, BAM) vs. 1-based inclusive (FASTA, GFF, VCF, PDB).
- **Indexing & Silent Broadcasting:** Shape mismatch broadcasting in NumPy/PyTorch; silent `.dropna()` dropping whole biological cohorts.
- **Statistical & ML Leakage:** Preprocessing (scaling, imputation, feature selection) fitted on entire dataset before splitting train/test.
- **Portability & Cluster Readiness:** Hardcoded local directory paths (`/home/username` or `C:\Users`); unpinned Conda/Python dependencies.
