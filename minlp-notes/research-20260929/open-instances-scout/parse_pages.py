"""Parse cached MINLPLib instance pages (pages/<name>.html) for the candidates
selected by fetch_pages.py and write fetched.json / fetched.csv.

Per instance: all listed feasible primal values (infeas <= 1e-8), other
points (infeas > 1e-8), all single-solver dual bounds, the best of each,
the relative gap in MINLPLib's convention |p-d|/min(|p|,|d|) (inf if the
signs differ or one value is 0), problem type, objective sense, counts,
source, application and references.

Usage: python3 parse_pages.py
"""
import csv, html, json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def cells(page):
    """Map row label -> raw HTML of the value cell."""
    out = {}
    for m in re.finditer(r"<TR>\s*<TD><span>(.*?)<sup>.*?</TD>\s*<TD>(.*?)</TD>\s*</TR>", page, re.S):
        out[text(m.group(1))] = m.group(2)
    return out


NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"


def primal_points(raw):
    pts = []
    for m in re.finditer(r'<div title="Added on[^"]*">(.*?)</div>', raw, re.S):
        chunk = m.group(1)
        v = re.search(r"(" + NUM + r")\s*(?:</B>)?\s*<A href=[^>]*>(p\d+)</A>", chunk)
        if not v:
            continue
        inf = re.search(r"infeas:\s*(" + NUM + ")", chunk)
        pts.append(dict(value=float(v.group(1)), point=v.group(2),
                        infeas=float(inf.group(1)) if inf else None))
    return pts


def dual_bounds(raw):
    out = []
    for m in re.finditer(r'<div title="Last updated: ([^"]*)">(.*?)</div>', raw, re.S):
        t = text(m.group(2))
        mm = re.match(r"(\S+)\s*\((.*?)\)", t)
        if not mm:
            out.append(dict(raw=t, date=m.group(1)))
            continue
        v = mm.group(1).rstrip(".") if mm.group(1).endswith(".") else mm.group(1)
        try:
            val = float(v.replace("inf", "inf"))
        except ValueError:
            val = None
        out.append(dict(value=val, solver=mm.group(2).strip(), date=m.group(1), bold="<B>" in m.group(2), raw=t))
    return out


def relgap(p, d):
    if p is None or d is None:
        return math.inf
    if p == d:
        return 0.0
    if p * d <= 0:
        return math.inf
    return abs(p - d) / min(abs(p), abs(d))


def parse(name):
    page = open(os.path.join(HERE, "pages", name + ".html")).read()
    c = cells(page)
    sense = text(c.get("Objective Sense", "")).lower()
    sgn = 1 if sense == "min" else -1  # better primal = smaller sgn*p; better dual = larger sgn*d
    prim = primal_points(c.get("Primal Bounds (infeas ≤ 1e-08)", c.get("Primal Bounds (infeas &le; 1e-08)", "")))
    other = primal_points(c.get("Other points (infeas > 1e-08)", ""))
    duals = dual_bounds(c.get("Dual Bounds", ""))
    bp = min(prim, key=lambda x: sgn * x["value"]) if prim else None
    dv = [d for d in duals if d.get("value") is not None and math.isfinite(d["value"])]
    bd = max(dv, key=lambda x: sgn * x["value"]) if dv else None
    bold = sorted([d for d in dv if d["bold"]], key=lambda x: -sgn * x["value"])
    p = bp["value"] if bp else None
    d = bd["value"] if bd else None
    return dict(
        name=name, sense=sense,
        problem_type=text(c.get("Problem type", "")),
        nvars=text(c.get("#Variables", "")), nbin=text(c.get("#Binary Variables", "")),
        nint=text(c.get("#Integer Variables", "")), ncons=text(c.get("#Constraints", "")),
        best_primal=p, best_primal_point=bp["point"] if bp else None,
        best_primal_infeas=bp["infeas"] if bp else None,
        n_primal_points=len(prim),
        best_other_point=(min(other, key=lambda x: sgn * x["value"]) if other else None),
        best_dual=d, best_dual_solver=bd["solver"] if bd else None,
        best_dual_date=bd["date"] if bd else None,
        duals=duals,
        third_best_dual=bold[-1]["value"] if len(bold) >= 3 else None,
        gap_best=relgap(p, d), abs_gap_best=(abs(p - d) if p is not None and d is not None else math.inf),
        # dual bound on the wrong side of the listed primal value (min: d > p)
        inconsistent=(p is not None and d is not None and sgn * (p - d) < 0),
        source=text(c.get("Source", "")), application=text(c.get("Application", "")),
        references=text(c.get("References", ""))[:400],
        added=text(c.get("Added to library", "")),
    )


if __name__ == "__main__":
    cands = json.load(open(os.path.join(HERE, "candidates.json")))
    rows = []
    for r in cands:
        rec = parse(r["name"])
        rec.update(census_n=r["n"], census_n_nl=r["n_nl"], tw_fac_ub=r["tw_fac_ub"],
                   tw_nlprimal_ub=r["tw_nlprimal_ub"], metadata_gap=float(r["gap"]))
        rec["keep"] = rec["gap_best"] > 1e-4
        rows.append(rec)
    json.dump(rows, open(os.path.join(HERE, "fetched.json"), "w"), indent=1, default=str)
    cols = ["name", "problem_type", "sense", "nvars", "nbin", "nint", "census_n_nl", "tw_fac_ub",
            "tw_nlprimal_ub", "best_primal", "best_primal_point", "best_primal_infeas", "best_dual",
            "best_dual_solver", "best_dual_date", "gap_best", "abs_gap_best", "inconsistent", "metadata_gap", "keep",
            "application", "source"]
    with open(os.path.join(HERE, "fetched.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in sorted(rows, key=lambda r: r["name"]):
            w.writerow([r[k] for k in cols])
    kept = [r for r in rows if r["keep"]]
    print(len(rows), "parsed;", len(kept), "with best-listed gap > 1e-4")
    nod = [r["name"] for r in rows if r["best_dual"] is None]
    nop = [r["name"] for r in rows if r["best_primal"] is None]
    print("no finite dual:", len(nod), nod)
    print("no feasible primal:", len(nop), nop)
    print("dual beyond primal:", [r["name"] for r in rows if r["inconsistent"]])
