"""Numerical envelope/endpoint checks against exhaustive resistance scenarios.

These are mechanism checks, not a replacement for the written comparison proof.
The physical laws are the original unsmoothed quadratic laws.
"""
from itertools import product

import networkx as nx
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import root


def incidence(graph):
    edges = list(graph.edges)
    A = np.zeros((len(graph), len(edges)))
    for e, (u, v) in enumerate(edges):
        A[u, e], A[v, e] = 1., -1.
    return A, edges


def physical(A, b, cp, cm):
    x0 = np.linalg.lstsq(A, b, rcond=None)[0]
    C = null_space(A)
    if not C.shape[1]:
        return x0

    def fun(z):
        x = x0+C@z
        coef = np.where(x >= 0, cp, cm)
        return C.T@(coef*x*abs(x))

    def jac(z):
        x = x0+C@z
        coef = np.where(x >= 0, cp, cm)
        return C.T@((2*coef*abs(x))[:, None]*C)

    sol = root(fun, np.zeros(C.shape[1]), jac=jac, tol=1e-11)
    assert max(abs(fun(sol.x)), default=0.) < 1e-8
    x = x0+C@sol.x
    assert np.max(abs(A@x-b)) < 1e-9
    return x


def energy(x, cp, cm):
    return np.sum(np.where(x >= 0, cp, cm)*abs(x)**3)/3


def run():
    rng = np.random.default_rng(202609056)
    scenarios = extrema = rounded = energy_bounds = 0
    max_gap = max_residual = 0.
    for trial in range(12):
        graph = nx.complete_bipartite_graph(2, 3+trial % 2)
        graph.add_edge(0, len(graph))
        A, edges = incidence(graph)
        n, m = A.shape
        b = rng.uniform(-2, 2, n)
        b -= np.mean(b)
        lower = rng.uniform(.3, 1., m)
        upper = lower+rng.uniform(.2, 2., m)
        target = trial % m
        u, v = edges[target]
        q = np.zeros(n)
        q[u], q[v] = 1., -1.
        h = np.zeros(n)
        h[1:] = np.linalg.solve((A@A.T)[1:, 1:], q[1:])
        j = A.T@h
        signs = np.where(abs(j) < 1e-9, 0, np.sign(j))
        flows = []
        for choice in product([False, True], repeat=m):
            beta = np.where(choice, upper, lower)
            flows.append(physical(A, b, beta, beta)[target])
            scenarios += 1
        for direction in [1, -1]:
            # status +1 means pointwise maximum law, -1 means minimum.
            status = direction*signs
            status[target] = -direction
            cp = np.where(status > 0, upper, lower)
            cm = np.where(status < 0, upper, lower)
            x = physical(A, b, cp, cm)
            expected = max(flows) if direction == 1 else min(flows)
            gap = abs(x[target]-expected)
            assert gap < 1e-8, (trial, target, direction, gap)
            max_gap = max(max_gap, gap)
            extrema += 1
            beta = np.where(x >= 0, cp, cm)
            realized = physical(A, b, beta, beta)
            residual = max(abs(realized-x))
            assert residual < 1e-8
            max_residual = max(max_residual, residual)
            for eta in [.01, .1, .5]:
                noise = rng.uniform(-eta, eta, m)
                y = x+noise
                chosen = np.where(y >= 0, cp, cm)
                actual = physical(A, b, chosen, chosen)
                bound = np.sqrt(2*m*max(upper)/min(lower))*eta
                assert max(abs(actual-x)) <= bound+1e-8
                rounded += 1
            C = null_space(A)
            for _ in range(3):
                y = x+C@rng.normal(0, .2, C.shape[1])
                gap_e = energy(y, cp, cm)-energy(x, cp, cm)
                lower_bound = min(lower)*np.sum(abs(y-x)**3)/6
                assert gap_e+1e-9 >= lower_bound
                energy_bounds += 1
    print(f'{scenarios} endpoint scenarios, {extrema} envelope extrema checked.')
    print(f'{rounded} approximate-sign endpoint recoveries and {energy_bounds} energy bounds passed.')
    print(f'Max envelope mismatch {max_gap:.3g}; max endpoint-state residual {max_residual:.3g}.')


if __name__ == '__main__':
    run()
