#!/usr/bin/env python3
"""
verify_ids.py - Deterministic biological identifier & literature grounding tool.
Queries UniProt, RCSB PDB, Ensembl, and Crossref APIs to verify existence
and retrieve authoritative metadata. Caches responses to prevent rate limits.
"""

import sys
import os
import json
import urllib.request
import urllib.error
import argparse

CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', 'assets', 'verified_identifiers_cache.json')

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"[WARN] Failed to write cache: {e}", file=sys.stderr)

def query_endpoint(url: str, headers=None):
    req = urllib.request.Request(url, headers=headers or {'User-Agent': 'Antigravity-Harness-Verifier/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Unknown failure"}

def verify_uniprot(accession: str, cache):
    key = f"uniprot:{accession.upper()}"
    if key in cache:
        return True, cache[key], True

    url = f"https://rest.uniprot.org/uniprotkb/{accession.upper()}.json"
    res = query_endpoint(url)
    if "error" in res:
        return False, res, False

    entry = {
        "accession": accession.upper(),
        "primary_gene": res.get("genes", [{}])[0].get("geneName", {}).get("value", "N/A") if res.get("genes") else "N/A",
        "organism": res.get("organism", {}).get("scientificName", "Unknown"),
        "protein_name": res.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", "Unknown")
    }
    cache[key] = entry
    save_cache(cache)
    return True, entry, False

def verify_pdb(pdb_id: str, cache):
    key = f"pdb:{pdb_id.upper()}"
    if key in cache:
        return True, cache[key], True

    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id.upper()}"
    res = query_endpoint(url)
    if "error" in res:
        return False, res, False

    entry = {
        "pdb_id": pdb_id.upper(),
        "title": res.get("struct", {}).get("title", "No Title"),
        "method": res.get("exptl", [{}])[0].get("method", "Unknown"),
        "resolution": res.get("rcsb_entry_info", {}).get("resolution_combined", [None])[0]
    }
    cache[key] = entry
    save_cache(cache)
    return True, entry, False

def verify_doi(doi: str, cache):
    clean_doi = doi.strip()
    key = f"doi:{clean_doi.lower()}"
    if key in cache:
        return True, cache[key], True

    url = f"https://api.crossref.org/works/{clean_doi}"
    res = query_endpoint(url)
    if "error" in res or res.get("status") != "ok":
        return False, res, False

    msg = res.get("message", {})
    entry = {
        "doi": clean_doi,
        "title": msg.get("title", ["Unknown Title"])[0],
        "container_title": msg.get("container-title", ["Unknown Journal"])[0] if msg.get("container-title") else "Unknown Journal",
        "year": msg.get("published", {}).get("date-parts", [[None]])[0][0]
    }
    cache[key] = entry
    save_cache(cache)
    return True, entry, False

def verify_ensembl(ensembl_id: str, cache):
    clean_id = ensembl_id.strip().upper()
    key = f"ensembl:{clean_id}"
    if key in cache:
        return True, cache[key], True

    url = f"https://rest.ensembl.org/lookup/id/{clean_id}?content-type=application/json"
    res = query_endpoint(url, headers={'Content-Type': 'application/json', 'User-Agent': 'Antigravity-Harness-Verifier/1.0'})
    if "error" in res:
        return False, res, False

    entry = {
        "ensembl_id": clean_id,
        "symbol": res.get("display_name", "Unknown"),
        "species": res.get("species", "Unknown"),
        "biotype": res.get("biotype", "Unknown"),
        "description": res.get("description", "No Description"),
        "locus": f"chr{res.get('seq_region_name')}:{res.get('start')}-{res.get('end')}" if res.get('seq_region_name') else "N/A"
    }
    cache[key] = entry
    save_cache(cache)
    return True, entry, False

def verify_pubmed(pmid: str, cache):
    clean_pmid = str(pmid).strip()
    key = f"pubmed:{clean_pmid}"
    if key in cache:
        return True, cache[key], True

    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={clean_pmid}&retmode=json"
    res = query_endpoint(url)
    if "error" in res:
        return False, res, False

    result_block = res.get("result", {})
    item = result_block.get(clean_pmid, {})
    if not item or "title" not in item:
        return False, {"error": f"PMID {clean_pmid} not found in PubMed"}, False

    authors = [a.get("name") for a in item.get("authors", []) if isinstance(a, dict) and "name" in a]
    entry = {
        "pmid": clean_pmid,
        "title": item.get("title", "No Title"),
        "journal": item.get("source", "Unknown Journal"),
        "pubdate": item.get("pubdate", "Unknown Date"),
        "first_author": authors[0] if authors else "Unknown"
    }
    cache[key] = entry
    save_cache(cache)
    return True, entry, False

def main():
    parser = argparse.ArgumentParser(description="Verify biological database IDs and publication DOIs/PMIDs.")
    parser.add_argument("--type", choices=["uniprot", "pdb", "doi", "ensembl", "pubmed", "pmid"], required=True)
    parser.add_argument("--id", required=True, help="Accession / PDB ID / DOI / Ensembl ID / PMID to verify")
    args = parser.parse_args()

    cache = load_cache()

    if args.type == "uniprot":
        ok, data, from_cache = verify_uniprot(args.id, cache)
    elif args.type == "pdb":
        ok, data, from_cache = verify_pdb(args.id, cache)
    elif args.type == "doi":
        ok, data, from_cache = verify_doi(args.id, cache)
    elif args.type == "ensembl":
        ok, data, from_cache = verify_ensembl(args.id, cache)
    elif args.type in ["pubmed", "pmid"]:
        ok, data, from_cache = verify_pubmed(args.id, cache)

    print("====================================================")
    print(f"IDENTIFIER GROUNDING REPORT: {args.type.upper()} '{args.id}'")
    print("====================================================")
    if ok:
        source = "Local Verified Cache" if from_cache else "Live Authority REST API"
        print(f"Status:   ✅ VERIFIED ({source})")
        for k, v in data.items():
            print(f"  {k}: {v}")
        print("====================================================")
        sys.exit(0)
    else:
        print(f"Status:   ❌ UNVERIFIED OR NOT FOUND")
        print(f"Details:  {data.get('error', 'Unknown')}")
        print("====================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
