"""E10: explicit family showing the closure of ALL constant-Gamma (symmetric) maximal
quadratic-free sets has unbounded approximation factor w.r.t. the quadratic corner hull.
S = {y^2 >= x^2 + 1}, xbar = 0, rays toward T1 = (a, r) and (slightly rotated) T2 = (-a, -r),
r = sqrt(1+a^2), w = (1, 1).  Oblique split {|y - a x / r| <= 1/r} (non-constant Gamma) is optimal."""
import numpy as np
from scipy.optimize import linprog
from sfree import corner_bound, step_length

Q = np.diag([1.0, -1.0]); b = np.zeros(2); c = 1.0; sbar = np.zeros(2)
phis = np.linspace(1e-6, np.pi - 1e-6, 20001)
for a in [1, 3, 10, 30, 100]:
    r = np.sqrt(1 + a * a)
    eta = 1e-3
    r1 = np.array([a, r]); r2 = np.array([-a, -r]) + eta * np.array([r, -a]) / r
    P = np.stack([r1, r2], 1); w = np.array([1.0, 1.0])
    zk = corner_bound(Q, b, c, sbar, P, w)
    cuts = []
    for ph in phis:
        g1, g2 = np.cos(ph), np.sin(ph)
        G = lambda s: max(s[1] - (g1 * s[0] + g2), -s[1] - (g1 * s[0] + g2))
        al = [step_length(G, sbar, P[:, j]) for j in range(2)]
        cuts.append([0 if not np.isfinite(x) else 1 / x for x in al])
    cuts = np.array(cuts)
    lp = linprog(w, A_ub=-cuts, b_ub=-np.ones(len(cuts)), bounds=[(0, None)] * 2, method='highs')
    # oblique split: y <= (a x + 1)/r and y >= (a x - 1)/r
    Gs = lambda s: max(s[1] - (a * s[0] + 1) / r, (a * s[0] - 1) / r - s[1])
    als = [step_length(Gs, sbar, P[:, j]) for j in range(2)]
    zsplit = min(w[j] * als[j] for j in range(2) if np.isfinite(als[j]))
    print(f"a={a:5}: z_K={zk:.5f}  split cut bound={zsplit:.5f}  closure(all symmetric)={lp.fun:.5f}  ratio={lp.fun/zk:.5f}  2/(2+2a^2)={2/(2+2*a*a):.5f}")
