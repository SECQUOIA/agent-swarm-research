"""Part A: compare the current MINLPLib pages and model files with the copies
used in the September 29 work.

Inputs:
  pages/instances/<name>.html          current page heads (fetch_current.py)
  pages/site/instances.html, minlplib.solu  current listing and solu file
  ../../bound-audit/pages/<name>.html  pages fetched 2026-09-30 (audit)
  ../../bound-audit/pages.json         parsed audit pages
  ../../open-instances-scout/pages/<name>.html, fetched.json  (2026-09-29)
  ../../reviews/*/data|web/<name>.html other stored copies, where present
  ~/.cache/minlplib/minlplib/osil/<name>.osil  OSIL files used by all work
  pages/models/osil/<name>.osil, pages/models/gms/<name>.gms  current files

Output: data/part_a.json and a printed summary.

The page parser is bound-audit/parse_pages.py (imported), so old and new
pages are parsed by the same code.
"""
import glob
import hashlib
import json
import os
import sys

from instances import ALL, GROUP

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(R, "bound-audit"))
import parse_pages as PP  # noqa: E402

CACHE = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def parse_head(path):
    page = open(path).read()
    c = PP.cells(page)
    prim = PP.points(c.get("Primal Bounds (infeas ≤ 1e-08)", ""), "primal")
    other = PP.points(c.get("Other points (infeas > 1e-08)", ""), "other")
    return dict(sense=PP.text(c.get("Objective Sense", "")).lower(),
                problem_type=PP.text(c.get("Problem type", "")),
                added_to_library=PP.text(c.get("Added to library", "")),
                points=prim + other, duals=PP.duals(c.get("Dual Bounds", "")))


def listing(path):
    PP_PAGES = PP.PAGES
    PP.PAGES = os.path.dirname(path)
    try:
        return PP.listing()
    finally:
        PP.PAGES = PP_PAGES


def key_pt(p):
    return (p["point"], p["value"], p["infeas"], p["section"], p["added"], p["bold"])


def key_du(d):
    return (d["solver"], d["value"], d["date"], d["bold"])


def main():
    site = os.path.join(HERE, "pages", "site")
    res = dict(site={}, instances={})
    for f in ("instances.html", "minlplib.solu"):
        new, old = os.path.join(site, f), os.path.join(R, "bound-audit", "pages", f)
        res["site"][f] = dict(new_sha256=sha(new), old_sha256=sha(old), identical=sha(new) == sha(old))
    Lnew = listing(os.path.join(site, "instances.html"))
    Lold = listing(os.path.join(R, "bound-audit", "pages", "instances.html"))
    old_json = {r["name"]: r for r in json.load(open(os.path.join(R, "bound-audit", "pages.json")))}
    scout = {r["name"]: r for r in json.load(open(os.path.join(R, "open-instances-scout", "fetched.json")))}
    man = json.load(open(os.path.join(HERE, "data", "fetch_manifest.json")))
    other_copies = {}
    for p in glob.glob(os.path.join(R, "reviews", "**", "*.html"), recursive=True):
        other_copies.setdefault(os.path.basename(p)[:-5], []).append(p)
    for name in ALL:
        newp = os.path.join(HERE, "pages", "instances", name + ".html")
        new = parse_head(newp)
        rec = dict(group=GROUP[name], listing_new=Lnew.get(name), listing_changed=Lnew.get(name) != Lold.get(name))
        # byte comparison against every stored copy of the page head
        comps = []
        for label, p in [("bound-audit 2026-09-30", os.path.join(R, "bound-audit", "pages", name + ".html")),
                         ("scout 2026-09-29", os.path.join(R, "open-instances-scout", "pages", name + ".html"))] + \
                [("review copy", p) for p in other_copies.get(name, [])]:
            if not os.path.exists(p):
                continue
            a, b = open(newp, "rb").read(), open(p, "rb").read()
            full_copy = b.find(b"<PRE>") > 0
            if full_copy:  # review copies are full pages: compare the head only
                b = b[:b.find(b"<PRE>")]
            same = a == b
            semantic = None
            if not same:
                old = parse_head(p)
                semantic = dict(points_added=[x for x in map(key_pt, new["points"]) if x not in set(map(key_pt, old["points"]))],
                                points_removed=[x for x in map(key_pt, old["points"]) if x not in set(map(key_pt, new["points"]))],
                                duals_added=[x for x in map(key_du, new["duals"]) if x not in set(map(key_du, old["duals"]))],
                                duals_removed=[x for x in map(key_du, old["duals"]) if x not in set(map(key_du, new["duals"]))],
                                sense_changed=old["sense"] != new["sense"])
            comps.append(dict(copy=label, path=os.path.relpath(p, R), byte_identical=same, full_copy=full_copy,
                              old_bytes=len(b), new_bytes=len(a), semantic_diff=semantic))
        rec["page_comparisons"] = comps
        # parsed comparison against pages.json
        oj = old_json.get(name)
        rec["pages_json_match"] = (oj is not None
                                   and sorted(map(key_pt, oj["points"])) == sorted(map(key_pt, new["points"]))
                                   and sorted(map(key_du, oj["duals"])) == sorted(map(key_du, new["duals"]))
                                   and oj["sense"] == new["sense"] and oj["problem_type"] == new["problem_type"])
        # scout fetched.json stores floats of the duals
        if name in scout:
            s = scout[name]
            sd = sorted((d["solver"], float(d["value"]), d["date"]) for d in s["duals"])
            nd = sorted((d["solver"], float(d["value"]), d["date"]) for d in new["duals"] if d["value"] is not None)
            rec["scout_json_match"] = (sd == nd and s.get("added") == new["added_to_library"])
        rec["page"] = new
        # model files
        o = man[f"{name}:osil"]
        g = man[f"{name}:gms"]
        cpath = os.path.join(CACHE, name + ".osil")
        rec["osil"] = dict(current_sha256=o["sha256"], current_bytes=o["bytes"], last_modified=o["last_modified"],
                           cache_sha256=sha(cpath) if os.path.exists(cpath) else None)
        rec["osil"]["identical_to_cache"] = rec["osil"]["current_sha256"] == rec["osil"]["cache_sha256"]
        rec["gms"] = dict(current_sha256=g["sha256"], current_bytes=g["bytes"], last_modified=g["last_modified"])
        res["instances"][name] = rec
    json.dump(res, open(os.path.join(HERE, "data", "part_a.json"), "w"), indent=1)
    # summary
    print("site files:", {k: v["identical"] for k, v in res["site"].items()})
    nI = len(res["instances"])
    print("instances:", nI)
    print("listing rows changed:", [n for n, r in res["instances"].items() if r["listing_changed"]])
    for lab in ("bound-audit 2026-09-30", "scout 2026-09-29", "review copy"):
        c = [(n, x["byte_identical"]) for n, r in res["instances"].items() for x in r["page_comparisons"] if x["copy"] == lab]
        print(f"{lab}: {len(c)} compared, {sum(1 for _, s in c if s)} byte-identical, differ: {[n for n, s in c if not s]}")
    print("pages.json parsed match:", sum(r["pages_json_match"] for r in res["instances"].values()), "of", nI,
          [n for n, r in res["instances"].items() if not r["pages_json_match"]])
    sc = [(n, r["scout_json_match"]) for n, r in res["instances"].items() if "scout_json_match" in r]
    print("scout fetched.json match:", sum(s for _, s in sc), "of", len(sc), [n for n, s in sc if not s])
    print("OSIL identical to cache:", sum(r["osil"]["identical_to_cache"] for r in res["instances"].values()), "of", nI,
          [n for n, r in res["instances"].items() if not r["osil"]["identical_to_cache"]])
    lm = {}
    for n, r in res["instances"].items():
        lm.setdefault(("osil", r["osil"]["last_modified"]), []).append(n)
        lm.setdefault(("gms", r["gms"]["last_modified"]), []).append(n)
    for k in sorted(lm):
        print(k, len(lm[k]), lm[k] if len(lm[k]) < 12 else "")


if __name__ == "__main__":
    main()
