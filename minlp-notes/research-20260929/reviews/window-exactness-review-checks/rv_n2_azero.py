"""Reviewer check of window-exactness.md Section 7.5, degenerate example A0' (kappa_tau = 0), eps = 0.1:
full minimum of the window {n-K..n+K} over the reachable entry box x U^W by enumerating all faces
(float), with the reviewer's window objective (rv_n2.window).  The report used a sufficient Schur test.
usage: python3 rv_n2_azero.py"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rv_n2 import data, window, EXAMPLES, transferred, dz  # noqa: E402
from fractions import Fraction as Fr

out = []
p = EXAMPLES["Azero"]
for N in (1000, 4000):
    kk = dz.solve_kkt(p, N)
    D = data(p, kk)
    h = float(D["h"])
    Pf, _ = transferred(p, kk, 0.1, 0.1)
    Ps = [[[Fr(float(Pf[t][i][j])) for j in range(2)] for i in range(2)] for t in range(N + 1)]
    box = dz.reach_box(p, N, h)
    loss = {t: -window(D, Ps, t, t + 1, box) for t in range(kk["m"] - 5, kk["m"] + 6)}
    n = max(loss, key=loss.get)
    rec = dict(N=N, s=kk["m"], n=n, loss_n_over_h3=loss[n] / h ** 3, windows=[])
    for K in (1, 2, 3, 4):
        t0 = time.time()
        val = window(D, Ps, n - K, n + K + 1, box)
        rec["windows"].append(dict(K=K, deficit_over_h3=-val / h ** 3, time=time.time() - t0))
        print(json.dumps(rec), flush=True)
    out.append(rec)
json.dump(out, open(os.path.join(HERE, "logs", "n2_azero.json"), "w"), indent=1)
