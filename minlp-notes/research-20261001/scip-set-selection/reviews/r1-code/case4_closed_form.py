"""Review r1: compare the closed form of phi_lambda(yhat) = max{beta^T yhat : ||beta|| <= 1, beta_last <= lambda_last}
used by the patch (pieces a/b, condition -ll*||yhat|| + yhat_last <= 0) with a numerical maximization (SLSQP),
and check Case-4 S-freeness of C_lambda for random unit lambda on random points of S (q <= 0)."""
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(7)
worst = 0.0
failed = 0
for _ in range(2000):
    m = rng.integers(1, 4) + 1
    yh = rng.normal(size=m) * rng.choice([0.1, 1, 10])
    ll = rng.uniform(-0.999, 0.999)
    ny = np.linalg.norm(yh)
    closed = ny if -ll * ny + yh[-1] <= 0 else np.sqrt(max(0, (1 - ll**2) * (ny**2 - yh[-1]**2))) + ll * yh[-1]
    best = -np.inf
    for start in range(4):
        b0 = rng.normal(size=m); b0 /= 2 * np.linalg.norm(b0)
        res = minimize(lambda b: -b @ yh, b0, method='SLSQP', jac=lambda b: -yh,
                       constraints=[{'type': 'ineq', 'fun': lambda b: 1 - b @ b, 'jac': lambda b: -2 * b},
                                    {'type': 'ineq', 'fun': lambda b: ll - b[-1], 'jac': lambda b: -np.eye(m)[-1]}],
                       options={'ftol': 1e-14, 'maxiter': 500})
        if res.success and 1 - res.x @ res.x > -1e-9 and ll - res.x[-1] > -1e-9:
            best = max(best, -res.fun)
    if not np.isfinite(best):
        failed += 1
        continue
    worst = max(worst, abs(best - closed) / (1 + abs(closed)))
print('closed form vs SLSQP, max relative difference over %d random cases (SLSQP failed on %d): %.2e' % (2000 - failed, failed, worst))
# S-freeness in Case 4: q = ||x||^2 - ||y||^2 + w + kappa, xhat = (x, (w+kappa+r)/(2 sqrt r)), yhat = (y, (w+kappa-r)/(2 sqrt r))
viol = 0; tested = 0
for _ in range(20000):
    p, n = rng.integers(1, 3), rng.integers(1, 3)
    kappa = rng.normal() * rng.choice([0, 0.3, 3])
    r = np.sqrt(1 + kappa**2); sr = np.sqrt(r)
    lam = rng.normal(size=p + 1); lam /= np.linalg.norm(lam)
    x = rng.normal(size=p) * 2; y = rng.normal(size=n) * 2
    w = -(x @ x - y @ y + kappa) - abs(rng.normal())  # forces q < 0
    q = x @ x - y @ y + w + kappa
    xh = np.append(x, (w + kappa + r) / (2 * sr)); yh = np.append(y, (w + kappa - r) / (2 * sr))
    ll = lam[-1]; ny = np.linalg.norm(yh)
    phi = ny if -ll * ny + yh[-1] <= 0 else np.sqrt(max(0, (1 - ll**2) * (ny**2 - yh[-1]**2))) + ll * yh[-1]
    tested += 1
    if phi - lam @ xh < -1e-9 * (1 + abs(phi)):
        viol += 1
print('Case 4, random unit lambda: %d points of S tested, %d inside int C_lambda' % (tested, viol))
