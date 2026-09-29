"""Verify point-rule failures from rv_ms_rule.py with an exact one-parameter description.

Point-rule family at sbar (MS lambda = x'(T sbar)/|.|, all T in SO+(2,1)) =
{C_Gamma : xi_bar in int C_Gamma and xi_bar in span of the two tangency null lines}, where
Gamma(1) = g1, Gamma(-1) = g2 have tangency lines (g1, 1) and (-g2, 1).  Given g1 on the circle,
g2 is determined: the second null line of span{(g1,1), xi_bar}.  We scan g1 densely (1e5 angles)
and apply the MPS completion when ||a|| <= |d|.  Instances are regenerated with the same RNG.
"""
import numpy as np, importlib.util, sys
spec = importlib.util.spec_from_file_location('rv', 'rv_ms_rule.py'); rv = importlib.util.module_from_spec(spec)
sys.argv = ['x', '0', '0']; spec.loader.exec_module(rv)
rng = np.random.default_rng(0)
targets = {13, 14, 17, 23}
done = 0
while done < 24:
    Q = rng.standard_normal((2, 2)); Q = (Q + Q.T) / 2
    b = rng.standard_normal(2); c = rng.standard_normal()
    Qh = np.block([[Q, b[:, None] / 2], [b[None, :] / 2, np.array([[c]])]])
    W = rv.sylvester(Qh)
    if W is None:
        continue
    sbar = rng.standard_normal(2) * 1.5
    ubar = np.append(sbar, 1.0)
    if ubar @ Qh @ ubar <= 0.05:
        continue
    P = rng.standard_normal((2, 2)); w = rng.uniform(0.3, 1.5, 2)
    zk = rv.zK_two(Qh, ubar, P, w)
    if not np.isfinite(zk):
        continue
    done += 1
    if done not in targets:
        continue
    Winv = np.linalg.inv(W); ad = -W[2, :]
    xb = Winv @ ubar; x_, y_ = xb[:2], xb[2]
    best = {False: 0.0, True: 0.0}
    for th in np.linspace(0, 2 * np.pi, 100001):
        g1 = np.array([np.cos(th), np.sin(th)])
        den = 2 * (g1 @ x_ - y_)
        if abs(den) < 1e-14:
            continue
        mu = (y_ ** 2 - x_ @ x_) / den
        n = np.append(mu * g1 + x_, mu + y_)
        if abs(n[2]) < 1e-14:
            continue
        g2 = -n[:2] / n[2]
        for comp in (False, True):
            val = rv.bound_of(rv.set_from_gammas(g1, g2, Winv, ad, comp), ubar, P, w)
            best[comp] = max(best[comp], val)
    print('inst %2d: z_K=%.6f  1-D scan point-rule/zK=%.6f  with completion=%.6f  (|a|=%.3f |d|=%.3f)' % (done, zk, best[False] / zk, best[True] / zk, np.linalg.norm(ad[:2]), abs(ad[2])))
