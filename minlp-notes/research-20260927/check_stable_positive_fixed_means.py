"""One focused check of the stable-positive submodular fixed-mean claim.

The graph is K_{2,3} with a triangle on the three binary vertices. Exact
fractions verify the common-threshold distribution and its moment lift.
Floating-point full and upper-RLT SDP solves challenge the predicted
fixed-mean optimum; they do not prove that optimum or the universal theorem.
"""

from fractions import Fraction as F

import cvxpy as cp
import numpy as np


CENTERS = (0, 1)
BINARY = (2, 3, 4)
D = (F(3, 2), F(5, 4), F(-1, 3), F(0), F(-2, 5))
LINEAR = (F(1, 2), F(3, 4), F(2, 3), F(-1, 4), F(7, 5))
WEIGHTS = {
    (0, 2): F(1),
    (0, 3): F(3, 2),
    (0, 4): F(2),
    (1, 2): F(2),
    (1, 3): F(1),
    (1, 4): F(1, 2),
    (2, 3): F(3, 4),
    (2, 4): F(2, 3),
    (3, 4): F(5, 6),
}
FIXED_MEANS = {2: F(1, 5), 3: F(1, 2), 4: F(4, 5)}


def objective(point):
    return sum(D[i] * point[i] ** 2 + LINEAR[i] * point[i] for i in range(5)) - sum(
        weight * point[i] * point[j] for (i, j), weight in WEIGHTS.items()
    )


def main():
    thresholds = sorted({F(0), F(1), *FIXED_MEANS.values()})
    atoms = []
    unclipped = {center: [] for center in CENTERS}
    for lower, upper in zip(thresholds, thresholds[1:]):
        midpoint = (lower + upper) / 2
        point = [F(0) for _ in range(5)]
        for binary in BINARY:
            point[binary] = F(FIXED_MEANS[binary] >= midpoint)
        for center in CENTERS:
            response = (
                sum(WEIGHTS[center, binary] * point[binary] for binary in BINARY)
                - LINEAR[center]
            ) / (2 * D[center])
            unclipped[center].append(response)
            point[center] = min(F(1), max(F(0), response))
        atoms.append((upper - lower, point))

    assert sum(probability for probability, _ in atoms) == 1
    for center in CENTERS:
        assert min(unclipped[center]) < 0
        assert max(unclipped[center]) > 1
        assert any(0 < response < 1 for response in unclipped[center])

    # The displayed finite positive rank-one decomposition proves PSD exactly.
    exact_lift = [[F(0) for _ in range(6)] for _ in range(6)]
    for probability, point in atoms:
        assert probability > 0
        assert all(0 <= value <= 1 for value in point)
        vector = [F(1), *point]
        for i in range(6):
            for j in range(6):
                exact_lift[i][j] += probability * vector[i] * vector[j]

    for i in range(1, 6):
        for j in range(1, 6):
            left, right = exact_lift[0][i], exact_lift[0][j]
            assert max(F(0), left + right - 1) <= exact_lift[i][j] <= min(left, right)
    for binary in BINARY:
        assert exact_lift[0][binary + 1] == FIXED_MEANS[binary]

    predicted = sum(probability * objective(point) for probability, point in atoms)
    lifted_value = sum(
        D[i] * exact_lift[i + 1][i + 1] + LINEAR[i] * exact_lift[0][i + 1]
        for i in range(5)
    ) - sum(weight * exact_lift[i + 1][j + 1] for (i, j), weight in WEIGHTS.items())
    assert predicted == lifted_value

    moment = cp.Variable((6, 6), symmetric=True)
    means = moment[0, 1:]
    products = moment[1:, 1:]
    upper_constraints = [moment >> 0, moment[0, 0] == 1, means >= 0, means <= 1]
    lower_constraints = []
    for i in range(5):
        for j in range(i, 5):
            lower_constraints.extend([
                products[i, j] >= 0,
                products[i, j] >= means[i] + means[j] - 1,
            ])
            upper_constraints.extend([
                products[i, j] <= means[i],
                products[i, j] <= means[j],
            ])
    upper_constraints.extend(means[i] == float(value) for i, value in FIXED_MEANS.items())
    relaxed = sum(float(D[i]) * products[i, i] + float(LINEAR[i]) * means[i] for i in range(5))
    relaxed -= sum(float(weight) * products[i, j] for (i, j), weight in WEIGHTS.items())
    for probability, point in atoms:
        print(f"probability={probability}; point={tuple(map(str, point))}; objective={objective(point)}")
    print(f"Exact common-threshold expectation: {predicted} ({float(predicted):.12f})")

    for name, include_lower in [("full SDP-RLT", True), ("PSD + upper RLT", False)]:
        constraints = upper_constraints + (lower_constraints if include_lower else [])
        problem = cp.Problem(cp.Minimize(relaxed), constraints)
        problem.solve(solver="CLARABEL", tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
        assert problem.status in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE), problem.status
        difference = problem.value - float(predicted)
        assert abs(difference) < 1e-7, difference

        solution = moment.value
        mean_solution = solution[0, 1:]
        product_solution = solution[1:, 1:]
        residuals = [abs(solution[0, 0] - 1), -np.min(np.linalg.eigvalsh(solution))]
        residuals.extend(-mean_solution)
        residuals.extend(mean_solution - 1)
        residuals.extend(abs(mean_solution[i] - float(value)) for i, value in FIXED_MEANS.items())
        for i in range(5):
            for j in range(5):
                value = product_solution[i, j]
                residuals.extend([value - mean_solution[i], value - mean_solution[j]])
                if include_lower:
                    residuals.extend([-value, mean_solution[i] + mean_solution[j] - 1 - value])
        largest_violation = max(0.0, *residuals)
        assert largest_violation < 1e-7, largest_violation
        print(f"{name} fixed-mean value: {problem.value:.12f}")
        print(f"  Solver status: {problem.status}")
        print(f"  Numerical minus exact value: {difference:.3e}")
        print(f"  Largest numerical constraint violation: {largest_violation:.3e}")
    print("Exact lift checks and both numerical fixed-mean comparisons passed.")


if __name__ == "__main__":
    main()
