"""Validate exact_bb.exact_lb: guided face solve vs full face enumeration (both exact), and vs Clarabel (float)."""
import random, sys
from fractions import Fraction as Fr
import numpy as np, cvxpy as cp
import exact_bb as E
random.seed(1)
def rbox(n, depth=6):
    l, u = [], []
    for _ in range(n):
        a, c = sorted(random.sample(range(-2**depth, 2**depth + 1), 2))
        l.append(Fr(a, 2**depth)); u.append(Fr(c, 2**depth))
    return l, u
mism = 0; worst = 0.0; cnt = 0
for n in (2, 3, 4):
    for t in range(60 if n < 4 else 25):
        # mix: random boxes and boxes with a vertex at 0 (degenerate, like the B&B)
        l, u = rbox(n)
        if t % 2:
            s = [random.choice((-1, 1)) for _ in range(n)]
            W = [Fr(random.randint(1, 16), 16) for _ in range(n)]
            l = [min(0, s[i] * W[i]) for i in range(n)]; u = [max(0, s[i] * W[i]) for i in range(n)]
        g, _ = E.exact_lb(l, u, allow_enum=False)
        en, _ = E.enum_lb(l, u)
        lf, uf = np.array([float(x) for x in l]), np.array([float(x) for x in u])
        x = cp.Variable(n); w = cp.Variable(n - 1)
        cons = [x >= lf, x <= uf, w >= cp.multiply(lf[1:], x[:-1]) + cp.multiply(lf[:-1], x[1:]) - lf[:-1] * lf[1:],
                w >= cp.multiply(uf[1:], x[:-1]) + cp.multiply(uf[:-1], x[1:]) - uf[:-1] * uf[1:]]
        pr = cp.Problem(cp.Minimize(cp.sum_squares(x) + 0.8 * cp.sum(w)), cons); pr.solve(solver="CLARABEL", tol_gap_abs=1e-12, tol_gap_rel=1e-12, tol_feas=1e-12)
        cnt += 1
        if g is None or g != en:
            mism += 1; print("MISMATCH", n, l, u, g, en)
        worst = max(worst, abs(float(en) - pr.value))
print(f"validate: {cnt} boxes (n=2,3,4; half with a vertex at x*=0): guided==enumeration on all but {mism}; "
      f"max |exact - Clarabel| = {worst:.1e}; guided={E.STATS['guided']}")
