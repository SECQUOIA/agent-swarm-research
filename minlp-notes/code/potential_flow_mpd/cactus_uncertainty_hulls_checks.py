"""Exact identities and smoothly regularized cactus hull mechanism checks."""
from fractions import Fraction as F
from itertools import product

import networkx as nx
import numpy as np

from block_rank_checks import solve_smoothed


def value(G, b, source, sink):
    _, pi, _, _, _, residual = solve_smoothed(G, b, 1e-9)
    assert residual < 1e-8
    return pi[source]-pi[sink]


def run():
    # The exact theta obstruction does not depend on floating-point evidence.
    for z, theta, span in [(F(3, 2), F(23, 108), F(49, 24)),
                           (F(1), F(1), F(2)),
                           (F(1, 2), F(71, 12), F(49, 24))]:
        assert (12*theta+1)*z*z+10*z-23 == 0
        assert (3*(z+1)**2+(7-z)**2)/24 == span
        assert ((7-z)**2-3*(z+1)**2)/24 == theta*z*z
    rng = np.random.default_rng(590529)
    max_excess = max_monotonic_violation = 0.
    for trial in range(18):
        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (2, 0), (2, 3),
                          (3, 4), (4, 5), (5, 6), (6, 3)])
        for u, v in G.edges:
            G[u][v]['beta'] = float(rng.uniform(.5, 2.))
        edges = list(G.edges)
        chosen = rng.choice(len(edges), 3, replace=False)
        b = rng.uniform(-1, 1, len(G))
        b[-1] = -sum(b[:-1])
        source, sink = 0, 5
        extrema, corners = [], []
        for inds in product(range(3), repeat=3):
            for e, ind in zip(chosen, inds):
                u, v = edges[e]
                G[u][v]['beta'] = [.2, 1., 4.][ind]
            f = value(G, b, source, sink)
            extrema.append(f)
            if all(ind != 1 for ind in inds):
                corners.append(f)
        excess = max(max(extrema)-max(corners), min(corners)-min(extrema))
        max_excess = max(max_excess, excess)
        assert excess < 2e-8
        # Vary one coefficient finely with all others held fixed.
        u, v = edges[chosen[0]]
        fs = []
        for beta in np.geomspace(.1, 10., 23):
            G[u][v]['beta'] = float(beta)
            fs.append(value(G, b, source, sink))
        diffs = np.diff(fs)
        violation = min(max(0., -min(diffs)), max(0., max(diffs)))
        max_monotonic_violation = max(max_monotonic_violation, violation)
        assert violation < 2e-8
    # Restore the missing edge in the theta example with growing resistance.
    G = nx.Graph()
    for u, v, beta in [(0, 2, .5), (2, 1, 1/6), (0, 3, 1/6),
                        (3, 1, .5), (2, 3, 1.)]:
        G.add_edge(u, v, beta=beta)
    b = np.array([4., -4., 3., -3.])
    gaps = []
    for M in [1e2, 1e4, 1e6]:
        G.add_edge(0, 1, beta=M)
        fs = []
        for theta in [23/108, 1., 71/12]:
            G[2][3]['beta'] = theta
            fs.append(value(G, b, 1, 0))
        gap = fs[1]-max(fs[0], fs[2])
        assert gap > 0
        gaps.append(gap)
    print('3 exact rational theta states, 18 cactus box grids, and 18 coordinate sweeps passed.')
    print(f'Max box-grid excess {max_excess:.3g}; monotonicity violation {max_monotonic_violation:.3g}.')
    print(f'Restored-edge interior gaps {gaps}; theta limit {1/24:.12g}.')


if __name__ == '__main__':
    run()
