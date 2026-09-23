"""Cross-check that the original and lifted SYNHEAT formulations describe the same problem:
the solution point of each formulation is feasible in the other with the same objective."""
import json, sys
from common import *
from synheat import EXAMPLES, build, max_violation

solver = sys.argv[1] if len(sys.argv) > 1 else "gurobi"
for ex in EXAMPLES:
    for src, dst in (("orig", "lift"), ("lift", "orig")):
        f = RES / f"synheat_{ex}_{src}_{solver}.json"
        if not f.exists():
            continue
        pt = json.load(open(f))["point"]
        m = build(EXAMPLES[ex], lifted=(dst == "lift"))
        viol, obj = max_violation(m, pt)
        print(f"{ex}: point from {src} evaluated in {dst}: max violation {viol:.2e}, obj {obj:.3f} (source obj {json.load(open(f))['obj']:.3f})")
