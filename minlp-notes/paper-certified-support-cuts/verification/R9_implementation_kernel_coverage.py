"""R9 implementation lens: which blocks can the frozen support kernels certify?

Calls the campaign-4 snapshot's certify_support (as the separator does) on
small blocks to test the statement of Section 7.2 that only polynomial
remainders of degree >= 3 in three or four variables are uncertifiable.
Cases:
  A  block {x,y}: features x, y, exp(x), x*y; direction puts weight only on x*y
  B  block {x,y,z}: features x, y, z, x^2*y*z (degree 4), x*z; weight only on x*z
  C  as B, weight on the degree-4 feature
  D  block {x}: feature x^4 - x^2 with a target above the exact minimum
     (the separator passes target = LP activity + threshold for
     non-quadratic blocks)
No solver is run.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # never write into the frozen snapshot

import sympy as sp

SNAP = Path(__file__).resolve().parents[1] / "experiments/v4/snapshot"
sys.path.insert(0, str(SNAP / "research-20261003-convexification"))
sys.path.insert(0, str(SNAP / "code/univariate_envelopes"))
from solver.support import certify_support  # noqa: E402

x, y, z = sp.symbols("x0 x1 x2", real=True)
box2, box3 = ((0.5, 2.0), (0.0, 1.0)), ((0.0, 1.0),) * 3
cases = {
    "A {x,y} with exp(x) side, weight on x*y only":
        ((x, y, sp.exp(x), x*y), (x, y), box2, (0.0, 0.0, 0.0, 1.0), None),
    "B {x,y,z} with degree-4 side, weight on x*z only":
        ((x, y, z, x**2*y*z, x*z), (x, y, z), box3, (0.0, 0.0, 0.0, 0.0, 1.0), None),
    "C {x,y,z} weight on degree-4 side":
        ((x, y, z, x**2*y*z, x*z), (x, y, z), box3, (0.0, 0.0, 0.0, 1.0, 0.0), None),
    "D {x} x^4-x^2, target 0 (exact min -1/4)":
        ((x, x**4 - x**2), (x,), ((0.0, 1.0),), (0.0, 1.0), 0.0),
    "D' {x} x^4-x^2, no target":
        ((x, x**4 - x**2), (x,), ((0.0, 1.0),), (0.0, 1.0), None),
}
for name, (features, symbols, box, coefficients, target) in cases.items():
    result = certify_support(features, symbols, box, coefficients, rows=(), target=target,
                             max_cells=128, max_depth=16, max_polytope_faces=2000)
    rhs = None if result.cut is None else result.cut.rhs
    print(f"{name:50s} status={result.status:11s} method={result.stats.get('method')} "
          f"reason={result.stats.get('reason')} rhs={rhs}")
