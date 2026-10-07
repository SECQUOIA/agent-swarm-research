"""Independent check of adversarial margin restart 3: maximize the exact orbit bound
z_{C_F}(w) (generalized-eigenvalue step lengths, no SDP) over F by random search + Nelder-Mead."""
import json, numpy as np, warnings; warnings.filterwarnings('ignore')
from scipy.optimize import minimize
from adversarial_ratio import build
from core import bilinear_quadratic, corner_bound, qval, Mmat
from bilinear import step_A, symm
Q, b, c = bilinear_quadratic('+')
r = [json.loads(l) for l in open('../logs/adversarial_ratio_8_margin.log') if l.startswith('{')][3]
sbar, P = build(np.array(r['theta'])); w = np.ones(3)
zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
print('sbar', sbar.round(4), 'q(sbar)', round(qval(Q, b, c, sbar), 5)); print('P', P.round(4)); print('zK', zk, 'lam', lam.round(5), 'cond P %.1f' % np.linalg.cond(P))
def bound(x):
    F = x.reshape(2, 2)
    if np.linalg.det(F) <= 0: return 0.0
    A = symm(F.T @ Mmat('+', sbar))
    if np.linalg.eigvalsh(A)[0] <= 0: return 0.0
    vals = [step_A(F, '+', sbar, P[:, j]) for j in range(3)]
    return min(vals)
rng = np.random.default_rng(0); best = 0; bestx = None
for k in range(20000):
    x = rng.normal(size=4); v = bound(x)
    if v > best: best, bestx = v, x
print('random search best', best)
for k in range(30):
    x0 = bestx + 0.3 * rng.normal(size=4) if k else bestx
    res = minimize(lambda x: -bound(x), x0, method='Nelder-Mead', options=dict(maxiter=3000, xatol=1e-12, fatol=1e-14))
    if -res.fun > best: best, bestx = -res.fun, res.x
print('Nelder-Mead best exact orbit bound', best)
