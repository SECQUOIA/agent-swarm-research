"""M2: adversarial checks of exact quadratic support on a bounded rational polytope.

Independent of the report code: exact linear algebra uses python-flint fmpq_mat,
not the reports' Fraction elimination.  Run with
    code/minlp_solver_lab/.venv/bin/python -B \
        paper-certified-support-cuts/verification/M2_polytope_checks.py

Conventions: q(x) = 1/2 x^T H x + c^T x + c0, P = {x : A x <= b} (bounds included
as rows).  Bordered system for a row subset S:
    [H  A_S^T] [x]   [-c ]
    [A_S  0  ] [l] = [b_S]
KKT sign convention: grad q + A_S^T l = 0, so l >= 0 at a KKT point.
"""

import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

from fractions import Fraction as Fr
from itertools import combinations, product
import math
import random

import flint
import numpy as np
from scipy.optimize import minimize

random.seed(20261003)
CHECKS = []


def check(name, condition):
    CHECKS.append((name, bool(condition)))
    if not condition:
        print("FAIL:", name)


def fq(v):
    v = Fr(v)
    return flint.fmpq(v.numerator, v.denominator)


def to_fr(v):
    return Fr(int(v.p), int(v.q))


def box_rows(lo, hi):
    d = len(lo)
    rows = []
    for i in range(d):
        e = [0] * d
        e[i] = -1
        rows.append((tuple(e), -Fr(lo[i])))
        e = [0] * d
        e[i] = 1
        rows.append((tuple(e), Fr(hi[i])))
    return rows


def qval(H, c, c0, x):
    d = len(x)
    return Fr(c0) + sum(Fr(c[i]) * x[i] for i in range(d)) + Fr(1, 2) * sum(
        Fr(H[i][j]) * x[i] * x[j] for i in range(d) for j in range(d))


def feasible(rows, x):
    return all(sum(Fr(a[i]) * x[i] for i in range(len(x))) <= Fr(b) for a, b in rows)


def rank_rows(rows_S, d):
    if not rows_S:
        return 0
    M = flint.fmpq_mat(len(rows_S), d, [fq(a[i]) for a, _ in rows_S for i in range(d)])
    return M.rank()


def bordered(H, c, rows_S):
    d, k = len(c), len(rows_S)
    n = d + k
    ent = []
    for i in range(d):
        ent += [fq(H[i][j]) for j in range(d)] + [fq(rows_S[s][0][i]) for s in range(k)]
    for s in range(k):
        ent += [fq(rows_S[s][0][j]) for j in range(d)] + [fq(0)] * k
    K = flint.fmpq_mat(n, n, ent)
    r = flint.fmpq_mat(n, 1, [fq(-Fr(v)) for v in c] + [fq(rows_S[s][1]) for s in range(k)])
    return K, r


def enumerate_support(H, c, c0, rows, mode="all"):
    """mode: all | independent | vertices | kkt (sign and reduced-Hessian filter)."""
    d = len(c)
    cand = {}
    dependent_nonsingular = 0
    for k in range(d + 1):
        if mode == "vertices" and k != d:
            continue
        for S in combinations(range(len(rows)), k):
            rows_S = [rows[i] for i in S]
            indep = rank_rows(rows_S, d) == k
            if mode == "independent" and not indep:
                continue
            K, r = bordered(H, c, rows_S)
            if K.det() == 0:
                continue
            if not indep:
                dependent_nonsingular += 1
            z = K.solve(r)
            x = tuple(to_fr(z[i, 0]) for i in range(d))
            lam = tuple(to_fr(z[d + s, 0]) for s in range(k))
            if not feasible(rows, x):
                continue
            if mode == "kkt":
                if any(l < 0 for l in lam):
                    continue
                if not reduced_hessian_pd(H, rows_S, d):
                    continue
            cand.setdefault(x, S)
    vals = sorted((qval(H, c, c0, x), x) for x in cand)
    return (vals[0] if vals else None), cand, dependent_nonsingular


def nullspace_basis(rows_S, d):
    """Exact basis of ker A_S via rref."""
    if not rows_S:
        return [[Fr(int(i == j)) for i in range(d)] for j in range(d)]
    M = flint.fmpq_mat(len(rows_S), d, [fq(a[i]) for a, _ in rows_S for i in range(d)])
    R, rk = M.rref()
    R = [[to_fr(R[i, j]) for j in range(d)] for i in range(len(rows_S))]
    pivots = []
    for i in range(rk):
        for j in range(d):
            if R[i][j] != 0:
                pivots.append(j)
                break
    free = [j for j in range(d) if j not in pivots]
    basis = []
    for f in free:
        v = [Fr(0)] * d
        v[f] = Fr(1)
        for i, p in enumerate(pivots):
            v[p] = -R[i][f]
        basis.append(v)
    return basis


def reduced_hessian_pd(H, rows_S, d):
    Z = nullspace_basis(rows_S, d)
    t = len(Z)
    if t == 0:
        return True
    M = [[sum(Z[a][i] * Fr(H[i][j]) * Z[b][j] for i in range(d) for j in range(d))
          for b in range(t)] for a in range(t)]
    # Sylvester: leading principal minors positive
    for s in range(1, t + 1):
        mat = flint.fmpq_mat(s, s, [fq(M[i][j]) for i in range(s) for j in range(s)])
        if mat.det() <= 0:
            return False
    return True


def grid_min(H, c, c0, rows, lo, hi, G):
    """Exact minimum over the rational grid points of P (an upper bound on min q)."""
    d = len(c)
    axes = [[Fr(lo[i]) + Fr(hi[i] - lo[i]) * Fr(t, G) for t in range(G + 1)] for i in range(d)]
    best = None
    for x in product(*axes):
        if feasible(rows, x):
            v = qval(H, c, c0, x)
            if best is None or v < best:
                best = v
    return best


def float_multistart(H, c, c0, rows, lo, hi, starts=30):
    d = len(c)
    Hf = np.array(H, dtype=float)
    cf = np.array([float(v) for v in c])
    A = np.array([[float(v) for v in a] for a, _ in rows])
    b = np.array([float(v) for _, v in rows])
    f = lambda x: 0.5 * x @ Hf @ x + cf @ x + float(c0)
    g = lambda x: Hf @ x + cf
    cons = [{"type": "ineq", "fun": lambda x: b - A @ x, "jac": lambda x: -A}]
    best = math.inf
    for _ in range(starts):
        x0 = np.array([random.uniform(float(lo[i]), float(hi[i])) for i in range(d)])
        res = minimize(f, x0, jac=g, constraints=cons, method="SLSQP",
                       options={"maxiter": 300, "ftol": 1e-12})
        if np.all(A @ res.x <= b + 1e-9):
            best = min(best, res.fun)
    return best


# ---------------------------------------------------------------- random cross-checks
def random_instance(d):
    lo, hi = [-1] * d, [1] * d
    rows = box_rows(lo, hi)
    for _ in range(random.randint(0, 3)):
        a = tuple(random.randint(-3, 3) for _ in range(d))
        rows.append((a, Fr(random.randint(-2, 4), random.randint(1, 3))))
    kind = random.random()
    if kind < 0.15 and len(rows) > 2 * d:          # duplicate / scaled / opposite rows
        a, bb = rows[-1]
        rows.append((tuple(2 * v for v in a), 2 * bb))
        rows.append((a, bb))
    if 0.15 <= kind < 0.30:                          # implicit equality (two sides)
        a = tuple(random.randint(-2, 2) for _ in range(d))
        bb = Fr(random.randint(-1, 1), 2)
        rows += [(a, bb), (tuple(-v for v in a), -bb)]
    if 0.30 <= kind < 0.35:
        rows.append((tuple([0] * d), Fr(0)))         # zero row 0 <= 0
    Hl = [[0] * d for _ in range(d)]
    style = random.choice(["indef", "psd", "nsd", "singular", "zero"])
    if style == "zero":
        pass
    else:
        R = [[random.randint(-2, 2) for _ in range(d)] for _ in range(d)]
        if style == "indef":
            for i in range(d):
                for j in range(i, d):
                    Hl[i][j] = Hl[j][i] = random.randint(-3, 3)
        else:
            r = d - 1 if style == "singular" else d
            sgn = -1 if style == "nsd" else 1
            for i in range(d):
                for j in range(d):
                    Hl[i][j] = sgn * sum(R[t][i] * R[t][j] for t in range(r))
    c = [Fr(random.randint(-4, 4), random.randint(1, 2)) for _ in range(d)]
    return Hl, c, Fr(random.randint(-2, 2)), rows, lo, hi


n_random = 0
for d, count, G in ((1, 60, 64), (2, 60, 16), (3, 25, 6)):
    for _ in range(count):
        H, c, c0, rows, lo, hi = random_instance(d)
        best, cand, depns = enumerate_support(H, c, c0, rows)
        check(f"dependent subsets are always singular (d={d})", depns == 0)
        bi, _, _ = enumerate_support(H, c, c0, rows, mode="independent")
        bk, _, _ = enumerate_support(H, c, c0, rows, mode="kkt")
        if best is None:
            check("empty result only if grid finds no point", grid_min(H, c, c0, rows, lo, hi, G) is None)
            check("independent-only agrees on emptiness", bi is None)
            n_random += 1
            continue
        val, x = best
        check("minimizer feasible", feasible(rows, x))
        check("independent-only subsets give same minimum", bi is not None and bi[0] == val)
        check("KKT-sign + PD reduced Hessian filter gives same minimum", bk is not None and bk[0] == val)
        gm = grid_min(H, c, c0, rows, lo, hi, G)
        check("exact grid never beats enumerated minimum", gm is None or gm >= val)
        fm = float_multistart(H, c, c0, rows, lo, hi, starts=15 if d < 3 else 25)
        check("float multistart never beats enumerated minimum by > 1e-7", fm >= float(val) - 1e-7)
        n_random += 1

# d = 4 random (smaller number; float check only)
for _ in range(8):
    H, c, c0, rows, lo, hi = random_instance(4)
    best, cand, depns = enumerate_support(H, c, c0, rows)
    check("dependent subsets are always singular (d=4)", depns == 0)
    if best is not None:
        fm = float_multistart(H, c, c0, rows, lo, hi, starts=30)
        check("d=4 float multistart never beats enumerated minimum", fm >= float(best[0]) - 1e-7)
    n_random += 1

# ---------------------------------------------------------------- structured adversarial cases
# (a) degenerate apex of a square pyramid: 4 active facets of rank 3
rows = [((1, 0, 1), Fr(1)), ((-1, 0, 1), Fr(1)), ((0, 1, 1), Fr(1)), ((0, -1, 1), Fr(1)),
        ((0, 0, -1), Fr(0))] + box_rows([-2, -2, -2], [2, 2, 2])
H = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
c = [0, 0, -4]          # q = |x - (0,0,2)|^2 - 4, minimized at apex (0,0,1)
best, cand, _ = enumerate_support(H, c, 0, rows)
check("degenerate apex is the minimizer", best[1] == (0, 0, 1) and best[0] == -3)
apex_bases = [S for S in combinations(range(4), 3)
              if bordered(H, c, [rows[i] for i in S])[0].det() != 0]
check("every 3-subset (basis) of the 4 apex facets is nonsingular", len(apex_bases) == 4)

# (b) redundant facet through an edge, minimizer interior to the edge
rows = box_rows([0, 0, 0], [1, 1, 1]) + [((1, 1, 0), Fr(2))]   # x+y<=2 tight on edge x=y=1
H = [[0, 0, 0], [0, 0, 0], [0, 0, 2]]
c = [-1, -1, -1]        # min at x=y=1, z=1/2
best, cand, _ = enumerate_support(H, c, 0, rows)
check("edge minimizer with 3 active rows of rank 2", best[1] == (1, 1, Fr(1, 2)))

# (c) flat valley: minimizer set is a segment; must return an endpoint
H = [[2, -2], [-2, 2]]   # (x-y)^2, min 0 on the diagonal
best, cand, _ = enumerate_support(H, [0, 0], 0, box_rows([0, 0], [1, 1]))
check("flat valley: value 0 attained", best[0] == 0)
interior_diag = [x for x in cand if x[0] == x[1] and 0 < x[0] < 1]
check("flat valley: no relative-interior diagonal point is a candidate", not interior_diag)

# (d) skew implicit equality 3x - 2y = 1/2 inside a box, indefinite objective
rows = box_rows([-1, -1], [1, 1]) + [((3, -2), Fr(1, 2)), ((-3, 2), Fr(-1, 2))]
H = [[2, 3], [3, -4]]
best, cand, _ = enumerate_support(H, [1, -1], 0, rows)
# independent: parametrize x = t, y = (3t - 1/2)/2 on the segment, minimize exactly
def seg_q(t):
    x, y = t, (3 * t - Fr(1, 2)) / 2
    return qval(H, [1, -1], 0, (x, y))
ts = [Fr(-1, 1), Fr(1, 1)]   # feasible t: -1<=t<=1 and -1<=y<=1  ->  t in [-1/2, 5/6]
tlo, thi = Fr(-1, 2), Fr(5, 6)
# q along the line: quadratic a t^2 + b t + e
a2 = (seg_q(Fr(1)) + seg_q(Fr(-1)) - 2 * seg_q(Fr(0))) / 2
b1 = (seg_q(Fr(1)) - seg_q(Fr(-1))) / 2
cands = [tlo, thi] + ([-b1 / (2 * a2)] if a2 > 0 and tlo < -b1 / (2 * a2) < thi else [])
check("skew implicit equality: matches 1-D parametrization", best[0] == min(seg_q(t) for t in cands))

# (e) singleton from coupled inequalities x+y<=1, -x-y<=-1, x-y<=0, -x+y<=0
rows = box_rows([-5, -5], [5, 5]) + [((1, 1), Fr(1)), ((-1, -1), Fr(-1)), ((1, -1), Fr(0)), ((-1, 1), Fr(0))]
best, cand, _ = enumerate_support([[0, 1], [1, 0]], [0, 0], 0, rows)
check("singleton domain", set(cand) == {(Fr(1, 2), Fr(1, 2))} and best[0] == Fr(1, 4))

# (f) empty by a gap 2^-200, and a contradictory zero row
eps = Fr(1, 2 ** 200)
rows = box_rows([0], [1]) + [((1,), Fr(1, 2)), ((-1,), -Fr(1, 2) - eps)]
check("empty by tiny gap", enumerate_support([[1]], [0], 0, rows)[0] is None)
rows = box_rows([0], [1]) + [((0,), Fr(-1))]
check("contradictory zero row gives empty", enumerate_support([[1]], [0], 0, rows)[0] is None)
check("reversed bounds give empty", enumerate_support([[1]], [0], 0, box_rows([1], [0]))[0] is None)

# (g) constant objective on a lower-dimensional domain
rows = box_rows([0, 0, 0], [1, 1, 1]) + [((1, 1, 1), Fr(1)), ((-1, -1, -1), Fr(-1))]
best, cand, _ = enumerate_support([[0] * 3] * 3, [0, 0, 0], 7, rows)
check("constant objective returns its value", best[0] == 7)

# (h) vertices-only enumeration is NOT enough
best_all = enumerate_support([[2]], [-1], 0, box_rows([0], [1]))[0]   # x^2 - x
best_v = enumerate_support([[2]], [-1], 0, box_rows([0], [1]), mode="vertices")[0]
check("vertices-only misses interior minimum (x^2-x on [0,1])", best_all[0] == Fr(-1, 4) and best_v[0] == 0)

# (i) boundedness is essential: P = {x >= 0} (no upper bound), q = -x
best_unb = enumerate_support([[0]], [-1], 0, [((-1,), Fr(0))])[0]
check("unbounded P: enumeration reports 0 although inf q = -infinity", best_unb[0] == 0)
# ... and the emptiness conclusion also needs boundedness: P = R (no rows), q = x
check("unbounded nonempty P = R with q = x: no candidate retained (false 'empty')",
      enumerate_support([[0]], [1], 0, [])[0] is None)

# (j) retained candidates may be non-KKT (negative multiplier): q = x on [0,1]
_, cand, _ = enumerate_support([[0]], [1], 0, box_rows([0], [1]))
check("non-KKT feasible candidate (x=1) is retained harmlessly", (Fr(1),) in cand)

# ---------------------------------------------------------------- MaxCut reduction
def maxcut_brute(nv, w):
    best = 0
    for s in product((0, 1), repeat=nv):
        best = max(best, sum(wt for (i, j), wt in w.items() if s[i] != s[j]))
    return best


for trial in range(10):
    nv = random.choice([3, 4])
    w = {(i, j): random.randint(1, 4) for i in range(nv) for j in range(i + 1, nv) if random.random() < 0.7}
    H = [[0] * nv for _ in range(nv)]
    c = [0] * nv
    for (i, j), wt in w.items():
        c[i] -= wt
        c[j] -= wt
        H[i][j] += 2 * wt
        H[j][i] += 2 * wt     # q = -sum w (x_i + x_j - 2 x_i x_j); 1/2 x^T H x = sum 2w x_i x_j
    best = enumerate_support(H, c, 0, box_rows([0] * nv, [1] * nv))[0]
    check("exact box support equals -MaxCut", best[0] == -maxcut_brute(nv, w))

# ---------------------------------------------------------------- Hadamard encoding bound
def hadamard_check(trials=60):
    """|det K_S|, Cramer numerators <= n^{n/2} 2^{d eta + 2 k alpha}; value numerator bound."""
    ok = True
    worst = 0.0
    for _ in range(trials):
        d = random.choice([1, 2, 3])
        alpha = random.choice([1, 3, 6])
        eta = random.choice([1, 3, 6])
        A = [tuple(random.randint(-2 ** alpha, 2 ** alpha) for _ in range(d)) for _ in range(d + 2)]
        b = [random.randint(-2 ** alpha, 2 ** alpha) for _ in range(d + 2)]
        rows = list(zip(A, b))
        H = [[0] * d for _ in range(d)]
        for i in range(d):
            for j in range(i, d):
                H[i][j] = H[j][i] = random.randint(-2 ** eta, 2 ** eta)
        c = [random.randint(-2 ** eta, 2 ** eta) for _ in range(d)]
        c0 = random.randint(-2 ** eta, 2 ** eta)
        for k in range(d + 1):
            for S in combinations(range(len(rows)), k):
                K, r = bordered(H, c, [rows[i] for i in S])
                D = K.det()
                if D == 0:
                    continue
                n = d + k
                bound = (n ** (n / 2)) * 2 ** (d * eta + 2 * k * alpha)
                Dint = int(D.p)
                nums = []
                for j in range(d):
                    Kj = flint.fmpq_mat(K)
                    for i in range(n):
                        Kj[i, j] = r[i, 0]
                    nums.append(int(Kj.det().p))
                if abs(Dint) > bound or any(abs(v) > bound for v in nums):
                    ok = False
                # Cramer consistency with the solve
                z = K.solve(r)
                if any(to_fr(z[j, 0]) != Fr(nums[j], Dint) for j in range(d)):
                    ok = False
                # value: q(N/D) = M / (2 D^2), |M| <= 2 (d+1)^2 2^eta B^2
                M = (sum(H[i][j] * nums[i] * nums[j] for i in range(d) for j in range(d))
                     + 2 * Dint * sum(c[j] * nums[j] for j in range(d)) + 2 * Dint * Dint * c0)
                if abs(M) > 2 * (d + 1) ** 2 * 2 ** eta * bound ** 2:
                    ok = False
                worst = max(worst, max([abs(Dint)] + [abs(v) for v in nums]) / bound)
    return ok, worst


ok, worst = hadamard_check()
check("Hadamard bound n^{n/2} 2^{d eta + 2 k alpha} holds for |det K_S| and Cramer numerators", ok)

# ---------------------------------------------------------------- size bound in original encoding
def isize(z):
    return 1 + math.ceil(math.log2(abs(z) + 1))


def rsize(r):
    r = Fr(r)
    return isize(r.numerator) + isize(r.denominator)


def size_bound_check(trials=40):
    """Theorem (sizes): every retained candidate x has x_j = p/q (lowest terms) with
    |p|, q <= B = (2d)^d 2^{d(<q>+1) + 2 d alpha}; q(x) = M/R with |M| <= (d+1)^2 2^{<q>} B^2,
    R <= 2^{<q>} B^2, where alpha = max row size and <q> = size of the monomial coefficients."""
    ok = True
    for _ in range(trials):
        d = random.choice([1, 2, 3])
        lo = [Fr(random.randint(-9, -1), random.randint(1, 7)) for _ in range(d)]
        hi = [Fr(random.randint(1, 9), random.randint(1, 7)) for _ in range(d)]
        rows = box_rows(lo, hi)
        for _ in range(random.randint(0, 2)):
            rows.append((tuple(Fr(random.randint(-30, 30), random.randint(1, 30)) for _ in range(d)),
                         Fr(random.randint(-30, 30), random.randint(1, 30))))
        mono = {(i, j): Fr(random.randint(-50, 50), random.randint(1, 50)) for i in range(d) for j in range(i, d)}
        c = [Fr(random.randint(-50, 50), random.randint(1, 50)) for _ in range(d)]
        c0 = Fr(random.randint(-50, 50), random.randint(1, 50))
        H = [[(2 * mono[(i, i)] if i == j else mono[(min(i, j), max(i, j))]) for j in range(d)] for i in range(d)]
        qsize = rsize(c0) + sum(rsize(v) for v in c) + sum(rsize(v) for v in mono.values())
        alpha = max(sum(rsize(v) for v in a) + rsize(bb) for a, bb in rows)
        B = (2 * d) ** d * 2 ** (d * (qsize + 1) + 2 * d * alpha)
        best, cand, _ = enumerate_support(H, c, c0, rows)
        for x in cand:
            if any(abs(v.numerator) > B or v.denominator > B for v in x):
                ok = False
        if best is not None:
            v = best[0]
            if abs(v.numerator) > (d + 1) ** 2 * 2 ** qsize * B * B or v.denominator > 2 ** qsize * B * B:
                ok = False
    return ok


check("explicit size bound in original rational encoding holds", size_bound_check())

# ---------------------------------------------------------------- Report A polygon theorem
def polygon_candidates(H, c, c0, rows):
    """Report A rule: vertices, PD-curvature edge stationary points, PD interior point."""
    pts = set()
    for (r1, r2) in combinations(rows, 2):
        (a1, b1), (a2, b2) = r1, r2
        det = Fr(a1[0]) * a2[1] - Fr(a1[1]) * a2[0]
        if det == 0:
            continue
        x = ((Fr(b1) * a2[1] - Fr(a1[1]) * b2) / det, (Fr(a1[0]) * b2 - Fr(b1) * a2[0]) / det)
        if feasible(rows, x):
            pts.add(x)
    verts = sorted(pts)
    if not verts:
        return None
    cands = set(verts)
    for u, v in combinations(verts, 2):          # all vertex pairs: superset of edges, safe
        mid = ((u[0] + v[0]) / 2, (u[1] + v[1]) / 2)
        # keep only pairs whose segment lies on a common tight row (an edge or the segment P)
        common = [r for r in rows if sum(Fr(r[0][i]) * u[i] for i in range(2)) == r[1]
                  and sum(Fr(r[0][i]) * v[i] for i in range(2)) == r[1]]
        if not common and len(verts) > 2:
            continue
        dx, dy = v[0] - u[0], v[1] - u[1]
        curv = Fr(1, 2) * (Fr(H[0][0]) * dx * dx + 2 * Fr(H[0][1]) * dx * dy + Fr(H[1][1]) * dy * dy)
        slope = (Fr(H[0][0]) * u[0] + Fr(H[0][1]) * u[1] + Fr(c[0])) * dx + (
            Fr(H[1][0]) * u[0] + Fr(H[1][1]) * u[1] + Fr(c[1])) * dy
        if curv > 0:
            t = -slope / (2 * curv)
            if 0 < t < 1:
                cands.add((u[0] + t * dx, u[1] + t * dy))
    detH = Fr(H[0][0]) * H[1][1] - Fr(H[0][1]) * H[1][0]
    if H[0][0] > 0 and detH > 0:
        x = ((-Fr(c[0]) * H[1][1] + Fr(H[0][1]) * c[1]) / detH,
             (Fr(H[1][0]) * c[0] - Fr(H[0][0]) * c[1]) / detH)
        if feasible(rows, x):
            cands.add(x)
    return min(qval(H, c, c0, x) for x in cands)


for _ in range(80):
    H, c, c0, rows, lo, hi = random_instance(2)
    b_poly = enumerate_support(H, c, c0, rows)[0]
    p_poly = polygon_candidates(H, c, c0, rows)
    check("Report A polygon rule equals bordered enumeration",
          (b_poly is None and p_poly is None) or (b_poly is not None and p_poly == b_poly[0]))

# ---------------------------------------------------------------- Report A example on the simplex
simplex = [((-1, 0), Fr(0)), ((0, -1), Fr(0)), ((1, 1), Fr(1))]
# x + y - (x+y)^2 >= 0 :  q = x + y - x^2 - 2xy - y^2, H = [[-2,-2],[-2,-2]]
b1 = enumerate_support([[-2, -2], [-2, -2]], [1, 1], 0, simplex)[0]
check("x^2+2xy+y^2 <= x+y valid and tight on the simplex", b1[0] == 0)
# 1/4 - xy >= 0 : q = -xy + 1/4, H = [[0,-1],[-1,0]]
b2 = enumerate_support([[0, -1], [-1, 0]], [0, 0], Fr(1, 4), simplex)[0]
check("xy <= 1/4 valid and tight on the simplex at (1/2,1/2)", b2[0] == 0 and b2[1] == (Fr(1, 2), Fr(1, 2)))
# box-hull point: mass 1/2 at (0,0) and (1,1): (x, y, X, Z, Y) = (1/2, 1/2, 1/2, 1/2, 1/2)
pt = dict(x=Fr(1, 2), y=Fr(1, 2), X=Fr(1, 2), Z=Fr(1, 2), Y=Fr(1, 2))
check("point satisfies the row x+y<=1", pt["x"] + pt["y"] <= 1)
check("point violates X+2Z+Y <= x+y (2 > 1)", pt["X"] + 2 * pt["Z"] + pt["Y"] == 2)
check("point violates Z <= 1/4 (Z = 1/2)", pt["Z"] == Fr(1, 2))
# caveat: RLT product x*(1-x-y) >= 0, i.e. x - X - Z >= 0, already cuts this point
check("RLT product x(1-x-y)>=0 also cuts the point", pt["x"] - pt["X"] - pt["Z"] == Fr(-1, 2))
# largest violation over (box hull) ∩ {x+y<=1}, LP over measures on a grid containing (0,0),(1,1)
from scipy.optimize import linprog
g = [Fr(i, 8) for i in range(9)]
P2 = [(a, b) for a in g for b in g]
obj = [-float((a + b) ** 2 - (a + b)) for a, b in P2]
res = linprog(obj, A_ub=[[float(a + b) for a, b in P2]], b_ub=[1.0],
              A_eq=[[1.0] * len(P2)], b_eq=[1.0], bounds=[(0, None)] * len(P2), method="highs")
check("max violation of X+2Z+Y-x-y over box hull ∩ row is 1 (grid LP)", abs(-res.fun - 1.0) < 1e-9)

passed = sum(ok for _, ok in CHECKS)
print(f"random instances: {n_random}; checks passed {passed}/{len(CHECKS)}; "
      f"max Hadamard ratio {worst:.3g}")
raise SystemExit(0 if passed == len(CHECKS) else 1)
