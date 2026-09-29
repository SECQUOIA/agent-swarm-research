"""E7: integer points of continuous transportation polytopes with fractional
arc capacities (feasible integer supply/demand vectors, continuous flows).

S = { z in Z^V : exists real flow 0 <= xi <= cap on a bipartite graph with
      boundary z }.   S is the integer point set of a real g-polymatroid
(an M-convex polyhedron with fractional data).  We test integral convexity
(a) in M-form: all node coordinates (the set lies in {sum z = 0});
(b) in M-natural form: one sink coordinate dropped.
Hand example (report): sources s1..s3, sinks t1,t2, cap(s_i,t1)=2/3,
cap(s_i,t2)=1/3; x=0 and y=(1,1,1,-2,-1) are feasible but no feasible
integer point lies in N((x+y)/2), so S is not integrally convex in M-form.
"""
import itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from dcheck import ic_violations, INF

rng = np.random.default_rng(2)


def feasible(z, arcs, caps, V):
    E = len(arcs)
    A = np.zeros((V, E))
    for k, (i, j) in enumerate(arcs):
        A[i, k] += 1.0   # out of source i
        A[j, k] -= 1.0   # into sink j
    res = linprog(np.zeros(E), A_eq=A, b_eq=np.array(z, float),
                  bounds=[(0, float(c)) for c in caps], method="highs")
    return res.status == 0


def point_set(arcs, caps, V, drop):
    out_cap = [sum(float(c) for (i, j), c in zip(arcs, caps) if i == v) for v in range(V)]
    in_cap = [sum(float(c) for (i, j), c in zip(arcs, caps) if j == v) for v in range(V)]
    ranges = [range(-int(np.floor(in_cap[v] + 1e-9)), int(np.floor(out_cap[v] + 1e-9)) + 1) for v in range(V)]
    free = [v for v in range(V) if v != drop]
    f = {}
    for zz in itertools.product(*[ranges[v] for v in free]):
        z = [0] * V
        for v, t in zip(free, zz):
            z[v] = t
        if drop is not None:
            z[drop] = -sum(zz)
        ok = (drop is None and sum(zz) == 0) or drop is not None
        f[zz] = 0.0 if ok and feasible(z, arcs, caps, V) else INF
    return f


# hand example
arcs = [(0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4)]
caps = [Fr(2, 3)] * 3 + [Fr(1, 3)] * 3
fM = point_set(arcs, caps, 5, None)
print("hand example, M-form: IC violations =", len(ic_violations(fM)),
      "; feasible:", fM[(0, 0, 0, 0, 0)] == 0, fM[(1, 1, 1, -2, -1)] == 0)
fMn = point_set(arcs, caps, 5, 3)
print("hand example, M-natural form (drop t1): IC violations =", len(ic_violations(fMn)))

stats = {"M": [0, 0], "Mnat": [0, 0]}
ex = None
for trial in range(120):
    ns, nt = int(rng.integers(2, 4)), int(rng.integers(2, 4))
    V = ns + nt
    arcs = [(i, ns + j) for i in range(ns) for j in range(nt) if rng.random() < 0.8]
    if len(arcs) < 3:
        continue
    caps = [Fr(int(rng.integers(1, 7)), 3) for _ in arcs]
    if V <= 5:
        fM = point_set(arcs, caps, V, None)
        if sum(v == 0 for v in fM.values()) > 1:
            stats["M"][0] += 1
            vi = ic_violations(fM)
            stats["M"][1] += bool(vi)
    fMn = point_set(arcs, caps, V, ns)  # drop first sink
    if sum(v == 0 for v in fMn.values()) > 1:
        stats["Mnat"][0] += 1
        vi = ic_violations(fMn)
        stats["Mnat"][1] += bool(vi)
        if vi and ex is None:
            ex = (arcs, [str(c) for c in caps], vi[0])
print("random bipartite (instances, IC-violating):", stats)
print("first M-natural-form counterexample:", ex)
