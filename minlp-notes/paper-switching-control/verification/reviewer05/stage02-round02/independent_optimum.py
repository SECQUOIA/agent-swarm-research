"""Exact independent LP minimization over all words and affine switching cells.

Only the input knots are transcribed. No reach estimate or manuscript checker
is imported. Every bounded switching cell admits its minimum at a vertex of
the epigraph polyhedron, so all triples of tight constraints are enumerated.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import lcm

raw=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[(F(row[0],146),tuple(F(a,146) for a in row[1:])) for row in raw]
L=F(57,8); last,mass=knots[-1]
terminal=tuple(m+(L-last)/3 for m in mass)
knots.append((L,terminal)); seg=[]
for (lo,a),(hi,b) in zip(knots,knots[1:]):
    slopes=tuple((v-u)/(hi-lo) for u,v in zip(a,b)); intercepts=tuple(u-s*lo for u,s in zip(a,slopes))
    seg.append((lo,hi,slopes,intercepts))
def integer_row(values):
    values=list(map(F,values)); d=lcm(*(v.denominator for v in values))
    return tuple(int(v*d) for v in values)
def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def best_vertex(rows):
    best=None
    for a,b,c in combinations(rows,3):
        den=det(a,b,c)
        if den==0: continue
        nu=det((a[3],a[1],a[2]),(b[3],b[1],b[2]),(c[3],c[1],c[2]))
        nv=det((a[0],a[3],a[2]),(b[0],b[3],b[2]),(c[0],c[3],c[2]))
        ne=det((a[0],a[1],a[3]),(b[0],b[1],b[3]),(c[0],c[1],c[3]))
        if den<0: den,nu,nv,ne=-den,-nu,-nv,-ne
        if best is not None and ne*best[3]>=best[2]*den: continue
        if all(A*nu+B*nv+C*ne<=d*den for A,B,C,d in rows):
            best=(nu,nv,ne,den)
    return None if best is None else tuple(F(v,best[3]) for v in best[:3])
# Exercise a degenerate fixed point in the switching coordinates.
assert best_vertex([integer_row(r) for r in [(1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),(0,0,-1,-2)]])==(0,0,2)
byword={};cells=0
for p,q,r in product(range(3),repeat=3):
    best=None
    for j,(ulo,uhi,mu,cu) in enumerate(seg):
        for vlo,vhi,mv,cv in seg[j:]:
            rows=[(-1,0,0,-ulo),(1,0,0,uhi),(0,-1,0,-vlo),(0,1,0,vhi),(1,-1,0,0),(0,0,-1,0),
                  (1-mu[p],0,-1,cu[p]),(int(p==q)-1,1-mv[q],-1,cv[q]),
                  (int(p==r)-int(q==r),int(q==r)-1,-1,terminal[r]-L)]
            sol=best_vertex(list(map(integer_row,rows)))
            assert sol is not None
            if best is None or sol[2]<best[2]:best=sol
            cells+=1
    byword[p,q,r]=best
assert min(sol[2] for sol in byword.values())==F(18673,18396)
assert byword[0,2,1]==(F(8341,4599),F(17639,4599),F(18673,18396))
assert all(sol[2]>F(18673,18396) for word,sol in byword.items() if len(set(word))<3)
for word,sol in byword.items():print(word,'switches and exact optimum:',*[str(x) for x in sol])
print('PASS exact optimization:',cells,'affine switching cells; all 27 words; global optimum',F(18673,18396))
print('PASS repeated-word strict exclusion at optimum; scaled minimax lower coefficient',F(18673,18396)/L)
