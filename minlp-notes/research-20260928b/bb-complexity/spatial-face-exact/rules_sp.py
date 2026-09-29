"""Product-score strong branching (SCIP(1,.2)sp, COUEN(.25,.2)sp) on the Section 8 instances."""
import json, sys, time
from face_bb import run, RULES
import instances as I
from rules_table import lb_leaves
insts = {"kink": I.kink(), "kinkT": I.kink_mirror(), "sharp_pt": I.sharp_pt(), "iso": I.iso(), "diag": I.diag()}
for nm in sys.argv[1:] or list(insts):
    for rn in ("SCIP(1,.2)sp", "COUEN(.25,.2)sp"):
        for eps in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
            t = time.time()
            nodes = run(insts[nm], eps, RULES[rn], max_nodes=60000)
            print(json.dumps({"inst": nm, "rule": rn, "eps": eps, "nodes": nodes,
                              "lb_leaves": round(lb_leaves(nm, eps), 2), "sec": round(time.time() - t, 1)}), flush=True)
            if nodes is None:
                break
