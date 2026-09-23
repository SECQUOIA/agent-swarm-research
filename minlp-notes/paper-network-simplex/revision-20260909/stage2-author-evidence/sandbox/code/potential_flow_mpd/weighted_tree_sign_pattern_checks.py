"""Checks for the cut-direction parameter strengthening of the tree theorem."""
import networkx as nx
import numpy as np
from fixed_support_weighted_tree_checks import tree_check


def marked_by_direction(graph,c):
    directed=nx.DiGraph();directed.add_nodes_from(graph)
    for u,v in graph.edges():
        cut=graph.copy();cut.remove_edge(u,v)
        weight=sum(c[t] for t in nx.node_connected_component(cut,u))
        assert weight!=0
        directed.add_edge(u,v) if weight>0 else directed.add_edge(v,u)
    return {v for v in graph if (directed.in_degree(v),directed.out_degree(v))!=(1,1)}


def run():
    graph=nx.path_graph(5)
    checks=[([2,-1,2,-1,-2],2),([2,-1,-3,1,1],3)]
    count=0
    for coeff,expected in checks:
        c=np.array(coeff,dtype=float);marked=marked_by_direction(graph,c)
        assert len(marked)==expected
        candidates,best=tree_check(graph,c,np.array([-1,-1,-1,-1,-2.]),
                                  np.array([2,2,2,2,1.]),np.ones(4),np.array([2,3,4,5.]),marked=marked)
        count+=candidates
        print('support',np.count_nonzero(c),'marks',len(marked),'candidates',candidates,'optimum',best)
    # Exhaustive small integer path coefficients: marks = sign changes + 2.
    from itertools import product
    patterns=0
    for partial in product((-2,-1,1,2),repeat=4):
        coeff=list(partial)+[-sum(partial)]
        cumulative=np.cumsum(coeff)[:-1]
        if any(cumulative==0):continue
        marked=marked_by_direction(graph,coeff)
        flips=sum(a*b<0 for a,b in zip(cumulative,cumulative[1:]))
        assert len(marked)==flips+2
        assert len(marked)<=2*np.count_nonzero(coeff)-2
        patterns+=1
    print('PASS:',count,'stationary candidates;',patterns,'exact cut-direction counts')


if __name__=='__main__':run()
