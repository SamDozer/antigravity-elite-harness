# Genomic Coordinate Systems Reference

Prevent catastrophic off-by-one errors when intersecting genomics formats:

| Format / System | Indexing Base | Interval Type | Span Formula | Example for first 100bp |
| :--- | :--- | :--- | :--- | :--- |
| **BED** | 0-based | Half-open `[start, end)` | `end - start` | `0 100` |
| **BAM / CRAM** | 0-based (internal) | Half-open | `end - start` | Stored 0-indexed in binary |
| **Python / NumPy** | 0-based | Half-open `[0:100]` | `end - start` | `seq[0:100]` (extracts 100 bp) |
| **UCSC Browser** | 0-based (API) | Half-open | `end - start` | In URL display: 1-based |
| **FASTA** | 1-based | Closed `[start, end]` | `end - start + 1` | `1 100` |
| **GFF3 / GTF** | 1-based | Closed `[start, end]` | `end - start + 1` | `1 100` |
| **VCF** | 1-based | Point coordinate | `POS = 1` | `POS = 1` (first base) |
| **SAM POS column**| 1-based | Point coordinate | `POS = 1` | `POS = 1` (first base) |
| **PDB Residues** | 1-based (nominal) | Sequence number | Custom numbering | Insertion codes allowed (e.g. 52A) |

### Conversion Rules
- **From 1-based closed `[start, end]` to 0-based half-open (BED):**
  - `bed_start = start - 1`
  - `bed_end = end`
- **From 0-based half-open (BED) `[start, end)` to 1-based closed (GFF):**
  - `gff_start = start + 1`
  - `gff_end = end`
