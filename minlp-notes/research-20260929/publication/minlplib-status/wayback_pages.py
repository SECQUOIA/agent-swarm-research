"""Part B: Internet Archive captures of the instance pages of the audited
instances (bound and point history).

For each instance of the Part B list this queries the CDX index for
minlplib.org/<name>.html, downloads the earliest capture with status 200
(raw, id_), cuts it before <PRE>, parses it with bound-audit/parse_pages.py
and compares its points and per-solver dual bounds with the current page.
Requests are sequential with a delay of at least 1 s.

Output: data/wayback_pages.json
"""
import json
import os
import subprocess
import sys
import time

import instances as I

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(R, "bound-audit"))
import parse_pages as PP  # noqa: E402


def parse_head(path):
    """like compare_current.parse_head, but also reads the 2018 page layout
    (cell titled "Primal Bounds" without the infeasibility threshold)"""
    page = open(path).read()
    c = PP.cells(page)
    prim = c.get("Primal Bounds (infeas ≤ 1e-08)", c.get("Primal Bounds", ""))
    pts = PP.points(prim, "primal") + PP.points(c.get("Other points (infeas > 1e-08)", ""), "other")
    return dict(added_to_library=PP.text(c.get("Added to library", "")), points=pts,
                duals=PP.duals(c.get("Dual Bounds", "")))

UA = "minlp-notes MINLPLib history check (sequential, 1 req/s)"
OUT = os.path.join(HERE, "pages", "wayback", "instpages")
NAMES = I.AUDIT_I + I.AUDIT_IR + I.ROCKET


def curl(url, path=None):
    args = ["curl", "-s", "-L", "-m", "300", "-A", UA, url]
    if path:
        args[1:1] = ["-o", path]
    for attempt in range(3):
        p = subprocess.run(args, capture_output=True, text=path is None)
        time.sleep(1.2)
        if p.returncode == 0:
            return p.stdout if path is None else True
        time.sleep(10 * (attempt + 1))
    return None


def key_pt(p):
    return (p["point"], p["value"], p["infeas"], p["section"], p["added"])


def key_du(d):
    return (d["solver"], d["value"], d["date"])


def num_eq(a, b):
    """displayed values equal up to the display format (old pages show 8 decimals)"""
    if a == b:
        return True
    try:
        x, y = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return abs(x - y) <= 1e-8 * max(1.0, abs(x), abs(y))


def same_du(d, e):
    return d[0] == e[0] and d[2] == e[2] and num_eq(d[1], e[1])


def same_pt(p, q):
    return p[0] == q[0] and p[4] == q[4] and num_eq(p[1], q[1])


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for n in NAMES:
        cdx_path = os.path.join(HERE, "pages", "wayback", "cdx", f"page_{n}.txt")
        if not os.path.exists(cdx_path):
            txt = curl(f"http://web.archive.org/cdx/search/cdx?url=minlplib.org/{n}.html"
                       "&fl=timestamp,original,statuscode,digest,length") or ""
            open(cdx_path, "w").write(txt)
        rows = [l.split() for l in open(cdx_path) if l.strip()]
        ok = sorted(r for r in rows if len(r) >= 3 and r[2] == "200")
        rec = dict(captures=len(rows), captures_200=[r[0] for r in ok])
        if ok:
            ts, url = ok[0][0], ok[0][1]
            raw = os.path.join(OUT, f"{n}.{ts}.full.html")
            if not os.path.exists(raw):
                curl(f"http://web.archive.org/web/{ts}id_/{url}", raw)
            s = open(raw, "rb").read().decode("utf-8", "replace")
            k = s.find("<PRE>")
            head = os.path.join(OUT, f"{n}.{ts}.html")
            open(head, "w").write(s[:k] if k > 0 else s)
            old = parse_head(head)
            new = parse_head(os.path.join(HERE, "pages", "instances", n + ".html"))
            po, pn = [key_pt(p) for p in old["points"]], [key_pt(p) for p in new["points"]]
            do, dn = [key_du(d) for d in old["duals"]], [key_du(d) for d in new["duals"]]
            rec.update(earliest=ts, earliest_bytes=len(s), added_to_library=old["added_to_library"],
                       points_then=po, duals_then=do,
                       points_since_removed=[p for p in po if not any(same_pt(p, q) for q in pn)],
                       duals_since_removed_or_changed=[d for d in do if not any(same_du(d, e) for e in dn)],
                       points_added_since=[q for q in pn if not any(same_pt(p, q) for p in po)],
                       duals_added_or_changed_since=[e for e in dn if not any(same_du(d, e) for d in do)])
        res[n] = rec
        print(n, rec.get("earliest"), "captures:", len(rows), "removed:", rec.get("duals_since_removed_or_changed"),
              rec.get("points_since_removed"), flush=True)
    json.dump(res, open(os.path.join(HERE, "data", "wayback_pages.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
