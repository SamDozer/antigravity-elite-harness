# Authority Database REST APIs & Rate Limits

When validating biological data or resolving citations, adhere to these official REST endpoints:

### 1. UniProtKB REST API
- **Endpoint:** `https://rest.uniprot.org/uniprotkb/{accession}.json`
- **Rate Limit:** Unrestricted for reasonable batch rates (< 10 requests/sec). Include contact or agent header.
- **Payload:** Protein name, gene symbol, taxId, length, sequence, active features.

### 2. RCSB Protein Data Bank (PDB)
- **Endpoint:** `https://data.rcsb.org/rest/v1/core/entry/{pdb_id}`
- **Rate Limit:** Generous. Caching recommended for repeated workflow runs.
- **Payload:** Experimental method (X-ray, cryo-EM, NMR), resolution in Å, deposition date, title.

### 3. Ensembl REST API
- **Endpoint:** `https://rest.ensembl.org/lookup/id/{ensembl_id}?content-type=application/json`
- **Rate Limit:** Max 15 requests per second. Requires `content-type: application/json` header.

### 4. Crossref Works API
- **Endpoint:** `https://api.crossref.org/works/{doi}`
- **Etiquette:** Send polite `User-Agent: mailto:your-email@domain.com` for fast pool access.
