"""Reviewer's own rigorous 2-D interval branch and bound for the chain end window.

Bound (derived independently in the review):
  f >= B(z1, zN; V, H) = l0 + 3 lN + (V+L) zN - V z1 - G(V+L) + G(V) + (N-1) c,
  l0 = sqrt(eta^2 + (z1-1)^2), lN = sqrt(eta^2 + (zN-3)^2), L = 4 - l0 - lN,
  G(v) = (v sqrt(H^2+v^2) + H^2 asinh(v/H))/2 (increasing in v), c = 2 G(eta).
Domain: |z1 - 1| <= 3 + eta, |zN - 3| <= 3 + eta (from l0 + lN + (N-1)h <= 4, l >= eta).
Necessary condition for feasibility: L >= sqrt((1-h)^2 + (zN-z1)^2) (chord of the interior polyline).
Multipliers (V, H) are chosen per box (any choice is valid) as the maximiser of B at the box centre.
Interval arithmetic: mpmath iv (outward rounded), 30 digits.  Box bound = max(natural extension
with monotone G enclosure, first-order mean-value form around the centre).
"""
import json
import math
import os
import sys
import time

import mpmath as mp
from mpmath import iv
from scipy.optimize import brentq

import v_chain_checks as vc

# research-20260929/ of this checkout (this file is in research-20260929/reviews/<dir>/)
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

iv.dps = 30


def asinh_pos(x):          # x >= 0 interval; increasing
    return iv.log(x + iv.sqrt(x * x + 1))


def asinh_pt(t):           # enclosure of asinh at an exact point t (mpf)
    if t >= 0:
        return asinh_pos(iv.mpf(t))
    return -asinh_pos(iv.mpf(-t))


def G_pt(v, H):            # enclosure of G at an exact point v (mpf), H a point interval
    V = iv.mpf(v)
    return (V * iv.sqrt(H * H + V * V) + H * H * asinh_iv(V / H)) / 2


def asinh_iv(x):
    lo = asinh_pt(x.a).a
    hi = asinh_pt(x.b).b
    return iv.mpf([lo, hi])


def G_iv(v, H):
    """G is increasing in v: enclose by endpoint evaluations."""
    return iv.mpf([G_pt(v.a, H).a, G_pt(v.b, H).b])


class Window:
    def __init__(self, N):
        vc.load(N)                       # structure assertions (eta = 1/(2N) exactly)
        self.N = N
        self.eta = iv.mpf(1) / (2 * N)
        self.h = iv.mpf(1) / N
        self.etaf = 1.0 / (2 * N)
        self.hf = 1.0 / N

    # ------------- multipliers (float; validity does not depend on them) -------------
    def mult(self, z1, zN):
        N, e = self.N, self.etaf
        l0, lN = math.hypot(e, z1 - 1), math.hypot(e, zN - 3)
        L = 4 - l0 - lN
        D = zN - z1
        if L <= abs(D):
            return None
        T = math.sqrt(L * L - D * D) / 2           # = H sinh((N-1) asinh(eta/H))
        if T <= (N - 1) * e * (1 + 1e-13):
            return None

        def logF(t):                               # t = log H
            H = math.exp(t)
            x = (N - 1) * math.asinh(e / H)
            ls = x + math.log1p(-math.exp(-2 * x)) - math.log(2) if x > 1e-3 else math.log(math.sinh(x))
            return t + ls - math.log(T)
        lo, hi = -40.0, 10.0
        t = brentq(logF, lo, hi, xtol=1e-15, rtol=1e-15, maxiter=500)
        H = math.exp(t)
        pm = math.atanh(D / L)
        V = H * math.sinh(pm - (N - 1) * math.asinh(e / H))
        return V, H

    # ------------- interval pieces -------------
    def pieces(self, Z1, ZN):
        l0 = iv.sqrt(self.eta ** 2 + (Z1 - 1) ** 2)
        lN = iv.sqrt(self.eta ** 2 + (ZN - 3) ** 2)
        return l0, lN, 4 - l0 - lN

    def B(self, Z1, ZN, V, H):
        l0, lN, L = self.pieces(Z1, ZN)
        Vi, Hi = iv.mpf(V), iv.mpf(H)
        c = 2 * G_iv(self.eta, Hi)
        return l0 + 3 * lN + (Vi + L) * ZN - Vi * Z1 - G_iv(Vi + L, Hi) + G_iv(Vi, Hi) + (self.N - 1) * c

    def grad(self, Z1, ZN, V, H):
        l0, lN, L = self.pieces(Z1, ZN)
        Vi, Hi = iv.mpf(V), iv.mpf(H)
        g = iv.sqrt(Hi * Hi + (Vi + L) ** 2)       # G'(V+L)
        d0 = (Z1 - 1) / l0                          # d l0 / d z1 ;  dL/dz1 = -d0
        dN = (ZN - 3) / lN                          # d lN / d zN ;  dL/dzN = -dN
        g1 = d0 - d0 * ZN - Vi + g * d0
        gN = 3 * dN + (Vi + L) - dN * ZN + g * dN
        return g1, gN

    def infeasible(self, Z1, ZN):
        l0, lN, L = self.pieces(Z1, ZN)
        if L.b < 0:
            return True
        d = ZN - Z1
        dmin = 0 if (d.a <= 0 <= d.b) else min(abs(d.a), abs(d.b))
        chord2 = (1 - self.h) ** 2 + iv.mpf(dmin) ** 2
        return iv.mpf(L.b) ** 2 < chord2 and (iv.mpf(L.b) ** 2).b < chord2.a

    def box_lb(self, a1, b1, aN, bN, mult):
        Z1, ZN = iv.mpf([a1, b1]), iv.mpf([aN, bN])
        V, H = mult
        nat = self.B(Z1, ZN, V, H).a
        m1, mN = mp.mpf((a1 + b1) / 2), mp.mpf((aN + bN) / 2)
        Bc = self.B(iv.mpf(m1), iv.mpf(mN), V, H)
        g1, gN = self.grad(Z1, ZN, V, H)
        mv = (Bc + g1 * (Z1 - m1) + gN * (ZN - mN)).a
        return max(nat, mv)

    def run(self, target, max_boxes=3_000_000, min_w=1e-13):
        t0 = time.time()
        e = 3 + self.etaf
        root = (1 - e - 1e-9, 1 + e + 1e-9, 3 - e - 1e-9, 3 + e + 1e-9)
        stack = [(root, None)]
        nb = ninf = 0
        worst = mp.inf
        unresolved = []
        while stack:
            (a1, b1, aN, bN), pm = stack.pop()
            nb += 1
            if nb > max_boxes:
                raise RuntimeError("box limit")
            if self.infeasible(iv.mpf([a1, b1]), iv.mpf([aN, bN])):
                ninf += 1
                continue
            mult = self.mult((a1 + b1) / 2, (aN + bN) / 2)
            if mult is None:
                for s, t in ((0, 0), (0, 1), (1, 0), (1, 1), (.5, 0), (.5, 1), (0, .5), (1, .5)):
                    mult = self.mult(a1 + s * (b1 - a1), aN + t * (bN - aN))
                    if mult is not None:
                        break
            if mult is None:
                mult = pm
            if mult is None:
                lb = -mp.inf
            else:
                lb = self.box_lb(a1, b1, aN, bN, mult)
            if lb >= target:
                worst = min(worst, lb)
                continue
            if max(b1 - a1, bN - aN) < min_w:
                unresolved.append(((a1, b1, aN, bN), float(lb)))
                worst = min(worst, lb)
                continue
            if b1 - a1 >= bN - aN:
                m = (a1 + b1) / 2
                stack += [((a1, m, aN, bN), mult), ((m, b1, aN, bN), mult)]
            else:
                m = (aN + bN) / 2
                stack += [((a1, b1, aN, m), mult), ((a1, b1, m, bN), mult)]
        return dict(N=self.N, target=target, boxes=nb, infeasible=ninf, unresolved=len(unresolved),
                    min_leaf_lb=mp.nstr(worst, 20), certified_bound=float(worst) if not unresolved else None,
                    seconds=round(time.time() - t0, 1))


if __name__ == "__main__":
    gap = float(sys.argv[1])
    for N in [int(v) for v in sys.argv[2:]]:
        W = Window(N)
        path = os.path.join(R29, "open-instances-wave2/cops/logs/chain%d_primal.txt") % N
        m, eta = vc.load(N)
        pc = vc.primal_check(N, m, eta, path)
        fp = float(mp.mpf(pc["obj"]))
        # value of B at the primal's end values with its best multipliers (tightness check)
        X = [float(s) for s in open(path).read().split()]
        z1 = X[0] + W.etaf * X[N + 1]              # z_1 = x_0 + eta u_0
        zN = X[N] - W.etaf * X[2 * N + 1]
        mu = W.mult(z1, zN)
        Bp = W.B(iv.mpf(z1), iv.mpf(zN), *mu)
        res = W.run(fp - gap)
        res.update(primal_obj=pc["obj"], B_at_primal_ends=mp.nstr(Bp.a, 20), mult_at_primal_ends=mu)
        print(json.dumps(res), flush=True)
