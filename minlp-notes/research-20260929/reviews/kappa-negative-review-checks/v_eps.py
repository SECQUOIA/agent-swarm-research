"""Reviewer's float re-implementation of the greedy epsilon-partition of kappa-negative.md Section 4
(Theorem 4.3 table).  Independent code (numpy); same algorithm as described in the note: central node
[ub - w0, ub + w0] anchored at zbar, then nodes as wide as possible (bisection on the width) whose
bound, with the tangential family P = -k anchored at the node's own (coordinate-descent) optimum, is
>= J(zbar) - eps.  usage: python3 v_eps.py K N [N ...]
"""
import json
import math
import sys
from fractions import Fraction as Fr

import numpy as np

from vtoy import Toy, best_single_switch


def setup(k, N):
    R = 3 if k > 0.5 else 2
    toy = Toy(a_pts=((0, 2), (1, -1)), k_pts=((0, Fr(k)),), phi1=1, phi2=0, R=R)
    E = best_single_switch(toy, N)
    return toy, E


def fsim(N, k, u):
    h = 2.0 / N
    t = np.arange(N)
    a = np.where(2 * t < N, 2.0, -1.0)
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    J = h * np.sum((x[:N] - a) ** 2 / 2 + k * x[:N] * u) + x[N]
    p = np.empty(N + 1)
    p[N] = 1.0
    inc = h * (x[:N] - a + k * u)
    p[:N] = 1.0 + np.cumsum(inc[::-1])[::-1]
    sig = k * x[:N] + p[1:]
    return J, sig, h


def Hjj(N, k, j):
    h = 2.0 / N
    return h * h * (h * (N - 1 - j))


def node_bound(N, k, u0, n, l, r):
    u = u0.copy()
    u[n] = min(r, max(l, u[n]))
    lo = -np.ones(N); hi = np.ones(N)
    lo[n], hi[n] = l, r
    stages = list(range(max(0, n - 4), min(N, n + 5)))
    for _ in range(8):
        changed = False
        for j in stages:
            J, sig, h = fsim(N, k, u)
            H = Hjj(N, k, j)
            g = h * sig[j]
            cands = [lo[j], hi[j]]
            if H > 0:
                cands.append(min(hi[j], max(lo[j], u[j] - g / H)))
            best = min(cands, key=lambda c: g * (c - u[j]) + H * (c - u[j]) ** 2 / 2)
            if g * (best - u[j]) + H * (best - u[j]) ** 2 / 2 < -1e-18:
                u[j] = best
                changed = True
        if not changed:
            break
    J, sig, h = fsim(N, k, u)
    kap = -k
    f = lambda om: h * sig * om + h * h * kap * om * om / 2
    loss = np.maximum(0.0, -np.minimum(f(lo - u), f(hi - u)))
    return J - loss.sum()


def greedy(N, k, u0, n, J0, eps):
    h = 2.0 / N
    ub = u0[n]
    w0 = math.sqrt(2 * eps / (h * h * k))
    l0, r0 = max(-1.0, ub - w0), min(1.0, ub + w0)
    nodes = [(l0, r0)]
    for side in (1, -1):
        edge = r0 if side > 0 else l0
        far = 1.0 if side > 0 else -1.0
        cnt = 0
        while abs(far - edge) > 1e-12:
            def ok(w):
                a, b = (edge, edge + w) if side > 0 else (edge - w, edge)
                return node_bound(N, k, u0, n, a, b) >= J0 - eps
            wmax = abs(far - edge)
            if ok(wmax):
                w = wmax
            else:
                lo_w, hi_w = 0.0, wmax
                for _ in range(40):
                    mid = (lo_w + hi_w) / 2
                    if ok(mid):
                        lo_w = mid
                    else:
                        hi_w = mid
                w = lo_w
            if w <= 1e-12:
                return None
            a, b = (edge, edge + w) if side > 0 else (edge - w, edge)
            nodes.append((a, b))
            edge = b if side > 0 else a
            cnt += 1
            if cnt > 60:
                return None
    return nodes


def main():
    k = float(sys.argv[1])
    for N in [int(v) for v in sys.argv[2:]]:
        toy, E = setup(k, N)
        frac = [t for t in range(N) if -1 < E["u"][t] < 1]
        if not frac:
            print(json.dumps(dict(k=k, N=N, frac=None)))
            continue
        n = frac[0]
        u0 = np.array([float(v) for v in E["u"]])
        J0 = float(E["J"])
        h = 2.0 / N
        q = h * (N - 1 - n)
        rho = 1 + (q + math.sqrt(q * q + q * k)) / k
        row = []
        for er in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8):
            if er * h * h < 100 * 2.2e-16:
                continue
            nodes = greedy(N, k, u0, n, J0, er * h * h)
            w0 = math.sqrt(2 * er / k)
            pred = 1 + sum(math.ceil(math.log(a / w0) / math.log(rho)) for a in (1 - u0[n], 1 + u0[n]) if a > w0)
            row.append((er, None if nodes is None else len(nodes), pred))
        print(json.dumps(dict(k=k, N=N, n=n, u_n=u0[n], q=q, rho_star=rho, counts=row)), flush=True)


if __name__ == "__main__":
    main()
