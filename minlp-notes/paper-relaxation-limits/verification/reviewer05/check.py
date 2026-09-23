"""Independent finite checks; exact arithmetic except the explicitly marked LP check."""
from fractions import Fraction as F
from itertools import combinations, product
import json
import math
import networkx as nx
import numpy as np
from scipy.optimize import linprog


def solve(rows, n):
    a = [[F(x) for x in row] for row in rows]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        d = a[j][j]
        a[j] = [x/d for x in a[j]]
        for i in range(n):
            if i != j:
                d = a[i][j]
                a[i] = [x-d*y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def cell_check(n):
    planes = []
    for i in range(n):
        for rhs in (F(0), F(1, 2), F(1)):
            row = [F(0)] * (n+1)
            row[i], row[-1] = F(1), rhs
            planes.append(row)
    for i, j in combinations(range(n), 2):
        for sign, rhs in ((-1, 0), (1, 1)):
            row = [0] * (n+1)
            row[i], row[j], row[-1] = 1, sign, rhs
            planes.append(row)
    vertices = set()
    for rows in combinations(planes, n):
        x = solve(rows, n)
        if x is not None and all(0 <= t <= 1 for t in x):
            assert all(t in (0, F(1, 2), 1) for t in x)
            vertices.add(x)
    assert len(vertices) == 3**n
    return {"dimension": n, "bases": math.comb(len(planes), n), "vertices": len(vertices)}


def range_data(n, edges):
    signs = list(product((-1, 1), repeat=n))
    values = [sum(a*s[i]*s[j] for i,j,a in edges) for s in signs]
    return F(max(values)-min(values), 2), signs


def cut_checks():
    n = 4
    pairs = list(combinations(range(n), 2))
    total_induced = 0
    for weights in product((-1, 0, 1), repeat=len(pairs)):
        edges = [(i,j,a) for (i,j),a in zip(pairs, weights) if a]
        graph = nx.Graph()
        graph.add_nodes_from(range(n))
        graph.add_weighted_edges_from(edges)
        cycle_ok = all(
            sum(graph[u][v]['weight'] > 0 for u,v in zip(cyc, cyc[1:]+cyc[:1])) % 2 == 0
            and len(cyc) % 2 == 0 for cyc in nx.cycle_basis(graph)
        )
        full_R, _ = range_data(n, edges)
        assert (full_R == len(edges)) == cycle_ok
        for mask in range(1 << n):
            active = [(i,j,a) for i,j,a in edges if mask >> i & 1 and mask >> j & 1]
            R, signs = range_data(n, active)
            polarization = max(
                sum(a*s[i]*s[j] for i,j,a in active if ((cut >> i) ^ (cut >> j)) & 1)
                for cut in range(1 << n) for s in signs
            )
            assert R == polarization
            total_induced += 1
    return {"signed_supports": 3**6, "induced_checks": total_induced}


def flow_checks():
    n = 5
    pairs = list(combinations(range(n), 2))
    for flags in product((0, 1), repeat=len(pairs)):
        edges = [e for e, flag in zip(pairs, flags) if flag]
        if not edges:
            continue
        density = max(F(sum((mask >> i & 1) and (mask >> j & 1) for i,j in edges), mask.bit_count()) for mask in range(1, 1 << n))
        scale = density.denominator
        net = nx.DiGraph()
        for k, (i,j) in enumerate(edges):
            net.add_edge('source', ('edge', k), capacity=scale)
            for v in (i,j):
                net.add_edge(('edge', k), ('vertex', v), capacity=(len(edges)+1)*scale)
        for v in range(n):
            net.add_edge(('vertex', v), 'sink', capacity=density.numerator)
        value, _ = nx.maximum_flow(net, 'source', 'sink')
        assert value == len(edges)*scale
    return {"graphs": 2**10, "nonempty_flows": 2**10-1}


def numerical_envelopes():
    rng = np.random.default_rng(501)
    n = 4
    pairs = list(combinations(range(n), 2))
    verts = np.array(list(product((0, 1), repeat=n)))
    Aeq = np.vstack([np.ones(2**n), verts.T])
    points = list(product((0, .5, 1), repeat=n)) + list(rng.random((19, n)))
    for _ in range(12):
        weights = rng.integers(-4, 5, size=len(pairs))
        edges = [(i,j,int(a)) for (i,j),a in zip(pairs, weights) if a]
        ratios = []
        for mask in range(1 << n):
            active = [(i,j,a) for i,j,a in edges if mask >> i & 1 and mask >> j & 1]
            R, _ = range_data(n, active)
            ratios.append(float(sum(abs(a) for i,j,a in active)/R) if R else 0)
        cstar = max(ratios)
        obj = sum((a*verts[:, i]*verts[:, j] for i,j,a in edges), start=np.zeros(2**n))
        for x in points:
            rhs = np.r_[1, x]
            low = linprog(obj, A_eq=Aeq, b_eq=rhs, bounds=(0, None), method='highs')
            high = linprog(-obj, A_eq=Aeq, b_eq=rhs, bounds=(0, None), method='highs')
            assert low.success and high.success
            gap = -high.fun-low.fun
            term = sum(abs(a)*min(x[i], x[j], 1-x[i], 1-x[j]) for i,j,a in edges)
            assert term <= cstar*gap+1e-8
            if all(t in (0, .5, 1) for t in x):
                active = [(i,j,a) for i,j,a in edges if x[i] == x[j] == .5]
                R, _ = range_data(n, active)
                assert abs(gap-float(R)/2) < 1e-8
    return {"coefficient_vectors": 12, "points_per_vector": len(points), "LPs": 2400, "tolerance": 1e-8}


result = {"exact_cells": cell_check(4), "exact_cuts": cut_checks(), "exact_integer_flows": flow_checks(), "numerical_vertex_envelopes": numerical_envelopes()}
print(json.dumps(result, indent=2))
