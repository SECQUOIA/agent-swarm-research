"""Independent rigorous branch and bound for the KAN relaxation R (verifier's own code).

  python3 kan_bnb.py <name> <rel_tol> <time_limit_s> [batch]

Works directly with the model's exact piece polynomials P_k (kan_decode.py);
no "ideal spline" and no perturbation term Delta are used.  For a box of inputs
the lower bound holds for EVERY admissible choice of knot interval of every
edge (the hull over admissible pieces, and a reference piece plus an explicit
penalty |P_k - P_k0| in the second-order form).

R = { u in input box, h_j in [L_j, U_j] } with obj = A (beta0 + sum_j psi_j(h_j)) + B,
h_j = beta_j + sum_i phi_ij(u_i), phi = P_k + wb * silu on z in I_k.

Interval arithmetic: IEEE double with one-ulp outward rounding by nextafter
after every operation.  exp: numpy's exp widened by a relative 2^-50
(assumption: numpy's float64 exp is accurate to < 4 ulps; checked against
mpmath by `python3 kan_bnb.py --check-exp`).

Lower bounds per box: max of
  LB1  natural enclosure (tight per edge: hull over pieces; Taylor ranges of the
       cubic pieces intersected with mean-value forms),
  LB2  second-order form: psi_j(h) >= psi_j^k0(hhat_j) + D_j (h - hhat_j) - pen_j,
       D_j = [d_j -+ r_j] encloses psi_j^k0' on hull(H_j, hhat_j), or (per neuron,
       whichever is larger) psi_j(h) >= psi_j^k0(hhat_j) + psi_j^k0'(hhat_j)(h - hhat_j)
       + min(m_j, 0) (h - hhat_j)^2 / 2 - pen_j with m_j <= psi_j^k0'' on the hull; and
       sum_j d_j (h_j - hhat_j) splits into 1-D functions G_i(u_i) bounded by
       G_i'(c_i) s + m_i s^2 / 2 (m_i a lower bound of G_i'' on the box).
"""
import heapq
import json
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

from kan_decode import decode

INF = np.inf


def dn(x):
    return np.nextafter(x, -INF)


def up(x):
    return np.nextafter(x, INF)


def fdn(q):
    """largest float <= rational q"""
    f = float(q)
    return f if Fr(f) <= q else float(np.nextafter(f, -INF))


def fup(q):
    f = float(q)
    return f if Fr(f) >= q else float(np.nextafter(f, INF))


class Iv:
    __slots__ = ("lo", "hi")

    def __init__(s, lo, hi):
        s.lo, s.hi = lo, hi

    def __add__(s, o):
        if isinstance(o, Iv):
            return Iv(dn(s.lo + o.lo), up(s.hi + o.hi))
        return Iv(dn(s.lo + o), up(s.hi + o))
    __radd__ = __add__

    def __neg__(s):
        return Iv(-s.hi, -s.lo)

    def __sub__(s, o):
        if isinstance(o, Iv):
            return Iv(dn(s.lo - o.hi), up(s.hi - o.lo))
        return Iv(dn(s.lo - o), up(s.hi - o))

    def __rsub__(s, o):
        return (-s) + o

    def __mul__(s, o):
        if isinstance(o, Iv):
            a, b, c, d = s.lo * o.lo, s.lo * o.hi, s.hi * o.lo, s.hi * o.hi
            return Iv(dn(np.minimum(np.minimum(a, b), np.minimum(c, d))),
                      up(np.maximum(np.maximum(a, b), np.maximum(c, d))))
        a, b = s.lo * o, s.hi * o
        return Iv(dn(np.minimum(a, b)), up(np.maximum(a, b)))
    __rmul__ = __mul__

    def recip_pos(s):
        assert np.all(s.lo > 0)
        return Iv(dn(1.0 / s.hi), up(1.0 / s.lo))

    def mid(s):
        return 0.5 * s.lo + 0.5 * s.hi

    def hull(s, o):
        return Iv(np.minimum(s.lo, o.lo), np.maximum(s.hi, o.hi))

    def meet(s, o):
        return Iv(np.maximum(s.lo, o.lo), np.minimum(s.hi, o.hi))

    def mag(s):
        return np.maximum(np.abs(s.lo), np.abs(s.hi))

    def where(s, m, o):
        return Iv(np.where(m, s.lo, o.lo), np.where(m, s.hi, o.hi))

    def pt(x):
        return Iv(x, x)


# ---------------- rigorous exp / sigmoid / silu ----------------------------
EXPREL = 2.0 ** -50


import kan_iv as _KIV   # dossier variant: rigorous table exp built from IEEE + - * / only


def iexp(x):
    """x: Iv; exp is increasing.  Dossier variant: no libm exp; kan_iv.iexp_pt_fast
    (table of exp(j ln2/64) from 50-digit mpmath, degree-8 Taylor, explicit remainder)."""
    lo = np.asarray(x.lo, dtype=np.float64)
    hi = np.asarray(x.hi, dtype=np.float64)
    a = _KIV.iexp_pt_fast(lo).lo
    b = _KIV.iexp_pt_fast(hi).hi
    return Iv(np.broadcast_to(a, np.shape(lo)).copy() if np.ndim(lo) else a,
              np.broadcast_to(b, np.shape(hi)).copy() if np.ndim(hi) else b)


def isig(x):
    """sigmoid, increasing"""
    e_lo = iexp(Iv(-x.hi, -x.hi))   # exp(-x_hi) smallest -> sigma(x_hi) largest
    e_hi = iexp(Iv(-x.lo, -x.lo))
    lo = dn(1.0 / up(1.0 + e_hi.hi))
    hi = up(1.0 / dn(1.0 + e_lo.lo))
    return Iv(lo, hi)


def _zstar():
    """certified bracket of the minimiser z* of silu and a lower bound of min silu"""
    from mpmath import iv, mp, findroot, mpf
    mp.dps = 40
    f = lambda z: 1 + z * (1 - 1 / (1 + mp.exp(-z)))  # silu'/sigma
    z = findroot(f, mpf("-1.278"))
    iv.dps = 40
    zl, zr = z - mpf("1e-20"), z + mpf("1e-20")
    fi = lambda t: 1 + iv.mpf(t) * (1 - 1 / (1 + iv.exp(-iv.mpf(t))))
    assert fi(zl).b < 0 and fi(zr).a > 0     # silu' changes sign in [zl, zr]
    X = iv.mpf([zl, zr])
    smin = X / (1 + iv.exp(-X))
    return float(mp.mpf(zl)) - 1e-15, float(mp.mpf(zr)) + 1e-15, float(smin.a) - 1e-15


ZS_LO, ZS_HI, SMIN_LO = _zstar()


def silu_pt(x):
    """x: float array -> Iv enclosure of silu(x)"""
    return isig(Iv(x, x)) * x


def silu_rng(X):
    a = silu_pt(X.lo)
    b = silu_pt(X.hi)
    inc = X.lo >= ZS_HI
    dec = X.hi <= ZS_LO
    lo = np.where(inc, a.lo, np.where(dec, b.lo, SMIN_LO))
    hi = np.where(inc, b.hi, np.where(dec, a.hi, np.maximum(a.hi, b.hi)))
    return Iv(lo, hi)


def silu_d1_nat(X):
    s = isig(X)
    return s * (1.0 + X * (1.0 - s))


def silu_d2_nat(X):
    s = isig(X)
    return s * (1.0 - s) * (2.0 + X * (1.0 - 2.0 * s))


def silu_d1_pt(x):
    return silu_d1_nat(Iv(x, x))


def silu_d1_rng(X):
    m = X.mid()
    mv = silu_d1_pt(m) + silu_d2_nat(X) * (X - m)
    return mv.meet(silu_d1_nat(X))


# ---------------- model tables -----------------------------------------------
def shift(P, c):
    """coefficients of P(c + d) in d (exact)"""
    out = []
    for m in range(4):
        s = Fr(0)
        for d in range(m, 4):
            from math import comb
            s += P[d] * comb(d, m) * c ** (d - m)
        out.append(s)
    return out


class Layer:
    """a set of edges stacked as columns: pieces (K, ncol)"""

    def __init__(self, edges):
        K = len(edges[0]["I"])
        assert all(len(e["I"]) == K for e in edges)
        nc = len(edges)
        self.K, self.nc = K, nc
        self.Ilo = np.array([[fdn(e["I"][k][0]) for e in edges] for k in range(K)])
        self.Ihi = np.array([[fup(e["I"][k][1]) for e in edges] for k in range(K)])
        self.Ilo_in = np.array([[fup(e["I"][k][0]) for e in edges] for k in range(K)])
        self.Ihi_in = np.array([[fdn(e["I"][k][1]) for e in edges] for k in range(K)])
        self.c = np.array([[float((e["I"][k][0] + e["I"][k][1]) / 2) for e in edges] for k in range(K)])
        A = np.zeros((4, 2, K, nc))
        for k in range(K):
            for j, e in enumerate(edges):
                a = shift(e["P"][k], Fr(self.c[k, j]))
                for mm in range(4):
                    A[mm, 0, k, j] = fdn(a[mm])
                    A[mm, 1, k, j] = fup(a[mm])
        self.A = A
        self.wb = Iv(np.array([fdn(e["wb"]) for e in edges]), np.array([fup(e["wb"]) for e in edges]))
        # knot difference polynomials Q_k = P_{k+1} - P_k about t_k = float(I_{k+1}.lo)
        Q = np.zeros((4, K - 1, nc))
        T = np.zeros((K - 1, nc))
        for k in range(K - 1):
            for j, e in enumerate(edges):
                t = float(e["I"][k + 1][0])
                T[k, j] = t
                q = shift([e["P"][k + 1][d] - e["P"][k][d] for d in range(4)], Fr(t))
                for mm in range(4):
                    Q[mm, k, j] = fup(abs(q[mm]))
        self.Q, self.T = Q, T
        self.cols = np.arange(nc)[None, :]

    def coeffs(self, k):
        cols = np.broadcast_to(self.cols, k.shape)
        return [Iv(self.A[mm, 0][k, cols], self.A[mm, 1][k, cols]) for mm in range(4)], self.c[k, cols]

    def krange(self, X):
        """admissible piece index range for argument intervals X (N, nc)"""
        kmin = (self.Ihi[None, :, :] < X.lo[:, None, :]).sum(axis=1)
        kmax = (self.Ilo[None, :, :] <= X.hi[:, None, :]).sum(axis=1) - 1
        return kmin, kmax

    def kref(self, x, kmin, kmax):
        k = (self.Ihi[None, :, :] < x[:, None, :]).sum(axis=1)
        return np.clip(k, kmin, np.maximum(kmin, kmax))

    # polynomial of piece k: value at point x, range on X, derivatives
    def p_pt(self, k, x):
        a, c = self.coeffs(k)
        d = Iv(x, x) - c
        return ((a[3] * d + a[2]) * d + a[1]) * d + a[0]

    def p_d1_pt(self, k, x):
        a, c = self.coeffs(k)
        d = Iv(x, x) - c
        return (a[3] * 3.0 * d + a[2] * 2.0) * d + a[1]

    def p_d1_rng(self, k, X):
        a, c = self.coeffs(k)
        d = X - c
        return (a[3] * 3.0 * d + a[2] * 2.0) * d + a[1]

    def p_d2_rng(self, k, X):
        a, c = self.coeffs(k)
        d = X - c
        return a[3] * 6.0 * d + a[2] * 2.0

    def p_rng(self, k, X):
        a, c = self.coeffs(k)
        D = X - c
        mu = D.mid()
        rho = up(np.maximum(mu - D.lo, D.hi - mu))
        m = Iv(mu, mu)
        b0 = ((a[3] * m + a[2]) * m + a[1]) * m + a[0]
        b1 = (a[3] * 3.0 * m + a[2] * 2.0) * m + a[1]
        b2 = a[3] * 3.0 * m + a[2]
        r2 = up(rho * rho)
        r3 = up(r2 * rho)
        t1 = Iv(-rho, rho) * b1
        t2 = b2 * Iv(np.zeros_like(r2), r2)
        t3 = a[3] * Iv(-r3, r3)
        return b0 + t1 + t2 + t3

    def phi_rng(self, k, X):
        """enclosure of P_k + wb*silu on X: natural and mean-value, intersected"""
        nat = self.p_rng(k, X) + self.wb * silu_rng(X)
        m = X.mid()
        mv = self.phi_pt(k, m) + (self.p_d1_rng(k, X) + self.wb * silu_d1_rng(X)) * (X - m)
        return nat.meet(mv)

    def phi_pt(self, k, x):
        return self.p_pt(k, x) + self.wb * silu_pt(x)

    def phi_d1_pt(self, k, x):
        return self.p_d1_pt(k, x) + self.wb * silu_d1_pt(x)

    def phi_d1_rng(self, k, X):
        return self.p_d1_rng(k, X) + self.wb * silu_d1_rng(X)

    def phi_d2_rng(self, k, X):
        return self.p_d2_rng(k, X) + self.wb * silu_d2_nat(X)

    def natural(self, X, kmin, kmax):
        """hull over admissible pieces of the edge range on X; (N, nc)"""
        span = int((kmax - kmin).max()) if kmin.size else 0
        lo = np.full(X.lo.shape, INF)
        hi = np.full(X.lo.shape, -INF)
        for o in range(span + 1):
            k = np.minimum(kmin + o, self.K - 1)
            ok = (kmin + o) <= kmax
            cols = np.broadcast_to(self.cols, k.shape)
            Xk = X.meet(Iv(self.Ilo[k, cols], self.Ihi[k, cols]))
            ok &= Xk.lo <= Xk.hi
            Xk = Iv(np.where(ok, Xk.lo, X.lo), np.where(ok, Xk.hi, X.lo))
            R = self.phi_rng(k, Xk)
            lo = np.where(ok, np.minimum(lo, R.lo), lo)
            hi = np.where(ok, np.maximum(hi, R.hi), hi)
        return Iv(lo, hi)

    def penalty(self, X, kmin, kmax, k0):
        """bound on |P_k - P_k0| over X cap I_k for admissible k != k0 (inf if a
        piece further than one knot from k0 is admissible)"""
        pen = np.zeros(X.lo.shape)
        far = (kmin < k0 - 1) | (kmax > k0 + 1)
        cols = np.broadcast_to(self.cols, k0.shape)
        for side in (-1, 1):
            k = k0 + side
            has = (k >= kmin) & (k <= kmax) & ~far
            kc = np.clip(k, 0, self.K - 1)
            knot = np.clip(np.minimum(k0, kc), 0, self.K - 2)
            Xk = X.meet(Iv(self.Ilo[kc, cols], self.Ihi[kc, cols]))
            d = Xk - self.T[knot, cols]
            dm = d.mag()
            q = [self.Q[mm][knot, cols] for mm in range(4)]
            v = up(q[0] + up(dm * up(q[1] + up(dm * up(q[2] + up(dm * q[3]))))))
            pen = np.where(has & (Xk.lo <= Xk.hi), np.maximum(pen, v), pen)
        return np.where(far, INF, pen)


def _half_ginv_g(H, g):
    """exact: if the float matrix H is positive definite (rational LDL^T), return an
    upper-rounded float >= g^T H^-1 g / 2; else None"""
    n = len(g)
    A = [[Fr(float(H[a, b])) for b in range(n)] for a in range(n)]
    L = [[Fr(0)] * n for _ in range(n)]
    D = [Fr(0)] * n
    for j in range(n):
        s = A[j][j] - sum(L[j][k] * L[j][k] * D[k] for k in range(j))
        if s <= 0:
            return None
        D[j] = s
        L[j][j] = Fr(1)
        for i in range(j + 1, n):
            L[i][j] = (A[i][j] - sum(L[i][k] * L[j][k] * D[k] for k in range(j))) / s
    # H = L D L^T ; g^T H^-1 g = sum_k y_k^2 / D_k with L y = g
    y = [Fr(0)] * n
    for i in range(n):
        y[i] = Fr(float(g[i])) - sum(L[i][k] * y[k] for k in range(i))
    q = sum(y[k] * y[k] / D[k] for k in range(n)) / 2
    return fup(q)


def minquad(gl, gh, m, sl, sh):
    """lower bound of min over g in [gl,gh], s in [sl,sh] of g*s + m*s^2/2 (m a float lower bound)"""
    best = np.full(gl.shape, INF)
    half_m = 0.5 * m   # exact
    for g in (gl, gh):
        for s in (sl, sh):
            gs = dn(g * s)
            ms = np.where(half_m >= 0, dn(half_m * dn(s * s)), dn(half_m * up(s * s)))
            best = np.minimum(best, dn(gs + ms))
        # convex case: the vertex s* = -g/m, value -g^2/(2m), if s* can lie in [sl, sh]
        mpos = np.where(m > 0, m, 1.0)
        vert = -up(up(g * g) / dn(2.0 * mpos))
        sstar = -g / mpos
        inside = (m > 0) & (sstar >= sl * (1 + 1e-9) - 1e-300) & (sstar <= sh * (1 + 1e-9) + 1e-300)
        best = np.where(inside, np.minimum(best, vert), best)
    return best


class Model:
    def __init__(self, name):
        D = decode(name)
        self.D = D
        self.name = name
        assert D["A"] > 0
        self.A = (fdn(D["A"]), fup(D["A"]))
        self.B = (fdn(D["B"]), fup(D["B"]))
        self.beta0 = (fdn(D["beta0"]), fup(D["beta0"]))
        self.d = len(D["inputs"])
        self.nh = len(D["hiddens"])
        self.ulo_in = np.array([fup(inp["lo"]) for inp in D["inputs"]])
        self.uhi_in = np.array([fdn(inp["hi"]) for inp in D["inputs"]])
        # outward box (the B&B covers the outward-rounded box: sound)
        self.ulo = np.array([fdn(inp["lo"]) for inp in D["inputs"]])
        self.uhi = np.array([fup(inp["hi"]) for inp in D["inputs"]])
        self.L1 = [Layer([h["edge_from"][i] for h in D["hiddens"]]) for i in range(self.d)]
        self.L2 = Layer([h["edge2"] for h in D["hiddens"]])
        self.beta = Iv(np.array([fdn(h["beta"]) for h in D["hiddens"]]), np.array([fup(h["beta"]) for h in D["hiddens"]]))
        self.Hlo = np.array([fdn(h["lo"]) for h in D["hiddens"]])
        self.Hhi = np.array([fup(h["hi"]) for h in D["hiddens"]])
        self.Hlo_in = np.array([fup(h["lo"]) for h in D["hiddens"]])
        self.Hhi_in = np.array([fdn(h["hi"]) for h in D["hiddens"]])

    def evaluate(self, ul, uh, want_ub=True, thr=None, wmax3=0.05, force3=False):
        """ul, uh: (N, d).  Returns LB (N,), UB candidate (N,) (inf if not certified feasible).
        If thr is given, the third-order bound LB3 is also computed for boxes of
        width <= wmax3 whose bound is still below thr."""
        N = ul.shape[0]
        nh = self.nh
        c = 0.5 * ul + 0.5 * uh
        H = Iv(np.broadcast_to(self.beta.lo, (N, nh)).copy(), np.broadcast_to(self.beta.hi, (N, nh)).copy())
        Hh = Iv(H.lo.copy(), H.hi.copy())
        feas = np.ones(N, bool)
        cfeas = np.ones(N, bool)
        g1, h2, pen1, d2c, d1U, rngU = [], [], [], [], [], []
        for i in range(self.d):
            L = self.L1[i]
            U = Iv(np.repeat(ul[:, i:i + 1], nh, 1), np.repeat(uh[:, i:i + 1], nh, 1))
            ci = np.repeat(c[:, i:i + 1], nh, 1)
            kmin, kmax = L.krange(U)
            feas &= np.all(kmin <= kmax, axis=1)
            kmin = np.clip(kmin, 0, L.K - 1)          # infeasible boxes: keep indices valid
            kmax = np.clip(np.maximum(kmax, kmin), 0, L.K - 1)
            H = H + L.natural(U, kmin, kmax)
            k0 = L.kref(ci, kmin, kmax)
            Hh = Hh + L.phi_pt(k0, ci)
            cols = np.broadcast_to(L.cols, k0.shape)
            cfeas &= np.all((L.Ilo_in[k0, cols] <= ci) & (ci <= L.Ihi_in[k0, cols]), axis=1)
            g1.append(L.phi_d1_pt(k0, ci))
            h2.append(L.phi_d2_rng(k0, U))
            pen1.append(L.penalty(U, kmin, kmax, k0))
            if thr is not None:
                d2c.append(L.phi_d2_rng(k0, Iv(ci, ci)))
                d1U.append(L.phi_d1_rng(k0, U))
                rngU.append(L.phi_rng(k0, U))
        Hp = H.meet(Iv(self.Hlo[None, :], self.Hhi[None, :]))
        feas &= np.all(Hp.lo <= Hp.hi, axis=1)
        cfeas &= np.all((Hh.lo >= self.Hlo_in[None, :]) & (Hh.hi <= self.Hhi_in[None, :]), axis=1)
        # make empty intervals harmless for the arithmetic below
        Hp = Iv(np.where(Hp.lo <= Hp.hi, Hp.lo, H.lo), np.where(Hp.lo <= Hp.hi, Hp.hi, H.lo))
        L2 = self.L2
        kmin, kmax = L2.krange(Hp)
        feas &= np.all(kmin <= kmax, axis=1)
        kmin = np.clip(kmin, 0, L2.K - 1)
        kmax = np.clip(np.maximum(kmax, kmin), 0, L2.K - 1)
        Psi = L2.natural(Hp, kmin, kmax)
        lb1 = self._outer_lb(Psi.lo)
        # second-order form
        hm = Hh.mid()
        k0 = L2.kref(hm, kmin, kmax)
        psi0 = L2.phi_rng(k0, Hh)            # psi^k0 over the tiny interval hhat
        Hx = Hp.hull(Hh)
        Dd = L2.phi_d1_rng(k0, Hx)
        d = Dd.mid()
        r = up(np.maximum(Dd.hi - d, d - Dd.lo))
        rho = up(np.maximum(up(Hp.hi - Hh.lo), up(Hh.hi - Hp.lo)))
        pen2 = L2.penalty(Hp, kmin, kmax, k0)
        term_a = dn(dn(psi0.lo - pen2) - up(r * rho))
        # variant b: Taylor at hhat with the curvature sign,
        # psi(h) >= psi(hhat) + psi'(hhat)(h - hhat) + min(m, 0) (h - hhat)^2 / 2
        p1h = L2.phi_d1_rng(k0, Hh)
        db = p1h.mid()
        rb = up(np.maximum(p1h.hi - db, db - p1h.lo))
        mcurv = L2.phi_d2_rng(k0, Hx).lo
        term_b = dn(dn(dn(psi0.lo - pen2) - up(rb * rho)) + dn(0.5 * dn(np.minimum(mcurv, 0.0) * up(rho * rho))))
        useb = term_b > term_a         # choose per hidden neuron (both are valid)
        d = np.where(useb, db, d)
        term = np.where(useb, term_b, term_a)
        absd = np.abs(d)
        for i in range(self.d):
            term = dn(term - up(absd * pen1[i]))
        tot = self._sum_dn(term)
        for i in range(self.d):
            gI = Iv(d, d) * g1[i]
            g = Iv(self._sum_dn(gI.lo), self._sum_up(gI.hi))
            mI = Iv(d, d) * h2[i]
            m = self._sum_dn(mI.lo)
            sl = dn(ul[:, i] - c[:, i])
            sh = up(uh[:, i] - c[:, i])
            tot = dn(tot + minquad(g.lo, g.hi, m, sl, sh))
        lb2 = self._obj_lb(tot)
        lb2 = np.where(np.isfinite(lb2), lb2, -INF)     # also maps nan -> -inf
        lb1 = np.where(np.isnan(lb1), -INF, lb1)
        lb = np.maximum(lb1, lb2)
        lb = np.where(feas, lb, INF)
        if thr is not None:
            lb3 = self._lb3(ul, uh, c, lb, thr, wmax3, k0, Hh, Hp, psi0, pen2, pen1, g1, h2, d2c, d1U, rngU, force3)
            lb = np.maximum(lb, np.where(feas, lb3, INF))
        ub = np.full(N, INF)
        if want_ub:
            ctop = self._obj_ub(self._sum_up(psi0.hi))
            ok = cfeas & feas & np.all((c >= self.ulo_in[None, :]) & (c <= self.uhi_in[None, :]), axis=1)
            cols = np.broadcast_to(L2.cols, k0.shape)
            ok &= np.all((L2.Ilo_in[k0, cols] <= Hh.lo) & (Hh.hi <= L2.Ihi_in[k0, cols]), axis=1)
            ub = np.where(ok, ctop, INF)
        return lb, ub, lb1, lb2


    def _lb3(self, ul, uh, c, lb, thr, wmax3, k0, Hh, Hp, psi0, pen2, pen1, g1, h2, d2c, d1U, rngU, force3=False):
        """third-order form with the reference pieces (extended polynomials):
        V(u,K) >= Vref(u) - A*sum_j (pen2_j + Lip_j * sum_i pen1_ij)
        Vref(u) = Vref(c) + g.s + s^T H(xi) s / 2 >= Vref(c) + gm.s + s^T Hm s / 2 - gr.r - r^T Rad r / 2
                >= Vref(c) - gm^T Hm^-1 gm / 2 - gr.r - r^T Rad r / 2      (Hm proved PD exactly)."""
        N, d, nh = ul.shape[0], self.d, self.nh
        out = np.full(N, -INF)
        pentot = np.zeros(N, bool)
        w = (uh - ul).max(axis=1)
        cand = (w <= wmax3) & (lb < thr)
        for i in range(d):
            cand &= np.all(np.isfinite(pen1[i]), axis=1)
        cand &= np.all(np.isfinite(pen2), axis=1)
        idx = np.nonzero(cand)[0]
        if len(idx) == 0:
            return out
        L2 = self.L2

        def sel(X):
            return Iv(X.lo[idx], X.hi[idx])
        k0s = k0[idx]
        Hhs = sel(Hh)
        Hr = Iv(np.broadcast_to(self.beta.lo, (len(idx), nh)).copy(), np.broadcast_to(self.beta.hi, (len(idx), nh)).copy())
        for i in range(d):
            Hr = Hr + sel(rngU[i])
        p1c = L2.phi_d1_rng(k0s, Hhs)
        p2c = L2.phi_d2_rng(k0s, Hhs)
        p1B = L2.phi_d1_rng(k0s, Hr)
        p2B = L2.phi_d2_rng(k0s, Hr)
        lip = L2.phi_d1_rng(k0s, sel(Hp).hull(Hr)).mag()
        Aiv = Iv(np.full(len(idx), self.A[0]), np.full(len(idx), self.A[1]))
        g1s = [sel(t) for t in g1]
        d2cs = [sel(t) for t in d2c]
        d1Us = [sel(t) for t in d1U]
        h2s = [sel(t) for t in h2]

        def rowsum(X):
            return Iv(self._sum_dn(X.lo), self._sum_up(X.hi))
        G = [rowsum(p1c * g1s[a]) * Aiv for a in range(d)]
        Hm = np.zeros((len(idx), d, d))
        Rad = np.zeros((len(idx), d, d))
        for a in range(d):
            for b in range(a, d):
                hc = p2c * g1s[a] * g1s[b]
                hB = p2B * d1Us[a] * d1Us[b]
                if a == b:
                    hc = hc + p1c * d2cs[a]
                    hB = hB + p1B * h2s[a]
                hc = rowsum(hc) * Aiv
                hB = rowsum(hB) * Aiv
                m = hc.mid()
                rr = up(np.maximum(hB.hi - m, m - hB.lo))
                Hm[:, a, b] = Hm[:, b, a] = m
                Rad[:, a, b] = Rad[:, b, a] = rr
        gm = np.stack([t.mid() for t in G], axis=1)
        gr = np.stack([up(np.maximum(t.hi - t.mid(), t.mid() - t.lo)) for t in G], axis=1)
        sl = dn(ul[idx] - c[idx])
        sh = up(uh[idx] - c[idx])
        r = np.maximum(np.abs(sl), np.abs(sh))
        err = np.zeros(len(idx))
        for a in range(d):
            err = up(err + up(gr[:, a] * r[:, a]))
            for b in range(d):
                err = up(err + up(0.5 * up(Rad[:, a, b] * up(r[:, a] * r[:, b]))))
        pen = np.zeros(len(idx))
        for j in range(nh):
            sp = pen2[idx, j]
            for i in range(d):
                sp = up(sp + up(lip[:, j] * pen1[i][idx, j]))
            pen = up(pen + sp)
        pen = up(pen * self.A[1])
        vc = self._obj_lb(self._sum_dn(psi0.lo[idx]))
        # float estimate, then exact certificate only where it can help
        ev = np.linalg.eigvalsh(Hm)
        pd = ev[:, 0] > 0
        qest = np.full(len(idx), INF)
        if pd.any():
            sol = np.linalg.solve(Hm[pd], gm[pd][:, :, None])[:, :, 0]
            qest[pd] = 0.5 * np.einsum("ij,ij->i", gm[pd], sol)
        est = vc - qest - err - pen
        # exact certificate only where LB3 would prune (below thr, LB1/LB2 are kept)
        for t in np.nonzero(pd & ((est > lb[idx]) if force3 else (est >= thr)))[0]:
            q = _half_ginv_g(Hm[t], gm[t])
            if q is None:
                continue
            v = dn(dn(dn(vc[t] - q) - err[t]) - pen[t])
            out[idx[t]] = v
        return out

    # ---- rounding-safe sums and the outer affine map obj = A*(beta0 + s) + B
    @staticmethod
    def _sum_dn(X):
        s = np.zeros(X.shape[0])
        for j in range(X.shape[1]):
            s = dn(s + X[:, j])
        return s

    @staticmethod
    def _sum_up(X):
        s = np.zeros(X.shape[0])
        for j in range(X.shape[1]):
            s = up(s + X[:, j])
        return s

    def _obj_lb(self, s):
        t = dn(s + self.beta0[0])
        return dn(dn(np.where(t >= 0, dn(self.A[0] * t), dn(self.A[1] * t))) + self.B[0])

    def _obj_ub(self, s):
        t = up(s + self.beta0[1])
        return up(up(np.where(t >= 0, up(self.A[1] * t), up(self.A[0] * t))) + self.B[1])

    def _outer_lb(self, psilo):
        return self._obj_lb(self._sum_dn(psilo))


def check_exp(n=200000):
    from mpmath import mp, mpf, exp
    mp.dps = 40
    rng = np.random.default_rng(1)
    x = rng.uniform(-8, 8, n)
    y = np.exp(x)
    worst = 0.0
    for xi, yi in zip(x[:n], y[:n]):
        t = exp(mpf(float(xi)))
        err = abs(mpf(float(yi)) - t) / t
        worst = max(worst, float(err))
    print("numpy exp: max relative error on %d points in [-8, 8]: %.3g (= %.2f ulp of 2^-52); widening used %.3g"
          % (n, worst, worst / 2.0 ** -52, EXPREL))


def vfloat_factory(M):
    """plain float evaluation of V(u) with the pieces containing each argument (heuristic use only)"""
    def piece(L, x):
        k = np.array([min(max(int(np.searchsorted(L.Ihi[:, j], x[j])), 0), L.K - 1) for j in range(L.nc)])
        a = [0.5 * (L.A[mm, 0][k, np.arange(L.nc)] + L.A[mm, 1][k, np.arange(L.nc)]) for mm in range(4)]
        d = x - L.c[k, np.arange(L.nc)]
        wb = 0.5 * (L.wb.lo + L.wb.hi)
        return ((a[3] * d + a[2]) * d + a[1]) * d + a[0] + wb * x / (1 + np.exp(-x))
    beta = 0.5 * (M.beta.lo + M.beta.hi)
    A, B, b0 = 0.5 * sum(M.A), 0.5 * sum(M.B), 0.5 * sum(M.beta0)

    def f(u):
        u = np.clip(u, M.ulo_in, M.uhi_in)
        h = beta.copy()
        for i in range(M.d):
            h = h + piece(M.L1[i], np.full(M.nh, u[i]))
        viol = np.maximum(M.Hlo_in - h, 0).sum() + np.maximum(h - M.Hhi_in, 0).sum()
        return A * (b0 + piece(M.L2, h).sum()) + B + 1e6 * viol
    return f


def local_ub(M, starts, rng):
    """float local search (heuristic); the result is re-evaluated rigorously by the caller"""
    from scipy.optimize import minimize
    f = vfloat_factory(M)
    best = (INF, None)
    bounds = list(zip(M.ulo_in, M.uhi_in))
    for s in starts:
        r = minimize(f, s, method="L-BFGS-B", bounds=bounds, options=dict(ftol=1e-16, gtol=1e-12, maxiter=2000))
        r = minimize(f, r.x, method="Nelder-Mead", options=dict(xatol=1e-13, fatol=1e-17, maxiter=4000, maxfev=8000))
        x = np.clip(r.x, M.ulo_in, M.uhi_in)
        _, ub, _, _ = M.evaluate(x[None, :], x[None, :])
        if ub[0] < best[0]:
            best = (float(ub[0]), x)
    return best


def bnb(name, rtol, tlim, batch=512, starts=None, log=print, seed=0, third=True):
    M = Model(name)
    t0 = time.time()
    rng = np.random.default_rng(seed)
    d = M.d
    # incumbent: multistart local search from random points (and optional given starts)
    S = [M.ulo + rng.random(d) * (M.uhi - M.ulo) for _ in range(20)]
    if starts is not None:
        S += [np.array(s) for s in starts]
    UB, ubx = local_ub(M, S, rng)
    log("incumbent from local search: %.17g at %s (%.1fs)" % (UB, list(ubx), time.time() - t0))
    tol = rtol * max(1.0, abs(UB))
    # open boxes: arrays
    lo = M.ulo[None, :].copy()
    hi = M.uhi[None, :].copy()
    lb, ub, _, _ = M.evaluate(lo, hi)
    LB = lb.copy()
    processed = 1
    it = 0
    closed_final = []
    while True:
        if len(LB) == 0:
            break
        if time.time() - t0 > tlim:
            break
        # pick the batch of lowest-LB boxes
        nb = min(batch, len(LB))
        if nb < len(LB):
            sel = np.argpartition(LB, nb - 1)[:nb]
        else:
            sel = np.arange(len(LB))
        keep = np.ones(len(LB), bool)
        keep[sel] = False
        blo, bhi = lo[sel], hi[sel]
        lo, hi, LB = lo[keep], hi[keep], LB[keep]
        w = bhi - blo
        ax = np.argmax(w, axis=1)
        mid = 0.5 * blo[np.arange(nb), ax] + 0.5 * bhi[np.arange(nb), ax]
        c1lo, c1hi = blo.copy(), bhi.copy()
        c2lo, c2hi = blo.copy(), bhi.copy()
        c1hi[np.arange(nb), ax] = mid
        c2lo[np.arange(nb), ax] = mid
        clo = np.vstack([c1lo, c2lo])
        chi = np.vstack([c1hi, c2hi])
        clb, cub, _, _ = M.evaluate(clo, chi, thr=(UB - tol) if third else None)
        processed += len(clb)
        if np.min(cub) < UB:
            UB = float(np.min(cub))
            ubx = 0.5 * clo[np.argmin(cub)] + 0.5 * chi[np.argmin(cub)]
            tol = rtol * max(1.0, abs(UB))
        alive = clb < UB - tol
        lo = np.vstack([lo, clo[alive]])
        hi = np.vstack([hi, chi[alive]])
        LB = np.concatenate([LB, clb[alive]])
        if len(LB):
            alive_all = LB < UB - tol
            lo, hi, LB = lo[alive_all], hi[alive_all], LB[alive_all]
        it += 1
        if it % 200 == 0:
            log("  it %d processed %d open %d UB %.17g minLB %.17g maxwidth %.3g t %.0fs" % (
                it, processed, len(LB), UB, LB.min() if len(LB) else INF,
                (hi - lo).max() if len(LB) else 0, time.time() - t0))
    done = len(LB) == 0
    final = min(UB - tol, float(LB.min()) if len(LB) else INF)
    final = float(dn(final))
    res = dict(name=name, done=done, processed=processed, open=int(len(LB)), UB=UB, ub_u=list(map(float, ubx)),
               tol=tol, lower_bound=final, time=time.time() - t0)
    log(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    if sys.argv[1] == "--check-exp":
        check_exp()
        sys.exit()
    name = sys.argv[1]
    rtol = float(sys.argv[2])
    tlim = float(sys.argv[3])
    batch = int(sys.argv[4]) if len(sys.argv) > 4 else 512
    starts = None
    if len(sys.argv) > 5:
        starts = [json.loads(sys.argv[5])]
    res = bnb(name, rtol, tlim, batch, starts)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "%s.bnb.json" % name)
    json.dump(res, open(out, "w"), indent=1)
