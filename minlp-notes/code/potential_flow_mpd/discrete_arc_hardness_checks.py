"""Coupled physical-state checks for the discrete arc-capacity reduction."""
from fractions import Fraction as F
from itertools import product

import mpmath as mp
import networkx as nx
import numpy as np
import sympy as sp


def real(x):
    return mp.mpf(x.numerator)/x.denominator


def run():
    q, t = sp.symbols('q t')
    x, y, z = (1+t+q)/2, (7+t-q)/2, 1-t
    for identity in [x+y-t-4, -x-y-z+5, y+q-x-3, x-y-q+3, z+t-1]:
        assert sp.expand(identity) == 0
    mp.mp.dps = 90
    rng = np.random.default_rng(590531)
    scenarios = targets = 0
    max_loss_ratio = mp.mpf(0)
    min_gap_ratio = mp.inf
    for trial in range(18):
        n = int(rng.integers(2, 6))
        a = list(map(int, rng.integers(1, 16, n)))
        K = int(rng.integers(1, sum(a)+1))
        A = 31*K+18*sum(a)
        Delta = F(6, A*A)
        D = (10000*Delta.denominator+Delta.numerator-1)//Delta.numerator
        H = 1-Delta/2
        M = H*D*D
        scale = 6*n*K*A*A
        assert (M*scale).denominator == 1
        G = nx.Graph()
        G.add_edges_from([(0, 2), (2, 1), (0, 3), (3, 1), (4, 1), (4, 0)])
        path = [2]+list(range(5, 5+n-1))+[3]
        G.add_edges_from(zip(path, path[1:]))
        assert nx.is_biconnected(G)
        assert G.number_of_edges()-len(G)+1 == 3
        assert max(dict(G.degree()).values()) == 3
        for sigma in product([0, 1], repeat=n):
            subtotal = sum(ai*si for ai, si in zip(a, sigma))
            tau = real(F(1, 2)+F(subtotal, 2*K))
            q0 = 46/(10+mp.sqrt(192+1104*tau))
            F0 = 1-(q0-1)**2/6
            def equations(qv, v):
                tv = v/D
                xv, yv = (1+tv+qv)/2, (7+tv-qv)/2
                span = xv*xv/2+yv*yv/6
                cross = yv*yv/6-xv*xv/2-tau*qv*qv
                drop = 3*(1-tv)**2-span
                return cross, drop-real(H)*v*v
            qr, vr = mp.findroot(equations, (q0, mp.sqrt(F0/real(H))), tol=mp.mpf('1e-78'))
            assert max(map(abs, equations(qr, vr))) < mp.mpf('1e-72')
            tr = vr/D
            drop = real(H)*vr*vr
            assert 0 < tr < 2/mp.mpf(D)
            loss = F0-drop
            assert -mp.mpf('1e-70') < loss < real(Delta)/8
            max_loss_ratio = max(max_loss_ratio, loss/real(Delta))
            if subtotal == K:
                targets += 1
                assert vr > 1
            else:
                assert vr < 1
            gap_ratio = abs(vr-1)/(3*real(Delta)/32)
            assert gap_ratio > 1
            min_gap_ratio = min(min_gap_ratio, gap_ratio)
            scenarios += 1
    assert targets > 0
    print(f'5 exact symbolic balances and {scenarios} coupled physical scenarios passed; {targets} target subsets.')
    print('All graphs are simple biconnected, degree3, rank3; integer scaling exact.')
    print(f'Max pressure loss/Delta {float(max_loss_ratio):.3g}; min flow gap/bound ratio {float(min_gap_ratio):.3g}.')


if __name__ == '__main__':
    run()
