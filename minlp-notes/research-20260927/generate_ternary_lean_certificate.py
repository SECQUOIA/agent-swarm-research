"""Print the rational weighted-square block checked in TernarySOSDescent.lean.

The generated identity is proved by Lean, independently of this generator.
Run from any directory; the existing targeted exact checker supplies M-I=LDL^T.
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import runpy

import sympy as s


with redirect_stdout(StringIO()):
    data = runpy.run_path(str(Path(__file__).with_name(
        "check_ternary_rational_sos_convex_counterexample.py")))
L, D = data["L"], data["D"]

lines = ["noncomputable def hessianGapSOS (x y z a b c : ℝ) : ℝ :=",
         "  let Z0 := a", "  let Z1 := b", "  let Z2 := c"]
for i, shift in enumerate(["x - 3 / 4", "y - 1", "z - 1 / 2"]):
    for j, direction in enumerate(["a", "b", "c"]):
        lines.append(f"  let Z{3+3*i+j} := ({shift}) * {direction}")

terms = []
for i in range(12):
    denominator = s.ilcm(*[L[j, i].q for j in range(12)])
    row = [int(denominator * L[j, i]) for j in range(12)]
    weight = D[i, i] / denominator**2
    assert weight > 0
    expression = ""
    for j, value in enumerate(row):
        if not value:
            continue
        term = f"Z{j}" if abs(value) == 1 else f"{abs(value)} * Z{j}"
        if expression:
            expression += (" + " if value > 0 else " - ") + term
        else:
            expression = ("" if value > 0 else "-") + term
    lines.append(f"  let W{i} := {expression}")
    coefficient = str(weight.p) if weight.q == 1 else f"({weight.p} / {weight.q})"
    terms.append(f"{coefficient} * W{i} ^ 2")
terms.extend(f"Z{i} ^ 2" for i in range(3, 12))
lines.extend("  " + term + (" +" if i < len(terms)-1 else "")
             for i, term in enumerate(terms))
print("\n".join(lines))
