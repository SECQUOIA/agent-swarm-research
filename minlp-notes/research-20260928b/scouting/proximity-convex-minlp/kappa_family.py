"""How fast can the unconstrained l_inf proximity rho_inf(Q) grow with the
condition number in dimension 2?  Upper bound: rho <= 1/2 sqrt(tr Q/lambda_min)
~ sqrt(kappa/2) with kappa ~ R.  Family Q = R w w^T + I with w = (1, -1/(2K)),
best K for each R, and a badly approximable slope w = (1, -sqrt 2)."""
import signal
import numpy as np
from voronoi import rho_inf


class TO(Exception):
    pass


def _alarm(s, f):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)
for e in range(2, 10):
    R = 10.0 ** e
    best, skipped = (0, None), 0
    for K in sorted(set(int(round(x)) for x in np.geomspace(1, 4 * R ** 0.5, 40))):
        w = np.array([1.0, -1.0 / (2 * K)])
        signal.alarm(5)
        try:
            r, _, _ = rho_inf(R * np.outer(w, w) + np.eye(2))
        except TO:
            skipped += 1
            continue
        finally:
            signal.alarm(0)
        if r > best[0]:
            best = (r, K)
    w = np.array([1.0, -2 ** 0.5])
    rs, _, _ = rho_inf(R * np.outer(w, w) + np.eye(2))
    print(f"R=1e{e}: max_K rho={best[0]:.1f} (K={best[1]}, skipped {skipped})  R^(1/3)={R**(1/3):.1f}  "
          f"rho(sqrt2 slope)={rs:.1f}  R^(1/4)={R**0.25:.1f}  sqrt(R)={R**0.5:.0f}", flush=True)
