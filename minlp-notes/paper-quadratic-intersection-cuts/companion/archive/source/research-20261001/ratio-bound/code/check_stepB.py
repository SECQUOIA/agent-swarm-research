"""Check the closed-form family-(B) step length (rb.stepB_closed) against the bisection with an
exact concave tau-search (rb.stepB_X) on random X and rays."""
import time
import numpy as np
import rb

rng = np.random.default_rng(3)
mx, n, ninf = 0.0, 0, 0
t0 = time.time()
for k in range(4000):
    X = rb.X_from(rng.normal(size=3) * 2)
    p = rng.normal(size=3) * np.exp(rng.normal(size=3))
    a, b = rb.stepB_closed(X, p), rb.stepB_X(X, p)
    if np.isinf(a) and np.isinf(b):
        ninf += 1
        continue
    if np.isinf(a) != np.isinf(b):
        print('INF MISMATCH', X.tolist(), p.tolist(), a, b)
        mx = np.inf
        continue
    n += 1
    mx = max(mx, abs(a - b) / max(1.0, b))
print('finite pairs', n, 'both infinite', ninf, 'max rel diff %.2e' % mx, 'time %.1fs' % (time.time() - t0))
print('PASS' if mx < 1e-6 else 'FAIL')
