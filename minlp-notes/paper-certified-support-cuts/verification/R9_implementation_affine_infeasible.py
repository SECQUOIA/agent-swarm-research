"""R9 implementation lens: the eight Part D pool models that the model builder
refused as 'affine_infeasible'. For each, run the snapshot's exact bound
propagation and print the deduction chain that ends in the contradiction:
the rows involved, whether integer rounding was used, and the size of the
exact excess. Then re-derive the contradiction independently in exact
rational arithmetic from the original rows only (no snapshot code beyond the
OSiL reader). Read-only; no solver is run.
"""
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.dont_write_bytecode = True  # never write into the frozen snapshot
HERE = Path(__file__).resolve().parents[1]
SNAP = HERE / "experiments/v4/snapshot"
sys.path.insert(0, str(SNAP / "research-20261003-convexification"))
sys.path.insert(0, str(SNAP / "code/univariate_envelopes"))
from uenv.osil import read_osil                      # noqa: E402
from solver.bounds import propagate_bounds          # noqa: E402

records = [json.loads(l) for l in (HERE / "experiments/v4/scanD/records.jsonl").read_text().splitlines() if l]
bad = [r for r in records if r.get("status") == "affine_infeasible"]
for r in bad:
    inst = read_osil(r["path"])
    p = propagate_bounds(inst)
    steps = p.certificate["steps"]
    kinds = {}
    for s in steps:
        kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
    last = steps[-1]
    # Independent recheck of the last step against a box rebuilt from the chain.
    lo = [Q(float(x)) if math.isfinite(x) else None for x in inst.var_lb]
    hi = [Q(float(x)) if math.isfinite(x) else None for x in inst.var_ub]
    for s in steps[:-1]:
        if s["kind"] in ("affine", "integer", "binary"):
            (lo if s["bound"] == "lower" else hi)[s["variable"]] = Q(s["new"])
    detail = ""
    if last["kind"] == "contradiction":
        row = inst.rows[last["row"] + 1]
        coefficients = {int(j): Q(float(a)) for j, a in row["lin"].items() if a}
        sign = 1 if last["side"] == "upper" else -1
        rhs = Q(float(row["ub"])) if sign == 1 else -Q(float(row["lb"]))
        minimum = sum((sign * a) * (lo[j] if sign * a > 0 else hi[j]) for j, a in coefficients.items())
        detail = (f"row {last['row']} {last['side']}: exact minimum activity {float(minimum):.6g} > rhs {float(rhs):.6g},"
                  f" excess {float(minimum - rhs):.3g}; recheck {'OK' if minimum > rhs else 'FAILED'}")
    else:
        j = last["variable"]
        detail = (f"crossed bounds on variable {j}: lower {float(lo[j] if last['bound']=='upper' else Q(last['new'])):.6g}"
                  f" upper {float(Q(last['new']) if last['bound']=='upper' else hi[j]):.6g} via {last['kind']}")
    print(f"{r['name']:18s} steps {len(steps):5d} {kinds}  {detail}")
