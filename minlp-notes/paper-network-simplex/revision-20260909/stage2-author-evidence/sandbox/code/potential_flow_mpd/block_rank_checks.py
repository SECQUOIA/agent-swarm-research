"""Checks for the bounded-block-cycle-rank MPD proof candidate.

Verifies suppression counts, smoothed adjoint derivatives, the positive-source
current identity, and all path threshold patterns, including an exact two-node
maximum plateau. This is not an implementation of real-algebraic optimization.
"""
import numpy as np
import networkx as nx
from pbflow import Graph


def core_paths(graph, a, c):
    core = {v for v in graph if graph.degree(v) >= 3} | {a, c}
    seen, paths = set(), []
    for v in sorted(core):
        for u in graph.neighbors(v):
            edge = frozenset((u, v))
            if edge in seen:
                continue
            path = [v, u]
            seen.add(edge)
            while path[-1] not in core:
                nxt, = [w for w in graph.neighbors(path[-1]) if w != path[-2]]
                seen.add(frozenset((path[-1], nxt)))
                path.append(nxt)
            paths.append(path)
    assert len(seen) == graph.number_of_edges()
    return core, paths


def path_patterns(k):
    """Finite states implied by a unimodal adjoint on k internal vertices."""
    states = set()
    for left in range(2*k+1):
        for right in range(left, 2*k+1):
            states.add(tuple('free' if 2*j+1 in (left, right)
                             else 'upper' if left < 2*j+1 < right else 'lower'
                             for j in range(k)))
    return states


def solve_smoothed(graph, b, rho):
    n = len(graph)
    arcs = [(u, v, d['beta']) for u, v, d in graph.edges(data=True)]
    G = Graph(n, arcs)
    tree, chords = G.spanning_forest()
    x0 = G.tree_flow(b, tree)
    Z = np.array([G.cycle_vector(tree, e) for e in chords])
    beta = np.array([d[2] for d in arcs])
    lam = np.zeros(len(chords))
    def energy(x):
        return np.sum(beta*(np.abs(x)**3/3+rho*x*x/2))
    for iteration in range(150):
        x = x0+Z.T@lam
        drop = beta*(x*np.abs(x)+rho*x)
        grad = Z@drop
        if np.max(np.abs(grad)) < 2e-11:
            break
        resistance = beta*(2*np.abs(x)+rho)
        hessian = (Z*resistance)@Z.T
        step = -np.linalg.solve(hessian, grad)
        if np.max(np.abs(grad)) < 1e-5:
            lam += step
            continue
        alpha = 1.
        while energy(x0+Z.T@(lam+alpha*step)) > energy(x)+1e-4*alpha*(grad@step):
            alpha *= 0.5
            if alpha < 1e-10:
                break
        lam += alpha*step
    x = x0+Z.T@lam
    drop = beta*(x*np.abs(x)+rho*x)
    incidence = np.zeros((n, len(arcs)))
    for j, (u, v, _) in enumerate(arcs):
        incidence[u, j], incidence[v, j] = 1., -1.
    pi = np.zeros(n)
    pi[1:] = np.linalg.lstsq(incidence[1:].T, drop, rcond=None)[0]
    residual = max(np.max(np.abs(incidence@x-b)), np.max(np.abs(incidence.T@pi-drop)))
    assert residual < 2e-8, (iteration, residual)
    return x, pi, incidence, beta, arcs, residual


def subdivided_core(kind, rng):
    skeleton = nx.MultiGraph()
    if kind == 'theta':
        skeleton.add_edges_from([(0, 1)]*3)
    else:
        skeleton = nx.MultiGraph(nx.complete_graph(4))
    graph = nx.Graph()
    graph.add_nodes_from(skeleton.nodes)
    next_vertex = len(skeleton)
    for u, v in skeleton.edges():
        count = int(rng.integers(1, 5))
        path = [u]+list(range(next_vertex, next_vertex+count))+[v]
        next_vertex += count
        for s, t in zip(path, path[1:]):
            graph.add_edge(s, t, beta=float(rng.uniform(.5, 3.)))
    return graph


def check():
    rng = np.random.default_rng(90526)
    worst_current = worst_derivative = worst_residual = 0.
    path_count = pattern_count = 0
    for trial in range(18):
        graph = subdivided_core('theta' if trial % 2 == 0 else 'k4', rng)
        # Some terminals have degree two, testing the marked-terminal count.
        a, c = (0, 1) if trial % 3 == 0 else (len(graph)-1, len(graph)-3)
        assert nx.is_biconnected(graph)
        rank = graph.number_of_edges()-len(graph)+1
        core, paths = core_paths(graph, a, c)
        assert len(core) <= 2*rank
        assert len(paths) == rank+len(core)-1 <= 3*rank-1
        assert len(core)+2*len(paths) <= 8*rank-2
        b = rng.uniform(-1, 1, len(graph))
        b[c] = -sum(np.delete(b, c))
        rho, delta = .2, .3
        x, pi, incidence, beta, arcs, residual = solve_smoothed(graph, b, rho)
        worst_residual = max(worst_residual, residual)
        resistance = beta*(2*np.abs(x)+rho)
        L = (incidence/resistance)@incidence.T
        rhs = np.zeros(len(graph))
        rhs[a], rhs[c] = 1., -1.
        internal = sorted(set(graph)-core)
        rhs[internal] += delta
        rhs[c] -= delta*len(internal)
        keep = [v for v in graph if v != c]
        h = np.zeros(len(graph))
        h[keep] = np.linalg.solve(L[np.ix_(keep, keep)], rhs[keep])
        resistance_map = {frozenset((u, v)): R for (u, v, _), R in zip(arcs, resistance)}
        for path in paths:
            path_count += 1
            current = np.array([(h[u]-h[v])/resistance_map[frozenset((u, v))]
                                for u, v in zip(path, path[1:])])
            if len(current) > 1:
                error = max(abs(np.diff(current)-delta))
                worst_current = max(worst_current, error)
                assert error < 1e-9
            states = path_patterns(len(path)-2)
            values = h[path[1:-1]]
            for level in list(values)+[min(h)-1., max(h)+1.]+list(rng.uniform(min(h), max(h), 5)):
                status = tuple('free' if abs(v-level) < 1e-9 else 'upper' if v > level else 'lower'
                               for v in values)
                assert status.count('free') <= 2
                assert status in states, (path, values, level, status)
                pattern_count += 1
        # Independent balanced-direction finite differences of the nonlinear
        # perturbed physical objective versus the electrical adjoint.
        def perturbed_objective(load):
            _, potential, _, _, _, _ = solve_smoothed(graph, load, rho)
            return potential[a]-potential[c]+delta*sum(potential[v]-potential[c] for v in internal)
        for v in rng.choice(keep, min(3, len(keep)), replace=False):
            direction = np.zeros(len(graph))
            direction[v], direction[c] = 1., -1.
            step = 1e-5
            fd = (perturbed_objective(b+step*direction)-perturbed_objective(b-step*direction))/(2*step)
            error = abs(fd-h[v])
            worst_derivative = max(worst_derivative, error)
            assert error < 2e-5, (trial, v, fd, h[v])
    # Exact integer plateau: currents -2,-1,0,1,2 have increment delta=1.
    plateau = [0, 2, 3, 3, 2, 0]
    current = [a-b for a, b in zip(plateau, plateau[1:])]
    assert all(b-a == 1 for a, b in zip(current, current[1:]))
    state = tuple('free' if h == 3 else 'lower' for h in plateau[1:-1])
    assert state == ('lower', 'free', 'free', 'lower')
    assert state in path_patterns(4)
    print(f'18 subdivided theta/K4 blocks: {path_count} paths and {pattern_count} threshold patterns passed.')
    print(f'Worst current identity error {worst_current:.3g}; adjoint finite-difference error {worst_derivative:.3g}; physical residual {worst_residual:.3g}.')
    print('Suppression counts and exact two-vertex maximum plateau passed.')


if __name__ == '__main__':
    check()
