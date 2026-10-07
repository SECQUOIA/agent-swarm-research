"""Reviewer's own Hessian map Psi(theta), affine arithmetic, and exact negative-definiteness test.

Psi (derived independently in pindyck-review.md, Section 3): per period t, with gradients g and
Hessians H of s_{t-1}, cs_{t-1}, R_{t-1} carried forward,
  w = K beta phi, io = 1/(1 + w), kap = phi io
  gb = .1 E e_t - K beta gc
  Hb = beta (K^2 gc gc' - K Hc) - .1 K E (e_t gc' + gc e_t')
  gs = .75 io gs_prev + kap gb
  Hs = .75 io Hs_prev + kap Hb - K kap (gb gs' + gs gb') + K^2 beta kap gs gs'
  gc += gs, Hc += Hs;  gd = gtd_t - gs, Hd = -Hs;  gR -= gd, HR -= Hd
  gq = e_t + 250 v2 gR,  Hq = 250 v2 HR - 500 v3 gR gR'
  HJ += delta_t (u Hd + d Hq + gd gq' + gq gd')

AF (affine form with INTERVAL coefficients; no rounding-error analysis needed):
  for every eps in [-1,1]^m the true value lies in [c] + sum_k [a_k] eps_k + [-r, r],
  evaluated in exact real interval arithmetic. All float operations are rounded outward with
  nextafter (each IEEE result is within half an ulp of the exact result).
Matrix test: exact rational arithmetic (Python Fraction / int).
"""
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

import own_model as MOD

T = n = 16
GR = ["beta", "E", "phi", "d", "u", "v2", "v3"]
m = len(GR) * T
INF = np.inf
iv = mp.iv
iv.dps = 30


def dn(x):
    return np.nextafter(x, -INF)


def up(x):
    return np.nextafter(x, INF)


def fl_dn(q):
    f = float(q)
    return f if Fr(f) <= q else float(np.nextafter(f, -INF))


def fl_up(q):
    f = float(q)
    return f if Fr(f) >= q else float(np.nextafter(f, INF))


def raw2fr(r):
    sgn, man, ex, _ = r
    q = Fr(man) * (Fr(2) ** ex)
    return -q if sgn else q


def ivlo(x):
    return raw2fr(x._mpi_[0])


def ivhi(x):
    return raw2fr(x._mpi_[1])


# exact constants
KIV = -iv.mpf(MOD.KAPSTR) * iv.log(iv.mpf("1.02"))
K_LO, K_HI = fl_dn(ivlo(KIV)), fl_up(ivhi(KIV))
DELTA_Q = MOD.DELTAq
GTD_Q = [[-Fr(13, 100) * Fr(87, 100) ** (t - j) if j <= t else Fr(0) for j in range(T)] for t in range(T)]


# ---------------------------------------------------------------- float version
def psi_float(th):
    """float Psi(theta); th[g][t] floats"""
    K = 0.5 * (K_LO + K_HI)
    gs, Hs, gc, Hc, gR, HR = np.zeros(n), np.zeros((n, n)), np.zeros(n), np.zeros((n, n)), np.zeros(n), np.zeros((n, n))
    HJ = np.zeros((n, n))
    for t in range(T):
        e = np.zeros(n)
        e[t] = 1.0
        beta, phi, d, u, v2, v3 = (th[g][t] for g in ["beta", "phi", "d", "u", "v2", "v3"])
        E = 1.0 if t == 0 else th["E"][t]
        io = 1.0 / (1.0 + K * beta * phi)
        kap = phi * io
        gb = 0.1 * E * e - K * beta * gc
        Hb = beta * (K * K * np.outer(gc, gc) - K * Hc) - 0.1 * K * E * (np.outer(e, gc) + np.outer(gc, e))
        gs = 0.75 * io * gs + kap * gb
        Hs = 0.75 * io * Hs + kap * Hb - K * kap * (np.outer(gb, gs) + np.outer(gs, gb)) + K * K * beta * kap * np.outer(gs, gs)
        gc, Hc = gc + gs, Hc + Hs
        gd = np.array([float(v) for v in GTD_Q[t]]) - gs
        Hd = -Hs
        gR, HR = gR - gd, HR - Hd
        gq = e + 250 * v2 * gR
        Hq = 250 * v2 * HR - 500 * v3 * np.outer(gR, gR)
        HJ = HJ + float(DELTA_Q[t]) * (u * Hd + d * Hq + np.outer(gd, gq) + np.outer(gq, gd))
    return HJ


def theta_mp(p, dps=40):
    """theta(p) at high precision (own recursion), returned as floats, plus J(p) as mpf"""
    with mp.workdps(dps):
        K = -mp.mpf(MOD.KAPSTR) * mp.log(mp.mpf("1.02"))
        td, s, cs, R, J = mp.mpf(18), mp.mpf("6.5"), mp.mpf(0), mp.mpf(500), mp.mpf(0)
        th = {g: [0.0] * T for g in GR}
        for t in range(T):
            pt = mp.mpf(p[t])
            td = mp.mpf(".87") * td - mp.mpf(".13") * pt + mp.mpf(MOD.CT[t])
            E = mp.exp(-K * cs)
            beta = (mp.mpf("1.1") + mp.mpf(".1") * pt) * E
            a = mp.mpf(".75") * s
            y = a + beta
            for _ in range(100):
                y = y - (y - a - beta * mp.exp(-K * y)) / (1 + K * beta * mp.exp(-K * y))
            s = y
            cs = cs + s
            d = td - s
            R = R - d
            u = pt - 250 / R
            J = J + mp.mpf(MOD.DELTA[t]) * d * u
            for g, v in zip(GR, [beta, E, mp.exp(-K * s), d, u, 1 / R ** 2, 1 / R ** 3]):
                th[g][t] = float(v)
        return th, J


def J_mp(p, dps=40):
    return theta_mp(p, dps)[1]


# ---------------------------------------------------------------- interval-coefficient affine forms
def imul(al, ah, bl, bh):
    p1, p2, p3, p4 = al * bl, al * bh, ah * bl, ah * bh
    return dn(np.minimum(np.minimum(p1, p2), np.minimum(p3, p4))), up(np.maximum(np.maximum(p1, p2), np.maximum(p3, p4)))


def mag(lo, hi):
    return np.maximum(np.abs(lo), np.abs(hi))


def _pairwise(x, rnd):
    """sum over the last axis, every addition rounded by rnd (dn or up)"""
    while x.shape[-1] > 1:
        if x.shape[-1] % 2:
            x = np.concatenate([x, np.zeros(x.shape[:-1] + (1,))], axis=-1)
        x = rnd(x[..., 0::2] + x[..., 1::2])
    return x[..., 0]


def usum(x):
    return _pairwise(x, up)


def dsum(x):
    return _pairwise(x, dn)


class AF:
    __slots__ = ("cl", "ch", "al", "ah", "r")

    def __init__(self, cl, ch, al, ah, r):
        self.cl, self.ch, self.al, self.ah, self.r = cl, ch, al, ah, r

    @staticmethod
    def const(lo, hi=None, shape=()):
        lo = np.broadcast_to(np.asarray(lo, dtype=float), shape).copy()
        hi = lo.copy() if hi is None else np.broadcast_to(np.asarray(hi, dtype=float), shape).copy()
        assert np.all(lo <= hi)
        z = np.zeros(shape + (m,))
        return AF(lo, hi, z, z.copy(), np.zeros(shape))

    @staticmethod
    def rat(q, shape=()):
        return AF.const(fl_dn(q), fl_up(q), shape)

    def S(self):
        return usum(mag(self.al, self.ah))

    def range(self):
        s = up(self.S() + self.r)
        return dn(self.cl - s), up(self.ch + s)

    def __add__(self, o):
        if not isinstance(o, AF):
            o = AF.const(o)
        return AF(dn(self.cl + o.cl), up(self.ch + o.ch), dn(self.al + o.al), up(self.ah + o.ah), up(self.r + o.r))

    def __neg__(self):
        return AF(-self.ch, -self.cl, -self.ah, -self.al, self.r)

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        if not isinstance(o, AF):
            o = AF.const(o)
        cl, ch = imul(self.cl, self.ch, o.cl, o.ch)
        # quadratic part: 1/2 sum_k ax_k ay_k goes to the centre
        ql, qh = imul(self.al, self.ah, o.al, o.ah)
        cl = dn(cl + dn(0.5 * dsum(ql)))          # dn/up also cover underflow in the halving
        ch = up(ch + up(0.5 * usum(qh)))
        a1l, a1h = imul(self.cl[..., None], self.ch[..., None], o.al, o.ah)
        a2l, a2h = imul(o.cl[..., None], o.ch[..., None], self.al, self.ah)
        al, ah = dn(a1l + a2l), up(a1h + a2h)
        mx, my = mag(self.al, self.ah), mag(o.al, o.ah)
        Sx, Sy = usum(mx), usum(my)
        # |Q - 1/2 sum ax ay| <= Sx Sy - 1/2 sum_k mx_k my_k
        nl = up(up(Sx * Sy) - dn(0.5 * dsum(dn(mx * my))))
        nl = np.maximum(nl, 0.0)
        mcx, mcy = mag(self.cl, self.ch), mag(o.cl, o.ch)
        r = up(nl + up(o.r * up(mcx + Sx)))
        r = up(r + up(self.r * up(mcy + Sy)))
        r = up(r + up(self.r * o.r))
        return AF(cl, ch, al, ah, r)

    def col(self):
        return AF(self.cl[:, None], self.ch[:, None], self.al[:, None, :], self.ah[:, None, :], self.r[:, None])

    def row(self):
        return AF(self.cl[None, :], self.ch[None, :], self.al[None, :, :], self.ah[None, :, :], self.r[None, :])


def outer(x, y):
    return x.col() * y.row()


def recip1p(w):
    """AF of 1/(1+w) for an AF w with range inside (-1, inf):
    f(w) = alpha w + h(w), h = f - alpha w convex; max h at an end point (interval evaluation),
    min h >= 2 sqrt(-alpha) + alpha for all w > -1 (AM-GM: 1/v + c v >= 2 sqrt(c), v = 1 + w)."""
    lo, hi = w.range()
    lo, hi = float(lo), float(hi)
    assert lo > -1 + 1e-9
    if hi - lo < 1e-12:
        v = 1 / (1 + iv.mpf([lo, hi]))
        return AF.const(fl_dn(ivlo(v)), fl_up(ivhi(v)))
    alpha = (1 / (1 + hi) - 1 / (1 + lo)) / (hi - lo)
    assert alpha < 0
    A = iv.mpf(alpha)
    hmax = max(ivhi(1 / (1 + iv.mpf(x)) - A * iv.mpf(x)) for x in (lo, hi))
    hmin = ivlo(2 * iv.sqrt(-A) + A)
    return w * AF.const(alpha) + AF.const(fl_dn(hmin), fl_up(hmax))


def param_forms(lo, hi):
    """theta_k = c_k + rad_k eps_k covering [lo_k, hi_k] (checked exactly)"""
    par = {}
    for gi, g in enumerate(GR):
        par[g] = []
        for t in range(T):
            l, h = float(lo[g][t]), float(hi[g][t])
            assert l <= h
            c = 0.5 * (l + h)
            rad = float(up(max(h - c, c - l)))
            assert Fr(c) - Fr(rad) <= Fr(l) and Fr(c) + Fr(rad) >= Fr(h)
            a = np.zeros(m)
            a[gi * T + t] = rad
            par[g].append(AF(np.array(c), np.array(c), a, a.copy(), np.array(0.0)))
    return par


def psi_af(lo, hi):
    par = param_forms(lo, hi)
    K = AF.const(K_LO, K_HI)
    K2 = K * K
    c01, c75, c250, c500 = AF.rat(Fr(1, 10)), AF.const(0.75), AF.const(250.0), AF.const(500.0)
    zv, zm = AF.const(0.0, shape=(n,)), AF.const(0.0, shape=(n, n))
    gs, Hs, gc, Hc, gR, HR, HJ = zv, zm, zv, zm, zv, zm, zm
    one = AF.const(1.0)
    for t in range(T):
        ev = np.zeros(n)
        ev[t] = 1.0
        e = AF.const(ev, shape=(n,))
        beta, phi, d, u, v2, v3 = (par[g][t] for g in ["beta", "phi", "d", "u", "v2", "v3"])
        E = one if t == 0 else par["E"][t]
        io = recip1p(K * beta * phi)
        kap = phi * io
        gb = e * (c01 * E) - gc * (K * beta)
        Hb = (outer(gc, gc) * K2 - Hc * K) * beta - (outer(e, gc) + outer(gc, e)) * (c01 * K * E)
        gs = gs * (c75 * io) + gb * kap
        Hs = Hs * (c75 * io) + Hb * kap - (outer(gb, gs) + outer(gs, gb)) * (K * kap) + outer(gs, gs) * (K2 * beta * kap)
        gc, Hc = gc + gs, Hc + Hs
        gtd = AF.const([fl_dn(q) for q in GTD_Q[t]], [fl_up(q) for q in GTD_Q[t]], shape=(n,))
        gd = gtd - gs
        Hd = -Hs
        gR, HR = gR - gd, HR - Hd
        gq = e + gR * (c250 * v2)
        Hq = HR * (c250 * v2) - outer(gR, gR) * (c500 * v3)
        HJ = HJ + (Hd * u + Hq * d + outer(gd, gq) + outer(gq, gd)) * AF.rat(DELTA_Q[t])
    return HJ


# ---------------------------------------------------------------- exact matrix test
def _int_scale(x):
    """exact integers N and common exponent L with x = N / 2^L (x: float array)"""
    rat = [float(v).as_integer_ratio() for v in np.ravel(x)]
    L = max(max(d.bit_length() - 1 for _, d in rat), 0)
    ints = [num << (L - (d.bit_length() - 1)) for num, d in rat]
    return np.array(ints, dtype=object).reshape(np.shape(x)), L


def point_form(H):
    """C, A (m, n, n), R: Psi(theta(eps)) = C + sum eps_k A_k + Delta, |Delta| <= R entrywise,
    all float; upper triangle mirrored (the true Psi is symmetric)."""
    C = 0.5 * (H.cl + H.ch)
    A = 0.5 * (H.al + H.ah)
    radc = up(np.maximum(H.ch - C, C - H.cl))
    rada = up(np.maximum(H.ah - A, A - H.al))
    R = up(up(H.r + radc) + usum(rada))
    iu = np.triu_indices(n)
    Cs, Rs, As = np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n, m))
    Cs[iu], Rs[iu], As[iu] = C[iu], R[iu], A[iu]
    il = np.tril_indices(n, -1)
    Cs[il], Rs[il] = Cs.T[il], Rs.T[il]
    As[il] = np.swapaxes(As, 0, 1)[il]
    return Cs, np.moveaxis(As, -1, 0), Rs


def float_estimate(C, A, R):
    Xs = np.zeros((n, n))
    for k in range(A.shape[0]):
        if np.any(A[k]):
            w, V = np.linalg.eigh(A[k])
            Xs += (V * np.abs(w)) @ V.T
    rho = np.linalg.eigvalsh(R)[-1]
    return float(np.linalg.eigvalsh(C + Xs)[-1] + rho)


def exact_test(C, A, R, mu=Fr(1, 1000)):
    """True if -C - sum_k X_k - (rho_bar + mu) I is positive definite in exact arithmetic, where
    X_k = V|L|V^T + e_k I >= +-A_k (e_k >= ||A_k - V L V^T||_inf) and rho_bar >= rho(R)."""
    # rho_bar: Collatz-Wielandt, exact
    w, V = np.linalg.eigh(R)
    x = np.maximum(np.abs(V[:, -1]), 1e-6)
    xq = [Fr(v) for v in x]
    Rq = [[Fr(float(R[i, j])) for j in range(n)] for i in range(n)]
    rho_bar = max(sum(Rq[i][j] * xq[j] for j in range(n)) / xq[i] for i in range(n))
    # sum of X_k in exact arithmetic (integers with a common power-of-two scale per k)
    Xsum = [[Fr(0)] * n for _ in range(n)]
    esum = Fr(0)
    for k in range(A.shape[0]):
        Ak = A[k]
        if not np.any(Ak):
            continue
        lam, Vk = np.linalg.eigh(Ak)
        Vi, LV = _int_scale(Vk)
        Li, LL = _int_scale(lam)
        Ai, LA = _int_scale(Ak)
        S = 2 * LV + LL
        P = [[0] * n for _ in range(n)]      # V diag(lam) V^T * 2^S
        Q = [[0] * n for _ in range(n)]      # V diag(|lam|) V^T * 2^S
        absL = [abs(v) for v in Li]
        for i in range(n):
            for j in range(i, n):
                sp = 0
                sq = 0
                for l in range(n):
                    vv = Vi[i, l] * Vi[j, l]
                    sp += vv * Li[l]
                    sq += vv * absL[l]
                P[i][j] = P[j][i] = sp
                Q[i][j] = Q[j][i] = sq
        Sc = max(S, LA)
        ek = Fr(0)
        for i in range(n):
            row = 0
            for j in range(n):
                row += abs((Ai[i, j] << (Sc - LA)) - (P[i][j] << (Sc - S)))
            ek = max(ek, Fr(row, 1 << Sc))
        esum += ek
        for i in range(n):
            for j in range(i, n):
                Xsum[i][j] += Fr(Q[i][j], 1 << S)
    Mq = [[-Fr(float(C[i, j])) - Xsum[min(i, j)][max(i, j)] for j in range(n)] for i in range(n)]
    for i in range(n):
        Mq[i][i] -= esum + rho_bar + mu
    # exact Gaussian elimination without pivoting (full matrix); all pivots > 0 <=> PD
    Mw = [row[:] for row in Mq]
    for k in range(n):
        piv = Mw[k][k]
        if piv <= 0:
            return False, float(rho_bar)
        for i in range(k + 1, n):
            f = Mw[i][k] / piv
            if f:
                for j in range(k + 1, n):
                    Mw[i][j] -= f * Mw[k][j]
    return True, float(rho_bar)
