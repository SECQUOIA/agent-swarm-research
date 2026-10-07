"""Exact re-check (reviewer) of the reviewer's own float greedy partition (k = 0.5, N = 1000) for
eps/h^2 = 1e-4 and 1e-8, built with target 0.9 eps: node ends converted exactly from floats (consecutive
nodes share the same float end, so the cover has no gaps; the outer ends are checked to be exactly -1, 1),
anchors refined exactly, bounds by the exact closed-form losses."""
import json
from fractions import Fraction as Fr
import numpy as np
from vtoy import traj, node_bound, coord_refine
from v_eps import setup, greedy
k, N = 0.5, 1000
toy, E = setup(k, N)
n = [t for t in range(N) if -1 < E["u"][t] < 1][0]
u0 = np.array([float(v) for v in E["u"]])
h = Fr(2, N)
P = [Fr(-1, 2)] * (N + 1)
for er in (1e-4, 1e-8):
    nodes = None
    for fac in (0.9, 0.95, 0.99, 1.0):
        nodes = greedy(N, k, u0, n, float(E["J"]), fac * er * float(h) ** 2)
        if nodes is not None:
            break
    if nodes is None:
        print(json.dumps(dict(eps_over_h2=er, stuck=True)), flush=True)
        continue
    ends = sorted(set([a for a, b in nodes] + [b for a, b in nodes]))
    cover_ok = ends[0] == -1.0 and ends[-1] == 1.0 and all(any(a == e for a, b in nodes) or e == 1.0 for e in ends)
    worst = None
    for (a, b) in nodes:
        l, r = Fr(a), Fr(b)
        u = list(E["u"])
        u[n] = min(r, max(l, E["u"][n]))
        lo = [Fr(-1)] * N; hi = [Fr(1)] * N
        lo[n], hi[n] = l, r
        A = coord_refine(toy, traj(toy, N, u), lo, hi, list(range(n - 4, n + 5)))
        B, _, _ = node_bound(toy, A, P, lo, hi)
        m = (B - E["J"]) / h ** 2
        worst = m if worst is None or m < worst else worst
    print(json.dumps(dict(eps_over_h2=er, target_factor=fac, n_nodes=len(nodes), cover_ok=bool(cover_ok), worst_exact_bound_minus_J_over_eps=float(worst / Fr(er)))), flush=True)
