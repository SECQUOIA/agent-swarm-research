"""etamac: rigorous dual bound via a convex relaxation (hidden convexity).

Relaxation R: replace the 9 production equalities
    YN_t - CES_t(KN_t, LN_t, EN_t) = 0   (e9..e16),   Y_1 - CES_1(LN_1, EN_1) = 3.4653339648 (e43)
by  YN_t - CES~_t <= 0  and  Y_1 - CES~_1 <= 3.4653339648, where CES~ >= CES is concave
(see below). Every feasible point of etamac is feasible for R, so min R <= min etamac.

Concavity. CES_t = (a KN^-p1 + b LN^-p2 EN^-p3)^-q (decimal exponents from the file).
With r = 1/q, u = KN^(p1 q), v = LN^(p2 q) EN^(p3 q): CES = (a u^-r + b v^-r)^(-1/r), a
weighted power mean with exponent -r < 0, which is concave and nondecreasing in (u, v) > 0.
u is concave (0 < p1 q < 1). v is Cobb-Douglas with degree s = (p2 + p3) q, and with the
file's decimals s = 1 + 4.2e-16 > 1 (not concave). With w = LN^(p2 q/s) EN^(p3 q/s)
(degree exactly 1, concave), v = w^s <= kappa w for w <= W, kappa = max(1, W)^(s-1).
CES~ := (a u^-r + b (kappa w)^-r)^(-1/r) = (a KN^-p1 + b kappa^-r LN^(-p2/s) EN^(-p3/s))^-q
is concave (composition rule) and CES~ >= CES on the box. Same for period 1 (constant c0
in place of a u^-r).

Box X (valid for R): upper bounds propagated forward: Y_1 <= 3.4653339648 + c0^-q;
YN_t <= a_t^-q KN_t^(p1 q) (drop the LN/EN term, which is >= 0); KN_t = 4.91287681 I_{t-1};
I_t <= Y_t - C_lb - EC_lb,t; Y_{t+1} = .8153726976 Y_t + YN_{t+1}; then C, EC, L, E, LN, EN,
K from the linear rows. Lower bounds: file bounds (EC from its row).

Certificate: Lagrangian l(x) = f(x) + sum nu_j h_j(x) + sum mu_c g~_c(x) + mu70 g70(x),
nu free on linear equalities, mu >= 0 on the relaxed rows and on e70. l is convex on X, so
min_X l >= l(xh) + sum_k min(dl_k (lb_k - xh_k), dl_k (ub_k - xh_k)), evaluated in mpmath.iv
at a point xh and multipliers from a 50-digit Newton solve of the KKT system.

Usage: python3 etamac.py
"""
import os
import sys
from fractions import Fraction

import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402
import ia  # noqa: E402
from ia import AD  # noqa: E402

LOG = open(os.path.join(ev.HERE, "logs", "etamac.log"), "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


I = ev.load("etamac")
NM = I["names"]
ix = {n: j for j, n in enumerate(NM)}
T = range(1, 10)
K = {t: ix[f"x{t}"] for t in T}
KN = {t: ix[f"x{8 + t}"] for t in range(2, 10)}
Y = {t: ix[f"x{17 + t}"] for t in T}
YN = {t: ix[f"x{25 + t}"] for t in range(2, 10)}
L = {t: ix[f"x{34 + t}"] for t in T}
LN = {t: ix[f"x{43 + t}"] for t in T}
E = {t: ix[f"x{52 + t}"] for t in T}
EN = {t: ix[f"x{61 + t}"] for t in T}
C = {t: ix[f"x{70 + t}"] for t in T}
IV = {t: ix[f"x{79 + t}"] for t in T}
EC = {t: ix[f"x{88 + t}"] for t in T}
R = I["cons"]
D = ".8153726976"


def V(j):
    return ("var", j, "1")


def pw(j, e):
    return ("power", V(j), ("num", e))


# ---------------- structure assertions ----------------
P1, P2, P3, Q, B = "-.342222222222222", "-.427777777777778", "-.794444444444445", "-.818181818181818", ".306708090151268"
acoef = {}
for t in range(1, 9):
    r = R[t - 1]
    assert (r["lb"], r["ub"], r["lin"], r["nl"]) == ("0", "0", {KN[t + 1]: "1", IV[t]: "-4.91287681"}, None)
    r = R[8 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["lin"] == {YN[t + 1]: "1"}
    nl = r["nl"]
    acoef[t + 1] = nl[1][1][1][2][1]
    assert nl == ("negate", ("power", ("sum", ("product", pw(KN[t + 1], P1), ("num", acoef[t + 1])),
                                       ("product", pw(LN[t + 1], P2), ("num", B), pw(EN[t + 1], P3))), ("num", Q)))
r = R[16]
assert (r["lb"], r["ub"], r["lin"], r["nl"]) == ("-2.038431744", "-2.038431744", {L[1]: "-1", LN[1]: "1"}, None)
r = R[25]
assert (r["lb"], r["ub"], r["lin"], r["nl"]) == ("-40.76863488", "-40.76863488", {E[1]: "-1", EN[1]: "1"}, None)
for t in range(1, 9):
    assert (R[16 + t]["lb"], R[16 + t]["ub"], R[16 + t]["lin"], R[16 + t]["nl"]) == ("0", "0", {L[t]: D, L[t + 1]: "-1", LN[t + 1]: "1"}, None)
    assert (R[25 + t]["lb"], R[25 + t]["ub"], R[25 + t]["lin"], R[25 + t]["nl"]) == ("0", "0", {E[t]: D, E[t + 1]: "-1", EN[t + 1]: "1"}, None)
    assert (R[33 + t]["lb"], R[33 + t]["ub"], R[33 + t]["lin"], R[33 + t]["nl"]) == ("0", "0", {K[t]: "-" + D, K[t + 1]: "1", KN[t + 1]: "-1"}, None)
    assert (R[42 + t]["lb"], R[42 + t]["ub"], R[42 + t]["lin"], R[42 + t]["nl"]) == ("0", "0", {Y[t]: "-" + D, Y[t + 1]: "1", YN[t + 1]: "-1"}, None)
r = R[42]
C0 = ".612508399277048"
assert r["lb"] == r["ub"] == "3.4653339648" and r["lin"] == {Y[1]: "1"}
assert r["nl"] == ("negate", ("power", ("sum", ("product", pw(LN[1], P2), ("num", B), pw(EN[1], P3)), ("num", C0)), ("num", Q)))
cL, cE = {}, {}
for t in T:
    r = R[50 + t]
    assert r["lb"] == r["ub"] == "0" and r["nl"] is None and set(r["lin"]) == {L[t], E[t], EC[t]} and r["lin"][EC[t]] == "1e3"
    cL[t], cE[t] = r["lin"][L[t]].lstrip("-"), r["lin"][E[t]].lstrip("-")
    assert r["lin"][L[t]].startswith("-") and r["lin"][E[t]].startswith("-")
    r = R[59 + t]
    assert (r["lb"], r["ub"], r["lin"], r["nl"]) == ("0", "0", {Y[t]: "1", C[t]: "-1", IV[t]: "-1", EC[t]: "-1"}, None)
r = R[69]
assert (r["lb"], r["ub"], r["lin"], r["nl"]) == ("-INF", "0", {K[9]: "7e-2", IV[9]: "-1"}, None)
assert len(R) == 70 and all(c["constant"] == "0" and not c["quad"] for c in R)
o = I["obj"]
assert o["sense"] == "min" and o["constant"] == "0" and not o["lin"] and not o["quad"] and o["nl"][0] == "negate"
beta = {}
for t, term in zip(T, o["nl"][1][1:]):
    assert term[0] == "product" and term[1] == ("ln", V(C[t])) and term[2][0] == "num"
    beta[t] = term[2][1]
    assert Fraction(beta[t]) > 0
assert len(o["nl"][1]) == 10
for j in range(97):
    assert I["vt"][j] == "C" and I["ub"][j] == ("12.32657617084" if j == K[1] else "INF")
assert I["lb"][K[1]] == "12.32657617084"
for t in T:
    assert I["lb"][EC[t]] == "-INF" and all(Fraction(I["lb"][d[t]]) > 0 for d in (C, IV, L, E, LN, EN, Y, K))
say("structure asserted: 70 rows, 97 variables, objective -sum beta_t ln C_t (beta_t > 0)")

# ---------------- exponent facts (exact) ----------------
p1, p2, p3, q = -Fraction(P1), -Fraction(P2), -Fraction(P3), -Fraction(Q)
s_deg = (p2 + p3) * q
say(f"p1*q = {float(p1 * q)!r} (in (0,1): {0 < p1 * q < 1});  s = (p2+p3) q = 1 + {float(s_deg - 1):.3e}")
assert 0 < p1 * q < 1 and s_deg > 1
e2, e3 = p2 / s_deg, p3 / s_deg  # exponents of the concave majorant (exact rationals)
assert (e2 + e3) * q == 1

# ---------------- box X (mpmath interval, outward) ----------------
iv = mp.iv
iv.dps = 40


def I_(s):
    return iv.mpf(s)


def ipow(x, e):  # x > 0, e rational
    return iv.exp(iv.mpf(Fraction(e).numerator) / iv.mpf(Fraction(e).denominator) * iv.log(x))


lbv = [I_(I["lb"][j]) if I["lb"][j] != "-INF" else None for j in range(97)]
ub = [None] * 97
Dv = I_(D)
Ybar, Ibar = {}, {}
ECl = {t: (I_(cL[t]) * lbv[L[t]] + I_(cE[t]) * lbv[E[t]]) / I_("1e3") for t in T}
Ybar[1] = I_("3.4653339648") + ipow(I_(C0), q * -1)   # (b w-term + c0)^-q <= c0^-q
for t in range(1, 9):
    Ibar[t] = Ybar[t] - lbv[C[t]] - ECl[t]
    knb = I_("4.91287681") * Ibar[t]
    ynb = ipow(I_(acoef[t + 1]), -q) * ipow(knb, p1 * q)
    ub[KN[t + 1]], ub[YN[t + 1]] = knb, ynb
    Ybar[t + 1] = Dv * Ybar[t] + ynb
Ibar[9] = Ybar[9] - lbv[C[9]] - ECl[9]
for t in T:
    ub[Y[t]], ub[IV[t]] = Ybar[t], Ibar[t]
    ub[C[t]] = Ybar[t] - lbv[IV[t]] - ECl[t]
    ecb = Ybar[t] - lbv[C[t]] - lbv[IV[t]]
    ub[EC[t]] = ecb
    lbv[EC[t]] = ECl[t]
    ub[L[t]] = (I_("1e3") * ecb - I_(cE[t]) * lbv[E[t]]) / I_(cL[t])
    ub[E[t]] = (I_("1e3") * ecb - I_(cL[t]) * lbv[L[t]]) / I_(cE[t])
ub[LN[1]] = ub[L[1]] - I_("2.038431744")
ub[EN[1]] = ub[E[1]] - I_("40.76863488")
ub[K[1]] = lbv[K[1]]
for t in range(1, 9):
    ub[LN[t + 1]] = ub[L[t + 1]] - Dv * lbv[L[t]]
    ub[EN[t + 1]] = ub[E[t + 1]] - Dv * lbv[E[t]]
    ub[K[t + 1]] = Dv * ub[K[t]] + ub[KN[t + 1]]
assert all(u is not None for u in ub) and all(l is not None for l in lbv)
ubs = [mp.mpf(u.b) for u in ub]                       # upper ends: valid upper bounds
lbs = [mp.mpf(l.a) for l in lbv]                      # lower ends: valid lower bounds
for j in range(97):
    assert lbs[j] <= ubs[j], NM[j]
say("box: max upper bound", mp.nstr(max(ubs), 6), "at", NM[max(range(97), key=lambda j: ubs[j])],
    "; Ybar_9 =", mp.nstr(ubs[Y[9]], 6))
W = max(max(ubs[LN[t]], ubs[EN[t]]) for t in T)
kappa_exp = s_deg - 1                                  # kappa = max(1, W)^(s-1)
iv.dps = 40
kappa = ipow(iv.mpf(max(W, 1)), kappa_exp)
kappa_ub = kappa.b
say(f"W = {mp.nstr(W, 6)}, kappa - 1 <= {mp.nstr(mp.mpf(kappa_ub) - 1, 3)}")

# ---------------- models: functions with pluggable arithmetic ----------------


def ces_orig(num, powf, t, x):
    """CES_t as in the file (t = 2..9) or period 1 (t = 1). Variables stay on the left of
    mixed operations (AD objects)."""
    wt = powf(x[LN[t]], -p2) * powf(x[EN[t]], -p3) * num(B)
    s_ = wt + num(C0) if t == 1 else wt + powf(x[KN[t]], -p1) * num(acoef[t])
    return powf(s_, -q)


def ces_tilde(num, powf, kap, t, x):
    wt = powf(x[LN[t]], -e2) * powf(x[EN[t]], -e3) * num(B) * powf(kap, -1 / q)
    s_ = wt + num(C0) if t == 1 else wt + powf(x[KN[t]], -p1) * num(acoef[t])
    return powf(s_, -q)


def lin_rows():
    """linear equality rows (index, lin, rhs) and e70."""
    out = []
    for k, r in enumerate(R):
        if r["nl"] is None and k != 69:
            out.append((k, r["lin"], r["lb"]))
    return out


LROWS = lin_rows()
CESROWS = [(8 + t - 2, t) for t in range(2, 10)] + [(42, 1)]   # (row index, period)
assert len(LROWS) == 60 and all(R[k]["lb"] == R[k]["ub"] for k, _, _ in LROWS)


def lagr(x, nu, mu, mu70, num, powf, logf, ces):
    """l(x) = f + sum nu h + sum mu (lhs - rhs) + mu70 g70 (all rows written as lhs - rhs)."""
    acc = None
    for t in T:
        term = logf(x[C[t]]) * num(beta[t])
        acc = term if acc is None else acc + term
    val = -acc
    for (k, lin, rhs), n in zip(LROWS, nu):
        row = None
        for j, c in lin.items():
            term = x[j] * num(c)
            row = term if row is None else row + term
        val = val + (row - num(rhs)) * n
    for (k, t), m in zip(CESROWS, mu):
        lhs = x[YN[t]] if t >= 2 else x[Y[1]]
        val = val + (lhs - ces(t, x) - num(R[k]["lb"])) * m
    val = val + (x[K[9]] * num("7e-2") - x[IV[9]]) * mu70
    return val


# ---------------- KKT solve (original equality model, 50 digits) ----------------
mp.mp.dps = 50
sol = ev.read_sol(os.path.join(ev.HERE, "sol", "etamac.p1.sol"))
x0 = [mp.mpf(sol[n]) for n in NM]
free = [j for j in range(97) if j != K[1]]
x0[K[1]] = mp.mpf(I["lb"][K[1]])


def mp_pow(a, e):
    return a ** (mp.mpf(Fraction(e).numerator) / Fraction(e).denominator) if isinstance(e, Fraction) else a ** e


def grad_lagr(xv, nu, mu, mu70):
    """gradient of the original Lagrangian (CES as in the file) via AD over the free variables."""
    nfree = len(free)
    zero = mp.mpf(0)
    pos = {j: k for k, j in enumerate(free)}
    xa = []
    for j in range(97):
        if j in pos:
            g = [zero] * nfree
            g[pos[j]] = mp.mpf(1)
            xa.append(AD(xv[j], tuple(g)))
        else:
            xa.append(AD(xv[j], tuple([zero] * nfree)))

    def powf(a, e):
        ev_ = mp.mpf(Fraction(e).numerator) / Fraction(e).denominator
        v = a.v ** ev_
        return AD(v, tuple(gg * ev_ * v / a.v for gg in a.g))

    def logf(a):
        return ia.ad_log(a, mp.log)

    ces = lambda t, x: ces_orig(mp.mpf, powf, t, x)  # noqa: E731
    lv = lagr(xa, nu, mu, mu70, mp.mpf, powf, logf, ces)
    return lv


def rows_orig(xv):
    out = []
    for k, lin, rhs in LROWS:
        out.append(sum(mp.mpf(c) * xv[j] for j, c in lin.items()) - mp.mpf(rhs))
    for k, t in CESROWS:
        lhs = xv[YN[t]] if t >= 2 else xv[Y[1]]
        out.append(lhs - ces_orig(mp.mpf, mp_pow, t, xv) - mp.mpf(R[k]["lb"]))
    out.append(mp.mpf("7e-2") * xv[K[9]] - xv[IV[9]])
    return out


NU, NMU = len(LROWS), len(CESROWS)


def F(z):
    xv = list(x0)
    for k, j in enumerate(free):
        xv[j] = z[k]
    nu = z[len(free):len(free) + NU]
    mu = z[len(free) + NU:len(free) + NU + NMU]
    mu70 = z[-1]
    g = grad_lagr(xv, nu, mu, mu70)
    return list(g.g) + rows_orig(xv)


# initial multipliers: least squares on stationarity at p1 (float)
import numpy as np  # noqa: E402

nz = len(free) + NU + NMU + 1
z = [x0[j] for j in free] + [mp.mpf(0)] * (NU + NMU + 1)
# gradient of f and each row separately -> least squares
base = F(z)[:len(free)]
cols = []
for k in range(NU + NMU + 1):
    zz = list(z)
    zz[len(free) + k] = mp.mpf(1)
    cols.append([float(a - b) for a, b in zip(F(zz)[:len(free)], base)])
A = np.array(cols).T
mult, *_ = np.linalg.lstsq(A, -np.array([float(v) for v in base]), rcond=None)
z = [x0[j] for j in free] + [mp.mpf(float(v)) for v in mult]
say("initial stationarity residual (float LS):", float(np.max(np.abs(A @ mult + np.array([float(v) for v in base])))))
for it in range(12):
    Fz = F(z)
    res = max(abs(v) for v in Fz)
    say(f"  Newton it {it}: residual {mp.nstr(res, 3)}")
    if res < mp.mpf("1e-40"):
        break
    J = mp.matrix(nz, nz)
    h = mp.mpf("1e-22")
    for c in range(nz):
        zz = list(z)
        zz[c] += h
        Fc = F(zz)
        for r_ in range(nz):
            J[r_, c] = (Fc[r_] - Fz[r_]) / h
    dz = mp.lu_solve(J, mp.matrix([-v for v in Fz]))
    z = [z[i] + dz[i] for i in range(nz)]
xh = list(x0)
for k, j in enumerate(free):
    xh[j] = z[k]
nu = z[len(free):len(free) + NU]
mu = z[len(free) + NU:len(free) + NU + NMU]
mu70 = z[-1]
say("mu (relaxed rows) min:", mp.nstr(min(mu), 6), " mu70:", mp.nstr(mu70, 6))
assert min(mu) > 0 and mu70 > 0
for j in free:
    assert lbs[j] <= xh[j] <= ubs[j], NM[j]
active = [NM[j] for j in free if xh[j] - lbs[j] < mp.mpf("1e-8")]
say("variables at a lower bound at the KKT point:", active)

# ---------------- primal: the KKT point, rounded to 17 digits ----------------
xs = [mp.nstr(v, 17) if j != K[1] else I["lb"][K[1]] for j, v in enumerate(xh)]
r = ev.evaluate(I, xs, dps=50)
say(f"primal (KKT point, 17 digits): obj {mp.nstr(r['obj'], 18)}, max row viol {mp.nstr(r['row_viol'], 3)} ({r['worst_row']}), "
    f"bound viol {mp.nstr(r['bound_viol'], 3)}")
with open(os.path.join(ev.HERE, "logs", "etamac_primal.txt"), "w") as fo:
    for j, n in enumerate(NM):
        fo.write(f"{n} {xs[j]}\n")
r1 = ev.eval_sol("etamac.p1")
say(f"MINLPLib p1: obj {mp.nstr(r1['obj'], 18)}, max row viol {mp.nstr(r1['row_viol'], 3)}, bound viol {mp.nstr(r1['bound_viol'], 3)}")

# ---------------- certificate in interval arithmetic ----------------
iv.dps = 40
nuq = [iv.mpf(mp.nstr(v, 30)) for v in nu]
muq = [iv.mpf(mp.nstr(v, 30)) for v in mu]
mu70q = iv.mpf(mp.nstr(mu70, 30))
assert all(m.a > 0 for m in muq) and mu70q.a > 0
xq = [iv.mpf(mp.nstr(v, 30)) if j != K[1] else iv.mpf(I["lb"][K[1]]) for j, v in enumerate(xh)]
kap = iv.mpf(kappa_ub)
n97 = 97
zero = iv.mpf(0)
xa = []
for j in range(n97):
    g = [zero] * n97
    g[j] = iv.mpf(1)
    xa.append(AD(xq[j], tuple(g)))


def ivpow(a, e):
    if isinstance(a, AD):
        ev_ = iv.mpf(Fraction(e).numerator) / iv.mpf(Fraction(e).denominator)
        v = iv.exp(ev_ * iv.log(a.v))
        return AD(v, tuple(gg * ev_ * v / a.v for gg in a.g))
    ev_ = iv.mpf(Fraction(e).numerator) / iv.mpf(Fraction(e).denominator)
    return iv.exp(ev_ * iv.log(a))


def ivlog(a):
    return ia.ad_log(a, iv.log)


ces_t = lambda t, x: ces_tilde(iv.mpf, ivpow, kap, t, x)  # noqa: E731
lv = lagr(xa, nuq, muq, mu70q, iv.mpf, ivpow, ivlog, ces_t)
bound = lv.v
worst_term = None
for j in range(n97):
    d = lv.g[j]
    lo_t = d * (iv.mpf(lbs[j]) - xq[j])
    hi_t = d * (iv.mpf(ubs[j]) - xq[j])
    t_ = iv.mpf([min(lo_t.a, hi_t.a), min(lo_t.a, hi_t.a)])
    bound = bound + t_
say("l(xh) =", mp.nstr(mp.mpf(lv.v.a), 20), " max |dl/dx_j(xh)| over free j =",
    mp.nstr(max(max(abs(mp.mpf(lv.g[j].a)), abs(mp.mpf(lv.g[j].b))) for j in free), 3),
    "; dl/dK_1 (fixed variable) =", mp.nstr(mp.mpf(lv.g[K[1]].a), 6))
say(f"RIGOROUS DUAL BOUND (etamac): {mp.nstr(mp.mpf(bound.a), 17)}")
say(f"primal {mp.nstr(r['obj'], 17)}; gap {mp.nstr(r['obj'] - mp.mpf(bound.a), 3)}")
