"""Referee's own uniform 2^n-ary bisection for separable objectives (recheck).

Model: exact alphaBB, f_B = f - alpha q_B, UBD = f* = 0, prune iff LB(B) >= -eps.
For separable f = sum_i f_i(y_i), LB(B) = sum_i min_{[l_i,u_i]} (f_i - alpha (y-l_i)(u_i-y)),
and each 1D term is convex, so it is minimized by bisection on its (monotone) derivative.
Per level only 2^j intervals per coordinate occur, so the 1D minima are tabulated.
Near-ties |LB + eps| < TIE are re-decided in 60-digit mpmath arithmetic.
Usage: python3 sepbisect.py INSTANCE ALPHA EPS [EPS ...]
Prints one JSON line per eps.
"""
import sys, json
import numpy as np
import mpmath as mp

mp.mp.dps = 60
TIE = 1e-10

# each coordinate: (f, fprime, lo, hi) with numpy-callable f, fprime, and an mpmath f
def quartic():
    return (lambda y: y**4, lambda y: 4*y**3, lambda y: y**4, lambda y: 4*y**3)
def xonemx():
    return (lambda y: y*(1-y), lambda y: 1-2*y, lambda y: y*(1-y), lambda y: 1-2*y)
def lin_quad(a, b):  # a y^2 + b y
    return (lambda y: a*y*y + b*y, lambda y: 2*a*y + b,
            lambda y: a*y*y + b*y, lambda y: 2*a*y + b)

INST = {
    "face4d": ([xonemx(), quartic(), quartic(), quartic()], [0.0, -0.4, -0.4, -0.4], 0.9),
    "bdry":   ([xonemx(), quartic()], [0.0, -0.4], 0.9),
    "vsharp": ([lin_quad(-0.4, 1.0), lin_quad(-0.4, 1.0)], [0.0, 0.0], 1.0),
    "vflat":  ([lin_quad(-0.4, 1.0), lin_quad(1.0, 0.0)], [0.0, 0.0], 1.0),
}

def min1d(f, fp, l, u, alpha):
    """vectorized min over [l,u] of phi = f - alpha (y-l)(u-y) (convex)."""
    dphi = lambda y: fp(y) - alpha*(l + u - 2*y)
    a, b = l.copy(), u.copy()
    for _ in range(80):
        c = 0.5*(a + b)
        pos = dphi(c) > 0
        b = np.where(pos, c, b)
        a = np.where(pos, a, c)
    y = 0.5*(a + b)
    return f(y) - alpha*(y - l)*(u - y)

def min1d_mp(fm, fpm, l, u, alpha):
    l, u, alpha = mp.mpf(l), mp.mpf(u), mp.mpf(alpha)
    dphi = lambda y: fpm(y) - alpha*(l + u - 2*y)
    phi = lambda y: fm(y) - alpha*(y - l)*(u - y)
    if dphi(l) >= 0: return phi(l)
    if dphi(u) <= 0: return phi(u)
    a, b = l, u
    for _ in range(220):
        c = (a + b)/2
        if dphi(c) > 0: b = c
        else: a = c
    return phi((a + b)/2)

def run(name, alpha, eps):
    coords, lo, side = INST[name]
    n = len(coords)
    lo = np.array(lo, float)
    alpha = float(alpha)
    # level 0
    K = np.zeros((1, n), dtype=np.int64)
    processed = 0; nonpruned_per_level = []; ties = 0; flips = 0; minmargin = np.inf
    j = 0
    while len(K):
        s = side / 2**j
        idx = np.arange(2**j)
        tabs = []
        for i, (f, fp, fm, fpm) in enumerate(coords):
            l = lo[i] + idx*s; u = l + s
            tabs.append(min1d(f, fp, l, u, alpha))
        LB = sum(tabs[i][K[:, i]] for i in range(n))
        processed += len(K)
        marg = LB + eps
        minmargin = min(minmargin, float(np.min(np.abs(marg))))
        near = np.nonzero(np.abs(marg) < TIE)[0]
        nonpr = marg < 0
        for t in near:
            ties += 1
            lbm = mp.mpf(0)
            for i, (f, fp, fm, fpm) in enumerate(coords):
                k = int(K[t, i])
                l = mp.mpf(lo[i]) + k*mp.mpf(side)/2**j
                lbm += min1d_mp(fm, fpm, l, l + mp.mpf(side)/2**j, alpha)
            exact_np = (lbm + mp.mpf(eps)) < 0
            if bool(exact_np) != bool(nonpr[t]):
                flips += 1
                nonpr[t] = bool(exact_np)
        P = K[nonpr]
        nonpruned_per_level.append(int(len(P)))
        if len(P) == 0:
            break
        bits = np.array(np.meshgrid(*[[0, 1]]*n, indexing="ij")).reshape(n, -1).T
        K = (2*P[:, None, :] + bits[None, :, :]).reshape(-1, n)
        j += 1
    nonpr_total = sum(nonpruned_per_level)
    return dict(instance=name, alpha=alpha, eps=eps, nodes=processed,
                leaves=processed - nonpr_total, nonpruned_per_level=nonpruned_per_level,
                near_ties=ties, flips=flips, min_abs_margin=minmargin)

if __name__ == "__main__":
    name, alpha = sys.argv[1], sys.argv[2]
    for e in sys.argv[3:]:
        print(json.dumps(run(name, alpha, float(e))), flush=True)
