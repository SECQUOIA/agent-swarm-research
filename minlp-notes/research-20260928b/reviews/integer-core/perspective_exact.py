"""Reviewer checks for Section 4 (perspective relaxation versus pairwise hull), exact arithmetic.

1. Lemma 4.1: y'(I + X diag(z) X'/lam)^{-1} y equals min_beta ||y - X beta||^2 + lam sum beta_i^2/z_i
   (beta_i = 0 where z_i = 0), compared EXACTLY (Fractions) on random rational data, with the
   minimizer computed from the support's normal equations (independent of the Woodbury route).
2. Lemma 4.2: closed forms g00, g10 = g01, g11, ghat, delta and the condition-(i) difference,
   checked exactly at 40 rational points (Pythagorean directions v = (c, s_), rational s^2, lam),
   using the explicit 2x2 inverse; plus a sympy identity check in the variable c.
3. Theorem 4.4 on the note's asymmetric data (the numbers dirs/sig/pert are copied from the
   author's script; everything else is recomputed here): (H1), (H2), unique optimum by exhaustive
   enumeration (k <= 4, separable formula, cross-checked against a full 2k x 2k exact inverse
   for k <= 3), all one-per-block pairs conflicting, and the pairwise-hull root value computed
   as the exact LP optimum (maximum of the concave Lagrangian dual over all breakpoints).
4. Theorem 4.3 on the symmetric instance u=(1,0), v=(3/5,4/5), y=u+v, lam=1: same checks.
"""
import random
from fractions import Fraction as F
from itertools import combinations, product
import sympy as sp

rnd = random.Random(7)


def solve(M, rhs):
    n = len(M)
    A = [list(row) + [rhs[i]] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def quad_inv(M, y):
    x = solve(M, y)
    return sum(a * b for a, b in zip(y, x))


def g_woodbury(X, y, z, lam):
    m = len(y)
    M = [[(F(1) if a == b else F(0)) + sum(X[a][i] * z[i] * X[b][i] for i in range(len(z))) / lam
          for b in range(m)] for a in range(m)]
    return quad_inv(M, y)


def g_direct(X, y, z, lam):
    S = [i for i in range(len(z)) if z[i] != 0]
    m = len(y)
    if not S:
        return sum(v * v for v in y)
    # normal equations: (X_S'X_S + lam diag(1/z_S)) beta = X_S'y
    M = [[sum(X[r][i] * X[r][j] for r in range(m)) + (lam / z[i] if i == j else 0) for j in S] for i in S]
    rhs = [sum(X[r][i] * y[r] for r in range(m)) for i in S]
    beta = solve(M, rhs)
    res = [y[r] - sum(X[r][S[a]] * beta[a] for a in range(len(S))) for r in range(m)]
    return sum(v * v for v in res) + sum(lam * beta[a] ** 2 / z[S[a]] for a in range(len(S)))


def check_lemma41():
    worst = 0
    for trial in range(30):
        m, p = rnd.randint(2, 5), rnd.randint(2, 5)
        X = [[F(rnd.randint(-5, 5), rnd.randint(1, 4)) for _ in range(p)] for _ in range(m)]
        y = [F(rnd.randint(-5, 5), rnd.randint(1, 3)) for _ in range(m)]
        z = [F(0) if rnd.random() < 0.3 else F(rnd.randint(1, 9), 9) for _ in range(p)]
        lam = F(rnd.randint(1, 6), rnd.randint(1, 4))
        d = g_woodbury(X, y, z, lam) - g_direct(X, y, z, lam)
        worst = max(worst, abs(d))
    print(f"[4.1] 30 random rational nodes (with zero z entries): max |Woodbury - direct| = {worst} (exact)")


def block(u, v, y, lam, a, b):
    m11 = 1 + (a * u[0] * u[0] + b * v[0] * v[0]) / lam
    m12 = (a * u[0] * u[1] + b * v[0] * v[1]) / lam
    m22 = 1 + (a * u[1] * u[1] + b * v[1] * v[1]) / lam
    det = m11 * m22 - m12 * m12
    return (m22 * y[0] * y[0] - 2 * m12 * y[0] * y[1] + m11 * y[1] * y[1]) / det


def block_values(u, v, y, lam):
    return {"g00": block(u, v, y, lam, 0, 0), "g10": block(u, v, y, lam, 1, 0), "g01": block(u, v, y, lam, 0, 1),
            "g11": block(u, v, y, lam, 1, 1), "gh": block(u, v, y, lam, F(1, 2), F(1, 2))}


PYTH = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 35, 37), (9, 40, 41), (28, 45, 53)]


def check_lemma42():
    bad = 0
    tested = 0
    for (a, b, cc) in PYTH:
        for sgn in (1, -1):
            for lam in (F(1, 3), F(1), F(5, 2)):
                c, sn = F(sgn * a, cc), F(b, cc)
                u, v = (F(1), F(0)), (c, sn)
                w = (1 + c, sn)                      # u + v, norm^2 = 2 + 2c
                t = F(rnd.randint(1, 9), rnd.randint(1, 5))
                y = (t * w[0], t * w[1])             # y = s w/|w| with s^2 = t^2 (2 + 2c)
                s2 = t * t * (2 + 2 * c)
                B = block_values(u, v, y, lam)
                forms = {
                    "g00": s2,
                    "g10": s2 * (1 + 2 * lam - c) / (2 * (1 + lam)),
                    "g01": s2 * (1 + 2 * lam - c) / (2 * (1 + lam)),
                    "g11": s2 * lam / (lam + 1 + c),
                    "gh": 2 * lam * s2 / (2 * lam + 1 + c),
                }
                delta = s2 * (1 - c * c) / (2 * (1 + lam) * (1 + 2 * lam + c))
                condi = s2 * c * (1 + c) / ((1 + lam) * (1 + lam + c))
                ok = all(B[k] == forms[k] for k in forms) and B["g10"] - B["gh"] == delta and \
                    (B["g00"] - B["g10"]) - (B["g10"] - B["g11"]) == condi
                tested += 1
                bad += not ok
    print(f"[4.2] exact rational checks of all closed forms: {tested} parameter sets, failures: {bad}")
    c, lam, s = sp.symbols("c lam s", positive=True)
    sn = sp.sqrt(1 - c ** 2)
    u, v = sp.Matrix([1, 0]), sp.Matrix([c, sn])
    y = s * (u + v) / sp.sqrt(2 + 2 * c)
    def gb(a, b):
        M = sp.eye(2) + (a * u * u.T + b * v * v.T) / lam
        return (y.T * M.adjugate() * y)[0] / M.det()
    res = [sp.simplify(gb(1, 0) - gb(sp.Rational(1, 2), sp.Rational(1, 2)) - s ** 2 * (1 - c ** 2) / (2 * (1 + lam) * (1 + 2 * lam + c))),
           sp.simplify((gb(0, 0) - gb(1, 0)) - (gb(1, 0) - gb(1, 1)) - s ** 2 * c * (1 + c) / ((1 + lam) * (1 + lam + c)))]
    print(f"[4.2] sympy (adjugate route) residuals for delta and condition (i): {res}")


def lp_hull_value(G, k):
    """exact min sum_j sum_p mu_jp G_j(p) s.t. mu_j in simplex, sum_j sum_p mu_jp |p| <= k,
    via max over pi >= 0 of q(pi) = sum_j min_p (G_j(p) + pi |p|) - pi k (LP duality, one coupling row)."""
    P = list(product((0, 1), repeat=2))
    bps = {F(0)}
    for Gj in G:
        for p, q in combinations(P, 2):
            if sum(p) != sum(q):
                t = (Gj[q] - Gj[p]) / (sum(p) - sum(q))
                if t >= 0:
                    bps.add(t)
    q = lambda pi: sum(min(Gj[p] + pi * sum(p) for p in P) for Gj in G) - pi * k
    return max(q(t) for t in bps)


def analyze(blocks, lam, eps_label, exhaustive, fullcheck):
    k = len(blocks)
    Bs = [block_values(u, v, y, lam) for (u, v, y) in blocks]
    G = [{(0, 0): B["g00"], (1, 0): B["g10"], (0, 1): B["g01"], (1, 1): B["g11"]} for B in Bs]
    gstar = [min(B["g10"], B["g01"]) for B in Bs]
    Delta = [abs(B["g10"] - B["g01"]) for B in Bs]
    dl = [gs - B["gh"] for gs, B in zip(gstar, Bs)]
    H1 = max(gs - B["g11"] for gs, B in zip(gstar, Bs)) < min(B["g00"] - gs for gs, B in zip(gstar, Bs))
    H2margin = min(dl) - sum(Delta)
    OPT = sum(gstar)
    line = f"   k={k}: (H1) {H1}; min delta - sum Delta = {float(H2margin):.5f} (eps allowed below this)"
    if exhaustive:
        best, arg = None, []
        for size in range(k + 1):
            for S in combinations(range(2 * k), size):
                val = sum(G[j][(int(2 * j in S), int(2 * j + 1 in S))] for j in range(k))
                if best is None or val < best:
                    best, arg = val, [S]
                elif val == best:
                    arg.append(S)
        line += f"; exhaustive OPT == sum g*: {best == OPT}; #argmin = {len(arg)}"
    # pairwise conflicts among one-per-block supports (separable midpoint values)
    worst = None
    for s1, s2 in combinations(list(product((0, 1), repeat=k)), 2):
        mid = sum(Bs[j]["gh"] if s1[j] != s2[j] else (Bs[j]["g10"] if s1[j] == 0 else Bs[j]["g01"]) for j in range(k))
        gap = OPT - mid
        worst = gap if worst is None else min(worst, gap)
    line += f"; min_pairs OPT - g(mid) = {float(worst):.5f} >= margin: {worst >= H2margin}"
    hull = lp_hull_value(G, k)
    line += f"; hull LP root value == OPT: {hull == OPT}"
    if fullcheck:
        # full 2k x 2k exact inverse versus separable sum, on all supports and all pairwise midpoints
        def full(z):
            m = 2 * k
            M = [[F(0)] * m for _ in range(m)]
            yv = []
            for j, (u, v, y) in enumerate(blocks):
                yv += list(y)
                for a in range(2):
                    for b in range(2):
                        M[2 * j + a][2 * j + b] = (F(1) if a == b else F(0)) + (z[2 * j] * u[a] * u[b] + z[2 * j + 1] * v[a] * v[b]) / lam
            return quad_inv(M, yv)
        agree = True
        for bits in product((0, F(1, 2), 1), repeat=2 * k):
            z = [F(b) for b in bits]
            sep = sum(block(*blocks[j], lam, z[2 * j], z[2 * j + 1]) for j in range(k))
            if full(z) != sep:
                agree = False
        line += f"; full-matrix == separable on all z in {{0,1/2,1}}^{2*k}: {agree}"
    print(line)


def main():
    check_lemma41()
    check_lemma42()
    lam = F(1)
    print("[4.3] symmetric instance u=(1,0), v=(3/5,4/5), y=u+v, lam=1:")
    u0, v0 = (F(1), F(0)), (F(3, 5), F(4, 5))
    y0 = (u0[0] + v0[0], u0[1] + v0[1])
    B = block_values(u0, v0, y0, lam)
    print("   block values:", {k: str(v) for k, v in B.items()}, " delta =", B["g10"] - B["gh"])
    for k in (2, 3, 4):
        analyze([(u0, v0, y0)] * k, lam, "", exhaustive=True, fullcheck=(k <= 3))
    print("[4.4] asymmetric instance (data copied from the author's script):")
    dirs = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)), (F(20, 29), F(21, 29)),
            (F(12, 37), F(35, 37)), (F(28, 53), F(45, 53))]
    sig = [F(1), F(43, 40), F(25, 24), F(35, 36), F(11, 10), F(45, 44)]
    pert = [F(1, 200), F(-1, 150), F(1, 180), F(-1, 250), F(1, 300), F(-1, 220)]
    blocks = []
    for j in range(6):
        u, v = (F(1), F(0)), dirs[j]
        blocks.append((u, v, (sig[j] * (u[0] + v[0]) + pert[j], sig[j] * (u[1] + v[1]))))
    for k in (2, 3, 4):
        analyze(blocks[:k], lam, "", exhaustive=True, fullcheck=(k <= 3))
    analyze(blocks, lam, "", exhaustive=False, fullcheck=False)


if __name__ == "__main__":
    main()
