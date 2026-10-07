# Copied from /tmp work dir; self-contained (no repository module or data is read).
# Run: OMP_NUM_THREADS=1 python3 r2_band_checks.py > logs/r2_band_checks.log
# Independent spot checks of Theorem 5 (band identity, affine class) and the
# lower bound of Theorem 6 on random 3-bag paths over finite grids (HiGHS LPs,
# floating point; illustration only).  Also Proposition 7 in exact rationals.
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as Fr
rng = np.random.default_rng(20261004)
def lp(c, A, b, nv):
    r = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)]*nv, method="highs")
    assert r.status == 0, r.message
    return r
def dist_aff(s, L, U):            # min delta: L - delta <= lam*s + c <= U + delta
    A=[]; b=[]
    for si, Li, Ui in zip(s, L, U):
        A.append([-si, -1, -1]); b.append(-Li)
        A.append([ si,  1, -1]); b.append(Ui)
    return lp([0, 0, 1], A, b, 3).fun
def delta_aff(s, L, U):           # inf_lam max(L - lam s) + max(lam s - U)
    A=[]; b=[]
    for si, Li, Ui in zip(s, L, U):
        A.append([-si, -1, 0]); b.append(-Li)   # p >= L - lam s
        A.append([ si, 0, -1]); b.append(Ui)    # q >= lam s - U
    return lp([0, 1, 1], A, b, 3).fun
def split_bound(s, t, a, B, c):   # max za+zb+zc over affine splits
    m, k = len(s), len(t); A=[]; b=[]
    # vars: l1, l2, za, zb, zc ; maximize -> minimize negative
    for i in range(m): A.append([-s[i], 0, 1, 0, 0]); b.append(a[i])
    for i in range(m):
        for j in range(k): A.append([s[i], -t[j], 0, 1, 0]); b.append(B[i, j])
    for j in range(k): A.append([0, t[j], 0, 0, 1]); b.append(c[j])
    return -lp([0, 0, -1, -1, -1], A, b, 5).fun
worst5 = 0.0; viol6 = 0; attained = 0; N = 300
for trial in range(N):
    m, k = rng.integers(3, 9), rng.integers(3, 9)
    s = np.sort(rng.uniform(-1, 1, m)); t = np.sort(rng.uniform(-1, 1, k))
    a = rng.normal(size=m) + rng.uniform(0, 2) * s**2
    c = rng.normal(size=k) - rng.uniform(0, 2) * t**2
    B = rng.normal(size=(m, k)) + rng.uniform(-2, 2) * np.outer(s, t)
    fstar = min(a[i] + B[i, j] + c[j] for i in range(m) for j in range(k))
    L1 = fstar - a; U1 = np.array([min(B[i, j] + c[j] for j in range(k)) for i in range(m)])
    G2 = np.array([min(a[i] + B[i, j] for i in range(m)) for j in range(k)]); L2 = fstar - G2; U2 = c
    d1, d2 = dist_aff(s, L1, U1), dist_aff(t, L2, U2)
    worst5 = max(worst5, abs(delta_aff(s, L1, U1) - 2 * d1), abs(delta_aff(t, L2, U2) - 2 * d2))
    gap = fstar - split_bound(s, t, a, B, c)
    if gap < 2 * max(d1, d2) - 1e-9: viol6 += 1
    if abs(gap - 2 * max(d1, d2)) < 1e-7: attained += 1
print(f"Theorem 5, affine class, {2*N} separators: max |inf Delta - 2 dist| = {worst5:.2e}")
print(f"Theorem 6 lower bound on {N} random 3-bag paths: violations {viol6}; lower end attained (1e-7) in {attained}")
# Proposition 7 in exact rationals on a grid (multilinear data: vertex values decide)
g = [Fr(i, 20) for i in range(21)]
a = lambda x: 10 * (1 - x); b = lambda x, y: x + y - x * y; cc = lambda y: 10 * (1 - y)
F = {(x, y): a(x) + b(x, y) + cc(y) for x in g for y in g}
fstar = min(F.values()); Bconst = min(a(x) for x in g) + min(b(x, y) for x in g for y in g) + min(cc(y) for y in g)
V1 = {x: min(b(x, y) + cc(y) for y in g) for x in g}; L1 = {x: fstar - a(x) for x in g}
G2 = {y: min(a(x) + b(x, y) for x in g) for y in g}; L2 = {y: fstar - G2[y] for y in g}
print("Prop 7: f* =", fstar, " constant-split bound =", Bconst,
      " const 1 in Band_1:", all(L1[x] <= 1 <= V1[x] for x in g),
      " const 0 in Band_2:", all(L2[y] <= 0 <= cc(y) for y in g))
