"""List citing works from the OpenCitations Index (API v2) for the given DOIs.

Usage: python3 opencitations.py DOI [DOI ...] > ../logs/opencitations.log
For each DOI prints "== DOI", the number of citing records, and the 'citing'
identifier field of each record (sorted).
"""
import json, sys, time, urllib.request

for doi in sys.argv[1:]:
    url = "https://api.opencitations.net/index/v2/citations/doi:" + doi
    req = urllib.request.Request(url, headers={"User-Agent": "minlp-notes-audit/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        recs = json.load(r)
    print("==", doi)
    print(len(recs))
    for c in sorted(rec["citing"] for rec in recs):
        print(c)
    sys.stdout.flush()
    time.sleep(1)
