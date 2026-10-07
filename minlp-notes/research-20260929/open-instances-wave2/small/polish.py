"""Polish a MINLPLib point to (numerically) exact feasibility with some variables held fixed.

With the listed variables and all fixed-bound variables held at their values, the remaining
rows must form a square system. Newton with exact residuals (mpmath, 60 digits) and a double
precision sparse Jacobian (forward-mode AD per row): each step multiplies the residual by
about cond(J) * 1e-16, so a few steps reach residuals near 1e-50.

Usage: python3 polish.py <name>.<pk> <var> [<var> ...]      (held-fixed variables)
Writes logs/<name>.<pk>.polished.txt (30-digit values) and reports objective and violation.
"""
import os
import sys

import mpmath as mp
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402
import ia  # noqa: E402
import osilx  # noqa: E402
from ia import AD  # noqa: E402

tag = sys.argv[1]
name = tag.split(".")[0]
hold = set(sys.argv[2:])
I = ev.load(name)
N = I["names"]
vals = ev.read_sol(os.path.join(ev.HERE, "sol", tag + ".sol"))
mp.mp.dps = 60
x = [mp.mpf(vals.get(n, "0")) for n in N]
fixed = [j for j in range(len(N)) if I["lb"][j] == I["ub"][j] or N[j] in hold]
for j in range(len(N)):
    if I["lb"][j] == I["ub"][j]:
        x[j] = mp.mpf(I["lb"][j])
free = [j for j in range(len(N)) if j not in set(fixed)]
rows = [c for c in I["cons"]]
assert all(c["lb"] == c["ub"] for c in rows), "only equality rows supported"
assert len(free) == len(rows), (len(free), len(rows))
col = {j: k for k, j in enumerate(free)}


def vars_of(c):
    s = set(c["lin"])
    for a, b, _ in c["quad"]:
        s |= {a, b}
    if c["nl"] is not None:
        s |= _tv(c["nl"])
    return sorted(s)


def _tv(t):
    if t[0] == "var":
        return {t[1]}
    if t[0] == "num":
        return set()
    out = set()
    for c in t[1:]:
        out |= _tv(c)
    return out


RV = [vars_of(c) for c in rows]
FN = {"ln": lambda a: ia.ad_log(a, np.log), "exp": lambda a: ia.ad_exp(a, np.exp)}


def jac(xf):
    ri, ci, vv = [], [], []
    for r, c in enumerate(rows):
        vs = [j for j in RV[r] if j in col]
        loc = {j: k for k, j in enumerate(vs)}
        xa = {}
        for j in RV[r]:
            g = [0.0] * len(vs)
            if j in loc:
                g[loc[j]] = 1.0
            xa[j] = AD(float(xf[j]), tuple(g))
        s = AD(0.0, tuple([0.0] * len(vs)))
        for j, cc in c["lin"].items():
            s = s + xa[j] * float(cc)
        for a, b, cc in c["quad"]:
            s = s + xa[a] * xa[b] * float(cc)
        if c["nl"] is not None:
            s = s + ia.ev_ad(c["nl"], xa, float, FN)
        for j in vs:
            ri.append(r)
            ci.append(col[j])
            vv.append(s.g[loc[j]])
    return sp.csc_matrix((vv, (ri, ci)), shape=(len(rows), len(free)))


def resid(xv):
    return [osilx.ev_row(c, xv, ev.mpnum, ev.MPFNS) - mp.mpf(c["lb"]) for c in rows]


for it in range(8):
    r = resid(x)
    rn = max(abs(v) for v in r)
    print(f"it {it}: max residual {mp.nstr(rn, 3)}", flush=True)
    if rn < mp.mpf("1e-50"):
        break
    J = jac(x)
    dx = spla.spsolve(J, -np.array([float(v) for v in r]))
    step = float(np.max(np.abs(dx)))
    for k, j in enumerate(free):
        x[j] += mp.mpf(float(dx[k]))
    print(f"   step max {step:.3e}", flush=True)
xs = [mp.nstr(v, 30) for v in x]
res = ev.evaluate(I, xs, dps=60)
print(f"{tag} polished ({len(hold)} variables held): obj {mp.nstr(res['obj'], 20)}  max row viol {mp.nstr(res['row_viol'], 3)}  "
      f"bound viol {mp.nstr(res['bound_viol'], 3)} ({res['worst_var']})")
with open(os.path.join(ev.HERE, "logs", f"{tag}.polished.txt"), "w") as f:
    for j, n in enumerate(N):
        f.write(f"{n} {xs[j]}\n")
