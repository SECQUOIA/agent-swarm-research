"""Heterogeneous C1 polynomial-law checks for the extension candidate."""
from fractions import Fraction as F

import numpy as np
from pbflow import Graph
from block_rank_checks import core_paths, subdivided_core


# Each tuple is (law, derivative, primitive), scalar operations supporting
# exact Fractions for the law and floats for numerical physical solves.
LAWS = [
    (lambda x: x, lambda x: 1., lambda x: x*x/2),
    (lambda x: x*abs(x), lambda x: 2*abs(x), lambda x: abs(x)**3/3),
    (lambda x: x**3+x/3, lambda x: 3*x*x+1/3, lambda x: x**4/4+x*x/6),
    (lambda x: x+max(x-1, 0)**2,
     lambda x: 1+2*max(x-1, 0),
     lambda x: x*x/2+max(x-1, 0)**3/3),
    (lambda x: x+max(x-1, 0)**4-max(-x-1, 0)**4,
     lambda x: 1+4*max(x-1, 0)**3+4*max(-x-1, 0)**3,
     lambda x: x*x/2+(max(x-1, 0)**5+max(-x-1, 0)**5)/5),
]


def solve(G, b, laws, beta, rho=.1):
    tree, chords = G.spanning_forest()
    x0 = G.tree_flow(b, tree)
    Z = np.array([G.cycle_vector(tree, e) for e in chords])
    lam = np.zeros(len(chords))
    def values(x, item):
        return np.array([LAWS[i][item](v) for i, v in zip(laws, x)])
    def energy(x):
        return np.sum(beta*(values(x, 2)+rho*x*x/2))
    for iteration in range(150):
        x = x0+Z.T@lam
        drop = beta*(values(x, 0)+rho*x)
        grad = Z@drop
        if max(abs(grad)) < 1e-10:
            break
        resistance = beta*(values(x, 1)+rho)
        step = -np.linalg.solve((Z*resistance)@Z.T, grad)
        if max(abs(grad)) < 1e-5:
            lam += step
            continue
        alpha = 1.
        while energy(x0+Z.T@(lam+alpha*step)) > energy(x)+1e-4*alpha*(grad@step):
            alpha *= .5
            assert alpha > 1e-12
        lam += alpha*step
    x = x0+Z.T@lam
    drop = beta*(values(x, 0)+rho*x)
    resistance = beta*(values(x, 1)+rho)
    incidence = np.zeros((G.n, G.m))
    for j, (u, v, _) in enumerate(G.arcs):
        incidence[u, j], incidence[v, j] = 1., -1.
    pi = np.zeros(G.n)
    pi[1:] = np.linalg.lstsq(incidence[1:].T, drop, rcond=None)[0]
    residual = max(max(abs(incidence@x-b)), max(abs(incidence.T@pi-drop)))
    assert residual < 2e-8
    return x, pi, resistance, incidence, residual


def check():
    rng = np.random.default_rng(590526)
    worst_derivative = worst_residual = 0.
    exact_identities = 0
    for trial in range(20):
        graph = subdivided_core('theta' if trial % 2 == 0 else 'k4', rng)
        arcs = list(graph.edges())
        G = Graph(len(graph), [(u, v, 1.) for u, v in arcs])
        laws = rng.integers(0, len(LAWS), len(arcs))
        # Exact physical construction tests non-odd and mixed-degree laws.
        potential = list(map(int, rng.permutation(len(graph))))
        xf, bf = [], []
        for (u, v), law in zip(arcs, laws):
            x = F(int(rng.integers(1, 5)), 2)
            if potential[u] < potential[v]:
                x = -x
            f = LAWS[law][0](x)
            beta = F(potential[u]-potential[v])/f
            assert beta > 0 and beta*f == potential[u]-potential[v]
            xf.append(x)
            bf.append(beta)
        tree, chords = G.spanning_forest()
        for e in chords:
            z = list(map(int, G.cycle_vector(tree, e)))
            assert sum(s*beta*LAWS[law][0](x) for s, beta, law, x in zip(z, bf, laws, xf)) == 0
            exact_identities += 1
        # Independent finite differences of the smoothed physical objective.
        b = rng.uniform(-.7, .7, len(graph))
        b[-1] = -sum(b[:-1])
        beta = rng.uniform(.5, 2., len(arcs))
        x, pi, R, incidence, residual = solve(G, b, laws, beta)
        worst_residual = max(worst_residual, residual)
        a, c = 0, 1
        core, paths = core_paths(graph, a, c)
        internal = sorted(set(graph)-core)
        rhs = np.zeros(len(graph))
        rhs[a], rhs[c] = 1., -1.
        rhs[internal] += .2
        rhs[c] -= .2*len(internal)
        L = (incidence/R)@incidence.T
        keep = [v for v in graph if v != c]
        h = np.zeros(len(graph))
        h[keep] = np.linalg.solve(L[np.ix_(keep, keep)], rhs[keep])
        def objective(load):
            _, p, _, _, _ = solve(G, load, laws, beta)
            return p[a]-p[c]+.2*sum(p[v]-p[c] for v in internal)
        for v in rng.choice(keep, 2, replace=False):
            d = np.zeros(len(graph))
            d[v], d[c] = 1., -1.
            step = 1e-5
            fd = (objective(b+step*d)-objective(b-step*d))/(2*step)
            error = abs(fd-h[v])
            worst_derivative = max(worst_derivative, error)
            assert error < 1e-5, (trial, error)
    print(f'20 heterogeneous-law blocks: {exact_identities} exact rational cycle identities and 40 adjoint derivative checks passed.')
    print(f'Maximum derivative error {worst_derivative:.3g}; physical residual {worst_residual:.3g}.')


if __name__ == '__main__':
    check()
