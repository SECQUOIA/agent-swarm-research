"""Exact independent boundary checks for near-optimal response compression.

These calculations use rational arithmetic, no repository solver, and no
floating-point tolerances. They supplement the proof audit; they do not
implement quantifier elimination or establish the general theorem.
"""

from fractions import Fraction as F
from itertools import combinations, product
import json


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def cost(x, z):
    return z*z*(1-z)**2 + x*(3*z*z-2*z**3)


def run():
    checks = {}

    # A nonconvex near-optimal maximizer need not be an unrestricted KKT
    # point. With delta=9/256, the projection consists of [0,1/4] U [3/4,1].
    delta = F(9, 256)
    for z in [F(1, 4), F(3, 4)]:
        assert z*z*(1-z)**2 == delta
        assert 2*z*(1-z)*(1-2*z) != 0
        assert -(z-F(1, 2))**2 == -F(1, 16)
    assert F(1, 16) > delta  # the middle stationary point is inadmissible
    for z in [F(0), F(1)]:
        assert -(z-F(1, 2))**2 == -F(1, 4)
    checks['nonstationary_worst_response'] = 2

    # Exact weighted minimum on an affine measurement fiber. Algebraically,
    # sum_i a_i*z_i^2 = t^2/S + sum_i a_i*(z_i-t*c_i/(a_i*S))^2,
    # where t=c^T z and S=sum_i c_i^2/a_i. The same square-root field gives
    # the maximum measurement and every coordinate of its witness.
    models = 0
    grid_points = 0
    for n in range(1, 8):
        a = [F(i+1) for i in range(n)]
        measurements = [tuple(F(i == j) for i in range(n)) for j in range(n)]
        measurements += [tuple(F((-1)**i*(i+1)) for i in range(n))]
        for c in measurements:
            s = sum(ci*ci/ai for ai, ci in zip(a, c))
            assert s > 0
            delta = F(1, 4)
            q_squared = delta*s
            witness_factor = [ci/(ai*s) for ai, ci in zip(a, c)]
            assert sum(ci*yi for ci, yi in zip(c, witness_factor)) == 1
            assert sum(ai*yi*yi for ai, yi in zip(a, witness_factor))*q_squared == delta
            assert all(yi*yi*q_squared <= 1 for yi in witness_factor)
            for z in product([F(-1, 2), F(0), F(1, 2)], repeat=n):
                t = sum(ci*zi for ci, zi in zip(c, z))
                lhs = sum(ai*zi*zi for ai, zi in zip(a, z))
                residual = sum(ai*(zi-t*yi)**2 for ai, zi, yi in zip(a, z, witness_factor))
                assert lhs == t*t/s+residual
                grid_points += 1
            models += 1
    checks['measurement_models'] = models
    checks['fiber_identity_points'] = grid_points

    # Positive budget, fixed normals, and a unique nominal optimizer still
    # permit robust nonattainment if the follower cost is nonconvex.
    delta = F(1, 16)
    # f(delta,z)-delta = (z-1)^2*(z^2-2*delta*z-delta).
    expected = [-delta, F(0), 1+3*delta, -2-2*delta, F(1)]
    assert mul([F(1), F(-2), F(1)], [-delta, -2*delta, F(1)]) == expected
    # The final quadratic is strictly positive throughout (1/2,1].
    assert F(1, 4)-2*delta*F(1, 2)-delta > 0
    assert 1-2*delta > 0  # its derivative is positive on [1/2,1]
    assert cost(delta, F(1)) == delta
    sampled_exclusions = 0
    for x in [delta+F(i, 1024) for i in range(1, 65)]:
        assert delta < x <= F(1, 8)
        assert cost(x, F(0)) == 0
        for z in [F(i, 64) for i in range(33, 65)]:
            assert cost(x, z) > delta
            sampled_exclusions += 1
    checks['positive_budget_polynomial_identity'] = 1
    checks['positive_budget_sampled_exclusions'] = sampled_exclusions

    # Every graph on at most four vertices: no ternary cube point beats
    # the best binary cut. The written coordinate-convexity proof covers
    # all real cube points and arbitrary graph sizes.
    graphs = 0
    graph_points = 0
    for n in range(1, 5):
        all_edges = list(combinations(range(n), 2))
        for present in product([False, True], repeat=len(all_edges)):
            edges = [edge for edge, included in zip(all_edges, present) if included]
            max_cut = max(sum((z[i]-z[j])**2 for i, j in edges)
                          for z in product([0, 1], repeat=n))
            for z in product([F(0), F(1, 2), F(1)], repeat=n):
                assert sum(zi*zi for zi in z)/2 <= F(n, 2)
                assert sum((z[i]-z[j])**2 for i, j in edges) <= max_cut
                graph_points += 1
            graphs += 1
    checks['maxcut_graphs'] = graphs
    checks['maxcut_cube_points'] = graph_points
    print(json.dumps(checks, sort_keys=True))


if __name__ == '__main__':
    run()
