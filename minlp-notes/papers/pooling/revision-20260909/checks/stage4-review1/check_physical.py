from fractions import Fraction as F
from itertools import product
from random import Random
rng=Random(43)
count=0
for n in range(2,8):
    s=[F(1,4**(n-j-1)) for j in range(n)]
    d=[3*t*t for t in s[:-1]]
    vertices=[]
    for bits in product((0,1),repeat=n):
        x=[]
        for b in bits:
            prev=x[-1] if x else F(0)
            x.append(b+(1-2*b)*prev/4)
        vertices.append(x)
    assert len({x[-1] for x in vertices})==2**n
    samples=vertices[:]
    for _ in range(100):
        a,b=rng.sample(vertices,2); w=F(rng.randrange(1,17),17)
        samples.append([(1-w)*u+w*v for u,v in zip(a,b)])
    for x in samples:
        t=[a*b for a,b in zip(s,x)]
        low=x[-1]-x[-1]**2
        for z in (low,(low+1)/2,F(1)):
            # Assemble original source, product, and pool flows.
            supplies={f'i{j}':s[j] for j in range(n)}|{'A':F(1),'B':F(1),'Z':z}
            qualities={f'i{j}':F(n-j-1) for j in range(n)}|{'A':F(1),'B':F(2),'Z':F(0),'P':2-t[-1]}
            arcs={(f'i{j}',f'o{j}'):s[j]-t[j] for j in range(n)}
            arcs.update({(f'i{j}',f'o{j+1}'):t[j] for j in range(n)})
            arcs.update({('A',f'o{n}'):1-t[-1],('A','P'):t[-1],('B','P'):1-t[-1],('B','W'):t[-1],('P','W'):1-t[-1],('P','V'):t[-1],('Z','V'):z})
            assert all(0<=f<=1 for f in arcs.values())
            for u,amount in supplies.items(): assert sum(f for (a,b),f in arcs.items() if a==u)==amount
            assert sum(f for (a,b),f in arcs.items() if b=='P')==1
            assert sum(f for (a,b),f in arcs.items() if a=='P')==1
            assert sum(qualities[a]*f for (a,b),f in arcs.items() if b=='P')==qualities['P']
            caps={f'o0':s[0]}|{f'o{j}':s[j] for j in range(1,n)}|{f'o{n}':F(1),'W':F(1),'V':F(2)}
            bounds={f'o0':F(n-1)}|{f'o{j}':F(2*n-2*j-1,2) for j in range(1,n)}|{f'o{n}':F(1),'W':F(2),'V':F(1)}
            totals={}
            for v,cap in caps.items():
                flow=sum(f for (a,b),f in arcs.items() if b==v)
                mass=sum(qualities[a]*f for (a,b),f in arcs.items() if b==v)
                assert 0<=flow<=cap and mass<=bounds[v]*flow
                totals[v]=flow
            assert totals[f'o{n}']==totals['W']==1
            costs={f'i{j}':s[j] for j in range(n)}|{'A':F(1),'B':F(1),'Z':F(2)}
            revenues={f'o{j}':s[j] for j in range(n)}|{f'o{n}':F(1),'W':F(1),'V':F(1)}
            profit=sum(revenues[v]*amount for v,amount in totals.items())-sum(costs[u]*amount for u,amount in supplies.items())
            assert profit==sum(a*b for a,b in zip(d,x))-z<=0
            certificate=low-sum(a*b for a,b in zip(d,x))
            assert certificate>=0
            assert certificate==sum(F(1,4**(2*(n-j-1)))*(x[j]-(x[j-1]/4 if j else 0))*(1-(x[j-1]/4 if j else 0)-x[j]) for j in range(n))
            count+=1
    delta=F(1,4**n)
    for i,v in enumerate(vertices):
        # The endpoint-bit adjacency agrees with the triangular cube graph.
        for bit in range(n):
            w=vertices[i^(1<<bit)]; gap=w[-1]-v[-1]
            assert -gap*gap+delta*gap<0
print(f'PASS: {count} original physical-flow/economic checks, n=2,...,7; all endpoint-edge derivative checks passed.')
