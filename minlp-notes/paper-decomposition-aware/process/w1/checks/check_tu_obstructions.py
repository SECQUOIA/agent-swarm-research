"""Exact checks for the structural-limit statements of the TU cluster.

(1) Tightness of the uniform-mesh state count. Separable box instance
    F = (L/2) sum_i (x_i - 1/2)^2 on [0,1]^n (A empty, hence TU).
    With uniform mesh, uniform allowance E_j = n L h^2/8, U_j = v_j = 0, every
    level keeps >= 2*floor(sqrt(n)/2)+1 nodes and the next grid has
    4*(floor(sqrt(n)/2)+1)+1 >= 2 sqrt(n) + 1 nodes per coordinate. Growth
    g = L/2, so the upper bound is 5 + floor(2 sqrt(2n)).
(2) Curvature-only unary corrections are unsound on non-aligned grids for an
    order constraint x1 <= x2: F_lam = (L/2)((x1-m)^2+(x2-m)^2) + lam (x2-x1),
    F* = 0 at (m,m), Hess = L I, growth L/2, but min_grid (F - D) > 0.
    Done for {0,1/2,1} x {0,1/3,1} and for the graded grids of the box theorem
    built around two different feasible centres.
(3) Same failure for a sum equality x1 + x2 = x3 with a *common* graded offset
    pattern around a feasible centre (no multiplier needed).
"""
import math
from fractions import Fraction as Fr
from itertools import product


# ---------- (1) tightness ----------

def uniform_tightness(n, levels=9, L=Fr(1)):
    out = []
    lo, hi = Fr(0), Fr(1)
    for j in range(1, levels + 1):
        h = Fr(1, 2 ** j)
        nodes = []
        t = lo
        while t <= hi:
            nodes.append(t)
            t += h
        E = n * L * h * h / 8
        U = Fr(0)               # all centres are grid nodes: v_j = F* = 0
        Mi = {t: L / 2 * (t - Fr(1, 2)) ** 2 for t in nodes}
        kept = [(a, a + h) for a in nodes[:-1] if min(Mi[a], Mi[a + h]) - E <= U]
        lo, hi = kept[0][0], kept[-1][1]
        nxt = int((hi - lo) / (h / 2)) + 1
        bound = 5 + math.isqrt(math.floor(4 * n * L / (L / 2)))
        assert nxt <= bound
        if lo > 0 and hi < 1:       # window not clipped by the box
            assert (nxt - 1) ** 2 >= 4 * n, (n, j, nxt)   # nxt >= 2 sqrt(n) + 1
        out.append(nxt)
    return out


# ---------- grids of the box theorem ----------

def graded_grid(c, lo, hi, h, theta):
    """Nodes built outward from c with steps h + theta*t, clipped to [lo,hi]."""
    pts = {c}
    for sgn in (1, -1):
        t = Fr(0)
        while True:
            t = t + h + theta * t
            p = c + sgn * t
            if p >= hi:
                pts.add(hi)
                break
            if p <= lo:
                pts.add(lo)
                break
            pts.add(p)
    return sorted(pts)


def corr(grid, L):
    """d(v) = L * (largest adjacent interval)^2 / 8."""
    d = {}
    for k, v in enumerate(grid):
        w = Fr(0)
        if k > 0:
            w = max(w, v - grid[k - 1])
        if k + 1 < len(grid):
            w = max(w, grid[k + 1] - v)
        d[v] = L * w * w / 8
    return d


def order_unsound(G1, G2, m, L, lam):
    d1, d2 = corr(G1, L), corr(G2, L)
    best = None
    for y1 in G1:
        for y2 in G2:
            if y1 <= y2:
                q = L / 2 * ((y1 - m) ** 2 + (y2 - m) ** 2) + lam * (y2 - y1) - d1[y1] - d2[y2]
                best = q if best is None or q < best else best
    return best


def graded_order_example():
    L = Fr(1)
    h, theta = Fr(1, 16), Fr(1, 4)
    G1 = graded_grid(Fr(3, 10), Fr(0), Fr(1), h, theta)
    G2 = graded_grid(Fr(7, 10), Fr(0), Fr(1), h, theta)
    common = sorted(set(G1) & set(G2))
    # midpoint of the largest gap of the common nodes
    gaps = [(b - a, a, b) for a, b in zip(common, common[1:])]
    w, a, b = max(gaps)
    m = (a + b) / 2
    lam = Fr(10 ** 6)
    val = order_unsound(G1, G2, m, L, lam)
    return G1, G2, common, m, val


# ---------- (3) sum equality with a common offset pattern ----------

def offsets(h, theta, R):
    o = [Fr(0)]
    t = Fr(0)
    while t < R:
        t = t + h + theta * t
        o.append(t)
    return sorted(set(o) | {-v for v in o})


def sum_equality_example():
    L = Fr(1)
    h, theta = Fr(1), Fr(1, 4)
    O = offsets(h, theta, Fr(40))
    d = corr(O, L)
    Oset = set(O)
    feas = [(a, b, a + b) for a in O for b in O if a + b in Oset]
    best_pt, best_val = None, None
    # candidate optimizers x* = (a, b, a+b) on a 1/4 lattice in [0,12]^2
    for a4 in range(0, 49):
        for b4 in range(0, 49):
            a, b = Fr(a4, 4), Fr(b4, 4)
            xs = (a, b, a + b)
            q = min(L / 2 * sum((y[i] - xs[i]) ** 2 for i in range(3))
                    - d[y[0]] - d[y[1]] - d[y[2]] for y in feas)
            if best_val is None or q > best_val:
                best_val, best_pt = q, xs
    return O, best_pt, best_val


def sum_equality_near_centre():
    """Smallest-norm violating x* = (a, b, a+b) with a, b in {0,1/4,...,4}."""
    L = Fr(1)
    O = offsets(Fr(1), Fr(1, 4), Fr(40))
    d = corr(O, L)
    Oset = set(O)
    feas = [(a, b, a + b) for a in O for b in O if a + b in Oset]
    viol = []
    for a4 in range(0, 17):
        for b4 in range(0, 17):
            a, b = Fr(a4, 4), Fr(b4, 4)
            xs = (a, b, a + b)
            q = min(L / 2 * sum((y[i] - xs[i]) ** 2 for i in range(3))
                    - d[y[0]] - d[y[1]] - d[y[2]] for y in feas)
            if q > 0:
                viol.append((a * a + b * b + (a + b) ** 2, xs, q))
    viol.sort()
    return viol[0], len(viol)


if __name__ == "__main__":
    for n in (4, 9, 16, 25, 100, 400):
        cnt = uniform_tightness(n)
        print("tightness n=%d: next-grid nodes per level %s, bound %d, 2sqrt(n)+1=%.1f"
              % (n, cnt, 5 + math.isqrt(8 * n), 2 * math.sqrt(n) + 1))
    v = order_unsound([Fr(0), Fr(1, 2), Fr(1)], [Fr(0), Fr(1, 3), Fr(1)], Fr(2, 5),
                      Fr(1), Fr(1))
    print("order x1<=x2, grids {0,1/2,1},{0,1/3,1}, m=2/5, L=lam=1: corrected grid min =",
          v, "> F* = 0" if v > 0 else "")
    assert v > 0
    G1, G2, common, m, val = graded_order_example()
    print("graded grids (h=1/16, theta=1/4) centred at 3/10 and 7/10: |G1|=%d |G2|=%d,"
          " common nodes %s, m=%s, corrected min = %s" %
          (len(G1), len(G2), [str(c) for c in common], m, float(val)))
    assert val > 0
    O, pt, val = sum_equality_example()
    print("sum equality x1+x2=x3, common offsets (h=1, theta=1/4): worst x* =",
          [str(v) for v in pt], "corrected min =", val, "=", float(val))
    assert val > 0
    (nrm2, xs, q), nv = sum_equality_near_centre()
    print("sum equality: smallest-norm violating x* =", [str(v) for v in xs],
          "|x*-c|^2 =", nrm2, "corrected min =", q, "=", float(q),
          "; violating points in [0,4]^2 grid:", nv)
    assert q > 0
    print("ALL OBSTRUCTION CHECKS PASSED")


def small_sum_example():
    """x1 + x2 = x3 on [0,3]^3, graded grid around the feasible centre 0 with
    h = 1, theta = 1/4: G = {0, 1, 9/4, 3}; F = (L/2)||x - (1,1,2)||^2."""
    L = Fr(1)
    G = graded_grid(Fr(0), Fr(0), Fr(3), Fr(1), Fr(1, 4))
    assert G == [Fr(0), Fr(1), Fr(9, 4), Fr(3)], G
    d = corr(G, L)
    xs = (Fr(1), Fr(1), Fr(2))
    feas = [(a, b, a + b) for a in G for b in G if a + b in G]
    vals = {y: L / 2 * sum((y[i] - xs[i]) ** 2 for i in range(3)) - sum(d[t] for t in y)
            for y in feas}
    return G, vals


if __name__ == "__main__":
    G, vals = small_sum_example()
    print("small sum example grid", [str(g) for g in G])
    for y, q in sorted(vals.items(), key=lambda kv: kv[1]):
        print("   feasible grid point", [str(t) for t in y], "corrected value", q)
    assert min(vals.values()) == Fr(31, 64)
    print("SMALL SUM EXAMPLE PASSED (min corrected value 31/64 > F* = 0)")
