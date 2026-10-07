"""Exact-arithmetic support check (lit-core cluster).

Claim checked: for a product grid with node correction d_i(v) = L w_i(v)^2/8
(w_i(v) = largest adjacent interval width, unit integer intervals ignored),
the corrected grid minimum

    b = min_y [F(y) - sum_i d_i(y_i)]

equals the minimum over all grid cells C of the cellwise edge-concave
(Bajaj--Hasan type) vertex bound

    BH(C) = min_{v vertex of C} F(v) - (L/8) sum_i Delta_i(C)^2,

where Delta_i(C) is the width of the i-th interval of C (0 for unit integer
intervals).  Also spot-checks that both are <= F at random rational points of
every cell (support only; not a proof), and the conditional (min-marginal)
version for a fixed coordinate interval.

Run: python3 lit_core_cell_equivalence.py   (a few seconds)
"""
from fractions import Fraction as Fr
import itertools
import random

random.seed(20261003)


def rand_frac(lo, hi, den=16):
    return Fr(random.randint(int(lo * den), int(hi * den)), den)


def make_instance(n):
    # symmetric rational H with some positive diagonal, linear term h
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = Fr(random.randint(-4, 6), random.choice([1, 2, 3]))
        for j in range(i + 1, n):
            if random.random() < 0.7:
                v = Fr(random.randint(-5, 5), random.choice([1, 2, 4]))
                H[i][j] = H[j][i] = v
    h = [Fr(random.randint(-6, 6), random.choice([1, 2, 3])) for _ in range(n)]
    return H, h


def F(H, h, x):
    n = len(x)
    s = Fr(0)
    for i in range(n):
        s += h[i] * x[i]
        for j in range(n):
            s += H[i][j] * x[i] * x[j] / 2
    return s


def graded_grid(lo, hi, integer):
    # random nonuniform grid containing both endpoints
    pts = {lo, hi}
    k = random.randint(1, 4)
    for _ in range(k):
        if integer:
            pts.add(Fr(random.randint(int(lo), int(hi))))
        else:
            pts.add(rand_frac(lo, hi, den=random.choice([4, 8, 12])))
    return sorted(pts)


def intervals(G, integer):
    out = []
    for a, b in zip(G, G[1:]):
        width = b - a
        eff = Fr(0) if (integer and width == 1) else width
        out.append((a, b, eff))
    return out


def node_corr(G, integer, L):
    # L may be a per-coordinate curvature bound L_i
    ivs = intervals(G, integer)
    d = {}
    for v in G:
        w = Fr(0)
        for a, b, eff in ivs:
            if v in (a, b):
                w = max(w, eff)
        d[v] = L * w * w / 8
    return d


def run_one(n, per_coord=False):
    H, h = make_instance(n)
    L = max([H[i][i] for i in range(n)] + [Fr(0)])
    if L == 0:
        L = Fr(1, 2)  # any positive valid bound
    # per-coordinate variant: L_i = max(H_ii, 0) (zero correction where the
    # diagonal is nonpositive); uniform variant: L_i = L for all i
    Ls = [max(H[i][i], Fr(0)) if per_coord else L for i in range(n)]
    is_int = [random.random() < 0.4 for _ in range(n)]
    boxes = []
    grids = []
    for i in range(n):
        lo = Fr(random.randint(-3, 0))
        hi = lo + random.randint(2, 5)
        boxes.append((lo, hi))
        grids.append(graded_grid(lo, hi, is_int[i]))
    corr = [node_corr(grids[i], is_int[i], Ls[i]) for i in range(n)]
    Q = {}
    for y in itertools.product(*grids):
        Q[y] = F(H, h, y) - sum(corr[i][y[i]] for i in range(n))
    b = min(Q.values())
    ivs = [intervals(grids[i], is_int[i]) for i in range(n)]
    best_cell = None
    for cell in itertools.product(*ivs):
        verts = itertools.product(*[(a, bb) for (a, bb, _) in cell])
        vmin = min(F(H, h, v) for v in verts)
        bh = vmin - sum(Ls[k] * cell[k][2] ** 2 for k in range(n)) / 8
        best_cell = bh if best_cell is None else min(best_cell, bh)
        # spot-check validity of the cell bound and of b on this cell
        for _ in range(6):
            x = []
            for i, (a, bb, e) in enumerate(cell):
                if is_int[i]:
                    x.append(random.choice([a, bb]) if e == 0 else
                             Fr(random.randint(int(a), int(bb))))
                else:
                    t = Fr(random.randint(0, 64), 64)
                    x.append(a + t * (bb - a))
            fx = F(H, h, x)
            assert bh <= fx, ("cell bound violated", cell, x)
            assert b <= fx
    assert b == best_cell, (b, best_cell)
    # conditional version: coordinate 0, each interval [a,b']
    i = 0
    m = {}
    for v in grids[i]:
        m[v] = min(val for y, val in Q.items() if y[i] == v)
    for (a, bb, e) in ivs[i]:
        cond = min(m[a], m[bb])
        # min over cells with coordinate-i interval [a,bb] of BH(C)
        others = [ivs[k] for k in range(n) if k != i]
        best = None
        for rest in itertools.product(*others):
            cell = list(rest)
            cell.insert(i, (a, bb, e))
            verts = itertools.product(*[(p, q) for (p, q, _) in cell])
            vmin = min(F(H, h, v) for v in verts)
            bh = vmin - sum(Ls[k] * cell[k][2] ** 2 for k in range(n)) / 8
            best = bh if best is None else min(best, bh)
        # node-correction conditional bound is at most the cellwise one
        # (equality fails only because d_i(a), d_i(bb) may use the *other*
        # adjacent interval of a or bb in coordinate i)
        assert cond <= best, (cond, best)
        # interval-specific sharpening: replace d_i at the endpoint by the
        # interval's own correction L e^2/8; this equals the cellwise value
        sharp = min(m[a] + corr[i][a], m[bb] + corr[i][bb]) - Ls[i] * e * e / 8
        assert cond <= sharp, (cond, sharp)
        assert sharp == best, (sharp, best)
        # validity of the sharpened bound on random points with x_i in [a,bb]
        for _ in range(8):
            x = []
            for k in range(n):
                if k == i:
                    lo_k, hi_k = a, bb
                else:
                    lo_k, hi_k = boxes[k]
                if is_int[k]:
                    x.append(Fr(random.randint(int(lo_k), int(hi_k))))
                else:
                    t = Fr(random.randint(0, 64), 64)
                    x.append(lo_k + t * (hi_k - lo_k))
            assert sharp <= F(H, h, x), ("sharpened conditional bound", x)
    return b


def main():
    count = 0
    for per_coord in (False, True):
        for n in (1, 2, 3):
            for _ in range(40):
                run_one(n, per_coord)
                count += 1
    print(f"PASS: {count} random instances; b == min over cells of the "
          f"edge-concave vertex bound (uniform L and per-coordinate L_i); "
          f"spot checks of validity passed.")


if __name__ == "__main__":
    main()
