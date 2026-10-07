"""For each DOI print OpenAlex open-access status, OA URL and all locations' URLs."""
import json, sys, urllib.request, time
for doi in sys.argv[1:]:
    try:
        w = json.load(urllib.request.urlopen(f"https://api.openalex.org/works/doi:{doi}", timeout=60))
    except Exception as e:
        print(doi, "NOT FOUND", e); continue
    oa = w.get("open_access", {})
    locs = [l.get("landing_page_url") or "" for l in w.get("locations", [])] + [l.get("pdf_url") or "" for l in w.get("locations", [])]
    print(json.dumps({"doi": doi, "title": w["title"], "year": w["publication_year"], "cited_by": w["cited_by_count"],
                      "is_oa": oa.get("is_oa"), "oa_url": oa.get("oa_url"), "locs": sorted(set(x for x in locs if x))}))
    time.sleep(0.5)
