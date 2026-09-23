"""Independent flat-chain implementation checks using directed-path vertices.

Global validity is checked exactly by maximizing each cut over all path/simplex
vertices with an independent separable path calculation, including long chains.
Small-chain membership comparisons use a separately assembled vertex-mixture LP.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from network_simplex import Point


def vertex_matrix(length, m, observations):
    paths = [(F(0),) * (2 * length) + (F(1),)]
    for choice in product((0, 1), repeat=length):
        paths.append(tuple(F(e % 2 == choice[e // 2]) for e in range(2 * length)) + (F(0),))
    points = []
    for path in paths:
        for state in range(m + 1):
            y = tuple(F(j == state) for j in range(m))
            z = {(e, j): path[e] * y[j] for e, j in observations}
            points.append(Point(path, y, z))
    columns = [(F(1),) + p.x + p.y + tuple(p.z[o] for o in observations) for p in points]
    return np.array(columns, dtype=float).T


def direct_membership(length, m, observations, point):
    matrix = vertex_matrix(length, m, observations)
    rhs = (F(1),) + point.x + point.y + tuple(point.z[o] for o in observations)
    result = linprog(np.zeros(matrix.shape[1]), A_eq=matrix, b_eq=np.array(rhs, float),
                     bounds=(0, None), method="highs")
    assert result.status in (0, 2), result.message
    return result.success


def exact_global_cut(length, m, cut):
    # The base flow vertices are bypass or a choice of one arc per serial gadget.
    # Linear maximization over the latter separates independently by gadget.
    for state in range(m + 1):
        coefficients = [F(0)] * (2 * length + 1)
        constant = cut.constant
        for key, value in cut.coefficients.items():
            if key[0] == "x":
                coefficients[key[1]] += value
            elif key[0] == "y" and key[1] == state:
                constant += value
            elif key[0] == "z" and key[2] == state:
                coefficients[key[1]] += value
        chain_max = sum(max(coefficients[2 * i], coefficients[2 * i + 1]) for i in range(length))
        maximum = constant + max(coefficients[-1], chain_max)
        assert maximum <= 0, (state, cut, maximum)
    bound = {0: 2, 1: 3, 2: 8}[m]
    assert all(abs(value) <= bound for key, value in cut.coefficients.items() if key[0] in ("x", "z"))


def random_point(length, m, observations, rng, zero_explicit=False, zero_residual=False):
    raw = [rng.randint(1, 8) for _ in range(m + 1)]
    if zero_explicit and m:
        raw[0] = 0
    if zero_residual and m and not (zero_explicit and m == 1):
        raw[-1] = 0
    weights = tuple(F(v, sum(raw)) for v in raw)
    profile = [weight * F(rng.randint(0, 6), 6) for weight in weights]
    flows = [[F(0)] * (2 * length + 1) for _ in weights]
    for state, weight in enumerate(weights):
        flows[state][-1] = weight - profile[state]
        for i in range(length):
            a = profile[state] * F(rng.randint(0, 7), 7)
            flows[state][2 * i] = a
            flows[state][2 * i + 1] = profile[state] - a
    x = tuple(sum(flow[e] for flow in flows) for e in range(2 * length + 1))
    z = {(e, state): flows[state][e] for e, state in observations}
    return Point(x, weights[:-1], z)


def exact_decomposition(length, point, decomposition):
    weights = point.y + (1 - sum(point.y),)
    assert tuple(decomposition.weights) == weights
    flows = {}
    for state, weight in enumerate(weights):
        if not weight:
            continue
        flow = tuple(decomposition.flow(state))
        assert len(flow) == 2 * length + 1
        assert all(0 <= value <= 1 for value in flow)
        branch = 1 - flow[-1]
        assert all(flow[2 * i] + flow[2 * i + 1] == branch for i in range(length))
        flows[state] = flow
    for e, aggregate in enumerate(point.x):
        assert sum(weights[state] * flow[e] for state, flow in flows.items()) == aggregate
    for (e, state), value in point.z.items():
        assert (weights[state] * flows[state][e] if weights[state] else 0) == value


def run():
    from network_simplex.flat_chain import FlatChainSimplex, circuit_library, _profile_bases
    rng = random.Random(493772)
    counts = Counter()
    for d, expected in ((1, 1), (2, 5), (3, 41)):
        normals, circuits = circuit_library(d)
        assert len(circuits) == expected
        assert len({indices for indices, _ in circuits}) == expected
        for indices, multipliers in circuits:
            assert all(value > 0 for value in multipliers)
            assert all(sum(weight * normals[i][j] for i, weight in zip(indices, multipliers)) == 0 for j in range(d))
        for indices, inverse in _profile_bases(d):
            matrix = ((1,) * d,) + tuple(normals[i] for i in indices)
            assert all(sum(matrix[i][k] * inverse[k][j] for k in range(d)) == int(i == j)
                       for i in range(d) for j in range(d))
        counts["verified circuit count d=" + str(d)] = expected
    for m in range(3):
        for length in (1, 2, 3, 5, 40):
            for trial in range(12):
                observations = [(e, j) for e in range(2 * length + 1) for j in range(m)
                                if rng.random() < (.15 + .07 * trial)]
                model = FlatChainSimplex(length, m, observations)
                point = random_point(length, m, observations, rng, trial % 3 == 0, trial % 4 == 0)
                candidates = [point]
                if observations:
                    changed = dict(point.z)
                    for key in rng.sample(observations, min(len(observations), 1 + trial % 3)):
                        changed[key] += rng.choice((-1, 1)) * F(1, 13)
                    candidates.append(Point(point.x, point.y, changed))
                for candidate in candidates:
                    result = model.separate(candidate)
                    if length <= 5:
                        assert result.feasible == direct_membership(length, m, observations, candidate)
                        counts["direct path-hull comparisons"] += 1
                    assert result.feasible == model.separate(candidate, decompose=False).feasible
                    if result.feasible:
                        exact_decomposition(length, candidate, result.decomposition)
                        counts["exact accepted decomposition"] += 1
                    else:
                        assert result.cut.evaluate(candidate) > 0
                        exact_global_cut(length, m, result.cut)
                        counts[result.cut.reason] += 1
                domain = [Point((-F(1, 7),) + point.x[1:], point.y, point.z)]
                domain.append(Point((F(0) if point.x[0] else F(1),) + point.x[1:], point.y, point.z))
                if m:
                    domain += [Point(point.x, (-1,) + point.y[1:], point.z),
                               Point(point.x, (2,) + point.y[1:], point.z)]
                for candidate in domain:
                    result = model.separate(candidate)
                    assert not result.feasible and result.cut.evaluate(candidate) > 0
                    exact_global_cut(length, m, result.cut)
                    counts["domain: " + result.cut.reason] += 1
    # Individually feasible gadget states with mutually inconsistent shared
    # branch profile; all observed values and original-domain constraints pass.
    obs = [(e, 0) for e in range(4)]
    model = FlatChainSimplex(2, 1, obs)
    inconsistent = Point((F(1, 4),) * 4 + (F(1, 2),), (F(1, 2),),
                         {(0, 0): 0, (1, 0): 0, (2, 0): F(1, 4), (3, 0): F(1, 4)})
    result = model.separate(inconsistent)
    assert not result.feasible and result.cut.reason == "flat profile positive circuit"
    assert result.cut.evaluate(inconsistent) > 0
    exact_global_cut(2, 1, result.cut)
    assert not direct_membership(2, 1, obs, inconsistent)
    counts["structured shared-profile contradiction"] += 1
    # Complete observations at two extreme profiles: all bypass, or all chain.
    for m in range(3):
        length = 5
        obs = [(e, j) for e in range(2 * length + 1) for j in range(m)]
        model = FlatChainSimplex(length, m, obs)
        y = (F(1, m + 1),) * m
        for bypass in (F(0), F(1)):
            x = ((1 - bypass) / 2,) * (2 * length) + (bypass,)
            point = Point(x, y, {(e, j): x[e] * y[j] for e, j in obs})
            result = model.separate(point)
            assert result.feasible
            exact_decomposition(length, point, result.decomposition)
            counts["extreme-profile exact decomposition"] += 1
    for observation in ((F(1, 2), 0), (0, F(1, 2))):
        try:
            FlatChainSimplex(2, 1, [observation])
        except ValueError:
            pass
        else:
            raise AssertionError("Noninteger observation index accepted")
    print(dict(sorted(counts.items())))
    print("PASS: independent path-hull membership, exact global cuts, exact state-flow reconstruction")


if __name__ == "__main__":
    run()
