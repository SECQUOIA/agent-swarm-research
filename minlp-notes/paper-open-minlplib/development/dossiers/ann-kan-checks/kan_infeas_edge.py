"""Independent exact check (dossier author): OSIL infeasibility of a KAN model via one edge.

For the edge whose argument is variable ZV: fix the edge's one-hot binaries to e_k for every
piece k whose big-M interval I_k meets the argument's own variable bounds (a superset of the
input-class box, so the test is conservative), propagate the equality rows that involve only
ZV, the edge binaries and still-unknown continuous variables (each solved for its single
unknown, which must enter linearly with a nonzero constant coefficient), and test whether the
three partition rows (continuous variables, all coefficients 1, rhs 1) can hold simultaneously
for some z in I_k ∩ bounds.  Exact rationals (sympy QQ) only.
usage: python3 kan_infeas_edge.py <instance> <edge-argument-variable>
"""
import os, sys
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import osilx

name, ZV = sys.argv[1], sys.argv[2]
I = osilx.read(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
N, cons, vt = I["names"], I["cons"], I["vt"]
idx = {n: j for j, n in enumerate(N)}
zj = idx[ZV]
z = sp.Symbol("z")
Q = lambda s: sp.Rational(Fr(s).numerator, Fr(s).denominator)

def rvars(c):
    s = set(c["lin"]) | {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}
    assert c["nl"] is None or True
    return s

# big-M rows: linear rows with exactly ZV and at most one binary
bins, lo_rows, hi_rows = set(), {}, {}
for c in cons:
    if c["nl"] is not None or c["quad"] or zj not in c["lin"]:
        continue
    vs = set(c["lin"])
    bs = [j for j in vs if vt[j] == "B"]
    if vs - {zj} - set(bs) or len(bs) > 1 or not osilx.isinf(c["lb"]):
        continue
    a = Q(c["lin"][zj]); ub = Q(c["ub"])
    b = bs[0] if bs else None
    cb = Q(c["lin"][b]) if b is not None else 0
    if b is not None:
        bins.add(b)
    # a*z + cb*bin <= ub
    (hi_rows if a > 0 else lo_rows)[b] = (a, cb, ub)
bins = sorted(bins)
# the one-hot row of these binaries
onehot = [c for c in cons if c["nl"] is None and not c["quad"] and set(c["lin"]) == set(bins)]
assert len(onehot) == 1 and onehot[0]["lb"] == onehot[0]["ub"] == "1"
zlo, zhi = Q(I["lb"][zj]), Q(I["ub"][zj])
print(f"{name}: edge argument {ZV}, own bounds [{float(zlo)}, {float(zhi)}], {len(bins)} binaries")

def interval_for(bk):
    """[lo, hi] for z when bin bk = 1 and all others 0 (from all big-M rows)."""
    lo, hi = -sp.oo, sp.oo
    for b, (a, cb, ub) in list(hi_rows.items()) + list(lo_rows.items()):
        val = (cb if b == bk else 0)
        bound = (ub - val) / a           # a z <= ub - val
        if a > 0:
            hi = min(hi, bound)
        else:
            lo = max(lo, bound)
    return lo, hi

def is_partition(c):
    return (c["nl"] is None and not c["quad"] and c["lb"] == c["ub"] and Fr(c["lb"]) == 1
            and c["lin"] and all(Fr(a) == 1 for a in c["lin"].values())
            and not any(vt[j] == "B" for j in c["lin"]))

n_inf = 0; n_adm = 0
for bk in bins:
    a, b = interval_for(bk)
    A, B = max(a, zlo), min(b, zhi)
    if A > B:
        continue
    n_adm += 1
    val = {zj: sp.Poly(z, z, domain="QQ")}
    for bb in bins:
        val[bb] = sp.Poly(1 if bb == bk else 0, z, domain="QQ")
    changed = True
    used = set()
    while changed:
        changed = False
        for r, c in enumerate(cons):
            if r in used or c["nl"] is not None or c["lb"] != c["ub"] or osilx.isinf(c["lb"]) or is_partition(c):
                continue
            vs = rvars(c)
            unk = [j for j in vs if j not in val]
            if len(unk) != 1:
                continue
            v = unk[0]
            # only rows local to this edge: every known variable must be z, a binary of the edge, or a solved basis var
            if vt[v] == "B":
                continue
            if any(v in (p, q) for p, q, _ in c["quad"]):
                continue
            coef = Q(c["lin"].get(v, 0))
            if coef == 0:
                continue
            rest = sp.Poly(0, z, domain="QQ")
            for j, s in c["lin"].items():
                if j != v:
                    rest += Q(s) * val[j]
            for p, q, s in c["quad"]:
                rest += Q(s) * val[p] * val[q]
            val[v] = (sp.Poly(Q(c["lb"]), z, domain="QQ") - rest) * (1 / coef)
            used.add(r); changed = True
    # stop propagation leaking beyond the edge: restrict to partition rows whose variables are all solved
    parts = [c for c in cons if is_partition(c) and all(j in val for j in c["lin"])]
    res = []
    for c in parts:
        p = sp.Poly(0, z, domain="QQ")
        for j in c["lin"]:
            p += val[j]
        p -= 1
        res.append((c["name"], p))
    nz = [(nm, p) for nm, p in res if not p.is_zero]
    g = None
    for nm, p in nz:
        g = p if g is None else sp.gcd(g, p)
    if g is None:
        verdict = "NOT certified (all residuals vanish identically)"
    elif g.degree() == 0:
        verdict = "infeasible (residuals have no common root at all)"; n_inf += 1
    else:
        cnt = g.count_roots(A, B)
        verdict = f"common-root count in [{float(A):.6f},{float(B):.6f}] = {cnt}"
        if cnt == 0:
            n_inf += 1; verdict = "infeasible (" + verdict + ")"
    degs = [(nm, p.degree(), float(max(abs(x) for x in p.all_coeffs()))) for nm, p in res]
    print(f"  piece bin {N[bk]}: z in [{float(A):.6f}, {float(B):.6f}]; partition residuals (row, degree, max|coef|) {degs}; {verdict}")
print(f"{name}/{ZV}: {n_inf} of {n_adm} admissible pieces certified infeasible"
      + (" => the OSIL model has no exactly feasible point" if n_inf == n_adm else ""))
