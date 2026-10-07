"""Local convexity certificate around a near-optimal input point (verifier's own code).

  python3 kan_local.py <name> '<u-json>' <halfwidth> [<halfwidth> ...]

For the box B = u +- r (clipped to the input box) it proves:
  1. every edge argument range over B (layer 1: the input interval; layer 2:
     the natural enclosure of h_j over B, intersected with [L_j, U_j]) meets
     exactly one admissible knot interval (outward-rounded), so V is one
     smooth function on B (layer-2 ranges: natural enclosure over B, not
     intersected with [L_j, U_j], because Taylor segments may leave it);
  2. the interval Hessian [H] of V over B satisfies
     lambda_min(Hc) - ||Rad||_F > 0, with lambda_min(Hc) > mu proved by an
     exact rational LDL^T of (Hc - mu I);
then for u' in B cap R:  V(u') >= V(u) + g.s + lam |s|^2 / 2 >= V(u) - |g|^2/(2 lam),
with g an interval enclosure of grad V(u).  Prints the certified lower bound
LB_B for min over B cap R.
"""
import json
import sys
from fractions import Fraction as Fr

import numpy as np

from kan_bnb import Iv, Model, dn, silu_d1_rng, silu_d2_nat, up


def ldl_pd(Mq):
    """exact LDL^T positive-definiteness test of a symmetric rational matrix"""
    n = len(Mq)
    A = [row[:] for row in Mq]
    for k in range(n):
        if A[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return True


def certify(M, u, r):
    d, nh = M.d, M.nh
    lo = np.maximum(u - r, M.ulo)
    hi = np.minimum(u + r, M.uhi)
    N = 1
    # layer 1 over B: phi', phi'' and value ranges; unique pieces
    H = Iv(M.beta.lo[None, :].copy(), M.beta.hi[None, :].copy())
    d1, d2 = [], []
    for i in range(d):
        L = M.L1[i]
        U = Iv(np.full((N, nh), lo[i]), np.full((N, nh), hi[i]))
        kmin, kmax = L.krange(U)
        if not np.all(kmin == kmax):
            return None, "layer-1 edge of input %d meets more than one knot interval" % i
        k = kmin
        H = H + L.natural(U, kmin, kmax)
        d1.append(L.phi_d1_rng(k, U))
        d2.append(L.phi_d2_rng(k, U))
    # the Taylor segment stays in B but h(segment) may leave [L_j, U_j]: use the
    # unrestricted enclosure H of h over B for the layer-2 derivatives
    Hp = H
    L2 = M.L2
    kmin, kmax = L2.krange(Hp)
    if not np.all(kmin == kmax):
        return None, "layer-2 edge meets more than one knot interval"
    k2 = kmin
    p1 = L2.phi_d1_rng(k2, Hp)            # psi'
    p2 = L2.phi_d2_rng(k2, Hp)            # psi''
    Alo, Ahi = M.A
    Aiv = Iv(np.array([Alo]), np.array([Ahi]))
    # interval Hessian
    Hlo = np.zeros((d, d))
    Hhi = np.zeros((d, d))
    for a in range(d):
        for b in range(d):
            t = p2 * d1[a] * d1[b]
            if a == b:
                t = t + p1 * d2[a]
            s = Iv(M._sum_dn(t.lo), M._sum_up(t.hi))
            s = s * Aiv
            Hlo[a, b], Hhi[a, b] = s.lo[0], s.hi[0]
    Hc = [[Fr(float(0.5 * Hlo[a, b] + 0.5 * Hhi[a, b])) for b in range(d)] for a in range(d)]
    # radius (exact rational upper bound)
    rad2 = Fr(0)
    for a in range(d):
        for b in range(d):
            ra = max(Fr(float(Hhi[a, b])) - Hc[a][b], Hc[a][b] - Fr(float(Hlo[a, b])))
            rad2 += ra * ra
    ev = np.linalg.eigvalsh(np.array([[float(x) for x in row] for row in Hc]))
    mu = Fr(float(ev[0])) * Fr(99, 100)
    if mu <= 0 or not ldl_pd([[Hc[a][b] - (mu if a == b else 0) for b in range(d)] for a in range(d)]):
        return None, "midpoint Hessian not certified PD (eigs %s)" % ev
    # lam = mu - ||Rad||_F  (need ||Rad||_F < mu  <=>  rad2 < mu^2)
    if rad2 >= mu * mu:
        return None, "Hessian variation too large: ||Rad||_F^2 %.3g >= mu^2 %.3g" % (float(rad2), float(mu * mu))
    # lower bound on sqrt(rad2) is not needed; upper bound: use a rational upper bound of sqrt
    rf = Fr(float(np.sqrt(float(rad2)))) * Fr(1000001, 1000000)
    assert rf * rf >= rad2
    lam = mu - rf
    # gradient and value at u
    uu = u[None, :]
    lb, ub, _, _ = M.evaluate(uu, uu)
    Hh = Iv(M.beta.lo[None, :].copy(), M.beta.hi[None, :].copy())
    g1 = []
    for i in range(d):
        L = M.L1[i]
        x = np.full((1, nh), u[i])
        kmin, kmax = L.krange(Iv(x, x))
        k = L.kref(x, kmin, kmax)
        Hh = Hh + L.phi_pt(k, x)
        g1.append(L.phi_d1_pt(k, x))
    kmin, kmax = L2.krange(Hh)
    q1 = L2.phi_d1_rng(L2.kref(Hh.mid(), kmin, kmax), Hh)
    g2 = Fr(0)
    for i in range(d):
        t = q1 * g1[i]
        s = Iv(M._sum_dn(t.lo), M._sum_up(t.hi)) * Aiv
        gm = max(abs(Fr(float(s.lo[0]))), abs(Fr(float(s.hi[0]))))
        g2 += gm * gm
    drop = g2 / (2 * lam)
    LB = Fr(float(lb[0])) - drop
    return dict(r=r, lo=list(map(float, lo)), hi=list(map(float, hi)), lam=float(lam), mu=float(mu),
                radF=float(rf), grad2=float(g2), V_lb=float(lb[0]), V_ub=float(ub[0]),
                LB_box=float(dn(np.float64(float(LB))))), "ok"


if __name__ == "__main__":
    name = sys.argv[1]
    u = np.array(json.loads(sys.argv[2]))
    M = Model(name)
    for r in sys.argv[3:]:
        res, msg = certify(M, u, float(r))
        print(name, "halfwidth", r, msg, json.dumps(res) if res else "")
