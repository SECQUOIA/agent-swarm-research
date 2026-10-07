"""pindyck: rigorous global dual bound via concavity of the reduced objective J(p).

Model (checked against the OSIL below, same assertions as pindyck.py): prices p_t >= 0,
td_t = .87 td_{t-1} - .13 p_t + c_t (td_0 = 18), s_t = .75 s_{t-1} + exp(-K cs_t)(1.1 + .1 p_t),
cs_t = cs_{t-1} + s_t (s_0 = 6.5, cs_0 = 0), K = .142857142857143 ln 1.02, d_t = td_t - s_t >= 0,
R_t = R_{t-1} - d_t (R_0 = 500), objective min -J(p), J(p) = sum_t delta_t d_t (p_t - 250/R_t).

Certificate (details in pindyck-extension.md):
 1. LP over a linear relaxation of the feasible set F gives CSH_t >= cs_t on F (dual certificates
    checked in exact rational arithmetic).
 2. G = {p >= 0 : W p <= gam} with W, gam built from CSH is a polytope containing F.
 3. A McCormick LP over G bounds, for all p in G, cs_t, s_t, d_t, R_t (exact dual certificates).
 4. The Hessian of J at p equals Psi(theta(p)), an explicit function of per-period quantities
    theta = (beta_t, E_t, phi_t, d_t, u_t, 1/R_t^2, 1/R_t^3); step 3 puts theta(p) in a box Theta.
 5. First-order Taylor models of Psi over sub-boxes of Theta (branch and bound) plus an exact
    interval LDL^T test prove Psi(theta) <= -mu I on Theta. Hence J is concave on the convex set
    G, and for every p in F:  J(p) <= J(p*) + grad J(p*).(p - p*).
 6. J(p*) and grad J(p*) are enclosed by interval arithmetic (mpmath.iv) at the decimal point p*.

Usage: python3 pindyck_global.py      (about 20 s, single-threaded)
"""
import os
import sys
import time
from fractions import Fraction as Fr

os.environ.setdefault("OMP_NUM_THREADS", "1")
import mpmath as mp
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev  # noqa: E402
import tm1  # noqa: E402
from ia import NI  # noqa: E402
from tm1 import TM, iv  # noqa: E402

LOG = open(os.path.join(ev.HERE, "logs", "pindyck_global.log"), "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


T = n = 16
t_start = time.time()

# ---------------- structure (exact string checks against the OSIL) ----------------
I = ev.load("pindyck")
ix = {nm: j for j, nm in enumerate(I["names"])}
P_ = [ix[f"x{t}"] for t in range(1, 17)]
TD = [ix[f"x{17 + t}"] for t in range(0, 17)]
S_ = [ix[f"x{34 + t}"] for t in range(0, 17)]
CS = [ix[f"x{51 + t}"] for t in range(0, 17)]
D_ = [None] + [ix[f"x{67 + t}"] for t in range(1, 17)]
R_ = [ix[f"x{84 + t}"] for t in range(0, 17)]
REV = [None] + [ix[f"x{100 + t}"] for t in range(1, 17)]
C = I["cons"]
KAP = "-.142857142857143"
fixed = {TD[0]: "18", S_[0]: "6.5", CS[0]: "0", R_[0]: "500"}
assert len(I["names"]) == 116 and len(C) == 96
for j in range(116):
    if j in fixed:
        assert I["lb"][j] == I["ub"][j] == fixed[j]
    elif j in REV[1:]:
        assert (I["lb"][j], I["ub"][j]) == ("-INF", "INF")
    else:
        assert (I["lb"][j], I["ub"][j]) == ("0", "INF")
cvals = []
for t in range(1, 17):
    r = C[t - 1]
    assert r["lb"] == r["ub"] and r["nl"] is None and r["lin"] == {P_[t - 1]: ".13", TD[t - 1]: "-.87", TD[t]: "1"}
    cvals.append(r["lb"])
    r = C[16 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["lin"] == {S_[t - 1]: "-.75", S_[t]: "1"}
    assert r["nl"] == ("negate", ("product", ("power", ("num", "1.02"), ("var", CS[t], KAP)),
                                  ("sum", ("num", "1.1"), ("var", P_[t - 1], ".1"))))
    r = C[32 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["nl"] is None and r["lin"] == {S_[t]: "-1", CS[t - 1]: "-1", CS[t]: "1"}
    r = C[48 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["nl"] is None and r["lin"] == {TD[t]: "-1", S_[t]: "1", D_[t]: "1"}
    r = C[64 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["nl"] is None and r["lin"] == {D_[t]: "1", R_[t - 1]: "-1", R_[t]: "1"}
    r = C[80 + t - 1]
    assert r["lb"] == r["ub"] == "0" and r["lin"] == {REV[t]: "1"}
    assert r["nl"] == ("product", ("sum", ("negate", ("divide", ("num", "2.5e2"), ("var", R_[t], "1"))),
                                   ("var", P_[t - 1], "1")), ("var", D_[t], "-1"))
o = I["obj"]
assert o["sense"] == "min" and o["constant"] == "0" and not o["quad"] and o["nl"] is None
assert set(o["lin"]) == set(REV[1:]) and all(o["lin"][REV[t]].startswith("-") for t in range(2, 17))
assert o["lin"][REV[1]] == "-1"
delta = [o["lin"][REV[t]][1:] for t in range(1, 17)]
say("structure asserted (96 rows, 116 variables); delta =", delta[:3], "...")

Kiv = -iv.mpf(KAP) * iv.log(iv.mpf("1.02"))        # K = -KAP ln 1.02 > 0
Kf = float(Kiv.mid)
Fq = {s: Fr(s) for s in [".87", ".13", ".75", ".1", "1.1", "6.5", "18", "500", "2.5e2"]}
alphaq = []                                        # alpha_t = td_t(p = 0), exact
a_ = Fr(18)
for t in range(T):
    a_ = Fq[".87"] * a_ + Fr(cvals[t])
    alphaq.append(a_)
L13q = [[Fq[".13"] * Fq[".87"] ** (t - k) if k <= t else Fr(0) for k in range(T)] for t in range(T)]


def fdn(x):
    """largest double <= the Fraction/iv lower value"""
    if isinstance(x, Fr):
        f = float(x)
        return f if Fr(f) <= x else float(np.nextafter(f, -np.inf))
    return float(np.nextafter(float(x.a), -np.inf))


def fup(x):
    if isinstance(x, Fr):
        f = float(x)
        return f if Fr(f) >= x else float(np.nextafter(f, np.inf))
    return float(np.nextafter(float(x.b), np.inf))


def expK_iv(lo, hi):
    """enclosure [exp(-K hi), exp(-K lo)] as floats (outward)"""
    return fdn(iv.exp(-Kiv * iv.mpf(float(hi)))), fup(iv.exp(-Kiv * iv.mpf(float(lo))))


# ---------------- rigorous LP bounds (weak duality, exact rationals) ----------------
class LP:
    """max/min c.x s.t. rows (sparse dict, rhs) with sense '<=' or '=', lb <= x <= ub (finite).
    Data are Fractions; HiGHS is used only to propose dual multipliers."""

    def __init__(self, nv, lb, ub):
        self.nv, self.lb, self.ub = nv, [Fr(v) for v in lb], [Fr(v) for v in ub]
        self.rows = []  # (dict, rhs, is_eq)

    def add(self, coef, rhs, eq=False):
        self.rows.append(({k: Fr(v) for k, v in coef.items() if v != 0}, Fr(rhs), eq))

    def _mats(self):
        ub_r = [r for r in self.rows if not r[2]]
        eq_r = [r for r in self.rows if r[2]]
        def dense(rs):
            A = np.zeros((len(rs), self.nv))
            for i, (cf, _, _) in enumerate(rs):
                for k, v in cf.items():
                    A[i, k] = float(v)
            return A, np.array([float(r[1]) for r in rs])
        self._ub, self._eq = ub_r, eq_r
        self._Aub, self._bub = dense(ub_r)
        self._Aeq, self._beq = dense(eq_r) if eq_r else (None, None)

    def bound(self, cobj, maximize):
        """rigorous upper bound of max c.x (maximize) or lower bound of min c.x"""
        if not hasattr(self, "_Aub"):
            self._mats()
        c = np.zeros(self.nv)
        for k, v in cobj.items():
            c[k] = float(v)
        f = -c if maximize else c
        res = linprog(f, A_ub=self._Aub, b_ub=self._bub, A_eq=self._Aeq, b_eq=self._beq,
                      bounds=list(zip([float(v) for v in self.lb], [float(v) for v in self.ub])), method="highs")
        assert res.status == 0, res.message
        # min f.x >= sum y_i b_i + sum mu_j beq_j + sum_k min_box (f - A^T y - Aeq^T mu)_k x_k, y <= 0
        y = [min(Fr(float(v)), Fr(0)) for v in res.ineqlin.marginals]
        mu = [Fr(float(v)) for v in res.eqlin.marginals] if self._eq else []
        fq = [Fr(0)] * self.nv
        for k, v in cobj.items():
            fq[k] = -Fr(v) if maximize else Fr(v)
        val = Fr(0)
        for (cf, rhs, _), yi in zip(self._ub, y):
            if yi:
                val += yi * rhs
                for k, v in cf.items():
                    fq[k] -= yi * v
        for (cf, rhs, _), mj in zip(self._eq, mu):
            if mj:
                val += mj * rhs
                for k, v in cf.items():
                    fq[k] -= mj * v
        for k in range(self.nv):
            val += min(fq[k] * self.lb[k], fq[k] * self.ub[k])
        lower_f = val                              # rigorous lower bound of min f.x
        bnd = -lower_f if maximize else lower_f
        lpval = -res.fun if maximize else res.fun
        return bnd, lpval


# ---------------- step 1: CSH on the feasible set F ----------------
def lp_F(CSL, CSH):
    """relaxation of F in (p, s): s_k <= td_k(p) (d >= 0), supply bounds with e in [e(CSH), e(CSL)]"""
    lp = LP(2 * T, [0] * (2 * T), [alphaq[k] / Fq[".13"] for k in range(T)] + [alphaq[k] for k in range(T)])
    for k in range(T):
        elo, _ = expK_iv(CSH[k], CSH[k])
        _, ehi = expK_iv(CSL[k], CSL[k])
        elo, ehi = Fr(elo), Fr(ehi)
        cf = {T + k: 1}
        for j in range(k + 1):
            cf[j] = L13q[k][j]
        lp.add(cf, alphaq[k])                                   # s_k + .13 sum .87^(k-j) p_j <= alpha_k
        s0 = Fq[".75"] * Fq["6.5"] if k == 0 else Fr(0)
        cf = {T + k: -1, k: Fq[".1"] * elo}
        if k:
            cf[T + k - 1] = Fq[".75"]
        lp.add(cf, -Fq["1.1"] * elo - s0)                       # s_k >= .75 s_{k-1} + (1.1+.1p_k) elo
        cf = {T + k: 1, k: -Fq[".1"] * ehi}
        if k:
            cf[T + k - 1] = -Fq[".75"]
        lp.add(cf, Fq["1.1"] * ehi + s0)                        # s_k <= .75 s_{k-1} + (1.1+.1p_k) ehi
    return lp


CSL = [0.0] * T
CSH = [fup(sum(alphaq[:k + 1])) for k in range(T)]          # s_j <= td_j <= alpha_j on F
for it in range(6):
    lp = lp_F(CSL, CSH)
    nH, nL = [], []
    for k in range(T):
        obj = {T + j: 1 for j in range(k + 1)}
        nH.append(fup(lp.bound(obj, True)[0]))
        nL.append(fdn(lp.bound(obj, False)[0]))
    CSH = [min(a, b) for a, b in zip(CSH, nH)]
    CSL = [max(a, b) for a, b in zip(CSL, nL)]
say("step 1: cs_t upper bounds on F (certified):", [round(v, 3) for v in CSH])

# ---------------- step 2: the polytope G ----------------
elo_F = [Fr(expK_iv(CSH[k], CSH[k])[0]) for k in range(T)]
Wq = [[L13q[k][j] + Fq[".1"] * Fq[".75"] ** (k - j) * elo_F[j] if j <= k else Fr(0) for j in range(T)] for k in range(T)]
gamq = [alphaq[k] - Fq["6.5"] * Fq[".75"] ** (k + 1) - Fq["1.1"] * sum(Fq[".75"] ** (k - j) * elo_F[j] for j in range(k + 1))
        for k in range(T)]
W = np.array([[fdn(Wq[k][j]) if j <= k else 0.0 for j in range(T)] for k in range(T)])
gam = np.array([fup(g) for g in gamq])
pmax = [fup(Fr(gam[k]) / Fr(W[k, k])) for k in range(T)]   # p_k <= gam_k / W_kk on G
say("step 2: G = {p >= 0, W p <= gam}; p_t <= ", [round(v, 2) for v in pmax])

# primal point p* (decimal strings from pindyck.py's 50-digit Newton solve)
prim = {}
for line in open(os.path.join(ev.HERE, "logs", "pindyck_primal.txt")):
    k, v = line.split()
    prim[k] = v
pstr = [prim[f"x{t}"] for t in range(1, 17)]
pq = [Fr(s) for s in pstr]
slack = [Fr(gam[k]) - sum(Fr(W[k, j]) * pq[j] for j in range(T)) for k in range(T)]
assert all(v > 0 for v in slack) and all(v > 0 for v in pq)
say("p* is in the interior of G: min slack", float(min(slack)))

# ---------------- step 3: state ranges on G (McCormick LP) ----------------
# variables: p (0..15), s (16..31), e_k = exp(-K cs_k) (32..47), z_k = p_k e_k (48..63)
def valid_lines(L, H):
    """lines a + b x below exp(-K x) on [L, H] (tangents) and one above (secant), all verified"""
    out_lo = []
    for x0 in np.linspace(L, H, 5):
        f0 = float(np.exp(-Kf * x0))
        b = -Kf * f0
        a = f0 - b * x0
        # h(x) = exp(-Kx) - a - b x convex; min >= h(x0) - |h'(x0)| (H - L)
        h0 = iv.exp(-Kiv * f2(x0)) - f2(a) - f2(b) * f2(x0)
        dh = -Kiv * iv.exp(-Kiv * f2(x0)) - f2(b)
        low = h0 - abs(dh) * f2(H - L + 1.0)
        if float(low.a) < 0:
            a = fdn(iv.mpf(a) + low.a)
        out_lo.append((a, b))
    if H > L:
        fL, fH = float(np.exp(-Kf * L)), float(np.exp(-Kf * H))
        b = (fH - fL) / (H - L)
        a = fL - b * L
        # h = a + b x - exp(-Kx) concave: min at end points
        m = min((f2(a) + f2(b) * f2(x) - iv.exp(-Kiv * f2(x))).a for x in (L, H))
        if float(m) < 0:
            a = fup(iv.mpf(a) - m)
        up = (a, b)
    else:
        up = (fup(iv.exp(-Kiv * f2(L))), 0.0)
    return out_lo, up


def f2(x):
    return iv.mpf(float(x))


def lp_G(CSL, CSH):
    sub = []
    s_ = Fr(13, 2)
    for k in range(T):
        s_ = Fq[".75"] * s_ + Fq["1.1"] + Fq[".1"] * Fr(pmax[k])        # e <= 1
        sub.append(s_)
    e_lo = [expK_iv(CSH[k], CSH[k])[0] for k in range(T)]
    e_hi = [expK_iv(CSL[k], CSL[k])[1] for k in range(T)]
    lb = [0] * T + [0] * T + e_lo + [0] * T
    ub = pmax + sub + e_hi + [Fr(pmax[k]) * Fr(e_hi[k]) for k in range(T)]
    lp = LP(4 * T, lb, ub)
    for k in range(T):
        lp.add({j: W[k, j] for j in range(k + 1)}, gam[k])
        cf = {T + k: 1, 2 * T + k: -Fq["1.1"], 3 * T + k: -Fq[".1"]}
        if k:
            cf[T + k - 1] = -Fq[".75"]
        lp.add(cf, Fq[".75"] * Fq["6.5"] if k == 0 else 0, eq=True)
        tang, (au, bu) = valid_lines(CSL[k], CSH[k])
        for (a, b) in tang:          # e_k >= a + b cs_k  <=>  -e_k + b sum s <= -a
            cf = {2 * T + k: -1}
            for j in range(k + 1):
                cf[T + j] = b
            lp.add(cf, -Fr(a))
        cf = {2 * T + k: 1}          # e_k <= au + bu cs_k
        for j in range(k + 1):
            cf[T + j] = -bu
        lp.add(cf, Fr(au))
        P, el, eh = Fr(pmax[k]), Fr(e_lo[k]), Fr(e_hi[k])
        zk, ek, pk = 3 * T + k, 2 * T + k, k
        lp.add({zk: -1, pk: el}, 0)                          # z >= el p
        lp.add({zk: -1, ek: P, pk: eh}, P * eh)              # z >= P e + eh p - P eh
        lp.add({zk: 1, ek: -P, pk: -el}, -P * el)            # z <= P e + el p - P el
        lp.add({zk: 1, pk: -eh}, 0)                          # z <= eh p
    return lp


GCSL = [0.0] * T
GCSH = []
acc, s_ = 0.0, 6.5
for k in range(T):
    s_ = 0.75 * s_ + 1.1 + 0.1 * pmax[k]
    acc += s_
    GCSH.append(acc * (1 + 1e-12) + 1e-9)
for it in range(7):
    lp = lp_G(GCSL, GCSH)
    nH, nL = [], []
    for k in range(T):
        obj = {T + j: 1 for j in range(k + 1)}
        nH.append(fup(lp.bound(obj, True)[0]))
        nL.append(fdn(lp.bound(obj, False)[0]))
    GCSH = [min(a, b) for a, b in zip(GCSH, nH)]
    GCSL = [max(a, b) for a, b in zip(GCSL, nL)]
say("step 3: cs_t on G in", [(round(a, 2), round(b, 2)) for a, b in zip(GCSL, GCSH)][::5])
lp = lp_G(GCSL, GCSH)
rng = {"s": [], "d": [], "R": []}
gaps = []
for t in range(T):
    ob = {T + t: 1}
    hi_, v1 = lp.bound(ob, True)
    lo_, v2 = lp.bound(ob, False)
    rng["s"].append((fdn(lo_), fup(hi_)))
    gaps.append(float(hi_ - Fr(v1)))
    ob = {j: -L13q[t][j] for j in range(t + 1)}              # d_t = alpha_t - L13 p - s_t
    ob[T + t] = -1
    hi_, _ = lp.bound(ob, True)
    lo_, _ = lp.bound(ob, False)
    rng["d"].append((fdn(lo_ + alphaq[t]), fup(hi_ + alphaq[t])))
    ob = {}                                                  # R_t = 500 - sum_{k<=t} d_k
    for k in range(t + 1):
        for j in range(k + 1):
            ob[j] = ob.get(j, 0) + L13q[k][j]
        ob[T + k] = 1
    base = Fr(500) - sum(alphaq[:t + 1])
    hi_, _ = lp.bound(ob, True)
    lo_, _ = lp.bound(ob, False)
    rng["R"].append((fdn(lo_ + base), fup(hi_ + base)))
say("       s_t in", [(round(a, 2), round(b, 2)) for a, b in rng["s"]][::5])
say("       d_t in", [(round(a, 2), round(b, 2)) for a, b in rng["d"]][::5])
say("       R_t in", [(round(a, 1), round(b, 1)) for a, b in rng["R"]][::5])
say("       (dual-certificate slack vs. LP value, max over s bounds: %.1e)" % max(gaps))
assert min(r[0] for r in rng["R"]) > 0

# ---------------- step 4: parameter box Theta ----------------
GROUPS = ["beta", "E", "phi", "d", "u", "v2", "v3"]
lo0, hi0 = {g: np.zeros(T) for g in GROUPS}, {g: np.zeros(T) for g in GROUPS}
for t in range(T):
    El, Eh = (1.0, 1.0) if t == 0 else expK_iv(GCSL[t - 1], GCSH[t - 1])
    lo0["E"][t], hi0["E"][t] = El, Eh
    lo0["beta"][t] = fdn(iv.mpf("1.1") * f2(El))
    hi0["beta"][t] = fup((iv.mpf("1.1") + iv.mpf(".1") * f2(pmax[t])) * f2(Eh))
    lo0["phi"][t], hi0["phi"][t] = expK_iv(*rng["s"][t])
    lo0["d"][t], hi0["d"][t] = rng["d"][t]
    Rl, Rh = f2(rng["R"][t][0]), f2(rng["R"][t][1])
    lo0["u"][t] = fdn(-iv.mpf(250) / Rl)
    hi0["u"][t] = fup(f2(pmax[t]) - iv.mpf(250) / Rh)
    lo0["v2"][t], hi0["v2"][t] = fdn(1 / (Rh * Rh)), fup(1 / (Rl * Rl))
    lo0["v3"][t], hi0["v3"][t] = fdn(1 / (Rh * Rh * Rh)), fup(1 / (Rl * Rl * Rl))
say("step 4: Theta built (beta_16 in [%.3f, %.3f], E_16 in [%.3f, %.3f], u_16 in [%.2f, %.2f])"
    % (lo0["beta"][15], hi0["beta"][15], lo0["E"][15], hi0["E"][15], lo0["u"][15], hi0["u"][15]))


# ---------------- step 4b: float sanity checks (not part of the proof) ----------------
def float_states(p):
    """float recursion: theta(p) and the float Hessian of J (forward second-order AD)"""
    cf, df = [float(v) for v in cvals], [float(v) for v in delta]
    Z1, Z2 = np.zeros(n), np.zeros((n, n))
    td, s, cs, R = (18.0, Z1, Z2), (6.5, Z1, Z2), (0.0, Z1, Z2), (500.0, Z1, Z2)
    JH = Z2.copy()
    th = {g: np.zeros(T) for g in GROUPS}
    mul = lambda x, y: (x[0] * y[0], x[1] * y[0] + y[1] * x[0], x[2] * y[0] + y[2] * x[0] + np.outer(x[1], y[1]) + np.outer(y[1], x[1]))
    for t in range(T):
        et = np.eye(n)[t]
        td = (0.87 * td[0] - 0.13 * p[t] + cf[t], 0.87 * td[1] - 0.13 * et, Z2)
        Ev = np.exp(-Kf * cs[0])
        E = (Ev, -Kf * Ev * cs[1], Kf * Kf * Ev * np.outer(cs[1], cs[1]) - Kf * Ev * cs[2])
        b = mul((1.1 + 0.1 * p[t], 0.1 * et, Z2), E)
        a = (0.75 * s[0], 0.75 * s[1], 0.75 * s[2])
        x = a[0] + b[0]
        for _ in range(60):
            x -= (x - a[0] - b[0] * np.exp(-Kf * x)) / (1 + Kf * b[0] * np.exp(-Kf * x))
        ph = np.exp(-Kf * x)
        Dn = 1 + Kf * b[0] * ph
        sg = (a[1] + b[1] * ph) / Dn
        sH = (a[2] + b[2] * ph - Kf * ph * (np.outer(b[1], sg) + np.outer(sg, b[1])) + Kf * Kf * b[0] * ph * np.outer(sg, sg)) / Dn
        s = (x, sg, sH)
        cs = (cs[0] + x, cs[1] + sg, cs[2] + sH)
        d = (td[0] - x, td[1] - sg, -sH)
        R = (R[0] - d[0], R[1] - d[1], R[2] - d[2])
        rr = 1 / R[0]
        q = (p[t] - 250 * rr, et + 250 * R[1] * rr * rr, 250 * (R[2] * rr * rr - 2 * np.outer(R[1], R[1]) * rr ** 3))
        JH += df[t] * mul(d, q)[2]
        for g, v in zip(GROUPS, [b[0], Ev, ph, d[0], q[0], rr * rr, rr ** 3]):
            th[g][t] = v
    return th, JH


rs_ = np.random.default_rng(0)
p_ = np.array([float(v) for v in pstr])
A_ = np.vstack([W, -np.eye(T)])
b_ = np.concatenate([gam, np.zeros(T)])
inside, lam_max, nsamp = True, -1.0, 0
for it in range(3000):                               # hit-and-run in G
    u_ = rs_.normal(size=T)
    Au, sl = A_ @ u_, b_ - A_ @ p_
    tmax = np.min(np.where(Au > 1e-12, sl / np.where(Au > 1e-12, Au, 1), np.inf))
    tmin = np.max(np.where(Au < -1e-12, sl / np.where(Au < -1e-12, Au, 1), -np.inf))
    p_ = p_ + rs_.uniform(tmin, tmax) * u_
    if it % 10 == 0:
        th, JH = float_states(np.maximum(p_, 0))
        nsamp += 1
        lam_max = max(lam_max, np.linalg.eigvalsh(JH)[-1])
        for g in GROUPS:
            inside &= bool(np.all(th[g] >= lo0[g] - 1e-12) and np.all(th[g] <= hi0[g] + 1e-12))
say(f"step 4b (float check): {nsamp} hit-and-run points of G: theta inside Theta: {inside}; "
    f"largest Hessian eigenvalue {lam_max:.4f}")


# ---------------- step 5: Taylor model of Psi and the concavity branch and bound ----------------
def recipTM(x):
    lo, hi = x.range()
    assert lo > 0
    return tm1.linearize(x, lambda t: 1 / t, lambda t: -1 / (t * t), lambda al: 1 / np.sqrt(-al) if al < 0 else float(hi))


tdg_iv = [[iv.mpf(".13") * iv.mpf(".87") ** (t - k) for k in range(T)] for t in range(T)]


def psi_tm(lo, hi):
    """TM over the box [lo, hi] of Psi(theta) = Hessian of J (see module docstring)."""
    m = len(GROUPS) * T
    tm1.M[0] = m
    par = {}
    for gi, g in enumerate(GROUPS):
        par[g] = []
        for t in range(T):
            l, h = float(lo[g][t]), float(hi[g][t])
            c = 0.5 * (l + h)
            r = float(np.nextafter(max(h - c, c - l), np.inf))
            assert Fr(c) - Fr(r) <= Fr(l) and Fr(c) + Fr(r) >= Fr(h)
            a = np.zeros(m)
            a[gi * T + t] = r
            par[g].append(TM(np.float64(c), a, np.float64(0.0)))
    K = TM.from_iv(Kiv)
    K2 = K * K
    z1, z2 = TM.const(0.0, 0.0, (n,)), TM.const(0.0, 0.0, (n, n))
    sg, sH, csg, csH, Rg, RH, JH = z1, z2, z1, z2, z1, z2, z2
    c75, c1, c250, two, one = TM.dec(".75"), TM.dec(".1"), TM.dec("2.5e2"), TM.const(2.0), TM.const(1.0)
    for t in range(T):
        tdg = TM(np.array([-float(tdg_iv[t][k].mid) if k <= t else 0.0 for k in range(n)]), np.zeros((n, m)),
                 np.array([float(tdg_iv[t][k].delta) + abs(float(tdg_iv[t][k].mid)) * 2.0 ** -51 + 1e-300 if k <= t else 0.0
                           for k in range(n)]))
        et = np.zeros(n)
        et[t] = 1.0
        ET = TM.const(et, 0.0, (n,))
        E = one if t == 0 else par["E"][t]
        beta, phi, d, u, v2, v3 = [par[g][t] for g in ["beta", "phi", "d", "u", "v2", "v3"]]
        io = recipTM(one + K * beta * phi)           # 1 / (1 + K w_t), w_t = beta_t phi_t
        kap = phi * io
        ag, aH = sg * c75, sH * c75
        Eg = csg * (-(K * E))                        # grad exp(-K cs_{t-1})
        bg = ET * (c1 * E) - csg * (K * beta)        # b = (1.1 + .1 p_t) exp(-K cs_{t-1})
        bH = (csg.col() * csg.row() * K2 - csH * K) * beta + (ET.col() * Eg.row() + Eg.col() * ET.row()) * c1
        sg = ag * io + bg * kap                      # implicit differentiation of s = a + b exp(-K s)
        sH = aH * io + bH * kap - (bg.col() * sg.row() + sg.col() * bg.row()) * (K * kap) \
            + (sg.col() * sg.row()) * (K2 * beta * kap)
        csg, csH = csg + sg, csH + sH
        dg, dH = tdg - sg, -sH
        Rg, RH = Rg - dg, RH - dH
        rg = -(Rg * v2)                              # grad 1/R
        rH = -(RH * v2) + (Rg.col() * Rg.row()) * (two * v3)
        qg, qH = ET - rg * c250, -(rH * c250)        # q = p_t - 250/R_t
        revH = dH * u + qH * d + dg.col() * qg.row() + qg.col() * dg.row()
        JH = JH + revH * TM.dec(delta[t])
    return JH


def ildl_pd(Mlo, Mhi):
    """batch (B, n, n) interval matrices; True where every matrix in the enclosure has positive
    pivots in Gaussian elimination without pivoting (hence the exact symmetric member is PD)."""
    A = NI(Mlo.copy(), Mhi.copy())
    B = Mlo.shape[0]
    ok = np.ones(B, bool)
    for k in range(n):
        plo, phi_ = A.lo[:, k, k].copy(), A.hi[:, k, k].copy()
        ok &= plo > 0
        plo = np.where(ok, plo, 1.0)
        phi_ = np.where(ok, phi_, 1.0)
        if k == n - 1:
            break
        col = NI(A.lo[:, k + 1:, k], A.hi[:, k + 1:, k]) / NI(plo[:, None], phi_[:, None])
        row = NI(A.lo[:, k, k + 1:], A.hi[:, k, k + 1:])
        upd = NI(col.lo[:, :, None], col.hi[:, :, None]) * NI(row.lo[:, None, :], row.hi[:, None, :])
        sub = NI(A.lo[:, k + 1:, k + 1:], A.hi[:, k + 1:, k + 1:]) - upd
        A.lo[:, k + 1:, k + 1:], A.hi[:, k + 1:, k + 1:] = sub.lo, sub.hi
    return ok


def rho_up(N):
    """rigorous upper bound of the Perron root of a nonnegative matrix (Collatz-Wielandt)"""
    w, V = np.linalg.eigh((N + N.T) / 2)
    x = np.maximum(np.abs(V[:, -1]), 1e-3)
    Nx = N @ x
    Nx = Nx * (1 + 64 * 2.0 ** -52) + 1e-300
    return float(np.max(Nx / x) * (1 + 4 * 2.0 ** -52))


MU = 1e-3


def mabs_upper(Ak):
    """For symmetric float matrices A_k (m, n, n) return interval enclosures of matrices X_k with
    X_k >= A_k and X_k >= -A_k (Loewner order):  X_k = V |L| V^T + e_k I, where A_k ~ V L V^T is a
    float eigendecomposition and e_k >= ||A_k - V L V^T||_2.  Then X_k -+ A_k = V (|L| -+ L) V^T
    + e_k I -+ (A_k - V L V^T) >= 0 exactly, for any real V."""
    w, V = np.linalg.eigh(Ak)
    m_ = Ak.shape[0]
    B = NI(np.zeros((m_, n, n)))
    X0 = NI(np.zeros((m_, n, n)))
    for j in range(n):
        vj = V[:, :, j]
        outer = NI(vj[:, :, None]) * NI(vj[:, None, :])
        B = B + outer * NI(w[:, j][:, None, None])
        X0 = X0 + outer * NI(np.abs(w[:, j])[:, None, None])
    E = NI(Ak) - B
    Eab = np.maximum(np.abs(E.lo), np.abs(E.hi))
    e = Eab.sum(-1).max(-1) * (1 + 64 * 2.0 ** -52) + 1e-300      # >= ||E||_inf >= ||E||_2 (E symmetric)
    return X0 + NI(e[:, None, None] * np.eye(n)), w


def check_box(lo, hi, rigorous=True):
    """returns (float estimate of the bound on lambda_max, certified?)"""
    H = psi_tm(lo, hi)
    # symmetrize: true Hessian in (c + c^T)/2 + sum eps_k (a_k + a_k^T)/2 +- r_s
    cs = 0.5 * (H.c + H.c.T)
    As = 0.5 * (H.a + np.swapaxes(H.a, 0, 1))
    rs = tm1.upb(0.5 * (H.r + H.r.T) + 2.0 ** -52 * (np.abs(cs) + np.abs(As).sum(-1)))
    rs = np.maximum(rs, rs.T)
    Ak = np.moveaxis(As, -1, 0)                          # (m, n, n)
    X, w = mabs_upper(Ak)
    rho = rho_up(rs)
    est = float(np.linalg.eigvalsh(cs + X.hi.sum(0))[-1] + rho)
    if not rigorous or est > -MU:
        return est, False
    # -(c_s + sum X_k) - (rho + MU) I > 0 by exact interval LDL^T
    Ssum = NI(-cs)
    for k in range(X.lo.shape[0]):
        Ssum = Ssum - X[k]
    Ssum = Ssum - NI(np.eye(n) * rho) - NI(np.eye(n) * MU)
    ok = bool(ildl_pd(Ssum.lo[None], Ssum.hi[None])[0])
    return est, ok


th, JH = float_states(np.array([float(v) for v in pstr]))
Hp = psi_tm({g: th[g].copy() for g in GROUPS}, {g: th[g].copy() for g in GROUPS})
say(f"step 5 (float check): Psi at theta(p*) vs float Hessian of J at p*: max diff {np.abs(Hp.c - JH).max():.1e}")
# branch and bound on Theta; split order: parameter with the largest (sensitivity x relative width)
t0 = time.time()
est0, _ = check_box(lo0, hi0, rigorous=False)
say(f"step 5: root box estimate lambda_max <= {est0:.4f} (needs < {-MU})")
sens = {}
for g in ["beta", "u", "E", "d"]:
    sens[g] = np.zeros(T)
    for t in range(T):
        hi2 = {k: v.copy() for k, v in hi0.items()}
        hi2[g][t] = 0.5 * (lo0[g][t] + hi0[g][t])
        sens[g][t] = max(est0 - check_box(lo0, hi2, rigorous=False)[0], 0.0)
queue = [(lo0, hi0, 0)]
nbox, worst, maxdep, splits = 0, -1.0, 0, {}
while queue:
    lo, hi, dep = queue.pop()
    est, ok = check_box(lo, hi)
    if ok:
        nbox += 1
        worst, maxdep = max(worst, est), max(maxdep, dep)
        continue
    assert dep < 30, "branch and bound depth limit"
    best = max(((sens[g][t] * (hi[g][t] - lo[g][t]) / (hi0[g][t] - lo0[g][t]), g, t)
                for g in sens for t in range(T) if hi0[g][t] > lo0[g][t]))
    _, g, t = best
    splits[f"{g}_{t + 1}"] = splits.get(f"{g}_{t + 1}", 0) + 1
    mid = 0.5 * (lo[g][t] + hi[g][t])
    l1, h1 = {k: v.copy() for k, v in lo.items()}, {k: v.copy() for k, v in hi.items()}
    l2, h2 = {k: v.copy() for k, v in lo.items()}, {k: v.copy() for k, v in hi.items()}
    h1[g][t] = mid
    l2[g][t] = mid
    queue += [(l1, h1, dep + 1), (l2, h2, dep + 1)]
say(f"        certified: Psi(theta) <= -{MU} I on all of Theta ({nbox} boxes, depth <= {maxdep}, "
    f"largest float estimate {worst:.4f}, {time.time() - t0:.1f} s); splits: {splits}")

# ---------------- step 6: J(p*) and grad J(p*) by interval arithmetic ----------------
class G1:
    """value + gradient, mpmath iv"""

    def __init__(self, v, g):
        self.v, self.g = v, g

    def __add__(self, o):
        if isinstance(o, G1):
            return G1(self.v + o.v, [a + b for a, b in zip(self.g, o.g)])
        return G1(self.v + o, self.g)

    def __sub__(self, o):
        if isinstance(o, G1):
            return G1(self.v - o.v, [a - b for a, b in zip(self.g, o.g)])
        return G1(self.v - o, self.g)

    def __mul__(self, o):
        if isinstance(o, G1):
            return G1(self.v * o.v, [a * o.v + self.v * b for a, b in zip(self.g, o.g)])
        return G1(self.v * o, [a * o for a in self.g])


iv.dps = 40
mp.mp.dps = 40
zero = [iv.mpf(0)] * T
pv = [G1(iv.mpf(pstr[t]), [iv.mpf(1) if k == t else iv.mpf(0) for k in range(T)]) for t in range(T)]
td, s, cs, R, J = G1(iv.mpf(18), zero), G1(iv.mpf("6.5"), zero), G1(iv.mpf(0), zero), G1(iv.mpf(500), zero), G1(iv.mpf(0), zero)
mins = []
for t in range(T):
    td = td * iv.mpf(".87") - pv[t] * iv.mpf(".13") + iv.mpf(cvals[t])
    a = s * iv.mpf(".75")
    E = iv.exp(-Kiv * cs.v)
    b = (pv[t] * iv.mpf(".1") + iv.mpf("1.1")) * E
    b = G1(b.v, [bg - (pv[t].v * iv.mpf(".1") + iv.mpf("1.1")) * Kiv * E * cg for bg, cg in zip(b.g, cs.g)])
    # s = a + b exp(-K s): interval fixed point with verified inclusion
    x = mp.mpf((a.v + b.v).mid)
    for _ in range(100):
        x = mp.mpf((a.v + b.v * iv.exp(-Kiv * x)).mid)
    X = iv.mpf([x - mp.mpf(10) ** -30, x + mp.mpf(10) ** -30])
    TX = a.v + b.v * iv.exp(-Kiv * X)
    assert X.a <= TX.a and TX.b <= X.b, "no inclusion for s"
    sv = TX
    phi = iv.exp(-Kiv * sv)
    Dn = 1 + Kiv * b.v * phi
    s = G1(sv, [(ag + bg * phi) / Dn for ag, bg in zip(a.g, b.g)])
    cs = cs + s
    d = td - s
    R = R - d
    q = G1(pv[t].v - iv.mpf(250) / R.v, [(iv.mpf(1) if k == t else iv.mpf(0)) + iv.mpf(250) * R.g[k] / (R.v * R.v) for k in range(T)])
    J = J + (d * q) * iv.mpf(delta[t])
    mins.append((float(d.v.a), float(R.v.a)))
assert all(md > 0 and mr > 0 for md, mr in mins)
def ends(x):
    """exact mpf end points of an mpmath interval"""
    with mp.workprec(400):
        return mp.mpf(x._mpi_[0]), mp.mpf(x._mpi_[1])


def dec_down(x, k=19):
    """decimal string <= x (mpf), k digits after the point"""
    sgn, man, ex, _ = mp.mpf(x)._mpf_          # x = (-1)^sgn man 2^ex (man_exp drops the sign)
    q = (-1) ** sgn * Fr(man) * Fr(2) ** ex
    f = (q * 10 ** k).__floor__()
    sign, f = ("-", -f) if f < 0 else ("", f)
    if sign:                                  # floor of a negative number: keep rounding downward
        return f"-{f // 10 ** k}.{f % 10 ** k:0{k}d}"
    return f"{f // 10 ** k}.{f % 10 ** k:0{k}d}"


ub = J.v
for t in range(T):
    ga, gb = ends(J.g[t])
    gmax = max(abs(ga), abs(gb))
    dist = fup(max(pq[t], Fr(pmax[t]) - pq[t]))                  # max |p_t - p*_t| on G
    ub = ub + iv.mpf(gmax) * iv.mpf(dist)
Jlo, Jhi = ends(J.v)
UB = ends(ub)[1]
gmax = max(max(abs(v) for v in ends(g)) for g in J.g)
say(f"step 6: J(p*) in [{mp.nstr(Jlo, 25)}, {mp.nstr(Jhi, 25)}] (width {mp.nstr(Jhi - Jlo, 2)}); max |grad J(p*)| <= {mp.nstr(gmax, 3)}; "
    f"min d_t(p*) = {min(m_[0] for m_ in mins):.3f}, min R_t(p*) = {min(m_[1] for m_ in mins):.2f}")
say(f"RIGOROUS GLOBAL BOUND (min form): every feasible point has objective >= {dec_down(-UB)}")
say(f"   the feasible point defined by p* has objective -J(p*) <= {mp.nstr(-Jlo, 25)}; gap <= {mp.nstr(UB - Jlo, 3)}")
say(f"total time {time.time() - t_start:.1f} s")
