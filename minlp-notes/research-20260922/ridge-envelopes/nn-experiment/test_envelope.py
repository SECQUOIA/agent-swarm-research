"""Check the batched solver against the verified code (code/ridge_envelope.py).

For random boxes, weights and points (interior, ties, boundary, vertex), both
sides and all five activations: the batched cut value must not exceed the
verified envelope upper bound, must be close to the verified value, and the cut
must be valid at random points, random vertices and all vertices (n <= 10).
Results: results/test_envelope.json.
"""
import json
import time

import numpy as np

from acts import ACTS
from envelope import Problem, cut_violation_samples, solve_batch
from ridge_envelope import envelope_box

rng = np.random.default_rng(12345)
rows = []
for name, act in ACTS.items():
    probs, ref = [], []
    for inst in range(40):
        n = [1, 2, 3, 5, 8, 16, 32][inst % 7]
        l = rng.uniform(-2, 0, n)
        u = l + rng.uniform(0.05, 2, n)
        a = rng.normal(size=n) * rng.uniform(0.3, 3)
        if n > 2 and inst % 5 == 0:
            a[0] = 0.0
        if n > 3 and inst % 6 == 0:
            u[1] = l[1] + 1e-9  # nearly fixed coordinate
        b = rng.uniform(-2, 2)
        kind = inst % 4
        if kind == 0:
            x = rng.uniform(l, u)
        elif kind == 1:  # ties at bounds (typical LP vertex point)
            x = np.where(rng.random(n) < 0.5, l, u)
            x[0] = rng.uniform(l[0], u[0])
        elif kind == 2:
            x = l + (u - l) * rng.choice([0.25, 0.5], n)
        else:
            x = np.where(rng.random(n) < 0.5, l, u)
        # the verified solver keeps a segment of length ~1e-9 for a nearly fixed
        # coordinate, where its LP bound is unreliable; the reference therefore
        # fixes that coordinate at its midpoint (allowed slack L1 |a_1| width / 2)
        lr, ur, xr = l.copy(), u.copy(), x.copy()
        slack = 0.0
        if n > 3 and inst % 6 == 0:
            lr[1] = ur[1] = xr[1] = 0.5 * (l[1] + u[1])
            slack = act.L1 * abs(a[1]) * (u[1] - l[1]) / 2
        for sgn in (1, -1):
            probs.append(Problem(sgn, l, u, a, b, x))
            sig = act.f if sgn > 0 else (lambda s, f=act.f: -f(s))
            R = envelope_box(sig, lr, ur, a, b, xr)
            R["slack"] = slack
            ref.append(R)
    t0 = time.time()
    solve_batch(name, probs)
    tb = time.time() - t0
    for P, R in zip(probs, ref):
        rng2 = np.random.default_rng(len(rows))
        rows.append(dict(act=name, n=len(P.a), sgn=P.sgn, value=P.value, ref_low=R["value"], ref_up=R["value_up"],
                         excess_over_ref_up=P.value - R["value_up"] - R["slack"], loss_vs_ref=R["value"] - P.value,
                         sample_violation=cut_violation_samples(name, P, rng=rng2),
                         concavity_defect=float(np.max(np.diff(np.diff(P.yc) / np.diff(P.t)), initial=0.0)) if len(P.t) > 2 else 0.0))
    sub = [r for r in rows if r["act"] == name]
    print("%-8s batch %.2fs for %d problems | max excess over verified UB %.2e | max loss %.2e | max sample viol %.2e | max slope increase %.1e"
          % (name, tb, len(probs), max(r["excess_over_ref_up"] for r in sub), max(r["loss_vs_ref"] for r in sub),
             max(r["sample_violation"] for r in sub), max(r["concavity_defect"] for r in sub)))
json.dump(rows, open("results/test_envelope.json", "w"), indent=0)
