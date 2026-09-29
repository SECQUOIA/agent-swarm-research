"""Node counts of practical branching rules versus eps on face-exact (McCormick) instances.

Usage: python3 rules_table.py [instance ...]   (default: all)
Prints one JSON line per (instance, rule, eps) with processed nodes (None = cap exceeded) and the
proved lower bound on the number of LEAVES of any certificate (see the note, Section 3).
"""
import json
import math
import sys
import time
from face_bb import run, RULES
import instances as I

EPS = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]


def lb_leaves(name, eps):
    if name.startswith("kink"):
        return 2.0                                        # Theorem 4.1: N_opt = 2 exactly
    if name.startswith("tilt"):
        th = float(name[5:-1])
        return 0.5 * math.sqrt(th / eps)                  # Theorem 3.5 (flat stratum), c = 1
    if name == "diag":
        return math.sqrt(0.5) / math.sqrt(eps)            # Theorem 3.5, alpha = 2, v = (1,-1)/sqrt2
    if name.startswith("iso"):
        return (math.asinh((math.sqrt(2) - 1) / math.sqrt(eps)) + math.asinh((1 / 3) / math.sqrt(eps))) / math.pi  # Thm 3.1
    if name == "aligned_quad":
        return 0.5 / math.sqrt(eps)                       # Proposition 3.8 (box region), gamma = c = 1
    return float("nan")


def main():
    insts = {"kink": I.kink(), "kinkT": I.kink_mirror(), "tilt(0.3)": I.tilt(0.3), "tilt(0.03)": I.tilt(0.03),
             "tilt(0.003)": I.tilt(0.003), "diag": I.diag(), "iso": I.iso(), "sharp_pt": I.sharp_pt(),
             "aligned_quad": I.aligned_quad()}
    names = sys.argv[1:] or list(insts)
    for nm in names:
        P = insts[nm]
        for rname, rule in RULES.items():
            if rname == "xonly" and P.n != 2:
                continue
            for eps in EPS:
                t = time.time()
                cap = 60000 if rname.endswith("s") else 150000
                nodes = run(P, eps, rule, max_nodes=cap)
                print(json.dumps({"inst": nm, "rule": rname, "eps": eps, "nodes": nodes,
                                  "lb_leaves": round(lb_leaves(nm, eps), 2), "sec": round(time.time() - t, 1)}),
                      flush=True)
                if nodes is None:
                    break


if __name__ == "__main__":
    main()
