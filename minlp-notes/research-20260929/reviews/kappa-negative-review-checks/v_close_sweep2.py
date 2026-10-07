"""N-sweep of the maximal-recursion break for several close-switch configurations (float)."""
import json, sys
from v_close import CONFIGS, data, kkt_point, rmax
idx = int(sys.argv[1])
k1, k2, t1, t2, tk, guess = CONFIGS[idx]
res = []
for N in [int(v) for v in sys.argv[2:]]:
    a, k = data(k1, k2, t1, t2, tk, N)
    u, sig, frac, viol, J = kkt_point(N, a, k, guess)
    sw = [t for t in range(1, N) if u[t] != u[t - 1]]
    br = rmax(N, k, sig, frac)
    res.append((N, bool(viol < 1e-12), None if br is None else br - sw[0]))
print(json.dumps(dict(kappa1=-k1, kappa2=-k2, t1=t1, t2=t2, sweep=res)), flush=True)
