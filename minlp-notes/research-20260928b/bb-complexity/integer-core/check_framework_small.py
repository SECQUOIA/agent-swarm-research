"""Small exact checks for Sections 1 and 2 of relaxation-intrinsic-bounds.md.

Part A (Theorem 1.8(c), domain reductions): convex quadratics phi(x) = ||Ax - y||^2 on
  the box K = [0,2]^2, P = box integer points (9 points), tau = OPT - 1e-6.
  kappa  = exact minimum number of admissible classes (bitmask DP; admissibility
           of a class I is inf_{conv I} phi >= tau, decided by a small QP);
  For every variable-branching tree with incumbent OBBT at each node we build the
  minimum-node tree by DP and record L (leaves), N (nodes), S (number of removed
  pieces); Theorem 1.8(c) says kappa <= L + S <= (2n+1) N.
  Also the 1D counterexample phi = (x - 0.4)^2.
Part B (Proposition 2.1, linear collapse): random ILPs min c.x, A x <= b on the box
  [0,2]x[0,3] with integral data; exact kappa over the 12 box points versus m_nonbox + 1.
Part C (Proposition 2.4, quadratic Jeroslow instance): phi = (1.x - n/2)^2 on
  [0,1]^n, n odd; exact minimum variable-branching tree by DP over partial
  assignments versus C(n+1, (n+1)/2) and the two-class certificate.
Floating point with explicit tolerances; all margins are large compared to them.
"""
import itertools
import functools
import math
import numpy as np
from scipy.optimize import minimize, linprog, lsq_linear

rng = np.random.default_rng(20260928)


# ---------------------------------------------------------------- helpers
def min_partition(nv, ok):
    okm = [False] * (1 << nv)
    for mask in range(1, 1 << nv):
        if mask & (mask - 1) == 0:
            okm[mask] = ok(mask)
            continue
        good = True
        mm = mask
        while mm:
            b = mm & -mm
            mm ^= b
            if not okm[mask ^ b]:
                good = False
                break
        okm[mask] = good and ok(mask)
    INF = 10 ** 9
    f = [INF] * (1 << nv)
    f[0] = 0
    for rem in range(1, 1 << nv):
        low = rem & -rem
        sub = rem
        best = INF
        while sub:
            if sub & low and okm[sub]:
                best = min(best, f[rem ^ sub] + 1)
            sub = (sub - 1) & rem
        f[rem] = best
    return f[(1 << nv) - 1]


def seg_min(A, y, a, b):
    ra = A @ a - y
    Ad = A @ (b - a)
    den = Ad @ Ad
    lam = 0.0 if den == 0 else min(1.0, max(0.0, -(ra @ Ad) / den))
    r = ra + lam * Ad
    return float(r @ r)


def in_hull_2d(p, pts):
    """p in conv(pts) for points in R^2 (Caratheodory: some triangle, segment or point)."""
    def cross(o, q, r):
        return (q[0] - o[0]) * (r[1] - o[1]) - (q[1] - o[1]) * (r[0] - o[0])
    for a, b, c in itertools.combinations(pts, 3):
        d1, d2, d3 = cross(a, b, p), cross(b, c, p), cross(c, a, p)
        if cross(a, b, c) == 0:
            continue
        if (d1 >= -1e-12 and d2 >= -1e-12 and d3 >= -1e-12) or (d1 <= 1e-12 and d2 <= 1e-12 and d3 <= 1e-12):
            return True
    return False


def qp_min_over_hull(A, y, pts):
    """Exact min of ||A x - y||^2 over conv(pts), pts in R^2 (A of full column rank):
    the unconstrained minimizer if it lies in the hull, otherwise the minimum over all
    segments between the points (these cover the boundary and lie in the hull)."""
    P = [np.array(p, float) for p in pts]
    if len(P) == 1:
        r = A @ P[0] - y
        return float(r @ r)
    xs = np.linalg.lstsq(A, y, rcond=None)[0]
    if len(P) >= 3 and in_hull_2d(xs, P):
        r = A @ xs - y
        return float(r @ r)
    return min(seg_min(A, y, a, b) for a, b in itertools.combinations(P, 2))


# ---------------------------------------------------------------- Part A
def part_A(trials=40):
    print("== Part A: 1D counterexample phi=(x-0.4)^2, eps=0.01 ==")
    OPT = 0.16
    print(f"   phi(0.5)={0.01:.2f} < OPT-eps={OPT-0.01:.2f}: points 0 and 1 conflict -> kappa >= 2")
    lo, hi = 0.4 - math.sqrt(OPT), 0.4 + math.sqrt(OPT)
    print(f"   OBBT on {{phi <= UB=OPT}} gives [{lo:.2f},{hi:.2f}] -> integer bounds [{math.ceil(lo)},{math.floor(hi)}]: one-node tree")
    print("== Part A: random convex quadratics on [0,2]^2 with OBBT at every node ==")
    n, m = 2, 2
    viol = 0
    ratios = []
    for tr in range(trials):
        A = rng.standard_normal((3, n))
        t = rng.uniform(0.2, m - 0.2, n)
        y = A @ t + 0.3 * rng.standard_normal(3)
        pts = [np.array(p, float) for p in itertools.product(range(m + 1), repeat=n)]
        vals = [float(np.sum((A @ p - y) ** 2)) for p in pts]
        OPT = min(vals)
        tau = OPT - 1e-6
        kappa = min_partition(len(pts), lambda mask: qp_min_over_hull(A, y, [pts[i] for i in range(len(pts)) if mask >> i & 1]) >= tau - 1e-9)

        @functools.lru_cache(maxsize=None)
        def bound(lo, hi):
            lo_, hi_ = np.array(lo, float), np.array(hi, float)
            if np.any(lo_ > hi_):
                return math.inf
            fixed = lo_ == hi_
            if np.all(fixed):
                return float(np.sum((A @ lo_ - y) ** 2))
            yy = y - A[:, fixed] @ lo_[fixed]
            r = lsq_linear(A[:, ~fixed], yy, bounds=(lo_[~fixed], hi_[~fixed]), method="bvls", tol=1e-13)
            return 2 * r.cost

        def obbt(lo, hi):
            lo, hi = list(lo), list(hi)
            removed = 0
            if bound(tuple(lo), tuple(hi)) > OPT + 1e-9:
                return None, 0
            for i in range(n):
                c = lo[i]
                while c < hi[i]:
                    h = list(hi); h[i] = c
                    if bound(tuple(lo), tuple(h)) <= OPT + 1e-9:
                        break
                    c += 1
                if c > lo[i]:
                    removed += 1
                lo_new = c
                c = hi[i]
                while c > lo_new:
                    l2 = list(lo); l2[i] = c
                    if bound(tuple(l2), tuple(hi)) <= OPT + 1e-9:
                        break
                    c -= 1
                if c < hi[i]:
                    removed += 1
                lo[i], hi[i] = lo_new, c
            return (tuple(lo), tuple(hi)), removed

        @functools.lru_cache(maxsize=None)
        def TO(lo, hi):
            """min-node tree with OBBT; returns (nodes, leaves, removed pieces)."""
            red, s = obbt(lo, hi)
            if red is None:
                return (1, 1, 0)  # whole node pruned by bound (bound > UB)
            lo2, hi2 = red
            if bound(lo2, hi2) >= tau - 1e-9:
                return (1, 1, s)
            best = None
            for i in range(n):
                for c in range(lo2[i], hi2[i]):
                    h1 = list(hi2); h1[i] = c
                    l2 = list(lo2); l2[i] = c + 1
                    a, b = TO(lo2, tuple(h1)), TO(tuple(l2), hi2)
                    cand = (1 + a[0] + b[0], a[1] + b[1], s + a[2] + b[2])
                    if best is None or cand[0] < best[0]:
                        best = cand
            return best

        N, L, S = TO((0,) * n, (m,) * n)
        ok = kappa <= L + S <= (2 * n + 1) * N
        viol += not ok
        ratios.append((kappa, L, S, N))
    print(f"   {trials} instances: violations of kappa <= L+S <= (2n+1)N: {viol}")
    print(f"   instances with L < kappa (leaf form fails): {sum(1 for k_, L, S, N in ratios if L < k_)}")
    print(f"   max kappa/N = {max(k_ / N for k_, L, S, N in ratios):.2f} (bound 2n+1 = {2*n+1}); examples (kappa,L,S,N): {ratios[:6]}")


# ---------------------------------------------------------------- Part B
def part_B(trials=30):
    print("== Part B: linear collapse, random ILPs on the box [0,2]x[0,3] ==")
    n = 2
    ub = np.array([2.0, 3.0])
    pts = [np.array(p, float) for p in itertools.product(range(3), range(4))]
    viol = 0
    rows = []
    for tr in range(trials):
        while True:
            q = int(rng.integers(1, 4))
            A = rng.integers(-4, 5, (q, n)).astype(float)
            b = rng.integers(-2, 8, q).astype(float)
            c = rng.integers(-5, 6, n).astype(float)
            feas = [p for p in pts if np.all(A @ p <= b + 1e-9)]
            if not feas or np.all(c == 0):
                continue
            OPT = min(float(c @ p) for p in feas)
            tau = OPT - 0.5
            Abox = np.vstack([A, np.eye(n), -np.eye(n)])
            bbox = np.concatenate([b, ub, np.zeros(n)])
            root = linprog(c, A_ub=Abox, b_ub=bbox, bounds=[(None, None)] * n, method="highs")
            if root.status == 0 and root.fun < tau - 1e-9:
                break  # nontrivial instance: the root relaxation does not certify OPT

        def adm(mask):
            idx = [i for i in range(len(pts)) if mask >> i & 1]
            Pm = np.array([pts[i] for i in idx]).T
            k = len(idx)
            # min c.x over conv(I) cap K : variables lambda >= 0, sum = 1, Abox P lambda <= bbox
            res = linprog(c @ Pm, A_ub=Abox @ Pm, b_ub=bbox, A_eq=np.ones((1, k)), b_eq=[1], bounds=[(0, None)] * k, method="highs")
            if res.status == 2:
                return True  # conv(I) misses K
            return res.fun >= tau - 1e-9
        kappa = min_partition(len(pts), adm)
        viol += kappa > q + 1
        rows.append((q, kappa))
    from collections import Counter
    print(f"   {trials} instances with root gap (kappa >= 2): violations of kappa <= (#non-box rows)+1: {viol}")
    print(f"   (q, kappa) counts: {sorted(Counter(rows).items())}")


# ---------------------------------------------------------------- Part C
def part_C():
    print("== Part C: quadratic Jeroslow instance phi=(1.x - n/2)^2 on [0,1]^n ==")
    for n in (3, 5, 7):
        tau = 0.25 - 0.01

        @functools.lru_cache(maxsize=None)
        def T(state):
            # state: tuple over variables in {-1 (free), 0, 1}
            fixed_sum = sum(v for v in state if v == 1)
            free = sum(1 for v in state if v == -1)
            lo, hi = fixed_sum, fixed_sum + free
            val = 0.0 if lo <= n / 2 <= hi else min((lo - n / 2) ** 2, (hi - n / 2) ** 2)
            if val >= tau:
                return 1
            best = math.inf
            for i, v in enumerate(state):
                if v == -1:
                    s0 = state[:i] + (0,) + state[i + 1:]
                    s1 = state[:i] + (1,) + state[i + 1:]
                    best = min(best, T(s0) + T(s1))
            return best
        Lmin = T((-1,) * n)
        h = (n + 1) // 2
        # two-class certificate: inf over [0,1]^n cap {1.x <= h-1} of phi = (h-1-n/2)^2 = 1/4
        print(f"   n={n}: min variable-tree leaves = {Lmin}, C(n+1,(n+1)/2) = {math.comb(n + 1, h)}, "
              f"counting bound 2^((n+1)/2) = {2 ** h}; kappa = 2 (classes 1.x <= {h-1} and 1.x >= {h}, each with inf phi = 1/4 >= tau)")


if __name__ == "__main__":
    import sys
    parts = sys.argv[1] if len(sys.argv) > 1 else "ABC"
    if "A" in parts:
        part_A()
    if "B" in parts:
        part_B()
    if "C" in parts:
        part_C()
