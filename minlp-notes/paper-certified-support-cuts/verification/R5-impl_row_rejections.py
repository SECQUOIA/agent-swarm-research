"""R5-impl: classify stored-row audit rejections on one Part B model.

Runs the snapshot separator once (root, node limit 1) with a wrapped audit
that records why SCIP's stored row differs from the exported row.
"""
import collections, json, math, sys
from fractions import Fraction as Q
from pathlib import Path

part = Path(sys.argv[1]); name = sys.argv[2]; mode = sys.argv[3] if len(sys.argv) > 3 else "all"
snap = part / "snapshot" / "research-20261003-convexification"
sys.path.insert(0, str(snap)); sys.path.insert(0, str(snap / "experiments"))
from worker import load_model
import solver.integration as integ

reasons = collections.Counter()
original = integ._audit_inserted_row

def audit(model, row, variables, coefficients, rhs):
    result = original(model, row, variables, coefficients, rhs)
    if result is None:
        actual = {c.getVar().name: v for c, v in zip(row.getCols(), row.getVals()) if v}
        expected = {}
        for var, coef in zip(variables, coefficients):
            if coef:
                t = model.getTransformedVar(var)
                expected[t.name] = expected.get(t.name, 0.0) + coef
                status = t.getStatus() if hasattr(t, "getStatus") else "?"
                if status not in ("COLUMN", "LOOSE"):
                    reasons["variable status " + str(status)] += 1
        if set(actual) != set(expected):
            reasons["column set differs"] += 1
        else:
            for k in actual:
                if actual[k] != expected[k]:
                    reasons["coefficient changed (%s): %r -> %r" % ("rounded to integer" if actual[k] == round(expected[k]) else "other", expected[k], actual[k])] += 1
        if float(row.getConstant()) != 0.0:
            reasons["nonzero row constant"] += 1
    return result

integ._audit_inserted_row = audit
case = json.loads((part / "cases" / (name + ".json")).read_text())
if "path" in case:
    case = {**case, "path": str(part / "snapshot" / "original-osil" / (name + ".osil"))}
inst = load_model(case)
cfg = integ.Config()
result = integ.run_instance(inst, mode, time_limit=60.0, node_limit=1, config=cfg)
print(name, mode, "cuts", len(result["cuts"]), "rejections", result["separation"]["row_binding_rejections"], dict(reasons))
