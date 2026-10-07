"""Uniform dyadic mesh with unions of retained cells (no hulls) on instances
with several isolated optima. Checks: valid lower bounds, every optimizer
retained, per-coordinate node counts stay bounded independently of the
stage, and below the proved cap K_S = 12 r (2 sqrt(n kappa) + 1) computed with a
sampled-growth upper estimate of kappa (the cap is informational; validity
does not depend on it). Continuous coordinates only. Part (3) runs UC + snapping recovery +
candidate-denominator acceptance end to end.
"""
import math
import random
from fractions import Fraction as Fr
from itertools import product

random.seed(5)


def run(Ffun, Ldiag, bounds, S, J, label):
    n = len(bounds)
    Fstar = Ffun(S[0])
    s = max(u - l for l, u in bounds)
    cells = [[(l, u)] for l, u in bounds]
    U = Ffun([l for l, _ in bounds])
    yinc = [l for l, _ in bounds]
    counts = []
    for j in range(J + 1):
        h = s / 2 ** j
        grids, wid = [], []
        newcells = []
        for i in range(n):
            l = bounds[i][0]
            nodes = set()
            sub = []
            for a, b in cells[i]:
                pts = {a, b}
                k0 = math.ceil((a - l) / h)
                k = k0
                while l + k * h < b:
                    if l + k * h > a:
                        pts.add(l + k * h)
                    k += 1
                pts = sorted(pts)
                sub.extend(zip(pts, pts[1:]))
                nodes.update(pts)
            nodes = sorted(nodes)
            w = {v: Fr(0) for v in nodes}
            for a, b in sub:
                w[a] = max(w[a], b - a)
                w[b] = max(w[b], b - a)
            grids.append(nodes)
            wid.append(w)
            newcells.append(sub)
        counts.append([len(g) for g in grids])
        marg = [dict() for _ in range(n)]
        best, arg = None, None
        for y in product(*grids):
            q = Ffun(list(y)) - sum(Ldiag[i] * wid[i][y[i]] ** 2 / 8 for i in range(n))
            if best is None or q < best:
                best, arg = q, y
            for i in range(n):
                if y[i] not in marg[i] or q < marg[i][y[i]]:
                    marg[i][y[i]] = q
        assert best <= Fstar
        if Ffun(list(arg)) < U:
            U, yinc = Ffun(list(arg)), list(arg)
        cells = []
        for i in range(n):
            kept = [(a, b) for a, b in newcells[i] if min(marg[i][a], marg[i][b]) <= U]
            cells.append(kept)
            for sopt in S:
                assert any(a <= sopt[i] <= b for a, b in kept)
    print(label, "gap", float(U - best), "node counts per stage:", counts)
    return counts


# (1) F_M(x,z) = x^2 - 2xz + Mz on [0,M]^2, S = {(0,0),(M,M)}; g >= 1/20.
M = 64
c1 = run(lambda v: v[0] ** 2 - 2 * v[0] * v[1] + M * v[1], [Fr(2), Fr(0)],
         [(Fr(0), Fr(M))] * 2, [[Fr(0), Fr(0)], [Fr(M), Fr(M)]], 11, "F_64")
cap1 = 12 * 2 * (2 * math.sqrt(2 * 40) + 1)  # K_S = 12 r (2 sqrt(n kappa) + 1)
assert max(max(c) for c in c1) <= cap1
print("  cap with r=2, n=2, kappa<=40:", round(cap1, 1))

# (2) wells: x1(1-x1) + x2(1-x2) + (x3-(x1+x2)/2)^2 - 1/2 + 1/2, S = 4 points,
#     projections {0,1},{0,1},{0,1/2,1}; L = 2 on x3, others concave.
def f2(v):
    return v[0] * (1 - v[0]) + v[1] * (1 - v[1]) + (v[2] - (v[0] + v[1]) / 2) ** 2


S2 = [[Fr(a), Fr(b), Fr(a + b, 2)] for a in (0, 1) for b in (0, 1)]
# sampled growth estimate
worst = None
for _ in range(3000):
    v = [Fr(random.randint(0, 300), 300) for _ in range(3)]
    d2 = min(sum((v[i] - s[i]) ** 2 for i in range(3)) for s in S2)
    if d2:
        r = f2(v) / d2
        worst = r if worst is None or r < worst else worst
print("  wells sampled growth ratio min:", float(worst))
c2 = run(f2, [Fr(0), Fr(0), Fr(2)], [(Fr(0), Fr(1))] * 3, S2, 8, "wells")
kappa2 = 2 / float(worst)
cap2 = 12 * 3 * (2 * math.sqrt(3 * kappa2) + 1)
assert max(max(c) for c in c2) <= cap2
print("  cap with r=3, n=3, sampled kappa:", round(cap2, 1))


# (3) End-to-end exact output: UC certificate + snapping recovery (REC) +
#     candidate-denominator acceptance, on the two instances above.
from exact_common import heights, value
from exact_check_recovery import recover


def uc_final(Ffun, Ldiag, bounds, J):
    """Rerun UC and return (incumbent, beta) after stage J."""
    n = len(bounds)
    s = max(u - l for l, u in bounds)
    cells = [[(l, u)] for l, u in bounds]
    yinc = [l for l, _ in bounds]
    U = Ffun(yinc)
    for j in range(J + 1):
        h = s / 2 ** j
        grids, wid, newcells = [], [], []
        for i in range(n):
            l = bounds[i][0]
            sub, nodes = [], set()
            for a, b in cells[i]:
                pts = {a, b}
                k = math.ceil((a - l) / h)
                while l + k * h < b:
                    if l + k * h > a:
                        pts.add(l + k * h)
                    k += 1
                pts = sorted(pts)
                sub.extend(zip(pts, pts[1:]))
                nodes.update(pts)
            w = {v: Fr(0) for v in nodes}
            for a, b in sub:
                w[a] = max(w[a], b - a)
                w[b] = max(w[b], b - a)
            grids.append(sorted(nodes)); wid.append(w); newcells.append(sub)
        marg = [dict() for _ in range(n)]
        best, arg = None, None
        for y in product(*grids):
            q = Ffun(list(y)) - sum(Ldiag[i] * wid[i][y[i]] ** 2 / 8 for i in range(n))
            if best is None or q < best:
                best, arg = q, y
            for i in range(n):
                if y[i] not in marg[i] or q < marg[i][y[i]]:
                    marg[i][y[i]] = q
        if Ffun(list(arg)) < U:
            U, yinc = Ffun(list(arg)), list(arg)
        cells = [[(a, b) for a, b in newcells[i] if min(marg[i][a], marg[i][b]) <= U]
                 for i in range(n)]
    return yinc, best


cases = [
    ("F_64", [[Fr(2), Fr(-2)], [Fr(-2), Fr(0)]], [Fr(0), Fr(64)], Fr(0),
     [(Fr(0), Fr(64))] * 2, Fr(0)),
    ("wells", [[Fr(-3, 2), Fr(1, 2), Fr(-1)], [Fr(1, 2), Fr(-3, 2), Fr(-1)],
               [Fr(-1), Fr(-1), Fr(2)]], [Fr(1), Fr(1), Fr(0)], Fr(0),
     [(Fr(0), Fr(1))] * 3, Fr(0)),
]
for name, H, b, c, bounds, Fstar in cases:
    hs = heights(H, b, c, bounds, set())
    R, V = hs["R_had"], hs["V_had"]
    tau = Fr(1, 4 * len(b) * R)
    f = lambda v, H=H, b=b, c=c: value(H, b, c, v)
    Ld = [max(H[i][i], Fr(0)) for i in range(len(b))]
    for J in range(2, 16):
        y, beta = uc_final(f, Ld, bounds, J)
        x, free = recover(H, b, bounds, set(), y, tau)
        if x is None or not all(bounds[i][0] <= x[i] <= bounds[i][1] for i in range(len(b))):
            continue
        Fx = f(x)
        if Fx - beta < Fr(1, V * Fx.denominator):
            assert Fx == Fstar
            print(f"  exact output for {name} at stage {J}: x={[str(t) for t in x]}, "
                  f"F={Fx}, R={R}, V={V}, gap at acceptance={float(f(y) - beta):.3g}")
            break
    else:
        raise AssertionError("no acceptance for " + name)
