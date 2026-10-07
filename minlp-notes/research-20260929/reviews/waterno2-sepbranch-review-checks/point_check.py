"""Necessary-condition test of the certified pair bounds at known feasible points.

For a point x of waterno2_06 (MINLPLib .sol file), and each period t, every leaf
pair (D, D') with s_t(x) in D and e_t(x) in D' must satisfy
    B_t(D, D') <= cost_t(x) + lam_{t-1}.s_t(x) - lam_t.e_t(x)
(up to the point's own row violation).  The sum of the per-period Lagrangian
values equals f(x) (checked exactly).  Own code; model via the first verifier's
vmodel; pickle via stub loader.

usage: python3 point_check.py cert.pkl sol1 [sol2 ...]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys
from fractions import Fraction as F

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vmodel  # noqa: E402
import load_cert  # noqa: E402

T = 6


def read_sol(path, names):
    idx = {n: i for i, n in enumerate(names)}
    x = [F(0)] * len(names)
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and p[0] != "objvar":
            x[idx[p[0]]] = F(p[1])
    return x


def row_viol(c, x):
    p = vmodel.poly(c)
    s = F(0)
    for mono, a in p.items():
        term = a
        for v in mono:
            term *= x[v]
        s += term
    v = F(0)
    if c["lb"].upper() != "-INF":
        v = max(v, F(c["lb"]) - s)
    if c["ub"].upper() not in ("INF", "+INF"):
        v = max(v, s - F(c["ub"]))
    return v


def main():
    P = load_cert.load(sys.argv[1]).__dict__
    I = vmodel.instance(T)
    m = I["m"]
    names = m["names"]
    lam = P["lam"]
    for sol in sys.argv[2:]:
        x = read_sol(sol, names)
        f = sum(F(a) * x[v] for v, a in m["obj"]["lin"].items())
        allviol = max(row_viol(c, x) for c in m["cons"])
        print(f"{sol}: f = {float(f):.9f}, max row violation (all rows) {float(allviol):.3e}")
        # per-period Lagrangian values
        vals = []
        for t in range(T):
            c = vmodel.period_objective(I, t, lam, 0.0)
            vals.append(sum(a * x[v] for v, a in c.items()))
        assert sum(vals) - f == sum(
            F(lam[t][k]) * (x[b] - x[a]) for t in range(T - 1) for k, (i, a, b) in enumerate(I["links"][t]))
        term = F(1, 2) * x[names.index("x253")] + F(1, 5) * x[names.index("x265")] + F(4, 9) * x[
            names.index("x277")] - F(3913, 900)
        print(f"  terminal row slack at x: {float(term):.6e}")
        lev = [[x[a] for (i, a, b) in I["links"][t]] for t in range(T - 1)]

        def containing(link):
            out = []
            for pos, cid in enumerate(P["leaves"][link]):
                c = P["cells"][link][cid]
                if all(F(c["lo"][k]) <= lev[link][k] <= F(c["hi"][k]) for k in range(3)):
                    out.append(pos)
            return out
        cont = [containing(l) for l in range(T - 1)]
        print("  leaves containing x's levels per link:", cont)
        worst = None
        pathsum = F(0)
        for t in range(T):
            rs = [0] if t == 0 else cont[t - 1]
            cs = [0] if t == T - 1 else cont[t]
            viol = max(row_viol(m["cons"][i], x) for i in I["per_rows"][t])
            bmax = max(P["tables"]["CB"][t][r, c] for r in rs for c in cs)
            gap = vals[t] - F(bmax)
            pathsum += F(bmax)
            worst = gap if worst is None else min(worst, gap)
            print(f"  period {t}: Lagrangian value {float(vals[t]):.6f}, largest pair bound on x's cells "
                  f"{bmax:.6f}, value - bound {float(gap):+.6f}, period row violation {float(viol):.1e}")
        print(f"  sum of pair bounds along x's cells {float(pathsum):.6f} <= f(x) {float(f):.6f}: {pathsum <= f}; "
              f"min (value - bound) {float(worst):+.6f}")


if __name__ == "__main__":
    main()
