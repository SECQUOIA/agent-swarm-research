"""Reviewer: KKT point of the COPS catmix transcription with the
bang-singular-bang active set, reached by Newton from a SMOOTH start
(u = u_s on the arc stages), N = 100.  Uses the author's reduced model
catmix_trap.Red only for the objective and gradient (its objective was
checked above against the reviewer's 2-D mpmath code: J of the stored COPS
controls and of the saved saddle agree to 1e-16).  Reports the alternating
content of the result and compares with the author's saved point."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys
import numpy as np
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-bangbang/singular'))
import catmix_trap as C
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
R = C.Red(N)
saved = np.load((_PUBLIC_REPO + '/research-20260929/theory-bangbang/singular/logs/catmix%d_smooth_u.npy') % N)
free = np.where((saved > 1e-9) & (saved < 1 - 1e-9))[0]
us = 0.227142082708498
u = saved.copy()
u[free] = us
def alt_content(v):
    f = v[free]
    return np.max(np.abs(f[1:-1] - 0.5*(f[:-2] + f[2:])))
def gfree(v):
    return R.grad_logJ(v)[1][free]
for it in range(40):
    g = gfree(u)
    Hm = np.zeros((len(free), len(free)))
    e = 1e-6
    for jj, j in enumerate(free):
        up, um = u.copy(), u.copy(); up[j] += e; um[j] -= e
        Hm[:, jj] = (gfree(up) - gfree(um))/(2*e)
    Hm = 0.5*(Hm + Hm.T)
    du = np.linalg.solve(Hm, -g)
    lam = 1.0
    while lam > 1e-8:
        un = u.copy(); un[free] += lam*du
        if np.linalg.norm(gfree(un)) < np.linalg.norm(g)*(1 - 1e-4*lam) + 1e-16:
            break
        lam /= 2
    u = un
    if it < 3 or it % 5 == 0:
        print('it %d |g| %.2e step %.2e lam %g alt-content %.3f' % (it, np.linalg.norm(gfree(u)), np.max(np.abs(lam*du)), lam, alt_content(u)), flush=True)
    if np.linalg.norm(gfree(u)) < 1e-16:
        break
cost = R.simulate(u)[1]
print('final |g|=%.2e  u range on arc [%.4f, %.4f]  alt-content %.3f  J = %.13f' % (np.linalg.norm(gfree(u)), u[free].min(), u[free].max(), alt_content(u), np.exp(cost) - 1))
print('saved point: alt-content %.3f  J = %.13f ; max |u - saved| = %.2e' % (alt_content(saved), np.exp(R.simulate(saved)[1]) - 1, np.max(np.abs(u - saved))))
print('smooth start: gradient projection on the alternating direction vs on a smooth direction:')
u0 = saved.copy(); u0[free] = us
g0 = gfree(u0); n = len(free)
alt = np.array([(-1)**k for k in range(n)])/np.sqrt(n); sm = np.ones(n)/np.sqrt(n)
print('  g.alt = %.2e   g.smooth = %.2e   |g| = %.2e' % (g0@alt, g0@sm, np.linalg.norm(g0)))
