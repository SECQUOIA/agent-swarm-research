"""Small cross-workflow integration checks; no broad component random suite."""
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "solver"))
from certified_grid import BoxQP
from convex_recourse import solve_convex_recourse, verify_convex_recourse
from polynomial_grid import PolynomialBox, PolynomialFactor, solve as solve_polynomial
from polynomial_boundary import certify_boundary, discover_boundary
from verify_polynomial import verify_polynomial
from verify_polynomial_boundary import verify_certificate as verify_boundary
from recourse import solve_with_recourse
from verify_recourse import verify_pipeline
from submodular_recourse import solve_submodular
from verify_submodular_recourse import verify_submodular

rejected_mutations = 0


def wire(value):
    return json.loads(json.dumps(value))


def rejects(call):
    global rejected_mutations
    try:
        result = call()
    except ValueError:
        rejected_mutations += 1
        return
    assert result is False, result
    rejected_mutations += 1


records = []


def qp_model():
    # Effective integer z labels {-1,0,1,2}; fixed t=1/3. There are tied
    # optima (z,y)=(-1,0),(2,1), both value -22/9. The private response
    # y=clip((z+1)/2,0,1) changes its active face.
    return BoxQP([[-2, -1, 2], [-1, 2, -3], [2, -3, 4]], [1, 0, 0],
                 [(F(-4, 3), F(7, 3)), (0, 1), (F(1, 3), F(1, 3))],
                 [0], [(2, 0, 1)], [])


qp = qp_model()
other = BoxQP(qp.A, [1, 0, 1], qp.bounds, qp.integers, qp.bags, qp.edges)
expected = F(-22, 9)
poly = PolynomialBox(qp.bounds, [
    PolynomialFactor((2, 0, 1), [(-1, (0, 2, 0)), (-1, (0, 1, 1)),
        (2, (1, 1, 0)), (1, (0, 0, 2)), (-3, (1, 0, 1)),
        (2, (2, 0, 0)), (1, (0, 1, 0))])], [0], [(2, 0, 1)], [])
for z in range(-1, 3):
    for y in (F(0), F(1, 3), F(1)):
        x = (F(z), y, F(1, 3))
        assert qp.value(x) == poly.value(x)

for route in ("convex", "submodular"):
    for cap in (None, "time", "oracle"):
        options = ({"time_limit": 0} if cap == "time" else
                   {"max_faces": 0} if cap == "oracle" else {})
        if route == "convex":
            cert = wire(solve_convex_recourse(qp, [[1]], exact=True, **options))
            verifier = verify_convex_recourse
        else:
            cert = wire(solve_submodular(qp, exact=True, **options))
            verifier = verify_submodular
        with patch("rational_optimization.solve_lp", side_effect=AssertionError("LP called")), \
             patch("convex_recourse.solve_convex_box_qp", side_effect=AssertionError("QP called")), \
             patch("submodular_recourse.solve_convex_box_qp", side_effect=AssertionError("QP called")):
            assert verifier(cert, qp)
        assert F(cert["lower"]) <= expected <= F(cert["upper"])
        if cap is None:
            assert cert["status"] == "exact" and F(cert["upper"]) == expected
        rejects(lambda: verifier(cert, other))
        bad = copy.deepcopy(cert)
        bad["problem"]["integers"] = [0, 1]
        rejects(lambda: verifier(bad, qp))
        records.append({"workflow": route, "cap": cap, "status": cert["status"],
                        "lower": cert["lower"], "upper": cert["upper"]})

for route in ("convex", "submodular"):
    for cap in (None, "time"):
        options = {"time_limit": 0} if cap else {}
        result = wire(solve_with_recourse(qp, blocks=[[1, 2]], discover=False,
                      backend=route, exact=True, **options))
        assert verify_pipeline(result, qp)["valid"]
        assert F(result["lower"]) <= expected <= F(result["upper"])
        if cap is None:
            assert result["status"] == "exact"
            assert result["method"] == route
        rejects(lambda: verify_pipeline(result, other))
        if result["inner"]:
            bad = copy.deepcopy(result)
            bad["inner"]["problem"]["constant"] = "123"
            rejects(lambda: verify_pipeline(bad, qp))
        records.append({"workflow": "pipeline_" + route, "cap": cap,
                        "status": result["status"], "method": result["method"],
                        "lower": result["lower"], "upper": result["upper"]})

# Scalar piece certificates survive fixed-integer substitution in the outer
# pipeline. The added (w-2)z term vanishes on the original fixed face.
m = 64
stiff = BoxQP([[2*m+10, -2*m-4, -2*m, 1],
               [-2*m-4, 2*m+2, 2*m, 0], [-2*m, 2*m, 2*m, 0],
               [1, 0, 0, 0]], [-4, 1, 0, 0],
              [(0, F(3, 4)), (0, 1), (0, 1), (2, 2)], [3],
              [(3, 0, 2, 1)], [], F(1, 4))
result = wire(solve_with_recourse(stiff, blocks=[[1, 2, 3]], discover=False,
              backend="convex", epsilon=F(1, 100), max_stages=40))
assert verify_pipeline(result, stiff)["valid"]
assert result["status"] in ("certified", "exact")
assert F(result["lower"]) <= F(1, 20) <= F(result["upper"])
assert F(result["gap"]) <= F(1, 100)
pieces = result["inner"]["curvature_proofs"]
assert len(pieces) == 1 and len(pieces[0]["pieces"]) == 3
bad = copy.deepcopy(result)
bad["inner"]["curvature_proofs"][0]["pieces"][0]["value"][2] = "-99999"
rejects(lambda: verify_pipeline(bad, stiff))
records.append({"workflow": "pipeline_scalar_curvature", "status": result["status"],
                "lower": result["lower"], "upper": result["upper"],
                "private_blocks": len(pieces), "pieces": len(pieces[0]["pieces"])})

for options in ({"epsilon": F(1, 100), "max_stages": 32},
                {"max_stages": 0}, {"time_limit": 0}, {"max_table_states": 1}):
    cert = wire(solve_polynomial(poly, **options))
    with patch("polynomial_grid.solve", side_effect=AssertionError("solver called")), \
         patch("finite_dp.solve_tree", side_effect=AssertionError("DP called")):
        assert verify_polynomial(cert, expected_problem=poly)["valid"]
    assert cert["problem"] == poly.to_dict()
    assert F(cert["lower"]) <= expected <= F(cert["upper"])
    if "epsilon" in options:
        assert F(cert["gap"]) <= options["epsilon"]
    bad = copy.deepcopy(cert)
    bad["upper"] = str(expected - 1)
    rejects(lambda: verify_polynomial(bad))
    rejects(lambda: verify_polynomial(cert, expected_problem=PolynomialBox(poly.bounds, [])))
    records.append({"workflow": "polynomial", "options": {k: str(v) for k, v in options.items()},
                    "status": cert["status"], "lower": cert["lower"], "upper": cert["upper"]})

# Exact implicit output keeps the irrational free minimizer and substitutes
# an already fixed native integer coordinate, then removes a monotone face.
boundary_model = PolynomialBox([(0, 1), (0, 1), (-2, -2)], [
    PolynomialFactor((1,), [(1, (4,)), (-1, (2,)), (F(1, 4), (0,))]),
    PolynomialFactor((1, 0), [(1, (0, 1)), (1, (2, 1))]),
    PolynomialFactor((2,), [(1, (2,)), (4, (1,)), (4, (0,))])], [2])
boundary = wire(discover_boundary(boundary_model, time_limit=15))
assert boundary["status"] == "certified", boundary
with patch("polynomial_grid.solve", side_effect=AssertionError("solver called")), \
     patch("polynomial_boundary.certify_boundary", side_effect=AssertionError("discovery called")):
    descriptor = verify_boundary(boundary["certificate"], boundary_model)
assert descriptor["kind"] == "strongly_convex_patch"
assert descriptor["free"] == (1,)
assert descriptor["face_bounds"][0] == (0, 0)
assert descriptor["face_bounds"][2] == (-2, -2)
lo, hi = descriptor["face_bounds"][1]
assert lo * lo < F(1, 2) < hi * hi
assert "point" not in descriptor and "value" not in descriptor
wrong = PolynomialBox(boundary_model.bounds, [])
rejects(lambda: verify_boundary(boundary["certificate"], wrong))
bad = copy.deepcopy(boundary["certificate"])
bad["grid_certificate"]["problem"]["factors"] = []
rejects(lambda: verify_boundary(bad, boundary_model))
assert certify_boundary(boundary_model, boundary["certificate"]["grid_certificate"],
                        time_limit=0)["status"] == "inconclusive"
records.append({"workflow": "polynomial_boundary", "status": boundary["status"],
                "kind": descriptor["kind"], "free": list(descriptor["free"]),
                "rounds": len(boundary["attempts"])})

sources = ["polynomial_grid.py", "verify_polynomial.py", "polynomial_boundary.py",
           "verify_polynomial_boundary.py", "convex_recourse.py", "submodular_recourse.py",
           "verify_submodular_recourse.py", "recourse.py", "verify_recourse.py"]
hashes = {
    name: hashlib.sha256((ROOT / "solver" / name).read_bytes()).hexdigest()
    for name in sources}
helper = "completion/theory/piecewise-recourse/scalar_piecewise.py"
hashes[helper] = hashlib.sha256((ROOT / helper).read_bytes()).hexdigest()
print(json.dumps({"passed": True, "rejected_mutations": rejected_mutations,
                  "records": records, "source_sha256": hashes}, indent=2))
