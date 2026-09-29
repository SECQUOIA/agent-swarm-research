"""Revision after review (2026-09-29): reruns with corrected rule labels.
- Counterexample A (instances.box_aligned, convex and K = 2 variants): proved N_opt >= 1/(2 sqrt(eps)).
- SCIP 10 default point rule (SCIPdef), unclamped relaxation point LP(1,0), and incumbent branching
  (INC, incumbent = a known optimal point) on the Section 8 instances.
Usage: python3 revision_runs.py group   (group in: A, B)"""
import json, math, sys, time
import numpy as np
from face_bb import run, RULES
import instances as I

A0, B0 = I.A0, I.B0


def lb(name, eps):
    if name.startswith("box_aligned"):
        return 0.5 / math.sqrt(eps)
    if name.startswith("kink"):
        return 2.0
    if name.startswith("tilt"):
        th = float(name[5:-1]); return 0.5 * math.sqrt(th / eps)
    if name == "diag":
        return math.sqrt(0.5 / eps)
    if name == "iso":
        return (math.asinh((math.sqrt(2) - 1) / math.sqrt(eps)) + math.asinh((1 / 3) / math.sqrt(eps))) / math.pi
    if name == "aligned_quad":
        return 0.5 / math.sqrt(eps)
    return float("nan")


groups = {
    "A": [("box_aligned", I.box_aligned(), ["bisect", "LP(1,.2)w", "SCIPdef w", "LP(1,.2)sp", "INC w"]),
          ("box_alignedK2", I.box_aligned(K=2.0), ["bisect", "LP(1,.2)w", "SCIPdef w", "LP(1,.2)sp", "INC w"])],
    "B": [("kink", I.with_incumbent(I.kink(), [A0, 0.5]), ["SCIPdef w", "SCIPdef x", "LP(1,0)w", "INC w"]),
          ("kinkT", I.with_incumbent(I.kink_mirror(), [A0, B0]), ["SCIPdef w", "LP(1,0)w", "INC w"]),
          ("tilt(0.03)", I.with_incumbent(I.tilt_exact(0.03), [0.5, 0.5]), ["SCIPdef w", "INC w"]),
          ("iso", I.with_incumbent(I.iso(), [A0, B0]), ["SCIPdef w", "INC w"]),
          ("diag", I.with_incumbent(I.diag(), [0.5, 0.5]), ["SCIPdef w", "INC w"]),
          ("aligned_quad", I.with_incumbent(I.aligned_quad(), [A0, 0.5, 0.5]), ["SCIPdef w", "INC w"])],
}
for g in sys.argv[1:]:
    for name, P, rules in groups[g]:
        for rn in rules:
            for eps in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
                t = time.time()
                nodes = run(P, eps, RULES[rn], max_nodes=60000)
                print(json.dumps({"inst": name, "rule": rn, "eps": eps, "nodes": nodes, "lb_leaves": round(lb(name, eps), 2),
                                  "sec": round(time.time() - t, 1)}), flush=True)
                if nodes is None:
                    break
