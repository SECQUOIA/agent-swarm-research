"""Full-state and threshold diagnostics for globally correlated cactus flow."""
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
from random import Random
import mpmath as mp
import networkx as nx


def mpf(q):
    q = F(q)
    return mp.mpf(q.numerator)/q.denominator


def threshold(n, m, k):
    denominator = 1
    while denominator < 8192*(m+1):
        denominator *= 2
    sqrt2 = F(isqrt(2*denominator**2), denominator)
    sqrt3 = F(isqrt(3*denominator**2), denominator)
    a, b = 2*sqrt2-2, sqrt3/2
    return 4*m-1+n+(m-k+F(1, 2))*a+(k-F(1, 2))*b


def state(n, comparison, theta):
    m = len(comparison)
    edges, beta, flow = [], [], []
    for i in range(n):
        edges.append((-n+i, -n+i+1))
        beta.append(1+theta[i])
        flow.append(mp.mpf(1))
    for cycle, (i, j, sign) in enumerate((i, j, sign) for i, j in comparison for sign in (1, -1)):
        start, internal, end = 3*cycle, 3*cycle+1, 3*cycle+2
        resistance = 2+sign*(theta[i]-theta[j])
        q = 1/(1+mp.sqrt(mpf(resistance)))
        for edge, be, x in [((start, internal), resistance, q),
                            ((internal, end), resistance, q),
                            ((start, end), F(2), 1-q)]:
            edges.append(edge); beta.append(be); flow.append(x)
        if cycle < 2*m-1:
            edges.append((end, 3*(cycle+1))); beta.append(F(2)); flow.append(mp.mpf(1))
    graph = nx.DiGraph(edges)
    assert len(graph) == 6*m+n and len(edges) == 8*m-1+n
    assert nx.is_directed_acyclic_graph(graph)
    assert max(dict(graph.to_undirected().degree()).values()) <= 3
    assert len(nx.cycle_basis(graph.to_undirected())) == 2*m
    assert all(F(1) <= be <= F(3) for be in beta)
    assert min(flow) > 0
    balance = {v: mp.mpf(0) for v in graph}
    for (u, v), x in zip(edges, flow):
        balance[u] += x; balance[v] -= x
    balance[-n] -= 1; balance[6*m-1] += 1
    residual = max(map(abs, balance.values()))
    for cycle in range(2*m):
        i = n+4*cycle
        q = flow[i]
        residual = max(residual, abs(2*mpf(beta[i])*q*q-2*(1-q)**2))
    assert residual < mp.mpf('1e-70')
    return sum(flow), residual


def run():
    mp.mp.dps = 90
    rng = Random(931028)
    all_edges = list(combinations(range(4), 2))
    kappa = mp.sqrt(3)/2-2*mp.sqrt(2)+2
    assert kappa > mp.mpf(1)/32
    states = thresholds = 0
    largest_residual = mp.mpf(0)
    for mask in range(1, 64):
        comparison = [e for i, e in enumerate(all_edges) if mask >> i & 1]
        m, n = len(comparison), 4
        bestcut = max(sum(bits[i] != bits[j] for i, j in comparison) for bits in product((0, 1), repeat=n))
        base = 4*m-1+n+m*(2*mp.sqrt(2)-2)
        optimum = base+kappa*bestcut
        for bits in product((0, 1), repeat=n):
            total, residual = state(n, comparison, list(map(F, bits)))
            cut = sum(bits[i] != bits[j] for i, j in comparison)
            assert abs(total-(base+kappa*cut)) < mp.mpf('1e-70')
            largest_residual = max(largest_residual, residual)
            states += 1
        for _ in range(3):
            theta = [F(rng.randrange(0, 17), 16) for _ in range(n)]
            total, residual = state(n, comparison, theta)
            assert total <= optimum+mp.mpf('1e-70')
            largest_residual = max(largest_residual, residual)
            states += 1
        for k in range(1, m+1):
            tau = threshold(n, m, k)
            midpoint = base+kappa*(k-mp.mpf('0.5'))
            assert abs(mpf(tau)-midpoint) < mp.mpf(1)/512
            assert (optimum-mpf(tau) > mp.mpf(7)/512) if bestcut >= k else (mpf(tau)-optimum > mp.mpf(7)/512)
            assert tau.denominator <= 65536*(m+1)
            assert abs(tau.numerator) < 10**7*(m+n+1)**2
            thresholds += 1
    print(f'PASS: {states} full positive DAG states, {thresholds} rational threshold gaps; '
          f'63 comparison graphs; max residual {mp.nstr(largest_residual, 6)}')


if __name__ == '__main__':
    run()
