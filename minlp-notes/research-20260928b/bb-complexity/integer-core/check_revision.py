"""Checks for the revision after review (Section 9 of relaxation-intrinsic-bounds.md).

R1  Theorem 1.7(b).  (a) The review's exact counterexample to the caterpillar:
    classes admissible (exact rational minima over the hulls), and conv(I_2 ∪ I_3)
    contains a point of I_1 that lies in neither child.  (b) On random 2-D
    instances: exact kappa and a minimum partition; the corrected binary tree with
    leaves G_j = {grad phi(xh_j).(x - xh_j) >= 0} (xh_j = argmin over conv I_j)
    and internal nodes N_j = complement of G_1 ∪ ... ∪ G_j is checked:
    I_j ⊆ G_j and inf_{G_j} phi >= tau (exact closed form for a halfspace).
R2  Example 2.1a (compact MILP with kappa = 2^n): phi(x) = ||x - 1/2||_1.
    All 2^n points of {0,1}^n pairwise conflict (exact), and the 2^n halfspaces
    {sum sigma_i (x_i - 1/2) >= n/2} cover a window of Z^n with phi >= OPT.
R3  Proposition 5.2(b) corrected: phi = sum (z_i - a)^2, a = 1/(2n), K = [0,1]^n,
    eps = 1/(8 n^2).  (C1) holds, kappa = 2, and the exact minimum
    variable-branching tree has n+1 leaves and 2n+1 nodes (exact rational DP).
R4  Theorem 1.8(c) corrected, meaningful tests:
    (a) binaries n = 3, phi = ||Az - y||^2 on [0,1]^3, P = {0,1}^3, exact kappa;
        exact minimum-node trees with incumbent probing iterated to a fixpoint at
        every node (each removal certified on the current set, one piece per
        fixing).  Check kappa <= L + S and kappa <= (n+1) N; report max kappa/N.
    (b) general integers on [0,2]x[0,3]: iterated sequential OBBT (Gauss-Seidel,
        repeated until no bound moves); each bound change, of any size, is one
        piece certified on the current box; check kappa <= L + S; report the
        slack and the largest number of changes at one node.
R5  delta ranges of Theorems 3.4 and 3.5 (exact roots).
"""
import itertools
import functools
import math
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import lsq_linear

rng = np.random.default_rng(20260929)


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
    g = [0] * (1 << nv)
    f[0] = 0
    for rem in range(1, 1 << nv):
        low = rem & -rem
        sub = rem
        while sub:
            if sub & low and okm[sub] and f[rem ^ sub] + 1 < f[rem]:
                f[rem] = f[rem ^ sub] + 1
                g[rem] = sub
            sub = (sub - 1) & rem
    # recover one minimum partition
    parts, rem = [], (1 << nv) - 1
    while rem:
        parts.append(g[rem])
        rem ^= g[rem]
    return f[(1 << nv) - 1], parts


# ---------------------------------------------------------------- exact 2-D QP (rationals)
def q_exact(A, y, x):
    r = [sum(A[i][j] * x[j] for j in range(2)) - y[i] for i in range(len(A))]
    return sum(v * v for v in r)


def seg_min_exact(A, y, a, b):
    d = [b[0] - a[0], b[1] - a[1]]
    Ad = [A[i][0] * d[0] + A[i][1] * d[1] for i in range(len(A))]
    ra = [A[i][0] * a[0] + A[i][1] * a[1] - y[i] for i in range(len(A))]
    den = sum(v * v for v in Ad)
    lam = Fr(0) if den == 0 else min(Fr(1), max(Fr(0), -sum(p * q for p, q in zip(ra, Ad)) / den))
    x = [a[0] + lam * d[0], a[1] + lam * d[1]]
    return q_exact(A, y, x), x


def unconstrained_min_exact(A, y):
    # normal equations for 2 unknowns
    G = [[sum(A[k][i] * A[k][j] for k in range(len(A))) for j in range(2)] for i in range(2)]
    h = [sum(A[k][i] * y[k] for k in range(len(A))) for i in range(2)]
    det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
    return [(h[0] * G[1][1] - h[1] * G[0][1]) / det, (G[0][0] * h[1] - G[1][0] * h[0]) / det]


def in_hull_exact(p, pts):
    def cross(o, q, r):
        return (q[0] - o[0]) * (r[1] - o[1]) - (q[1] - o[1]) * (r[0] - o[0])
    if len(pts) == 1:
        return list(pts[0]) == list(p)
    for a, b in itertools.combinations(pts, 2):  # segments
        if cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
            return True
    for a, b, c in itertools.combinations(pts, 3):
        d1, d2, d3 = cross(a, b, p), cross(b, c, p), cross(c, a, p)
        if cross(a, b, c) != 0 and ((d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0)):
            return True
    return False


def hull_min_exact(A, y, pts):
    """exact min of phi over conv(pts) in R^2 and a minimizer"""
    xs = unconstrained_min_exact(A, y)
    if in_hull_exact(xs, pts):
        return q_exact(A, y, xs), xs
    if len(pts) == 1:
        return q_exact(A, y, pts[0]), list(pts[0])
    return min((seg_min_exact(A, y, a, b) for a, b in itertools.combinations(pts, 2)), key=lambda t: t[0])


def halfspace_min_exact(A, y, g, c):
    """min phi over {x : g.x >= c} (exact): unconstrained min if feasible, else on the line."""
    xs = unconstrained_min_exact(A, y)
    if g[0] * xs[0] + g[1] * xs[1] >= c:
        return q_exact(A, y, xs)
    # minimize on the line g.x = c: x = x0 + s * t, t = (-g1, g0)
    if g[1] != 0:
        x0 = [Fr(0), c / g[1]]
    else:
        x0 = [c / g[0], Fr(0)]
    t = [-g[1], g[0]]
    At = [A[i][0] * t[0] + A[i][1] * t[1] for i in range(len(A))]
    r0 = [A[i][0] * x0[0] + A[i][1] * x0[1] - y[i] for i in range(len(A))]
    s = -sum(p * q for p, q in zip(r0, At)) / sum(v * v for v in At)
    return q_exact(A, y, [x0[0] + s * t[0], x0[1] + s * t[1]])


def grad_exact(A, y, x):
    r = [A[i][0] * x[0] + A[i][1] * x[1] - y[i] for i in range(len(A))]
    return [2 * sum(A[i][j] * r[i] for i in range(len(A))) for j in range(2)]


def R1():
    print("== R1 Theorem 1.7(b) ==")
    A = [[Fr(-2), Fr(1)], [Fr(3), Fr(3)]]
    y = [Fr(-3, 5), Fr(18, 7)]
    P = [(Fr(i), Fr(j)) for i in range(4) for j in range(3)]
    OPT = min(q_exact(A, y, p) for p in P)
    tau = OPT - Fr(1, 20)
    I1 = [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (3, 1), (3, 2)]
    I2 = [(0, 0)]
    I3 = [(1, 0), (2, 0), (2, 2), (3, 0)]
    cls = [[(Fr(a), Fr(b)) for a, b in I] for I in (I1, I2, I3)]
    mins = [hull_min_exact(A, y, I)[0] for I in cls]
    print(f"   OPT = {OPT}, tau = {tau}; hull minima {[str(m) for m in mins]}; all admissible: {all(m >= tau for m in mins)}")
    print(f"   whole P admissible: {hull_min_exact(A, y, P)[0] >= tau}; pairs: kappa >= 2 check done below")
    p = (Fr(1), Fr(1))
    print(f"   (1,1) in conv(I2 ∪ I3): {in_hull_exact(p, cls[1] + cls[2])}; in conv I2: {in_hull_exact(p, cls[1])}; in conv I3: {in_hull_exact(p, cls[2])}"
          " -> caterpillar violates the covering condition")
    # corrected tree on this instance
    ok = True
    for I in cls:
        m, xh = hull_min_exact(A, y, I)
        g = grad_exact(A, y, xh)
        c = g[0] * xh[0] + g[1] * xh[1]
        ok &= all(g[0] * q[0] + g[1] * q[1] >= c for q in I) and halfspace_min_exact(A, y, g, c) >= tau
    print(f"   gradient-halfspace chain valid on this instance: {ok}")
    # random instances with kappa >= 3: all minimum partitions (capped) and all orderings (capped)
    import random
    prng = random.Random(20260929)
    want, tried, done = 25, 0, 0
    stats = dict(pairs=0, chain_ok=0, cat_bad=0)
    ks = []
    while done < want and tried < 4000:
        tried += 1
        A = [[Fr(int(v)) for v in rng.integers(-4, 5, 2)] for _ in range(3)]
        G = [[sum(A[k][i] * A[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
        if G[0][0] * G[1][1] - G[0][1] * G[1][0] == 0:
            continue
        y = [Fr(int(rng.integers(-40, 41)), 7) for _ in range(3)]
        OPT = min(q_exact(A, y, p) for p in P)
        tau = OPT - Fr(1, 20)
        nv = len(P)
        # cheap float screen for kappa >= 3 (same algorithm in floats), then exact
        Af = np.array([[float(v) for v in row] for row in A]); yf = np.array([float(v) for v in y])
        Pf = [np.array([float(a), float(b)]) for a, b in P]
        xsf = np.linalg.lstsq(Af, yf, rcond=None)[0]
        def hull_min_float(idx):
            pts = [Pf[i] for i in idx]
            def qf(x):
                r = Af @ x - yf
                return float(r @ r)
            if len(pts) == 1:
                return qf(pts[0])
            best = min(qf(a + min(1.0, max(0.0, -((Af @ a - yf) @ (Af @ (b - a))) / max((Af @ (b - a)) @ (Af @ (b - a)), 1e-300))) * (b - a))
                       for a, b in itertools.combinations(pts, 2))
            if len(pts) >= 3 and in_hull_exact((Fr(xsf[0]), Fr(xsf[1])), [(Fr(a[0]), Fr(a[1])) for a in pts]):
                best = min(best, qf(xsf))
            return best
        tauf = float(tau)
        _, ff = admissible_table(nv, lambda mask: hull_min_float([i for i in range(nv) if mask >> i & 1]) >= tauf - 1e-9)
        if ff[(1 << nv) - 1] < 3:
            continue
        okm, f = admissible_table(nv, lambda mask: hull_min_exact(A, y, [P[i] for i in range(nv) if mask >> i & 1])[0] >= tau)
        kap = f[(1 << nv) - 1]
        if kap < 3:
            continue
        done += 1
        ks.append(kap)
        for parts in all_min_partitions(nv, okm, f, cap=30):
            classes = [[P[i] for i in range(nv) if mask >> i & 1] for mask in parts]
            halfs = []
            leaf_ok = True
            for I in classes:
                m, xh = hull_min_exact(A, y, I)
                g = grad_exact(A, y, xh)
                c = g[0] * xh[0] + g[1] * xh[1]
                leaf_ok &= g != [0, 0] and all(g[0] * q[0] + g[1] * q[1] >= c for q in I) and halfspace_min_exact(A, y, g, c) >= tau
                halfs.append((g, c))
            orders = list(itertools.permutations(range(kap)))
            prng.shuffle(orders)
            for order in orders[:24]:
                stats["pairs"] += 1
                inG = lambda q, j: halfs[j][0][0] * q[0] + halfs[j][0][1] * q[1] >= halfs[j][1]
                # covering at every internal node N_0..N_{kappa-2}, checked point by point
                cov = True
                for t in range(kap - 1):
                    rem = [q for q in P if not any(inG(q, order[i]) for i in range(t))]
                    kids = [order[t]] if t < kap - 2 else [order[kap - 2], order[kap - 1]]
                    if t < kap - 2:
                        continue  # N_t ⊆ G_{t+1} ∪ N_{t+1} holds by definition of N_{t+1}
                    cov &= all(any(inG(q, j) for j in kids) for q in rem)
                stats["chain_ok"] += leaf_ok and cov
                # old caterpillar in this order
                bad = False
                for t in range(kap - 2):
                    node = [q for j in order[t + 1:] for q in classes[j]] + []
                    node_all = [q for j in order[t:] for q in classes[j]]
                    left, right = classes[order[t]], [q for j in order[t + 1:] for q in classes[j]]
                    for q in P:
                        if in_hull_exact(q, node_all) and not (in_hull_exact(q, left) or in_hull_exact(q, right)):
                            bad = True
                            break
                    if bad:
                        break
                stats["cat_bad"] += bad
    print(f"   random instances with kappa >= 3: {done} (kappa distribution {dict(sorted((k, ks.count(k)) for k in set(ks)))}); "
          f"(partition, ordering) pairs tested: {stats['pairs']}; corrected chain valid: {stats['chain_ok']}; "
          f"old caterpillar invalid: {stats['cat_bad']}")


def admissible_table(nv, ok):
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
        while sub:
            if sub & low and okm[sub] and f[rem ^ sub] + 1 < f[rem]:
                f[rem] = f[rem ^ sub] + 1
            sub = (sub - 1) & rem
    return okm, f


def all_min_partitions(nv, okm, f, cap=30):
    out = []

    def rec(rem, acc):
        if len(out) >= cap:
            return
        if rem == 0:
            out.append(list(acc))
            return
        low = rem & -rem
        sub = rem
        while sub:
            if sub & low and okm[sub] and f[rem ^ sub] == f[rem] - 1:
                acc.append(sub)
                rec(rem ^ sub, acc)
                acc.pop()
            sub = (sub - 1) & rem
    rec((1 << nv) - 1, [])
    return out


def R2():
    print("== R2 Example 2.1a: phi = ||x - 1/2||_1, compact MILP with 2n rows ==")
    for n in range(2, 11):
        pts = list(itertools.product((0, 1), repeat=n))
        OPT = Fr(n, 2)
        eps = Fr(1, 4)
        conf = all(sum(abs(Fr(a + b, 2) - Fr(1, 2)) for a, b in zip(p, q)) < OPT - eps for p, q in itertools.combinations(pts, 2))
        cover = None
        if n <= 4:
            win = list(itertools.product(range(-2, 4), repeat=n))
            cover = all(any(sum(s * (Fr(z) - Fr(1, 2)) for s, z in zip(sig, w)) >= OPT for sig in itertools.product((-1, 1), repeat=n)) for w in win)
        print(f"   n={n}: all {len(pts)} points of {{0,1}}^n pairwise conflict: {conf}" + (f"; 2^n halfspaces cover window {{-2..3}}^n: {cover}" if cover is not None else ""))
    print("   (on each halfspace phi >= sum sigma_i (x_i - 1/2) >= n/2 = OPT, by |u| >= sigma u)")


def R3():
    print("== R3 Proposition 5.2(b) corrected ==")
    for n in range(2, 9):
        a = Fr(1, 2 * n)
        OPT = n * a * a
        eps = Fr(1, 8 * n * n)
        tau = OPT - eps
        c1 = (1 - a) ** 2 >= OPT
        # kappa: min over [0,1]^n ∩ {1.z >= 1} is at z = (1/n) 1 (projection of a 1)
        m1 = n * (Fr(1, n) - a) ** 2
        kappa_ok = m1 >= tau and 0 < tau  # classes {0} and {1.z >= 1}; root bound 0 < tau

        @functools.lru_cache(maxsize=None)
        def T(state):  # returns (leaves, nodes) of a minimum-node tree
            fixed = [v for v in state if v != -1]
            bound = sum((v - a) ** 2 for v in fixed)
            if bound >= tau:
                return (1, 1)
            best = None
            for i, v in enumerate(state):
                if v == -1:
                    l0 = T(state[:i] + (0,) + state[i + 1:])
                    l1 = T(state[:i] + (1,) + state[i + 1:])
                    cand = (l0[0] + l1[0], 1 + l0[1] + l1[1])
                    if best is None or cand[1] < best[1]:
                        best = cand
            return best
        L, N = T((-1,) * n)
        print(f"   n={n}: (C1) {c1}; kappa = 2 certified {kappa_ok}; min variable tree: {L} leaves, {N} nodes (n+1={n+1}, 2n+1={2*n+1})")


# ---------------------------------------------------------------- R4
def simplex_ls_min(M, y):
    """min ||M lam - y||^2 over the simplex, exact up to float, via Caratheodory
    enumeration of supports of size <= dim+1 (dim = M.shape[0] <= 3 here)."""
    k = M.shape[1]
    best = math.inf
    d = M.shape[0]
    for size in range(1, min(k, d + 1) + 1):
        for S in itertools.combinations(range(k), size):
            Ms = M[:, S]
            if size == 1:
                val = float(np.sum((Ms[:, 0] - y) ** 2))
                best = min(best, val)
                continue
            # lam = e_1-param: lam_0 = 1 - sum rest; solve LS in the affine hull
            B = Ms[:, 1:] - Ms[:, :1]
            rhs = y - Ms[:, 0]
            mu, *_ = np.linalg.lstsq(B, rhs, rcond=None)
            lam = np.concatenate([[1 - mu.sum()], mu])
            if np.all(lam >= -1e-12):
                val = float(np.sum((B @ mu - rhs) ** 2))
                best = min(best, val)
    return best


def R4a(trials=40, n=3):
    print("== R4(a) Theorem 1.8(c), binaries n=3 with iterated incumbent probing ==")
    pts = [np.array(p, float) for p in itertools.product((0, 1), repeat=n)]
    worst = 0.0
    viol = 0
    rows = []
    for tr in range(trials):
        A = rng.standard_normal((n, n))
        c = rng.uniform(0.25, 0.75, n)
        y = A @ c + 0.05 * rng.standard_normal(n)
        vals = [float(np.sum((A @ p - y) ** 2)) for p in pts]
        OPT = min(vals)
        tau = OPT - 1e-6
        UB = OPT

        def adm(mask):
            M = np.array([A @ pts[i] for i in range(len(pts)) if mask >> i & 1]).T
            return simplex_ls_min(M, y) >= tau - 1e-9
        kappa, _ = min_partition(len(pts), adm)

        @functools.lru_cache(maxsize=None)
        def bound(state):
            lo = np.array([0.0 if v == -1 else v for v in state])
            hi = np.array([1.0 if v == -1 else v for v in state])
            if np.all(lo == hi):
                return float(np.sum((A @ lo - y) ** 2))
            free = lo != hi
            r = lsq_linear(A[:, free], y - A[:, ~free] @ lo[~free], bounds=(lo[free], hi[free]), method="bvls", tol=1e-13)
            return 2 * r.cost

        def probe(state):
            """iterate probing to a fixpoint; each fixing removes one certified piece.
            Returns (reduced state or None if emptied, pieces)."""
            state = list(state)
            pieces = 0
            changed = True
            while changed:
                changed = False
                for i in range(n):
                    if state[i] != -1:
                        continue
                    for v in (0, 1):
                        s2 = state[:]
                        s2[i] = v
                        if bound(tuple(s2)) >= UB - 1e-6 - 1e-12:  # piece {x_i = v} certified on the current set
                            pieces += 1
                            other = 1 - v
                            s3 = state[:]
                            s3[i] = other
                            # if the other side is also certified, the node empties:
                            # the last piece replaces the leaf (see Theorem 1.8(c))
                            if bound(tuple(s3)) >= UB - 1e-6 - 1e-12:
                                return None, pieces
                            state = s3
                            changed = True
                            break
            return tuple(state), pieces

        @functools.lru_cache(maxsize=None)
        def TO(state):
            """(nodes, leaves, pieces) of a minimum-node tree with probing at every node"""
            red, s = probe(state)
            if red is None:
                # both values of some x_i are certified: the first is a counted piece, the
                # remaining side is the node's own (certified) leaf
                return (1, 1, s)
            if bound(red) >= tau - 1e-12:
                return (1, 1, s)
            best = None
            for i, v in enumerate(red):
                if v == -1:
                    a = TO(red[:i] + (0,) + red[i + 1:])
                    b = TO(red[:i] + (1,) + red[i + 1:])
                    cand = (1 + a[0] + b[0], a[1] + b[1], s + a[2] + b[2])
                    if best is None or cand[0] < best[0]:
                        best = cand
            return best
        N, L, S = TO((-1,) * n)
        ok = kappa <= L + S and kappa <= (n + 1) * N
        viol += not ok
        worst = max(worst, kappa / N)
        rows.append((kappa, L, S, N))
    print(f"   {trials} instances: violations of kappa <= L+S and kappa <= (n+1)N: {viol}; max kappa/N = {worst:.2f} (bound n+1 = {n+1})")
    print(f"   kappa distribution: {dict(sorted((k, [r[0] for r in rows].count(k)) for k in set(r[0] for r in rows)))}; "
          f"sample (kappa,L,S,N): {sorted(rows, key=lambda r: -r[0] / r[3])[:6]}")


def R4b(trials=100):
    print("== R4(b) Theorem 1.8(c), general integers on [0,2]x[0,3], iterated sequential OBBT ==")
    n = 2
    ub0 = (2, 3)
    maxchg = [0]
    pts = [np.array(p, float) for p in itertools.product(range(3), range(4))]
    viol = 0
    rows = []
    for tr in range(trials):
        A = rng.standard_normal((3, n))
        t = rng.uniform([0.2, 0.2], [1.8, 2.8])
        y = A @ t + 0.3 * rng.standard_normal(3)
        vals = [float(np.sum((A @ p - y) ** 2)) for p in pts]
        OPT = min(vals)
        tau = OPT - 1e-6

        def hullmin(mask):
            M = np.array([A @ pts[i] for i in range(len(pts)) if mask >> i & 1]).T
            return simplex_ls_min(M, y)
        kappa, _ = min_partition(len(pts), lambda mask: hullmin(mask) >= tau - 1e-9)

        @functools.lru_cache(maxsize=None)
        def bound(lo, hi):
            lo_, hi_ = np.array(lo, float), np.array(hi, float)
            if np.any(lo_ > hi_):
                return math.inf
            fixed = lo_ == hi_
            if np.all(fixed):
                return float(np.sum((A @ lo_ - y) ** 2))
            r = lsq_linear(A[:, ~fixed], y - A[:, fixed] @ lo_[fixed], bounds=(lo_[~fixed], hi_[~fixed]), method="bvls", tol=1e-13)
            return 2 * r.cost

        def obbt(lo, hi):
            """Iterated sequential OBBT: each bound change, of any size, is ONE piece
            certified on the current box (the rule of Theorem 1.8(c))."""
            lo, hi = list(lo), list(hi)
            pieces = 0
            changed = True
            while changed:
                changed = False
                for i in range(n):
                    # largest c with r(box ∩ {x_i <= c}) >= tau (bound decreases in c)
                    c = None
                    for cc in range(lo[i], hi[i] + 1):
                        h = hi[:]
                        h[i] = cc
                        if bound(tuple(lo), tuple(h)) >= tau - 1e-12:
                            c = cc
                        else:
                            break
                    if c is not None:
                        pieces += 1
                        changed = True
                        if c >= hi[i]:
                            return None, pieces  # this change empties the node
                        lo[i] = c + 1
                    c = None
                    for cc in range(hi[i], lo[i] - 1, -1):
                        l2 = lo[:]
                        l2[i] = cc
                        if bound(tuple(l2), tuple(hi)) >= tau - 1e-12:
                            c = cc
                        else:
                            break
                    if c is not None:
                        pieces += 1
                        changed = True
                        if c <= lo[i]:
                            return None, pieces
                        hi[i] = c - 1
            return (tuple(lo), tuple(hi)), pieces

        def obbt_tracked(lo, hi):
            red, pc = obbt(lo, hi)
            maxchg[0] = max(maxchg[0], pc)
            return red, pc

        @functools.lru_cache(maxsize=None)
        def TO(lo, hi):
            red, s = obbt_tracked(lo, hi)
            if red is None:
                return (1, 0, s)
            lo2, hi2 = red
            if bound(lo2, hi2) >= tau - 1e-12:
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
        N, L, S = TO((0, 0), ub0)
        viol += kappa > L + S
        rows.append((kappa, L, S, N))
    print(f"   {trials} instances: violations of kappa <= L + S: {viol}; instances with L < kappa: {sum(1 for r in rows if r[1] < r[0])}; "
          f"min slack L+S-kappa: {min(r[1] + r[2] - r[0] for r in rows)}; slack-0 instances: {sum(1 for r in rows if r[1] + r[2] == r[0])}; "
          f"max bound changes at one node: {maxchg[0]} (2n = {2*n}); sample (kappa,L,S,N): {rows[:6]}")


def R5():
    print("== R5 delta ranges ==")
    d34 = (3 - math.sqrt(8)) / 2
    d35 = (4 - math.sqrt(13)) / 3
    print(f"   Theorem 3.4 non-vacuous (rho -> 4/3) iff (4/3)((1-d)^2 - d) > 1 iff d < (3 - sqrt 8)/2 = {d34:.5f}")
    print(f"   Theorem 3.5 non-vacuous iff (3/2)(1-d)^2 - d > 1 iff d < (4 - sqrt 13)/3 = {d35:.5f}")
    for d in (0.05, 0.08):
        print(f"   delta={d}: (4/3)((1-d)^2-d) = {(4/3)*((1-d)**2-d):.5f}; (3/2)(1-d)^2-d = {1.5*(1-d)**2-d:.5f}")


if __name__ == "__main__":
    import sys
    parts = sys.argv[1] if len(sys.argv) > 1 else "12345ab"
    if "1" in parts:
        R1()
    if "2" in parts:
        R2()
    if "3" in parts:
        R3()
    if "a" in parts:
        R4a()
    if "b" in parts:
        R4b()
    if "5" in parts:
        R5()
