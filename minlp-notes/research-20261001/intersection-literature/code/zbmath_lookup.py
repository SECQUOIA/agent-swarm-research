"""Query zbMATH Open API; print id, source, title and review text (if licensed for the API)."""
import json, sys, urllib.parse, urllib.request, time
for q in sys.argv[1:]:
    url = "https://api.zbmath.org/v1/document/_search?" + urllib.parse.urlencode(
        {"search_string": q, "page": 0, "results_per_page": 10})
    try:
        d = json.load(urllib.request.urlopen(url, timeout=60))
    except Exception as e:
        print("###", q, "ERROR", e); continue
    print("###", q)
    for r in d.get("result", []):
        txt = " | ".join(c.get("text") or "" for c in r.get("editorial_contributions", []))
        print(" ", r.get("zbmath_url"), "|", r["source"]["source"], "|", r["title"]["title"])
        print("    review:", txt[:1200])
    time.sleep(1)
