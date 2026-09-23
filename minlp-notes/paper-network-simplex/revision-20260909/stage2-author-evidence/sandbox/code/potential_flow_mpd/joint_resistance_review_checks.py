"""Independent numerical checks of the joint MPD sensitivity bound.

This checks the ordinary unit-source adjoint used for rational recovery,
not the perturbed adjoint used in the nomination-face proof.
"""
import networkx as nx
import numpy as np

from block_rank_checks import solve_smoothed, subdivided_core


def check():
    rng = np.random.default_rng(77190526)
    max_current = max_derivative_error = max_residual = 0.0
    derivative_count = 0
    for trial in range(12):
        graph = subdivided_core('theta' if trial % 2 == 0 else 'k4', rng)
        n = len(graph)
        s, t = (0, 1) if trial % 3 == 0 else (n - 1, n - 3)
        rho = 0.13
        b = rng.uniform(-1.5, 1.5, n)
        c = b + rng.uniform(-0.2, 0.2, n)
        b[t] = -sum(np.delete(b, t))
        c[t] = -sum(np.delete(c, t))
        lower = np.minimum(b, c) - 0.1
        upper = np.maximum(b, c) + 0.1
        bound = sum(np.maximum(abs(lower), abs(upper)))

        x, pi, incidence, beta, arcs, residual = solve_smoothed(graph, b, rho)
        max_residual = max(max_residual, residual)
        electrical_resistance = beta * (2 * abs(x) + rho)
        laplacian = (incidence / electrical_resistance) @ incidence.T
        rhs = np.zeros(n)
        rhs[s], rhs[t] = 1.0, -1.0
        keep = [v for v in range(n) if v != t]
        adjoint = np.zeros(n)
        adjoint[keep] = np.linalg.solve(laplacian[np.ix_(keep, keep)], rhs[keep])
        current = (incidence.T @ adjoint) / electrical_resistance
        max_current = max(max_current, max(abs(current)))
        assert max(abs(current)) <= 1 + 1e-10
        predicted = current * (x * abs(x) + rho * x)
        assert max(abs(predicted)) <= bound**2 + rho * bound + 1e-10

        for edge in rng.choice(len(arcs), min(5, len(arcs)), replace=False):
            u, v, value = arcs[edge]
            step = 1e-5
            graph[u][v]['beta'] = value + step
            plus = solve_smoothed(graph, b, rho)[1]
            graph[u][v]['beta'] = value - step
            minus = solve_smoothed(graph, b, rho)[1]
            graph[u][v]['beta'] = value
            observed = ((plus[s] - plus[t]) - (minus[s] - minus[t])) / (2 * step)
            error = abs(observed - predicted[edge])
            max_derivative_error = max(max_derivative_error, error)
            assert error < 3e-6, (trial, edge, error)
            derivative_count += 1

        gamma = rng.uniform(0.5, 3.0, len(arcs))
        for (u, v, _), value in zip(arcs, gamma):
            graph[u][v]['beta'] = value
        _, other_pi, _, _, _, residual = solve_smoothed(graph, c, rho)
        max_residual = max(max_residual, residual)
        path_length = len(nx.shortest_path(graph, s, t)) - 1
        nomination_constant = (2 * bound + rho) * 3.0 * path_length
        resistance_constant = bound**2 + rho * bound
        joint_bound = (nomination_constant * sum(abs(b - c))
                       + resistance_constant * sum(abs(beta - gamma)))
        actual_change = abs((pi[s] - pi[t]) - (other_pi[s] - other_pi[t]))
        assert actual_change <= joint_bound + 1e-8

    print(f'PASS {derivative_count} ordinary-adjoint resistance derivatives and 12 joint bounds.')
    print(f'Maximum absolute unit-adjoint edge current: {max_current:.12g}.')
    print(f'Maximum finite-difference error: {max_derivative_error:.3g}.')
    print(f'Maximum physical residual: {max_residual:.3g}.')


if __name__ == '__main__':
    check()
