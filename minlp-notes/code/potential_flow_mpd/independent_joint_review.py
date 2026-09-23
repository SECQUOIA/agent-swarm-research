"""Independent numerical checks of joint resistance sensitivity and separation.

Uses a separately assembled incidence/cycle model and SciPy root solve.
This is not a global optimizer or a verification of the real-algebraic algorithm.
"""

import numpy as np
from scipy.optimize import root


EDGES = [(0, 1), (1, 3), (0, 2), (2, 3), (0, 4), (4, 3),
         (3, 5), (5, 6), (6, 7), (7, 5), (2, 8), (8, 9), (9, 2)]
N = 10
M = len(EDGES)
INCIDENCE = np.zeros((N, M))
for e, (u, v) in enumerate(EDGES):
    INCIDENCE[u, e] = 1
    INCIDENCE[v, e] = -1
TREE = [0, 1, 2, 4, 6, 7, 8, 10, 11]
CHORDS = [e for e in range(M) if e not in TREE]
BT = INCIDENCE[:-1, TREE]
CYCLES = np.zeros((len(CHORDS), M))
for i, e in enumerate(CHORDS):
    CYCLES[i, e] = 1
    CYCLES[i, TREE] = np.linalg.solve(BT, -INCIDENCE[:-1, e])
assert np.max(abs(INCIDENCE @ CYCLES.T)) == 0


def physical(b, beta, rho=0.0):
    tree_flow = np.zeros(M)
    tree_flow[TREE] = np.linalg.solve(BT, b[:-1])

    def residual(circulation):
        flow = tree_flow + CYCLES.T @ circulation
        return CYCLES @ (beta * (flow * abs(flow) + rho * flow))

    def jacobian(circulation):
        flow = tree_flow + CYCLES.T @ circulation
        return (CYCLES * (beta * (2 * abs(flow) + rho))) @ CYCLES.T

    result = root(residual, np.zeros(len(CHORDS)), jac=jacobian, tol=1e-11)
    assert np.max(abs(residual(result.x))) < 2e-9, result.message
    flow = tree_flow + CYCLES.T @ result.x
    drops = beta * (flow * abs(flow) + rho * flow)
    potential = np.zeros(N)
    potential[:-1] = np.linalg.solve(BT.T, drops[TREE])
    assert np.max(abs(INCIDENCE.T @ potential - drops)) < 2e-9
    return flow, potential, potential[0] - potential[7]


def main():
    rng = np.random.default_rng(672190)
    max_derivative_error = max_separation_error = max_current = 0.0
    derivative_checks = joint_checks = 0
    for _ in range(12):
        center = rng.uniform(-1, 1, N)
        center -= center.mean()
        lower, upper = center - 0.3, center + 0.3
        beta = rng.uniform(0.7, 1.8, M)
        rho = 0.13
        flow, _, _ = physical(center, beta, rho)
        conductance = 1 / (beta * (2 * abs(flow) + rho))
        laplacian = (INCIDENCE * conductance) @ INCIDENCE.T
        source = np.zeros(N)
        source[0], source[7] = 1, -1
        adjoint = np.zeros(N)
        adjoint[:-1] = np.linalg.solve(laplacian[:-1, :-1], source[:-1])
        current = conductance * (INCIDENCE.T @ adjoint)
        max_current = max(max_current, max(abs(current)))
        assert max(abs(current)) <= 1 + 1e-10
        predicted = current * (flow * abs(flow) + rho * flow)
        for e in range(M):
            displacement = np.zeros(M)
            displacement[e] = 1e-5
            finite_difference = (physical(center, beta + displacement, rho)[2]
                                 - physical(center, beta - displacement, rho)[2]) / 2e-5
            max_derivative_error = max(max_derivative_error, abs(finite_difference - predicted[e]))
            assert abs(finite_difference - predicted[e]) < 3e-7
            derivative_checks += 1

        old_flow, _, old_value = physical(center, beta)
        changed_b = center.copy()
        # Changes the active block's exit articulation load, but preserves
        # the active block total; downstream block flow must stay fixed.
        changed_b[3] += 0.1
        changed_b[1] -= 0.1
        changed_beta = beta.copy()
        changed_beta[:6] *= 0.8
        new_flow, _, _ = physical(changed_b, changed_beta)
        separation_error = max(abs(old_flow[6:] - new_flow[6:]))
        max_separation_error = max(max_separation_error, separation_error)
        assert separation_error < 2e-8

        # Off-path resistance changes must leave the entire s-t core flow fixed.
        offpath_beta = beta.copy()
        offpath_beta[10:] *= 1.1
        offpath_flow, _, _ = physical(center, offpath_beta)
        assert max(abs(offpath_flow[:10] - old_flow[:10])) < 2e-8

        rounded_b = np.round(center, 6)
        rounded_b[-1] = -sum(rounded_b[:-1])
        rounded_beta = np.round(beta, 6)
        assert np.all(lower <= rounded_b) and np.all(rounded_b <= upper)
        assert np.all(0.5 <= rounded_beta) and np.all(rounded_beta <= 2.0)
        rounded_value = physical(rounded_b, rounded_beta)[2]
        bound_b = sum(np.maximum(abs(lower), abs(upper)))
        # Simple objective path: 0--1--3--5--6--7, with beta_upper=2.
        lipschitz_b = 2 * bound_b * 10
        error_bound = (lipschitz_b * sum(abs(rounded_b - center))
                       + bound_b ** 2 * sum(abs(rounded_beta - beta)))
        assert abs(rounded_value - old_value) <= error_bound + 1e-9
        joint_checks += 1

    print(f"PASS: {derivative_checks} resistance finite differences; max error {max_derivative_error:.3g}.")
    print(f"PASS: 12 active-block and 12 off-path separation checks; max reported active-block error {max_separation_error:.3g}.")
    print(f"PASS: {joint_checks} balanced nomination/resistance rounding checks using recomputed physical flows.")
    print(f"Maximum absolute unit adjoint edge current: {max_current:.12g}.")


if __name__ == "__main__":
    main()
