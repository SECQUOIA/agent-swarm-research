"""Independent bounded checks of exact implicit polynomial boundary output."""

from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "solver"))
from polynomial_grid import PolynomialBox, PolynomialFactor, solve
from polynomial_boundary import certify_boundary, discover_boundary
from verify_polynomial_boundary import BoundaryCertificateError, verify_certificate


def reject(certificate, problem):
    try:
        verify_certificate(certificate, problem)
    except BoundaryCertificateError:
        return
    raise AssertionError("tampered boundary artifact accepted")


def main():
    counts = {}
    # The irrational minimizer is (sqrt(2), 0). Global curvature in x is
    # positive here but a coarse interval Hessian proof can fail; discovery
    # must obtain a sufficiently informative globally valid retained box.
    irrational = PolynomialBox([[1, 2], [0, 1]], [PolynomialFactor((0, 1), [
        (1, (4, 0)), (-4, (2, 0)), (4, (0, 0)), (1, (0, 1)), (1, (2, 1))])])
    result = discover_boundary(irrational, max_rounds=5, time_limit=10)
    assert result["status"] == "certified", result
    cert = result["certificate"]
    checked = verify_certificate(cert, irrational)
    assert checked["kind"] == "strongly_convex_patch"
    (lo, hi), fixed = checked["face_bounds"]
    assert lo * lo <= 2 <= hi * hi and fixed == (F(0), F(0))
    counts["irrational_global_optimizer_patch"] = 1

    # Independent proof replay must not call the producer's derivative or
    # Hessian implementation. The verifier computes its own monomial bounds.
    with patch.object(PolynomialBox, "derivative_bounds", side_effect=AssertionError("producer derivative used")):
        with patch.object(PolynomialBox, "hessian", side_effect=AssertionError("producer Hessian used")):
            assert verify_certificate(cert, irrational)["valid"]
    counts["independent_derivative_replay"] = 1

    for field in ("derivative_lower", "endpoint"):
        broken = deepcopy(cert)
        broken["reductions"][0][field] = str(F(broken["reductions"][0][field]) + 1)
        reject(broken, irrational)
    broken = deepcopy(cert)
    broken["hessian_error"] = str(F(broken["hessian_error"]) + 1)
    reject(broken, irrational)
    broken = deepcopy(cert)
    broken["hessian"][0][0] = str(F(broken["hessian"][0][0]) + 1)
    reject(broken, irrational)
    counts["sign_endpoint_curvature_tamper_rejections"] = 4

    # First coordinate has ambiguous derivative until the second is clamped.
    # A repeat scan is necessary. Use a zero-stage global interval certificate
    # to avoid solving the multiaffine endpoint problem before the face test.
    coupled = PolynomialBox([[0, 1], [0, 1]], [PolynomialFactor((0, 1), [
        (1, (1, 1)), (F(-1, 2), (1, 0)), (1, (0, 1))])])
    result = certify_boundary(coupled, solve(coupled, max_stages=0))
    assert result["status"] == "certified"
    checked = verify_certificate(result["certificate"], coupled)
    assert checked["kind"] == "point" and checked["point"] == (F(1), F(0))
    assert [r["coordinate"] for r in result["certificate"]["reductions"]] == [1, 0]
    assert checked["value"] == F(-1, 2)
    counts["sequential_monotonicity_rescan"] = 1

    # Weak clamping selects only one member of a nonunique original optimal
    # set. The patch is unique on its restricted face, not on the original box.
    weak = PolynomialBox([[0, 1], [0, 1]], [PolynomialFactor((0,), [
        (1, (2,)), (F(-2, 3), (1,)), (F(1, 9), (0,))])])
    result = certify_boundary(weak, solve(weak, max_stages=0))
    checked = verify_certificate(result["certificate"], weak)
    assert checked["kind"] == "strongly_convex_patch" and checked["free"] == (0,)
    assert checked["face_bounds"][1] == (F(0), F(0))
    assert weak.value((F(1, 3), F(0))) == weak.value((F(1, 3), F(1))) == 0
    counts["weak_clamp_nonunique_original_set"] = 1

    # The original full Hessian is indefinite at zero. Clamping x=-1 leaves
    # a strongly convex y problem and retains the exact original minimum.
    indefinite = PolynomialBox([[-1, 1], [-1, 1]], [PolynomialFactor((0,), [
        (1, (4,)), (-2, (2,)), (9, (1,))]), PolynomialFactor((1,), [(1, (2,))])])
    assert indefinite.hessian((F(0), F(0)))[0][0] < 0
    result = certify_boundary(indefinite, solve(indefinite, max_stages=0))
    checked = verify_certificate(result["certificate"], indefinite)
    assert checked["kind"] == "strongly_convex_patch"
    assert checked["face_bounds"][0] == (F(-1), F(-1)) and checked["free"] == (1,)
    counts["indefinite_full_hessian_restricted_patch"] = 1

    # A non-singleton integer domain blocks implicit convex-face output.
    integer = PolynomialBox([[0, 2]], [PolynomialFactor((0,), [(1, (2,)), (-2, (1,))])], [0])
    result = certify_boundary(integer, solve(integer, max_stages=0))
    assert result["status"] == "inconclusive" and result["reason"] == "integer_labels_not_fixed"
    counts["unfixed_integer_rejection"] = 1
    result = certify_boundary(irrational, cert["grid_certificate"], time_limit=0)
    assert result["status"] == "inconclusive" and result["reason"] == "time_limit"
    counts["time_limit_inconclusive"] = 1
    print(counts)


if __name__ == "__main__":
    main()
