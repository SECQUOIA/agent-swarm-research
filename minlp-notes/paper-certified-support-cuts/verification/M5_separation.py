"""M5: exact checks of complete positive-tolerance separation (C-SEP).

Checks, in exact rational arithmetic:
  1. the L1 distance identity dist_1(q, conv F(P) + cone{e_j : j in J})
     = max_{c in C_J} psi(c) on examples with known distance (including a
     cone coordinate, a lower-dimensional domain, a singleton domain and a
     constant graph);
  2. the grid theorem (Report B Theorem finite-separation) and its sharper
     covering radius 1/N;
  3. the column-generation (Kelley) algorithm of development note M5.md:
     exact master LP, exact primal convex-combination certificate, exact
     quadratic support from Report B's oracle; its support-call bound;
  4. consistency: every returned cut violation <= every certified distance
     upper bound for the same query.
Report B's oracle module is imported read-only.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import random
import sys
from fractions import Fraction
from itertools import product
from math import ceil

from sympy import Rational
import M5_exactlp as lp

sys.dont_write_bytecode = True  # never write into Report B
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261003-convexification/theory'))
import quadratic_polytope as qp  # noqa: E402

random.seed(11)
F = Fraction


def fr(x):
    x = Rational(x)
    return F(int(x.p), int(x.q))


# ---------------------------------------------------------------- problem data
class Problem:
    """Quadratic features F_j(x) given by oracle-order coefficient vectors."""

    def __init__(self, box, rows, features, query, cone=()):
        self.box = [tuple(map(F, b)) for b in box]
        self.rows = [tuple(map(F, r)) for r in rows]
        self.features = [tuple(map(F, f)) for f in features]
        self.q = tuple(map(F, query))
        self.J = set(cone)
        self.d = len(box)
        self.k = len(features)
        self.vertices = [tuple(map(F, v)) for v in qp.polytope_vertices(self.box, self.rows)]
        self.support_calls = 0

    def value(self, x):
        return tuple(qp.quadratic_value(f, x) for f in self.features)

    def support(self, c):
        """Exact min_x c^T F(x) and an exact minimizer."""
        self.support_calls += 1
        coeffs = [sum((cj * f[i] for cj, f in zip(c, self.features)), F(0))
                  for i in range(len(self.features[0]))]
        cert = qp.support_quadratic(self.box, self.rows, coeffs)
        return F(cert["bound"]), tuple(F(v) for v in cert["minimizer"])

    def feature_ranges(self):
        pairs = qp.coefficient_pairs(self.d)
        out = []
        for f in self.features:
            lo = hi = f[0]
            for i in range(self.d):
                a, b = self.box[i]
                lo += min(f[1 + i] * a, f[1 + i] * b)
                hi += max(f[1 + i] * a, f[1 + i] * b)
            for coef, (i, j) in zip(f[1 + self.d:], pairs):
                a, b = self.box[i]
                if i == j:
                    vals = [a * a, b * b] + ([F(0)] if a <= 0 <= b else [])
                else:
                    c_, d_ = self.box[j]
                    vals = [a * c_, a * d_, b * c_, b * d_]
                lo += min(coef * min(vals), coef * max(vals))
                hi += max(coef * min(vals), coef * max(vals))
            out.append((lo, hi))
        return out

    def radius(self):
        return sum(max(abs(lo - q), abs(hi - q)) for (lo, hi), q in zip(self.feature_ranges(), self.q))

    def cone_distance(self, z):
        return sum((max(z[j] - self.q[j], F(0)) if j in self.J else abs(z[j] - self.q[j]))
                   for j in range(self.k))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def feasible(p, x):
    return (all(lo <= xi <= hi for xi, (lo, hi) in zip(x, p.box))
            and all(dot(r[:-1], x) <= r[-1] for r in p.rows))


# ---------------------------------------------------------------- replay checks
def replay_cut(p, c, beta):
    """A cut c^T z >= beta is valid on U_J and strictly separates q."""
    assert all(c[j] >= 0 for j in p.J), "negative cone coefficient"
    true_min, _ = p.support(c)
    assert beta <= true_min, "cut is not valid"
    assert beta > dot(c, p.q), "cut does not separate"
    return beta - dot(c, p.q)


def replay_combination(p, points, weights, eps):
    assert all(w >= 0 for w in weights) and sum(weights) == 1
    assert all(feasible(p, x) for x in points)
    z = [sum((w * p.value(x)[j] for w, x in zip(weights, points)), F(0)) for j in range(p.k)]
    dist = p.cone_distance(z)
    assert dist <= eps, "combination is not within tolerance"
    return dist


# ---------------------------------------------------------------- exact LPs
def master_lp(p, columns):
    """max_{c in C_J} min_s c^T w_s (exact simplex). Returns (model value at c, c).

    The value is recomputed exactly from c; optimality is certified only by
    equality with the primal certificate value (LP duality)."""
    k = p.k
    # variables c_0..c_{k-1}, t ; minimize -t ; t - w_s^T c <= 0
    A = [[-w for w in ws] + [1] for ws in columns]
    b = [0] * len(columns)
    bounds = [((0, 1) if j in p.J else (-1, 1)) for j in range(k)] + [(None, None)]
    st, _, x = lp.solve([0] * k + [-1], A, b, bounds=bounds)
    assert st == "optimal"
    c = tuple(x[:k])
    return min(dot(c, ws) for ws in columns), c


def primal_certificate(p, columns):
    """min over convex weights of the cone-adjusted L1 distance (exact simplex)."""
    T, k = len(columns), p.k
    # variables lambda_0..lambda_{T-1}, e_0..e_{k-1}; minimize sum e
    A_ub, b_ub = [], []
    for j in range(k):
        row = [columns[s][j] for s in range(T)] + [0] * k
        row[T + j] = -1
        A_ub.append(row)            # sum_s lambda_s w_sj - e_j <= 0
        b_ub.append(0)
        if j not in p.J:
            row2 = [-columns[s][j] for s in range(T)] + [0] * k
            row2[T + j] = -1
            A_ub.append(row2)       # -sum_s lambda_s w_sj - e_j <= 0
            b_ub.append(0)
    A_eq = [[1] * T + [0] * k]
    st, _, x = lp.solve([0] * T + [1] * k, A_ub, b_ub, A_eq, [1])
    assert st == "optimal"
    w = list(x[:T])
    assert all(v >= 0 for v in w) and sum(w) == 1
    z = [sum((ws * cols[j] for ws, cols in zip(w, columns)), F(0)) for j in range(k)]
    val = sum((max(z[j], F(0)) if j in p.J else abs(z[j])) for j in range(k))
    return val, w


# ---------------------------------------------------------------- algorithms
def kelley(p, eps, deep=False):
    """Column generation with exact master LP and exact support.

    Returns ('cut', c, beta, certified_upper_or_None, calls) or
    ('within', points, weights, certified_distance, calls)."""
    if not p.vertices:
        return ("empty_domain",)
    pts = [p.vertices[0]]
    cols = [tuple(fi - qi for fi, qi in zip(p.value(pts[0]), p.q))]
    best = (F(0), None, None)  # certified lower bound on the distance and its cut
    iters = 0
    while True:
        ub, c = master_lp(p, cols)
        if (ub - best[0] <= eps) if deep else (ub <= eps):
            val, lam = primal_certificate(p, cols)
            assert val == ub, "master LP not certified optimal"
            if best[1] is not None:
                return ("cut", best[1], best[2], val, iters)
            keep = [(x, w) for x, w in zip(pts, lam) if w > 0]
            return ("within", [x for x, _ in keep], [w for _, w in keep], val, iters)
        assert max(abs(v) for v in c) == 1, "optimal master direction must have norm one"
        L, x = p.support(c)
        iters += 1
        viol = L - dot(c, p.q)
        if viol > best[0]:
            best = (viol, c, L)
            if not deep:
                return ("cut", c, L, None, iters)
        pts.append(x)
        cols.append(tuple(fi - qi for fi, qi in zip(p.value(x), p.q)))


def grid(p, eps, sharp=True):
    """Report B's normal grid; sharp=True uses covering radius 1/N (free) and 1/(2N) (cone)."""
    R = p.radius()
    if sharp:
        N = max(1, ceil(R / eps))
    else:
        N = max(1, ceil(2 * R / eps))
    axes = [[F(i, N) for i in range(N + 1)] if j in p.J else [F(-1) + F(2 * i, N) for i in range(N + 1)]
            for j in range(p.k)]
    pts = []
    for c in product(*axes):
        if not any(c):
            continue
        L, x = p.support(c)
        if L > dot(c, p.q):
            return ("cut", c, L, N)
        assert dot(c, [fi - qi for fi, qi in zip(p.value(x), p.q)]) <= 0
        pts.append(x)
    return ("within", N)


def kelley_bound(p, eps):
    """2k * ceil(2R/eps)^(k-1): cells of side <= eps/R covering the sphere ||c||_inf = 1."""
    R = p.radius()
    return 2 * p.k * max(1, ceil(2 * R / eps)) ** (p.k - 1)


def sphere_grid(p, eps):
    """Grid restricted to ||c||_inf = 1 with covering radius 1/N, N = ceil(R/eps)."""
    R = p.radius()
    N = max(1, ceil(R / eps))
    axes = [[F(i, N) for i in range(N + 1)] if j in p.J else [F(-1) + F(2 * i, N) for i in range(N + 1)]
            for j in range(p.k)]
    for c in product(*axes):
        if max(abs(v) for v in c) != 1:
            continue
        L, x = p.support(c)
        if L > dot(c, p.q):
            return ("cut", c, L, N)
    return ("within", N)


# ---------------------------------------------------------------- examples
def parabola(q, cone=()):
    # x in [0,1], F = (x, x^2); coefficients (const, x, x^2)
    return Problem([(0, 1)], [], [(0, 1, 0), (0, 0, 1)], q, cone)


def run_case(name, make, eps_list, expect=None, exact_dist=None):
    out = []
    for eps in eps_list:
        for deep in (False, True):
            p = make()
            res = kelley(p, F(eps), deep=deep)
            if res[0] == "cut":
                viol = replay_cut(p, res[1], res[2])
                if exact_dist is not None:
                    assert viol <= exact_dist
                    if deep:
                        assert viol >= exact_dist - F(eps)
                ub = res[3]
            elif res[0] == "within":
                d = replay_combination(p, res[1], res[2], F(eps))
                if exact_dist is not None:
                    assert exact_dist <= d
                ub = d
            else:
                ub = None
            if exact_dist is not None and exact_dist > F(eps):
                assert res[0] == "cut", (name, eps, res[0])
            assert p.support_calls <= kelley_bound(p, F(eps))
            out.append((name, str(eps), "deep" if deep else "first", res[0], p.support_calls))
    return out


def main():
    log = []
    # (1) parabola query from the Report B review: exact distance 1/100
    log += run_case("parabola", lambda: parabola((F(3, 10), F(2, 25))),
                    [F(1, 200), F(1, 50), F(1, 1000)], exact_dist=F(1, 100))
    # distance identity at the tangent normal
    p = parabola((F(3, 10), F(2, 25)))
    L, _ = p.support((F(-3, 5), F(1)))
    assert L - dot((F(-3, 5), F(1)), p.q) == F(1, 100)
    # (2) cone coordinate: above the chord is inside U_J, outside conv
    log += run_case("above-chord, J={}", lambda: parabola((F(1, 2), F(1))), [F(1, 100)], exact_dist=F(1, 2))
    log += run_case("above-chord, J={2}", lambda: parabola((F(1, 2), F(1)), cone=(1,)), [F(1, 100)], exact_dist=F(0))
    # (3) lower-dimensional domain x + y = 1/3 in [0,1]^2, F = (x, y, xy)
    seg = lambda: Problem([(0, 1), (0, 1)], [(1, 1, F(1, 3)), (-1, -1, -F(1, 3))],
                          [(0, 1, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 0)],
                          (F(1, 6), F(1, 6), F(1, 24)))
    log += run_case("segment x+y=1/3", seg, [F(1, 1000), F(1, 100)])
    # exact distance there: the hull is {(x,1/3-x,w): x(1/3-x)<=... } ; check cut found at eps < 1/72
    p = seg()
    res = kelley(p, F(1, 1000))
    assert res[0] == "cut"
    # (4) singleton domain and constant graph
    single = lambda: Problem([(F(1, 3), F(1, 3)), (F(1, 2), F(1, 2))], [],
                             [(0, 1, 0, 1, 0, 0), (0, 0, 1, 0, 3, 0)], (F(1, 3) + F(1, 9), F(1, 2) + F(1, 3) / 2))
    log += run_case("singleton", single, [F(1, 100)])
    const = lambda: Problem([(0, 1)], [], [(F(2), 0, 0)], (F(2),))
    log += run_case("constant", const, [F(1, 100)], exact_dist=F(0))
    # (5) random 2-D quadratic blocks; compare Kelley and grid verdicts and certificates
    for trial in range(16):
        k = 2 if trial < 8 else 3
        feats = [tuple(F(random.randint(-2, 2), random.randint(1, 2)) for _ in range(6)) for _ in range(k)]
        box = [(0, 1), (F(-1, 2), 1)]
        rows = [(1, 1, F(5, 4))]
        base = Problem(box, rows, feats, (0,) * k)
        x0 = (F(random.randint(0, 4), 4), F(random.randint(-2, 4), 4))
        if not feasible(base, x0):
            x0 = base.vertices[0]
        q = tuple(z + F(random.randint(-3, 3), 20) for z in base.value(x0))
        J = (k - 1,) if trial % 3 == 0 else ()
        mk = lambda: Problem(box, rows, feats, q, J)
        eps = F(1, 4) if k == 2 else F(1, 20)
        p1 = mk()
        r1 = kelley(p1, eps, deep=True)
        lower, upper = [], []
        if r1[0] == "cut":
            lower.append(replay_cut(mk(), r1[1], r1[2]))
            upper.append(r1[3])
            assert r1[3] - lower[0] <= eps          # two-sided eps-accurate distance
        else:
            upper.append(replay_combination(mk(), r1[1], r1[2], eps))
        assert p1.support_calls <= kelley_bound(p1, eps)
        note = f"kelley={p1.support_calls} bound={kelley_bound(p1, eps)}"
        if k == 2:
            p2 = mk()
            r2 = grid(p2, eps)
            if r2[0] == "cut":
                lower.append(replay_cut(mk(), r2[1], r2[2]))
            else:
                assert r1[0] == "within" or upper[0] <= eps + lower[0]
            note += f" grid={p2.support_calls}({r2[0]})"
            p3 = mk()
            r3 = sphere_grid(p3, eps)
            if r3[0] == "cut":
                lower.append(replay_cut(mk(), r3[1], r3[2]))
            N3 = r3[-1]
            assert p3.support_calls <= 2 * k * (N3 + 1) ** (k - 1)
            note += f" sphere-grid={p3.support_calls}({r3[0]})"
        assert max(lower, default=F(0)) <= min(upper)
        log.append(("random", f"k={k}", str(eps), "deep", r1[0], note))
    # (6) grid covering radius: nearest grid point within 1/N (free) and 1/(2N) (cone)
    for N in (1, 2, 3, 7):
        free_grid = [F(-1) + F(2 * i, N) for i in range(N + 1)]
        cone_grid = [F(i, N) for i in range(N + 1)]
        for s in range(0, 401):
            c = F(-1) + F(2 * s, 400)
            assert min(abs(c - g) for g in free_grid) <= F(1, N)
            c2 = F(s, 400)
            assert min(abs(c2 - g) for g in cone_grid) <= F(1, 2 * N)
    for eps in (F(1, 10**3), F(1, 10**5), F(1, 10**7)):
        p = parabola((F(1, 2), F(1, 4) + F(1, 2 * 10**4)))
        res = kelley(p, eps)
        assert res[0] == "within"
        replay_combination(p, res[1], res[2], eps)
        log.append(("parabola interior", str(eps), "first", res[0], p.support_calls, f"points={len(res[1])}"))
    box3 = [(0, 1), (0, 1)]
    for eps in (F(1, 10**2), F(1, 10**4), F(1, 10**6)):
        p = Problem(box3, [], [(0, 1, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 0)],
                    (F(1, 3), F(1, 2), F(1, 6) - F(1, 1000)))
        res = kelley(p, eps)
        if res[0] == "within":
            replay_combination(p, res[1], res[2], eps)
        else:
            replay_cut(p, res[1], res[2])
        log.append(("xy-box near McCormick face", str(eps), "first", res[0], p.support_calls,
                    f"bound={kelley_bound(p, eps)}"))
    # Example 5.8 of M5.md: q=(0,0) lies in conv{(t,(t^2-2)^2): t in [-3,3]} only via t=+-sqrt(2)
    import sympy as sp
    tt = sp.Symbol("t")
    g = (tt**2 - 2) ** 2
    mid = [(sp.sqrt(2) + (-sp.sqrt(2))) / 2, (g.subs(tt, sp.sqrt(2)) + g.subs(tt, -sp.sqrt(2))) / 2]
    assert [sp.simplify(v) for v in mid] == [0, 0]
    assert set(sp.solve(sp.Eq(g, 0), tt)) == {sp.sqrt(2), -sp.sqrt(2)}  # face z2 = 0 meets the graph only there
    log.append(("example 5.8", "q=(0,0) needs t=+-sqrt(2)", "ok"))
    for row in log:
        print(*row)
    print("all separation checks passed")


if __name__ == "__main__":
    main()
