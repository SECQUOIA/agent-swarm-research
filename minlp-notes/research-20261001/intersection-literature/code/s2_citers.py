"""List citing papers from the Semantic Scholar Graph API.
Usage: python3 s2_citers.py PAPERID ...  (e.g. arXiv:1911.12341, DOI:10.1007/...)
Prints one JSON line per citing paper."""
import json, sys, time, urllib.request, urllib.error
def get(url):
    for k in range(12):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(20 + 20 * k)
        except Exception:
            time.sleep(20 + 20 * k)
    raise RuntimeError(url)
for pid in sys.argv[1:]:
    meta = get(f"https://api.semanticscholar.org/graph/v1/paper/{pid}?fields=title,year,citationCount")
    print(json.dumps({"query": pid, "meta": meta}), flush=True)
    if not meta:
        continue
    off = 0
    while True:
        d = get(f"https://api.semanticscholar.org/graph/v1/paper/{pid}/citations?fields=title,year,venue,authors,externalIds&limit=100&offset={off}")
        if not d:
            break
        for c in d.get("data", []):
            p = c["citingPaper"]
            print(json.dumps({"cites": pid, "year": p.get("year"), "title": p.get("title"),
                              "venue": p.get("venue"), "ids": p.get("externalIds"),
                              "authors": ", ".join(a["name"] for a in (p.get("authors") or [])[:6])}), flush=True)
        if "next" not in d:
            break
        off = d["next"]
        time.sleep(3)
    time.sleep(3)
