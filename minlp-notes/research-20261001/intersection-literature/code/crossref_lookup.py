"""Crossref bibliographic lookup: top 3 hits per query (DOI, title, container, volume, issue, pages, year)."""
import json, sys, urllib.parse, urllib.request, time
for q in sys.argv[1:]:
    url = "https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(q)
    d = json.load(urllib.request.urlopen(url, timeout=60))
    print("###", q)
    for it in d["message"]["items"]:
        yr = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        au = ", ".join((a.get("family") or "") for a in it.get("author", [])[:5])
        print(" ", it["DOI"], "|", (it.get("title") or [""])[0][:90], "|", au, "|", (it.get("container-title") or [""])[0],
              it.get("volume"), it.get("issue"), it.get("page"), yr)
    time.sleep(1)
