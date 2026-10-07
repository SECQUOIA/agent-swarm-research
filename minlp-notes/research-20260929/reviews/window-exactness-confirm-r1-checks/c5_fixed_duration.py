"""Confirmation check (item 1, Section 7.3): exact change of J_W for the window [0, b) (x_0 fixed, exit S_b
with P = -k) when only the interior control u_n moves to its farther bound, against
(h^2 om^2 / 2) [h (b - 1 - n) - k] + h sigma_n om (sigma_n is ~1e-16, not exactly 0, for float controls).
Own code, rational arithmetic on the float KKT controls (converted exactly)."""
import json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from c1_rmax import toy_kkt
out = []
for N in (1000, 4000, 8000):
    kk = toy_kkt(N, k=0.5); n = kk["inter"][0]
    h = Fr(2, N); k = Fr(1, 2); P = -k
    a = [Fr(2) if t * 2 < N else Fr(-1) for t in range(N + 1)]
    u = [Fr(float(v)) for v in kk["u"]]
    x = [Fr(0)]
    for t in range(N): x.append(x[-1] + h * u[t])
    p = [None] * (N + 1); p[N] = Fr(1)
    for t in range(N - 1, -1, -1): p[t] = p[t + 1] + h * (x[t] - a[t] + k * u[t])
    sig_n = k * x[n] + p[n + 1]
    om = (1 if u[n] < 0 else -1) - u[n]
    L = int(k / h)
    for post in (L - 1, L, L + 1):
        b = n + 1 + post
        u2 = list(u); u2[n] += om
        x2 = [Fr(0)]
        for t in range(b): x2.append(x2[-1] + h * u2[t])
        run = lambda xx, uu: sum(h * ((xx[t] - a[t]) ** 2 / 2 + k * xx[t] * uu[t]) for t in range(n, b))
        Sb = lambda xb: p[b] * xb + P * (xb - x[b]) ** 2 / 2
        change = run(x2, u2) + Sb(x2[b]) - run(x, u) - Sb(x[b])
        formula = h * h * om * om / 2 * (h * (b - 1 - n) - k) + h * sig_n * om
        rec = dict(N=N, n=n, post_stages=post, k_over_h=L, change_over_h2=float(change / h ** 2),
                   formula_minus_change=float(formula - change), h_sig_n_om=float(h * sig_n * om))
        print(json.dumps(rec), flush=True); out.append(rec)
json.dump(out, open(os.path.join(HERE, "logs", "c5_fixed_duration.json"), "w"), indent=1)
