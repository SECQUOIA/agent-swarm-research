"""Exact rational controls for the bounded-data Max-Cut flow embedding."""
from fractions import Fraction as F
from itertools import combinations,product
import networkx as nx


def run():
    n=4;pairs=list(combinations(range(n),2));count=0
    graph=nx.DiGraph()
    for i in range(n):
        s,t,w=3*i,3*i+1,3*i+2
        graph.add_edges_from([(s,t),(s,w),(w,t)])
        if i<n-1:graph.add_edge(t,3*(i+1))
    assert len(graph)==3*n and len(graph.edges())==4*n-1
    assert max(dict(graph.to_undirected().degree()).values())==3 and nx.is_directed_acyclic_graph(graph)
    for mask in product((0,1),repeat=len(pairs)):
        edges=[e for e,bit in zip(pairs,mask) if bit]
        maxcut=max(sum(bits[i]!=bits[j] for i,j in edges) for bits in product((0,1),repeat=n))
        for z in product((F(0),F(1,2),F(1)),repeat=n):
            x=[(v+1)/3 for v in z];beta=[4*(1-v)**2/v**2 for v in x]
            assert all(1<=be<=16 for be in beta)
            assert all(be*v*v==4*(1-v)**2 for be,v in zip(beta,x))
            value=9*sum((x[i]-x[j])**2 for i,j in edges)
            assert value==sum((z[i]-z[j])**2 for i,j in edges) and value<=maxcut
            if all(v in (0,1) for v in z):assert value.denominator==1
            count+=1
    print('PASS:',count,'exact grid states across64 cut graphs; bounded-beta cube and integer endpoint values')


if __name__=='__main__':run()
