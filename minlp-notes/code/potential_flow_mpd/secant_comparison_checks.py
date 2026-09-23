"""Finite secant-adjoint identities on SP and non-SP physical networks."""
import networkx as nx
import numpy as np

from series_parallel_envelope_checks import incidence, physical


def run():
    rng = np.random.default_rng(509256)
    count = 0
    worst = 0.
    for trial in range(30):
        G = nx.complete_graph(4) if trial % 2 else nx.complete_bipartite_graph(2,4)
        G.add_edge(0,len(G))
        A, edges = incidence(G)
        n,m = A.shape
        b = rng.uniform(-2,2,n)
        b -= np.mean(b)
        gp,gm,Gp,Gm = rng.uniform(.2,3.,(4,m))
        x = physical(A,b,gp,gm)
        y = physical(A,b,Gp,Gm)
        gx = np.where(x>=0,gp,gm)*x*abs(x)
        Gx = np.where(x>=0,Gp,Gm)*x*abs(x)
        Gy = np.where(y>=0,Gp,Gm)*y*abs(y)
        d = Gx-gx
        r = np.ones(m)
        moving = abs(y-x)>1e-10
        r[moving] = (Gy-Gx)[moving]/(y-x)[moving]
        assert min(r)>0
        L = (A/r)@A.T
        for target,(u,v) in enumerate(edges):
            q = np.zeros(n)
            q[u],q[v] = 1.,-1.
            h = np.zeros(n)
            h[1:] = np.linalg.solve(L[1:,1:],q[1:])
            j = A.T@h/r
            assert -1e-8<=j[target]<=1+1e-8
            predicted = (j@d-d[target])/r[target]
            error = abs(predicted-(y[target]-x[target]))
            assert error < 1e-7, (trial,target,error)
            worst = max(worst,error)
            count += 1
    print(f'{count} finite target-arc secant identities passed on SP and K4 networks.')
    print(f'Max absolute identity discrepancy {worst:.3g}.')


if __name__ == '__main__':
    run()
