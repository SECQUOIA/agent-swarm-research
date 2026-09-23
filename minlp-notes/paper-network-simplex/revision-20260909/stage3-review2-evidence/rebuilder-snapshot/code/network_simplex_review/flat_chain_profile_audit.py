"""Compare the flat-chain profile reduction to direct hull-vertex mixtures."""

from itertools import combinations, product
import json

import numpy as np
from scipy.optimize import linprog
import sympy as sp


def hull_matrix(L, m, observations):
    arcs = 2 * L + 1
    paths = []
    bypass = np.zeros(arcs)
    bypass[-1] = 1
    paths.append(bypass)
    for choices in product(range(2), repeat=L):
        path = np.zeros(arcs)
        for i, choice in enumerate(choices):
            path[2 * i + choice] = 1
        paths.append(path)
    columns = []
    for path in paths:
        for state in range(-1, m):
            y = np.array([float(j == state) for j in range(m)])
            z = np.array([path[e] * y[j] for e, j in observations])
            columns.append(np.concatenate(([1], path, y, z)))
    return np.array(columns).T


def profile_feasible(L, weights, x, obs):
    d = len(weights)
    if min(obs.values(), default=0) < -1e-10:
        return False
    rows, rhs = [], []
    def add(row, bound):
        rows.append(row)
        rhs.append(bound)
    eye = np.eye(d)
    add(np.ones(d), 1 - x[-1])
    add(-np.ones(d), x[-1] - 1)
    for j in range(d):
        if (2 * L, j) in obs:
            value = weights[j] - obs[2 * L, j]
            add(eye[j], value)
            add(-eye[j], -value)
    for i in range(L):
        B, U = [], []
        R = x[2 * i]
        for j in range(d):
            a = obs.get((2 * i, j))
            b = obs.get((2 * i + 1, j))
            if a is not None and b is not None:
                add(eye[j], a + b)
                add(-eye[j], -a - b)
                R -= a
            elif a is not None:
                add(-eye[j], -a)
                R -= a
            elif b is not None:
                add(-eye[j], -b)
                B.append(j)
                R += b
            else:
                U.append(j)
        row = np.zeros(d)
        row[B] = 1
        add(row.copy(), R)
        row[U] = 1
        add(-row, -R)
    result = linprog(np.zeros(d), A_ub=np.array(rows), b_ub=np.array(rhs),
                     bounds=[(0, val) for val in weights], method="highs")
    return result.success


def simple_graph_check(N):
    # Original serial join v_i is replaced by incoming I_i / outgoing O_i.
    incoming = ["s"] + [f"I{i}" for i in range(1, N)] + ["t"]
    outgoing = ["s"] + [f"O{i}" for i in range(1, N)] + ["t"]
    edges = [("s", "t")]
    edge_maps = [None]
    for i in range(N):
        edges += [(outgoing[i], incoming[i + 1]), (outgoing[i], f"B{i}"), (f"B{i}", incoming[i + 1])]
        edge_maps += [2 * i, 2 * i + 1, 2 * i + 1]
    for i in range(1, N):
        edges.append((incoming[i], outgoing[i]))
        edge_maps.append(-1)
    nodes = set(v for edge in edges for v in edge)
    assert len(nodes) == 3 * N and len(edges) == 4 * N
    assert len(set(frozenset(edge) for edge in edges)) == len(edges)
    assert max(sum(v in edge for edge in edges) for v in nodes) == 3
    count = 0
    for choices in [None] + list(product(range(2), repeat=N)):
        original = np.zeros(2 * N)
        if choices is not None:
            for i, choice in enumerate(choices):
                original[2 * i + choice] = 1
        new = [int(choices is None) if index is None else int(choices is not None) if index == -1 else original[index]
               for index in edge_maps]
        for v in nodes:
            excess = sum(val for (a, b), val in zip(edges, new) if a == v) - sum(val for (a, b), val in zip(edges, new) if b == v)
            assert excess == (1 if v == "s" else -1 if v == "t" else 0)
        assert all(val in (0, 1) for val in new)
        count += 1
    return count


def circuit_check(d):
    rows = []
    for bits in product(range(2), repeat=d):
        if any(bits):
            rows += [bits, tuple(-x for x in bits)]
    count = largest = 0
    for size in range(2, d + 2):
        for subset in combinations(rows, size):
            kernel = sp.Matrix(subset).T.nullspace()
            if len(kernel) != 1:
                continue
            vector = kernel[0]
            if not (all(x > 0 for x in vector) or all(x < 0 for x in vector)):
                continue
            denominator = sp.ilcm(*[x.q for x in vector])
            vector = [abs(int(x * denominator)) for x in vector]
            divisor = sp.igcd(*vector)
            vector = [x // divisor for x in vector]
            count += 1
            largest = max(largest, max(vector))
    assert (count, largest) == {1: (1, 1), 2: (5, 1), 3: (41, 2)}[d]
    return {"circuits": count, "maximum_primitive_weight": int(largest)}


def main():
    rng = np.random.default_rng(531820)
    checked = feasible = zero_residual = zero_explicit = 0
    for m in [1, 2, 3, 4]:
        for L in [1, 2, 3, 5]:
            for trial in range(20):
                weights = rng.dirichlet(np.ones(m + 1))
                if trial % 3 == 0:
                    weights[-1] = 0
                if trial % 4 == 0:
                    weights[0] = 0
                if weights.sum() == 0:
                    weights[-1] = 1
                weights /= weights.sum()
                zero_residual += int(weights[-1] == 0)
                zero_explicit += int(weights[0] == 0)
                w = weights * rng.uniform(0, 1, m + 1)
                state_flow = np.zeros((2 * L + 1, m + 1))
                for i in range(L):
                    state_flow[2 * i] = w * rng.uniform(0, 1, m + 1)
                    state_flow[2 * i + 1] = w - state_flow[2 * i]
                state_flow[-1] = weights - w
                x = state_flow.sum(axis=1)
                observations = [(e, j) for e in range(2 * L + 1) for j in range(m) if rng.random() < 0.6]
                obs = {(e, j): state_flow[e, j] for e, j in observations}
                if trial % 2 and observations:
                    pair = observations[rng.integers(len(observations))]
                    obs[pair] += rng.choice([-1, 1]) * rng.uniform(0.02, 0.25)
                matrix = hull_matrix(L, m, observations)
                rhs = np.concatenate(([1], x, weights[:-1], [obs[pair] for pair in observations]))
                direct = linprog(np.zeros(matrix.shape[1]), A_eq=matrix, b_eq=rhs, bounds=(0, None), method="highs")
                reduced = profile_feasible(L, weights, x, obs)
                assert direct.success == reduced, (m, L, trial, direct.message)
                checked += 1
                feasible += reduced
    path_checks = sum(simple_graph_check(N) for N in [3, 5, 7, 9])
    circuits = {d: circuit_check(d) for d in [1, 2, 3]}
    print(json.dumps({"profile_vs_vertex_checks": checked, "feasible": feasible,
                      "infeasible": checked - feasible, "zero_residual_cases": zero_residual,
                      "zero_explicit_cases": zero_explicit, "simple_graph_path_lifts": path_checks,
                      "independent_circuit_counts": circuits,
                      "status": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
