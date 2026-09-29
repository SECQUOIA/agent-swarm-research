"""Sanity check of the line-lemma construction (n=1, d=2) on random instances.

For each instance: compute fiber max Tukey depths M_j (unnormalized), pick the
best threshold tau, build the segment between max-depth-region points at the
extreme levels of J_tau, check D(j, l(j)) >= tau along it, and compare the
guaranteed bound tau*ceil(N/2) with a numerically computed depth of (k, l(k)).
"""
import numpy as np
from scipy.optimize import minimize
from midepth import *
from search_random import rand_instance

TH = np.linspace(0, 2*np.pi, 720, endpoint=False)
AA = np.stack([np.cos(TH), np.sin(TH)], 1)

def fiber_depth(V, x):
    # unnormalized Tukey depth of x in polygon V (grid over directions; upper bound)
    e = np.roll(V, -1, 0) - V; w = x - V
    if np.any(e[:,0]*w[:,1] - e[:,1]*w[:,0] < -1e-12):
        return 0.0
    return clip_area(V, AA, AA @ x).min()

def max_depth_point(V):
    c = centroid(V)
    r = minimize(lambda x: -fiber_depth(V, x), c, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-12))
    x = r.x if -r.fun >= fiber_depth(V, c) else c
    return x, fiber_depth(V, x)

def region_point(V, tau, toward):
    # a point with depth >= tau, as close as possible to 'toward' (bisection on the segment from the deepest point)
    x0, m = max_depth_point(V)
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo+hi)/2
        if fiber_depth(V, x0 + mid*(toward - x0)) >= tau: lo = mid
        else: hi = mid
    return x0 + lo*(toward - x0)

rng = np.random.default_rng(123)
rows = []
for trial in range(400):
    P = rand_instance(rng)
    zs, F = slice_polytope(P)
    if len(F) < 3: continue
    S = MISet(F, zs, ntheta=120, nphi=61)
    M = np.array([max_depth_point(V)[1] for V in F])
    best = (0, None)
    for tau in M:
        J = [j for j, m in zip(zs, M) if m >= tau*(1-1e-9)]
        N = len(J)
        val = tau*int(np.ceil(N/2))
        if val > best[0]: best = (val, tau, J)
    val, tau, J = best
    a, b = min(J), max(J)
    Va, Vb = F[zs.index(a)], F[zs.index(b)]
    xa, _ = max_depth_point(Va); xb, _ = max_depth_point(Vb)
    ell = lambda j: xa + (xb - xa)*(j - a)/(b - a) if b > a else xa
    dmin = min(fiber_depth(F[zs.index(j)], ell(j)) for j in J)
    k = J[(len(J)-1)//2]
    true_depth = S.depth(k, ell(k), refine=True)
    rows.append((val/S.nu, true_depth/S.nu, dmin/tau, len(zs)))
rows = np.array(rows)
print("instances", len(rows))
print("min over instances of guaranteed bound/nu:", rows[:,0].min())
print("violations (true depth < bound):", np.sum(rows[:,1] < rows[:,0] - 1e-6))
print("min D along line / tau:", rows[:,2].min(), "(should be >= 1 up to grid error)")
print("min ratio true/bound:", (rows[:,1]/rows[:,0]).min())
