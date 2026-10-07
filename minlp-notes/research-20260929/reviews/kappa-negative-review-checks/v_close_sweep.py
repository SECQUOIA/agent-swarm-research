"""N-sweep of the maximal-recursion break for kappa 0.5 -> 0 at (0.6, 1.4) (eta^X = -0.275), float."""
import json, sys
import numpy as np
from v_close import data, kkt_point, rmax
k1, k2, t1, t2, tk, guess = -0.5, 0.0, 0.6, 1.4, 0.59375, (0.5, 0.725)
out = []
for N in [int(v) for v in sys.argv[1:]]:
    a, k = data(k1, k2, t1, t2, tk, N)
    u, sig, frac, viol, J = kkt_point(N, a, k, guess)
    sw = [t for t in range(1, N) if u[t] != u[t - 1]]
    br = rmax(N, k, sig, frac)
    h = 2.0 / N
    out.append((N, round(viol, 17), [round(t * h, 4) for t in frac], sw[0], None if br is None else br - sw[0]))
    print(json.dumps(out[-1]), flush=True)
