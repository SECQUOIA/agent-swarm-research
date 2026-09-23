"""Nonlinear checks of objective-inactive block contraction.

These checks compare full physical states before/after contraction; they do not
implement the face enumeration or the proposed real-algebraic optimizer.
"""
import networkx as nx
import numpy as np

from block_rank_checks import solve_smoothed


def chain(length, rng):
    graph = nx.Graph()
    graph.add_nodes_from(range(3*length+1))
    for i in range(length):
        nodes = [3*i, 3*i+1, 3*i+2, 3*i+3, 3*i]
        for u, v in zip(nodes, nodes[1:]):
            graph.add_edge(u, v, beta=float(rng.uniform(.4, 2.5)))
    return graph


def contract_zero_blocks(graph, b, c):
    groups = nx.utils.UnionFind(graph)
    removed = 0
    for edges in nx.biconnected_component_edges(graph):
        edges = list(edges)
        vertices = {v for edge in edges for v in edge}
        exterior = graph.copy()
        exterior.remove_edges_from(edges)
        gamma = [sum(c[u] for u in nx.node_connected_component(exterior, v))
                 for v in vertices]
        if all(value == 0 for value in gamma):
            groups.union(*vertices)
            removed += 1
    roots = sorted({groups[v] for v in graph})
    index = {root: i for i, root in enumerate(roots)}
    mapping = {v: index[groups[v]] for v in graph}
    reduced = nx.Graph()
    reduced.add_nodes_from(range(len(roots)))
    for u, v, data in graph.edges(data=True):
        if mapping[u] != mapping[v]:
            assert not reduced.has_edge(mapping[u], mapping[v])
            reduced.add_edge(mapping[u], mapping[v], **data)
    load = np.zeros(len(roots))
    objective = np.zeros(len(roots))
    for v in graph:
        load[mapping[v]] += b[v]
        objective[mapping[v]] += c[v]
    return reduced, load, objective, mapping, removed


def flow_map(arcs, flow):
    return {(min(u, v), max(u, v)): x if u < v else -x
            for (u, v, _), x in zip(arcs, flow)}


def run():
    rng = np.random.default_rng(609067)
    worst_objective = worst_flow = worst_residual = 0.
    contractions = scenarios = 0
    for length in (12, 16, 20):
        graph = chain(length, rng)
        c = np.zeros(len(graph))
        c[0], c[3*(length//4)] = 1., -1.
        c[3*(3*length//4)], c[3*length] = 2., -2.
        for _ in range(3):
            b = rng.uniform(-1., 1., len(graph))
            b -= sum(b)/len(b)
            reduced, load, objective, mapping, removed = contract_zero_blocks(graph, b, c)
            assert removed >= length//2-1
            assert np.count_nonzero(objective) <= 4
            contractions += removed
            for rho in (0., .2):
                x, pi, _, _, arcs, residual = solve_smoothed(graph, b, rho)
                y, pressure, _, _, edges, reduced_residual = solve_smoothed(reduced, load, rho)
                obj_error = abs(c@pi-objective@pressure)
                worst_objective = max(worst_objective, obj_error)
                assert obj_error < 2e-8
                yf = flow_map(edges, y)
                for (u, v, _), value in zip(arcs, x):
                    a, d = mapping[u], mapping[v]
                    if a != d:
                        predicted = yf[(min(a,d), max(a,d))]*(1 if a < d else -1)
                        error = abs(value-predicted)
                        worst_flow = max(worst_flow, error)
                        assert error < 2e-8
                worst_residual = max(worst_residual, residual, reduced_residual)
                scenarios += 1
    print(f'PASS: {scenarios} physical scenario comparisons, {contractions} contracted blocks')
    print(f'Max objective error {worst_objective:.3g}, surviving flow error {worst_flow:.3g}, residual {worst_residual:.3g}')


if __name__ == '__main__':
    run()
