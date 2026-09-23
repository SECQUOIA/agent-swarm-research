"""Adjacent-terminal adjoints and target-edge parameter sensitivity checks."""
import networkx as nx
import numpy as np

from block_rank_checks import solve_smoothed


def adjoint(A, R, source, sink):
    q = np.zeros(A.shape[0])
    q[source], q[sink] = 1., -1.
    L = (A/R)@A.T
    h = np.zeros(A.shape[0])
    h[1:] = np.linalg.solve(L[1:, 1:], q[1:])
    return A.T@h/R


def run():
    rng = np.random.default_rng(590532)
    sign_comparisons = derivative_checks = 0
    max_error = 0.
    for trial in range(18):
        # K2,k is series-parallel; k=4 already has block cycle rank three.
        k = 3+trial%2
        G = nx.complete_bipartite_graph(2, k)
        G.add_edge(0, k+2)  # a zero-adjoint dangling branch for most targets
        for u, v in G.edges:
            G[u][v]['beta'] = float(rng.uniform(.4, 2.))
        b = rng.uniform(-1.5, 1.5, len(G))
        b[-1] = -sum(b[:-1])
        x, pi, A, beta, arcs, _ = solve_smoothed(G, b, .03)
        target = int(rng.integers(len(arcs)))
        source, sink, _ = arcs[target]
        base_sign = None
        for _ in range(16):
            R = rng.lognormal(0, 1.8, len(arcs))
            j = adjoint(A, R, source, sink)
            sign = np.where(abs(j) < 1e-9, 0, np.sign(j)).astype(int)
            if base_sign is None:
                base_sign = sign
            else:
                assert np.all(sign == base_sign), (arcs, target, sign, base_sign)
                sign_comparisons += len(arcs)
        R = beta*(2*abs(x)+.03)
        j = adjoint(A, R, source, sink)
        f = x*abs(x)+.03*x
        assert -1e-10 <= j[target] <= 1+1e-10
        for edge in set([target]+list(map(int, rng.choice(len(arcs), 3, replace=False)))):
            u, v, old = arcs[edge]
            step = 1e-5
            G[u][v]['beta'] = old+step
            xp = solve_smoothed(G, b, .03)[0][target]
            G[u][v]['beta'] = old-step
            xm = solve_smoothed(G, b, .03)[0][target]
            G[u][v]['beta'] = old
            predicted = (j[edge]-(edge == target))*f[edge]/R[target]
            error = abs((xp-xm)/(2*step)-predicted)
            assert error < 2e-6, (trial, target, edge, error)
            max_error = max(max_error, error)
            derivative_checks += 1
    print(f'{sign_comparisons} adjacent-adjoint sign comparisons and {derivative_checks} arc-flow parameter derivatives passed.')
    print(f'Max derivative error {max_error:.3g}; all own-edge factor checks passed.')


if __name__ == '__main__':
    run()
