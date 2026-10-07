"""Review r2: independent check of the bracket z_A/z_K in [763/25000, 191/6250] for the sfree note's near-boundary
adversarial instance (adversarial_ratio_8_margin.log, restart 3), note Section 6.1.

Does not import the stream's code or the sfree code.  The instance is rebuilt from theta with the sfree
parametrization (t0 = (x0, y0, x0 y0), d = (1, -e^g, y0 - x0 e^g), v1 = t0 + e^a d, v2 = t0 - e^b d,
sbar = t0 + s, v3 = t0 + r, rays v_j - sbar, unit costs), in numpy floats; the floats are then taken as exact.

Unlike the stream's scripts, the scaled rays are not rounded: with unit costs p~_j = Z p_j, where Z is the
exact corner bound of the float data (computed here by face enumeration in 60-digit arithmetic).  Since
T_R(p~) = T_{RZ}(p):
  upper end: a dual certificate showing that no orbit set with sbar in its interior contains T_{R_u}(p), with a
             rational R_u <= (191/6250) Z, proves z_A/z_K <= 191/6250;
  lower end: an explicit rational F with sbar in int C_F and C_F containing T_{R_l}(p), with a rational
             R_l >= (763/25000) Z, proves z_A/z_K >= 763/25000.
Dual: symmetric Y_0 > 0, Y_1, Y_2, Y_3 >= 0 with sum_j M(v_j) Y_j = 0 (v_0 = sbar).  Then for any X with
sym(X M(sbar)) > 0: 0 = sum_j <sym(X M(v_j)), Y_j>, so some sym(X M(v_j)) is not PSD.
Symmetry of Y_0 := -M(sbar)^{-1} sum_{j>=1} M(v_j) Y_j is enforced by an exact correction of the (2,2) entry of
Y_3 (the stream rescales Y_1 instead).
"""
import json
import sys
from fractions import Fraction as Fr
import mpmath as mp
import numpy as np
import cvxpy as cp

mp.mp.dps = 60
LOG = '../../../../research-20260928b/sfree/logs/adversarial_ratio_8_margin.log'
rec = [json.loads(l) for l in open(LOG) if l.startswith('{')]
rec = [r for r in rec if r['restart'] == 3][0]
th = np.array(rec['theta'])
x0, y0, g, a, bb = th[:5]
s, r = th[5:8], th[8:11]
t0 = np.array([x0, y0, x0 * y0])
e = np.exp(g)
d = np.array([1.0, -e, y0 - x0 * e])
v1 = t0 + np.exp(a) * d
v2 = t0 - np.exp(bb) * d
sbar = t0 + s
v3 = t0 + r
P = np.stack([v1 - sbar, v2 - sbar, v3 - sbar], 1)

sb = [Fr(float(v)) for v in sbar]
Pq = [[Fr(float(P[i, j])) for i in range(3)] for j in range(3)]   # Pq[j] = ray j


def q(pt):
    return pt[2] - pt[0] * pt[1]


qbar = q(sb)
print('instance: q(sbar) = %.6e (exact from floats)' % float(qbar))

# ---------- exact-ish z_K of the float data: smallest c with min_{lambda in c*simplex} q(sbar + P lambda) <= 0
mf = lambda f: mp.mpf(f.numerator) / f.denominator
S = [mf(v) for v in sb]
PP = [[mf(v) for v in Pq[j]] for j in range(3)]


def qmp(lam):
    pt = [S[i] + sum(lam[j] * PP[j][i] for j in range(3)) for i in range(3)]
    return pt[2] - pt[0] * pt[1]


def gmin(c):
    best = min(qmp([c if j == k else 0 for j in range(3)]) for k in range(3))
    for i in range(3):
        for k in range(i + 1, 3):
            # lambda = (c - t) e_i + t e_k: quadratic in t
            f0 = qmp([c if j == i else 0 for j in range(3)])
            def f(t):
                lam = [0, 0, 0]
                lam[i] = c - t
                lam[k] = t
                return qmp(lam)
            fm = f(c / 2)
            fc = f(c)
            A2 = 2 * (fc - 2 * fm + f0) / c ** 2
            A1 = (fc - f0) / c - A2 * c
            if A2 > 0:
                ts = -A1 / (2 * A2)
                if 0 < ts < c:
                    best = min(best, f(ts))
    # interior of the 2-simplex: lambda = (c - u - v, u, v); stationary point of the quadratic in (u, v)
    def F(u, v):
        return qmp([c - u - v, u, v])
    h = c / 4
    F0 = F(h, h)
    Fu = (F(h + h / 2, h) - F(h - h / 2, h)) / h
    Fv = (F(h, h + h / 2) - F(h, h - h / 2)) / h
    Fuu = (F(h + h / 2, h) - 2 * F0 + F(h - h / 2, h)) / (h / 2) ** 2
    Fvv = (F(h, h + h / 2) - 2 * F0 + F(h, h - h / 2)) / (h / 2) ** 2
    Fuv = (F(h + h / 2, h + h / 2) - F(h + h / 2, h - h / 2) - F(h - h / 2, h + h / 2) + F(h - h / 2, h - h / 2)) / h ** 2
    det = Fuu * Fvv - Fuv ** 2
    if Fuu > 0 and det > 0:
        du = -(Fvv * Fu - Fuv * Fv) / det
        dv = -(Fuu * Fv - Fuv * Fu) / det
        u, v = h + du, h + dv
        if u > 0 and v > 0 and u + v < c:
            best = min(best, F(u, v))
    return best


cs = [mp.mpf(k) / 200 for k in range(1, 241)]
prev = mp.mpf(0)
for cc in cs:
    if gmin(cc) <= 0:
        lo, hi = prev, cc
        break
    prev = cc
for _ in range(190):
    m = (lo + hi) / 2
    if gmin(m) <= 0:
        hi = m
    else:
        lo = m
Z = hi
print('exact corner bound of the float data: Z = 1 + %s' % mp.nstr(Z - 1, 6))

R_up_note, R_lo_note = Fr(191, 6250), Fr(763, 25000)
# rational R_u <= R_up_note * Z and R_l >= R_lo_note * Z (Z is known to ~50 digits; use a 1e-30 safety gap)
R_u = Fr(int(mp.floor((mf(R_up_note) * Z - mp.mpf(10) ** -30) * 10 ** 40)), 10 ** 40)
R_l = Fr(int(mp.ceil((mf(R_lo_note) * Z + mp.mpf(10) ** -30) * 10 ** 40)), 10 ** 40)
print('R_u = %.15f (<= 191/6250 * Z), R_l = %.15f (>= 763/25000 * Z)' % (float(R_u), float(R_l)))


def Mq(pt):
    return [[pt[2], pt[0]], [pt[1], Fr(1)]]


def mul(A, B):
    return [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]


def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]


def verts(R):
    return [sb] + [[sb[i] + R * Pq[j][i] for i in range(3)] for j in range(3)]


# normalized frame (alpha = beta = 1/sqrt(qbar)): M(phi(s)) = A M(s) B^T
al = 1.0 / np.sqrt(float(qbar))
Af = np.array([[al, -al * float(sb[0])], [0.0, 1.0]])
Bf = np.array([[al, -al * float(sb[1])], [0.0, 1.0]])
Mf = lambda pt: np.array([[float(pt[2]), float(pt[0])], [float(pt[1]), 1.0]])

ok_all = True

# ---------- upper end: dual certificate at R_u
V = verts(R_u)
Mn = [Af @ Mf(v) @ Bf.T for v in V]
Ys = [cp.Variable((2, 2), symmetric=True) for _ in range(4)]
t = cp.Variable()
cons = [sum(Mn[j] @ Ys[j] for j in range(4)) == 0, sum(cp.trace(Y) for Y in Ys) == 1]
cons += [Y >> t * np.eye(2) for Y in Ys]
cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
print('upper end: normalized dual margin t = %.3e' % t.value)
Yo = [Bf.T @ Y.value @ Bf for Y in Ys]
Yq = [None] + [[[Fr(float(Yo[j][0, 0])), Fr(float(0.5 * (Yo[j][0, 1] + Yo[j][1, 0])))],
                [Fr(float(0.5 * (Yo[j][0, 1] + Yo[j][1, 0]))), Fr(float(Yo[j][1, 1]))]] for j in range(1, 4)]
M0 = Mq(V[0])
det0 = M0[0][0] * M0[1][1] - M0[0][1] * M0[1][0]
M0inv = [[M0[1][1] / det0, -M0[0][1] / det0], [-M0[1][0] / det0, M0[0][0] / det0]]


def Y0_of(Y3corr):
    Ysum = [[Fr(0)] * 2 for _ in range(2)]
    for j in range(1, 4):
        Yj = Yq[j] if j < 3 else add(Yq[3], [[Fr(0), Fr(0)], [Fr(0), Y3corr]])
        Ysum = add(Ysum, mul(Mq(V[j]), Yj))
    Y0 = mul(M0inv, Ysum)
    return [[-v for v in row] for row in Y0]


asym = lambda Y: Y[0][1] - Y[1][0]
s0, s1 = asym(Y0_of(Fr(0))), asym(Y0_of(Fr(1)))
corr = -s0 / (s1 - s0)
Yq[3] = add(Yq[3], [[Fr(0), Fr(0)], [Fr(0), corr]])
Yq[0] = Y0_of(Fr(0))
res = [[Fr(0)] * 2 for _ in range(2)]
for j in range(4):
    res = add(res, mul(Mq(V[j]), Yq[j]))
pdm = lambda Y: Y[0][1] == Y[1][0] and Y[0][0] > 0 and Y[0][0] * Y[1][1] - Y[0][1] ** 2 > 0
psdm = lambda Y: Y[0][1] == Y[1][0] and Y[0][0] >= 0 and Y[1][1] >= 0 and Y[0][0] * Y[1][1] - Y[0][1] ** 2 >= 0
c1 = all(v == 0 for row in res for v in row)
c2 = pdm(Yq[0])
c3 = all(psdm(Yq[j]) for j in range(1, 4))
print('  correction of Y_3[2,2] relative to its size: %.2e' % float(corr / Yq[3][1][1]))
print('  sum_j M(v_j) Y_j = 0 exactly: %s; Y_0 PD: %s; Y_1..Y_3 PSD: %s' % (c1, c2, c3))
ok_all &= c1 and c2 and c3

# ---------- lower end: explicit orbit set at R_l
V = verts(R_l)
Mn = [Af @ Mf(v) @ Bf.T for v in V]
X = cp.Variable((2, 2))
t = cp.Variable()
cons = [cp.abs(X) <= 1]
for j in range(4):
    Sj = X @ Mn[j]
    cons.append(0.5 * (Sj + Sj.T) >> t * np.eye(2))
cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
print('lower end: normalized primal margin t = %.3e' % t.value)
# map back: sym(X A M B^T) >= 0 iff sym(B^{-1} X A M) >= 0, so F^T = B^{-1} X A
FT = np.linalg.solve(Bf, X.value @ Af)
FTq = [[Fr(float(FT[i, j])) for j in range(2)] for i in range(2)]


def symFM(pt):
    A_ = mul(FTq, Mq(pt))
    return [[A_[0][0], (A_[0][1] + A_[1][0]) / 2], [(A_[0][1] + A_[1][0]) / 2, A_[1][1]]]


d1 = pdm(symFM(V[0]))
d2 = all(psdm(symFM(V[j])) for j in range(1, 4))
d3 = FTq[0][0] * FTq[1][1] - FTq[0][1] * FTq[1][0] > 0
print('  sym(F^T M(sbar)) PD: %s; sym(F^T M(v_j)) PSD for the other three vertices: %s; det F > 0: %s' % (d1, d2, d3))
ok_all &= d1 and d2 and d3
if ok_all:
    print('conclusion: 763/25000 <= z_A/z_K <= 191/6250 for the float instance with its exact corner bound Z')
print('ALL PASS' if ok_all else 'SOME FAIL')
