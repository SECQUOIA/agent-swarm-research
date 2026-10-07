"""Reviewer's own steps 1-4: a polytope G' containing the feasible price set F, state ranges
over G', and a box Theta' of the Hessian parameters (independent code; same mathematical
ideas as the author's steps 1-4, see pindyck-review.md).

Exact LP bounds: HiGHS proposes duals; the bound is recomputed in exact rationals by weak
duality with finite variable bounds (every variable bound used is itself proved valid).

Output: ranges.pkl with exact data (W', gam', pmax', Theta' as float bounds) and a comparison
with the author's numbers (logs/pindyck_global.log values are re-derived in author_data.py).
"""
import os
import pickle
import sys
import time
from fractions import Fraction as Fr

os.environ.setdefault("OMP_NUM_THREADS", "1")
import mpmath as mp
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import own_model as M  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = open(os.path.join(HERE, "logs", "own_ranges_authorG.log" if os.environ.get("USE_AUTHOR_G") == "1" else "own_ranges.log"), "w")


def say(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


iv = mp.iv
iv.dps = 50
T = 16
Kiv = -iv.mpf(M.KAPSTR) * iv.log(iv.mpf("1.02"))



def raw2fr(r):
    sgn, man, ex, _ = r
    q = Fr(man) * (Fr(2) ** ex)
    return -q if sgn else q


def lo_fr(x):
    return raw2fr(x._mpi_[0])


def hi_fr(x):
    return raw2fr(x._mpi_[1])


Kmid = float(lo_fr(Kiv))       # used only to propose line coefficients


def fl_dn(q):
    """largest double <= rational q"""
    f = float(q)
    return f if Fr(f) <= q else float(np.nextafter(f, -np.inf))


def fl_up(q):
    f = float(q)
    return f if Fr(f) >= q else float(np.nextafter(f, np.inf))


def ivq(q):
    """interval enclosing the rational q"""
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def exp_bounds(clo, chi):
    """rationals (l, h) with l <= exp(-K c) <= h for all c in [clo, chi] (clo, chi rationals)"""
    return lo_fr(iv.exp(-Kiv * ivq(Fr(chi)))), hi_fr(iv.exp(-Kiv * ivq(Fr(clo))))


F87, F13, F75, F1, F11 = Fr(87, 100), Fr(13, 100), Fr(75, 100), Fr(1, 10), Fr(11, 10)
CT = M.CTq
alpha = []
a_ = Fr(18)
for t in range(T):
    a_ = F87 * a_ + CT[t]
    alpha.append(a_)                                     # td_t(p = 0)
L13 = [[F13 * F87 ** (t - j) if j <= t else Fr(0) for j in range(T)] for t in range(T)]


class ExactLP:
    """rows: (coef dict, rhs, kind) kind in {'<=', '='}; lb <= x <= ub finite rationals"""

    def __init__(self, nv, lb, ub):
        self.nv, self.lb, self.ub = nv, list(map(Fr, lb)), list(map(Fr, ub))
        assert all(l <= u for l, u in zip(self.lb, self.ub))
        self.rows = []

    def le(self, cf, rhs):
        self.rows.append(({k: Fr(v) for k, v in cf.items() if v != 0}, Fr(rhs), "<="))

    def eq(self, cf, rhs):
        self.rows.append(({k: Fr(v) for k, v in cf.items() if v != 0}, Fr(rhs), "="))

    def _prep(self):
        self.ub_rows = [r for r in self.rows if r[2] == "<="]
        self.eq_rows = [r for r in self.rows if r[2] == "="]
        Au = np.zeros((len(self.ub_rows), self.nv))
        for i, (cf, _, _) in enumerate(self.ub_rows):
            for k, v in cf.items():
                Au[i, k] = float(v)
        Ae = np.zeros((len(self.eq_rows), self.nv))
        for i, (cf, _, _) in enumerate(self.eq_rows):
            for k, v in cf.items():
                Ae[i, k] = float(v)
        self.Au, self.bu = Au, np.array([float(r[1]) for r in self.ub_rows])
        self.Ae, self.be = Ae, np.array([float(r[1]) for r in self.eq_rows])
        self.bnds = [(float(l), float(u)) for l, u in zip(self.lb, self.ub)]

    def min_bound(self, obj):
        """rigorous lower bound of min obj.x (obj: dict of rationals)"""
        if not hasattr(self, "Au"):
            self._prep()
        c = np.zeros(self.nv)
        for k, v in obj.items():
            c[k] = float(v)
        res = linprog(c, A_ub=self.Au, b_ub=self.bu, A_eq=self.Ae if len(self.eq_rows) else None,
                      b_eq=self.be if len(self.eq_rows) else None, bounds=self.bnds, method="highs")
        assert res.status == 0, res.message
        yu = [min(Fr(float(v)), Fr(0)) for v in res.ineqlin.marginals]     # <= rows: multipliers <= 0
        ye = [Fr(float(v)) for v in res.eqlin.marginals] if len(self.eq_rows) else []
        red = [Fr(0)] * self.nv
        for k, v in obj.items():
            red[k] += Fr(v)
        val = Fr(0)
        for (cf, rhs, _), y in list(zip(self.ub_rows, yu)) + list(zip(self.eq_rows, ye)):
            if y == 0:
                continue
            val += y * rhs
            for k, v in cf.items():
                red[k] -= y * v
        # obj.x = sum_rows y_i (A_i x) + red.x  >=  sum y_i b_i + sum min(red_k l_k, red_k u_k)
        for k in range(self.nv):
            val += min(red[k] * self.lb[k], red[k] * self.ub[k])
        return val, res.fun

    def max_bound(self, obj):
        v, f = self.min_bound({k: -Fr(w) for k, w in obj.items()})
        return -v, -f


# ---------------- step 1': cumulative supply bounds on F ----------------
# variables p_0..p_15 (0..15), s_0..s_15 (16..31); rows valid on F:
#   s_t <= td_t(p) = alpha_t - L13_t.p                      (d_t >= 0)
#   s_t >= .75 s_{t-1} + (1.1 + .1 p_t) el_t,  s_t <= .75 s_{t-1} + (1.1 + .1 p_t) eh_t
# variable bounds valid on F: 0 <= p_t <= alpha_t/.13 (td_t >= s_t > 0), 0 <= s_t <= alpha_t.
def lp_F(CL, CH):
    lp = ExactLP(2 * T, [0] * (2 * T), [alpha[t] / F13 for t in range(T)] + alpha)
    for t in range(T):
        el, _ = exp_bounds(CH[t], CH[t])
        _, eh = exp_bounds(CL[t], CL[t])
        cf = {T + t: 1}
        cf.update({j: L13[t][j] for j in range(t + 1)})
        lp.le(cf, alpha[t])
        prev = {T + t - 1: F75} if t else {}
        s0 = F75 * Fr(13, 2) if t == 0 else Fr(0)
        cf = {T + t: -1, t: F1 * el}
        cf.update(prev)
        lp.le(cf, -F11 * el - s0)
        cf = {T + t: 1, t: -F1 * eh}
        cf.update({k: -v for k, v in prev.items()})
        lp.le(cf, F11 * eh + s0)
    return lp


t0 = time.time()
CL = [Fr(0)] * T
CH = [sum(alpha[:t + 1]) for t in range(T)]
for rnd in range(8):
    lp = lp_F(CL, CH)
    newH, newL = [], []
    for t in range(T):
        ob = {T + j: 1 for j in range(t + 1)}
        newH.append(lp.max_bound(ob)[0])
        newL.append(lp.min_bound(ob)[0])
    CH = [min(a, b) for a, b in zip(CH, newH)]
    CL = [max(a, b) for a, b in zip(CL, newL)]
    say(f"step 1' round {rnd}: CSH_16 = {float(CH[-1]):.6f}  CSL_16 = {float(CL[-1]):.6f}")
say("step 1': cs_t upper bounds on F:", [round(float(v), 4) for v in CH])

# ---------------- step 2': the polytope G' (exact rationals) ----------------
el_F = [exp_bounds(CH[t], CH[t])[0] for t in range(T)]
Wq = [[L13[t][j] + F1 * F75 ** (t - j) * el_F[j] if j <= t else Fr(0) for j in range(T)] for t in range(T)]
gq = [alpha[t] - Fr(13, 2) * F75 ** (t + 1) - F11 * sum(F75 ** (t - j) * el_F[j] for j in range(t + 1)) for t in range(T)]
pmaxq = [gq[t] / Wq[t][t] for t in range(T)]
say("step 2': pmax' =", [round(float(v), 3) for v in pmaxq])
AUTHOR_G = os.environ.get("USE_AUTHOR_G") == "1"
if AUTHOR_G:
    # compare with the author's G, then continue with the author's G (to check the author's Theta)
    A = pickle.load(open(os.path.join(HERE, "author_data.pkl"), "rb"))
    ok_csh = all(Fr(A["CSH"][t]) >= CH[t] for t in range(T))
    ok_W = all(Fr(float(A["W"][t, j])) <= Wq[t][j] for t in range(T) for j in range(T))
    ok_g = all(Fr(float(A["gam"][t])) >= gq[t] for t in range(T))
    say("author's CSH >= my rigorous CSH on F:", ok_csh, " author's W <= my W':", ok_W, " author's gam >= my gam':", ok_g)
    say("  => F is inside the author's G" if (ok_W and ok_g) else "  => containment not shown by this comparison")
    say("  max rel. difference CSH: %.2e" % max(abs(float(Fr(A["CSH"][t]) - CH[t])) / float(CH[t]) for t in range(T)))
    Wq = [[Fr(float(A["W"][t, j])) for j in range(T)] for t in range(T)]
    gq = [Fr(float(A["gam"][t])) for t in range(T)]
    pmaxq = [Fr(float(A["pmax"][t])) for t in range(T)]
    say("continuing with the author's G (W, gam, pmax as stored floats)")
PRIM = os.path.join(HERE, "..", "..", "open-instances-wave2", "small", "logs", "pindyck_primal.txt")
vals = dict(line.split() for line in open(PRIM))
pstar = [Fr(vals[f"x{t}"]) for t in range(1, 17)]
slack = [gq[t] - sum(Wq[t][j] * pstar[j] for j in range(T)) for t in range(T)]
assert all(v > 0 for v in slack) and all(v > 0 for v in pstar)
say("p* in G': min slack %.6f" % float(min(slack)))


# ---------------- step 3': ranges over G' ----------------
def lines_below(L, H, npts=7):
    """lines (a, b): exp(-K x) >= a + b x for ALL real x (tangents, globally valid), rationals"""
    out = []
    for x0 in np.linspace(float(L), float(H), npts):
        f0 = float(np.exp(-Kmid * x0))
        b = -Kmid * f0
        a = f0 - b * x0
        bq, aq = Fr(b), Fr(a)
        # min_x exp(-Kx) - a - b x = (-b/K)(1 - ln(-b/K)) - a   (b < 0)
        r = -ivq(bq) / Kiv
        m = r * (1 - iv.log(r)) - ivq(aq)
        mlo = lo_fr(m)
        if mlo < 0:
            aq = aq + mlo
        out.append((aq, bq))
    return out


def line_above(L, H):
    """(a, b): a + b x >= exp(-K x) on [L, H] (secant, concave gap: check end points)"""
    L, H = Fr(L), Fr(H)
    if H == L:
        return hi_fr(iv.exp(-Kiv * ivq(L))), Fr(0)
    fL, fH = float(np.exp(-Kmid * float(L))), float(np.exp(-Kmid * float(H)))
    bq = Fr((fH - fL) / float(H - L))
    aq = Fr(fL) - bq * L
    need = max(hi_fr(iv.exp(-Kiv * ivq(x)) - ivq(aq) - ivq(bq) * ivq(x)) for x in (L, H))
    if need > 0:
        aq += need
    return aq, bq


def lp_G(CL, CH):
    # variables: p (0..15), s (16..31), e_t = exp(-K cs_t) (32..47), z_t = p_t e_t (48..63)
    sub, s_ = [], Fr(13, 2)
    for t in range(T):
        s_ = F75 * s_ + F11 + F1 * pmaxq[t]               # s_t <= .75 s_{t-1} + 1.1 + .1 pmax (e <= 1)
        sub.append(s_)
    el = [exp_bounds(CH[t], CH[t])[0] for t in range(T)]
    eh = [exp_bounds(CL[t], CL[t])[1] for t in range(T)]
    lp = ExactLP(4 * T, [0] * T + [0] * T + el + [0] * T, pmaxq + sub + eh + [pmaxq[t] * eh[t] for t in range(T)])
    for t in range(T):
        lp.le({j: Wq[t][j] for j in range(t + 1)}, gq[t])
        cf = {T + t: 1, 2 * T + t: -F11, 3 * T + t: -F1}
        if t:
            cf[T + t - 1] = -F75
        lp.eq(cf, F75 * Fr(13, 2) if t == 0 else 0)
        for (a, b) in lines_below(CL[t], CH[t]):      # e_t >= a + b cs_t
            cf = {2 * T + t: -1}
            cf.update({T + j: b for j in range(t + 1)})
            lp.le(cf, -a)
        a, b = line_above(CL[t], CH[t])                # e_t <= a + b cs_t
        cf = {2 * T + t: 1}
        cf.update({T + j: -b for j in range(t + 1)})
        lp.le(cf, a)
        P = pmaxq[t]
        z, e, p = 3 * T + t, 2 * T + t, t
        lp.le({z: -1, p: el[t]}, 0)                          # z >= el p
        lp.le({z: -1, e: P, p: eh[t]}, P * eh[t])            # z >= P e + eh p - P eh
        lp.le({z: 1, e: -P, p: -el[t]}, -P * el[t])          # z <= P e + el p - P el
        lp.le({z: 1, p: -eh[t]}, 0)                          # z <= eh p
    return lp


GL = [Fr(0)] * T
GH, acc, s_ = [], Fr(0), Fr(13, 2)
for t in range(T):
    s_ = F75 * s_ + F11 + F1 * pmaxq[t]
    acc += s_
    GH.append(acc)
for rnd in range(10):
    lp = lp_G(GL, GH)
    nH, nL = [], []
    for t in range(T):
        ob = {T + j: 1 for j in range(t + 1)}
        nH.append(lp.max_bound(ob)[0])
        nL.append(lp.min_bound(ob)[0])
    GH = [min(a, b) for a, b in zip(GH, nH)]
    GL = [max(a, b) for a, b in zip(GL, nL)]
    say(f"step 3' round {rnd}: cs_16 on G' in [{float(GL[-1]):.5f}, {float(GH[-1]):.5f}]")
lp = lp_G(GL, GH)
rs, rd, rR = [], [], []
for t in range(T):
    ob = {T + t: 1}
    rs.append((lp.min_bound(ob)[0], lp.max_bound(ob)[0]))
    ob = {j: -L13[t][j] for j in range(t + 1)}
    ob[T + t] = -1                                        # d_t - alpha_t
    rd.append((lp.min_bound(ob)[0] + alpha[t], lp.max_bound(ob)[0] + alpha[t]))
    ob = {}
    for k in range(t + 1):
        for j in range(k + 1):
            ob[j] = ob.get(j, 0) + L13[k][j]
        ob[T + k] = 1                                     # R_t - (500 - sum alpha)
    base = 500 - sum(alpha[:t + 1])
    rR.append((lp.min_bound(ob)[0] + base, lp.max_bound(ob)[0] + base))
say("step 3': s ranges", [(round(float(a), 3), round(float(b), 3)) for a, b in rs])
say("step 3': d ranges", [(round(float(a), 3), round(float(b), 3)) for a, b in rd])
say("step 3': R ranges", [(round(float(a), 2), round(float(b), 2)) for a, b in rR])
assert all(a > 0 for a, _ in rR)

# ---------------- step 4': Theta' (float bounds, outward) ----------------
GR = ["beta", "E", "phi", "d", "u", "v2", "v3"]
lo = {g: [0.0] * T for g in GR}
hi = {g: [0.0] * T for g in GR}
for t in range(T):
    if t == 0:
        El, Eh = Fr(1), Fr(1)
    else:
        El, Eh = exp_bounds(GL[t - 1], GH[t - 1])       # E_t = exp(-K cs_{t-1})
    lo["E"][t], hi["E"][t] = fl_dn(El), fl_up(Eh)
    lo["beta"][t], hi["beta"][t] = fl_dn(F11 * El), fl_up((F11 + F1 * pmaxq[t]) * Eh)
    pl, ph = exp_bounds(rs[t][0], rs[t][1])
    lo["phi"][t], hi["phi"][t] = fl_dn(pl), fl_up(ph)
    lo["d"][t], hi["d"][t] = fl_dn(rd[t][0]), fl_up(rd[t][1])
    Rl, Rh = rR[t]
    lo["u"][t], hi["u"][t] = fl_dn(-250 / Rl), fl_up(pmaxq[t] - 250 / Rh)
    lo["v2"][t], hi["v2"][t] = fl_dn(1 / Rh ** 2), fl_up(1 / Rl ** 2)
    lo["v3"][t], hi["v3"][t] = fl_dn(1 / Rh ** 3), fl_up(1 / Rl ** 3)
say("step 4': Theta' built; beta_16 in [%.4f, %.4f], u_16 in [%.3f, %.3f]" % (lo["beta"][15], hi["beta"][15], lo["u"][15], hi["u"][15]))
if AUTHOR_G:
    bad = [(g, t) for g in GR for t in range(T) if not (A["lo0"][g][t] <= lo[g][t] and hi[g][t] <= A["hi0"][g][t])]
    say("my rigorous Theta over the author's G is inside the author's Theta:", not bad, bad[:10])
    for g in GR:
        say("  %-4s max gap lo: %.2e  hi: %.2e" % (g, max(lo[g][t] - A["lo0"][g][t] for t in range(T)),
                                                 max(A["hi0"][g][t] - hi[g][t] for t in range(T))))
    for g in GR:
        wl = [lo[g][t] - A["lo0"][g][t] for t in range(T)]
        wh = [A["hi0"][g][t] - hi[g][t] for t in range(T)]
        say("  %-4s min slack lo: %.3e  hi: %.3e" % (g, min(wl), min(wh)))
pickle.dump(dict(CH=CH, CL=CL, Wq=Wq, gq=gq, pmaxq=pmaxq, GL=GL, GH=GH, rs=rs, rd=rd, rR=rR, lo=lo, hi=hi),
            open(os.path.join(HERE, "ranges_authorG.pkl" if AUTHOR_G else "ranges.pkl"), "wb"))
say("time %.1f s" % (time.time() - t0))
