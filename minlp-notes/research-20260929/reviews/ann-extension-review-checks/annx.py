"""Reviewer's own rigorous lower bound for ann_cumene_tanh on boxes of the 5 inputs.

Model: the relaxation R as decoded by the wave-3 verifier's `annv.decode` (verifier code; nothing
is imported from open-instances-wave3/).  R: inputs x723..x727 in their box, the 779 forward rows
(529 linear, 250 tanh), objective f = const + sum lin_j x_j + sum bil_pr x_p x_r, and every finite
bound of a determined variable plus x772 >= 0.999.

Bound on a box Q (all steps valid for every point of Q, no feasibility assumption until step 4):
 1. Affine forms.  u = m + h*xi_{1..5} with m = fl(mid), h >= max(hi-m, m-lo) (rounded up), so
    xi in [-1,1]^5 covers Q.  Every determined variable gets x = C + A.xi + rho, |rho| <= r, with
    xi in [-1,1]^255: 5 input symbols and one symbol per tanh neuron.
 2. Rounding.  All float operations are covered by a generous relative slack TAU = 1e-12 per step
    (the true rounding errors are below gamma_n = n u/(1-n u) <= 3e-14 for the sums used here,
    n <= 256), see the comments at each step.  Constants are the correctly rounded doubles of the
    exact rationals; their representation error (<= u relative) is inside TAU.
 3. tanh.  On the argument range [l, t] = C -+ (S + r) (outward), tanh(s) = alpha s + beta + e,
    |e| <= delta, with (beta, delta) from a rigorous range of g = tanh - alpha s: the range of g is
    the hull of its ranges over pieces cut at 0 and near the stationary points +-s0; on a piece
    inside s <= 0 or s >= 0, g' = sech^2 - alpha is monotone, so if g' has one rigorous sign at both
    ends the extremes are at the ends; otherwise the piece gets the crude enclosure
    [tanh(a) - alpha b, tanh(b) - alpha a] (alpha >= 0).  tanh at float points uses our own interval
    exp (argument reduction by ln 2, degree-22 Taylor polynomial, remainder bound; + - * / only,
    each rounded outward with nextafter).  No libm transcendental is used for rigorous values.
 4. Constraints.  For each bound s(x_j - b) >= 0 (s = +1 lower, -1 upper) that the affine range
    can violate: s A_j.xi + s (C_j - b) + r_j >= 0 on feasible points.  An LP (HiGHS) over
    xi in [-1,1]^255 gives multipliers mu >= 0; the bound
        f >= C_f - r_f - sum_j mu_j (s (C_j - b) + r_j) - || A_f - sum_j mu_j s A_j ||_1
    is then evaluated in outward-rounded interval arithmetic (weak duality; any mu >= 0 is valid).
    If the LP is infeasible an elastic LP supplies large multipliers (still weak duality).
    If one side cannot hold anywhere on the box, the box is infeasible.

Branching (optional): bisection of the input with the largest relative width, until the bound
reaches the target or a node limit is hit.
"""
import os
import sys
import time
from fractions import Fraction as Fr

sys.dont_write_bytecode = True
import mpmath as mp  # noqa: E402
import numpy as np  # noqa: E402
import scipy.sparse as sp  # noqa: E402
from scipy.optimize import linprog  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "wave3-verification", "ann"))
import annv  # noqa: E402

INF = np.inf
TAU = 1e-12
TINY = 1e-300


def dn(x):
    return np.nextafter(x, -INF)


def up(x):
    return np.nextafter(x, INF)


def fiv(q):
    """float enclosure [lo, hi] of a rational q"""
    q = Fr(q)
    x = float(q)
    if Fr(x) == q:
        return x, x
    return (x, float(up(x))) if Fr(x) < q else (float(dn(x)), x)


# ----------------------------------------------------------------------------- interval arithmetic
class IV:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = np.asarray(lo, dtype=np.float64)
        self.hi = self.lo if hi is None else np.asarray(hi, dtype=np.float64)

    def __add__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return IV(dn(self.lo + o.lo), up(self.hi + o.hi))

    def __sub__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return IV(dn(self.lo - o.hi), up(self.hi - o.lo))

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __mul__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        p = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        lo = np.minimum(np.minimum(p[0], p[1]), np.minimum(p[2], p[3]))
        hi = np.maximum(np.maximum(p[0], p[1]), np.maximum(p[2], p[3]))
        return IV(dn(lo), up(hi))

    def __truediv__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        assert np.all((o.lo > 0) | (o.hi < 0))
        p = (self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi)
        lo = np.minimum(np.minimum(p[0], p[1]), np.minimum(p[2], p[3]))
        hi = np.maximum(np.maximum(p[0], p[1]), np.maximum(p[2], p[3]))
        return IV(dn(lo), up(hi))


# ln 2 enclosure: 60-digit decimal compared exactly with the doubles
with mp.workdps(60):
    _l2q = Fr(mp.nstr(mp.log(2), 58, strip_zeros=False))
_l2f = float(_l2q)
_eps = Fr(1, 10 ** 55)
LN2 = IV(_l2f if Fr(_l2f) <= _l2q - _eps else float(dn(_l2f)), _l2f if Fr(_l2f) >= _l2q + _eps else float(up(_l2f)))
assert Fr(float(LN2.lo)) < _l2q < Fr(float(LN2.hi))
_NT = 22
_INVF = [IV(1.0) / IV(float(np.prod(np.arange(1, j + 1, dtype=np.float64)))) if j > 0 else IV(1.0) for j in range(_NT + 1)]
# j! is exact in double for j <= 22
_REM = 1e-30   # >= |r|^23/23! * e^|r| for |r| <= 0.36  (0.36^23/23! ~ 2e-33)


def iexp_pt(x):
    """rigorous enclosure of exp(x) at float points, |x| <= 700"""
    x = np.asarray(x, dtype=np.float64)
    assert np.all(np.abs(x) <= 700)
    k = np.rint(x / 0.6931471805599453)
    r = IV(x) - IV(k) * LN2
    assert np.all(np.maximum(np.abs(r.lo), np.abs(r.hi)) <= 0.36)
    acc = _INVF[_NT]
    for j in range(_NT - 1, -1, -1):
        acc = _INVF[j] + r * acc
    acc = IV(dn(acc.lo - _REM), up(acc.hi + _REM))
    ki = k.astype(np.int64)
    return IV(np.ldexp(acc.lo, ki), np.ldexp(acc.hi, ki))   # exact scaling, no overflow for |x| <= 700


def itanh_pt(z):
    """rigorous enclosure of tanh at float points z"""
    z = np.asarray(z, dtype=np.float64)
    a = np.minimum(np.abs(z), 300.0)
    E = iexp_pt(2.0 * a)
    T = IV(1.0) - IV(2.0) / (E + IV(1.0))                 # tanh(a), a >= 0
    big = np.abs(z) >= 300.0
    lo = np.where(big, 1.0 - 1e-200, np.maximum(T.lo, 0.0))
    hi = np.where(big, 1.0, np.minimum(T.hi, 1.0))
    neg = z < 0
    return IV(np.where(neg, -hi, lo), np.where(neg, -lo, hi))


def tanh_lin(l, t):
    """alpha, beta, delta (float arrays) with |tanh(s) - alpha s - beta| <= delta on [l, t]."""
    l = np.asarray(l, dtype=np.float64); t = np.asarray(t, dtype=np.float64)
    Tl, Tt = itanh_pt(l), itanh_pt(t)
    w = t - l
    with np.errstate(all="ignore"):
        alpha = np.where(w > 0, (0.5 * (Tt.lo + Tt.hi) - 0.5 * (Tl.lo + Tl.hi)) / np.where(w > 0, w, 1.0), 0.0)
    alpha = np.clip(np.nan_to_num(alpha, nan=0.0), 0.0, 1.0)
    with np.errstate(all="ignore"):
        s0 = np.where((alpha > 0) & (alpha < 1), np.arccosh(1.0 / np.sqrt(np.where((alpha > 0) & (alpha < 1), alpha, 0.5))), 0.0)
    eps = 1e-7 * (np.abs(s0) + 1e-3)
    brk = [l, t, np.clip(0.0, l, t)]
    for c in (-s0 - eps, -s0 + eps, s0 - eps, s0 + eps):
        brk.append(np.clip(c, l, t))
    B = np.sort(np.stack(brk, axis=0), axis=0)                   # (7, ...)
    TB = itanh_pt(B)
    A = IV(alpha)
    gmin = np.full(l.shape, INF); gmax = np.full(l.shape, -INF)
    for q in range(B.shape[0] - 1):
        a, b = B[q], B[q + 1]
        Ta, Tb = IV(TB.lo[q], TB.hi[q]), IV(TB.lo[q + 1], TB.hi[q + 1])
        Ga = Ta - A * IV(a); Gb = Tb - A * IV(b)
        dGa = (IV(1.0) - Ta * Ta) - A
        dGb = (IV(1.0) - Tb * Tb) - A
        # (Ta*Ta as a product of intervals is a valid, slightly wide, enclosure of tanh^2)
        one_side = (a >= 0) | (b <= 0)
        mono = one_side & (((dGa.lo >= 0) & (dGb.lo >= 0)) | ((dGa.hi <= 0) & (dGb.hi <= 0)))
        lo_m = np.minimum(Ga.lo, Gb.lo); hi_m = np.maximum(Ga.hi, Gb.hi)
        crude_lo = (Ta - A * IV(b)).lo; crude_hi = (Tb - A * IV(a)).hi
        plo = np.where(mono, lo_m, crude_lo); phi = np.where(mono, hi_m, crude_hi)
        gmin = np.minimum(gmin, plo); gmax = np.maximum(gmax, phi)
    beta = 0.5 * (gmin + gmax)
    delta = up(np.maximum(up(gmax - beta), up(beta - gmin)))
    return alpha, beta, delta


# ----------------------------------------------------------------------------- model
class Model:
    def __init__(self):
        D = annv.decode()
        self.D = D
        N = D["N"]
        self.N = N
        self.nv = len(N)
        self.inputs = D["inputs"]
        self.box = D["box"]
        self.lo0 = np.array([fiv(a)[0] for a, b in D["box"]])
        self.hi0 = np.array([fiv(b)[1] for a, b in D["box"]])
        level = {j: 0 for j in self.inputs}
        for op in D["ops"]:
            if op[0] == "lin":
                level[op[1]] = 1 + max([level[o] for o, a in op[3]], default=0)
            else:
                level[op[1]] = 1 + level[op[2]]
        L = max(level.values())
        tanh_ops = [op for op in D["ops"] if op[0] == "tanh"]
        self.sym = {op[1]: 5 + q for q, op in enumerate(tanh_ops)}   # symbol of each tanh neuron
        self.K = 5 + len(tanh_ops)
        self.levels = []
        for lv in range(1, L + 1):
            lin = [op for op in D["ops"] if op[0] == "lin" and level[op[1]] == lv]
            th = [op for op in D["ops"] if op[0] == "tanh" and level[op[1]] == lv]
            ent = {}
            if lin:
                rows, cols, vals, bs, tv = [], [], [], [], []
                for r_, op in enumerate(lin):
                    _, v, cv, terms, rhs = op
                    tv.append(v)
                    for o, a in terms:
                        rows.append(r_); cols.append(o); vals.append(float(-a / cv))   # correctly rounded
                    bs.append(float(rhs / cv))
                W = sp.csr_matrix((vals, (rows, cols)), shape=(len(lin), self.nv))
                kmax = max(len(op[3]) for op in lin)
                assert kmax + 2 < 1000
                ent["lin"] = dict(tv=np.array(tv), W=W, Wa=abs(W), b=np.array(bs)[:, None])
            if th:
                ent["tanh"] = dict(tv=np.array([op[1] for op in th]), zv=np.array([op[2] for op in th]),
                                   sym=np.array([self.sym[op[1]] for op in th]))
            self.levels.append(ent)
        # objective terms
        self.const = float(D["const"])
        self.lin = [(j, float(a)) for j, a in D["lin"].items()]
        self.bil = [(p, r, float(a)) for (p, r), a in D["bil"].items()]
        # constraint sides: (j, s, b_lo, b_hi) meaning s*(x_j - b) >= 0 for the exact b in [b_lo, b_hi]
        sides = []
        for j, lo, hi in D["cb"]:
            if lo is not None:
                sides.append((j, 1.0) + fiv(lo))
            if hi is not None:
                sides.append((j, -1.0) + fiv(hi))
        self.sd_j = np.array([s[0] for s in sides]); self.sd_s = np.array([s[1] for s in sides])
        self.sd_blo = np.array([s[2] for s in sides]); self.sd_bhi = np.array([s[3] for s in sides])

    # ---------------- affine forward pass
    def forward(self, lo, hi):
        Nb = lo.shape[0]
        K = self.K
        m = 0.5 * (lo + hi)
        h = up(np.maximum(up(hi - m), up(m - lo)))
        assert np.all(m - h <= lo) and np.all(m + h >= hi)
        C = np.zeros((self.nv, Nb)); A = np.zeros((self.nv, Nb, K)); R = np.zeros((self.nv, Nb)); S = np.zeros((self.nv, Nb))
        for i, j in enumerate(self.inputs):
            C[j] = m[:, i]; A[j, :, i] = h[:, i]; S[j] = h[:, i]
        for ent in self.levels:
            if "lin" in ent:
                E = ent["lin"]
                tv = E["tv"]
                # exact: x_v = sum w x_o + b.  stored C, A: float results; error of each float dot
                # product <= gamma_{k+1} * (sum |w||.|); representation errors of w, b <= u relative.
                Wa = E["Wa"]
                Rn = Wa @ R + TAU * (Wa @ (np.abs(C) + S + R) + np.abs(E["b"]))
                C[tv] = E["W"] @ C + E["b"]
                A[tv] = (E["W"] @ A.reshape(self.nv, Nb * K)).reshape(len(tv), Nb, K)
                R[tv] = up(Rn * (1 + TAU) + TINY)
                S[tv] = up(np.abs(A[tv]).sum(axis=2) * (1 + TAU) + TINY)
            if "tanh" in ent:
                T = ent["tanh"]
                tv, zv, sym = T["tv"], T["zv"], T["sym"]
                Cz, Az, Rz, Sz = C[zv], A[zv], R[zv], S[zv]
                assert np.all(Az[np.arange(len(tv)), :, sym] == 0)
                w = up((Sz + Rz) * (1 + TAU) + TINY)
                zl, zu = dn(Cz - w), up(Cz + w)
                alpha, beta, delta = tanh_lin(zl, zu)
                C[tv] = alpha * Cz + beta
                An = alpha[:, :, None] * Az
                An[np.arange(len(tv)), :, sym] = delta
                A[tv] = An
                # exact: tanh(z) = alpha (Cz + Az.xi + rho) + beta + delta*eta; rounding of alpha*Cz + beta
                # <= 2u(|alpha Cz| + |beta|), of alpha*Az_i <= u alpha |Az_i|
                Rn = alpha * Rz + TAU * (alpha * np.abs(Cz) + np.abs(beta) + alpha * Sz)
                R[tv] = up(Rn * (1 + TAU) + TINY)
                S[tv] = up(np.abs(An).sum(axis=2) * (1 + TAU) + TINY)
        return m, h, C, A, R, S

    def objective(self, C, A, R, S):
        """affine form of f: Cf (Nb,), Af (Nb, K), Rf (Nb,)."""
        Nb = C.shape[1]
        terms = []   # (coef, Ct, At, Rt, St)
        for j, a in self.lin:
            terms.append((a, C[j], A[j], R[j], S[j]))
        for p, r, a in self.bil:
            Cp, Ap, Rp, Sp = C[p], A[p], R[p], S[p]
            Cr, Ar, Rr, Sr = C[r], A[r], R[r], S[r]
            xy = Ap * Ar
            Dsum = xy.sum(axis=1)
            E = np.abs(xy).sum(axis=1)
            Ct = Cp * Cr + 0.5 * Dsum
            At = Cp[:, None] * Ar + Cr[:, None] * Ap
            # (Ap.xi)(Ar.xi) = 1/2 D + N, |N| <= Sp Sr - 1/2 E  (xi_i^2 in [0, 1])
            nl = np.maximum(Sp * Sr * (1 + TAU) - 0.5 * E * (1 - TAU), 0.0)
            # remainder products and rounding of Ct, At (generous TAU)
            Rt = (nl + Rr * (np.abs(Cp) + Sp) + Rp * (np.abs(Cr) + Sr) + Rp * Rr
                  + TAU * (np.abs(Cp * Cr) + E + np.abs(Cp) * Sr + np.abs(Cr) * Sp))
            Rt = up(Rt * (1 + TAU) + TINY)
            St = up(np.abs(At).sum(axis=1) * (1 + TAU) + TINY)
            terms.append((a, Ct, At, Rt, St))
        Cf = np.full(Nb, self.const)
        Af = np.zeros((Nb, self.K))
        Rf = np.zeros(Nb)
        for a, Ct, At, Rt, St in terms:
            Cf = Cf + a * Ct
            Af = Af + a * At
            Rf = Rf + abs(a) * Rt + TAU * abs(a) * (np.abs(Ct) + St + Rt)
        Rf = up((Rf + TAU * abs(self.const)) * (1 + TAU) + TINY)
        return Cf, Af, Rf

    # ---------------- bound
    def bound(self, lo, hi, want_lp=True, target=None):
        """rigorous lower bounds of f over R intersected with each box; +inf if proved infeasible.
        With a target, the LP is skipped on boxes whose plain bound already reaches it."""
        lo = np.atleast_2d(lo); hi = np.atleast_2d(hi)
        Nb = lo.shape[0]
        m, h, C, A, R, S = self.forward(lo, hi)
        Cf, Af, Rf = self.objective(C, A, R, S)
        # plain bound (no constraints): Cf - Rf - |Af|_1
        Sf = up(np.abs(Af).sum(axis=1) * (1 + TAU) + TINY)
        plain = dn(dn(Cf - Rf) - Sf)
        j, s = self.sd_j, self.sd_s
        Cs, Rs, Ss = C[j], R[j], S[j]                      # (ns, Nb)
        bmid = np.where(s > 0, self.sd_blo, self.sd_bhi)   # float b for the LP
        # rigorous q_j = s (C_j - b) + r_j  (upper and lower float bounds)
        qI = IV(s[:, None]) * (IV(Cs) - IV(self.sd_blo[:, None], self.sd_bhi[:, None])) + IV(Rs)
        # side can hold somewhere only if q_hi + S_j >= 0 ... (s A.xi >= -q on feasible points; max s A.xi <= S)
        infeas_single = np.any(up(qI.hi + Ss) < 0, axis=0)
        # side redundant if s A.xi + (s(C-b) - r) >= 0 for all xi: s(C-b) - r - S >= 0
        qlow = (IV(s[:, None]) * (IV(Cs) - IV(self.sd_blo[:, None], self.sd_bhi[:, None])) - IV(Rs)).lo
        active = dn(qlow - Ss) < 0
        out = np.array(plain)
        info = []
        for n in range(Nb):
            if infeas_single[n]:
                out[n] = INF
                info.append(("infeasible-single", 0))
                continue
            if not want_lp or (target is not None and plain[n] >= target):
                info.append(("plain", 0)); continue
            act = np.nonzero(active[:, n])[0]
            if len(act) == 0:
                info.append(("no-active", 0)); continue
            # LP: min Af.xi  s.t.  -s A_j.xi <= s (C_j - b) + r_j
            Aub = -(s[act, None] * A[j[act], n, :])
            bub = s[act] * (Cs[act, n] - bmid[act]) + Rs[act, n]
            res = linprog(Af[n], A_ub=Aub, b_ub=bub, bounds=[(-1, 1)] * self.K, method="highs")
            if res.status == 0:
                mu = np.maximum(-res.ineqlin.marginals, 0.0)
                kind = "lp"
            elif res.status == 2:
                # elastic LP: min Af.xi + P sum t  s.t. -s A_j.xi - t_j <= q_j, t >= 0
                P = 1e8
                na = len(act)
                Aub2 = np.hstack([Aub, -np.eye(na)])
                c2 = np.concatenate([Af[n], np.full(na, P)])
                res = linprog(c2, A_ub=Aub2, b_ub=bub, bounds=[(-1, 1)] * self.K + [(0, None)] * na, method="highs")
                if res.status != 0:
                    info.append(("lp-fail", res.status)); continue
                mu = np.maximum(-res.ineqlin.marginals, 0.0)
                kind = "elastic"
            else:
                info.append(("lp-fail", res.status)); continue
            val = self.dual_value(n, act, mu, Cf, Af, Rf, C, A, R)
            out[n] = max(out[n], val)
            info.append((kind, len(act)))
        return out, info, plain

    def dual_value(self, n, act, mu, Cf, Af, Rf, C, A, R):
        """rigorous: Cf - Rf - sum mu_j (s(C_j - b) + r_j) - || Af - sum mu_j s A_j ||_1  (box n)."""
        j, s = self.sd_j[act], self.sd_s[act]
        keep = mu > 0
        j, s, mu = j[keep], s[keep], mu[keep]
        blo, bhi = self.sd_blo[act][keep], self.sd_bhi[act][keep]
        acc = IV(Cf[n]) - IV(Rf[n])
        g = IV(Af[n])
        for q in range(len(j)):
            M = IV(mu[q])
            qv = IV(s[q]) * (IV(C[j[q], n]) - IV(blo[q], bhi[q])) + IV(R[j[q], n])
            acc = acc - M * qv
            g = g - (M * IV(s[q])) * IV(A[j[q], n, :])
        mag = np.maximum(np.abs(g.lo), np.abs(g.hi))
        tot = up(mag.sum() * (1 + TAU) + TINY)
        return float(dn(acc.lo - tot))

    # ---------------- small branch and bound on one box
    def prove(self, lo, hi, target, max_nodes=2000, batch=16):
        """try to prove f >= target on R intersected with [lo, hi]; returns (ok, nodes, min bound of
        the leaves that fell short (or +inf), min leaf bound overall)."""
        W0 = self.hi0 - self.lo0
        stack_lo = [np.asarray(lo, float)]; stack_hi = [np.asarray(hi, float)]
        nodes = 0
        worst = INF
        while stack_lo:
            if nodes >= max_nodes:
                blo = np.array(stack_lo); bhi = np.array(stack_hi)
                lb, _, _ = self.bound(blo, bhi)
                return False, nodes, float(lb.min()), worst
            k = min(batch, len(stack_lo))
            blo = np.array(stack_lo[-k:]); bhi = np.array(stack_hi[-k:])
            del stack_lo[-k:]; del stack_hi[-k:]
            lb, _, _ = self.bound(blo, bhi, target=target)
            nodes += k
            for q in range(k):
                if lb[q] >= target:
                    worst = min(worst, lb[q])
                    continue
                w = (bhi[q] - blo[q]) / W0
                d = int(np.argmax(w))
                if bhi[q][d] - blo[q][d] <= 1e-13 * max(1.0, abs(blo[q][d])):
                    return False, nodes, float(lb[q]), worst
                mid = 0.5 * (blo[q][d] + bhi[q][d])
                l1, h1 = blo[q].copy(), bhi[q].copy(); h1[d] = mid
                l2, h2 = blo[q].copy(), bhi[q].copy(); l2[d] = mid
                stack_lo += [l1, l2]; stack_hi += [h1, h2]
        return True, nodes, INF, worst


# ----------------------------------------------------------------------------- float / 50-digit evaluation
_FM = None


def float_model():
    global _FM
    if _FM is None:
        _FM = annv.FloatModel(annv.decode())
    return _FM


def mp_eval(D, u, dps=50):
    """f and the minimum slack of the R constraints at the float input u, at dps digits."""
    with mp.workdps(dps):
        x = annv.forward_mp(D, [mp.mpf(float(v)) for v in u])
        f = annv.fobj(D, x, lambda q: mp.mpf(q.numerator) / q.denominator)
        sl = mp.inf
        for j, lo, hi in D["cb"]:
            if lo is not None:
                sl = min(sl, x[j] - mp.mpf(lo.numerator) / lo.denominator)
            if hi is not None:
                sl = min(sl, mp.mpf(hi.numerator) / hi.denominator - x[j])
        inbox = all(mp.mpf(a.numerator) / a.denominator <= mp.mpf(float(v)) <= mp.mpf(b.numerator) / b.denominator
                    for v, (a, b) in zip(u, D["box"]))
        return f, sl, inbox
