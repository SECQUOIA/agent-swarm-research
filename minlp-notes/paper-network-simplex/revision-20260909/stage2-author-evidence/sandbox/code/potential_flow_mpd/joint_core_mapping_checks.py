"""Exact cycle/leaf identities and numerical LP-to-physical recovery checks."""
from fractions import Fraction as F

import numpy as np
import networkx as nx
from scipy.optimize import linprog

from block_rank_checks import subdivided_core, solve_smoothed
from pbflow import Graph


def check():
    rng = np.random.default_rng(290526)
    worst = 0.
    for trial in range(40):
        graph = subdivided_core('theta' if trial % 2 == 0 else 'k4', rng)
        n, m = len(graph), graph.number_of_edges()
        potential = list(map(int, rng.permutation(n)))
        exact_flow, exact_beta, arcs = [], [], []
        b = [F(0)]*n
        for u, v in graph.edges():
            drop = potential[u]-potential[v]
            x = F(int(rng.integers(1, 5)), int(rng.integers(1, 4)))
            if drop < 0:
                x = -x
            beta = F(drop)/(x*abs(x))
            assert beta > 0
            exact_flow.append(x)
            exact_beta.append(beta)
            arcs.append((u, v, beta))
            graph[u][v]['beta'] = float(beta)
            b[u] += x
            b[v] -= x
        G = Graph(n, arcs)
        tree, chords = G.spanning_forest()
        Z = [[int(z) for z in G.cycle_vector(tree, e)] for e in chords]
        A = [[F(z)*x*abs(x) for z, x in zip(row, exact_flow)] for row in Z]
        assert all(sum(a*beta for a, beta in zip(row, exact_beta)) == 0 for row in A)
        assert sum(b) == 0
        lower, upper = [beta/2 for beta in exact_beta], [2*beta for beta in exact_beta]
        # At fixed nonlinear core (hence fixed x), optimize the resistance
        # leaves by a conventional LP with r aggregate cycle equations.
        # The objective is a physical potential difference along a path.
        path = nx.shortest_path(graph, 0, 1)
        edge_index = {frozenset((u, v)): j for j, (u, v, _) in enumerate(arcs)}
        c = [F(0)]*m
        for u, v in zip(path, path[1:]):
            j = edge_index[frozenset((u, v))]
            sign = 1 if arcs[j][:2] == (u, v) else -1
            c[j] = sign*exact_flow[j]*abs(exact_flow[j])
        lp = linprog(-np.array(c, dtype=float), A_eq=np.array(A, dtype=float),
                     b_eq=np.zeros(len(chords)),
                     bounds=list(zip(map(float, lower), map(float, upper))), method='highs')
        assert lp.success
        for (u, v, _), beta in zip(arcs, lp.x):
            graph[u][v]['beta'] = beta
        x, pi, _, _, _, residual = solve_smoothed(graph, np.array(b, dtype=float), 0.)
        flow_error = max(abs(x-np.array(exact_flow, dtype=float)))
        drop_error = abs((pi[0]-pi[1])-np.array(c, dtype=float)@lp.x)
        worst = max(worst, flow_error, drop_error, residual)
        assert flow_error < 2e-7 and drop_error < 2e-7
        # The same core has the affine target-edge flow independently of
        # which LP-feasible resistance vector is used.
        target = trial % m
        assert abs(x[target]-float(exact_flow[target])) < 2e-7
    print('40 exact rational cycle/leaf identities passed on subdivided theta/K4 blocks.')
    print(f'LP resistance recovery preserved physical flows and path/edge objectives; max error {worst:.3g}.')


if __name__ == '__main__':
    check()
