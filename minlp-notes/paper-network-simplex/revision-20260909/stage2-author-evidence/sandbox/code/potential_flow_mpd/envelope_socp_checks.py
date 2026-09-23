"""Solve the explicit cubic SOC lift and compare with physical circulation roots.

Uses CVXPY/Clarabel only for numerical validation; the theorem's bit guarantee
comes from its separate rational-oracle proof.
"""
import cvxpy as cp
import networkx as nx
import numpy as np

from series_parallel_envelope_checks import incidence, physical


def conic_flow(A,b,positive,negative):
    m=A.shape[1]
    p,n=cp.Variable(m,nonneg=True),cp.Variable(m,nonneg=True)
    up,un=cp.Variable(m,nonneg=True),cp.Variable(m,nonneg=True)
    wp,wn=cp.Variable(m,nonneg=True),cp.Variable(m,nonneg=True)
    constraints=[A@(p-n)==b]
    for z,w,u in [(p,wp,up),(n,wn,un)]:
        for e in range(m):
            constraints += [cp.SOC(w[e]+1,cp.hstack([2*z[e],w[e]-1])),
                            cp.SOC(u[e]+z[e],cp.hstack([2*w[e],u[e]-z[e]]))]
    problem=cp.Problem(cp.Minimize((positive@up+negative@un)/3),constraints)
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,
                  tol_feas=1e-10,max_iter=300)
    assert problem.status in [cp.OPTIMAL,cp.OPTIMAL_INACCURATE],problem.status
    x=p.value-n.value
    return x,float(problem.value),float(max(abs(A@x-b))),problem.status


def run():
    rng=np.random.default_rng(5092523)
    worst_flow=worst_balance=worst_value=0.
    count=inaccurate=0
    for k in [3,5,9,15]:
        graph=nx.complete_bipartite_graph(2,k)
        A,edges=incidence(graph)
        b=rng.uniform(-1,1,len(graph))
        b-=np.mean(b)
        m=len(edges)
        lower=rng.uniform(.5,1,m)
        upper=lower+rng.uniform(.1,1,m)
        target=k % m
        u,v=edges[target]
        q=np.zeros(len(graph))
        q[u],q[v]=1.,-1.
        h=np.zeros(len(graph))
        h[1:]=np.linalg.solve((A@A.T)[1:,1:],q[1:])
        signs=np.sign(A.T@h)
        for direction in [-1,1]:
            status=direction*signs
            status[target]=-direction
            positive=np.where(status>0,upper,lower)
            negative=np.where(status<0,upper,lower)
            exact=physical(A,b,positive,negative)
            computed,value,balance,status=conic_flow(A,b,positive,negative)
            inaccurate += status==cp.OPTIMAL_INACCURATE
            expected=np.sum(np.where(exact>=0,positive,negative)*abs(exact)**3)/3
            error=max(abs(computed-exact))
            assert error<1e-4,(k,direction,error)
            assert balance<1e-7
            assert abs(value-expected)<1e-7
            worst_flow=max(worst_flow,error)
            worst_balance=max(worst_balance,balance)
            worst_value=max(worst_value,abs(value-expected))
            count+=1
    print(f'{count} explicit cubic SOCPs checked on block ranks2,4,8,14; {inaccurate} reported optimal_inaccurate.')
    print(f'Max flow discrepancy {worst_flow:.3g}; balance residual {worst_balance:.3g}; energy discrepancy {worst_value:.3g}.')


if __name__=='__main__':
    run()
