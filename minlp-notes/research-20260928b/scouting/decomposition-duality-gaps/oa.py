"""Search OpenAlex works; print year | title | venue | first authors | doi | cites."""
import sys, json, subprocess, urllib.parse, time
def search(q, n=12, since=None):
    f = "&filter=from_publication_date:%s" % since if since else ""
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(q) + f"&per-page={n}" + f
           + "&select=title,publication_year,primary_location,authorships,doi,cited_by_count")
    print("###", q, "(since %s)" % since if since else "")
    d = {}
    for k in range(6):
        s = subprocess.run(["curl", "-s", "-m", "60", url], capture_output=True, text=True).stdout
        try:
            d = json.loads(s)
        except Exception:
            d = {}
        if "results" in d:
            break
        time.sleep(int(d.get("retryAfter", 20)) + 2)
    if "results" not in d:
        print("  FAILED", str(d)[:200]); return
    for w in d.get("results", []):
        src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        a = ", ".join((x.get("author") or {}).get("display_name", "") for x in (w.get("authorships") or [])[:3])
        print(" ", w.get("publication_year"), "|", (w.get("title") or "")[:115], "|", src[:35], "|", a, "|",
              (w.get("doi") or "").replace("https://doi.org/", ""), "| c", w.get("cited_by_count"))
if __name__ == "__main__":
    since = None
    args = []
    for x in sys.argv[1:]:
        if x.startswith("--since="):
            since = x.split("=", 1)[1]
        else:
            args.append(x)
    for q in args:
        search(q, since=since)
        time.sleep(1)
