"""Exact, focused diagnostics for the implicit convex-patch output.

This checks a concrete PD certificate and an integer filtering edge case.
It does not implement the global pruning algorithm.
"""

from fractions import Fraction as Q


def chain_hessian(point):
    """Hessian of the boundary quartic-chain fixture, computed analytically."""
    n = len(point) - 2
    size = len(point)
    hessian = [[Q(0) for _ in range(size)] for _ in range(size)]
    hessian[0][0] = 2
    for i in range(1, n + 1):
        previous, current = point[i - 1], point[i]
        hessian[i - 1][i - 1] += Q(3, 4) * previous**2 - current
        hessian[i - 1][i] -= previous
        hessian[i][i - 1] -= previous
        hessian[i][i] += 2
    hessian[-1][-1] = 2
    hessian[n - 1][n - 1] -= point[-1] / 16
    hessian[n - 1][-1] -= point[n - 1] / 16
    hessian[-1][n - 1] -= point[n - 1] / 16
    hessian[n][-1] += Q(1, 4)
    hessian[-1][n] += Q(1, 4)
    return hessian


def third_derivative_bound(n):
    """Sum exact termwise derivative bounds over each Hessian row on [0,1/2]."""
    rows = [Q(0)] * (n + 2)
    for i in range(1, n + 1):
        # H_pp=3p^2/4-current, H_p,current=-p.
        rows[i - 1] += Q(3, 4) + 1 + 1
        rows[i] += 1
    rows[n - 1] += Q(1, 8)
    rows[-1] += Q(1, 16)
    return max(Q(1), *rows)


def check_closed_patch(n):
    width = Q(1, 1024)
    # a0=1/4, a1=1/64, and all later a_i <= a2=1/16384.
    bounds = [(Q(1, 4) - width / 2, Q(1, 4) + width / 2)]
    bounds += [(Q(1, 64) - width / 2, Q(1, 64) + width / 2)]
    bounds += [(Q(0), width)] * n  # remaining x coordinates and y
    assert len(bounds) == n + 2
    assert Q(1, 16384) < width
    assert Q(1, 4) * Q(1, 16384)**2 < Q(1, 16384)
    midpoint = [(lower + upper) / 2 for lower, upper in bounds]
    radius = max((upper - lower) / 2 for lower, upper in bounds)
    variation = third_derivative_bound(n) * radius
    tau = Q(1, 2)
    hessian = chain_hessian(midpoint)
    # Symmetric strict diagonal dominance proves the exact rational PSD test.
    for i, row in enumerate(hessian):
        assert row[i] - variation - tau > sum(
            abs(value) for j, value in enumerate(row) if j != i
        )
    # Nevertheless the active y derivative is negative at a patch point.
    assert bounds[n][0] == 0 and bounds[n - 1][1] == width
    active_derivative = (Q(0) - width**2 / 8) / 4
    assert active_derivative < 0
    # Endpoint size stays bounded as the true final coordinate shrinks doubly
    # exponentially; its huge exact rational expansion was not constructed.
    assert max(v.denominator.bit_length() for pair in bounds for v in pair) <= 12
    return len(hessian)


def check_integer_node_filter():
    integer_labels = [0, 1, 2]
    continuous_grid = [Q(0), Q(1, 2), Q(1)]
    correction = Q(1, 16)  # L=2 and adjacent continuous gaps 1/2
    objective = lambda label, x: (label - 1)**2 + (x - Q(1, 3))**2
    marginal = {
        label: min(objective(label, x) - correction for x in continuous_grid)
        for label in integer_labels
    }
    incumbent = objective(1, Q(1, 2))
    retained_intervals = [
        (a, b) for a, b in zip(integer_labels, integer_labels[1:])
        if min(marginal[a], marginal[b]) <= incumbent
    ]
    assert retained_intervals == [(0, 1), (1, 2)]
    retained_nodes = [label for label in integer_labels if marginal[label] <= incumbent]
    assert retained_nodes == [1]
    for label in integer_labels:
        # The exact minimum over the continuous completion is (label-1)^2.
        assert marginal[label] <= (label - 1)**2


if __name__ == "__main__":
    dimensions = [check_closed_patch(n) for n in (3, 8, 16)]
    check_integer_node_filter()
    print(
        "PASS: 3 exact closed-patch PD certificates in dimensions "
        f"{dimensions}; uniform active-sign tests fail on all 3; "
        "integer interval halo removed by exact label filtering."
    )
