"""Crossref title search for candidate missing references (R7 literature review)."""
import json, sys, time, urllib.request, urllib.parse
for q in sys.argv[1:]:
    url = "https://api.crossref.org/works?rows=1&query.bibliographic=" + urllib.parse.quote(q)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "r7-check"}), timeout=30) as r:
            m = json.load(r)["message"]["items"][0]
        auth = [a.get("family", "") for a in m.get("author", [])]
        date = (m.get("published-print") or m.get("issued"))["date-parts"]
        print(f"Q: {q}\n  -> {m.get('DOI')} | {m.get('title')} | {auth} | {m.get('container-title')} vol {m.get('volume')} iss {m.get('issue')} pp {m.get('page')} | {date}")
    except Exception as e:
        print(f"Q: {q}\n  ERROR {e}")
    time.sleep(1)
