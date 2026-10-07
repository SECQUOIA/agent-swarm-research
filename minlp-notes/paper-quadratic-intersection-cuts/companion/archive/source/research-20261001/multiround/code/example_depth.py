"""Proposition D (bound-optimal sets can have vanishing depth at a fixed violation).

S = {(x, y, w) : w <= x y}, sbar = (0, 0, 1) (q(sbar) = 1), rays p1 = e_y, p2 = e_x, p3 = e_w,
reduced costs w = (1, eps, 1).  Claims checked here:
  (a) exact: z_K = 2 sqrt(eps), attained at lam = (sqrt(eps), 1/sqrt(eps), 0) (sympy);
  (b) exact: SCIP's Case-4 set at sbar is {w >= (x + y)^2 / 4}; it is S-free because
      (x + y)^2/4 - x y = (x - y)^2/4 >= 0; its steps are (2, 2, inf) (sympy), and the
      Python model of SCIP's set (scout_sfree.ms_set) gives the same steps numerically;
  (c) numerical: the best orbit set (bisection, as in the loop) has alpha1 * alpha2 <= 4 and
      alpha1 ~ sqrt(eps), while the geo and pertE0.1 rules keep alpha1 bounded below.
"""
import numpy as np
import sympy as sp
import mrcore as M

x, y, w, t, e = sp.symbols('x y w t epsilon', positive=True)
# (a) min l1 + eps l2 s.t. l1 l2 >= 1 (the e_w ray only increases q): AM-GM
l1 = sp.sqrt(e); l2 = 1 / sp.sqrt(e)
assert sp.simplify(l1 * l2 - 1) == 0
print('(a) z_K = l1 + eps*l2 =', sp.simplify(l1 + e * l2), '(AM-GM: l1 + eps l2 >= 2 sqrt(eps l1 l2) >= 2 sqrt(eps))')
# (b) SCIP set: x_hat = ((x-y)/2, (w+1)/2), y_hat = ((x+y)/2, (w-1)/2), lambda = x_hat(sbar)/|x_hat(sbar)| = (0, 1)
xh = sp.Matrix([(x - y) / 2, (w + 1) / 2]); yh = sp.Matrix([(x + y) / 2, (w - 1) / 2])
assert sp.expand(xh.dot(xh) - yh.dot(yh) - (w - x * y)) == 0
G = sp.expand(yh.dot(yh) - ((w + 1) / 2) ** 2)          # |y_hat|^2 <= (lambda^T x_hat)^2, lambda^T x_hat >= 0
print('(b) SCIP set: |y_hat|^2 - (lambda^T x_hat)^2 =', sp.factor(G), ' i.e. {w >= (x+y)^2/4}')
assert sp.expand(G - ((x + y) ** 2 / 4 - w)) == 0
assert sp.expand((x + y) ** 2 / 4 - x * y - (x - y) ** 2 / 4) == 0
for name, d in (('e_y', (0, t, 1)), ('e_x', (t, 0, 1))):
    sol = sp.solve(sp.Eq((d[0] + d[1]) ** 2 / 4, d[2]), t)
    print('    step along %s: %s' % (name, sol))
Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = -0.5
sbar = np.array([0.0, 0.0, 1.0]); P = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]).T
print('    Python model of SCIP set, steps:', M.scip_alpha('+', sbar, P))

# (c) numerical
print('\n(c)   eps      z_K      2sqrt(eps) | orbit: alpha1    alpha2    a1*a2   z_C/z_K | geo alpha1 | pertE0.1 alpha1')
R = P.copy()
for eps in [1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
    wv = np.array([1.0, eps, 1.0])
    zk = M.zk_vec('+', sbar, P, wv)
    al, F, _ = M.orbit_alpha('+', sbar, P, wv)
    zc = min(wv[j] * al[j] for j in range(3) if np.isfinite(al[j]))
    nr = np.linalg.norm(R, axis=0)
    ag, _, _ = M.orbit_alpha('+', sbar, P, nr)
    rate = wv / nr; u = nr * (rate / rate.max() + 0.1)
    ap, _, _ = M.orbit_alpha('+', sbar, P, u)
    print('  %8.0e  %.6f  %.6f | %.3e  %.3e  %.4f  %.6f | %.4f | %.4f' % (
        eps, zk, 2 * np.sqrt(eps), al[0], al[1], al[0] * al[1], zc / zk, ag[0], ap[0]))
