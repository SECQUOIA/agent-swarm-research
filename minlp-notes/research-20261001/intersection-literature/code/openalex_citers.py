"""List works citing given OpenAlex IDs (union), with year, venue, DOI, title.
Usage: python3 openalex_citers.py ID1 ID2 ...  Output: JSON lines on stdout."""
import json, sys, time, urllib.request
def get(url):
    for k in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 + 3 * k)
    raise RuntimeError(url)
for wid in sys.argv[1:]:
    cursor = "*"
    while cursor:
        d = get(f"https://api.openalex.org/works?filter=cites:{wid}&per-page=200&cursor={cursor}"
                "&select=id,doi,title,publication_year,primary_location,authorships")
        for w in d["results"]:
            pl = w.get("primary_location") or {}
            s = pl.get("source") or {}
            au = ", ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:6])
            print(json.dumps({"cites": wid, "id": w["id"], "year": w["publication_year"],
                              "doi": w["doi"], "venue": s.get("display_name"),
                              "authors": au, "title": w["title"]}))
        cursor = d["meta"].get("next_cursor")
        if not d["results"]:
            break
