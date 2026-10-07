"""Referee check (R2): toy plus (x' = u, a = 2 on [0,1), -1 on [1,2], k = 1/2, Phi = x, T = 2), own float code.
KKT point with one fractional stage; q, rho*, w0 and the per-side predicted counts
1 + sum_sides ceil(log(a_side / w0) / log rho*) (a side with a_side <= w0 needs no outer node)."""
import json
import math
import numpy as np

k = 0.5
for N in (1000, 4000, 8000):
    h = 2.0 / N
    a = np.where(np.arange(N) * h < 1.0, 2.0, -1.0)

    def sig_of(u):
        x = np.concatenate([[0.0], np.cumsum(h * u)])
        p = np.empty(N + 1); p[N] = 1.0
        p[:N] = p[N] + np.cumsum((h * (x[:N] - a + k * u))[::-1])[::-1]
        return k * x[:N] + p[1:]
    best = None
    for s in range(int(0.15 * N), int(0.35 * N)):
        u = np.ones(N); u[s:] = -1.0; u[s] = 0.0
        s0 = sig_of(u)[s]
        Hss = h * h * (h * (N - 1 - s) + 0.0)
        v = -h * s0 / Hss
        if -1 < v < 1:
            u[s] = v
            sg = sig_of(u)
            viol = max(np.max(np.maximum(sg[:s], 0)), np.max(np.maximum(-sg[s + 1:], 0))) / h
            if viol < 1e-9:
                best = (s, v, h * (N - 1 - s))
    s, v, q = best
    rho = 1 + (q + math.sqrt(q * q + q * k)) / k
    rows = []
    for e in (1e-1, 1e-2, 1e-3, 1e-4):
        w0 = math.sqrt(2 * e / k)
        side = [math.ceil(math.log(d / w0) / math.log(rho)) if d > w0 else 0 for d in (1 - v, 1 + v)]
        rows.append(dict(eps_over_h2=e, w0=round(w0, 4), plus_minus=side, predicted=1 + sum(side),
                         central=[round(max(-1, v - w0), 4), round(min(1, v + w0), 4)]))
    print(json.dumps(dict(N=N, n=s, u_n=round(v, 4), q=round(q, 5), rho_star=round(rho, 4), rows=rows)))
