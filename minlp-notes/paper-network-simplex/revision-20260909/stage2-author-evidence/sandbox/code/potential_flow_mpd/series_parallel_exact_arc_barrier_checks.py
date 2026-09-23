"""Exact encoders and high-precision complete-state checks for SRS arc probing."""
from fractions import Fraction

import mpmath as mp
import networkx as nx
import numpy as np
import sympy as sp

from square_root_sum_reduction import reduce_srs


def run():
    mp.mp.dps = 90
    rng = np.random.default_rng(592605)
    count = trivial = equality = 0
    worst = mp.mpf(0)
    cases = [([4,9],5), ([4],2), ([0,1],1), ([2],100)]
    cases += [(list(map(int, rng.integers(0,19,int(rng.integers(1,7))))),
               int(rng.integers(0,24))) for _ in range(64)]
    for aa, K in cases:
        inst = reduce_srs(aa,K)
        truth = bool(sum(sp.sqrt(a) for a in aa) <= K)
        if inst.threshold <= 0:
            assert truth
            trivial += 1
            continue
        n = inst.n
        arcs = inst.arcs+[(n,inst.source,Fraction(1)),
                         (inst.sink,n+1,Fraction(1)),
                         (n,n+1,inst.threshold+2)]
        graph = nx.Graph()
        graph.add_edges_from((u,v) for u,v,_ in arcs)
        assert graph.number_of_edges() == len(arcs)
        assert nx.is_biconnected(graph)
        assert max(dict(graph.degree()).values()) <= 3
        assert all(be.denominator == 1 and be > 0 for _,_,be in arcs)
        if inst.radicands:
            unit = []
            for i,a in enumerate(inst.radicands):
                root_a = mp.sqrt(a)
                unit += [1/(root_a+1),root_a/(root_a+1),root_a/(root_a+1)]
                if i:
                    unit.append(mp.mpf(1))
            D = inst.scale*(inst.constant-2*sum(mp.sqrt(a) for a in inst.radicands))
        else:
            unit = [mp.mpf(1)]
            D = mp.mpf(1)
        H = mp.mpf(inst.threshold.numerator)
        x = mp.sqrt(D+2)/(mp.sqrt(D+2)+mp.sqrt(H+2))
        q = 1-x
        flows = [q*f for f in unit]+[q,q,x]
        load = [mp.mpf(0)]*(n+2)
        for (u,v,_),f in zip(arcs,flows):
            load[u] += f
            load[v] -= f
        expected = [mp.mpf(0)]*n+[mp.mpf(1),-mp.mpf(1)]
        assert max(abs(a-b) for a,b in zip(load,expected)) < mp.mpf('1e-75')
        potentials = {n:mp.mpf(0)}
        todo = [n]
        adjacency = [[] for _ in range(n+2)]
        for (u,v,be),f in zip(arcs,flows):
            drop = mp.mpf(be.numerator)*f*abs(f)
            adjacency[u].append((v,-drop))
            adjacency[v].append((u,drop))
        while todo:
            u = todo.pop()
            for v,diff in adjacency[u]:
                value = potentials[u]+diff
                if v in potentials:
                    worst = max(worst,abs(potentials[v]-value))
                else:
                    potentials[v] = value
                    todo.append(v)
        source_equal = sp.simplify(sum(sp.sqrt(a) for a in aa)-K) == 0
        if source_equal:
            assert abs(x-mp.mpf('.5')) < mp.mpf('1e-75')
            equality += 1
        else:
            assert (x>mp.mpf('.5')) == truth
        count += 1
    assert worst < mp.mpf('1e-65')
    print(f'{count} full graph/state/threshold checks, {trivial} nonpositive-threshold preprocess cases, {equality} exact equalities passed.')
    print('Maximum complete-state potential residual:',mp.nstr(worst,8))


if __name__ == '__main__':
    run()
