"""Adjoint/threshold checks for fixed global rank and weighted objective support."""
import networkx as nx
import numpy as np
from block_rank_checks import path_patterns, solve_smoothed


def paths_of(graph, c):
    marked={v for v in graph if c[v] != 0 or graph.degree(v)>=3}
    seen=set(); paths=[]
    for start in sorted(marked):
        for nxt in graph[start]:
            edge=frozenset((start,nxt))
            if edge in seen: continue
            path=[start,nxt];seen.add(edge)
            while path[-1] not in marked:
                nxt=next(v for v in graph[path[-1]] if v!=path[-2])
                seen.add(frozenset((path[-1],nxt)));path.append(nxt)
            paths.append(path)
    assert len(seen)==len(graph.edges())
    return marked,paths


def example(kind,rng):
    if kind==0:
        original=nx.cycle_graph(7); coefficients={0:2,2:-5,5:3}
    elif kind==1:
        original=nx.disjoint_union(nx.cycle_graph(5),nx.cycle_graph(5))
        original.add_edge(2,5);coefficients={0:1,7:-3,9:2}
    else:
        original=nx.cycle_graph(6)
        original.add_edges_from([(0,6),(6,7),(7,8)])
        coefficients={6:2,8:-2}
    graph=nx.Graph();graph.add_nodes_from(original)
    nxt=len(original)
    for u,v in original.edges():
        count=int(rng.integers(1,3))
        path=[u]+list(range(nxt,nxt+count))+[v];nxt+=count
        for a,b in zip(path,path[1:]): graph.add_edge(a,b,beta=float(rng.uniform(.5,2)))
    c=np.zeros(len(graph))
    for v,value in coefficients.items(): c[v]=value
    return graph,c


def run():
    rng=np.random.default_rng(371690)
    worst_current=worst_gradient=worst_residual=0.
    path_count=level_count=loop_count=derivatives=0
    for trial in range(12):
        graph,c=example(trial%3,rng)
        rank=len(graph.edges())-len(graph)+1;p=np.count_nonzero(c)
        marked,paths=paths_of(graph,c)
        assert len(marked)<=2*rank+2*p-2
        assert len(paths)==len(marked)+rank-1<=3*rank+2*p-3
        assert len(marked)+2*len(paths)<=8*rank+6*p-8
        internal=sorted(set(graph)-marked);ref=min(marked)
        b=rng.uniform(-.8,.8,len(graph));b[ref]=-sum(np.delete(b,ref))
        rho,delta=.2,.3
        x,pi,A,beta,arcs,residual=solve_smoothed(graph,b,rho)
        worst_residual=max(worst_residual,residual)
        resistance=beta*(2*abs(x)+rho)
        L=(A/resistance)@A.T
        source=c.copy();source[internal]+=delta;source[ref]-=delta*len(internal)
        keep=[v for v in graph if v!=ref]
        h=np.zeros(len(graph));h[keep]=np.linalg.solve(L[np.ix_(keep,keep)],source[keep])
        resmap={frozenset((u,v)):R for (u,v,_),R in zip(arcs,resistance)}
        for path in paths:
            path_count+=1;loop_count+=path[0]==path[-1]
            current=np.array([(h[u]-h[v])/resmap[frozenset((u,v))] for u,v in zip(path,path[1:])])
            if len(current)>1:
                error=max(abs(np.diff(current)-delta));worst_current=max(worst_current,error)
                assert error<1e-8
            values=h[path[1:-1]];patterns=path_patterns(len(values))
            levels=list(values)+[min(h)-1,max(h)+1]+list(rng.uniform(min(h),max(h),4))
            for level in levels:
                pattern=tuple('free' if abs(v-level)<1e-8 else 'upper' if v>level else 'lower' for v in values)
                assert pattern.count('free')<=2 and pattern in patterns
                level_count+=1
        def objective(load):
            _,potential,*_=solve_smoothed(graph,load,rho)
            return c@potential+delta*sum(potential[v]-potential[ref] for v in internal)
        for v in rng.choice(keep,3,replace=False):
            direction=np.zeros(len(graph));direction[v]=1;direction[ref]=-1
            step=1e-5
            fd=(objective(b+step*direction)-objective(b-step*direction))/(2*step)
            error=abs(fd-h[v]);worst_gradient=max(worst_gradient,error)
            assert error<3e-5
            derivatives+=1
    assert loop_count>0
    print('PASS: 12 graphs;',path_count,'paths;',loop_count,'returning paths;',level_count,'threshold levels;',derivatives,'balanced gradient checks')
    print('Max current error',worst_current,'gradient error',worst_gradient,'physical residual',worst_residual)


if __name__=='__main__': run()
