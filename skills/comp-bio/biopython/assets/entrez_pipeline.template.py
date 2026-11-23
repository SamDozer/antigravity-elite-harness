#!/usr/bin/env python3
"""Reproducible Biopython Entrez & SeqIO template with NCBI rate-limit compliance."""
import os
from Bio import Entrez, SeqIO

Entrez.email = os.environ.get("NCBI_EMAIL", "researcher@example.org")
if os.environ.get("NCBI_API_KEY"):
    Entrez.api_key = os.environ["NCBI_API_KEY"]

def fetch_genbank_record(accession: str, out_fasta: str) -> None:
    with Entrez.efetch(db="nucleotide", id=accession, rettype="gb", retmode="text") as handle:
        record = SeqIO.read(handle, "genbank")
    SeqIO.write(record, out_fasta, "fasta")
