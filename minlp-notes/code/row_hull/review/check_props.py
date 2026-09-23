"""Independent checks of Propositions 3, 4, 5, 6, the lattice corollary and the Shapley-Folkman
count in results/row-hull-separable-concave.md. Exact rational arithmetic except where an LP is used."""
import itertools
import random
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import linprog

rnd = random.Random(7)


def vertices(ws, B):
    """All (S, j, r) with r = B - w(S) in [0, w_j]; returns list of (z, j, r)."""
    n = len(ws)
    out = []
    for j in range(n):
        others = [i for i in range(n) if i != j]
        for pat in itertools.product((0, 1), repeat=n - 1):
            z = [Fr(0)] * n
            for p, i in zip(pat, others):
                z[i] = ws[i] * p
            r = B - sum(z)
            if 0 <= r <= ws[j]:
                z[j] = r
                out.append((tuple(z), j, r))
    return out


def make_gamma(kind, c, w):
    if kind == "quad":
        return lambda z: c * z * (w - z)
    if kind == "tent":          # concave piecewise linear, peak at w/3
        p = w / 3
        return lambda z: c * min(z / p, (w - z) / (w - p))
    if kind == "fixed":         # chord gap of a fixed charge: jump at 0
        return lambda z: Fr(0) if z == 0 else c * (1 - z / w)
    if kind == "zero":
        return lambda z: Fr(0)
    raise ValueError(kind)


def prop3(ws, B, gammas):
    """Returns (nondegenerate, number of vertex points violating the Prop. 3 inequality)."""
    n = len(ws)
    V = vertices(ws, B)
    nondeg = all(0 < r < ws[j] for _, j, r in V)
    a, b = {}, {}
    for _, j, r in V:
        if 0 < r < ws[j]:
            a[j] = min(a.get(j, r), r)
            b[j] = max(b.get(j, r), r)
    delta = {i: min(gammas[i](a[i]), gammas[i](b[i])) for i in a}
    bad = 0
    for z, j, r in V:
        tau = [gammas[i](z[i]) for i in range(n)]
        lhs = Fr(0)
        for i in a:
            ent = [z[i] / a[i], (ws[i] - z[i]) / (ws[i] - b[i])]
            if delta[i] != 0:
                ent.append(tau[i] / delta[i])
            lhs += min(ent)
        if lhs < 1:
            bad += 1
    return nondeg, bad, len(V)


def run_prop3():
    kinds = ["quad", "tent", "fixed", "zero"]
    stats = {"nondeg_ok": 0, "nondeg_bad": 0, "deg_ok": 0, "deg_bad": 0}
    for _ in range(400):
        n = rnd.randint(2, 6)
        ws = [Fr(rnd.randint(1, 7)) for _ in range(n)]
        B = Fr(rnd.randint(1, 2 * int(sum(ws)) - 1), 2)      # half-integers: both degenerate and nondegenerate cases
        if not 0 < B < sum(ws):
            continue
        gammas = [make_gamma(rnd.choice(kinds), Fr(rnd.randint(1, 5)), ws[i]) for i in range(n)]
        nondeg, bad, nv = prop3(ws, B, gammas)
        key = ("nondeg" if nondeg else "deg") + ("_bad" if bad else "_ok")
        stats[key] += 1
    print("Prop 3, random unequal widths:", stats)
    print("  (nondeg_bad must be 0; deg_ok must be 0 if the hypothesis is also necessary)")

    # lattice corollary: interior values lie in [r, w_i - g + r]
    viol = 0
    for _ in range(300):
        n = rnd.randint(2, 6)
        g = Fr(rnd.randint(1, 4), rnd.randint(1, 3))
        ws = [g * rnd.randint(1, 4) for _ in range(n)]
        r = g * Fr(rnd.randint(1, 9), 10)
        q = rnd.randint(0, int(sum(ws) / g) - 1)
        B = q * g + r
        for _, j, rv in vertices(ws, B):
            if not (0 < rv < ws[j] and r <= rv <= ws[j] - g + r):
                viol += 1
    print("lattice corollary: vertex interior values outside [r, w_i - g + r]:", viol)

    # "is the hull for equal widths and is weaker otherwise": unequal widths where Prop. 3 IS the hull
    ws, B = [Fr(1), Fr(2)], Fr(3, 2)
    V = vertices(ws, B)
    print("n=2, w=(1,2), B=3/2, gamma_2 = z(2-z): vertices", sorted({(z, j, r) for z, j, r in V}))
    print("  item 1 is never interior; a_2=1/2, b_2=3/2, delta_2 = 3/4 = gamma_2 at both vertices,")
    print("  so Prop. 3 reads tau_2 >= 3/4 on the segment X, which is exactly conv of the two vertex points + rays.")


def run_prop4():
    # min sum tau over Q = min over vertices of r (w_j - r); zero iff a subset sums to B
    mism = 0
    for _ in range(300):
        n = rnd.randint(2, 7)
        ws = [Fr(rnd.randint(1, 9)) for _ in range(n)]
        B = Fr(rnd.randint(1, int(sum(ws)) * 2 - 1), rnd.choice([1, 2]))
        if not 0 <= B <= sum(ws):
            continue
        V = vertices(ws, B)
        val = min(sum(z[i] * (ws[i] - z[i]) for i in range(n)) for z, _, _ in V)
        subset = any(sum(w for w, p in zip(ws, pat) if p) == B for pat in itertools.product((0, 1), repeat=n))
        if (val == 0) != subset:
            mism += 1
    print("Prop 4: instances where (min = 0) != (subset sum exists):", mism)


def run_prop5():
    """Interval-merged leave-one-out pricing: L_merged <= exact min phi, including fixed-charge jumps."""
    worst_slack, viol = Fr(0), 0
    for _ in range(300):
        n = rnd.randint(3, 7)
        ws = [Fr(rnd.randint(1, 9), rnd.choice([1, 2, 3])) for _ in range(n)]
        B = Fr(rnd.randint(1, 60), 7)
        if not 0 < B < sum(ws):
            continue
        kinds = [rnd.choice(["quad", "tent", "fixed", "zero"]) for _ in range(n)]
        gam = [make_gamma(kinds[i], Fr(rnd.randint(1, 5)), ws[i]) for i in range(n)]
        pi = [Fr(rnd.randint(-5, 5), 2) for _ in range(n)]
        om = [Fr(rnd.randint(0, 4)) for _ in range(n)]
        V = vertices(ws, B)
        exact = min(om[j] * gam[j](r) - pi[j] * r - sum(pi[i] * z[i] for i in range(n) if i != j) for z, j, r in V)
        K = rnd.randint(1, 4)
        L = None
        for j in range(n):
            others = [i for i in range(n) if i != j]
            states = [(Fr(0), Fr(0), Fr(0))]             # (lo, hi, best profit)
            for i in others:
                new = states + [(lo + ws[i], hi + ws[i], p + pi[i] * ws[i]) for lo, hi, p in states]
                new.sort()
                while len(new) > K:                       # merge the two closest neighbours
                    t = min(range(len(new) - 1), key=lambda s: new[s + 1][0] - new[s][1])
                    a_, b_ = new[t], new[t + 1]
                    new[t:t + 2] = [(a_[0], max(a_[1], b_[1]), max(a_[2], b_[2]))]
                states = new
            for lo, hi, p in states:
                rlo, rhi = max(B - hi, Fr(0)), min(B - lo, ws[j])     # r = B - w(S), clipped to [0, w_j]
                if rlo > rhi:
                    continue
                h = lambda r_: om[j] * gam[j](r_) - pi[j] * r_
                cand = min(h(rlo), h(rhi)) - p
                L = cand if L is None else min(L, cand)
        if L > exact:
            viol += 1
        worst_slack = max(worst_slack, exact - L)
    print("Prop 5: merged lower bound exceeded exact minimum in", viol, "instances (must be 0); largest slack", float(worst_slack))


def run_prop6():
    # feasible set
    import sympy as sp
    x1, x2, x3 = sp.symbols("x1 x2 x3")
    sol = sp.solve([x1 + x2 + x3 - 2, x1 + x2 - x3 - 1], [x2, x3], dict=True)[0]
    print("Prop 6: rows imply", sol)                       # x3 = 1/2, x2 = 3/2 - x1
    # x1 in [1/2, 1]; end points
    g = lambda x: x * (1 - x)
    for p in [(Fr(1), Fr(1, 2), Fr(1, 2)), (Fr(1, 2), Fr(1), Fr(1, 2)), (Fr(3, 4), Fr(3, 4), Fr(1, 2))]:
        print("  point", p, "row1", sum(p), "row2", p[0] + p[1] - p[2], "sum gamma", sum(g(v) for v in p))
    obj = sp.expand(sum(v * (1 - v) for v in (x1, sol[x2], sol[x3])))
    print("  objective on the segment:", obj, "-> concave, end values", obj.subs(x1, sp.Rational(1, 2)), obj.subs(x1, 1))
    # row 2 normalized: z3 = 1 - x3 -> z1+z2+z3 = 1 - 1 + ... check B
    print("  row 2 normalized right-hand side B = 1 + 1 =", 2, "(integral, unit widths) -> r = 0 for both rows")
    # aggregated rows: 2 x3 = 1 (w=2,k=0,r=1) and 2x1+2x2 = 3 (w=2,k=1,r=1); delta = gamma(x=1/2) = 1/4
    # LP: min tau1+tau2+tau3 over both rows, box, tau>=0, EF of the two aggregated rows
    # variables x1,x2,x3,t1,t2,t3,zeta1,zeta2 (row A: items 1,2), zeta3 (row B)
    c = [0, 0, 0, 1, 1, 1, 0, 0, 0]
    A_eq = [[1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1]]
    b_eq = [2, 1, 1, 1]
    A_ub, b_ub = [], []
    for i, zc in ((0, 6), (1, 7), (2, 8)):
        row = [0] * 9; row[zc] = 1; row[i] = -2; A_ub.append(row); b_ub.append(0)       # r zeta <= z = 2x
        row = [0] * 9; row[zc] = 1; row[i] = 2; A_ub.append(row); b_ub.append(2)        # (w-r) zeta <= w - z
        row = [0] * 9; row[zc] = 0.25; row[3 + i] = -1; A_ub.append(row); b_ub.append(0)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, 1)] * 3 + [(0, None)] * 6, method="highs")
    print("  bound with row hulls of the two aggregated rows:", res.fun, "(claimed 1/2)")
    res0 = linprog(c[:6], A_eq=[r_[:6] for r_ in A_eq[:2]], b_eq=b_eq[:2], bounds=[(0, 1)] * 3 + [(0, None)] * 3, method="highs")
    print("  bound with original row hulls (= term-wise, r = 0):", res0.fun, "(claimed 0)")


def run_sf():
    """Basic optimal solutions of the term-wise relaxation: number of x strictly inside bounds <= m."""
    rng = np.random.default_rng(3)
    worst = 0
    for _ in range(60):
        n, m = int(rng.integers(4, 12)), int(rng.integers(1, 4))
        A = rng.integers(-3, 4, size=(m, n)).astype(float)
        x0 = rng.uniform(0.2, 0.8, n)
        b = A @ x0
        neq = int(rng.integers(0, m + 1))                   # first neq rows equalities, rest <=
        slope = rng.normal(size=n)                          # chord slopes + linear costs
        res = linprog(slope, A_eq=A[:neq] if neq else None, b_eq=b[:neq] if neq else None,
                      A_ub=A[neq:] if neq < m else None, b_ub=(b[neq:] + rng.uniform(0, 0.3, m - neq)) if neq < m else None,
                      bounds=[(0, 1)] * n, method="highs-ds")
        assert res.status == 0
        interior = int(np.sum((res.x > 1e-9) & (res.x < 1 - 1e-9)))
        worst = max(worst, interior - m)
    print("Shapley-Folkman count: max (interior variables - m) over 60 random LPs with mixed =/<= rows:", worst, "(must be <= 0)")


if __name__ == "__main__":
    run_prop3()
    run_prop4()
    run_prop5()
    run_prop6()
    run_sf()
