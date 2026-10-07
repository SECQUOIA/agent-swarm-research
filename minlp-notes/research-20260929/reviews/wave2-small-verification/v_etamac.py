"""etamac: independent check of the convex-relaxation certificate.

1. Structure: every row, bound and the objective are matched against templates
   built from an explicit role map (K, KN, Y, YN, L, LN, E, EN, C, I, EC).
2. Exponent facts in exact rationals: p1 q < 1; s = (p2+p3) q > 1 (so the
   Cobb-Douglas part LN^{p2 q} EN^{p3 q} is NOT concave with the file's decimals).
3. Box for etamac-feasible points, derived from etamac's own rows (not from the
   relaxation), with outward-rounded iv arithmetic.
4. Majorant: w = LN^{p2/(p2+p3)} EN^{p3/(p2+p3)} (degree 1, concave),
   v = w^s <= kappa w for w <= W, kappa >= W^{s-1};
   CES~ = (a KN^-p1 + b kappa^{-1/q} LN^{-p2/s} EN^{-p3/s})^{-q} >= CES on the box,
   concave on the positive orthant.
5. Relaxation R: YN_t <= CES~_t, Y_1 - CES~_1 <= 3.4653339648, plus all linear
   rows and e70.  Own KKT solve (scipy SLSQP start, then 50-digit Newton).
6. Rigorous bound: l = f + nu.h + mu.g (mu >= 0) is convex on the box, so
   min l >= l(xh) + sum_j min_{x_j in box} dl/dx_j(xh) (x_j - xh_j)  (iv, 40 digits).
7. Own exactly feasible etamac point by forward construction (real-number
   recursion from decimal choices of I_1..I_8, LN_t, EN_t, with I_9 := 0.07 K_9),
   objective enclosed with iv.
"""
import json
import os
from fractions import Fraction

import mpmath
import numpy as np
import sympy as sp
from mpmath import iv
from scipy.optimize import minimize

import common
import ivgen

m = common.load("etamac")
N = len(m["names"])
cons = m["cons"]
out = {}
T = range(1, 10)

# ---------------- 1. role map and templates ----------------
K = {t: t - 1 for t in T}
KN = {t: 7 + t for t in range(2, 10)}
Y = {t: 16 + t for t in T}
YN = {t: 24 + t for t in range(2, 10)}
L = {t: 33 + t for t in T}
LN = {t: 42 + t for t in T}
E = {t: 51 + t for t in T}
EN = {t: 60 + t for t in T}
C = {t: 69 + t for t in T}
I = {t: 78 + t for t in T}
EC = {t: 87 + t for t in T}
allv = sorted(set().union(*[set(d.values()) for d in (K, KN, Y, YN, L, LN, E, EN, C, I, EC)]))
assert allv == list(range(N))
P1, P2, P3, Q, B = "-.342222222222222", "-.427777777777778", "-.794444444444445", "-.818181818181818", ".306708090151268"
g = "4.91287681"
dec = ".8153726976"


def pw(v, e):
    return ("power", ("var", v, "1"), ("num", e))


a_t, cL, cE = {}, {}, {}
rows = {c["name"]: c for c in cons}
for t in range(2, 10):
    r = rows["e%d" % (t - 1)]
    assert r["lin"] == {KN[t]: "1", I[t - 1]: "-" + g} and r["nl"] is None and r["lb"] == r["ub"] == "0"
    r = rows["e%d" % (t + 7)]
    assert r["lin"] == {YN[t]: "1"} and r["lb"] == r["ub"] == "0"
    a_t[t] = r["nl"][1][1][1][2][1]
    tmpl = ("negate", ("power", ("sum", ("product", pw(KN[t], P1), ("num", a_t[t])),
                                 ("product", pw(LN[t], P2), ("num", B), pw(EN[t], P3))), ("num", Q)))
    assert r["nl"] == tmpl, t
    assert Fraction(a_t[t]) > 0
r = rows["e17"]; assert r["lin"] == {L[1]: "-1", LN[1]: "1"} and r["lb"] == r["ub"] == "-2.038431744"
r = rows["e26"]; assert r["lin"] == {E[1]: "-1", EN[1]: "1"} and r["lb"] == r["ub"] == "-40.76863488"
for t in range(2, 10):
    assert rows["e%d" % (16 + t)]["lin"] == {L[t - 1]: dec, L[t]: "-1", LN[t]: "1"}
    assert rows["e%d" % (25 + t)]["lin"] == {E[t - 1]: dec, E[t]: "-1", EN[t]: "1"}
    assert rows["e%d" % (33 + t)]["lin"] == {K[t - 1]: "-" + dec, K[t]: "1", KN[t]: "-1"}
    assert rows["e%d" % (42 + t)]["lin"] == {Y[t - 1]: "-" + dec, Y[t]: "1", YN[t]: "-1"}
    for nm in ("e%d" % (16 + t), "e%d" % (25 + t), "e%d" % (33 + t), "e%d" % (42 + t)):
        assert rows[nm]["lb"] == rows[nm]["ub"] == "0" and rows[nm]["nl"] is None
r = rows["e43"]
C0 = ".612508399277048"
assert r["lin"] == {Y[1]: "1"} and r["lb"] == r["ub"] == "3.4653339648"
assert r["nl"] == ("negate", ("power", ("sum", ("product", pw(LN[1], P2), ("num", B), pw(EN[1], P3)), ("num", C0)), ("num", Q)))
for t in T:
    r = rows["e%d" % (51 + t)]
    ks = r["lin"]
    assert set(ks) == {L[t], E[t], EC[t]} and ks[EC[t]] == "1e3" and r["lb"] == r["ub"] == "0" and r["nl"] is None
    cL[t], cE[t] = ks[L[t]][1:], ks[E[t]][1:]
    assert ks[L[t]][0] == "-" and ks[E[t]][0] == "-"
    r = rows["e%d" % (60 + t)]
    assert r["lin"] == {Y[t]: "1", C[t]: "-1", I[t]: "-1", EC[t]: "-1"} and r["lb"] == r["ub"] == "0" and r["nl"] is None
r = rows["e70"]
assert r["lin"] == {K[9]: "7e-2", I[9]: "-1"} and r["lb"] == "-INF" and r["ub"] == "0" and r["nl"] is None
assert len(rows) == 70 and all(c["constant"] == "0" and not c["quad"] for c in cons)
o = m["obj"]
assert o["lin"] == {} and o["constant"] == "0" and not o["quad"] and o["nl"][0] == "negate"
beta = {}
for t, term in zip(T, o["nl"][1][1:]):
    assert term[0] == "product" and term[1] == ("ln", ("var", C[t], "1"))
    beta[t] = term[2][1]
    assert Fraction(beta[t]) > 0
assert len(o["nl"][1]) == 10
# bounds
assert m["lb"][K[1]] == m["ub"][K[1]] == "12.32657617084"
for j in range(N):
    if j in EC.values():
        assert (m["lb"][j], m["ub"][j]) == ("-INF", "INF")
    elif j != K[1]:
        assert m["ub"][j] == "INF" and Fraction(m["lb"][j]) > 0
out["structure"] = "70 rows, 97 bounds and objective match templates; beta_t > 0, a_t > 0, cL,cE > 0"

# ---------------- 2. exponents ----------------
p1, p2, p3, q = (-Fraction(P1), -Fraction(P2), -Fraction(P3), -Fraction(Q))
s = (p2 + p3) * q
out["exponents"] = dict(p1q=str(float(p1 * q)), s_minus_1=str(float(s - 1)), s_exact=str(s))
assert p1 * q < 1 and s > 1
print("s - 1 =", float(s - 1), " p1*q =", float(p1 * q))

# ---------------- 3. box for etamac-feasible points ----------------
iv.dps = 40
mpmath.mp.prec = 400  # endpoint copies below are exact (iv works at ~136 bits)
ivf = lambda x: iv.mpf(x)
lbv = {j: (ivf(m["lb"][j]) if m["lb"][j] != "-INF" else None) for j in range(N)}
ub = {}
dI = ivf(dec)
EClb = {t: (ivf(cL[t]) * lbv[L[t]] + ivf(cE[t]) * lbv[E[t]]) / 1000 for t in T}
Yub = {1: ivf("3.4653339648") + iv.exp(-ivf(Q.lstrip("-")) * iv.log(ivf(C0)))}
KNub, YNub, Iub = {}, {}, {}
for t in range(1, 9):
    Iub[t] = Yub[t] - lbv[C[t]] - EClb[t]
    KNub[t + 1] = ivf(g) * Iub[t]
    # YN = (a KN^-p1 + positive)^-q <= a^-q KN^(p1 q) <= a^-q KNub^(p1 q)
    qI = iv.mpf(q.numerator) / q.denominator
    p1I = iv.mpf(p1.numerator) / p1.denominator
    YNub[t + 1] = iv.exp(-qI * iv.log(ivf(a_t[t + 1]))) * iv.exp(p1I * qI * iv.log(KNub[t + 1]))
    Yub[t + 1] = dI * Yub[t] + YNub[t + 1]
Iub[9] = Yub[9] - lbv[C[9]] - EClb[9]
up = lambda x: mpmath.mpf(x.b)
for t in T:
    ub[Y[t]] = up(Yub[t]); ub[I[t]] = up(Iub[t])
    ub[C[t]] = up(Yub[t] - lbv[I[t]] - EClb[t])
    ECub = Yub[t] - lbv[C[t]] - lbv[I[t]]
    ub[EC[t]] = up(ECub)
    ub[L[t]] = up((1000 * ECub - ivf(cE[t]) * lbv[E[t]]) / ivf(cL[t]))
    ub[E[t]] = up((1000 * ECub - ivf(cL[t]) * lbv[L[t]]) / ivf(cE[t]))
for t in range(2, 10):
    ub[KN[t]] = up(KNub[t]); ub[YN[t]] = up(YNub[t])
ub[LN[1]] = up(ivf(ub[L[1]]) - ivf("2.038431744"))
ub[EN[1]] = up(ivf(ub[E[1]]) - ivf("40.76863488"))
for t in range(2, 10):
    ub[LN[t]] = up(ivf(ub[L[t]]) - dI * lbv[L[t - 1]])
    ub[EN[t]] = up(ivf(ub[E[t]]) - dI * lbv[E[t - 1]])
ub[K[1]] = mpmath.mpf(ivf("12.32657617084").b)
Kub = ivf("12.32657617084")
for t in range(2, 10):
    Kub = dI * Kub + ivf(ub[KN[t]])
    ub[K[t]] = up(Kub)
lo = {}
for j in range(N):
    if j in EC.values():
        t = [tt for tt in T if EC[tt] == j][0]
        lo[j] = mpmath.mpf(EClb[t].a)
    else:
        lo[j] = mpmath.mpf(lbv[j].a)
    assert lo[j] <= ub[j], (j, lo[j], ub[j])
out["box"] = dict(max_ub=float(max(ub.values())), argmax=m["names"][max(ub, key=ub.get)], Y9_ub=float(ub[Y[9]]),
                  Y1_ub=float(ub[Y[1]]))
print("box:", out["box"])

# ---------------- 4. majorant ----------------
alpha = p2 / (p2 + p3)
Wt = []
for t in T:
    Wt.append(iv.exp((iv.mpf(alpha.numerator) / alpha.denominator) * iv.log(ivf(ub[LN[t]]))
                     + (1 - iv.mpf(alpha.numerator) / alpha.denominator) * iv.log(ivf(ub[EN[t]]))))
W = max(mpmath.mpf(w.b) for w in Wt)
sI = iv.mpf(s.numerator) / s.denominator
kap_needed = iv.exp((sI - 1) * iv.log(iv.mpf(W)))
KAPPA = "1.000000000000004"
assert kap_needed.b <= iv.mpf(KAPPA).a, (kap_needed, KAPPA)
out["majorant"] = dict(W=float(W), W_pow_s_minus_1_upper=mpmath.nstr(kap_needed.b, 20), kappa=KAPPA)
print("majorant:", out["majorant"])

# ---------------- 5. sympy model of R and KKT ----------------
X = sp.symbols("x0:%d" % N, positive=True)
bsym = sp.Symbol("bt", positive=True)  # b * kappa^{-1/q}
Rr = sp.Rational
fS = -sum(Rr(beta[t]) * sp.log(X[C[t]]) for t in T)
hS, hname = [], []
for c in cons:
    if c["nl"] is None and c["lb"] == c["ub"]:
        hS.append(sum(Rr(v) * X[j] for j, v in c["lin"].items()) - Rr(c["lb"])); hname.append(c["name"])
assert len(hS) == 60
p2s, p3s = p2 / s, p3 / s


def cesT(t):
    return (Rr(a_t[t]) * X[KN[t]] ** (-Rr(p1)) + bsym * X[LN[t]] ** (-Rr(p2s)) * X[EN[t]] ** (-Rr(p3s))) ** (-Rr(q))


gS = [X[YN[t]] - cesT(t) for t in range(2, 10)]
gS.append(X[Y[1]] - (bsym * X[LN[1]] ** (-Rr(p2s)) * X[EN[1]] ** (-Rr(p3s)) + Rr(C0)) ** (-Rr(q)) - Rr("3.4653339648"))
gS.append(Rr("7e-2") * X[K[9]] - X[I[9]])
nu = sp.symbols("nu0:60"); mu = sp.symbols("mu0:10")
lag = fS + sum(nu[i] * hS[i] for i in range(60)) + sum(mu[i] * gS[i] for i in range(10))
free = [j for j in range(N) if j != K[1]]
grad = [sp.diff(lag, X[j]) for j in free]

# float start: solve etamac itself with SLSQP from MINLPLib p1
sol = common.read_sol(os.path.join(common.HERE, "sol", "etamac.p1.sol"))
x0 = np.array([float(sol.get(nm, "0")) for nm in m["names"]])
bt_f = float(Fraction(B)) * float(Fraction(KAPPA)) ** (-1 / float(q))
fl = {k: sp.lambdify([X, bsym], e, "numpy") for k, e in (("f", fS),)}
hF = sp.lambdify([X, bsym], hS, "numpy")
gF = sp.lambdify([X, bsym], gS, "numpy")
res = minimize(lambda x: fl["f"](x, bt_f), x0, method="SLSQP",
               constraints=[dict(type="eq", fun=lambda x: np.array(hF(x, bt_f))),
                            dict(type="ineq", fun=lambda x: -np.array(gF(x, bt_f)))],
               bounds=[(float(Fraction(m["lb"][j])) if m["lb"][j] != "-INF" else None,
                        float(Fraction(m["ub"][j])) if m["ub"][j] != "INF" else None) for j in range(N)],
               options=dict(maxiter=500, ftol=1e-15))
print("SLSQP on R:", res.status, res.fun)
xs = res.x
# multipliers by least squares at the float point (all 10 inequalities assumed active)
mpmath.mp.dps = 50
KKT = grad + hS + gS
unk = [X[j] for j in free] + list(nu) + list(mu)
Jm = sp.Matrix(KKT).jacobian(unk)
kF = sp.lambdify([unk, X[K[1]], bsym], KKT, "mpmath")
jF = sp.lambdify([unk, X[K[1]], bsym], Jm, "mpmath")
# initial multipliers from linear least squares on grad = 0
gradlin = sp.lambdify([X, bsym], [[sp.diff(gr, v) for v in list(nu) + list(mu)] for gr in grad], "numpy")
g0 = sp.lambdify([X, bsym, list(nu) + list(mu)], grad, "numpy")
Amat = np.array(gradlin(xs, bt_f), dtype=float)
rhs = -np.array(g0(xs, bt_f, [0.0] * 70), dtype=float)
lam0, *_ = np.linalg.lstsq(Amat, rhs, rcond=None)
z = [mpmath.mpf(float(xs[j])) for j in free] + [mpmath.mpf(float(v)) for v in lam0]
K1 = mpmath.mpf("12.32657617084")
btm = mpmath.mpf(Fraction(B).numerator) / Fraction(B).denominator * mpmath.mpf(KAPPA) ** (-1 / (mpmath.mpf(q.numerator) / q.denominator))
for it in range(40):
    Fv = mpmath.matrix(kF(z, K1, btm))
    nr = max(abs(v) for v in Fv)
    if nr < mpmath.mpf(10) ** -45:
        break
    Jv = mpmath.matrix(jF(z, K1, btm))
    dz = mpmath.lu_solve(Jv, -Fv)
    z = [z[k] + dz[k] for k in range(len(z))]
print("KKT Newton iterations", it, "residual", mpmath.nstr(nr, 3))
xk = [None] * N
xk[K[1]] = K1
for k, j in enumerate(free):
    xk[j] = z[k]
nuv = z[len(free):len(free) + 60]
muv = z[len(free) + 60:]
out["kkt"] = dict(residual=mpmath.nstr(nr, 3), min_mu=mpmath.nstr(min(muv), 6), mu70=mpmath.nstr(muv[-1], 6),
                  f=mpmath.nstr(-sum(mpmath.mpf(beta[t]) * mpmath.log(xk[C[t]]) for t in T), 25),
                  min_rel_dist_to_lb=mpmath.nstr(min((xk[j] - lo[j]) for j in free if j not in EC.values()), 6))
print("kkt:", out["kkt"])
assert min(muv) > 0

# ---------------- 6. rigorous bound ----------------
iv.dps = 40
xh = [mpmath.nstr(v, 30) for v in xk]
nuh = [mpmath.nstr(v, 30) for v in nuv]
muh = [mpmath.nstr(v, 30) for v in muv]
assert all(mpmath.mpf(v) > 0 for v in muh)
assert xh[K[1]] == "12.32657617084"
for j in range(N):
    if j != K[1]:
        assert lo[j] <= mpmath.mpf(iv.mpf(xh[j]).a) and mpmath.mpf(iv.mpf(xh[j]).b) <= ub[j], j
Lsub = lag.subs({nu[i]: Rr(nuh[i]) for i in range(60)}).subs({mu[i]: Rr(muh[i]) for i in range(10)})
gradsub = [sp.diff(Lsub, X[j]) for j in range(N)]
fac_l = ivgen.compile_exprs(list(X) + [bsym], [Lsub], "LAG")
fac_g = ivgen.compile_exprs(list(X) + [bsym], gradsub, "GRD")
lagI, grdI = fac_l(), fac_g()
btI = iv.mpf(Fraction(B).numerator) / Fraction(B).denominator * iv.exp(-(iv.mpf(q.denominator) / q.numerator) * iv.log(iv.mpf(KAPPA)))
xI = [iv.mpf(v) for v in xh]
(lval,) = lagI(*xI, btI)
gv = grdI(*xI, btI)
bound = lval
maxg = 0
for j in range(N):
    d = iv.mpf([lo[j], ub[j]]) - xI[j]
    if j == K[1]:
        d = iv.mpf(0)  # fixed variable: zero-width range
    bound = bound + gv[j] * d
    if j != K[1]:
        maxg = max(maxg, abs(mpmath.mpf(gv[j].a)), abs(mpmath.mpf(gv[j].b)))
out["bound"] = dict(l_at_xh=[mpmath.nstr(lval.a, 20), mpmath.nstr(lval.b, 20)],
                    dual_bound=mpmath.nstr(mpmath.mpf(bound.a), 20), max_abs_grad_free=mpmath.nstr(maxg, 3),
                    dl_dK1=mpmath.nstr(gv[K[1]].a, 4))
print("bound:", out["bound"])

# ---------------- 7. own exactly feasible etamac point ----------------
# decisions (decimals): I_1..I_8, LN_1..9, EN_1..9 from the KKT point; the rest follow exactly.
dI_ = {t: iv.mpf(mpmath.nstr(xk[I[t]], 25)) for t in range(1, 9)}
dLN = {t: iv.mpf(mpmath.nstr(xk[LN[t]], 25)) for t in T}
dEN = {t: iv.mpf(mpmath.nstr(xk[EN[t]], 25)) for t in T}


def ces_orig(t, kn, ln, en):
    z = iv.mpf(B) * iv.exp(ivf(P2) * iv.log(ln)) * iv.exp(ivf(P3) * iv.log(en))
    if t == 1:
        z = z + ivf(C0)
    else:
        z = z + ivf(a_t[t]) * iv.exp(ivf(P1) * iv.log(kn))
    return iv.exp(ivf(Q) * iv.log(z))


xv = {}
xv[K[1]] = ivf("12.32657617084")
Lv = dLN[1] + ivf("2.038431744"); Ev = dEN[1] + ivf("40.76863488")
xv[L[1]], xv[E[1]], xv[LN[1]], xv[EN[1]] = Lv, Ev, dLN[1], dEN[1]
xv[Y[1]] = ivf("3.4653339648") + ces_orig(1, None, dLN[1], dEN[1])
for t in range(2, 10):
    xv[KN[t]] = ivf(g) * dI_[t - 1]
    xv[K[t]] = dI * xv[K[t - 1]] + xv[KN[t]]
    xv[LN[t]], xv[EN[t]] = dLN[t], dEN[t]
    xv[L[t]] = dI * xv[L[t - 1]] + dLN[t]
    xv[E[t]] = dI * xv[E[t - 1]] + dEN[t]
    xv[YN[t]] = ces_orig(t, xv[KN[t]], dLN[t], dEN[t])
    xv[Y[t]] = dI * xv[Y[t - 1]] + xv[YN[t]]
for t in range(1, 9):
    xv[I[t]] = dI_[t]
xv[I[9]] = ivf("7e-2") * xv[K[9]]  # e70 active, holds with equality
for t in T:
    xv[EC[t]] = (ivf(cL[t]) * xv[L[t]] + ivf(cE[t]) * xv[E[t]]) / 1000
    xv[C[t]] = xv[Y[t]] - xv[I[t]] - xv[EC[t]]
minmargin = min(mpmath.mpf((xv[j] - ivf(m["lb"][j])).a) for j in range(N) if m["lb"][j] != "-INF" and j != K[1])
assert minmargin > 0
fP = -sum(ivf(beta[t]) * iv.log(xv[C[t]]) for t in T)
out["own_primal"] = dict(objective=[mpmath.nstr(fP.a, 20), mpmath.nstr(fP.b, 20)], min_bound_margin=mpmath.nstr(minmargin, 4),
                         construction="exact real recursion; all 70 rows hold exactly (e70 with equality)")
print("own primal:", out["own_primal"])
out["gap"] = mpmath.nstr(mpmath.mpf(fP.b) - mpmath.mpf(bound.a), 4)
print("gap primal_upper - bound =", out["gap"])

# MINLPLib p1
xp = [mpmath.mpf(sol.get(nm, "0")) for nm in m["names"]]
viol = max(max(0, (common.row_value(m, i, xp, common.mpnum, common.MPFNS) - mpmath.mpf(c["ub"])) if c["ub"] != "INF" else 0,
               (mpmath.mpf(c["lb"]) - common.row_value(m, i, xp, common.mpnum, common.MPFNS)) if c["lb"] != "-INF" else 0)
           for i, c in enumerate(cons))
out["minlplib_p1"] = dict(objective=mpmath.nstr(common.obj_value(m, xp, common.mpnum, common.MPFNS), 15), max_row_violation=mpmath.nstr(viol, 3))
print("p1:", out["minlplib_p1"])
json.dump(out, open(os.path.join(common.HERE, "logs", "etamac.json"), "w"), indent=1)
