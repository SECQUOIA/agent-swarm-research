"""Polynomial saturation-face enumeration for cactus MPD.

This module implements the structural reduction, not the theoretical exact
real-algebraic optimization subroutine. `numerical_check` maximizes every
one-dimensional face numerically and compares independent full-space SLSQP
solutions. Numerical success is evidence only.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product

import networkx as nx


@dataclass
class Face:
    fixed: list
    pivots: tuple
    lo: F
    hi: F
    balance: F

    def loads(self, z=None):
        z = self.lo if z is None else z
        b = list(self.fixed)
        if self.pivots:
            b[self.pivots[0]] = z
        if len(self.pivots) == 2:
            b[self.pivots[1]] = self.balance-z
        return b


def aggregate_core(graph, lower, upper, s, t):
    """Return core graph, summed intervals, terminals, and original groups."""
    blocks = [set(edges) for edges in nx.biconnected_component_edges(graph)]
    tree = nx.Graph()
    for i, edges in enumerate(blocks):
        nodes = set().union(*({u, v} for u, v in edges))
        assert len(edges) == 1 or len(edges) == len(nodes), 'graph must be a cactus'
        for v in nodes:
            tree.add_edge(('v', v), ('b', i))
    path = nx.shortest_path(tree, ('v', s), ('v', t))
    core_edges = set().union(*(blocks[i] for kind, i in path if kind == 'b'))
    core_nodes = sorted(set().union(*({u, v} for u, v in core_edges)))
    attached = graph.copy()
    attached.remove_edges_from(core_edges)
    groups = {}
    for component in nx.connected_components(attached):
        anchors = set(component).intersection(core_nodes)
        assert len(anchors) == 1
        groups[next(iter(anchors))] = sorted(component)
    index = {v: i for i, v in enumerate(core_nodes)}
    core = nx.Graph()
    core.add_nodes_from(range(len(core_nodes)))
    for u, v in core_edges:
        core.add_edge(index[u], index[v], beta=graph[u][v]['beta'])
    groups = [groups[v] for v in core_nodes]
    l = [sum((F(lower[v]) for v in group), F(0)) for group in groups]
    u = [sum((F(upper[v]) for v in group), F(0)) for group in groups]
    return core, l, u, index[s], index[t], groups


def nomination_faces(graph, lower, upper, s, t):
    """Enumerate feasible <=1D faces after core aggregation; exact rationals."""
    lower, upper = list(map(F, lower)), list(map(F, upper))
    blocks = [graph.edge_subgraph(edges).copy()
              for edges in nx.biconnected_component_edges(graph)]
    tree = nx.Graph()
    for i, block in enumerate(blocks):
        for v in block:
            tree.add_edge(('v', v), ('b', i))
    chain = nx.shortest_path(tree, ('v', s), ('v', t))
    ordered = [(blocks[chain[i][1]], chain[i-1][1], chain[i+1][1])
               for i in range(1, len(chain), 2)]
    n = len(graph)
    seen = set()

    def encode(assignments):
        pivots = tuple(v for v in range(n) if assignments[v] == 'free')
        assert len(pivots) <= 2
        fixed = [F(0) if assignments[v] == 'free' else
                 upper[v] if assignments[v] == 'upper' else lower[v]
                 for v in range(n)]
        balance = -sum(fixed)
        if not pivots:
            if balance:
                return None
            lo = hi = F(0)
        elif len(pivots) == 1:
            p, = pivots
            lo = hi = balance
            if not lower[p] <= lo <= upper[p]:
                return None
        else:
            p, q = pivots
            lo, hi = max(lower[p], balance-upper[q]), min(upper[p], balance-lower[q])
            if lo > hi:
                return None
        key = (tuple(fixed), pivots, lo, hi, balance)
        if key in seen:
            return None
        seen.add(key)
        return Face(fixed, pivots, lo, hi, balance)

    before = set()
    for block, entrance, exit in ordered:
        base = {v: 'upper' if v in before else 'lower' for v in graph}
        # A multiplier equal to either block terminal.
        for pivot, interior_state in [(entrance, 'lower'), (exit, 'upper')]:
            a = dict(base)
            a.update({v: interior_state for v in block})
            a[pivot] = 'free'
            face = encode(a)
            if face is not None:
                yield face
        paths = list(nx.all_simple_paths(block, entrance, exit))
        if len(paths) == 1:
            a = dict(base)
            a[entrance], a[exit] = 'upper', 'lower'
            face = encode(a)
            if face is not None:
                yield face
        else:
            assert len(paths) == 2

            def options(path):
                inner = path[1:-1]
                for gap in range(len(inner)+1):
                    yield {v: 'upper' if j < gap else 'lower'
                           for j, v in enumerate(inner)}
                for pivot in range(len(inner)):
                    yield {v: 'upper' if j < pivot else 'lower' if j > pivot else 'free'
                           for j, v in enumerate(inner)}

            for left, right in product(options(paths[0]), options(paths[1])):
                a = dict(base)
                a[entrance], a[exit] = 'upper', 'lower'
                a.update(left)
                a.update(right)
                face = encode(a)
                if face is not None:
                    yield face
        before.update(block.nodes)


def numerical_check(trials=20):
    import numpy as np
    from scipy.optimize import linprog, minimize, minimize_scalar
    from pbflow import Graph, solve_flow, check_flow

    rng = np.random.default_rng(50926)
    max_violation = 0.
    min_margin = float('inf')
    total_faces = 0
    variable_faces = 0
    for trial in range(trials):
        graph = nx.Graph()
        # Two cycles sharing an articulation, followed by a bridge;
        # a third off-path triangle tests aggregation separately.
        for cycle in ([0, 1, 2, 3], [2, 4, 5, 6]):
            for u, v in zip(cycle, cycle[1:]+cycle[:1]):
                graph.add_edge(u, v, beta=F(int(rng.integers(1, 8)), 3))
        graph.add_edge(5, 7, beta=F(2))
        for u, v in [(1, 8), (8, 9), (9, 1)]:
            graph.add_edge(u, v, beta=F(1))
        n = len(graph)
        half = rng.integers(-2, 3, n//2)
        offset = np.concatenate((half, -half))
        rng.shuffle(offset)
        lower = [int(offset[v]-rng.integers(1, 5)) for v in range(n)]
        upper = [int(offset[v]+rng.integers(1, 5)) for v in range(n)]
        original_s, original_t = [(0, 7), (1, 6), (3, 4), (8, 9)][trial % 4]
        core, lo, hi, s, t, groups = aggregate_core(graph, lower, upper, original_s, original_t)
        G = Graph(len(core), [(u, v, d['beta']) for u, v, d in core.edges(data=True)])

        def objective(b):
            b = np.array(b, dtype=float)
            # Smooth objective extension for SLSQP finite differences away
            # from its equality constraint; feasible iterates are unchanged.
            b[-1] = -sum(b[:-1])
            x, pi = solve_flow(G, b)
            nonlocal max_violation
            max_violation = max(max_violation, *check_flow(G, b, x, pi))
            return pi[s]-pi[t]

        faces = list(nomination_faces(core, lo, hi, s, t))
        assert faces
        total_faces += len(faces)
        variable_faces += sum(face.lo < face.hi for face in faces)
        best = -float('inf')
        best_b = None
        for face in faces:
            if face.lo == face.hi:
                candidates = [float(face.lo)]
            else:
                grid = np.linspace(float(face.lo), float(face.hi), 17)
                values = [objective(face.loads(z)) for z in grid]
                candidates = [grid[0], grid[-1]]
                for j in range(1, len(grid)-1):
                    if values[j] >= max(values[j-1], values[j+1]):
                        result = minimize_scalar(lambda z: -objective(face.loads(z)),
                                                 bounds=(grid[j-1], grid[j+1]),
                                                 method='bounded',
                                                 options={'xatol': 1e-10})
                        candidates.append(result.x)
            for z in candidates:
                b = face.loads(z)
                assert abs(float(sum(b))) < 1e-8
                assert all(float(l)-1e-8 <= float(v) <= float(u)+1e-8
                           for l, v, u in zip(lo, b, hi))
                value = objective(b)
                if value > best:
                    best, best_b = value, np.array(b, dtype=float)
        # Independent optimization on the full balanced box.
        full_best = -float('inf')
        for repeat in range(7):
            vertex = linprog(rng.normal(size=len(core)), A_eq=np.ones((1, len(core))),
                             b_eq=[0.], bounds=list(zip(map(float, lo), map(float, hi))),
                             method='highs')
            assert vertex.success
            start = vertex.x
            result = minimize(lambda b: -objective(b), start, method='SLSQP',
                              bounds=list(zip(map(float, lo), map(float, hi))),
                              constraints={'type': 'eq', 'fun': lambda b: b.sum()},
                              options={'ftol': 1e-9, 'maxiter': 150})
            if result.success and abs(result.x.sum()) < 1e-8:
                full_best = max(full_best, -result.fun)
        assert np.isfinite(full_best), 'all full-space numerical solves failed'
        margin = best-full_best
        min_margin = min(min_margin, margin)
        assert margin >= -2e-5, (trial, best, full_best)
        # Lipschitz test on balanced segments between the face optimum and
        # independent rational polytope vertices; use any fixed s-t path.
        path = nx.shortest_path(core, s, t)
        B = sum(max(abs(float(l)), abs(float(u))) for l, u in zip(lo, hi))
        C = 2*B*sum(float(core[u][v]['beta']) for u, v in zip(path, path[1:]))
        for weight in [0.1, 0.4, 0.8]:
            c = (1-weight)*best_b+weight*vertex.x
            assert abs(objective(c)-best) <= C*np.abs(c-best_b).sum()+1e-7
        # Exact interval disaggregation and physical invariance of the core.
        original_b = []
        for _ in range(n):
            original_b.append(F(0))
        # Use an exact face endpoint to avoid float feasibility ambiguity.
        agg_b = faces[0].loads()
        for group, total in zip(groups, agg_b):
            remainder = total-sum(lower[v] for v in group)
            for v in group:
                take = min(remainder, F(upper[v]-lower[v]))
                original_b[v] = F(lower[v])+take
                remainder -= take
            assert remainder == 0
        original = Graph(n, [(u, v, d['beta']) for u, v, d in graph.edges(data=True)])
        x, pi = solve_flow(original, original_b)
        assert max(check_flow(original, original_b, x, pi)) < 1e-7
        assert abs((pi[original_s]-pi[original_t])-objective(agg_b)) < 1e-7
    print(f'{trials} multi-entry cacti: {total_faces} feasible structural faces checked, {variable_faces} nondegenerate one-dimensional.')
    print(f'Every 7-start full-space SLSQP value <= face search within tolerance; min margin {min_margin:.3g}.')
    print(f'Aggregation/disaggregation and Lipschitz checks passed; maximum physical residual {max_violation:.3g}.')


if __name__ == '__main__':
    numerical_check()
