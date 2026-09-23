from fractions import Fraction
from itertools import product, combinations
from math import sqrt
import numpy as np
from scipy.optimize import linprog

n=4
edges=list(combinations(range(n),2))
signs=list(product((-1,1),repeat=n))
vertices=np.array(list(product((0,1),repeat=n)),dtype=float)
Aeq=np.vstack((np.ones(len(vertices)),vertices.T))
exact=lpchecks=0
for coeff in product((-1,0,1),repeat=len(edges)):
    active=[(i,j,a) for (i,j),a in zip(edges,coeff) if a]
    worst=Fraction(0)
    rho=Fraction(0)
    for mask in range(1<<n):
        sub=[(i,j,a) for i,j,a in active if (mask>>i)&1 and (mask>>j)&1]
        L=len(sub)
        if mask: rho=max(rho,Fraction(L,mask.bit_count()))
        if not L: continue
        vals=[sum(a*s[i]*s[j] for i,j,a in sub) for s in signs]
        R=Fraction(max(vals)-min(vals),2)
        polar=max(sum(a*s[i]*s[j] for i,j,a in sub if ((cut>>i)&1)!=((cut>>j)&1)) for cut in range(1<<n) for s in signs)
        assert polar==R
        worst=max(worst,Fraction(L,R))
        degree=max(sum(i==v or j==v for i,j,a in sub) for v in range(n))
        assert L*L<=4*degree*R*R
        exact+=1
    if active:
        assert worst*worst<=16*rho
        # Equality needs both the positive edges and negative edges to be cuts.
        poscut=any(all((s[i]!=s[j])==(a>0) for i,j,a in active) for s in signs)
        negcut=any(all((s[i]!=s[j])==(a<0) for i,j,a in active) for s in signs)
        assert (worst==1)==(poscut and negcut)
    # Non-half-integral and boundary means test the cell extension independently.
    if sum(abs(a) for a in coeff)%3==0:
        fv=np.array([sum(a*v[i]*v[j] for i,j,a in active) for v in vertices])
        for x in [(0,.2,.7,1),(.1,.3,.6,.8),(.5,.5,.5,.5)]:
            beq=np.r_[1,x]
            lo=linprog(fv,A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs')
            hi=linprog(-fv,A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs')
            assert lo.success and hi.success
            H=-hi.fun-lo.fun
            T=sum(abs(a)*min(x[i],x[j],1-x[i],1-x[j]) for i,j,a in active)
            assert T<=float(worst)*H+1e-8
            lpchecks+=1
print(f'PASS: {3**len(edges)} signed/zero coefficient vectors; {exact} exact nonempty induced cut checks; {lpchecks} numerical vertex-LP gap checks.')
