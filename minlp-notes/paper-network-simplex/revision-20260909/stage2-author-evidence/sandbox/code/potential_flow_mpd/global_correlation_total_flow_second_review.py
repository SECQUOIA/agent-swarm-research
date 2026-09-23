"""Independent exact checks of the actual globally correlated cactus gadget.

Tests every nonempty simple source graph on two through four vertices,
every binary parameter profile, and every nontrivial source threshold.
Radicals use exact arithmetic in Q(sqrt(2), sqrt(3)).
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt

import networkx as nx


def field(a=0, b=0, c=0, d=0):
    return tuple(map(F, (a, b, c, d)))


ZERO, ONE = field(), field(1)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale(s, a):
    return tuple(s*x for x in a)


def square(a):
    out = [F(0)]*4
    for i, x in enumerate(a):
        for j, y in enumerate(a):
            common = i & j
            out[i ^ j] += x*y*(2 if common & 1 else 1)*(3 if common & 2 else 1)
    return tuple(out)


def triangle_flow(r):
    return {1: field(F(1, 2)), 2: field(-1, 1),
            3: field(F(-1, 2), 0, F(1, 2))}[r]


def build(n, comparison_edges):
    graph = nx.DiGraph()
    triples = []
    # This actual bridge path stores every uncertain parameter r_i.
    for i in range(n):
        graph.add_edge(i, i+1, role="parameter", index=i)
    next_vertex = n+1
    previous_exit = None
    for comparison in comparison_edges:
        for sign in (1, -1):
            source = n if previous_exit is None else next_vertex
            if previous_exit is not None:
                next_vertex += 1
                graph.add_edge(previous_exit, source, role="fixed_bridge")
            middle, sink = next_vertex, next_vertex+1
            next_vertex += 2
            for u, v in ((source, middle), (middle, sink)):
                graph.add_edge(u, v, role="path", comparison=comparison, sign=sign)
            graph.add_edge(source, sink, role="alternate")
            triples.append((source, middle, sink))
            previous_exit = sink
    return graph, triples, previous_exit


def run():
    graphs = profiles = thresholds = 0
    a, b = field(-2, 2), field(0, 0, F(1, 2))
    kappa = add(b, scale(-1, a))
    assert F(173, 100)**2 < 3 and F(283, 200)**2 > 2
    assert F(173, 200)-F(283, 100)+2 == F(7, 200) > F(1, 32)
    for n in range(2, 5):
        possible = list(combinations(range(n), 2))
        for present in product((0, 1), repeat=len(possible)):
            edges = [e for e, yes in zip(possible, present) if yes]
            m = len(edges)
            if not m:
                continue
            graph, triangles, sink = build(n, edges)
            assert graph.number_of_nodes() == 6*m+n
            assert graph.number_of_edges() == 8*m-1+n
            assert nx.is_directed_acyclic_graph(graph)
            assert max(dict(graph.degree()).values()) <= 3
            blocks = list(nx.biconnected_components(graph.to_undirected()))
            assert sum(len(block) == 3 for block in blocks) == 2*m
            assert all(len(block) in (2, 3) for block in blocks)
            for theta in product((0, 1), repeat=n):
                flows, resistance = {}, {}
                balance = {v: ZERO for v in graph}
                total = ZERO
                for u, v, data in graph.edges(data=True):
                    role = data["role"]
                    if role == "parameter":
                        resistance[u, v] = 1+theta[data["index"]]
                        flow = ONE
                    elif role == "fixed_bridge":
                        resistance[u, v], flow = 2, ONE
                    elif role == "path":
                        i, j = data["comparison"]
                        r = 2+data["sign"]*(theta[i]-theta[j])
                        resistance[u, v], flow = r, triangle_flow(r)
                    else:
                        first = next(w for w in graph.successors(u) if w != v)
                        data_path = graph.edges[u, first]
                        i, j = data_path["comparison"]
                        r = 2+data_path["sign"]*(theta[i]-theta[j])
                        resistance[u, v], flow = 2, add(ONE, scale(-1, triangle_flow(r)))
                    assert 1 <= resistance[u, v] <= 3
                    flows[u, v] = flow
                    balance[u] = add(balance[u], flow)
                    balance[v] = add(balance[v], scale(-1, flow))
                    total = add(total, flow)
                for v in graph:
                    assert balance[v] == (ONE if v == 0 else scale(-1, ONE) if v == sink else ZERO)
                for source, middle, target in triangles:
                    assert flows[source, middle] == flows[middle, target]
                    path_drop = scale(resistance[source, middle]+resistance[middle, target],
                                      square(flows[source, middle]))
                    assert path_drop == scale(2, square(flows[source, target]))
                cut = sum(theta[i] != theta[j] for i, j in edges)
                predicted = add(field(4*m-1+n), add(scale(m, a), scale(cut, kappa)))
                assert total == predicted
                profiles += 1
            den = 1 << (8192*(m+1)-1).bit_length()
            midpoint2 = F(2*isqrt(2*den*den)+1, 2*den)
            midpoint3 = F(2*isqrt(3*den*den)+1, 2*den)
            for target in range(1, m+1):
                ca, cb = F(m-target)+F(1, 2), F(target)-F(1, 2)
                tau = 4*m-1+n+ca*(2*midpoint2-2)+cb*midpoint3/2
                error = ca/den+cb/(4*den)
                assert error <= F(1, 512)
                assert F(7, 400)-error > F(7, 512)
                assert tau.denominator <= 8*den
                thresholds += 1
            graphs += 1
    print(f"PASS: {graphs} actual cacti, {profiles} exact physical profiles, "
          f"{thresholds} rational thresholds; graph counts, cycle laws, objectives and gaps")


if __name__ == "__main__":
    run()
