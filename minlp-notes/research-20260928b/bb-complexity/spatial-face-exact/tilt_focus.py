"""Rules on tilt(theta) with the exact closed-form node bound (instances.tilt_exact).
Question: does a rule's count follow N_opt = (1/2) sqrt(theta/eps) + O(1) (Prop. 3.13) or eps^(-1/2)?"""
import json, math, sys, time
from face_bb import run, RULES
import instances as I
args = sys.argv[1:]
fast = "--no-minscore" in args          # skip min-score strong branching (slow; pathology shown to 1e-5)
thetas = [float(t) for t in args if not t.startswith("--")] or [0.3, 0.03, 0.003]
RL = ["bisect", "SCIP(1,.2)w", "SCIP(1,.2)c", "ANTIG(.75,.1)w", "BARON(.7,.01)w", "COUEN(.25,.2)w",
      "SCIP(1,.2)sp", "COUEN(.25,.2)sp"] + ([] if fast else ["SCIP(1,.2)s", "COUEN(.25,.2)s"])
for th in thetas:
    P = I.tilt_exact(th)
    for rn in RL:
        for eps in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
            t = time.time()
            nodes = run(P, eps, RULES[rn], max_nodes=20000 if rn.endswith(("s", "sp")) else 60000)
            print(json.dumps({"inst": f"tilt({th})", "rule": rn, "eps": eps, "nodes": nodes,
                              "lb_leaves": round(0.5 * math.sqrt(th / eps), 2), "sec": round(time.time() - t, 1)}), flush=True)
            if nodes is None:
                break
