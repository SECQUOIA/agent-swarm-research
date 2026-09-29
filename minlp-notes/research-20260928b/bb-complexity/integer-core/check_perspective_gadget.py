"""Exact and high-precision checks for Section 4 (perspective versus pairwise hull).

1. Symbolic: block closed forms, delta = s^2 sin^2(th) / (2(1+lam)(1+2lam+c)),
   and condition (i) <=> c (1 + c) > 0.
2. The perspective formula g(z) = y'(I + X diag(z) X'/lam)^{-1} y against direct
   minimization over beta (mpmath, 40 digits), including zero entries of z.
3. Exact rational symmetric instance (u = (1,0), v = (3/5,4/5), y = u + v, lam = 1):
   enumerate all supports with |S| <= k (k <= 4) with exact Fractions via the full
   2k x 2k matrix; check OPT = k g10, the argmin set, and g(mid) = OPT - |D| delta
   for all pairs of optimal supports.
4. Exact rational asymmetric instance (distinct Pythagorean directions and
   perturbed responses per block): check the hypotheses of Theorem 4.4, unique
   optimum, and that all 2^k one-per-block supports pairwise conflict (k <= 4
   exhaustively with full matrices; k = 6 via the separable formula).
5. Pairwise-hull (disjunctive) root value: exact dual certificate showing the
   root bound equals OPT for both instances.
"""
from fractions import Fraction as F
from itertools import combinations, product
import sympy as sp
import mpmath as mp

# ---------------------------------------------------------------- 1. symbolic
c, s, lam = sp.symbols("c s lam", positive=True)
sn = sp.sqrt(1 - c ** 2)
u = sp.Matrix([1, 0])
v = sp.Matrix([c, sn])
w = (u + v) / sp.sqrt(((u + v).T * (u + v))[0])
y = s * w
I2 = sp.eye(2)


def gblock(z1, z2):
    M = I2 + (z1 * u * u.T + z2 * v * v.T) / lam
    return sp.simplify((y.T * M.inv() * y)[0])


g00 = sp.simplify((y.T * y)[0])
g10, g01, g11 = gblock(1, 0), gblock(0, 1), gblock(1, 1)
gh = gblock(sp.Rational(1, 2), sp.Rational(1, 2))
checks = {
    "g00 = s^2": sp.simplify(g00 - s ** 2),
    "g10 formula": sp.simplify(g10 - s ** 2 * (1 + 2 * lam - c) / (2 * (1 + lam))),
    "g01 = g10": sp.simplify(g01 - g10),
    "g11 formula": sp.simplify(g11 - s ** 2 * lam / (lam + 1 + c)),
    "ghat formula": sp.simplify(gh - 2 * lam * s ** 2 / (2 * lam + 1 + c)),
    "delta formula": sp.simplify((g10 - gh) - s ** 2 * (1 - c ** 2) / (2 * (1 + lam) * (1 + 2 * lam + c))),
}
for k_, val in checks.items():
    print(f"[symbolic] {k_}: residual = {val}")
cond = sp.factor(sp.simplify(((g00 - g10) - (g10 - g11)) * 2 * (1 + lam) * (1 + lam + c) / s ** 2))
print(f"[symbolic] ((g00-g10)-(g10-g11)) * 2(1+lam)(1+lam+c)/s^2 = {cond}")

# ---------------------------------------------------------------- 2. perspective formula
mp.mp.dps = 40


def g_matrix(X, y, z, lamv):
    m = len(y)
    M = mp.eye(m) + X * mp.diag(z) * X.T / lamv
    return (y.T * mp.lu_solve(M, y))[0]


def g_direct(X, y, z, lamv):
    idx = [i for i in range(len(z)) if z[i] != 0]
    if not idx:
        return (y.T * y)[0]
    Xs = mp.matrix([[X[r, i] for i in idx] for r in range(X.rows)])
    D = mp.diag([lamv / z[i] for i in idx])
    beta = mp.lu_solve(Xs.T * Xs + D, Xs.T * y)
    r = y - Xs * beta
    return (r.T * r)[0] + sum(lamv * beta[a] ** 2 / z[idx[a]] for a in range(len(idx)))


rng_state = 12345


def rnd():
    global rng_state
    rng_state = (1103515245 * rng_state + 12345) % (2 ** 31)
    return mp.mpf(rng_state) / 2 ** 31


worst = mp.mpf(0)
for trial in range(20):
    m, p = 5, 4
    X = mp.matrix([[rnd() - mp.mpf(1) / 2 for _ in range(p)] for _ in range(m)])
    yy = mp.matrix([rnd() for _ in range(m)])
    z = [rnd() if (trial + i) % 3 else mp.mpf(0) for i in range(p)]
    lamv = mp.mpf(1) / 2 + rnd()
    worst = max(worst, abs(g_matrix(X, yy, z, lamv) - g_direct(X, yy, z, lamv)))
print(f"[perspective formula] max |matrix - direct| over 20 random nodes (40 digits): {mp.nstr(worst, 5)}")

# ---------------------------------------------------------------- exact helpers


def mat_inv_quad(Mrows, yv):
    """y' M^{-1} y for a small exact Fraction matrix via Gaussian elimination."""
    n = len(yv)
    A = [row[:] + [yv[i]] for i, row in enumerate(Mrows)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col] / A[col][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[col])]
    x = [A[i][n] / A[i][i] for i in range(n)]
    return sum(a * b for a, b in zip(yv, x))


def full_g(blocks, z, lamv):
    """Exact perspective value for block-diagonal design; blocks = [(u, v, y)]."""
    k = len(blocks)
    m = 2 * k
    M = [[F(0)] * m for _ in range(m)]
    yv = []
    for j, (uu, vv, yj) in enumerate(blocks):
        yv += list(yj)
        zu, zv = z[2 * j], z[2 * j + 1]
        for a in range(2):
            for b in range(2):
                M[2 * j + a][2 * j + b] = (F(1) if a == b else F(0)) + (zu * uu[a] * uu[b] + zv * vv[a] * vv[b]) / lamv
    return mat_inv_quad(M, yv)


def block_vals(uu, vv, yj, lamv):
    def gb(z1, z2):
        M = [[(F(1) if a == b else F(0)) + (z1 * uu[a] * uu[b] + z2 * vv[a] * vv[b]) / lamv for b in range(2)] for a in range(2)]
        return mat_inv_quad(M, list(yj))
    return dict(g00=gb(0, 0), g10=gb(1, 0), g01=gb(0, 1), g11=gb(1, 1), gh=gb(F(1, 2), F(1, 2)))


def enumerate_supports(blocks, k, lamv):
    vals = {}
    for size in range(k + 1):
        for S in combinations(range(2 * k), size):
            z = [F(1) if i in S else F(0) for i in range(2 * k)]
            vals[S] = full_g(blocks, z, lamv)
    return vals


def one_per_block(k):
    for choice in product((0, 1), repeat=k):
        yield tuple(2 * j + choice[j] for j in range(k))


def midpoint_value(blocks, S, T, lamv, k):
    z = [(F(1 if i in S else 0) + F(1 if i in T else 0)) / 2 for i in range(2 * k)]
    return full_g(blocks, z, lamv)


# ---------------------------------------------------------------- 3. symmetric exact instance
lamv = F(1)
u0, v0 = (F(1), F(0)), (F(3, 5), F(4, 5))
y0 = (u0[0] + v0[0], u0[1] + v0[1])
bv = block_vals(u0, v0, y0, lamv)
cth = F(3, 5)
s2 = y0[0] ** 2 + y0[1] ** 2
delta_formula = s2 * (1 - cth ** 2) / (2 * (1 + lamv) * (1 + 2 * lamv + cth))
print(f"[symmetric] block values: " + ", ".join(f"{k_}={v_}" for k_, v_ in bv.items()))
print(f"[symmetric] delta = g10 - ghat = {bv['g10'] - bv['gh']}; closed form = {delta_formula}; g10==g01: {bv['g10'] == bv['g01']}")
print(f"[symmetric] (g00-g10) - (g10-g11) = {(bv['g00'] - bv['g10']) - (bv['g10'] - bv['g11'])} (> 0 required)")
for k in (2, 3, 4):
    blocks = [(u0, v0, y0)] * k
    vals = enumerate_supports(blocks, k, lamv)
    OPT = min(vals.values())
    argmin = sorted(S for S, val in vals.items() if val == OPT)
    opb = sorted(one_per_block(k))
    ok_mid = True
    for S, T in combinations(opb, 2):
        D = sum(1 for j in range(k) if S[j] != T[j])
        if midpoint_value(blocks, S, T, lamv, k) != OPT - D * (bv["g10"] - bv["gh"]):  # OPT - |D| delta
            ok_mid = False
    print(f"[symmetric k={k}] supports={len(vals)} OPT={OPT} == k*g10: {OPT == k * bv['g10']}; "
          f"argmin == one-per-block ({len(opb)}): {argmin == opb}; all midpoints = OPT - |D| delta: {ok_mid}")

# ---------------------------------------------------------------- 4. asymmetric exact instance
dirs = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)), (F(20, 29), F(21, 29)),
        (F(12, 37), F(35, 37)), (F(28, 53), F(45, 53))]
sig = [F(1), F(43, 40), F(25, 24), F(35, 36), F(11, 10), F(45, 44)]  # equalizes s_j^2 = sig_j^2 (2 + 2 c_j) near 16/5
pert = [F(1, 200), F(-1, 150), F(1, 180), F(-1, 250), F(1, 300), F(-1, 220)]


def asym_blocks(k):
    out = []
    for j in range(k):
        uu, vv = (F(1), F(0)), dirs[j]
        yj = (sig[j] * (uu[0] + vv[0]) + pert[j], sig[j] * (uu[1] + vv[1]))
        out.append((uu, vv, yj))
    return out


def asym_report(k, exhaustive):
    blocks = asym_blocks(k)
    B = [block_vals(*b, lamv) for b in blocks]
    gstar = [min(b["g10"], b["g01"]) for b in B]
    Delta = [abs(b["g10"] - b["g01"]) for b in B]
    dlt = [gs - b["gh"] for gs, b in zip(gstar, B)]
    first = [b["g00"] - gs for gs, b in zip(gstar, B)]
    second = [gs - b["g11"] for gs, b in zip(gstar, B)]
    hyp_convex = max(second) < min(first)
    hyp_gap = sum(Delta) < min(dlt)
    distinct = len(set(B[j]["g10"] for j in range(k)) | set(B[j]["g01"] for j in range(k))) == 2 * k
    eps_max = min(dlt) - sum(Delta)
    print(f"[asym k={k}] max second gain {float(max(second)):.4f} < min first gain {float(min(first)):.4f}: {hyp_convex}; "
          f"sum Delta={float(sum(Delta)):.5f} < min delta={float(min(dlt)):.5f}: {hyp_gap}; "
          f"eps allowed < {float(eps_max):.5f}; all 2k singleton values distinct: {distinct}")
    OPT = sum(gstar)
    if exhaustive:
        vals = enumerate_supports(blocks, k, lamv)
        vmin = min(vals.values())
        argmin = [S for S, val in vals.items() if val == vmin]
        print(f"   exhaustive: OPT={float(vmin):.6f} == sum g*: {vmin == OPT}; unique argmin: {len(argmin) == 1}")
    worst = None
    for S, T in combinations(sorted(one_per_block(k)), 2):
        if exhaustive:
            mv = midpoint_value(blocks, S, T, lamv, k)
        else:
            mv = sum(B[j]["gh"] if S[j] != T[j] else (B[j]["g10"] if S[j] % 2 == 0 else B[j]["g01"]) for j in range(k))
        gap = OPT - mv
        worst = gap if worst is None or gap < worst else worst
    print(f"   min over pairs of OPT - g(mid) = {float(worst):.6f} (> eps_allowed bound {float(eps_max):.6f} expected)")
    # 5. hull dual certificate: common pi in [max second, min first]
    pi = max(second)
    ok = all(min(B[j]["g00"], gstar[j] + pi, B[j]["g11"] + 2 * pi) == gstar[j] + pi for j in range(k))
    dual = sum(min(B[j]["g00"], min(B[j]["g10"], B[j]["g01"]) + pi, B[j]["g11"] + 2 * pi) for j in range(k)) - pi * k
    print(f"   hull root dual certificate (pi={float(pi):.5f}): dual value == OPT: {dual == OPT}; minimizers at |p|=1: {ok}")


asym_report(2, True)
asym_report(3, True)
asym_report(4, True)
asym_report(6, False)

# symmetric hull certificate
for k in (2, 5, 10):
    pi = bv["g10"] - bv["g11"]
    dual = k * min(bv["g00"], bv["g10"] + pi, bv["g11"] + 2 * pi) - pi * k
    print(f"[symmetric hull k={k}] dual value {dual} == k*g10: {dual == k * bv['g10']}")
