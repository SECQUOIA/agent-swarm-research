"""Independent, bounded adversarial checks for optimal-set certificates.

Run from the repository root with python3 -B and this file's path.
"""

from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
from random import Random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "solver"))
from certified_grid import BoxQP, grid_dp
from optimal_sets import (diagonal_certificate, discover_diagonal_set,
                          recovery_radius, solve_endpoint_set)
from verify_optimal_sets import CertificateError, _psd, contains, verify_certificate


def determinant(matrix):
    answer = F(0)
    for order in permutations(range(len(matrix))):
        sign = (-1) ** sum(order[i] > order[j] for i in range(len(order))
                          for j in range(i + 1, len(order)))
        term = F(sign)
        for i, j in enumerate(order):
            term *= matrix[i][j]
        answer += term
    return answer


def main():
    rng = Random(83027)
    counts = {}
    # Principal minors provide a separate PSD criterion from Schur elimination.
    for case in range(150):
        n = 1 + case % 4
        matrix = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                matrix[i][j] = matrix[j][i] = F(rng.randrange(-3, 4))
        expected = all(determinant([[matrix[i][j] for j in indices] for i in indices]) >= 0
                       for k in range(1, n + 1) for indices in combinations(range(n), k))
        assert _psd(matrix, lambda: None) == expected
    counts["PSD_principal_minor_comparisons"] = 150

    endpoint_points = 0
    for case in range(24):
        # This is a branching decomposition whose vertex orders differ by bag.
        matrix = [[F(0)] * 4 for _ in range(4)]
        for i in range(4):
            matrix[i][i] = -F(rng.randrange(3))
        for i in (1, 2, 3):
            matrix[0][i] = matrix[i][0] = F(rng.randrange(-3, 4))
        bounds = [(F(-1), F(1)), (F(0), F(3)), (F(1, 3), F(4, 3)), (F(-2), F(2))]
        if case % 3 == 0:
            bounds[3] = (F(5, 7), F(5, 7))
            matrix[3][3] = F(7)  # Fixed coordinates need not be concave.
        model = BoxQP(matrix, [rng.randrange(-3, 4) for _ in range(4)], bounds, [1],
                      [[1, 0], [0, 3], [2, 0]], [[0, 1], [0, 2]], constant=F(2, 7))
        result = solve_endpoint_set(model)
        assert result["status"] == "certified"
        cert = result["certificate"]
        minimum = min(model.value(x) for x in product(*(tuple(dict.fromkeys(b)) for b in model.bounds)))
        assert verify_certificate(cert, model)["minimum"] == minimum
        domains = [tuple(dict.fromkeys((lo, (lo + hi) / 2, hi))) for lo, hi in model.bounds]
        domains[1] = tuple(map(F, range(4)))
        for point in product(*domains):
            assert contains(cert, point, model) == (model.value(point) == minimum)
            endpoint_points += 1
        broken = deepcopy(cert)
        broken["residuals"][0][0]["value"] = str(F(broken["residuals"][0][0]["value"]) + 1)
        try:
            verify_certificate(broken, model)
        except CertificateError:
            pass
        else:
            raise AssertionError("tampered residual accepted")

        # Finite DP must support negative corrections used by proximal search.
        grids = domains
        penalties = [[F(rng.randrange(-8, 9), 5) for x in grid] for grid in grids]
        finite = grid_dp(model, grids, penalties)
        rows = []
        for indices in product(*(range(len(grid)) for grid in grids)):
            point = tuple(grids[i][label] for i, label in enumerate(indices))
            value = model.value(point) - sum((penalties[i][label] for i, label in enumerate(indices)), F(0))
            rows.append((indices, value))
        assert finite["lower"] == min(v for _, v in rows)
        for i, grid in enumerate(grids):
            for label in range(len(grid)):
                assert finite["marginals"][i][label] == min(v for indices, v in rows if indices[i] == label)
    counts["endpoint_memberships"] = endpoint_points
    counts["signed_penalty_DP_and_marginal_comparisons"] = 24
    counts["tampered_residual_rejections"] = 24

    # Tilted and disconnected optimal continua, with positive diagonals.
    vector = [F(1), F(-1), F(1, 2)]
    hessian = [[2 * a * b for b in vector] for a in vector]
    hessian[2][2] -= F(1, 4)
    model = BoxQP(hessian, [0, 0, F(1, 8)], [[0, 1]] * 3, [], [[2, 0, 1]], [])
    diagonal_points = 0
    for anchor in ((F(0), F(0), F(0)), (F(1, 3), F(5, 6), F(1))):
        cert = diagonal_certificate(model, anchor)
        assert cert is not None
        for point in product((F(0), F(1, 4), F(1, 2), F(3, 4), F(1)), repeat=3):
            assert contains(cert, point) == (model.value(point) == 0)
            diagonal_points += 1
    counts["diagonal_full_set_memberships"] = diagonal_points

    # False K=1 yields a narrow interval around the wrong local minimum in
    # the original proximal theorem. Discovery must reject that candidate.
    model = BoxQP([[2, -3], [-3, 2]], [F(63, 128)] * 2, [[0, 1]] * 2,
                  [], [[1, 0]], [])
    assert diagonal_certificate(model, (F(0), F(0))) is None
    result = discover_diagonal_set(model, max_trials=1, max_stages=100,
                                  early_accept=False, time_limit=15)
    assert result["status"] == "inconclusive", result
    assert "certificate" not in result
    assert result["trials"][0]["rejected_candidates"] == 1
    counts["false_conditioning_final_candidate_rejections"] = 1

    # A fixed rational coordinate changes both the reduced linear coefficient
    # and its denominator, and hence the stationary-polytope height radius.
    full = BoxQP([[2, 1], [1, 7]], [-1, 4], [[0, 1], [F(1, 13), F(1, 13)]],
                 [], [[1, 0]], [])
    reduced = BoxQP([[2]], [F(-12, 13)], [[0, 1]], [], [[0]], [],
                    constant=F(7, 338) + F(4, 13))
    assert recovery_radius(full) == recovery_radius(reduced)
    result = discover_diagonal_set(full, max_trials=1, max_stages=100,
                                  early_accept=False, time_limit=15)
    assert result["status"] == "certified", result
    assert verify_certificate(result["certificate"], full)["point"] == (F(6, 13), F(1, 13))
    assert result["trials"][0]["completed_stages"] == result["trials"][0]["required_stages"]
    counts["fixed_substitution_complete_trial"] = 1
    # Each practical resource stop is inconclusive and must not carry a
    # certificate. A zero LP pivot budget exercises the shared oracle path.
    for limits, reason in (({"time_limit": 0}, "time_limit"),
                           ({"max_table_states": 1}, "table_limit"),
                           ({"max_stages": 1}, "stage_limit"),
                           ({"max_lp_pivots": 0}, "lp_pivot_limit")):
        result = discover_diagonal_set(full, early_accept=False, **limits)
        assert result["status"] == "inconclusive" and result["reason"] == reason, result
        assert "certificate" not in result
    endpoint = BoxQP([[-2]], [1], [[0, 3]], [0], [[0]], [])
    result = solve_endpoint_set(endpoint, max_table_states=1)
    assert result["status"] == "resource_limit" and "certificate" not in result
    counts["resource_stop_checks"] = 5
    print(counts)


if __name__ == "__main__":
    main()
