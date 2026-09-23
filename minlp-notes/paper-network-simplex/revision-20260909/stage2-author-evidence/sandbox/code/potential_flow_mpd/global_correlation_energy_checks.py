"""Paired-bridge energy and pressure checks for correlated cactus design."""
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
from random import Random
import mpmath as mp
import networkx as nx


def mpf(x):
    x = F(x)
    return mp.mpf(x.numerator)/x.denominator


def run():
    mp.mp.dps = 90
    rng = Random(223744)
    ae, be = 24-16*mp.sqrt(2), mp.mpf(13)/2-3*mp.sqrt(3)
    gap = ae-be
    assert gap > mp.mpf(1)/20
    states = thresholds = 0
    residual = mp.mpf(0)
    for mask in range(1, 64):
        n = 4
        comparisons = [e for i, e in enumerate(combinations(range(n), 2)) if mask >> i & 1]
        m = len(comparisons)
        graph = nx.DiGraph()
        graph.add_edges_from((i, i+1) for i in range(-2*n, 0))
        for cycle in range(2*m):
            start, middle, end = 3*cycle, 3*cycle+1, 3*cycle+2
            graph.add_edges_from([(start, middle), (middle, end), (start, end)])
            if cycle < 2*m-1:
                graph.add_edge(end, 3*(cycle+1))
        assert len(graph) == 6*m+2*n and graph.number_of_edges() == 8*m-1+2*n
        assert nx.is_directed_acyclic_graph(graph)
        assert max(dict(graph.to_undirected().degree()).values()) <= 3
        bestcut = max(sum(bits[i] != bits[j] for i, j in comparisons) for bits in product((0, 1), repeat=n))
        base = 3*n+4*m-2+m*ae
        optimum = base-gap*bestcut
        profiles = [tuple(map(F, bits)) for bits in product((0, 1), repeat=n)]
        profiles += [tuple(F(rng.randrange(17), 16) for _ in range(n)) for _ in range(3)]
        for theta in profiles:
            prefix = sum((1+t)+(2-t) for t in theta)
            assert prefix == 3*n
            energy = pressure = mpf(prefix)+4*m-2
            for i, j in comparisons:
                for sign in (1, -1):
                    resistance = 2+sign*(theta[i]-theta[j])
                    assert 1 <= resistance <= 3
                    q = 1/(1+mp.sqrt(mpf(resistance)))
                    dissipated = 2*mpf(resistance)*q**3+2*(1-q)**3
                    drop = 2*mpf(resistance)*q**2
                    residual = max(residual, abs(dissipated-drop))
                    energy += dissipated
                    pressure += drop
            assert abs(energy-pressure) < mp.mpf('1e-70')
            assert energy >= optimum-mp.mpf('1e-70')
            if all(t in (0, 1) for t in theta):
                cut = sum(theta[i] != theta[j] for i, j in comparisons)
                assert abs(energy-(base-gap*cut)) < mp.mpf('1e-70')
            states += 1
        denominator = 1
        while denominator < 65536*(m+1):
            denominator *= 2
        sqrt2 = F(isqrt(2*denominator**2), denominator)
        sqrt3 = F(isqrt(3*denominator**2), denominator)
        ar, br = 24-16*sqrt2, F(13, 2)-3*sqrt3
        for k in range(1, m+1):
            tau = 3*n+4*m-2+(m-k+F(1, 2))*ar+(k-F(1, 2))*br
            exact_midpoint = base-gap*(k-mp.mpf('0.5'))
            assert abs(mpf(tau)-exact_midpoint) < mp.mpf(1)/512
            if bestcut >= k:
                assert mpf(tau)-optimum > mp.mpf(7)/512
            else:
                assert optimum-mpf(tau) > mp.mpf(7)/512
            assert tau.denominator <= 524288*(m+1)
            thresholds += 1
    print(f'PASS: {states} energy/pressure scenarios, {thresholds} rational threshold gaps; '
          f'63 actual paired-bridge cactus graphs; max local identity residual {mp.nstr(residual, 6)}')


if __name__ == '__main__':
    run()
