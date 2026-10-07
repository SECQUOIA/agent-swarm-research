"""Print OpenAlex metadata and reconstructed abstract for each DOI."""
import json, sys, urllib.request, time
for doi in sys.argv[1:]:
    try:
        w = json.load(urllib.request.urlopen(f"https://api.openalex.org/works/doi:{doi}", timeout=60))
    except Exception as e:
        print("==", doi, "NOT FOUND", e); continue
    inv = w.get("abstract_inverted_index") or {}
    pos = sorted((p, t) for t, ps in inv.items() for p in ps)
    print("==", doi, "|", w["title"], "|", w["publication_year"], "| cited_by", w["cited_by_count"])
    print("   ", " ".join(t for _, t in pos) if pos else "(no abstract)")
    time.sleep(0.5)
