"""Exact checks of the proximal grid generator under set growth and of the
unknown-growth discovery loop for the diagonal certificate class.

Continuous box QPs F(x)=1/2 x^T H x + b^T x + c.  Brute-force minimization of the
proximal corrected objective over the fresh product grid (small n only).
For instances with a known optimal set S (finite union of segments) and a valid
guess K >= L/g, every stage is checked for:
  * nearest optimizer to the centre lies in the fresh box,
  * F(y_j) - f* <= (99/256) L n h_j^2,
  * dist(y_j,S)^2 <= (99/256) K n h_j^2,
  * per-coordinate grid size <= 100/theta * ceil(log2(n+2)).
Then the discovery loop K=1,2,4,... (bound selection within tau, exact
stationary-face vertex, KKT + PSD acceptance) is run; acceptance is checked to
be globally optimal.
Run: python3 -B check_proximal.py
"""
from fractions import Fraction as Fr
from itertools import product
from math import isqrt


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fr(0))


def mv(A, x):
    return [dot(row, x) for row in A]


def Fval(P, x):
    H, b, c = P
    return dot(x, mv(H, x)) / 2 + dot(b, x) + c


def ceil_sqrt(m):
    r = isqrt(m)
    return r if r * r == m else r + 1


def ceil_log2(m):
    k = 0
    while (1 << k) < m:
        k += 1
    return k


def coord_grid(c, lo, hi, h, theta):
    nodes = [c]
    for direction in (1, -1):
        t = Fr(0)
        end = hi - c if direction == 1 else c - lo
        while t < end:
            t = min(t + h + theta * t, end)
            nodes.append(c + direction * t)
    return sorted(set(nodes))


def corrections(nodes, L):
    out = {}
    for k, v in enumerate(nodes):
        w = Fr(0)
        if k > 0:
            w = max(w, v - nodes[k - 1])
        if k + 1 < len(nodes):
            w = max(w, nodes[k + 1] - v)
        out[v] = L * w * w / 8
    return out


def dist2_segments(x, segs):
    best = None
    for p, q in segs:
        d = [qi - pi for pi, qi in zip(p, q)]
        dd = dot(d, d)
        t = Fr(0) if dd == 0 else min(max(dot([xi - pi for xi, pi in zip(x, p)], d) / dd, Fr(0)), Fr(1))
        z = [pi + t * di for pi, di in zip(p, d)]
        val = dot([xi - zi for xi, zi in zip(x, z)], [xi - zi for xi, zi in zip(x, z)])
        if best is None or val < best[0]:
            best = (val, z)
    return best


def proximal_run(P, box, L, K, J, fstar=None, segs=None, check=False):
    n = len(box)
    mu = 2
    while Fr(K, 4 ** mu) > Fr(1, 8):
        mu += 1
    theta = Fr(1, 2 ** mu)
    eta = L * theta * theta / 4
    rho = 2 * ceil_sqrt(K * n)
    s0 = max(hi - lo for lo, hi in box)
    cap = 100 * 2 ** mu * ceil_log2(n + 2)
    c = [lo for lo, hi in box]
    y = c
    maxgrid = 0
    for j in range(J + 1):
        h = s0 / 2 ** j
        fb = [(max(lo, ci - rho * h), min(hi, ci + rho * h)) for (lo, hi), ci in zip(box, c)]
        grids = [coord_grid(ci, lo, hi, h, theta) for ci, (lo, hi) in zip(c, fb)]
        maxgrid = max(maxgrid, max(len(g) for g in grids))
        assert max(len(g) for g in grids) <= cap
        corr = [corrections(g, L) for g in grids]
        if check:
            _, z = dist2_segments(c, segs)
            assert all(lo <= zi <= hi for zi, (lo, hi) in zip(z, fb)), "nearest optimizer left fresh box"
        best = None
        for pt in product(*grids):
            pt = list(pt)
            val = Fval(P, pt) - sum(corr[i][pt[i]] for i in range(n)) + eta * dot([a - b for a, b in zip(pt, c)], [a - b for a, b in zip(pt, c)])
            if best is None or val < best[0]:
                best = (val, pt)
        y = best[1]
        if check:
            gap = Fval(P, y) - fstar
            assert gap >= 0
            assert gap <= Fr(99, 256) * L * n * h * h, (j, gap)
            d2, _ = dist2_segments(y, segs)
            assert d2 <= Fr(99, 256) * K * n * h * h, (j, d2)
        c = y
    return y, maxgrid, theta


def solve_unique(rows, rhs, nvars):
    """Gaussian elimination; return the unique solution or None."""
    A = [r[:] + [v] for r, v in zip(rows, rhs)]
    m = len(A)
    piv_cols = []
    r = 0
    for col in range(nvars):
        p = next((i for i in range(r, m) if A[i][col] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][col]
        A[r] = [v / pv for v in A[r]]
        for i in range(m):
            if i != r and A[i][col] != 0:
                f = A[i][col]
                A[i] = [a - f * bb for a, bb in zip(A[i], A[r])]
        piv_cols.append(col)
        r += 1
    for i in range(r, m):
        if A[i][nvars] != 0:
            return None
    if r < nvars:
        return None
    x = [Fr(0)] * nvars
    for i, col in enumerate(piv_cols):
        x[col] = A[i][nvars]
    return x


def psd(a):
    a = [row[:] for row in a]
    while a:
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        piv = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if piv is None:
            return all(v == 0 for row in a for v in row)
        others = [i for i in range(len(a)) if i != piv]
        a = [[a[i][j] - a[i][piv] * a[piv][j] / a[piv][piv] for j in others] for i in others]
    return True


def certificate(P, box, s):
    H, b, _ = P
    g = [u + v for u, v in zip(mv(H, s), b)]
    lam = []
    for (lo, hi), si, gi in zip(box, s, g):
        if si == lo and gi >= 0:
            lam.append(2 * gi / (hi - lo))
        elif si == hi and gi <= 0:
            lam.append(-2 * gi / (hi - lo))
        elif lo < si < hi and gi == 0:
            lam.append(Fr(0))
        else:
            return None
    n = len(s)
    M = [[H[i][j] + (lam[i] if i == j else 0) for j in range(n)] for i in range(n)]
    return lam if psd(M) else None


def height_tau(P, box):
    H, b, c = P
    n = len(box)
    den = 1
    for v in [x for row in H for x in row] + list(b) + [c] + [e for bb in box for e in bb]:
        den = den * v.denominator // __import__("math").gcd(den, v.denominator)
    C = max([1] + [abs(den * x) for row in H for x in row])
    Delta = (n * C) ** n
    R = den * Delta
    return Fr(1, 4 * n * R), den


def recover(P, box, y, tau):
    """Bound selection within tau, then a vertex of the selected stationary face."""
    H, b, _ = P
    n = len(box)
    fixed = {}
    for i, ((lo, hi), yi) in enumerate(zip(box, y)):
        if yi - lo <= tau:
            fixed[i] = lo
        elif hi - yi <= tau:
            fixed[i] = hi
    J = [i for i in range(n) if i not in fixed]
    for extra in product(*[("free", "l", "u") for _ in J]):
        rows, rhs = [], []
        for i, v in fixed.items():
            r = [Fr(0)] * n
            r[i] = Fr(1)
            rows.append(r)
            rhs.append(v)
        for i in J:
            rows.append(list(H[i]))
            rhs.append(-b[i])
        for i, e in zip(J, extra):
            if e != "free":
                r = [Fr(0)] * n
                r[i] = Fr(1)
                rows.append(r)
                rhs.append(box[i][0] if e == "l" else box[i][1])
        x = solve_unique(rows, rhs, n)
        if x is not None and all(lo <= xi <= hi for (lo, hi), xi in zip(box, x)):
            return x
    return None


def discover(P, box, L, fstar=None, maxK=4096):
    n = len(box)
    tau, _ = height_tau(P, box)
    s0 = max(hi - lo for lo, hi in box)
    K = 1
    log = []
    while K <= maxK:
        J = 0
        while K * n * s0 * s0 / 4 ** J > tau * tau / 4:
            J += 1
        y, mg, theta = proximal_run(P, box, L, K, J)
        x = recover(P, box, y, tau)
        acc = x is not None and certificate(P, box, x) is not None
        log.append((K, J, mg, acc))
        if acc:
            if fstar is not None:
                assert Fval(P, x) == fstar
            return x, log
        K *= 2
    return None, log


def main():
    # (1) flat diagonal: F=(x-y)^2 on [0,1]^2, S=diagonal, g=2, L=2, kappa=1
    P1 = ([[Fr(2), Fr(-2)], [Fr(-2), Fr(2)]], [Fr(0), Fr(0)], Fr(0))
    box1 = [(Fr(0), Fr(1)), (Fr(0), Fr(1))]
    segs1 = [([Fr(0), Fr(0)], [Fr(1), Fr(1)])]
    for K in (1, 2, 8):
        proximal_run(P1, box1, Fr(2), K, 12, fstar=Fr(0), segs=segs1, check=True)
    # (2) tilted two segments: F=(x-y+t/2)^2+t(1-t)/8 on [0,1]^3, L=2.
    v = [Fr(1), Fr(-1), Fr(1, 2)]
    H = [[2 * a * bb for bb in v] for a in v]
    H[2][2] -= Fr(1, 4)
    P2 = (H, [Fr(0), Fr(0), Fr(1, 8)], Fr(0))
    box2 = [(Fr(0), Fr(1))] * 3
    segs2 = [([Fr(0), Fr(0), Fr(0)], [Fr(1), Fr(1), Fr(0)]), ([Fr(0), Fr(1, 2), Fr(1)], [Fr(1, 2), Fr(1), Fr(1)])]
    # verify growth g = 1/12 on a rational grid (supports kappa = 24)
    cnt = 0
    for pt in product(*[[Fr(k, 6) for k in range(7)]] * 3):
        pt = list(pt)
        d2, _ = dist2_segments(pt, segs2)
        assert Fval(P2, pt) >= d2 / 12
        cnt += 1
    proximal_run(P2, box2, Fr(2), 32, 9, fstar=Fr(0), segs=segs2, check=True)
    # (3) discovery loop on (1), (2) and the invalid-growth trap
    x1, log1 = discover(P1, box1, Fr(2), fstar=Fr(0))
    x2, log2 = discover(P2, box2, Fr(2), fstar=Fr(0))
    P3 = ([[Fr(2), Fr(-3)], [Fr(-3), Fr(2)]], [Fr(63, 128)] * 2, Fr(0))
    box3 = [(Fr(0), Fr(1))] * 2
    x3, log3 = discover(P3, box3, Fr(2), fstar=Fr(-1, 64))
    assert x3 == [Fr(1), Fr(1)]
    print("growth grid points checked for example 2:", cnt)
    print("discovery logs (K, stages J, max grid, accepted):")
    print("  flat diagonal:", log1, "->", x1)
    print("  tilted segments:", log2, "->", x2)
    print("  trap:", log3, "->", x3)
    print("proximal/discovery checks passed")


if __name__ == "__main__":
    main()


def trap_all_stages():
    """For the trap, K in {1,2,4}: every iterate up to stage 33 is the origin."""
    P3 = ([[Fr(2), Fr(-3)], [Fr(-3), Fr(2)]], [Fr(63, 128)] * 2, Fr(0))
    box3 = [(Fr(0), Fr(1))] * 2
    for K in (1, 2, 4):
        for J in range(34):
            y, _, _ = proximal_run(P3, box3, Fr(2), K, J)
            assert y == [Fr(0), Fr(0)], (K, J, y)
    print("trap: K=1,2,4 iterates are the origin at every stage 0..33")


if __name__ == "__main__":
    trap_all_stages()
