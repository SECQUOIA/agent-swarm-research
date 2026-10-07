"""Per-edge cell counts of rule bd (check_bd_qg.py functions, unchanged) on the quadratic path of
Proposition 6, b = 0.8, eps = 1e-6, to see whether 'sqrt(n) cells per edge' holds on every edge or
only on the edges t <= (n+1)/2 covered by the proof.  Float, not exact."""
import sys, numpy as np
sys.path.insert(0, '../../theory-decomposition/adaptive2')
import check_bd_qg as c
eps = 1e-6
for n in (64, 256):
    u, v = c.riccati(n, c.B); q = u + v
    th = np.array([(2 * (n - t) + 1) / (2 * n) for t in range(n + 2)]); p = u - th * q
    for t in sorted(set([1, n // 4, n // 2, (3 * n) // 4, n - 2, n - 1, n])):
        cells = c.bd_cells(p[t], q[t], n, eps)
        K = (n * abs(p[t]) - q[t] / 2) / q[t]
        print("n=%3d edge t=%3d  theta_t=%.3f  K_t=%8.2f  bd cells=%5d  cells/sqrt(n)=%.2f" % (n, t, th[t], K, len(cells), len(cells) / np.sqrt(n)), flush=True)
