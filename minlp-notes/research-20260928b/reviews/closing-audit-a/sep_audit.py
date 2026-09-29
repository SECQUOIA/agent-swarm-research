"""Closing audit A, item 2: separable-omega.md, Section 6 (Theorems C, C',
Proposition 6.2 and the tie-free variant).  Independent code, exact rationals.

Node data in coordinate i for J = [l, u] (alpha = 1):
  phi_J(t) = m(t) - (t - l)(u - t) = H(t) - (l + u) t + l u   (m = H - t^2),
a convex piecewise-linear function, so its minimum is attained at a knot of H
or an endpoint.  F(J) = min phi_J; minimizer set is an interval [ya, yb].

Run: python3 sep_audit.py > sep_audit.log
"""
import itertools
import random
import sys
from fractions import Fraction as Fr

sys.setrecursionlimit(10000)


class Coord:
    """m = H - t^2 on [0,1], H = max of lines (slope, intercept)."""

    def __init__(self, lines):
        self.lines = [(Fr(s), Fr(b)) for s, b in lines]
        pts = {Fr(0), Fr(1)}
        for (s1, b1), (s2, b2) in itertools.combinations(self.lines, 2):
            if s1 != s2:
                t = (b2 - b1) / (s1 - s2)
                if 0 <= t <= 1:
                    pts.add(t)
        # true knots: points where the active slopes differ
        self.knots = sorted(t for t in pts if 0 < t < 1 and self._is_knot(t))
        self.cand = sorted(pts)

    def H(self, t):
        return max(s * t + b for s, b in self.lines)

    def _is_knot(self, t):
        h = self.H(t)
        act = {s for s, b in self.lines if s * t + b == h}
        return len(act) > 1

    def m(self, t):
        return self.H(t) - t * t

    def data(self, l, u, sel):
        """F, selected minimizer y, w = a_J(y)."""
        pts = [l, u] + [t for t in self.cand if l < t < u]
        vals = {t: self.H(t) - (l + u) * t + l * u for t in pts}
        F = min(vals.values())
        mins = sorted(t for t in pts if vals[t] == F)
        ya, yb = mins[0], mins[-1]
        if sel == 'proj':
            cen = (l + u) / 2
            y = min(max(cen, ya), yb)
        else:  # 'knot': minimizing knots and endpoints, largest w, then leftmost
            ks = [t for t in mins if t in (l, u) or t in self.knots]
            y = max(ks, key=lambda t: ((t - l) * (u - t), -t))
        return F, y, (y - l) * (u - y), (ya, yb)


def make_RN(n, eps, c):
    n, eps, c = Fr(n), Fr(eps), Fr(c)
    sL = 1 - eps / (4 * (n - 1))
    sR = 1 + eps / (4 * (n - 1))
    phi = (n - 1) * c - eps / 2
    phip = c - eps / (2 * (n - 1))
    half = Fr(1, 2)
    lL = (sL, half - c - sL * half)
    lR = (sR, half - c - sR * half)
    R = Coord([lL, lR, (half, phi), (Fr(3, 2), -half + phi)])
    N = Coord([lL, lR, (half, -phip), (Fr(3, 2), -half - phip)])
    return R, N, phi, phip


def make_Rprime(n, eps, c, p):
    n, eps, c, p = Fr(n), Fr(eps), Fr(c), Fr(p)
    sL = 1 - eps / (4 * (n - 1))
    sR = 1 + eps / (4 * (n - 1))
    phi = (n - 1) * c - eps / 2
    # lines through (p, p - c) with slopes sL, sR
    return Coord([(sL, p - c - sL * p), (sR, p - c - sR * p), (p, phi), (1 + p, -p + phi)])


def box_value(coords, box, sel='knot'):
    return sum(cd.data(l, u, sel)[0] for cd, (l, u) in zip(coords, box))


# ---------------------------------------------------------------- Lemma 6.1 / Theorem C
def agree_interval(A, B, t0, target):
    """Largest interval around t0 (between candidate points) on which A.H - B.H == target,
    checked on all candidate points of both functions (PL, so exact)."""
    pts = sorted(set(A.cand) | set(B.cand) | {t0})
    ok = [A.H(t) - B.H(t) == target for t in pts]
    i = pts.index(t0)
    if not ok[i]:
        return None
    lo = i
    while lo > 0 and ok[lo - 1]:
        lo -= 1
    hi = i
    while hi < len(pts) - 1 and ok[hi + 1]:
        hi += 1
    return pts[lo], pts[hi]


def check_lemma61_thmC(n, eps, c, ncut=199, rng=None):
    eps, c = Fr(eps), Fr(c)
    R, N, phi, phip = make_RN(n, eps, c)
    res = {}
    # (a) root minimizer unique at 1/2 with value -c, both functions
    for name, cd in (('R', R), ('N', N)):
        F, y, w, (ya, yb) = cd.data(Fr(0), Fr(1), 'knot')
        res[f'a_{name}'] = (F == -c and ya == yb == Fr(1, 2))
    # (b) R = N near 1/2, R - N = phi + phi' near 0 and 1
    mid = agree_interval(R, N, Fr(1, 2), 0)
    left = agree_interval(R, N, Fr(0), phi + phip)
    right = agree_interval(R, N, Fr(1), phi + phip)
    res['b_mid'] = mid is not None and mid[0] < Fr(1, 2) < mid[1]
    res['b_ends'] = left is not None and right is not None and left[1] > 0 and right[0] < 1
    # (c) min R = phi, min N = -phi' (m = H - t^2 is concave on each linear piece)
    res['c'] = (min(R.m(t) for t in R.cand) == phi and min(N.m(t) for t in N.cand) == -phip
                and phi - (n - 1) * phip == 0)
    # (d)
    res['d'] = (R.data(Fr(0), Fr(1, 2), 'knot')[0] == phi and R.data(Fr(1, 2), Fr(1), 'knot')[0] == phi)
    # (e)
    res['e'] = N.m(Fr(0)) == -phip and N.m(Fr(1)) == -phip
    # Theorem C steps 2-4 on A_1 (coordinate 0 = R); by symmetry all A_i
    coords = [R] + [N] * (n - 1)
    root = [(Fr(0), Fr(1))] * n
    res['root_invalid'] = box_value(coords, root) + eps < 0
    rc = []
    for half in ((Fr(0), Fr(1, 2)), (Fr(1, 2), Fr(1))):
        b = list(root); b[0] = half
        rc.append(box_value(coords, b) + eps)
    res['right_cut_margin_eps/2'] = all(v == eps / 2 for v in rc)
    worst = None
    pts = [Fr(k, ncut + 1) for k in range(1, ncut + 1)]
    if rng is not None:
        pts += [Fr(rng.randint(1, 10 ** 6 - 1), 10 ** 6) for _ in range(50)]
    pts += [Fr(1, 10 ** 9), 1 - Fr(1, 10 ** 9)]
    if n >= 2:
        for t in pts:
            for half in ((Fr(0), t), (t, Fr(1))):
                b = list(root); b[1] = half
                v = box_value(coords, b) + eps
                worst = v if worst is None else max(worst, v)
    res['wrong_cut_children_invalid'] = worst < 0
    bound = -n * c + eps + eps / (2 * (n - 1))
    res['wrong_cut_bound_holds'] = worst <= bound
    return res, (mid, left, right, worst, bound)


# ---------------------------------------------------------------- tree simulation
def run_rule(coords, eps, choose, sel='knot', limit=100000):
    """Count nodes of the tree built by `choose(box, data)` -> (coord, point) on invalid boxes."""
    n = len(coords)
    stack = [tuple((Fr(0), Fr(1)) for _ in range(n))]
    T = 0
    while stack:
        box = stack.pop()
        T += 1
        if T > limit:
            return None
        data = [cd.data(l, u, sel) for cd, (l, u) in zip(coords, box)]
        if sum(d[0] for d in data) + eps >= 0:
            continue
        j, pt = choose(box, data)
        l, u = box[j]
        assert l < pt < u, (box, j, pt)
        for half in ((l, pt), (pt, u)):
            b = list(box); b[j] = half
            stack.append(tuple(b))
    return T


def omega_choose(box, data):
    ws = [d[2] for d in data]
    j = max(range(len(ws)), key=lambda k: (ws[k], -k))
    return j, data[j][1]


def deficit_choose(box, data):
    cands = [k for k in range(len(data)) if data[k][2] > 0]
    j = min(cands, key=lambda k: (data[k][0], k))
    return j, data[j][1]


# ---------------------------------------------------------------- G(n) by Pareto DP
def pareto_min(vecs):
    vecs = sorted(set(vecs), key=lambda v: (sum(v), v))
    out = []
    for v in vecs:
        if not any(all(a <= b for a, b in zip(o, v)) for o in out):
            out.append(v)
    return out


def G_dp(n, cap=None):
    """P[S] = Pareto-minimal count vectors (N_i) of subtrees rooted at a corner node with
    cut set S, when every node with a free coordinate cuts a free coordinate.  A node is
    counted in N_i iff i is free there.  Vectors with max > cap are dropped; this is exact
    whenever the result has max <= cap (components only grow towards the root)."""
    full = (1 << n) - 1
    P = {full: [tuple([0] * n)]}
    back = {}
    for size in range(n - 1, -1, -1):
        for S in range(1 << n):
            if bin(S).count('1') != size:
                continue
            free = [i for i in range(n) if not S >> i & 1]
            ind = tuple(0 if S >> i & 1 else 1 for i in range(n))
            vecs = {}
            for j in free:
                ch = P[S | 1 << j]
                for a in ch:
                    for b in ch:
                        v = tuple(x + y + z for x, y, z in zip(ind, a, b))
                        if (cap is None or max(v) <= cap) and v not in vecs:
                            vecs[v] = (j, a, b)
            P[S] = pareto_min(list(vecs))
            for v in P[S]:
                back[(S, v)] = vecs[v]
    if not P[0]:
        return None, None, P, back
    best = min(P[0], key=max)
    return max(best), best, P, back


def plan_rule_counts(n, eps, c):
    """Follow an optimal reference tree from the DP; cut free coordinates at 1/2.
    Simulate exactly on every A_i and return the node counts."""
    G, best, P, back = G_dp(n)
    R, N, phi, phip = make_RN(n, eps, c)
    Ts = []
    for i in range(n):
        coords = [R if k == i else N for k in range(n)]
        T = 0
        stack = [(tuple((Fr(0), Fr(1)) for _ in range(n)), 0, best)]
        while stack:
            box, S, v = stack.pop()
            T += 1
            val = box_value(coords, box)
            if val + eps >= 0:
                continue
            # must be a planned corner node with a free coordinate
            j, a, b = back[(S, v)]
            for half, vv in (((Fr(0), Fr(1, 2)), a), ((Fr(1, 2), Fr(1)), b)):
                bb = list(box); bb[j] = half
                stack.append((tuple(bb), S | 1 << j, vv))
        Ts.append(T)
    return G, best, Ts


def random_corner_node(n, S, rng):
    box = []
    for k in range(n):
        if S >> k & 1:
            t = Fr(rng.randint(1, 999), 1000)
            box.append((Fr(0), t) if rng.random() < 0.5 else (t, Fr(1)))
        else:
            box.append((Fr(0), Fr(1)))
    return box


def main(parts):
    rng = random.Random(20260929)
    eps = Fr(1, 100)
    if 'C' in parts:
        partC(rng, eps)
    if 'corner' in parts:
        part_corner(rng, eps)
    if 'G' in parts:
        part_G(eps)
    if 'omega' in parts:
        part_omega(eps)


def partC(rng, eps):
    print('== Lemma 6.1 and Theorem C, eps = 1/100, c = 1/(5n), n = 2..40')
    allok = True
    for n in range(2, 41):
        res, (mid, left, right, worst, bound) = check_lemma61_thmC(n, eps, Fr(1, 5 * n), ncut=99)
        ok = all(res.values())
        allok &= ok
        if n in (2, 3, 5, 12, 17, 40) or not ok:
            print(f'n={n}: all={ok} {"" if ok else res}; R=N on [{float(mid[0]):.5f},{float(mid[1]):.5f}]; '
                  f'R-N const on [0,{left[1]}] and [{right[0]},1]; worst wrong-cut child value+eps = {worst} '
                  f'<= bound {bound}')
    print(f'all n = 2..40 pass: {allok}')

    print('\n== random admissible (eps, c) inside (6.1), n = 2..12 (incl. c near both ends)')
    cnt = bad = 0
    for _ in range(300):
        n = rng.randint(2, 12)
        emax = Fr(n - 1, 2 * n)
        e = emax * Fr(rng.randint(1, 999), 1000)
        lo = e * (2 * n - 1) / (2 * n * (n - 1))
        hi = (1 + 2 * e) / (4 * n)
        r = rng.choice([Fr(1, 10 ** 6), Fr(rng.randint(1, 999), 1000), 1 - Fr(1, 10 ** 6)])
        cc = lo + (hi - lo) * r
        res, _ = check_lemma61_thmC(n, e, cc, ncut=29, rng=rng)
        cnt += 1
        if not all(res.values()):
            bad += 1
            print('FAIL', n, e, cc, res)
    print(f'{cnt} random admissible parameter sets, failures: {bad}')

    print('\n== (6.1) is needed: parameters just outside each end')
    for n in (2, 3, 6):
        e = Fr(1, 100)
        lo = e * (2 * n - 1) / (2 * n * (n - 1))
        hi = (1 + 2 * e) / (4 * n)
        for tag, cc in (('c = left end', lo), ('c = right end', hi)):
            res, _ = check_lemma61_thmC(n, e, cc, ncut=9)
            print(f'n={n} {tag}: failing items = {[k for k, v in res.items() if not v]}')


def part_corner(rng, eps):
    print('\n== Theorem C\': corner nodes (identical data for all free i, invalid), eps = 1/100, c = 1/(5n)')
    for n in range(2, 8):
        R, N, phi, phip = make_RN(n, eps, Fr(1, 5 * n))
        tested = bad = 0
        for _ in range(400):
            S = rng.randrange(0, (1 << n) - 1)  # at least one free coordinate
            box = random_corner_node(n, S, rng)
            free = [i for i in range(n) if not S >> i & 1]
            sig = set()
            for i in free:
                coords = [R if k == i else N for k in range(n)]
                for sel in ('knot', 'proj'):
                    data = [cd.data(l, u, sel) for cd, (l, u) in zip(coords, box)]
                    val = sum(d[0] for d in data)
                    sig.add((sel, val, tuple(d[1] for d in data)))
                    if val + eps >= 0:
                        bad += 1
            if len(sig) != 2:
                bad += 1
            tested += 1
        print(f'n={n}: {tested} random corner nodes, mismatches/valid: {bad}')


CAPS = {2: None, 3: None, 4: None, 5: None, 6: 26, 7: 44}


def part_G(eps):
    print('\n== Theorem C\': G(n) by an independent Pareto DP')
    for n in range(2, 8):
        cap = CAPS[n]
        G, best, P, back = G_dp(n, cap)
        while G is None:
            cap += 4
            G, best, P, back = G_dp(n, cap)
        avg = Fr(2 ** (n + 1) - n - 2, n)
        det = Fr(2 * G + 1, 3)
        rnd = (2 * avg + 1) / 3
        print(f'n={n}: G={G} vector={best} sum_i N_i >= {2 ** (n + 1) - n - 2}, ceil(avg)={-(-avg.numerator // avg.denominator)}; '
              f'det ratio (2G+1)/3 = {det}; rand ratio = {rnd}; 2^(n+2)/(3n) = {Fr(2 ** (n + 2), 3 * n)}; '
              f'|P(empty)| = {len(P[0])}', flush=True)
    print('\n== attainment: rule following an optimal reference tree, cuts at 1/2')
    for n in range(2, 6):
        G, best, Ts = plan_rule_counts(n, eps, Fr(1, 5 * n))
        print(f'n={n}: T(A_i) = {Ts}, 2*vector+1 = {[2 * v + 1 for v in best]}, max = {max(Ts)} = 2G+1: {max(Ts) == 2 * G + 1}')


def part_omega(eps):
    print('\n== Proposition 6.2: omega (ties lowest index) and deficit on A_i, both selections')
    for n in range(2, 7):
        R, N, phi, phip = make_RN(n, eps, Fr(1, 5 * n))
        for sel in ('knot', 'proj'):
            om, de = [], []
            for i in range(n):
                coords = [R if k == i else N for k in range(n)]
                om.append(run_rule(coords, eps, omega_choose, sel))
                de.append(run_rule(coords, eps, deficit_choose, sel))
            exp = [2 ** (i + 2) - 1 for i in range(n)]
            print(f'n={n} sel={sel}: omega {om} deficit {de} expected 2^(i+1)-1 (i 1-based) {exp}: '
                  f'{om == exp and de == exp}')
    print('\n== tie-free variant R\' (p = 1/2 + 1/50), every labelling')
    p = Fr(1, 2) + Fr(1, 50)
    for n in range(2, 7):
        c = Fr(1, 5 * n)
        R, N, phi, phip = make_RN(n, eps, c)
        Rp = make_Rprime(n, eps, c, p)
        Fp, yp, wp, (ya, yb) = Rp.data(Fr(0), Fr(1), 'knot')
        cond = n * c < p * (1 - p) + eps / 2
        halves = [Rp.data(Fr(0), p, 'knot')[0], Rp.data(p, Fr(1), 'knot')[0]]
        for sel in ('knot', 'proj'):
            om = []
            for i in range(n):
                coords = [Rp if k == i else N for k in range(n)]
                om.append(run_rule(coords, eps, omega_choose, sel))
            # OPT_min: cut R' first at its minimizer
            print(f'n={n} sel={sel}: root F_R\'={Fp} (=-c: {Fp == -c}), minimizer {ya}={yb}, w={wp}; '
                  f'nc < p(1-p)+eps/2: {cond}; F_R\' on halves = {halves} (=phi: {all(h == phi for h in halves)}); '
                  f'omega on every labelling {om} (2^(n+1)-1 = {2 ** (n + 1) - 1})')

    print('\n== simpler argument for Prop 6.2: a cut coordinate of length < 1 has w <= len^2/4 < 1/4')
    print('   (checked implicitly above; the knot distance t_N is not needed)')


if __name__ == '__main__':
    main(sys.argv[1:] or ['C', 'corner', 'G', 'omega'])
