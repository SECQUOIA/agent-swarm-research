"""Exact and high-precision controls for the finite-resistance inverse boundary."""
from itertools import product
import mpmath as mp
import networkx as nx
import numpy as np


def run():
    mp.mp.dps=80;rng=np.random.default_rng(240197)
    cases=[([1,1],1),([2,2],1),([2,4],3),([1,2,3],3)]
    cases += [(list(map(int,rng.integers(1,12,int(rng.integers(2,8))))),int(rng.integers(1,30))) for _ in range(30)]
    checked=target=interval_false_positive=0
    for aa,K in cases:
        n=len(aa);S=sum(aa);D=n+K;M=n+S+K
        graph=nx.DiGraph();graph.add_edges_from(zip(range(n),range(1,n+1)));graph.add_edge(0,n)
        assert nx.is_directed_acyclic_graph(graph)
        assert len(graph)==len(graph.edges())==n+1
        assert all(degree==2 for _,degree in graph.to_undirected().degree())
        target_balance=[0]*(n+1)
        for u,v in graph.edges():target_balance[u]+=1;target_balance[v]-=1
        assert target_balance==[2]+[0]*(n-1)+[-2]
        attainable=False
        for bits in product((0,1),repeat=n):
            theta=n+sum(a*z for a,z in zip(aa,bits));exact=theta==D
            p=2*mp.sqrt(D)/(mp.sqrt(theta)+mp.sqrt(D));z=2-p
            assert p>0 and z>0
            assert abs(theta*p*p-D*z*z)<mp.mpf('1e-74')
            assert abs(abs(p-1)-abs(D-theta)/(mp.sqrt(D)+mp.sqrt(theta))**2)<mp.mpf('1e-74')
            if exact:
                attainable=True;target+=1;assert abs(p-1)<mp.mpf('1e-74')
            else:
                assert abs(p-1)>=mp.mpf(1)/(4*M)
                assert max(p,z)>1+mp.mpf(1)/(4*M)
            assert exact==(sum(a*bit for a,bit in zip(aa,bits))==K)
            checked+=1
        interval_feasible=0<=K<=S
        if interval_feasible and not attainable:interval_false_positive+=1
    assert interval_false_positive>0
    print('PASS:',checked,'scenarios;',target,'exact target choices;',interval_false_positive,'interval-feasible finite-infeasible controls')


if __name__=='__main__':run()
