"""Exact gadget identities and exhaustive tiny Subset-Sum reductions."""
from fractions import Fraction as F
from itertools import product

import mpmath as mp
import networkx as nx
import numpy as np
import sympy as sp


def topology(n):
    G = nx.Graph()
    G.add_edges_from([(0, 2), (2, 1), (0, 3), (3, 1), (4, 1)])
    path = [2]+list(range(5, 5+n-1))+[3]
    G.add_edges_from(zip(path, path[1:]))
    assert max(dict(G.degree()).values()) == 3
    ranks = sorted(G.subgraph(block).number_of_edges()-len(block)+1
                   for block in nx.biconnected_components(G))
    assert ranks == [0, 2]


def run():
    q, tau = sp.symbols('q tau')
    x, y = (q+1)/2, (7-q)/2
    assert sp.expand(x+y-4) == 0
    assert sp.expand(y+q-x-3) == 0
    span = x*x/2+y*y/6
    assert sp.expand(span-2-(q-1)**2/6) == 0
    cycle = sp.expand(y*y/6-x*x/2-tau*q*q)
    assert sp.expand(12*cycle+((12*tau+1)*q*q+10*q-23)) == 0
    assert sp.expand(3-span-(1-(q-1)**2/6)) == 0
    mp.mp.dps = 80
    rng = np.random.default_rng(590530)
    yes = no = scenarios = 0
    min_gap_ratio = mp.inf
    for trial in range(48):
        n = int(rng.integers(2, 8))
        a = list(map(int, rng.integers(1, 25, n)))
        S = sum(a)
        K = int(rng.integers(1, S+1))
        topology(n)
        Delta = mp.mpf(6)/(31*K+18*S)**2
        best = -mp.inf
        feasible = False
        for sigma in product([0, 1], repeat=n):
            subtotal = sum(ai*si for ai, si in zip(a, sigma))
            feasible |= subtotal == K
            beta = [F(1, 2*n)+F(ai*si, 2*K) for ai, si in zip(a, sigma)]
            tf = sum(beta)
            assert tf == F(1, 2)+F(subtotal, 2*K)
            assert [6*n*K*bi for bi in beta] == [3*K+3*n*ai*si for ai, si in zip(a, sigma)]
            t = mp.mpf(tf.numerator)/tf.denominator
            root = 46/(10+mp.sqrt(192+1104*t))
            assert 0 < root < 2
            assert abs((12*t+1)*root*root+10*root-23) < mp.mpf('1e-70')
            score = 1-(root-1)**2/6
            best = max(best, score)
            if subtotal != K:
                assert 1-score >= Delta-mp.mpf('1e-70')
                min_gap_ratio = min(min_gap_ratio, (1-score)/Delta)
            scenarios += 1
        if feasible:
            yes += 1
            assert abs(best-1) < mp.mpf('1e-70')
        else:
            no += 1
            assert best <= 1-Delta+mp.mpf('1e-70')
    assert yes > 0 and no > 0
    print(f'Exact symbolic balances/laws/objective passed; {scenarios} scenarios across {yes} yes and {no} no instances checked.')
    print(f'All graphs degree3 with block ranks[0,2]; integer scaling exact; minimum observed gap/bound ratio {float(min_gap_ratio):.3g}.')


if __name__ == '__main__':
    run()
