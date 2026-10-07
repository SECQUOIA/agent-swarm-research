"""Fetch Crossref metadata for a list of DOIs and print key fields (R7 literature review)."""
import json, sys, time, urllib.request, urllib.parse
dois = sys.argv[1:]
for d in dois:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(d, safe="/")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "r7-check"}), timeout=30) as r:
            m = json.load(r)["message"]
        auth = [(a.get("given", "") + " " + a.get("family", "")).strip() for a in m.get("author", [])]
        date = (m.get("published-print") or m.get("issued"))["date-parts"]
        print(f"== {d}\n  title: {m.get('title')}\n  authors: {auth}\n  venue: {m.get('container-title')} vol {m.get('volume')} iss {m.get('issue')} pp {m.get('page')} art {m.get('article-number')} date {date}")
    except Exception as e:
        print(f"== {d}\n  ERROR {e}")
    time.sleep(1)
