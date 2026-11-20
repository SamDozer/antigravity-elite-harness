---
name: bio-literature-grounding
description: Ground biological identifiers, citations, gene symbols, and macromolecular structures against authoritative REST APIs (UniProt, RCSB PDB, Ensembl, Europe PMC/PubMed, Crossref). Use when validating biological accession numbers (e.g. UniProt P04637, PDB 1TUP), citing scientific papers with DOIs or PMIDs, verifying gene symbols with Ensembl IDs, or preventing hallucinated literature references. Do NOT use when reviewing git diffs for software syntax errors, writing CSS styles, or configuring build tools.
---

# Bio-Literature Grounding Skill

Prevent hallucinated biological identifiers, phantom citations, and invalid database accessions through live deterministic REST API verification.

## The Grounding Rule
Never cite a paper, hardcode a UniProt accession, or reference a PDB code based purely on LLM memory. You MUST verify its existence via:
```bash
python skills/comp-bio/bio-literature-grounding/scripts/verify_ids.py --type uniprot --id P04637
python skills/comp-bio/bio-literature-grounding/scripts/verify_ids.py --type pdb --id 1TUP
python skills/comp-bio/bio-literature-grounding/scripts/verify_ids.py --type doi --id 10.1038/nature12373
```

## Supported Authority Endpoints
- **UniProtKB:** `https://rest.uniprot.org/uniprotkb/{accession}.json` (Protein names, genes, organisms)
- **RCSB PDB:** `https://data.rcsb.org/rest/v1/core/entry/{pdb_id}` (Deposition date, resolution, experimental method)
- **Ensembl:** `https://rest.ensembl.org/lookup/id/{id}` (Gene coordinates, biotypes, canonical transcripts)
- **Crossref / Europe PMC:** `https://api.crossref.org/works/{doi}` (Journal title, publication year, authors)

## Workflow

### 1. Verification Query
- Run `verify_ids.py` for each accession mentioned in a report or pipeline script.
- The script checks local cache in `assets/verified_identifiers_cache.json` first, then issues a live HTTP request.

### 2. Annotation Embedding
- Embed retrieved canonical metadata (e.g. Gene symbol, UniProt entry name, Resolution in Å) into code comments or documentation tables.

### 3. Cache Updates
- When a new ID is successfully verified, write it to `assets/verified_identifiers_cache.json` for offline reproducibility.

## Hard Constraints
- Citing a paper with a non-resolving DOI or fabricated title is an automatic failure.
- Using an inactive or deleted UniProt/PDB identifier without flagging deprecation is prohibited.
