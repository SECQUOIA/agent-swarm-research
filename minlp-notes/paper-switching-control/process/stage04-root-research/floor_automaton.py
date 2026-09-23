"""Independent exploratory min-switch automaton; not yet a theorem checker."""
from itertools import permutations
from collections import deque, Counter

PERMS=tuple(permutations(range(3)))
INF=10**9

def offset(s,i):
    return tuple(int(j==i) if s==1 else int(j!=i) for j in range(3))

def choices(s):
    for t in (1,2):
        if s==1 and t==2:
            yield t,(0,0,0)
        else:
            for p in range(3):
                yield t,tuple(int(j!=p) if s==2 and t==1 else int(j==p) for j in range(3))

def step(s,cost,t,d):
    result=[INF]*9
    for u in range(3):
        for v in range(3):
            diff=tuple(d[j]+offset(t,v)[j]-offset(s,u)[j] for j in range(3))
            if sorted(diff)!=[0,0,1]:
                continue
            a=diff.index(1)
            result[3*v+a]=min(result[3*v+a],*(cost[3*u+b]+int(a!=b) for b in range(3)))
    minimum=min(result)
    assert minimum<INF
    return tuple(x-minimum if x<INF else INF for x in result),minimum

def canon(cost):
    return min(tuple(cost[3*p[i]+p[j]] for i in range(3) for j in range(3)) for p in PERMS)

def explore(limit=10000, cap=None):
    initial=(1,canon(tuple(0 if i==j else INF for i in range(3) for j in range(3))))
    states=[initial]; lookup={initial:0}; edges=[]
    q=deque([0])
    while q:
        u=q.popleft();s,c=states[u]
        for t,d in choices(s):
            nc,w=step(s,c,t,d)
            if cap is not None: nc=tuple(x if x<=cap else INF for x in nc)
            state=(t,canon(nc))
            if state not in lookup:
                if len(states)>=limit:
                    return states,edges,False
                lookup[state]=len(states);states.append(state);q.append(lookup[state])
            edges.append((u,lookup[state],w))
    return states,edges,True

if __name__=='__main__':
    import sys
    cap=int(sys.argv[1]) if len(sys.argv)>1 else None
    states,edges,closed=explore(cap=cap)
    print('states',len(states),'edges',len(edges),'closed',closed)
    print('max finite costs',max(c for s,row in states for c in row if c<INF))
    print('edge increment counts',Counter(w for u,v,w in edges))
    # Longest path potential with weights 2*increment-1. Positive cycles
    # would disprove a uniform one-unit bound on this normalized excess.
    dist=[-INF]*len(states);dist[0]=0
    for iteration in range(len(states)):
        changed=False
        for u,v,w in edges:
            if dist[u]>-INF and dist[v]<dist[u]+2*w-1:
                dist[v]=dist[u]+2*w-1;changed=True
        if not changed:break
    print('potential iterations',iteration+1,'positive cycle',changed,'maximum excess',max(dist))
    if not changed:
        print('potential distribution',Counter(dist))
