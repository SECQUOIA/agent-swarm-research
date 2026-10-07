"""pindyck: attempt at a global certificate by concavity in the reduced space of prices.

Model (asserted from the OSIL): prices p_t = x_t >= 0 (t = 1..16); total demand
td_t = .87 td_{t-1} - .13 p_t + c_t (td_0 = 18); fringe supply
s_t = .75 s_{t-1} + 1.02^(-kap cs_t) (1.1 + .1 p_t), cs_t = cs_{t-1} + s_t (s_0 = 6.5, cs_0 = 0);
OPEC demand d_t = td_t - s_t >= 0; reserves R_t = R_{t-1} - d_t (R_0 = 500) >= 0;
revenue rev_t = d_t (p_t - 250/R_t); objective min -sum_t delta_t rev_t.
Given p, every other variable is determined (s_t is the unique root of a strictly increasing
function), so the problem is  max J(p) = sum_t delta_t d_t(p) (p_t - 250/R_t(p))  over
feasible p. Feasibility (d_t >= 0) implies p in the box B = prod [0, pbar_t] and in the
polytope P = {td_t(p) >= s_lb,t}; td is affine in p.

Certificate: if the Hessian of J is negative definite on the convex set B n P (interval
second-order forward AD over the whole set, then an exact rational LDL^T test of
-(mid) - rho(radius) I), J is concave there and for every feasible p
   J(p) <= J(p*) + grad J(p*).(p - p*) <= J(p*) + sum_t max(g_t (0 - p*_t), g_t (pbar_t - p*_t)).

Usage: python3 pindyck.py
"""
import os
import sys
from fractions import Fraction

import mpmath as mp
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402
import ia  # noqa: E402
from ia import NI  # noqa: E402

LOG = open(os.path.join(ev.HERE, "logs", "pindyck.log"), "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


I = ev.load("pindyck")
NM = I["names"]
ix = {n: j for j, n in enumerate(NM)}
T = 16
P_ = [ix[f"x{t}"] for t in range(1, 17)]
TD = [ix[f"x{17 + t}"] for t in range(0, 17)]
S = [ix[f"x{34 + t}"] for t in range(0, 17)]
CS = [ix[f"x{51 + t}"] for t in range(0, 17)]
D = [None] + [ix[f"x{67 + t}"] for t in range(1, 17)]
R = [ix[f"x{84 + t}"] for t in range(0, 17)]
REV = [None] + [ix[f"x{100 + t}"] for t in range(1, 17)]
C = I["cons"]
KAP = "-.142857142857143"
# ---------------- structure ----------------
fixed = {TD[0]: "18", S[0]: "6.5", CS[0]: "0", R[0]: "500"}
for j in range(116):
    if j in fixed:
        assert I["lb"][j] == I["ub"][j] == fixed[j], NM[j]
    elif j in REV[1:]:
        assert (I["lb"][j], I["ub"][j]) == ("-INF", "INF")
    else:
        assert (I["lb"][j], I["ub"][j]) == ("0", "INF"), NM[j]
cvals = []
for t in range(1, 17):
    r = C[t - 1]
    assert r["lb"] == r["ub"] and r["nl"] is None and r["lin"] == {P_[t - 1]: ".13", TD[t - 1]: "-.87", TD[t]: "1"}
    cvals.append(r["lb"])
    r = C[16 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["lin"] == {S[t - 1]: "-.75", S[t]: "1"}
    assert r["nl"] == ("negate", ("product", ("power", ("num", "1.02"), ("var", CS[t], KAP)), ("sum", ("num", "1.1"), ("var", P_[t - 1], ".1"))))
    r = C[32 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["nl"] is None and r["lin"] == {S[t]: "-1", CS[t - 1]: "-1", CS[t]: "1"}
    r = C[48 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["nl"] is None and r["lin"] == {TD[t]: "-1", S[t]: "1", D[t]: "1"}
    r = C[64 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["nl"] is None and r["lin"] == {D[t]: "1", R[t - 1]: "-1", R[t]: "1"}
    r = C[80 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["lin"] == {REV[t]: "1"}
    assert r["nl"] == ("product", ("sum", ("negate", ("divide", ("num", "2.5e2"), ("var", R[t], "1"))), ("var", P_[t - 1], "1")), ("var", D[t], "-1"))
o = I["obj"]
assert o["sense"] == "min" and o["constant"] == "0" and not o["quad"] and o["nl"] is None and set(o["lin"]) == set(REV[1:])
delta = [o["lin"][REV[t]].lstrip("-") for t in range(1, 17)]
assert all(o["lin"][REV[t]].startswith("-") for t in range(1, 17)) or o["lin"][REV[1]] == "-1"
assert len(C) == 96
say("structure asserted (96 rows, 116 variables)")

# ---------------- float model and primal ----------------
cf = [float(v) for v in cvals]
df = [float(v) for v in delta]
kf = -float(KAP) * np.log(1.02)


def sim(p):
    td, s, cs, Rr, J = 18.0, 6.5, 0.0, 500.0, 0.0
    for t in range(T):
        td = 0.87 * td - 0.13 * p[t] + cf[t]
        a, b = 0.75 * s, (1.1 + 0.1 * p[t]) * np.exp(-kf * cs)
        x = a + b
        for _ in range(60):
            x -= (x - a - b * np.exp(-kf * x)) / (1 + kf * b * np.exp(-kf * x))
        s = x
        cs += s
        d = td - s
        Rr -= d
        J += df[t] * d * (p[t] - 250 / Rr)
    return J


sol = ev.read_sol(os.path.join(ev.HERE, "sol", "pindyck.p1.sol"))
p1 = np.array([float(sol[f"x{t}"]) for t in range(1, 17)])
r = minimize(lambda p: -sim(p), p1, method="L-BFGS-B", bounds=[(0, 300)] * T, options={"ftol": 1e-15, "gtol": 1e-11})
say("float optimum J =", -r.fun)

# high precision: Newton on grad J = 0 (finite differences at 50 digits)
mp.mp.dps = 50
kmp = -mp.mpf(KAP) * mp.log(mp.mpf("1.02"))


def sim_mp(p, full=False):
    td, s, cs, Rr, J = mp.mpf(18), mp.mpf("6.5"), mp.mpf(0), mp.mpf(500), mp.mpf(0)
    rec = []
    for t in range(T):
        td = mp.mpf(".87") * td - mp.mpf(".13") * p[t] + mp.mpf(cvals[t])
        a, b = mp.mpf(".75") * s, (mp.mpf("1.1") + mp.mpf(".1") * p[t]) * mp.exp(-kmp * cs)
        x = a + b
        for _ in range(200):
            dx = (x - a - b * mp.exp(-kmp * (cs + x) + kmp * cs)) / (1 + kmp * b * mp.exp(-kmp * x))
            x -= dx
            if abs(dx) < mp.mpf(10) ** -55:
                break
        s = x
        cs += s
        d = td - s
        Rr -= d
        J += mp.mpf(delta[t]) * d * (p[t] - 250 / Rr)
        rec.append((td, s, cs, d, Rr, d * (p[t] - 250 / Rr)))
    return (J, rec) if full else J


def grad_mp(p, h=mp.mpf("1e-20")):
    return [(sim_mp([p[k] + (h if k == i else 0) for k in range(T)]) - sim_mp([p[k] - (h if k == i else 0) for k in range(T)])) / (2 * h) for i in range(T)]


pm_ = [mp.mpf(v) for v in r.x]
for it in range(6):
    g = grad_mp(pm_)
    gn = max(abs(v) for v in g)
    say(f"  Newton it {it}: |grad J| = {mp.nstr(gn, 3)}")
    if gn < mp.mpf("1e-30"):
        break
    h = mp.mpf("1e-12")
    H = mp.matrix(T, T)
    for j in range(T):
        gp = grad_mp([pm_[k] + (h if k == j else 0) for k in range(T)])
        for i in range(T):
            H[i, j] = (gp[i] - g[i]) / h
    dp = mp.lu_solve(H, mp.matrix([-v for v in g]))
    pm_ = [pm_[k] + dp[k] for k in range(T)]
Jstar, rec = sim_mp(pm_, True)
say("J(p*) (50 digits) =", mp.nstr(Jstar, 20))
# full primal point for the OSIL model (p rounded to 17 digits, states from the recursion at 50 digits)
ps = [mp.mpf(mp.nstr(v, 17)) for v in pm_]
Jr, rec = sim_mp(ps, True)
x = [mp.mpf(0)] * 116
for j, v in fixed.items():
    x[j] = mp.mpf(v)
for t in range(1, 17):
    td, s, cs, d, Rr, rv = rec[t - 1]
    x[P_[t - 1]], x[TD[t]], x[S[t]], x[CS[t]], x[D[t]], x[R[t]], x[REV[t]] = ps[t - 1], td, s, cs, d, Rr, rv
xs = [mp.nstr(v, 30) for v in x]
res = ev.evaluate(I, xs, dps=50)
say(f"primal point: obj {mp.nstr(res['obj'], 20)}, max row viol {mp.nstr(res['row_viol'], 3)}, bound viol {mp.nstr(res['bound_viol'], 3)}")
with open(os.path.join(ev.HERE, "logs", "pindyck_primal.txt"), "w") as f:
    for j, n in enumerate(NM):
        f.write(f"{n} {xs[j]}\n")
say("min d_t =", mp.nstr(min(rr[3] for rr in rec), 6), " min R_t =", mp.nstr(min(rr[4] for rr in rec), 6))


# ---------------- interval second-order AD over B n P ----------------
iv = mp.iv
iv.dps = 30


def fl(ivv):  # mpmath interval -> outward float NI
    return NI(ia.dn(np.float64(float(ivv.a))), ia.up(np.float64(float(ivv.b))))


K_ = fl(-iv.mpf(KAP) * iv.log(iv.mpf("1.02")))
n = T
Z = NI(np.zeros(n)), NI(np.zeros((n, n)))


class HD:
    def __init__(self, v, g, H):
        self.v, self.g, self.H = v, g, H

    @staticmethod
    def const(c):
        return HD(c if isinstance(c, NI) else NI.const(c), NI(np.zeros(n)), NI(np.zeros((n, n))))

    def __add__(self, o):
        if isinstance(o, HD):
            return HD(self.v + o.v, self.g + o.g, self.H + o.H)
        return HD(self.v + o, self.g, self.H)

    def __neg__(self):
        return HD(-self.v, -self.g, -self.H)

    def __sub__(self, o):
        return self + (-o)

    def scale(self, c):  # c: NI scalar
        return HD(self.v * c, self.g * c, self.H * c)

    def __mul__(self, o):
        if not isinstance(o, HD):
            return self.scale(o)
        gi, gj = self.g, o.g
        outer = NI(gi.lo[:, None], gi.hi[:, None]) * NI(gj.lo[None, :], gj.hi[None, :])
        outer2 = NI(gj.lo[:, None], gj.hi[:, None]) * NI(gi.lo[None, :], gi.hi[None, :])
        return HD(self.v * o.v, gi * o.v + gj * self.v, self.H * o.v + o.H * self.v + outer + outer2)

    def recip(self):
        assert np.all(self.v.lo > 0)
        rr = NI(1.0) / self.v
        r2 = rr * rr
        gg = NI(self.g.lo[:, None], self.g.hi[:, None]) * NI(self.g.lo[None, :], self.g.hi[None, :])
        return HD(rr, -(self.g * r2), -(self.H * r2) + gg * (r2 * rr * 2.0))


def with_range(h, lo, hi):
    """intersect the value enclosure with a known valid range"""
    return HD(NI(np.maximum(h.v.lo, lo), np.minimum(h.v.hi, hi)), h.g, h.H)


def iexp_neg(k, X):  # exp(-k X) for NI scalars (k > 0)
    a = iv.exp(-iv.mpf(float(k.hi)) * iv.mpf(float(X.hi)))
    b = iv.exp(-iv.mpf(float(k.lo)) * iv.mpf(float(X.lo)))
    return NI(ia.dn(np.float64(float(a.a))), ia.up(np.float64(float(b.b))))


def implicit_s(a, b):
    """s = a + b exp(-k s) with a, b HD (b > 0, a >= 0): value by monotone fixpoint, derivatives
    by implicit differentiation."""
    Sv = NI(a.v.lo, ia.up(a.v.hi + b.v.hi))
    for _ in range(40):
        e = iexp_neg(K_, Sv)
        new = a.v + b.v * e
        Sv = NI(np.maximum(Sv.lo, new.lo), np.minimum(Sv.hi, new.hi))
    e = iexp_neg(K_, Sv)
    Dn = NI(1.0) + K_ * b.v * e
    si = (a.g + b.g * e) / Dn
    bi = NI(b.g.lo[:, None], b.g.hi[:, None])
    bj = NI(b.g.lo[None, :], b.g.hi[None, :])
    s_i = NI(si.lo[:, None], si.hi[:, None])
    s_j = NI(si.lo[None, :], si.hi[None, :])
    num = a.H + b.H * e - (bi * s_j + bj * s_i) * (K_ * e) + (s_i * s_j) * (K_ * K_ * b.v * e)
    return HD(Sv, si, num / Dn)


def run(plo, phi, td_ranges=None):
    """interval HD evaluation of J over the box [plo, phi] (td ranges intersected with P)."""
    pv = []
    for t in range(n):
        g = np.zeros(n)
        g[t] = 1.0
        pv.append(HD(NI(plo[t], phi[t]), NI(g), NI(np.zeros((n, n)))))
    td = HD.const("18")
    s = HD.const("6.5")
    cs = HD.const("0")
    Rr = HD.const("500")
    J = HD.const("0")
    info = []
    for t in range(n):
        td = td.scale(NI.const(".87")) - pv[t].scale(NI.const(".13")) + NI.const(cvals[t])
        if td_ranges is not None:
            td = with_range(td, *td_ranges[t])
        a = s.scale(NI.const(".75"))
        eK = iexp_neg(K_, cs.v)
        # b = (1.1 + .1 p_t) exp(-k cs): HD product of (1.1 + .1 p) and E = exp(-k cs)
        Eg = cs.g * (-(K_ * eK))
        cg_i = NI(cs.g.lo[:, None], cs.g.hi[:, None])
        cg_j = NI(cs.g.lo[None, :], cs.g.hi[None, :])
        EH = (cg_i * cg_j) * (K_ * K_ * eK) - cs.H * (K_ * eK)
        E = HD(eK, Eg, EH)
        b = (pv[t].scale(NI.const(".1")) + NI.const("1.1")) * E
        s = implicit_s(a, b)
        cs = cs + s
        d = td - s
        Rr = Rr - d
        rev = d * (pv[t] - Rr.recip().scale(NI.const("2.5e2")))
        J = J + rev.scale(NI.const(delta[t]))
        info.append((td.v, s.v, d.v, Rr.v))
    return J, info


# box: alpha_t = td_t at p = 0; s lower bounds from an interval run with p in [0, big]; pbar from d_t >= 0
alpha = []
a_ = Fraction(18)
for t in range(n):
    a_ = Fraction(".87") * a_ + Fraction(cvals[t])
    alpha.append(a_)
# s_t lower bound valid for all p >= 0: interval run with p in [0, 1e6] (s is increasing in p_t,
# decreasing in past s via cs; the interval recursion covers it)
_, info0 = run(np.zeros(n), np.full(n, 1e6))
slb = [float(inf[1].lo) for inf in info0]
pbar = [float((alpha[t] - Fraction(slb[t])) / Fraction(".13")) * (1 + 1e-12) for t in range(n)]
say("s lower bounds:", [round(v, 3) for v in slb])
say("pbar:", [round(v, 2) for v in pbar])
tdr = [(slb[t], float(alpha[t]) * (1 + 1e-15)) for t in range(n)]
Jb, info = run(np.zeros(n), np.array(pbar), tdr)
say("ranges over B n P: R_t in", [(round(float(i[3].lo), 1), round(float(i[3].hi), 1)) for i in info[-1:]],
    " d range", [(round(float(i[2].lo), 1), round(float(i[2].hi), 1)) for i in info[:3]])
Hlo, Hhi = Jb.H.lo, Jb.H.hi
Cm = (Hlo + Hhi) / 2
Dl = (Hhi - Hlo) / 2
say("Hessian enclosure: max radius", float(Dl.max()), " eig(mid) max", float(np.linalg.eigvalsh((Cm + Cm.T) / 2)[-1]),
    " rho(radius) ~", float(np.max(np.abs(np.linalg.eigvalsh((Dl + Dl.T) / 2)))))


def neg_def_certificate(Hlo, Hhi):
    """True if every symmetric matrix in [Hlo, Hhi] is negative definite (exact rational test)."""
    Cq = [[(Fraction(float(Hlo[i, j])) + Fraction(float(Hhi[i, j])) + Fraction(float(Hlo[j, i])) + Fraction(float(Hhi[j, i]))) / 4
           for j in range(n)] for i in range(n)]
    Dq = [[max(Fraction(float(Hhi[i, j])) - Cq[i][j], Cq[i][j] - Fraction(float(Hlo[i, j])),
               Fraction(float(Hhi[j, i])) - Cq[i][j], Cq[i][j] - Fraction(float(Hlo[j, i]))) for j in range(n)] for i in range(n)]
    # rho(D) <= max_i (D x)_i / x_i for any x > 0 (Collatz-Wielandt); x = float Perron vector, rationalized
    w, V = np.linalg.eigh(np.array([[float(v) for v in row] for row in Dq]))
    xv = [Fraction(max(abs(float(v)), 1e-6)) for v in V[:, -1]]
    rho = max(sum(Dq[i][j] * xv[j] for j in range(n)) / xv[i] for i in range(n))
    Kq = [[-Cq[i][j] - (rho if i == j else 0) for j in range(n)] for i in range(n)]
    # exact LDL^T: K positive definite iff all pivots > 0
    A = [row[:] for row in Kq]
    for k in range(n):
        if A[k][k] <= 0:
            return False, float(rho), k
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return True, float(rho), None


ok, rho, kfail = neg_def_certificate(Hlo, Hhi)
say(f"negative definiteness on B n P: {ok} (rho(radius) <= {rho:.4g}{'' if ok else f', pivot {kfail} failed'})")
if ok:
    Jp, _ = run(np.array([float(v) for v in ps]), np.array([float(v) for v in ps]))
    g = Jp.g
    ub = Jp.v.hi
    for t in range(n):
        pt = float(ps[t])
        c1 = (NI(g.lo[t], g.hi[t]) * NI(ia.dn(0.0 - pt), ia.up(0.0 - pt))).hi
        c2 = (NI(g.lo[t], g.hi[t]) * NI(ia.dn(pbar[t] - pt), ia.up(pbar[t] - pt))).hi
        ub = ia.up(ub + max(c1, c2))
    say(f"RIGOROUS DUAL BOUND (min form): {-ub!r};  primal {mp.nstr(res['obj'], 17)};  gap {float(res['obj']) + ub:.3e}")
else:
    # ---------------- failure analysis ----------------
    # (1) tighten s lower bounds / pbar by a fixpoint with p in [0, pbar]
    sl, pb = list(slb), list(pbar)
    for it in range(6):
        _, inf_ = run(np.zeros(n), np.array(pb), [(sl[t], float(alpha[t]) * (1 + 1e-15)) for t in range(n)])
        sl = [max(sl[t], float(inf_[t][1].lo)) for t in range(n)]
        pb = [float((alpha[t] - Fraction(sl[t])) / Fraction(".13")) * (1 + 1e-12) for t in range(n)]
    say("tightened s_lb:", [round(v, 3) for v in sl])
    say("tightened pbar:", [round(v, 1) for v in pb])
    tdr = [(sl[t], float(alpha[t]) * (1 + 1e-15)) for t in range(n)]
    Jb, _ = run(np.zeros(n), np.array(pb), tdr)
    ok, rho, _k = neg_def_certificate(Jb.H.lo, Jb.H.hi)
    say(f"tightened B n P: negative definite {ok}, rho(radius) <= {rho:.4f}")
    # (2) how large a box around p* can be certified concave?
    pst = np.array([float(v) for v in ps])
    for w in [40, 20, 10, 5, 2, 1]:
        lo, hi = np.maximum(pst - w, 0), np.minimum(pst + w, pb)
        Jb, _ = run(lo, hi, tdr)
        ok, rho, _k = neg_def_certificate(Jb.H.lo, Jb.H.hi)
        say(f"box p* +- {w}: negative definite {ok}, rho(radius) <= {rho:.4f}, "
            f"max eig(mid) {np.linalg.eigvalsh((Jb.H.lo + Jb.H.hi) / 2)[-1]:.4f}")
