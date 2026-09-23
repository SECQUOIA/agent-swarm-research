"""Independent finite falsification checks; LP and radical comparisons are numerical."""
from itertools import product, combinations
from fractions import Fraction
import json
import numpy as np
from scipy.optimize import linprog

n=4
edges=list(combinations(range(n),2))
signs=np.array(list(product([-1,1],repeat=n)),dtype=int)
verts=(signs+1)//2
chars=np.array([signs[:,i]*signs[:,j] for i,j in edges]).T
monos=np.array([verts[:,i]*verts[:,j] for i,j in edges]).T
masks=np.array(list(product([False,True],repeat=n)))
edge_masks=np.array([[w[i] and w[j] for i,j in edges] for w in masks])
eq=np.vstack([np.ones(2**n),verts.T])

def gaps(a,x):
    values=monos@a
    lo=linprog(values,A_eq=eq,b_eq=np.r_[1,x],bounds=(0,None),method='highs')
    hi=linprog(-values,A_eq=eq,b_eq=np.r_[1,x],bounds=(0,None),method='highs')
    assert lo.success and hi.success
    hull=-hi.fun-lo.fun
    term=sum(abs(a[k])*min(x[i],x[j],1-x[i],1-x[j]) for k,(i,j) in enumerate(edges))
    return term,hull

cases=0
for aa in product([-1,0,1],repeat=len(edges)):
    a=np.array(aa,dtype=int)
    A=np.zeros((n,n),dtype=int)
    for k,(i,j) in enumerate(edges): A[i,j]=A[j,i]=a[k]
    vals=chars@a
    assert (int(vals.max())-int(vals.min()))%2==0
    R=(int(vals.max())-int(vals.min()))//2
    # Exact integer polarization verification, enumerating every partition and sign pair.
    polarized=0
    for w in masks:
        block=A*np.outer(w,~w)
        polarized=max(polarized,int((signs@block@signs.T).max()))
    assert R==polarized
    L=int(abs(a).sum())
    rho=max((Fraction(int(np.count_nonzero(a*w)),int(mask.sum())) for w,mask in zip(edge_masks,masks) if mask.any()),default=Fraction(0))
    deg=max(np.count_nonzero(A,axis=1))
    # Squared forms make these two finite parameter checks exact rational/integer.
    assert L*L<=16*rho*R*R
    assert L*L<=4*int(deg)*R*R
    assert R+1e-12>=np.linalg.norm(A,axis=1).sum()/4
    cases+=1

rng=np.random.default_rng(1092026)
trials=0
for k in range(240):
    a=rng.integers(-5,6,size=6)
    ratios=[]
    for w in edge_masks:
        aw=a*w; q=chars@aw
        R=Fraction(int(q.max()-q.min()),2); L=int(abs(aw).sum())
        ratios.append(Fraction(L,1)/R if R else Fraction(0))
    c=max(ratios)
    x=rng.choice([0,.125,.25,.375,.5,.625,.75,.875,1],size=n)
    T,H=gaps(a,x)
    assert T<=float(c)*H+1e-8,(a,x,c,T,H)
    # Explicit fixed-one as well as fixed-zero half-valued points.
    x=rng.choice([0,.5,1],size=n)
    T,H=gaps(a,x); w=x==.5
    aw=a*np.array([w[i] and w[j] for i,j in edges]); q=chars@aw
    assert abs(H-(q.max()-q.min())/4)<1e-8
    assert abs(T-abs(aw).sum()/2)<1e-8
    trials+=2

# The factorization convention is essential: cancellation makes scalar H zero.
x=np.full(n,.5)
one=np.array([1,0,0,0,0,0]); assert gaps(one,x)==(.5,.5)
assert gaps(one-one,x)==(0.,0.)
# Thus treating +x0*x1 and -x0*x1 separately gives term gap 1, scalar gap 0.
summary={'exact_ternary_K4_cases':cases,'numerical_LP_point_checks':trials,'lp_tolerance':1e-8,'status':'PASS','limits':'Finite checks do not prove universal statements. Row norms and LP optima use floating point.'}
print(json.dumps(summary,indent=2))
