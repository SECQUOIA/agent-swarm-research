"""Check of the explicit n=1 construction (Theorem C) on random d=2 instances.

sigma* maximizes sigma*ceil(N(sigma)/2), N(sigma) = #{j : V_j >= sigma}; J = [a,b];
query point: level k = floor((a+b)/2), on the segment joining the centroids of C_a, C_b.
Guarantee: depth >= g_d * sigma* * ceil(N/2)  (g_2 = 4/9).
"""
import numpy as np
from midepth import *
from search_random import rand_instance

g = 4/9
rng = np.random.default_rng(7)
out = []
for trial in range(150):
    P = rand_instance(rng)
    zs, F = slice_polytope(P)
    if len(F) < 3:
        continue
    S = MISet(F, zs, ntheta=240, nphi=121)
    V = S.v
    best = (0, None)
    for s in V:
        J = [j for j, v in zip(zs, V) if v >= s]
        val = s*np.ceil(len(J)/2)
        if val > best[0]:
            best = (val, J)
    val, J = best
    a, b = min(J), max(J)
    ca, cb = centroid(F[zs.index(a)]), centroid(F[zs.index(b)])
    k = (a + b)//2
    y = ca + (cb - ca)*((k - a)/(b - a) if b > a else 0.0)
    dep = S.depth(k, y, refine=True)
    out.append((g*val/S.nu, dep/S.nu, S.nu))
out = np.array(out)
print("instances", len(out))
print("min guaranteed/nu", out[:,0].min(), " (theory: >= g_2/kappa_2 ~ 0.0992; rigorous g_2/(2(1+e)) =", g/(2*(1+np.e)), ")")
print("violations:", int(np.sum(out[:,1] < out[:,0]*(1-1e-6))), " min ratio actual/guaranteed:", (out[:,1]/out[:,0]).min())
