"""Search for a counterexample to Corollary 1 as stated in the note:
    delta-minimizer splits  =>  T_eps <= 8 N_opt(eps - delta) - 9.

Target: N_opt(eps - delta) = 2 (breakpoint s) and a chain of 4 internal nodes
(T >= 9 > 7).  The chain follows the child containing s; pattern letters R/L
say on which side of s the split lies.  After len(pattern) splits the last
node must still be invalid.

MILP (scipy/HiGHS), alpha = 1, root [0,1], H = m + y^2 piecewise linear
through knots (optionally convex).  Variables: m_k, eps, delta, margin t,
binaries for the invalidity witness of every chain node and for the knot
attaining min m = eps.  Maximize t.  Positive t => candidate; the candidate
is rounded to rationals and re-verified exactly with exact1d (worst case over
all delta-minimizer choices).

Usage: python3 cor1_milp.py SEED TRIALS CONVEX(0/1)
"""
import random
import sys
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

from exact1d import Inst
from thm1_check import worst_tree


def chain_nodes(s, ys):
    l, u, out = 0.0, 1.0, []
    for y in ys:
        if not (l < y < u) or y == s:
            return None
        out.append((l, u, y))
        if y > s:
            u = y
        else:
            l = y
    out.append((l, u, None))            # final node: must be invalid
    return out


def build(s, ys, extra, convex):
    nodes = chain_nodes(s, ys)
    if nodes is None:
        return None
    xs = sorted(set([0.0, 1.0, s] + list(ys) + list(extra)))
    n = len(xs)
    idx = {x: i for i, x in enumerate(xs)}
    # variable layout: m (n), eps, delta, t, wit (per node per knot), zmin (n)
    nn = len(nodes)
    iE, iD, iT = n, n + 1, n + 2
    iW = n + 3
    iZ = iW + nn * n
    nv = iZ + n
    M = 2.0
    rows, lo, hi = [], [], []

    def add(coef, a, b):
        r = np.zeros(nv)
        for j, c in coef:
            r[j] += c
        rows.append(r); lo.append(a); hi.append(b)

    inf = np.inf
    # m_k >= eps + 0 ; min attained: m_k <= eps + M (1 - z_k), sum z >= 1
    for k in range(n):
        add([(k, 1), (iE, -1)], 0, inf)
        add([(k, 1), (iE, -1), (iZ + k, M)], -inf, M)
    add([(iZ + k, 1) for k in range(n)], 1, inf)
    # delta <= eps - t ; delta >= 0 ; eps <= 0.05
    add([(iD, 1), (iE, -1), (iT, 1)], -inf, 0)
    # certificate [0,s], [s,1] valid at eps - delta:  m_k - delta >= q_J(x_k) + t*0
    for k, x in enumerate(xs):
        if 0 < x < s:
            add([(k, 1), (iD, -1)], x * (s - x), inf)
        elif s < x < 1:
            add([(k, 1), (iD, -1)], (x - s) * (1 - x), inf)
    # convexity of H
    if convex:
        for j in range(1, n - 1):
            h1, h2 = xs[j] - xs[j - 1], xs[j + 1] - xs[j]
            c = -(xs[j] ** 2 - xs[j - 1] ** 2) / h1 + (xs[j + 1] ** 2 - xs[j] ** 2) / h2
            add([(j, 1 / h1 + 1 / h2), (j - 1, -1 / h1), (j + 1, -1 / h2)], -inf, c)
    # chain nodes
    for r_, (l, u, y) in enumerate(nodes):
        ins = [k for k, x in enumerate(xs) if l < x < u]
        q = {k: (xs[k] - l) * (u - xs[k]) for k in ins}
        if y is not None:
            jy = idx[y]
            # delta-minimizer: phi(y) <= phi(k) + delta  for all interior knots k
            for k in ins:
                if k != jy:
                    add([(jy, 1), (k, -1), (iD, -1)], -inf, q[jy] - q[k])
        # invalid: some knot w with phi(w) <= -t
        for k in ins:
            add([(k, 1), (iT, 1), (iW + r_ * n + k, M)], -inf, q[k] + M)
        add([(iW + r_ * n + k, 1) for k in ins], 1, inf)
    A = np.array(rows)
    c = np.zeros(nv); c[iT] = -1
    lb = np.zeros(nv); ub = np.full(nv, 1.0)
    lb[iT] = -1; ub[iE] = 0.05
    integ = np.zeros(nv); integ[iW:] = 1
    res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=integ,
               bounds=Bounds(lb, ub), options={"time_limit": 20})
    if res.x is None:
        return None
    return res.x[iT], xs, res.x[:n], res.x[iE], res.x[iD]


def verify(xs, ms, eps, delta, s):
    """round and re-verify exactly: worst delta-minimizer tree vs 8 N(eps-delta) - 9."""
    X = [Fr(x).limit_denominator(10 ** 9) for x in xs]
    Mv = [Fr(m).limit_denominator(10 ** 12) for m in ms]
    mn = min(Mv)
    I = Inst(X, Mv)
    d = Fr(delta).limit_denominator(10 ** 12)
    d = min(d, I.eps * Fr(999, 1000))
    T = 2 * worst_tree(I, delta=d) + 1
    N1 = len(I.greedy(shift=d)) - 1
    N2 = len(I.greedy(shift=2 * d)) - 1 if 2 * d < I.eps else None
    return T, N1, N2, I, d


def main():
    seed, trials, convex = map(int, sys.argv[1:4])
    rng = np.random.default_rng(seed)
    pats = ["RRR", "RRL", "RLR", "RLL"]
    best = {}
    found = None
    for tr in range(trials):
        pat = pats[tr % len(pats)]
        s = float(rng.uniform(0.2, 0.8))
        ys, l, u = [], 0.0, 1.0
        for ch in pat:
            f = float(np.exp(rng.uniform(-9, 0)))
            if ch == "R":
                y = s + f * (u - s) * float(rng.uniform(0.05, 0.95)); u = y
            else:
                y = s - f * (s - l) * float(rng.uniform(0.05, 0.95)); l = y
            ys.append(y)
        extra = list(rng.uniform(0, 1, 6)) + [s + float(rng.choice([-1, 1])) * float(np.exp(rng.uniform(-10, -2))) for _ in range(4)]
        extra = [x for x in extra if 0 < x < 1]
        r = build(s, ys, extra, convex)
        if r is None:
            continue
        t = r[0]
        if pat not in best or t > best[pat][0]:
            best[pat] = (t, s, ys)
        if t > 1e-9 and found is None:
            T, N1, N2, I, d = verify(r[1], r[2], r[3], r[4], s)
            found = (pat, t, T, N1, N2, float(I.eps), float(d), s, ys)
            print(f"CANDIDATE pattern {pat} margin {t:.3g}: exact T={T}, N(eps-delta)={N1}, "
                  f"bound 8N-9={8*N1-9}; N(eps-2delta)={N2}; eps={float(I.eps):.4g} delta={float(d):.4g}", flush=True)
            print("  knots", [float(x) for x in I.x], flush=True)
            print("  m    ", [float(m) for m in I.m], flush=True)
    for p, (t, s, ys) in best.items():
        print(f"pattern {p}: best margin {t:.3g} (s={s:.3f}, splits-s={[f'{y-s:.3g}' for y in ys]})")


if __name__ == "__main__":
    main()
