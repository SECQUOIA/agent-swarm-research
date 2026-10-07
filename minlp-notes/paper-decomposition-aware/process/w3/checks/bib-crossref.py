"""Print Crossref metadata for DOIs given on the command line (6 s between queries)."""
import json, sys, time, urllib.request, urllib.parse

UA = {"User-Agent": "bib-metadata-check/1.0 (python urllib)"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)

def show(m):
    au = ["%s, %s" % (a.get("family"), a.get("given")) for a in m.get("author", [])]
    ed = ["%s, %s" % (a.get("family"), a.get("given")) for a in m.get("editor", [])]
    date = (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0]
    print("  DOI      :", m.get("DOI"), "| type:", m.get("type"))
    print("  title    :", m.get("title"), m.get("subtitle") or "")
    print("  authors  :", "; ".join(au))
    if ed: print("  editors  :", "; ".join(ed))
    print("  container:", m.get("container-title"), "| publisher:", m.get("publisher"))
    print("  vol/iss/p:", m.get("volume"), m.get("issue"), m.get("page"), m.get("article-number", ""))
    print("  date     :", date, "| print:", (m.get("published-print") or {}).get("date-parts"), "| online:", (m.get("published-online") or {}).get("date-parts"))
    if m.get("ISBN"): print("  ISBN     :", m.get("ISBN"))
    if m.get("edition-number"): print("  edition  :", m.get("edition-number"))

args = sys.argv[1:]
for i, a in enumerate(args):
    if i: time.sleep(6)
    try:
        if a.startswith("q:"):
            q = urllib.parse.quote(a[2:])
            d = get("https://api.crossref.org/works?rows=3&query.bibliographic=" + q)
            print("== query:", a[2:])
            for m in d["message"]["items"]:
                show(m); print("  --")
        else:
            print("== doi:", a)
            show(get("https://api.crossref.org/works/" + urllib.parse.quote(a))["message"])
    except Exception as e:
        print("== ", a, "ERROR", e)
