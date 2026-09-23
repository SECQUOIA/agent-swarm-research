"""Evidence for the unreviewed joint-resistance MPD extension."""
from fractions import Fraction

import numpy as np
import networkx as nx
from block_rank_checks import core_paths, solve_smoothed, subdivided_core


def runs(sequence):
    return 0 if not sequence else 1+sum(a != b for a, b in zip(sequence, sequence[1:]))


def check():
    rng = np.random.default_rng(190526)
    worst = 0.
    for trial in range(8):
        graph = subdivided_core('theta' if trial % 2 == 0 else 'k4', rng)
        a, c = 0, 1
        core, paths = core_paths(graph, a, c)
        internal = sorted(set(graph)-core)
        b = rng.uniform(-1, 1, len(graph))
        b[c] = -sum(np.delete(b, c))
        rho, delta = .2, .3
        x, pi, incidence, beta, arcs, _ = solve_smoothed(graph, b, rho)
        resistance = beta*(2*np.abs(x)+rho)
        L = (incidence/resistance)@incidence.T
        rhs = np.zeros(len(graph))
        rhs[a], rhs[c] = 1., -1.
        rhs[internal] += delta
        rhs[c] -= delta*len(internal)
        keep = [v for v in graph if v != c]
        h = np.zeros(len(graph))
        h[keep] = np.linalg.solve(L[np.ix_(keep, keep)], rhs[keep])
        predicted = (incidence.T@h)/resistance*(x*np.abs(x)+rho*x)
        def obj():
            _, pot, _, _, _, _ = solve_smoothed(graph, b, rho)
            return pot[a]-pot[c]+delta*sum(pot[v]-pot[c] for v in internal)
        for edge in rng.choice(len(arcs), min(6, len(arcs)), replace=False):
            u, v, value = arcs[edge]
            step = 1e-5
            graph[u][v]['beta'] = value+step
            plus = obj()
            graph[u][v]['beta'] = value-step
            minus = obj()
            graph[u][v]['beta'] = value
            error = abs((plus-minus)/(2*step)-predicted[edge])
            worst = max(worst, error)
            assert error < 2e-6, (trial, edge, error)
    # Exact long-path sign counting with arbitrary free-pivot jumps.
    worst_flow_runs = worst_beta_runs = 0
    for _ in range(2000):
        k = int(rng.integers(2, 70))
        left, right = sorted(rng.integers(0, k, 2))
        physical = [Fraction(int(rng.integers(-10, 11)), 2)]
        for i in range(k):
            value = int(rng.integers(0, 11))
            if i in (left, right):
                value *= int(rng.choice([-1, 1]))
            elif i < left or i > right:
                value = -value
            physical.append(physical[-1]+value)
        start = Fraction(int(rng.integers(-2*k, 2*k)), 2)
        adjoint_current = [start+i for i in range(k+1)]
        sign = lambda value: (value > 0)-(value < 0)
        flow_signs = [sign(value) for value in physical]
        states = ['lower' if x == 0 else 'free' if j == 0 else 'upper' if x*j > 0 else 'lower'
                  for x, j in zip(physical, adjoint_current)]
        worst_flow_runs = max(worst_flow_runs, runs(flow_signs))
        worst_beta_runs = max(worst_beta_runs, runs(states))
        assert runs(flow_signs) <= 15
        assert runs(states) <= 17
        assert states.count('free') <= 1
    # Zero-flow resistance changes preserve physical variables but need not
    # preserve adjoints: this is why the proof must recompute KKT data.
    graph = nx.Graph()
    for u, v in [(0, 1), (1, 3), (0, 2), (2, 3), (1, 2)]:
        graph.add_edge(u, v, beta=1.)
    b = np.array([1., 0., 0., -1.])
    first = solve_smoothed(graph, b, .2)
    graph[1][2]['beta'] = 9.
    second = solve_smoothed(graph, b, .2)
    assert max(abs(first[0]-second[0])) < 1e-10
    assert max(abs(first[1]-second[1])) < 1e-10
    h_values = []
    for x, pi, incidence, beta, arcs, _ in [first, second]:
        resistance = beta*(2*abs(x)+.2)
        L = (incidence/resistance)@incidence.T
        h_values.append(np.linalg.solve(L[:3, :3], [1., .3, 0.]))
    assert max(abs(h_values[0]-h_values[1])) > .001
    print(f'48 resistance derivative checks passed; maximum finite-difference error {worst:.3g}.')
    print(f'2000 exact long-path checks passed; maximum physical sign runs {worst_flow_runs}, resistance-state runs {worst_beta_runs}.')
    print('Zero-flow resistance change preserved physical variables while changing the adjoint, as expected.')


if __name__ == '__main__':
    check()
