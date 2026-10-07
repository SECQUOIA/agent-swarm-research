"""Verify adversarial instances: z_K vs SCIP, relative discriminants of the rays, orbit
feasibility just below/above the reported value with Clarabel and SCS, and the best (B)
value found by Nelder-Mead (screen2.analyze)."""
import json, sys, numpy as np, warnings; warnings.filterwarnings('ignore')
from adversarial_ratio import build
from core import bilinear_quadratic, corner_bound, qval, orbit_feasible
from scout_sfree import corner_bound_scip
from screen2 import analyze
Q, b, c = bilinear_quadratic('+')
only = set(int(a) for a in sys.argv[2].split(',')) if len(sys.argv) > 2 else None
for line in open(sys.argv[1]):
    if not line.startswith('{'): continue
    r = json.loads(line)
    if only is not None and r['restart'] not in only: continue
    sbar, P = build(np.array(r['theta'])); w = np.ones(3); g0 = qval(Q, b, c, sbar)
    disc = []
    for j in range(3):
        p = P[:, j]; A = p @ Q @ p; B = 2 * p @ (Q @ sbar + b / 2)
        disc.append(round((B * B - 4 * A * g0) / (B * B + abs(4 * A * g0)), 4))
    zk = corner_bound(Q, b, c, sbar, P, w); zs = corner_bound_scip(Q, b, c, sbar, P, w)
    z = r['final']; feas = {}
    for f in (0.99 * z, 1.01 * z):
        pts = [sbar + f / zk * P[:, j] for j in range(3)]
        feas[round(f, 4)] = [orbit_feasible('+', [sbar], pts, solver=sv) is not None for sv in ('CLARABEL', 'SCS')]
    print('restart', r['restart'], 'reported', round(z, 4), 'rel.disc', disc, 'zK %.6f SCIP %.6f' % (zk, zs), 'feasible(Clarabel,SCS) at 0.99z/1.01z', feas, flush=True)
    print('   ', end=''); analyze('+', sbar, P, w, nm_restarts=10, seed=3)
