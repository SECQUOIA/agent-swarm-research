"""Necessary-condition test at MINLPLib's feasible points (own code).

For a point x and each period t, every leaf pair (D, D') with s_t(x) in D and
e_t(x) in D' must satisfy
    B_t(D, D') <= cost_t(x) + l_D . s_t(x) - l_D' . e_t(x)      (exact),
with l the LEAF slopes and B_t the exact pair bound (record of ind_verify_cs.py
plus the exact Lemma-2 correction).  Also checks exactly that, along any cell
path of x, the sum of these period values equals f(x) + sum_t l_{t,D_t}.(link-t
residual of x), i.e. that one slope per cell makes the link terms telescope.
Model via the first verifier's vmodel; pickle via stub.

usage: python3 point_check_cs.py cert.pkl.gz ind_verify.json sol1 [sol2 ...]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
from fractions import Fraction as F

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vmodel  # noqa: E402
import load_cs  # noqa: E402
from ind_verify_cs import corr_exact  # noqa: E402

T = 6


def read_sol(path, names):
    idx = {n: i for i, n in enumerate(names)}
    x = [F(0)] * len(names)
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and p[0] != "objvar":
            x[idx[p[0]]] = F(p[1])
    return x


def main():
    d = load_cs.load(sys.argv[1])
    R = json.load(open(sys.argv[2]))
    brid = R["brid"]
    recs, cells, leaves, lam = d["recs"], d["cells"], d["leaves"], d["lam"]
    I = vmodel.instance(T)
    m = I["m"]
    names = m["names"]
    obj = {v: F(a) for v, a in m["obj"]["lin"].items()}

    def pair_bound(t, r, c):
        rec = recs[brid[t][r][c]]
        if rec["bound"] == float("inf"):
            return None
        v = F(rec["bound"])
        if t > 0:
            cid = leaves[t - 1][r]
            v += corr_exact(lam[t - 1][cid], rec["lam_in"], cells[t - 1][cid]["lo"], cells[t - 1][cid]["hi"], 1)
        if t < T - 1:
            cid = leaves[t][c]
            v += corr_exact(lam[t][cid], rec["lam_out"], cells[t][cid]["lo"], cells[t][cid]["hi"], -1)
        return v

    for sol in sys.argv[3:]:
        x = read_sol(sol, names)
        f = sum(a * x[v] for v, a in obj.items())
        s_lev = [None] + [[x[b] for (i, a, b) in I["links"][t - 1]] for t in range(1, T)]   # start copies
        e_lev = [[x[a] for (i, a, b) in I["links"][t]] for t in range(T - 1)] + [None]       # end copies
        cost = [sum(obj.get(v, 0) * x[v] for v in I["per_vars"][t]) for t in range(T)]

        def containing(link, y):
            return [p for p, cid in enumerate(leaves[link])
                    if all(F(cells[link][cid]["lo"][k]) <= y[k] <= F(cells[link][cid]["hi"][k]) for k in range(3))]
        # a point lies in a cell through its link value; the two copies differ by the link residual
        rows = [[0]] + [containing(t - 1, s_lev[t]) for t in range(1, T)]
        cols = [containing(t, e_lev[t]) for t in range(T - 1)] + [[0]]
        assert all(rows) and all(cols), ("point outside all leaves", sol)
        minm = None
        lo_sum = hi_sum = F(0)
        for t in range(T):
            vals = []
            for r in rows[t]:
                for c in cols[t]:
                    val = cost[t]
                    if t > 0:
                        val += sum(F(lam[t - 1][leaves[t - 1][r]][k]) * s_lev[t][k] for k in range(3))
                    if t < T - 1:
                        val -= sum(F(lam[t][leaves[t][c]][k]) * e_lev[t][k] for k in range(3))
                    b = pair_bound(t, r, c)
                    assert b is not None, ("pair of a feasible point proved empty", sol, t)
                    assert val >= b, ("bound above the point's period value", sol, t, float(val - b))
                    minm = val - b if minm is None else min(minm, val - b)
                    vals.append(b)
            lo_sum += min(vals)
            hi_sum += max(vals)
        # telescoping along the first cell path of x
        path = [cols[t][0] for t in range(T - 1)]
        tot = F(0)
        resid = F(0)
        for t in range(T):
            v = cost[t]
            if t > 0:
                v += sum(F(lam[t - 1][leaves[t - 1][path[t - 1]]][k]) * s_lev[t][k] for k in range(3))
            if t < T - 1:
                v -= sum(F(lam[t][leaves[t][path[t]]][k]) * e_lev[t][k] for k in range(3))
                resid += sum(F(lam[t][leaves[t][path[t]]][k]) * (s_lev[t + 1][k] - e_lev[t][k]) for k in range(3))
            tot += v
        assert tot == f + resid
        lres = max(abs(s_lev[t + 1][k] - e_lev[t][k]) for t in range(T - 1) for k in range(3))
        print(f"{sol.split('/')[-1]}: f = {float(f):.6f}; containing leaves per link "
              f"{[cols[t] for t in range(T - 1)]} (entry side {[rows[t] for t in range(1, T)]}); "
              f"smallest margin (value - bound) {float(minm):.4f}; sum of pair bounds along x's cells "
              f"{float(lo_sum):.6f}..{float(hi_sum):.6f}; telescoping exact (max link residual {float(lres):.1e})")


if __name__ == "__main__":
    main()
