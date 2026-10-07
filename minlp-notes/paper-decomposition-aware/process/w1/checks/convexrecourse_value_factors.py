"""Exact checks for convex value factors, the piece-energy identity and the
three-piece example f_M.

Claims checked (finite exact evidence; proofs are in the LaTeX fragment):
  (1) f_M = M(y1+y2-z)^2+(y1-2z+1/2)^2, y in [0,1]^2, z in [0,3/4]:
      value pieces (1/2-2z)^2, 0, M(z-1/2)^2/(M+1) and their responses;
      with the v-only term moved to the retained part (direct diagonal 2M+8),
      piece energies sigma_r=(B_r' C B_r) are 2M, 2M+8, 2(M+2)^2/(M+1),
      so the certified curvature is 2M+8-min sigma = 8.
  (2) Random positive definite blocks: on the critical region of a random
      parameter, Gamma = B'CB + B'K + K'B equals -B'CB, its diagonal equals the
      least extension energy over free coordinates, and exact second
      differences of the value along coordinate lines equal Gamma_jj.
  (3) Along random coordinate lines, phi - (max_r Gamma_r,jj) t^2/2 has
      nonpositive exact second differences (concavity across pieces).
  (4) The three-piece ladder: identity z^2+f_M-1/20 = t^2+Mr^2+s^2+u/5 and
      growth F-F* >= |x-x*|^2/12 at random rational feasible points.
"""
import random
from fractions import Fraction as Fr
import sympy as sp

from convexrecourse_common import box_qp_pd, matmul, transpose, inverse, mat

random.seed(20261003)
counts = {}


def bump(k, n=1):
    counts[k] = counts.get(k, 0) + n


# ---------------------------------------------------------------- (1) f_M
def fM_block(M):
    # f = 1/2 y'Cy + y'K z + c'y + (z-only terms); y=(y1,y2)
    # M(y1+y2-z)^2 = M(y1+y2)^2 - 2M(y1+y2)z + M z^2
    # (y1-2z+1/2)^2 = y1^2 + 2 y1(-2z+1/2) + (-2z+1/2)^2
    C = mat([[2 * M + 2, 2 * M], [2 * M, 2 * M]])
    K = [[Fr(-2 * M - 4)], [Fr(-2 * M)]]
    c = [Fr(1), Fr(0)]
    return C, K, c


def fM_value(M, z):
    C, K, c = fM_block(M)
    g = [K[0][0] * z + c[0], K[1][0] * z + c[1]]
    val, y, pat = box_qp_pd(C, g, [Fr(0)] * 2, [Fr(1)] * 2)
    direct = M * z * z + (-2 * z + Fr(1, 2)) ** 2   # z-only terms
    return val + direct, y, pat


for M in [Fr(1), Fr(3), Fr(100), Fr(10 ** 6), Fr(7, 3)]:
    zs = [Fr(k, 240) for k in range(0, 181)]  # [0, 3/4]
    for z in zs:
        v, y, pat = fM_value(M, z)
        if z <= Fr(1, 4):
            exp_v, exp_y = (Fr(1, 2) - 2 * z) ** 2, [Fr(0), z]
        elif z <= Fr(1, 2):
            exp_v, exp_y = Fr(0), [2 * z - Fr(1, 2), Fr(1, 2) - z]
        else:
            exp_v = M * (z - Fr(1, 2)) ** 2 / (M + 1)
            exp_y = [((M + 2) * z - Fr(1, 2)) / (M + 1), Fr(0)]
        assert v == exp_v, (M, z, v, exp_v)
        assert y == exp_y, (M, z, y, exp_y)
        bump("fM value/response checks")
    C, K, _ = fM_block(M)
    Bs = [[[Fr(0)], [Fr(1)]], [[Fr(2)], [Fr(-1)]], [[(M + 2) / (M + 1)], [Fr(0)]]]
    sig = []
    for B in Bs:
        BtCB = matmul(matmul(transpose(B), C), B)[0][0]
        BtK = matmul(transpose(B), K)[0][0]
        Gamma = BtCB + 2 * BtK
        assert Gamma == -BtCB
        sig.append(BtCB)
    assert sig == [2 * M, 2 * M + 8, 2 * (M + 2) ** 2 / (M + 1)]
    direct = 2 * M + 8
    curv = [direct - s for s in sig]
    assert curv == [8, 0, 2 * M / (M + 1)]
    assert max(curv) == 8
    # exact second differences inside each piece
    for (a, b, want) in [(Fr(1, 16), Fr(3, 16), 8), (Fr(5, 16), Fr(7, 16), 0),
                         (Fr(9, 16), Fr(11, 16), 2 * M / (M + 1))]:
        hstep = (b - a) / 4
        mid = (a + b) / 2
        d2 = (fM_value(M, mid + hstep)[0] - 2 * fM_value(M, mid)[0]
              + fM_value(M, mid - hstep)[0]) / hstep ** 2
        assert d2 == want, (M, d2, want)
        bump("fM piece curvature checks")
    bump("fM energy identities", 3)

# ---------------------------------------------- (2),(3) random PD blocks
def rand_int(a, b):
    return Fr(random.randint(a, b))


def value_and_pattern(C, K, c, l, u, v):
    g = [c[i] + sum(K[i][j] * v[j] for j in range(len(v))) for i in range(len(c))]
    return box_qp_pd(C, g, l, u)


def affine_map(C, K, c, l, u, pat):
    """Affine response y = a + B v for a lower/free/upper pattern."""
    r, k = len(C), len(K[0])
    F = [i for i in range(r) if pat[i] == "F"]
    X = [i for i in range(r) if pat[i] != "F"]
    B = [[Fr(0)] * k for _ in range(r)]
    if F:
        CFF = [[C[i][j] for j in F] for i in F]
        inv = inverse(CFF)
        KF = [[K[i][j] for j in range(k)] for i in F]
        BF = matmul(inv, KF)
        for a_, i in enumerate(F):
            for j in range(k):
                B[i][j] = -BF[a_][j]
    return B, F


for trial in range(300):
    r, k = 3, 2
    R = [[rand_int(-2, 2) for _ in range(r)] for _ in range(r)]
    C = matmul(transpose(R), R)
    for i in range(r):
        C[i][i] += 1          # positive definite
    K = [[rand_int(-4, 4) for _ in range(k)] for _ in range(r)]
    c = [rand_int(-3, 3) for _ in range(r)]
    l = [Fr(0)] * r
    u = [Fr(random.randint(1, 2)) for _ in range(r)]
    v0 = [Fr(random.randint(1, 99), 100) for _ in range(k)]
    val0, y0, pat = value_and_pattern(C, K, c, l, u, v0)
    B, F = affine_map(C, K, c, l, u, pat)
    BtCB = matmul(matmul(transpose(B), C), B)
    BtK = matmul(transpose(B), K)
    Gamma = [[BtCB[i][j] + BtK[i][j] + BtK[j][i] for j in range(k)] for i in range(k)]
    assert Gamma == [[-x for x in row] for row in BtCB]
    bump("Gamma=-B'CB identities")
    for j in range(k):
        # least extension energy over free coordinates
        if F:
            CFF = [[C[a][b] for b in F] for a in F]
            KFj = [K[a][j] for a in F]
            col = matmul(inverse(CFF), [[x] for x in KFj])
            w = [-row[0] for row in col]
            energy = sum(w[a] * CFF[a][b] * w[b] for a in range(len(F)) for b in range(len(F))) \
                + 2 * sum(w[a] * KFj[a] for a in range(len(F)))
        else:
            energy = Fr(0)
        assert energy == Gamma[j][j]
        bump("energy formula checks")
        # second difference inside the region (small step, same pattern)
        hstep = Fr(1, 10 ** 6)
        vp = list(v0); vp[j] += hstep
        vm = list(v0); vm[j] -= hstep
        fp, _, pp = value_and_pattern(C, K, c, l, u, vp)
        fm, _, pm = value_and_pattern(C, K, c, l, u, vm)
        if pp == pat and pm == pat:
            d2 = (fp - 2 * val0 + fm) / hstep ** 2
            assert d2 == Gamma[j][j]
            bump("value second-difference = Gamma_jj")
    # (3) concavity along a coordinate line across pieces
    j = random.randrange(k)
    pts = [Fr(i, 200) for i in range(201)]
    vals, gams = [], []
    for t in pts:
        v = list(v0); v[j] = t
        val, _, pt = value_and_pattern(C, K, c, l, u, v)
        Bt, _ = affine_map(C, K, c, l, u, pt)
        g = -matmul(matmul(transpose(Bt), C), Bt)[j][j]
        vals.append(val)
        gams.append(g)
    ell = max(gams)
    assert ell <= 0
    for i in range(1, 200):
        t0, t1, t2 = pts[i - 1], pts[i], pts[i + 1]
        g0 = vals[i - 1] - ell * t0 * t0 / 2
        g1 = vals[i] - ell * t1 * t1 / 2
        g2 = vals[i + 1] - ell * t2 * t2 / 2
        assert g0 - 2 * g1 + g2 <= 0
        bump("concavity second differences across pieces")
    if len(set(gams)) > 1:
        bump("lines crossing pieces with different curvature")

# ---------------------------------------------- (4) three-piece ladder
z, y1, y2, M = sp.symbols("z y1 y2 M")
a = sp.Rational(1, 5)
t, u_, w = z - a, y1, y2 - a
rr, ss = u_ + w - t, u_ - 2 * t
lhs = z ** 2 + M * (y1 + y2 - z) ** 2 + (y1 - 2 * z + sp.Rational(1, 2)) ** 2 - sp.Rational(1, 20)
rhs = t ** 2 + M * rr ** 2 + ss ** 2 + u_ / 5
assert sp.expand(lhs - rhs) == 0
bump("ladder identity (10) symbolic")


def ladder_F(m, Mv, zz, vv, Y1, Y2):
    eta = Fr(1, 16)
    tot = Fr(0)
    for i in range(m):
        tot += zz[i] ** 2 + Mv * (Y1[i] + Y2[i] - zz[i]) ** 2 + (Y1[i] - 2 * zz[i] + Fr(1, 2)) ** 2 \
            - vv[i] ** 2 + 3 * vv[i] - (zz[i] - Fr(1, 5)) * vv[i]
    for i in range(m - 1):
        tot += eta * ((zz[i + 1] - zz[i]) ** 2 + (vv[i + 1] - vv[i]) ** 2)
    return tot


for m in [1, 2, 3, 5]:
    for Mv in [Fr(1), Fr(10), Fr(1000)]:
        opt = ladder_F(m, Mv, [Fr(1, 5)] * m, [Fr(0)] * m, [Fr(0)] * m, [Fr(1, 5)] * m)
        assert opt == Fr(m, 20)
        for _ in range(150):
            zz = [Fr(random.randint(0, 300), 400) for _ in range(m)]
            vv = [Fr(random.randint(0, 400), 400) for _ in range(m)]
            Y1 = [Fr(random.randint(0, 400), 400) for _ in range(m)]
            Y2 = [Fr(random.randint(0, 400), 400) for _ in range(m)]
            if random.random() < 0.5:   # points near the optimizer
                zz = [Fr(1, 5) + Fr(random.randint(-20, 20), 400) for _ in range(m)]
                vv = [Fr(random.randint(0, 20), 400) for _ in range(m)]
                Y1 = [Fr(random.randint(0, 20), 400) for _ in range(m)]
                Y2 = [Fr(1, 5) + Fr(random.randint(-20, 20), 400) for _ in range(m)]
            gap = ladder_F(m, Mv, zz, vv, Y1, Y2) - opt
            dist2 = sum((zz[i] - Fr(1, 5)) ** 2 + vv[i] ** 2 + Y1[i] ** 2 + (Y2[i] - Fr(1, 5)) ** 2
                        for i in range(m))
            assert gap >= dist2 / 12, (m, Mv, gap, dist2)
            bump("ladder growth 1/12 checks")

for k_, v_ in counts.items():
    print(f"{k_}: {v_}")
print("all value-factor checks passed")
