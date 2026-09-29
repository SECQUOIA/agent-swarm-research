"""Node counts of branching rules on pooling (Haverly) and random box-QP instances.
eps is relative: eps_abs = eps_rel * max(1, |f*|).  Illustrations only (see face_bb.py docstring).
Usage: python3 rules_table2.py name ...  with names from INSTS below."""
import json, sys, time
from face_bb import run, RULES
import instances as I

INSTS = {
    "haverly1": lambda: I.haverly(1), "haverly2": lambda: I.haverly(2), "haverly3": lambda: I.haverly(3),
    "haverly3q": lambda: I.haverly(3, qhi=3.3), "haverly1_2pool": lambda: I.haverly_2pool(1),
    "boxqp5s0b": lambda: I.boxqp(5, 0), "boxqp5s1b": lambda: I.boxqp(5, 1),
    "boxqp4s0c": lambda: I.boxqp(4, 0, diag=(0.5, 2.0)), "boxqp4s1c": lambda: I.boxqp(4, 1, diag=(0.5, 2.0)),
    "boxqp4s2c": lambda: I.boxqp(4, 2, diag=(0.5, 2.0)),
}
EPSREL = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
RL = ["bisect", "SCIP(1,.2)w", "SCIP(1,.2)c", "ANTIG(.75,.1)w", "BARON(.7,.01)w", "COUEN(.25,.2)w",
      "SCIP(1,.2)s", "COUEN(.25,.2)s", "SCIP(1,.2)sp", "COUEN(.25,.2)sp"]
for nm in sys.argv[1:]:
    P = INSTS[nm]()
    for rn in RL:
        for er in EPSREL:
            eps = er * max(1.0, abs(P.fstar))
            t = time.time()
            nodes = run(P, eps, RULES[rn], max_nodes=20000 if rn.endswith(("s", "sp")) else 60000)
            print(json.dumps({"inst": nm, "rule": rn, "eps": er, "nodes": nodes, "lb_leaves": float("nan"),
                              "fstar": P.fstar, "sec": round(time.time() - t, 1)}), flush=True)
            if nodes is None:
                break
