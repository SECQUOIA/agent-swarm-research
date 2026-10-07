"""ann_cumene_tanh: rigorous per-box lower bounds from first-order Taylor models
(affine arithmetic) and a per-box LP dual over linearized constraints, with
domain reduction, inside a best-first branch and bound over the 5 inputs.
Extension of ann_fast.py (see extension.md in this directory).

Classes: TMModel (5 input noise symbols, all linearization errors lumped into
one remainder per variable) and SepModel (additionally one noise symbol per
tanh neuron, 250 in total; used for the reported runs).

    python3 ann_tm.py tol_rel time_limit_s save.npz|- model [resume.npz]
model: sep-gradsmall (reported runs), sep-nofull, sep, sep-hybrid, sepfast,
sep-tmsmear, sep-nofull-tmsmear, tm (TMModel).

Notation.  A box [lo, hi] of the 5 inputs is written u = m + h*eps with
eps in [-1, 1]^5, m = fl((lo+hi)/2) and h >= max(hi-m, m-lo) rounded up, so the
eps-cube covers the box.  A Taylor model (TM) of a variable is (c, a, r) with
arrays c (N,), a (N, 5), r (N,), meaning
    x(eps) in [c + a.eps - r, c + a.eps + r]   for every eps in [-1, 1]^5,
where c + a.eps is evaluated exactly from the stored doubles.  Every rounding
error of the float computations is added to r (bounds below).

Linear rows (exact rationals W, b; W in wm +- wr, b in bm +- br by frac_iv):
    c' = fl(wm c + bm),  a' = fl(wm a),
    r' = |wm| r + wr (|c| + S + r) + br + g_{k+1} (|wm| (|c| + S) + |bm|),
S = sum_i |a_i| (rounded up), k = nonzeros per row, g_n = n u/(1 - n u).  The
computed r' is a sum of nonnegative floating-point products and is inflated by
(1 + g_{2k+20}) plus 1e-300.

tanh rows: on the range [l, t] of the argument TM, tanh(s) = alpha s + g(s) with
g(s) = tanh(s) - alpha s.  g is convex on s <= 0 and concave on s >= 0 (tanh is),
so on each piece the maximum (convex piece) or minimum (concave piece) is at an
end point, and the other extreme is bounded by the tangent line at any point p
of the piece: g(s) >= g(p) + g'(p)(s - p) on a convex piece, <= on a concave
piece.  p is chosen near the stationary point (float arccosh; any p is valid).
All values tanh(s), g, g' at float points are enclosed by the rigorous
table-exp tanh of ann_bb (no libm result is trusted).  Two slopes are tried
(chord slope and min-range slope) and the one with the smaller half-width
delta is kept.  Output TM: c' = fl(alpha c + beta), a' = fl(alpha a),
r' = |alpha| r + delta + g_2 (|alpha c| + |beta|) + u |alpha| S, inflated.

Products (objective): tm1.TM (the product rule reviewed for pindyck).

Per-box lower bound.  f(eps) >= c_f + a_f.eps - r_f.  Each bound x_j >= b
(resp. x_j <= b) of a determined variable gives, on feasible eps, the linear
inequality s a_j.eps >= beta_j with beta_j = s(b - c_j) - r_j rounded down
(s = +1 / -1).  For any multipliers mu >= 0 (weak duality over the eps-cube)
    f >= c_f - r_f + sum_j mu_j beta_j - || a_f - sum_j mu_j s_j a_j ||_1
on every feasible point of the box.  mu is chosen by enumerating the vertices
of the dual LP restricted to the (at most MSEL) sides most violated at the
unconstrained minimizer; the value is then evaluated in outward-rounded
interval arithmetic, so any mu (even a poor one) gives a valid bound.  A box is
infeasible if one side has beta_j > ||a_j||_1, or if for mu >= 0 with sum 1,
sum mu_j beta_j > ||sum mu_j s_j a_j||_1 (Farkas over the cube).

Domain reduction: the linear inequalities of all sides and the cut
a_f.eps <= UB - c_f + r_f (points with f > UB cannot improve the incumbent and
are not needed for a lower bound below UB) shrink the eps-box by interval
propagation over one inequality at a time (two rounds); the LP and the
infeasibility tests use the reduced eps-box; if a coordinate shrinks below 70%
the reduced box is mapped back to u with outward rounding and re-queued.

SepModel: x = c + a.eps + e.eta + rho with |rho| <= r and one eta_n in [-1, 1]
per tanh neuron, shared by all variables; the LP uses lumped remainders
(r + sum|e|) to choose mu, and the bound is also evaluated at that mu with the
eta terms combined (sum_n |e_f,n - sum_j mu_j s_j e_j,n|); the larger value is
kept.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import itertools
import sys
import time

import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/kan")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
import kan_iv as K  # noqa: E402
from kan_iv import NI, dn, up  # noqa: E402
import tm1  # noqa: E402

import ann_bb as ab  # noqa: E402
import ann_fast as af  # noqa: E402

INF = np.inf
U = 2.0 ** -53
D5 = 5
tm1.M[0] = D5


def gam(n):
    return n * U / (1 - n * U)


def upos(x):
    """upper bound for a nonnegative float sum of a few terms (<= 64 terms, 1 op each)"""
    return up(x * (1 + gam(128)) + 1e-300)


def usum(x, axis):
    """upper bound of the exact sum of the nonnegative floats x along axis (any summation order:
    relative error <= gamma_{n-1})"""
    n = x.shape[axis]
    return up(x.sum(axis=axis) * (1 + gam(n + 2)) + 1e-300)


# ----------------------------------------------------------------------------- tanh
def _tanh_ni(p):
    return ab.tanh_pt(p)


def _g_ni(p, alpha):
    """enclosures of g(p) = tanh(p) - alpha p and g'(p) = 1 - tanh(p)^2 - alpha at float points p."""
    T = _tanh_ni(p)
    A = NI(alpha)
    G = T - A * NI(p)
    dG = (NI(1.0) - ab.isq(T)) - A
    return G, dG


def _g_range(alpha, lo, hi, Glo, Ghi):
    """rigorous [gmin, gmax] of g = tanh - alpha s on [lo, hi] (arrays).  Glo/Ghi: NI of g at lo/hi."""
    has_neg = lo < 0
    has_pos = hi > 0
    # convex piece [lo, min(hi, 0)], concave piece [max(lo, 0), hi]
    a1, b1 = lo, np.minimum(hi, 0.0)
    a2, b2 = np.maximum(lo, 0.0), hi
    with np.errstate(all="ignore"):
        sc = np.where((alpha > 0) & (alpha < 1), np.arccosh(1.0 / np.sqrt(np.where((alpha > 0) & (alpha < 1), alpha, 0.5))), 0.0)
    p1 = np.clip(-sc, a1, b1)
    p2 = np.clip(sc, a2, b2)
    G1, dG1 = _g_ni(p1, alpha)
    G2, dG2 = _g_ni(p2, alpha)
    # g at the piece end points: at lo/hi from Glo/Ghi, at 0 exactly 0
    g_b1_lo = np.where(hi <= 0, Ghi.lo, 0.0)
    g_b1_hi = np.where(hi <= 0, Ghi.hi, 0.0)
    g_a2_lo = np.where(lo >= 0, Glo.lo, 0.0)
    g_a2_hi = np.where(lo >= 0, Glo.hi, 0.0)
    # convex piece: max at end points; min >= tangent at p1
    cmax = np.maximum(Glo.hi, g_b1_hi)
    t1 = (G1 + dG1 * (NI(a1) - NI(p1))).lo
    t2 = (G1 + dG1 * (NI(b1) - NI(p1))).lo
    cmin = np.minimum(t1, t2)
    # concave piece: min at end points; max <= tangent at p2
    kmin = np.minimum(g_a2_lo, Ghi.lo)
    t3 = (G2 + dG2 * (NI(a2) - NI(p2))).hi
    t4 = (G2 + dG2 * (NI(b2) - NI(p2))).hi
    kmax = np.maximum(t3, t4)
    gmin = np.minimum(np.where(has_neg, cmin, INF), np.where(has_pos, kmin, INF))
    gmax = np.maximum(np.where(has_neg, cmax, -INF), np.where(has_pos, kmax, -INF))
    # degenerate lo == hi == 0
    z = ~has_neg & ~has_pos
    gmin = np.where(z, 0.0, gmin)
    gmax = np.where(z, 0.0, gmax)
    return gmin, gmax


def tanh_lin(lo, hi):
    """alpha, beta, delta with tanh(s) in alpha s + beta +- delta for s in [lo, hi] (arrays)."""
    Tl, Th = _tanh_ni(lo), _tanh_ni(hi)
    w = hi - lo
    with np.errstate(all="ignore"):
        chord = np.where(w > 0, (0.5 * (Th.lo + Th.hi) - 0.5 * (Tl.lo + Tl.hi)) / np.where(w > 0, w, 1.0), 0.0)
    dl = (NI(1.0) - ab.isq(Tl)).lo
    dh = (NI(1.0) - ab.isq(Th)).lo
    chord = np.where(w > 0, chord, 1.0 - (0.5 * (Tl.lo + Tl.hi)) ** 2)
    chord = np.clip(chord, 0.0, 1.0)
    minr = np.clip(np.minimum(dl, dh), 0.0, 1.0)
    best = None
    for alpha in (chord, minr):
        A = NI(alpha)
        Glo = Tl - A * NI(lo)
        Ghi = Th - A * NI(hi)
        if alpha is minr:
            # alpha <= min of tanh' on [lo, hi] (tanh' is unimodal, so its minimum is at an end point):
            # g = tanh - alpha s is nondecreasing, g in [g(lo), g(hi)]
            gmin, gmax = Glo.lo, Ghi.hi
        else:
            gmin, gmax = _g_range(alpha, lo, hi, Glo, Ghi)
        beta = 0.5 * (gmin + gmax)
        delta = up(np.maximum(up(gmax - beta), up(beta - gmin)))
        if best is None:
            best = [alpha, beta, delta]
        else:
            s = delta < best[2]
            best = [np.where(s, alpha, best[0]), np.where(s, beta, best[1]), np.where(s, delta, best[2])]
    return best


# ----------------------------------------------------------------------------- model
class TMModel(af.FastModel):
    MSEL = 3

    def __init__(self):
        super().__init__()
        N = self.D["names"]
        tanh_out = {op[1] for op in self.D["ops"] if op[0] == "tanh"}
        # constraint sides that can bind: finite bounds of magnitude < 1e5 on non-tanh variables
        sides = []
        for j in self.cons_idx:
            if j in tanh_out:
                continue
            lo, hi = self.cb[j]
            if lo is not None and abs(lo) < 1e5:
                sides.append((int(j), +1, K.frac_iv(lo)[0]))      # x_j >= lo (lower float of lo)
            if hi is not None and abs(hi) < 1e5:
                sides.append((int(j), -1, K.frac_iv(hi)[1]))      # x_j <= hi (upper float of hi)
        self.sides = sides
        self.side_var = np.array([s[0] for s in sides])
        self.side_sgn = np.array([float(s[1]) for s in sides])
        self.side_b = np.array([s[2] for s in sides])
        # groups of identical variables (same float value at random points): used only to avoid
        # selecting duplicate sides in the LP (dropping constraints is always a relaxation)
        rng = np.random.default_rng(5)
        P = self.lo_in + (self.hi_in - self.lo_in) * rng.random((4, 5))
        vals = []
        for p in P:
            _, _, X, _ = self.ffun(p)
            vals.append([X[j] for j in self.side_var])
        vals = np.array(vals).T
        key = [tuple(np.round(v, 12)) + (s,) for v, s in zip(vals, self.side_sgn)]
        first = {}
        self.side_rep = np.array([first.setdefault(k, i) == i for i, k in enumerate(key)])
        self.names = N
        self.lag_fixed = None
        # clipping data per level (finite bounds of non-input variables; outer float bounds)
        self.clip = True
        self.clip_frac = 0.25
        lvl_of = {}
        for li, ent in enumerate(self.levels):
            for key in ("lin", "tanh"):
                if key in ent:
                    for v in ent[key]["tv"]:
                        lvl_of[int(v)] = li
        byl = {}
        for j, blo, bhi in zip(self.cons_idx, self.cons_lo[:, 0], self.cons_hi[:, 0]):
            if int(j) in tanh_out:
                continue
            if np.isfinite(blo) or np.isfinite(bhi):
                byl.setdefault(lvl_of[int(j)], []).append((int(j), blo, bhi))
        self.clip_by_level = {li: (np.array([t[0] for t in L]), np.array([t[1] for t in L])[:, None],
                                   np.array([t[2] for t in L])[:, None]) for li, L in byl.items()}

    # ---------------- TM forward pass
    def _tm_affine(self, E, C, A, R, with_b=True):
        n_used, Nb = C.shape
        S = upos(np.abs(A).sum(axis=2))
        Cn = E["Wm"] @ C
        if with_b:
            Cn = Cn + E["bm"]
        An = (E["Wm"] @ A.reshape(n_used, -1)).reshape(-1, Nb, D5)
        absC = np.abs(C)
        g1 = gam(E["k"] + 1)
        Rn = E["Wa"] @ R + E["Wr"] @ (absC + S + R) + g1 * (E["Wa"] @ (absC + S))
        if with_b:
            Rn = Rn + E["br"] + g1 * np.abs(E["bm"])
        Rn = up(Rn * (1 + gam(2 * E["k"] + 20)) + 1e-300)
        return Cn, An, Rn

    def _tm_tanh(self, C, A, R):
        S = upos(np.abs(A).sum(axis=2))
        w = upos(S + R)
        lo = dn(C - w)
        hi = up(C + w)
        alpha, beta, delta = tanh_lin(lo, hi)
        Cn = alpha * C + beta
        An = alpha[:, :, None] * A
        Rn = alpha * R + delta + gam(2) * (alpha * np.abs(C) + np.abs(beta)) + U * alpha * S
        Rn = up(Rn * (1 + gam(16)) + 1e-300)
        return Cn, An, Rn

    def tm_forward(self, lo, hi):
        Nb = lo.shape[0]
        m = 0.5 * (lo + hi)
        h = up(np.maximum(up(hi - m), up(m - lo)))
        C = np.zeros((self.nv, Nb))
        A = np.zeros((self.nv, Nb, D5))
        R = np.zeros((self.nv, Nb))
        for i, j in enumerate(self.inputs):
            C[j] = m[:, i]
            A[j, :, i] = h[:, i]
        for li, ent in enumerate(self.levels):
            if "lin" in ent:
                E = ent["lin"]
                u = E["used"]
                Cn, An, Rn = self._tm_affine(E, C[u], A[u], R[u])
                C[E["tv"]] = Cn; A[E["tv"]] = An; R[E["tv"]] = Rn
            if "tanh" in ent:
                T = ent["tanh"]
                Cn, An, Rn = self._tm_tanh(C[T["uv"]], A[T["uv"]], R[T["uv"]])
                C[T["tv"]] = Cn; A[T["tv"]] = An; R[T["tv"]] = Rn
            if self.clip:
                self._clip_level(li, C, A, R)
        return m, h, C, A, R

    def _clip_level(self, li, C, A, R):
        """On feasible points x_j lies in [cons_lo, cons_hi]; where the TM range sticks out and the
        constant enclosure of the intersection is narrower than the TM, use that constant TM
        (valid for every feasible eps; infeasible eps need no enclosure)."""
        sel = self.clip_by_level.get(li)
        if sel is None:
            return
        j, blo, bhi = sel
        S = upos(np.abs(A[j]).sum(axis=2))
        w = upos(S + R[j])
        lo = dn(C[j] - w); hi = up(C[j] + w)
        nlo = np.maximum(lo, blo); nhi = np.minimum(hi, bhi)
        ok = nlo <= nhi                               # empty: infeasible box, detected by the sides
        c2 = 0.5 * (nlo + nhi)
        r2 = up(np.maximum(up(nhi - c2), up(c2 - nlo)))
        use = ok & (r2 < self.clip_frac * w)
        C[j] = np.where(use, c2, C[j])
        R[j] = np.where(use, r2, R[j])
        A[j] = np.where(use[:, :, None], 0.0, A[j])

    def objective_tm(self, C, A, R):
        D = self.D
        X = {}

        def x(j):
            if j not in X:
                X[j] = tm1.TM(C[j], A[j], R[j])
            return X[j]

        def cq(q):
            lo_, hi_ = K.frac_iv(q)
            c = 0.5 * (lo_ + hi_)
            return tm1.TM.const(c, up(up(max(hi_ - c, c - lo_)) + abs(c) * 2 * U) + 1e-300)

        def P(key):
            if key == D["key793"]:
                v766, k792 = D["special793"]
                return x(v766) - P(k792)
            s = None
            for p, r, c in D["prod"][key]:
                t = (x(p) * x(r)) * cq(c)
                s = t if s is None else s + t
            return s
        f = cq(D["objconst"])
        for j, a in D["objlin"]:
            f = f + x(j) * cq(a)
        for key, c in D["objprod"]:
            f = f + P(key) * cq(c)
        return f

    # ---------------- per-box bound
    def lp_bound(self, cf, af_, rf, beta, at, avail, el, eu):
        """max over mu >= 0 of  sum mu beta + min_{eps in [el, eu]} (af - sum mu at).eps  over the MSEL
        sides most violated at the minimizer of af.eps; plus a Farkas infeasibility test.
        beta (S, N), at (S, N, d) (sign applied), avail (S, N) bool, el/eu (N, d).
        Returns rigorous lb (N,) (without cf - rf added? no: included), infeasible mask, mu, sel, use."""
        S_, Nb, d = at.shape
        ms = self.MSEL
        estar = np.where(af_ > 0, el, eu)                      # minimizer of af.eps over the eps-box
        viol = beta - np.einsum("snd,nd->sn", at, estar)
        viol = np.where(avail, viol, -INF)
        sel = np.argsort(-viol, axis=0)[:ms].T                 # (N, ms)
        nn = np.arange(Nb)[:, None]
        vs = viol[sel, nn]
        use = vs > 0
        B = np.where(use, beta[sel, nn], -1.0)                 # (N, ms)
        Aj = np.where(use[:, :, None], at[sel, nn], 0.0)       # (N, ms, d)
        cands = [np.zeros((Nb, ms))]
        rows = [(Aj[:, :, k], af_[:, k]) for k in range(d)]
        for j in range(ms):
            e = np.zeros((Nb, ms)); e[:, j] = 1.0
            rows.append((e, np.zeros(Nb)))
        for comb in itertools.combinations(range(len(rows)), ms):
            Mx = np.stack([rows[q][0] for q in comb], axis=1)
            rh = np.stack([rows[q][1] for q in comb], axis=1)
            cands.append(_solve_small(Mx, rh))
        mus = np.stack(cands, axis=1)                          # (N, nc, ms)
        mus = np.where(np.isfinite(mus), np.maximum(mus, 0.0), 0.0)
        g = af_[:, None, :] - np.einsum("ncj,njd->ncd", mus, Aj)
        val = np.einsum("ncj,nj->nc", mus, B) + np.where(g > 0, g * el[:, None, :], g * eu[:, None, :]).sum(axis=2)
        best = np.argmax(val, axis=1)
        mu = mus[np.arange(Nb), best]
        rows0 = [(Aj[:, :, k], np.zeros(Nb)) for k in range(d)] + [(np.eye(ms)[None, j].repeat(Nb, 0), np.zeros(Nb)) for j in range(ms)]
        fc = []
        for comb in itertools.combinations(range(len(rows0)), ms - 1):
            Mx = np.stack([rows0[q][0] for q in comb] + [np.ones((Nb, ms))], axis=1)
            rh = np.stack([rows0[q][1] for q in comb] + [np.ones(Nb)], axis=1)
            fc.append(_solve_small(Mx, rh))
        fmus = np.stack(fc, axis=1)
        fmus = np.where(np.isfinite(fmus), np.maximum(fmus, 0.0), 0.0)
        G = np.einsum("ncj,njd->ncd", fmus, Aj)
        fval = np.einsum("ncj,nj->nc", fmus, B) - np.where(G > 0, G * eu[:, None, :], G * el[:, None, :]).sum(axis=2)
        fmu = fmus[np.arange(Nb), np.argmax(fval, axis=1)]
        lb = _phi_rig(mu, B, Aj, af_, cf, rf, el, eu)
        finf = _farkas_rig(fmu, B, Aj, el, eu)
        return lb, finf, mu, sel, use

    def tmbound(self, lo, hi, UB=INF, fbbt_rounds=2):
        Nb = lo.shape[0]
        m, h, C, A, R = self.tm_forward(lo, hi)
        f = self.objective_tm(C, A, R)
        cf, af_, rf = f.c, f.a, f.r
        sv = self.side_var
        Cs, As, Rs = C[sv], A[sv], R[sv]                       # (S, N), (S, N, d), (S, N)
        sg = self.side_sgn[:, None]
        # beta = s (b - c) - r rounded down: every feasible eps satisfies at.eps >= beta
        beta = dn(dn(sg * (self.side_b[:, None] - Cs)) - Rs)
        at = sg[:, :, None] * As
        el = -np.ones((Nb, D5)); eu = np.ones((Nb, D5))
        infeas = np.zeros(Nb, bool)
        if fbbt_rounds > 0:
            # objective cut (points with f > UB are not needed): -af.eps >= cf - rf - UB
            b0 = dn(dn(cf - rf) - UB) if np.isfinite(UB) else np.full(Nb, -INF)
            Bf = np.concatenate([beta, b0[None]], axis=0)
            Af = np.concatenate([at, -af_[None]], axis=0)
            for _ in range(fbbt_rounds):
                el, eu, emp = _fbbt(Bf, Af, el, eu)
                infeas |= emp
                el = np.where(infeas[:, None], -1.0, el); eu = np.where(infeas[:, None], 1.0, eu)
        # single-side tests and redundancy on the (reduced) eps-box
        mx = _max_lin(at, el, eu)                              # upper bound of max at.eps
        mn = _min_lin(at, el, eu)                              # lower bound of min at.eps
        infeas |= np.any(beta > mx, axis=0)
        avail = (beta > mn) & self.side_rep[:, None]
        lb, finf, mu, sel, use = self.lp_bound(cf, af_, rf, beta, at, avail, el, eu)
        infeas |= finf
        lb = np.where(infeas, INF, lb)
        return dict(lb=lb, infeas=infeas, m=m, h=h, el=el, eu=eu, af=af_, mu=mu, sel=sel, use=use,
                    beta=beta, at=at, cf=cf, rf=rf)

    def reduced_box(self, lo, hi, m, h, el, eu):
        """u-box covering {m + h eps : eps in [el, eu]} intersected with [lo, hi] (outward rounded)."""
        nlo = dn(m + dn(h * el)); nhi = up(m + up(h * eu))
        # h*el: product of floats, dn/up of the rounded product bounds the exact product
        nlo = np.maximum(nlo, lo); nhi = np.minimum(nhi, hi)
        return nlo, np.maximum(nhi, nlo)

    def grad_only(self, lo, hi):
        """only the interval-gradient pass: natural enclosure of f (unclipped), infeasibility from the
        natural enclosures, and the gradient-width branching score."""
        Xlo, Xhi, Glo, Ghi, inf0 = self.fforward(lo, hi, grad=True)
        X, G = self._dicts(Xlo, Xhi, Glo, Ghi)
        fI, g = self.objective(X, G)
        Lf, Lg = self.lagr(X, fI, G, g)
        wL = np.maximum(Lg.hi - Lg.lo, 0.0)
        return dict(lb=fI.lo, infeas=inf0, ub=np.full(lo.shape[0], INF), wL=wL, Glo=Glo, Ghi=Ghi)

    def old_bounds(self, lo, hi):
        """interval bounds of ann_fast (natural with clipping, mean-value forms of f and of the
        Lagrangian with self.lag), the centre value, and the gradient-width branching score."""
        c = 0.5 * (lo + hi)
        Xclo, Xchi, _ = self.fforward(c, c, grad=False)
        Xc, _ = self._dicts(Xclo, Xchi)
        fc, _ = self.objective(Xc)
        Lc, _ = self.lagr(Xc, fc)
        Xlo, Xhi, Glo, Ghi, inf0 = self.fforward(lo, hi, grad=True)
        X, G = self._dicts(Xlo, Xhi, Glo, Ghi)
        fI, g = self.objective(X, G)
        Lf, Lg = self.lagr(X, fI, G, g)
        D_ = NI(dn(lo - c), up(hi - c))
        acc_f, acc_L = fc, Lc
        for i in range(D5):
            acc_f = acc_f + g[:, i] * D_[:, i]
            acc_L = acc_L + Lg[:, i] * D_[:, i]
        Xnlo, Xnhi, inf2 = self.fforward(lo, hi, grad=False, clip=True)
        Xn, _ = self._dicts(Xnlo, Xnhi)
        fn, _ = self.objective(Xn)
        lb_old = np.maximum(np.maximum(fn.lo, acc_f.lo), acc_L.lo)
        ci = self.cons_idx
        ok = np.all((Xclo[ci] >= self.cons_lo_in) & (Xchi[ci] <= self.cons_hi_in), axis=0)
        ok &= np.all((c >= self.lo_in) & (c <= self.hi_in), axis=1)
        ub = np.where(ok, fc.hi, INF)
        wL = np.maximum(Lg.hi - Lg.lo, 0.0)
        return dict(lb=lb_old, infeas=inf0 | inf2, ub=ub, wL=wL, Glo=Glo, Ghi=Ghi)

    def fbound_combo(self, lo, hi, UB, shrink=0.7):
        """max of the Taylor-model/LP bound (with domain reduction) and, on boxes wider than
        old_min_relw, the interval bounds of ann_fast.  Branching score: gradient-width score of the
        interval pass where it ran, otherwise the Taylor-model score."""
        Nb = lo.shape[0]
        T = self.tmbound(lo, hi, UB=UB)
        lb = T["lb"].copy()
        infeas = T["infeas"].copy()
        ub = np.full(Nb, INF)
        tiny = 1e-12 * (hi - lo) / (self.hi0 - self.lo0)
        if "smear_tm" in T:
            smear = np.where(np.isfinite(T["smear_tm"]), T["smear_tm"], 0.0) + tiny
        else:
            smear = np.abs(T["af"]) + tiny
        use_old = np.max((hi - lo) / (self.hi0 - self.lo0), axis=1) > getattr(self, "old_min_relw", -1.0)
        if not getattr(self, "old_pass", True):
            use_old[:] = False
        lb_old = np.full(Nb, -INF)
        passes = [(use_old, self.old_bounds)]
        if getattr(self, "grad_small", False):
            passes.append((~use_old & getattr(self, "old_pass", True), self.grad_only))
        for sel_pass, fn in passes:
            if not sel_pass.any():
                continue
            q = np.nonzero(sel_pass)[0]
            O = fn(lo[q], hi[q])
            lb_old[q] = O["lb"]
            infeas[q] |= O["infeas"]
            ub[q] = O["ub"]
            lb[q] = np.maximum(lb[q], O["lb"])
            if getattr(self, "smear_mode", "grad") != "tm":
                nq = np.arange(len(q))[:, None]
                jv = self.side_var[T["sel"][q]]
                wS = np.maximum(O["Ghi"][jv, nq] - O["Glo"][jv, nq], 0.0)
                wS = np.where(T["use"][q][:, :, None] & np.isfinite(wS), wS, 0.0)
                score = O["wL"] + np.einsum("nj,njd->nd", T["mu"][q], wS)
                score = np.where(np.isfinite(score), score, 1e300)
                smear[q] = score * (hi[q] - lo[q]) + tiny[q]
        lb = np.where(infeas, INF, lb)
        nlo, nhi = self.reduced_box(lo, hi, T["m"], T["h"], T["el"], T["eu"])
        frac = (nhi - nlo) / np.maximum(hi - lo, 1e-300)
        mod = np.any(frac < shrink, axis=1) & ~infeas
        return dict(lb=lb, ub=ub, x=0.5 * (lo + hi), smear=smear, newlo=nlo, newhi=nhi, mod=mod,
                    lb_tm=T["lb"], lb_old=np.where(infeas, INF, lb_old))


class SepModel(TMModel):
    """Taylor models with separate noise symbols for the linearization error of each tanh neuron
    (affine arithmetic): x = c + a.eps + e.eta + rho, |rho| <= r, where eta in [-1, 1]^250 is the
    SAME vector for all variables (eta_n = (tanh(z_n) - alpha_n z_n - beta_n)/delta_n).  Variables
    before the first tanh layer have e = 0; a first-layer tanh output has e = delta_n on its own
    symbol; later variables store e densely.  The rounding bounds are those of TMModel with S
    replaced by S = sum|a| + sum|e|."""

    def __init__(self):
        super().__init__()
        th = [li for li, ent in enumerate(self.levels) if "tanh" in ent]
        assert len(th) == 2
        self.t1, self.t2 = th
        self.t1_tv = np.array(self.levels[self.t1]["tanh"]["tv"])
        self.t2_tv = np.array(self.levels[self.t2]["tanh"]["tv"])
        self.NE = len(self.t1_tv) + len(self.t2_tv)
        self.full_mu = True
        self.ca_sweeps = 3
        self.old_pass = True
        self.old_min_relw = -1.0      # interval pass on boxes with max relative width above this
        self.col1 = {int(v): q for q, v in enumerate(self.t1_tv)}
        late = []
        for li, ent in enumerate(self.levels):
            if li <= self.t1:
                continue
            for key in ("lin", "tanh"):
                if key in ent:
                    late += [int(v) for v in ent[key]["tv"]]
        self.late_row = {v: q for q, v in enumerate(late)}
        self.n_late = len(late)
        # per linear level after t1: split of the used columns
        self.lvl_split = {}
        for li, ent in enumerate(self.levels):
            if li <= self.t1 or "lin" not in ent:
                continue
            E = ent["lin"]
            used = [int(v) for v in E["used"]]
            Wd = E["Wm"].toarray()
            p_t1 = [q for q, v in enumerate(used) if v in self.col1]
            p_lt = [q for q, v in enumerate(used) if v in self.late_row]
            self.lvl_split[li] = dict(
                W_t1=Wd[:, p_t1], c_t1=np.array([self.col1[used[q]] for q in p_t1], dtype=int),
                W_lt=E["Wm"][:, p_lt] if p_lt else None, r_lt=np.array([self.late_row[used[q]] for q in p_lt], dtype=int))

    def tm_forward(self, lo, hi):
        Nb = lo.shape[0]
        NE = self.NE
        m = 0.5 * (lo + hi)
        h = up(np.maximum(up(hi - m), up(m - lo)))
        C = np.zeros((self.nv, Nb)); A = np.zeros((self.nv, Nb, D5)); R = np.zeros((self.nv, Nb))
        SE = np.zeros((self.nv, Nb))                           # sum_n |e_n| (rounded up)
        Eb = np.zeros((self.n_late, Nb, NE))
        d1 = np.zeros((len(self.t1_tv), Nb))
        for i, j in enumerate(self.inputs):
            C[j] = m[:, i]
            A[j, :, i] = h[:, i]
        for li, ent in enumerate(self.levels):
            if "lin" in ent:
                Ed = ent["lin"]
                u = Ed["used"]; tv = Ed["tv"]
                Cn, An, Rn = self._tm_affine_s(Ed, C[u], A[u], R[u], SE[u])
                C[tv] = Cn; A[tv] = An; R[tv] = Rn
                if li > self.t1:
                    sp = self.lvl_split[li]
                    En = np.zeros((len(tv), Nb, NE))
                    if sp["W_lt"] is not None:
                        En += (sp["W_lt"] @ Eb[sp["r_lt"]].reshape(len(sp["r_lt"]), -1)).reshape(len(tv), Nb, NE)
                    if len(sp["c_t1"]):
                        En[:, :, sp["c_t1"]] += sp["W_t1"][:, None, :] * d1[sp["c_t1"]].T[None, :, :]
                    rows = np.array([self.late_row[int(v)] for v in tv])
                    Eb[rows] = En
                    SE[tv] = usum(np.abs(En), 2)
            if "tanh" in ent:
                T = ent["tanh"]
                uv, tv = T["uv"], T["tv"]
                Cu, Au, Ru, SEu = C[uv], A[uv], R[uv], SE[uv]
                S = upos(upos(np.abs(Au).sum(axis=2)) + SEu)
                w = upos(S + Ru)
                lo_, hi_ = dn(Cu - w), up(Cu + w)
                alpha, beta, delta = tanh_lin(lo_, hi_)
                attr = np.abs(Au) / np.maximum(w, 1e-300)[:, :, None]   # share of eps_k in the argument width
                if li == self.t1:
                    self._attr1 = attr
                else:
                    self._attr2 = attr
                C[tv] = alpha * Cu + beta
                A[tv] = alpha[:, :, None] * Au
                Rn = alpha * Ru + gam(2) * (alpha * np.abs(Cu) + np.abs(beta)) + U * alpha * S
                R[tv] = up(Rn * (1 + gam(16)) + 1e-300)
                if li == self.t1:
                    d1[:] = delta
                    SE[tv] = delta
                else:
                    rows_u = np.array([self.late_row[int(v)] for v in uv])
                    rows_t = np.array([self.late_row[int(v)] for v in tv])
                    En = alpha[:, :, None] * Eb[rows_u]
                    base = len(self.t1_tv)
                    for q in range(len(tv)):
                        En[q, :, base + q] += delta[q]
                    Eb[rows_t] = En
                    SE[tv] = usum(np.abs(En), 2)
            if self.clip:
                self._clip_level_s(li, C, A, R, SE, Eb)
        self._d1 = d1
        return m, h, C, A, R, SE, Eb

    def _tm_affine_s(self, E, C, A, R, SE, with_b=True):
        n_used, Nb = C.shape
        S = upos(upos(np.abs(A).sum(axis=2)) + SE)
        Cn = E["Wm"] @ C
        if with_b:
            Cn = Cn + E["bm"]
        An = (E["Wm"] @ A.reshape(n_used, -1)).reshape(-1, Nb, D5)
        absC = np.abs(C)
        g1 = gam(E["k"] + 1)
        Rn = E["Wa"] @ R + E["Wr"] @ (absC + S + R) + g1 * (E["Wa"] @ (absC + S))
        if with_b:
            Rn = Rn + E["br"] + g1 * np.abs(E["bm"])
        Rn = up(Rn * (1 + gam(2 * E["k"] + 20)) + 1e-300)
        return Cn, An, Rn

    def _clip_level_s(self, li, C, A, R, SE, Eb):
        sel = self.clip_by_level.get(li)
        if sel is None:
            return
        j, blo, bhi = sel
        S = upos(upos(np.abs(A[j]).sum(axis=2)) + SE[j])
        w = upos(S + R[j])
        lo = dn(C[j] - w); hi = up(C[j] + w)
        nlo = np.maximum(lo, blo); nhi = np.minimum(hi, bhi)
        ok = nlo <= nhi
        c2 = 0.5 * (nlo + nhi)
        r2 = up(np.maximum(up(nhi - c2), up(c2 - nlo)))
        use = ok & (r2 < self.clip_frac * w)
        if not use.any():
            return
        C[j] = np.where(use, c2, C[j])
        R[j] = np.where(use, r2, R[j])
        A[j] = np.where(use[:, :, None], 0.0, A[j])
        SE[j] = np.where(use, 0.0, SE[j])
        for q, v in enumerate(j):
            if int(v) in self.late_row and use[q].any():
                rr = self.late_row[int(v)]
                Eb[rr] = np.where(use[q][:, None], 0.0, Eb[rr])

    def efull(self, j, Nb, Eb):
        j = int(j)
        if j in self.late_row:
            return Eb[self.late_row[j]]
        e = np.zeros((Nb, self.NE))
        if j in self.col1:
            e[:, self.col1[j]] = self._d1[self.col1[j]]
        return e

    def objective_tm_s(self, C, A, R, Eb):
        Nb = C.shape[1]
        D = self.D
        X = {}
        tm1.M[0] = D5 + self.NE

        def x(j):
            if j not in X:
                X[j] = tm1.TM(C[j], np.concatenate([A[j], self.efull(j, Nb, Eb)], axis=1), R[j])
            return X[j]

        def cq(q):
            lo_, hi_ = K.frac_iv(q)
            c = 0.5 * (lo_ + hi_)
            return tm1.TM.const(c, up(up(max(hi_ - c, c - lo_)) + abs(c) * 2 * U) + 1e-300)

        def P(key):
            if key == D["key793"]:
                v766, k792 = D["special793"]
                return x(v766) - P(k792)
            s_ = None
            for p, r, c in D["prod"][key]:
                t = (x(p) * x(r)) * cq(c)
                s_ = t if s_ is None else s_ + t
            return s_
        f = cq(D["objconst"])
        for j, a in D["objlin"]:
            f = f + x(j) * cq(a)
        for key, c in D["objprod"]:
            f = f + P(key) * cq(c)
        tm1.M[0] = D5
        return f

    def tmbound(self, lo, hi, UB=INF, fbbt_rounds=2):
        Nb = lo.shape[0]
        m, h, C, A, R, SE, Eb = self.tm_forward(lo, hi)
        f = self.objective_tm_s(C, A, R, Eb)
        cf, rf = f.c, f.r
        af_ = f.a[:, :D5]
        ef = f.a[:, D5:]
        rfl = upos(rf + usum(np.abs(ef), 1))          # lumped remainder
        sv = self.side_var
        Cs, As, Rs, SEs = C[sv], A[sv], R[sv], SE[sv]
        sg = self.side_sgn[:, None]
        beta0 = dn(dn(sg * (self.side_b[:, None] - Cs)) - Rs)  # without the eta part
        beta = dn(beta0 - SEs)                                  # lumped
        at = sg[:, :, None] * As
        el = -np.ones((Nb, D5)); eu = np.ones((Nb, D5))
        infeas = np.zeros(Nb, bool)
        if fbbt_rounds > 0:
            b0 = dn(dn(cf - rfl) - UB) if np.isfinite(UB) else np.full(Nb, -INF)
            Bf = np.concatenate([beta, b0[None]], axis=0)
            Af = np.concatenate([at, -af_[None]], axis=0)
            for _ in range(fbbt_rounds):
                el, eu, emp = _fbbt(Bf, Af, el, eu)
                infeas |= emp
                el = np.where(infeas[:, None], -1.0, el); eu = np.where(infeas[:, None], 1.0, eu)
        mx = _max_lin(at, el, eu)
        mn = _min_lin(at, el, eu)
        infeas |= np.any(beta > mx, axis=0)
        avail = (beta > mn) & self.side_rep[:, None]
        lb_l, finf, mu, sel, use = self.lp_bound(cf, af_, rfl, beta, at, avail, el, eu)
        # refined value at the same mu with the eta terms combined (cancellation between f and sides)
        nn = np.arange(Nb)[:, None]
        B0 = np.where(use, beta0[sel, nn], -1.0)
        Aj = np.where(use[:, :, None], at[sel, nn], 0.0)
        Ej = np.zeros((Nb, self.MSEL, self.NE))
        for q in range(self.MSEL):
            for jj in np.unique(sv[sel[:, q]]):
                msk = (sv[sel[:, q]] == jj) & use[:, q]
                if msk.any():
                    Ej[msk, q] = self.efull(jj, Nb, Eb)[msk]
        Ej = Ej * self.side_sgn[sel][:, :, None]
        lb_s = _phi_rig_s(mu, B0, Aj, af_, cf, rf, el, eu, ef, Ej)
        lb = np.maximum(lb_l, lb_s)
        mu_f, sel_f, use_f, Ej_f, Aj_f = mu, sel, use, Ej, Aj
        if self.full_mu:
            # second selection by the violation without the eta part, multipliers by candidate
            # enumeration + exact coordinate ascent on the full dual function (eta terms included)
            estar = np.where(af_ > 0, el, eu)
            viol = beta0 - np.einsum("snd,nd->sn", at, estar)
            viol = np.where(avail, viol, -INF)
            sel2 = np.argsort(-viol, axis=0)[:self.MSEL].T
            use2 = viol[sel2, nn] > 0
            B02 = np.where(use2, beta0[sel2, nn], -1.0)
            Aj2 = np.where(use2[:, :, None], at[sel2, nn], 0.0)
            Ej2 = np.zeros((Nb, self.MSEL, self.NE))
            for q in range(self.MSEL):
                for jj in np.unique(sv[sel2[:, q]]):
                    msk = (sv[sel2[:, q]] == jj) & use2[:, q]
                    if msk.any():
                        Ej2[msk, q] = self.efull(jj, Nb, Eb)[msk]
            Ej2 = Ej2 * self.side_sgn[sel2][:, :, None]
            mu2 = _mu_full(B02, Aj2, af_, el, eu, ef, Ej2, sweeps=self.ca_sweeps)
            lb2 = _phi_rig_s(mu2, B02, Aj2, af_, cf, rf, el, eu, ef, Ej2)
            better = lb2 > lb
            lb = np.maximum(lb, lb2)
            mu_f = np.where(better[:, None], mu2, mu); sel_f = np.where(better[:, None], sel2, sel)
            use_f = np.where(better[:, None], use2, use)
            Ej_f = np.where(better[:, None, None], Ej2, Ej); Aj_f = np.where(better[:, None, None], Aj2, Aj)
        infeas |= finf
        lb = np.where(infeas, INF, lb)
        # branching score from the Taylor model: linear part of the final Lagrangian combination
        # (half-range per eps_k) plus the eta coefficients attributed to eps_k by each neuron's
        # share of its argument width
        g = af_ - np.einsum("nj,njd->nd", mu_f, Aj_f)
        coef = np.abs(ef - np.einsum("nj,njm->nm", mu_f, Ej_f))          # (N, NE)
        # add the fixed KKT Lagrangian (as the gradient-width score of the interval pass does)
        eL = ef.copy()
        for j, lam, bnd, sgn in self.lag:
            eL = eL - float(lam) * sgn * self.efull(j, Nb, Eb)
        coef = coef + np.abs(eL)
        attr = np.concatenate([self._attr1, self._attr2], axis=0)         # (NE, N, d)
        # (curvature part only: splitting along a direction of purely linear variation leaves the
        # lower child's bound unchanged)
        smear_tm = np.einsum("nm,mnd->nd", coef, attr)
        return dict(lb=lb, infeas=infeas, m=m, h=h, el=el, eu=eu, af=af_, mu=mu_f, sel=sel_f, use=use_f,
                    beta=beta, at=at, cf=cf, rf=rfl, rf_sep=rf, smear_tm=smear_tm)


def _phi_float(mu, B0, Aj, af_, el, eu, ef, Ej):
    """float value of the full dual function for candidate multipliers mu (N, nc, ms)."""
    g = af_[:, None, :] - np.einsum("ncj,njd->ncd", mu, Aj)
    h = ef[:, None, :] - np.einsum("ncj,njm->ncm", mu, Ej)
    return (np.einsum("ncj,nj->nc", mu, B0) + np.where(g > 0, g * el[:, None, :], g * eu[:, None, :]).sum(axis=2)
            - np.abs(h).sum(axis=2))


def _ca_1d(mu, j, B0, Aj, af_, el, eu, ef, Ej):
    """exact maximization over mu_j >= 0 of the concave piecewise-linear dual function."""
    Nb, ms = mu.shape
    oth = [i for i in range(ms) if i != j]
    g = af_ - np.einsum("nj,njd->nd", mu[:, oth], Aj[:, oth])
    hh = ef - np.einsum("nj,njm->nm", mu[:, oth], Ej[:, oth])
    A = Aj[:, j]; Ev = Ej[:, j]
    with np.errstate(all="ignore"):
        tk = np.where(A != 0, g / np.where(A != 0, A, 1.0), INF)
        tn = np.where(Ev != 0, hh / np.where(Ev != 0, Ev, 1.0), INF)
    sk = np.where((g > 0) | ((g == 0) & (A < 0)), -A * el, -A * eu)
    sn = np.where((hh > 0) | ((hh == 0) & (Ev < 0)), Ev, -Ev)
    s0 = B0[:, j] + sk.sum(axis=1) + sn.sum(axis=1)
    T = np.concatenate([tk, tn], axis=1)
    W = np.concatenate([np.abs(A) * (eu - el), 2 * np.abs(Ev)], axis=1)
    W = np.where(T > 0, W, 0.0); T = np.where(T > 0, T, INF)
    order = np.argsort(T, axis=1)
    Ts = np.take_along_axis(T, order, axis=1); Ws = np.take_along_axis(W, order, axis=1)
    cum = s0[:, None] - np.cumsum(Ws, axis=1)
    hit = cum <= 0
    has = hit.any(axis=1)
    idx = np.argmax(hit, axis=1)
    t_opt = Ts[np.arange(Nb), idx]
    fin = np.where(np.isfinite(Ts), Ts, 0.0).max(axis=1)
    t = np.where(s0 <= 0, 0.0, np.where(has & np.isfinite(t_opt), t_opt, 2.0 * fin + 1.0))
    return t


def _mu_full(B0, Aj, af_, el, eu, ef, Ej, sweeps=3):
    """multipliers for the full dual function: best vertex of the input-symbol arrangement, then
    coordinate ascent (exact 1-D steps).  Any mu >= 0 is valid; this only affects tightness."""
    Nb, ms, d = Aj.shape
    cands = [np.zeros((Nb, ms))]
    rows = [(Aj[:, :, k], af_[:, k]) for k in range(d)]
    for j in range(ms):
        e = np.zeros((Nb, ms)); e[:, j] = 1.0
        rows.append((e, np.zeros(Nb)))
    for comb in itertools.combinations(range(len(rows)), ms):
        Mx = np.stack([rows[q][0] for q in comb], axis=1)
        rh = np.stack([rows[q][1] for q in comb], axis=1)
        cands.append(_solve_small(Mx, rh))
    mus = np.stack(cands, axis=1)
    mus = np.where(np.isfinite(mus), np.maximum(mus, 0.0), 0.0)
    val = _phi_float(mus, B0, Aj, af_, el, eu, ef, Ej)
    mu = mus[np.arange(Nb), np.argmax(val, axis=1)]
    for _ in range(sweeps):
        for j in range(ms):
            mu[:, j] = _ca_1d(mu, j, B0, Aj, af_, el, eu, ef, Ej)
    return mu


def _phi_rig_s(mu, B0, Aj, af_, cf, rf, el, eu, ef, Ej):
    """rigorous lower bound of cf - rf + sum mu B0 + min_eps (af - sum mu Aj).eps
    - sum_n |ef_n - sum_j mu_j Ej_n| (eta terms, eta in [-1, 1])."""
    Nb, ms = mu.shape
    acc = NI(cf) - NI(rf)
    for j in range(ms):
        acc = acc + NI(mu[:, j]) * NI(B0[:, j])
    for k in range(Aj.shape[2]):
        g = NI(af_[:, k])
        for j in range(ms):
            g = g - NI(mu[:, j]) * NI(Aj[:, j, k])
        acc = acc + g * NI(el[:, k], eu[:, k])
    g = NI(ef)
    for j in range(ms):
        g = g - NI(mu[:, j][:, None]) * NI(Ej[:, j])
    mag = np.maximum(np.abs(g.lo), np.abs(g.hi))             # (N, NE)
    tot = usum(mag, 1)
    return dn(acc.lo - tot)


def _solve_small(Mx, rh):
    """solve Mx y = rh for batches of 1x1, 2x2, 3x3 systems by Cramer's rule; nan if singular."""
    n = Mx.shape[1]
    with np.errstate(all="ignore"):
        if n == 1:
            return rh / Mx[:, 0, :]
        if n == 2:
            a, b, c, d = Mx[:, 0, 0], Mx[:, 0, 1], Mx[:, 1, 0], Mx[:, 1, 1]
            det = a * d - b * c
            ok = np.abs(det) > 1e-14 * (np.abs(a * d) + np.abs(b * c) + 1e-300)
            y0 = (rh[:, 0] * d - b * rh[:, 1]) / det
            y1 = (a * rh[:, 1] - c * rh[:, 0]) / det
            y = np.stack([y0, y1], axis=1)
            return np.where(ok[:, None], y, np.nan)
        det = np.linalg.det(Mx)
        scale = np.abs(Mx).max(axis=(1, 2)) ** 3 + 1e-300
        ok = np.abs(det) > 1e-13 * scale
        Ms = np.where(ok[:, None, None], Mx, np.eye(n)[None])
        y = np.linalg.solve(Ms, rh[:, :, None])[:, :, 0]
        return np.where(ok[:, None], y, np.nan)


def _phi_rig(mu, B, Aj, af_, cf, rf, el, eu):
    """rigorous lower bound of cf - rf + sum mu B + min_{eps in [el, eu]} (af - sum mu Aj).eps."""
    Nb, ms = mu.shape
    acc = NI(cf) - NI(rf)
    for j in range(ms):
        acc = acc + NI(mu[:, j]) * NI(B[:, j])
    for k in range(Aj.shape[2]):
        g = NI(af_[:, k])
        for j in range(ms):
            g = g - NI(mu[:, j]) * NI(Aj[:, j, k])
        acc = acc + g * NI(el[:, k], eu[:, k])
    return acc.lo


def _farkas_rig(mu, B, Aj, el, eu):
    """True where sum mu B > max_{eps in [el, eu]} (sum mu Aj).eps holds rigorously."""
    Nb, ms = mu.shape
    acc = NI(np.zeros(Nb))
    for j in range(ms):
        acc = acc + NI(mu[:, j]) * NI(B[:, j])
    for k in range(Aj.shape[2]):
        g = NI(np.zeros(Nb))
        for j in range(ms):
            g = g + NI(mu[:, j]) * NI(Aj[:, j, k])
        acc = acc - g * NI(el[:, k], eu[:, k])
    return (acc.lo > 0) & (mu.sum(axis=1) > 0)


def _max_lin(at, el, eu):
    """upper bound of max over eps in [el, eu] of at.eps; at (S, N, d)."""
    P = NI(at) * NI(el[None], eu[None])
    tot = P.hi[:, :, 0]
    for k in range(1, at.shape[2]):
        tot = up(tot + P.hi[:, :, k])
    return tot


def _min_lin(at, el, eu):
    P = NI(at) * NI(el[None], eu[None])
    tot = P.lo[:, :, 0]
    for k in range(1, at.shape[2]):
        tot = dn(tot + P.lo[:, :, k])
    return tot


def _fbbt(beta, at, el, eu):
    """one round of interval propagation over the inequalities at.eps >= beta (S, N, d) on the
    eps-box [el, eu] (N, d).  Returns the reduced box and a mask of boxes proved empty."""
    P = NI(at) * NI(el[None], eu[None])
    Mh = P.hi                                               # >= max of at_k eps_k
    tot = Mh[:, :, 0]
    for k in range(1, at.shape[2]):
        tot = up(tot + Mh[:, :, k])
    el = el.copy(); eu = eu.copy()
    with np.errstate(all="ignore"):
        for k in range(at.shape[2]):
            rest = up(tot - Mh[:, :, k])                    # >= sum_{i != k} max at_i eps_i
            q = dn(beta - rest)                             # at_k eps_k >= q on feasible eps
            a = at[:, :, k]
            pos = a > 0
            neg = a < 0
            lo_k = np.where(pos & np.isfinite(q), dn(q / np.where(pos, a, 1.0)), -INF)
            hi_k = np.where(neg & np.isfinite(q), up(q / np.where(neg, a, -1.0)), INF)
            el[:, k] = np.maximum(el[:, k], lo_k.max(axis=0))
            eu[:, k] = np.minimum(eu[:, k], hi_k.min(axis=0))
    empty = np.any(el > eu, axis=1)
    return el, eu, empty


# ----------------------------------------------------------------------------- driver
U_WAVE3 = np.array([370.9280572920674, 0.7863373968889928, 1.620252679906157, 0.9494678019619749, 0.734065236105183])


def incumbent(M):
    """rigorous upper bound: a point certified strictly feasible in R by interval evaluation
    (local search with margin 1e-12 from the wave-3 optimum)."""
    u = ab.local_opt(M, U_WAVE3, margin=1e-12)
    ok, fv = M.point_value(u)
    assert ok
    return fv, u


def kkt_lag(M, u):
    """nonnegative KKT multipliers at u (NNLS on nearly active sides), as in ann_bb; any values >= 0
    keep the Lagrangian bound valid."""
    lag, res = ab.kkt_multipliers(M, u)
    return lag, res


def bnb(M, UB, xbest, tol_abs, tlim, batch=1024, log_every=25, save=None, init=None, log=print, prev_closed=INF):
    """best-first branch and bound (bbcore logic) with domain reduction.
    Final certified bound: min(UB, min lb over closed boxes with lb <= UB, min key over open boxes).
    Closed boxes: lb >= UB - tol_abs (or infeasible / emptied by the objective cut)."""
    t0 = time.time()
    if init is None:
        lo = M.lo0[None, :].copy(); hi = M.hi0[None, :].copy(); key = np.array([-INF])
    else:
        lo, hi, key = init
    vol0 = float(np.prod(M.hi0 - M.lo0))
    vol = lambda a, b: float(np.prod(np.maximum(b - a, 0.0), axis=1).sum()) / vol0
    closed_min = prev_closed
    vclosed = 0.0; vred = 0.0
    last_save = time.time(); save_every = 1200.0
    nproc = 0; it = 0
    while lo.shape[0] > 0 and time.time() - t0 < tlim:
        it += 1
        if lo.shape[0] > batch:
            idx = np.argpartition(key, batch - 1)[:batch]
            rest = np.ones(lo.shape[0], bool); rest[idx] = False
            blo, bhi, bk = lo[idx], hi[idx], key[idx]
            lo, hi, key = lo[rest], hi[rest], key[rest]
        else:
            blo, bhi, bk = lo, hi, key
            lo, hi, key = lo[:0], hi[:0], key[:0]
        pre = bk >= UB - tol_abs
        if pre.any():
            m_ = pre & (bk <= UB)
            if m_.any():
                closed_min = min(closed_min, float(bk[m_].min()))
            vclosed += vol(blo[pre], bhi[pre])
            blo, bhi, bk = blo[~pre], bhi[~pre], bk[~pre]
            if blo.shape[0] == 0:
                continue
        nproc += blo.shape[0]
        R = M.fbound_combo(blo, bhi, UB)
        lb = np.maximum(R["lb"], bk)
        j = int(np.argmin(R["ub"]))
        if R["ub"][j] < UB:
            UB, xbest = float(R["ub"][j]), R["x"][j].copy()
        keep = lb < UB - tol_abs
        vclosed += vol(blo[~keep], bhi[~keep])
        fath = (~keep) & (lb <= UB)
        if fath.any():
            closed_min = min(closed_min, float(lb[fath].min()))
        blo, bhi, lb, smear = blo[keep], bhi[keep], lb[keep], R["smear"][keep]
        mod = R["mod"][keep]
        if mod.any():
            nlo, nhi = R["newlo"][keep][mod], R["newhi"][keep][mod]
            vred += vol(blo[mod], bhi[mod]) - vol(nlo, nhi)
            lo = np.concatenate([lo, nlo]); hi = np.concatenate([hi, nhi]); key = np.concatenate([key, lb[mod]])
            blo, bhi, lb, smear = blo[~mod], bhi[~mod], lb[~mod], smear[~mod]
        if blo.shape[0]:
            w = bhi - blo
            k = np.argmax(smear, axis=1)
            r = np.arange(len(k))
            tiny = w[r, k] <= 1e-15 * np.maximum(1.0, np.abs(blo[r, k]))
            if tiny.any():
                closed_min = min(closed_min, float(lb[tiny].min()))
                vclosed += vol(blo[tiny], bhi[tiny])
                blo, bhi, lb, k = blo[~tiny], bhi[~tiny], lb[~tiny], k[~tiny]
                r = np.arange(len(k))
            mid = 0.5 * (blo[r, k] + bhi[r, k])
            l1, h1 = blo.copy(), bhi.copy(); h1[r, k] = mid
            l2, h2 = blo.copy(), bhi.copy(); l2[r, k] = mid
            lo = np.concatenate([lo, l1, l2]); hi = np.concatenate([hi, h1, h2]); key = np.concatenate([key, lb, lb])
        if save and time.time() - last_save > save_every:
            last_save = time.time()
            np.savez_compressed(save, lo=lo, hi=hi, key=key, UB=UB, closed_min=closed_min, xbest=xbest,
                                LB=min(closed_min, key.min() if key.size else INF, UB))
        if it % log_every == 0:
            glb = min(closed_min, key.min() if key.size else INF, UB)
            log(f"  it {it} processed {nproc} open {lo.shape[0]} UB {UB:.15g} LB {glb:.15g} closed-vol {vclosed:.6f} "
                f"reduced-vol {vred:.6f} t {time.time()-t0:.0f}s")
    omin = key.min() if key.size else INF
    LB = min(closed_min, omin, UB)
    if save:
        np.savez_compressed(save, lo=lo, hi=hi, key=key, UB=UB, LB=LB, closed_min=closed_min, xbest=xbest)
    return dict(LB=LB, UB=UB, x=xbest, processed=nproc, open=lo.shape[0], done=lo.shape[0] == 0,
                time=time.time() - t0, vclosed=vclosed, vred=vred)


def main(tol_rel=1e-6, tlim=600, batch=512, save=None, model="sep", resume=None):
    M = SepModel() if model.startswith("sep") else TMModel()
    if model == "sepfast":
        M.old_pass = False
    if model == "sep-nofull":
        M.full_mu = False
    if model == "sep-tmsmear":
        M.smear_mode = "tm"
    if model == "sep-nofull-tmsmear":
        M.full_mu = False
        M.smear_mode = "tm"
    if model == "sep-gradsmall":
        # full interval pass on boxes wider than 1/16 (relative); on smaller boxes only the
        # interval-gradient pass (for the branching score and the natural bound)
        M.full_mu = False
        M.old_min_relw = 1.0 / 16
        M.grad_small = True
    if model == "sep-hybrid":
        # interval pass only on large boxes; Taylor-model branching score (with KKT Lagrangian) elsewhere
        M.full_mu = False
        M.old_min_relw = 1.0 / 16
    print(f"model {model}: {type(M).__name__} old_pass={getattr(M, 'old_pass', True)} full_mu={getattr(M, 'full_mu', None)}", flush=True)
    t0 = time.time()
    UB, ub_u = incumbent(M)
    print(f"incumbent (rigorous, strictly feasible in R): f <= {UB!r} at {ub_u.tolist()} ({time.time()-t0:.0f}s)", flush=True)
    lag, res = kkt_lag(M, ub_u)
    M.lag = lag
    print("Lagrangian terms:", [(M.names[j], float(l), float(b), s) for j, l, b, s in lag], "KKT residual", res, flush=True)
    tol_abs = tol_rel * abs(UB)
    init, prev_closed = None, INF
    if resume:
        Z = np.load(resume)
        init = (Z["lo"], Z["hi"], Z["key"])
        prev_closed = float(Z["closed_min"])
        # every box closed in the earlier run(s) had lb >= prev_closed, so the bound of this run is
        # combined with it; the saved open boxes cover the rest of the domain
        print(f"resume from {resume}: {len(Z['key'])} open boxes, min key {Z['key'].min()!r}, "
              f"earlier closed_min {prev_closed!r}", flush=True)
    r = bnb(M, UB, ub_u, tol_abs, tlim, batch=batch, save=save, init=init, prev_closed=prev_closed,
            log=lambda s: print(s, flush=True))
    print(f"B&B: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s "
          f"closed-vol {r['vclosed']:.6f} reduced-vol {r['vred']:.6f}")
    print(f"  min f over R in [{r['LB']!r}, {r['UB']!r}]  tol_abs {tol_abs:.3e}")
    print(f"  best point u = {np.asarray(r['x']).tolist()}")
    return M, r


if __name__ == "__main__":
    tol = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-6
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600
    save = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
    model = sys.argv[4] if len(sys.argv) > 4 else "sep"
    resume = sys.argv[5] if len(sys.argv) > 5 else None
    main(tol, tl, save=save, model=model, resume=resume)
