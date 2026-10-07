# Own exact plane enumeration for every stored leaf box (concave envelope facets of F over the box)
import json, itertools
from fractions import Fraction as Fr
b = Fr(69060773480663, 1250000000000)
assert b == Fr('55.2486187845304')
def F(p,q,s): return s - 2*q/b + (q*q+p*p)/(b*b*s)
def solve4(M, rhs):
    # Gaussian elimination, exact
    A=[row[:]+[r] for row,r in zip(M,rhs)]; n=4
    for c in range(n):
        piv=next((i for i in range(c,n) if A[i][c]!=0),None)
        if piv is None: return None
        A[c],A[piv]=A[piv],A[c]
        for i in range(n):
            if i!=c and A[i][c]!=0:
                f=A[i][c]/A[c][c]; A[i]=[a-f*bb for a,bb in zip(A[i],A[c])]
    return tuple(A[i][n]/A[i][i] for i in range(n))
for name in ['powerflow0039p','powerflow0039r']:
    D=json.load(open(f'/tmp/pfcrit/rev/logs/{name}.bb3t.json'))
    for lf in D['leaves']:
        box=[(Fr(a),Fr(c)) for a,c in lf['box']]
        (p1,p2),(q1,q2),(s1,s2)=box
        V=[(p,q,s,F(p,q,s)) for p in (p1,p2) for q in (q1,q2) for s in (s1,s2)]
        H=set()
        for quad in itertools.combinations(V,4):
            sol=solve4([[t[0],t[1],t[2],Fr(1)] for t in quad],[t[3] for t in quad])
            if sol is None: continue
            if all(sol[0]*p+sol[1]*q+sol[2]*s+sol[3]>=f for p,q,s,f in V): H.add(sol)
        touch=[sum(1 for p,q,s,f in V if h[0]*p+h[1]*q+h[2]*s+h[3]==f) for h in H]
        print(name, [[float(a) for a in iv] for iv in box], 'planes', len(H), 'vertices on each plane', sorted(touch))
