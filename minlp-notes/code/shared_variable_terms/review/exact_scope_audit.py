"""Check the saved water point with exact OSiL decimal coefficients and two
mathematical scope counterexamples. No solver runs.

From the repository root:
code/minlp_solver_lab/.venv/bin/python code/shared_variable_terms/review/exact_scope_audit.py

The decimal check reuses the OSiL reader but replaces its numerical conversion
with Fraction before reading. Saved point floats retain their exact binary
values. This independently checks coefficient conversion, not XML parsing.
"""
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "code/univariate_envelopes"))
from uenv import osil


def decimal_number(value):
    if value.lower() in {"inf", "+inf", "-inf"}:
        return float(value)
    return F(value)


def evaluate(tree, point):
    op = tree[0]
    if op == "num":
        return F(tree[1])
    if op == "var":
        return point[tree[1]]
    children = [evaluate(child, point) for child in tree[1:]]
    if op == "sum":
        return sum(children, F(0))
    if op == "negate":
        return -children[0]
    if op == "times":
        return math.prod(children)
    if op == "divide":
        return children[0] / children[1]
    if op == "square":
        return children[0] ** 2
    if op == "power":
        exponent = children[1]
        assert exponent.denominator == 1, "Only integer powers are exact here"
        return children[0] ** int(exponent)
    raise NotImplementedError(op)


osil.float = decimal_number
instance = osil.read_osil(str(Path.home() / ".cache/minlplib/minlplib/osil/waterno2_18.osil"))
point = [F(value) for value in json.loads(
    (ROOT / "code/shared_variable_terms/point_waterno2_18.json").read_text()
)["point"]]
assert len(point) == len(instance.var_lb)
violations = [(F(0), "none")]
for i, (lower, upper, kind) in enumerate(zip(instance.var_lb, instance.var_ub, instance.var_type)):
    if math.isfinite(lower):
        violations.append((F(lower) - point[i], f"lb{i}"))
    if math.isfinite(upper):
        violations.append((point[i] - F(upper), f"ub{i}"))
    if kind in {"B", "I"}:
        violations.append((abs(point[i] - round(point[i])), f"int{i}"))
for index, row in enumerate(instance.rows):
    value = sum((F(c) * point[i] for i, c in row["lin"].items()), F(0))
    value += sum((F(c) * point[i] * point[j] for i, j, c in row["quad"]), F(0))
    if row["nl"] is not None:
        value += evaluate(row["nl"], point)
    if index == 0:
        objective = value + F(instance.obj_const)
        continue
    if math.isfinite(row["lb"]):
        violations.append((F(row["lb"]) - value, f"row{index}lb"))
    if math.isfinite(row["ub"]):
        violations.append((value - F(row["ub"]), f"row{index}ub"))
worst, where = max(violations)
assert objective == F(728761127366816713, 2**47)
assert worst == F(32325, 2**49)
assert worst < F("5.8e-11")
print(json.dumps({"coefficient_semantics": "exact OSiL decimal rationals",
                  "point_semantics": "exact saved binary floats",
                  "objective_exact": str(objective), "objective_float": float(objective),
                  "max_violation_exact": str(worst), "max_violation_float": float(worst),
                  "where": where}))

# Individual epigraph hulls: t1 >= x^2 and t2 >= x. Joint hull at
# t1=x^2 forces zero variance of X, hence t2 >= sqrt(x); this point fails.
x, t1, t2 = F(1, 2), F(1, 4), F(1, 2)
assert t1 >= x*x and t2 >= x
assert t2 >= 0 and t2*t2 < x

# Determinant inequalities alone do not specify the moment hull. This point
# satisfies both on [0,1], but violates t3-l*t2 >= 0 and cannot be a moment.
lower, upper, x, t2, t3 = map(F, (0, 1, 0, 0, -1))
assert (x-lower)*(t3-lower*t2) >= (t2-lower*x)**2
assert (upper-x)*(upper*t2-t3) >= (upper*x-t2)**2
assert t3-lower*t2 < 0
print("Exact scope checks passed: mixed-curvature epigraphs and cone-factor nonnegativity.")
