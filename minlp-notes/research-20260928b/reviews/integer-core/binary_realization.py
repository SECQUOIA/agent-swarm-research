"""Reviewer check for Theorem 1.7(b) (binary realization of a minimum admissible partition).

Exact rational arithmetic throughout (fractions.Fraction).

Setting: phi(x) = ||A x - y||^2 on K = R^2 (A, y rational), P = integer points of the box
{0..3} x {0..2} (12 points), OPT = min_P phi, tau = OPT - eps.
A class I (subset of P) is admissible iff min_{conv I} phi >= tau (computed exactly: the
unconstrained minimizer if it lies in conv I, otherwise the minimum over the hull edges).

For each random instance the script computes
  kappa        exact minimum number of admissible classes (bitmask DP);
  caterpillar  for EVERY minimum admissible partition and EVERY ordering of its classes, whether
               the note's caterpillar (children conv I_1 and conv(I_2 u ... u I_kappa), then
               recursively) satisfies the covering condition of Definition 1.1
               (Q_v cap P contained in the union of the children's sets);
  f_bin        exact minimum number of leaves of a binary P-covering tau-certificate whose
               pieces are convex hulls of subsets of P (recursion over P-convex sets; nesting
               is w.l.o.g. because replacing Q_v by the effective set keeps a valid tree);
  halfspace    the reviewer's replacement construction: for each class I_j of one minimum
               partition, the closed halfspace H_j = {g_j.(x - xh_j) >= 0} with xh_j the
               minimizer of phi over conv I_j and g_j = grad phi(xh_j); leaves H_1..H_kappa,
               internal nodes N_j = N_{j-1} minus H_j (intersections of open halfspaces).
               Checked: I_j in H_j, min_{H_j} phi >= tau, and the last internal node's
               integer points are covered by H_{kappa-1} u H_kappa.
Usage: python3 binary_realization.py [ninstances] [seed]
"""
import sys
import random
from fractions import Fraction as F
from itertools import permutations

NX, NY = 4, 3
PTS = [(F(i), F(j)) for i in range(NX) for j in range(NY)]
NP = len(PTS)
FULL = (1 << NP) - 1


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def on_segment(p, a, b):
    if cross(a, b, p) != 0:
        return False
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def in_hull(p, H):
    if len(H) == 1:
        return p == H[0]
    if len(H) == 2:
        return on_segment(p, H[0], H[1])
    for i in range(len(H)):
        if cross(H[i], H[(i + 1) % len(H)], p) < 0:
            return False
    return True


class Inst:
    def __init__(self, A, y, eps):
        self.A, self.y = A, y
        a11, a12, a21, a22 = A[0][0], A[0][1], A[1][0], A[1][1]
        # normal equations (A^T A) x = A^T y
        m11 = a11 * a11 + a21 * a21
        m12 = a11 * a12 + a21 * a22
        m22 = a12 * a12 + a22 * a22
        r1 = a11 * y[0] + a21 * y[1]
        r2 = a12 * y[0] + a22 * y[1]
        det = m11 * m22 - m12 * m12
        self.xs = ((m22 * r1 - m12 * r2) / det, (m11 * r2 - m12 * r1) / det)
        self.OPT = min(self.phi(p) for p in PTS)
        self.tau = self.OPT - eps
        self.hc = [0] * (1 << NP)      # P-content of conv(mask)
        self.adm = [False] * (1 << NP)
        self.argmin = [None] * (1 << NP)
        for mask in range(1, 1 << NP):
            pts = [PTS[i] for i in range(NP) if mask >> i & 1]
            H = hull(pts)
            self.hc[mask] = sum(1 << i for i in range(NP) if in_hull(PTS[i], H))
            val, arg = self.min_over(H)
            self.adm[mask] = val >= self.tau
            self.argmin[mask] = arg

    def res(self, x):
        A, y = self.A, self.y
        return (A[0][0] * x[0] + A[0][1] * x[1] - y[0], A[1][0] * x[0] + A[1][1] * x[1] - y[1])

    def phi(self, x):
        r = self.res(x)
        return r[0] * r[0] + r[1] * r[1]

    def grad(self, x):
        A = self.A
        r = self.res(x)
        return (2 * (A[0][0] * r[0] + A[1][0] * r[1]), 2 * (A[0][1] * r[0] + A[1][1] * r[1]))

    def seg_min(self, a, b):
        d = sub(b, a)
        A = self.A
        Ad = (A[0][0] * d[0] + A[0][1] * d[1], A[1][0] * d[0] + A[1][1] * d[1])
        r = self.res(a)
        den = Ad[0] ** 2 + Ad[1] ** 2
        lam = F(0) if den == 0 else min(F(1), max(F(0), -(r[0] * Ad[0] + r[1] * Ad[1]) / den))
        x = (a[0] + lam * d[0], a[1] + lam * d[1])
        return self.phi(x), x

    def min_over(self, H):
        if len(H) == 1:
            return self.phi(H[0]), H[0]
        if len(H) >= 3 and in_hull(self.xs, H):
            return self.phi(self.xs), self.xs
        edges = [(H[0], H[1])] if len(H) == 2 else [(H[i], H[(i + 1) % len(H)]) for i in range(len(H))]
        return min((self.seg_min(a, b) for a, b in edges), key=lambda t: t[0])

    def min_over_halfspace(self, g, xh):
        """exact min of phi over {x : g.(x - xh) >= 0}."""
        if g[0] * (self.xs[0] - xh[0]) + g[1] * (self.xs[1] - xh[1]) >= 0:
            return self.phi(self.xs)
        # minimum on the boundary line xh + s*(-g1, g0)
        d = (-g[1], g[0])
        A = self.A
        Ad = (A[0][0] * d[0] + A[0][1] * d[1], A[1][0] * d[0] + A[1][1] * d[1])
        r = self.res(xh)
        s = -(r[0] * Ad[0] + r[1] * Ad[1]) / (Ad[0] ** 2 + Ad[1] ** 2)
        return self.phi((xh[0] + s * d[0], xh[1] + s * d[1]))


def kappa_and_partitions(I, cap=3000):
    INF = 10 ** 9
    f = [INF] * (1 << NP)
    f[0] = 0
    for rem in range(1, 1 << NP):
        low = rem & -rem
        s = rem
        best = INF
        while s:
            if s & low and I.adm[s]:
                best = min(best, f[rem ^ s] + 1)
            s = (s - 1) & rem
        f[rem] = best
    parts = []

    def rec(rem, acc):
        if len(parts) >= cap:
            return
        if rem == 0:
            parts.append(list(acc))
            return
        low = rem & -rem
        s = rem
        while s:
            if s & low and I.adm[s] and f[rem ^ s] == f[rem] - 1:
                acc.append(s)
                rec(rem ^ s, acc)
                acc.pop()
            s = (s - 1) & rem
    rec(FULL, [])
    return f[FULL], parts


def caterpillar_ok(I, part, order):
    classes = [part[i] for i in order]
    k = len(classes)
    for j in range(k - 1):
        rest_here = 0
        for c in classes[j:]:
            rest_here |= c
        rest_next = 0
        for c in classes[j + 1:]:
            rest_next |= c
        node_content = FULL if j == 0 else I.hc[rest_here]
        covered = I.hc[classes[j]] | I.hc[rest_next]
        if node_content & ~covered:
            return False
    return True


def f_bin(I):
    memo = {}
    pconvex = [m for m in range(1, 1 << NP) if I.hc[m] == m]

    def f(W):
        if W in memo:
            return memo[W]
        if I.adm[W]:
            memo[W] = 1
            return 1
        best = 10 ** 9
        s = (W - 1) & W
        while s:
            if I.hc[s] == s:
                W2 = I.hc[W & ~s]
                if W2 != W:
                    best = min(best, f(s) + f(W2))
            s = (s - 1) & W
        memo[W] = best
        return best
    return f(FULL)


def halfspace_tree_ok(I, part):
    hs = []
    for c in part:
        xh = I.argmin[c]
        g = I.grad(xh)
        if g == (0, 0):
            return False, "zero gradient"
        # class inside H_j
        for i in range(NP):
            if c >> i & 1:
                p = PTS[i]
                if g[0] * (p[0] - xh[0]) + g[1] * (p[1] - xh[1]) < 0:
                    return False, "class not in H"
        if I.min_over_halfspace(g, xh) < I.tau:
            return False, "H not admissible"
        hs.append((g, xh))

    def inH(j, p):
        g, xh = hs[j]
        return g[0] * (p[0] - xh[0]) + g[1] * (p[1] - xh[1]) >= 0
    k = len(part)
    if k == 1:
        return True, "k=1"
    # internal node N_{k-2}: integer points not in H_0..H_{k-3}; must be in H_{k-2} u H_{k-1}
    for p in PTS:
        if not any(inH(j, p) for j in range(k - 2)):
            if not (inH(k - 2, p) or inH(k - 1, p)):
                return False, "last node not covered"
    return True, "ok"


def main():
    nins = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20260929
    rnd = random.Random(seed)
    stats = dict(inst=0, all_fail=0, some_fail=0, fbin_eq=0, hs_ok=0, kappa={}, pairs=0, fails=0,
                 kappa_gt4_E=0, E_holds=0)
    example = None
    while stats["inst"] < nins:
        A = [[F(rnd.randint(-3, 3)) for _ in range(2)] for _ in range(2)]
        if A[0][0] * A[1][1] - A[0][1] * A[1][0] == 0:
            continue
        t = (F(rnd.randint(0, 21), 7), F(rnd.randint(0, 14), 7))
        y = (A[0][0] * t[0] + A[0][1] * t[1] + F(rnd.randint(-3, 3), 5),
             A[1][0] * t[0] + A[1][1] * t[1] + F(rnd.randint(-3, 3), 5))
        eps = F(rnd.choice([1, 5, 20]), 100)
        I = Inst(A, y, eps)
        if I.tau <= I.phi(I.xs):
            continue  # root already certifies
        k, parts = kappa_and_partitions(I)
        if k < 3:
            continue  # caterpillar question is trivial for kappa <= 2
        stats["inst"] += 1
        stats["kappa"][k] = stats["kappa"].get(k, 0) + 1
        # (E) over Z^2 (global integer minimizer inside the box) -> Theorem 2.2 gives kappa <= 4
        big = [(F(i), F(j)) for i in range(-12, 16) for j in range(-12, 15)]
        if min(I.phi(p) for p in big) >= I.OPT:
            stats["E_holds"] += 1
            if k > 4:
                stats["kappa_gt4_E"] += 1
        n_ok = n_tot = 0
        for part in parts:
            for order in permutations(range(k)):
                n_tot += 1
                n_ok += caterpillar_ok(I, part, order)
        stats["pairs"] += n_tot
        stats["fails"] += n_tot - n_ok
        if n_ok < n_tot:
            stats["some_fail"] += 1
        if n_ok == 0:
            stats["all_fail"] += 1
            if example is None:
                example = (A, y, eps, k, parts[0], len(parts))
        fb = f_bin(I)
        stats["fbin_eq"] += fb == k
        ok, why = halfspace_tree_ok(I, parts[0])
        stats["hs_ok"] += ok
        if not ok:
            print("halfspace construction failed:", why, A, y, eps)
    print(f"instances with kappa >= 3: {stats['inst']}; kappa histogram: {dict(sorted(stats['kappa'].items()))}")
    print(f"(partition, ordering) caterpillar pairs tested: {stats['pairs']}; covering violated: {stats['fails']}")
    print(f"instances where SOME ordering of some minimum partition violates covering: {stats['some_fail']}")
    print(f"instances where EVERY ordering of EVERY minimum partition violates covering: {stats['all_fail']}")
    print(f"instances with exact binary minimum (hull pieces) f_bin == kappa: {stats['fbin_eq']}")
    print(f"instances where the halfspace/open-complement binary tree is valid with kappa leaves: {stats['hs_ok']}")
    print(f"instances where (E) holds on Z^2 (checked on a 28x27 box): {stats['E_holds']}; of these kappa > 4: {stats['kappa_gt4_E']}")
    if example:
        A, y, eps, k, part, npart = example
        print("example with every caterpillar invalid:")
        print(f"   A = {[[str(v) for v in r] for r in A]}, y = {[str(v) for v in y]}, eps = {eps}, kappa = {k}, "
              f"#minimum partitions = {npart}")
        print("   one minimum partition:", [[(int(PTS[i][0]), int(PTS[i][1])) for i in range(NP) if c >> i & 1] for c in part])


if __name__ == "__main__":
    main()
