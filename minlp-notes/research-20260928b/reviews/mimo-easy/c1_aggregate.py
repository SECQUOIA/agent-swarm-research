"""Aggregate c1_checks.jsonl (reviewer).  Usage: python3 c1_aggregate.py > c1_aggregate.out"""
import json
import numpy as np

R = [json.loads(l) for l in open("c1_checks.jsonl")]
print("instances:", len(R), " all nodes box-inactive in all:", all(r["all_inactive"] for r in R))
for b in (1.0, 1.5, 2.0, 3.0):
    for N in (200, 400, 800):
        S = [r for r in R if r["beta"] == b and r["N"] == N]
        if S:
            print(f"beta={b} N={N}: max NNLS coef over all nodes/instances = {max(r['umax'] for r in S):.3f}")
print("C1 frequency by theta/theta_c (all beta, N):")
for m in (0.5, 0.8, 1.0, 1.2, 1.5, 2.0):
    S = [r for r in R if r["mult"] == m]
    print(f"  {m}: {sum(r['c1'] for r in S)}/{len(S)}; mean node-0 gap {np.mean([r['gap0'] for r in S]):+.3f} "
          f"(first-order {S[0]['first']:+.3f}); mean(min gap - second-order) {np.mean([r['min_gap'] - r['second'] for r in S]):+.3f}")
for b in (1.0, 1.5, 2.0, 3.0):
    S = [r for r in R if r["beta"] == b]
    d = np.array([r["min_gap"] - r["second"] for r in S])
    print(f"beta={b}: min gap minus second-order prediction: mean {d.mean():+.3f}, range [{d.min():+.3f},{d.max():+.3f}]")
d = np.array([r["mean_ratio"] - r["law"] for r in R])
print("mean r/|v|^2 - law: range", round(d.min(), 3), round(d.max(), 3))
