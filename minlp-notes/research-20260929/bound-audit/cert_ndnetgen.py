"""Exact repair of a listed nd_netgen point (network design with perspective costs).

Structure (asserted): per arc a binary b, a flow f in [0, U] with f <= U b, a cost variable
u, and s, t defined by  s = (u - b)/2,  t = (u + b)/2  (equality rows), and the cone row
c f^2 + s^2 - t^2 <= 0, i.e. c f^2 <= u b. The remaining equality rows are flow
conservation rows over the flows only.

Repair: b rounded; flows corrected exactly (rational Gaussian elimination on a basis of
flows strictly inside their bounds) so that every conservation row holds exactly;
u := max(listed u, c f^2) where b = 1; s, t from their defining rows. Every row and bound
of the OSIL model is then checked in exact rational arithmetic and the objective is
evaluated exactly.

Usage: python3 cert_ndnetgen.py <name>.<pk>
"""
import json
import os
import sys
from fractions import Fraction

import audit_eval as A
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))


def main(tag):
    name = tag.rsplit(".", 1)[0]
    m = A.load(name)
    vals = A.read_sol(os.path.join(HERE, "sol", tag + ".sol"))
    names, cons = m["names"], m["cons"]
    nv = len(names)
    x = {j: Fraction(vals.get(names[j], "0")) for j in range(nv)}
    for j in range(nv):
        if m["vt"][j] in ("B", "I"):
            x[j] = Fraction(round(x[j]))
    cones = [c for c in cons if c["quad"]]
    defrow = {}  # s or t variable -> its defining row
    for c in cons:
        if c["lb"] == c["ub"] and len(c["lin"]) == 3 and not c["quad"]:
            for j, a in c["lin"].items():
                if Fraction(a) == -1:
                    defrow[j] = c
    arc = []
    for c in cones:
        assert c["ub"] == "0" and c["lb"] == "-INF" and not c["lin"]
        q = {a: Fraction(cf) for a, b, cf in c["quad"]}
        f = [a for a, cf in q.items() if cf > 1][0]
        s = [a for a, cf in q.items() if cf == 1][0]
        t = [a for a, cf in q.items() if cf == -1][0]
        rs, rt = defrow[s], defrow[t]
        u = [j for j in rs["lin"] if j != s and m["vt"][j] == "C"][0]
        b = [j for j in rs["lin"] if m["vt"][j] == "B"][0]
        arc.append(dict(f=f, s=s, t=t, u=u, b=b, c=q[f], rs=rs, rt=rt))
    flows = {a["f"] for a in arc}
    cons_rows = [c for c in cons if c["lb"] == c["ub"] and set(c["lin"]) <= flows and not c["quad"]]
    # exact flow correction
    res = []
    for c in cons_rows:
        v = Fraction(c["lb"]) - Fraction(c["constant"]) - sum((Fraction(a) * x[j] for j, a in c["lin"].items()), Fraction(0))
        res.append(v)
    margin = {j: min(x[j] - Fraction(m["lb"][j]), Fraction(m["ub"][j]) - x[j]) for j in flows}
    rows = [{j: Fraction(a) for j, a in c["lin"].items()} for c in cons_rows]
    rhs = list(res)
    pivots = []
    used_cols = set()
    for i in range(len(rows)):
        cands = [j for j in rows[i] if rows[i][j] != 0 and j not in used_cols and margin[j] > Fraction(1, 10 ** 6)]
        if not cands:
            if rhs[i] != 0:  # no free flow left in this row: it must already hold exactly
                nz = {names[j]: (float(v), float(margin[j]), str(x[j])) for j, v in rows[i].items() if v != 0}
                print("row", cons_rows[i]["name"], "residual", float(rhs[i]), "entries", list(nz.items())[:8])
                raise SystemExit("dependent row with residual")
            continue
        j = max(cands, key=lambda k: margin[k])
        used_cols.add(j)
        piv = rows[i][j]
        for k in range(len(rows)):
            if k != i and rows[k].get(j, 0) != 0:
                f = rows[k][j] / piv
                for jj, a in rows[i].items():
                    rows[k][jj] = rows[k].get(jj, 0) - f * a
                rhs[k] -= f * rhs[i]
        pivots.append((i, j))
    for i, j in pivots:
        # row i now reads sum_{jj} rows[i][jj] delta_jj = rhs[i] with delta = 0 off the pivots
        x[j] += rhs[i] / rows[i][j]
    changed = max(abs(x[j] - Fraction(vals.get(names[j], "0"))) for j in flows)
    for a in arc:
        if x[a["b"]] == 1:
            need = a["c"] * x[a["f"]] ** 2
            if x[a["u"]] < need:
                x[a["u"]] = need
        for v, r in ((a["s"], a["rs"]), (a["t"], a["rt"])):
            val = Fraction(r["lb"]) - Fraction(r["constant"])
            for j, cf in r["lin"].items():
                if j != v:
                    val -= Fraction(cf) * x[j]
            x[v] = val / Fraction(r["lin"][v])
    xs = [x[j] for j in range(nv)]
    bad = []
    for c in cons:
        if not V.row_ok_frac(c, V.row_frac(c, xs)):
            bad.append(c["name"])
    for j in range(nv):
        if (m["lb"][j] != "-INF" and xs[j] < Fraction(m["lb"][j])) or (m["ub"][j] != "INF" and xs[j] > Fraction(m["ub"][j])):
            bad.append(names[j])
        if m["vt"][j] in ("B", "I") and xs[j].denominator != 1:
            bad.append(names[j])
    o = m["obj"]
    assert o["nl"] is None and not o["quad"]
    fobj = Fraction(o["constant"]) + sum((Fraction(cf) * xs[j] for j, cf in o["lin"].items()), Fraction(0))
    out = dict(tag=tag, n_arcs=len(arc), n_conservation_rows=len(cons_rows), max_flow_change=float(changed),
               n_bad=len(bad), bad=bad[:10], status="proved" if not bad else "fail",
               objective_exact_30=str((fobj.numerator * 10 ** 30) // fobj.denominator) + "e-30",
               objective=float(fobj))
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, "logs", f"cert_ndnetgen_{tag}.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
