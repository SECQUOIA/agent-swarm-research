"""Checks the all-unit objective subdivision of the reviewed theta reduction."""
from fractions import Fraction as F
from itertools import product
import mpmath as mp
import networkx as nx
from weighted_arc_cycle_rank_hardness_checks import solve,mpf


def run():
    mp.mp.dps=90
    count=0
    for items,K in [([1],1),([2,4],3),([1,2,3],3),([2,3,5,7],8),([1,4,6,9,12],15)]:
        n=len(items)
        for bits in product((0,1),repeat=n):
            total=sum(a*z for a,z in zip(items,bits));theta=F(224,81)*(1+F(total,K))
            q,a=solve(theta);graph=nx.DiGraph();graph.add_nodes_from(range(4));nxt=4
            arcs=[];beta=[];flows=[]
            for u,v,res,flow in [(0,2,F(1),a),(2,1,F(1),a+3-q),(3,1,F(2),1-a+q)]:
                arcs.append((u,v));beta.append(res);flows.append(flow)
            path=[0]+list(range(nxt,nxt+9*n))+[3];nxt+=9*n
            for edge in zip(path,path[1:]):arcs.append(edge);beta.append(F(1,9*n+1));flows.append(4-a)
            path=[2]+list(range(nxt,nxt+5*n-1))+[3]
            resistance=[F(28,81*n)]*(4*n)+[F(112,81*n)+F(224*ai*z,81*K) for ai,z in zip(items,bits)]
            for edge,res in zip(zip(path,path[1:]),resistance):arcs.append(edge);beta.append(res);flows.append(q)
            graph.add_edges_from(arcs)
            assert nx.is_directed_acyclic_graph(graph)
            assert len(graph.edges())==14*n+4 and len(graph)==14*n+3
            assert max(dict(graph.to_undirected().degree()).values())==3
            assert sum(resistance)==theta and min(flows)>0
            expected=n*(-9*a+5*q)+36*n+8
            assert abs(sum(flows)-expected)<mp.mpf('1e-76')
            assert all((be*81*n*K*(9*n+1)).denominator==1 for be in beta)
            balance=[mp.mpf(0)]*len(graph)
            for (u,v),flow in zip(arcs,flows):balance[u]+=flow;balance[v]-=flow
            expected_b=[4,-4,3,-3]+[0]*(len(graph)-4)
            assert max(abs(x-y) for x,y in zip(balance,expected_b))<mp.mpf('1e-76')
            count+=1
    print('PASS:',count,'unit-cost DAG scenarios: counts, positivity, balances, objective and integer data')


if __name__=='__main__':run()
