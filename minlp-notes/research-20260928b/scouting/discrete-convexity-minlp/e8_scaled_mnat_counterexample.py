"""E8: an M-natural-convex set in Z^4 whose 3-scaling is not integrally convex.

S = { sum_i c_i (e_i - e_4) + sum_i k_i e_i : c_i in {0,1,2}, k_i in {0,1}, i=1,2,3 }
is M-natural-convex (Minkowski sum of M-natural segments).  It is the set of
integer boundaries of flows s_i -> t1 (cap 2) and s_i -> t2 (cap 1), with the
t2 coordinate dropped.  Its 3-scaling T = {y : 3y in S} = {0, (1,1,1,-2)}
has two points at l_inf distance 2 and no point of T in N((0+y)/2); so T is
not integrally convex.  Consequently, for the MINLP
    min c^T z  s.t. z in Z^4, z in (1/3) conv(S)   (continuous flows),
with c = (-1,-1,-1,0), z = 0 is an l_inf-neighbourhood local minimum that is
not global.  Also: the fractional-capacity continuous flow set restricted to
integer supplies is the same T.
"""
import itertools
from dcheck import ic_violations, mnat_violations, ninf_false_local_minima, INF

gens = []
for i in range(3):
    g = [0, 0, 0, 0]; g[i] = 1; g[3] = -1
    gens.append((tuple(g), 2))
    h = [0, 0, 0, 0]; h[i] = 1
    gens.append((tuple(h), 1))
S = {(0, 0, 0, 0)}
for g, u in gens:
    S = {tuple(x + k * gi for x, gi in zip(s, g)) for s in S for k in range(u + 1)}
print("|S| =", len(S))


def table(P):
    lo = [min(p[i] for p in P) for i in range(4)]
    hi = [max(p[i] for p in P) for i in range(4)]
    return {p: (0.0 if p in P else INF) for p in itertools.product(*[range(lo[i], hi[i] + 1) for i in range(4)])}


fS = table(S)
print("S: M-natural violations =", len(mnat_violations(fS)), " IC violations =", len(ic_violations(fS)))
T = {tuple(x // 3 for x in s) for s in S if all(x % 3 == 0 for x in s)}
print("T = 3-scaling of S =", sorted(T))
fT = table(T)
print("T: IC violations =", ic_violations(fT))
lin = {p: (-(p[0] + p[1] + p[2]) if v == 0 else INF) for p, v in fT.items()}
print("linear objective -(z1+z2+z3) on T: false N_inf local minima =", ninf_false_local_minima(lin))

# ---------------------------------------------------------------------------
# Part (b): capacity value function.  Super source S -> s_i with integer
# capacity u_i (i = 1..3), s_i -> t1 cap 2/3, s_i -> t2 cap 1/3 (fixed,
# fractional), t1 -> T with integer capacity u_4, t2 -> T uncapacitated.
# v(u) = -(max flow value) with continuous flows (exact rationals via a tiny
# enumeration-free LP in fractions is unnecessary: values are checked with
# HiGHS and printed; the hand computation in the report gives the same).
import numpy as np
from scipy.optimize import linprog
from dcheck import local_ext


def vcap(u):
    # variables: f_i1, f_i2 (i=1..3)
    c = -np.ones(6)
    A, b = [], []
    for i in range(3):
        row = np.zeros(6); row[2 * i] = 1; row[2 * i + 1] = 1
        A.append(row); b.append(u[i])            # supply of s_i <= u_i
    row = np.zeros(6); row[0::2] = 1
    A.append(row); b.append(u[3])                # into t1 <= u_4
    bounds = [(0, 2 / 3), (0, 1 / 3)] * 3
    r = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    return r.fun


F = {p: vcap(p) for p in itertools.product(range(0, 2), range(0, 2), range(0, 2), range(0, 3))}
m = (0.5, 0.5, 0.5, 1.0)
print("capacity value function: v(0) =", F[(0, 0, 0, 0)], " v(1,1,1,2) =", F[(1, 1, 1, 2)],
      " average =", (F[(0, 0, 0, 0)] + F[(1, 1, 1, 2)]) / 2)
print("local convex extension at midpoint (1/2,1/2,1/2,1) =", local_ext(F, m))
print("capacity value function IC violations on {0,1}^3 x {0,1,2}:", len(ic_violations(F)))
