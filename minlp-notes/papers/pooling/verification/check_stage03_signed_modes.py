"""Independent stage-3 reviewer 02 signed-mode regression.

Requires NumPy and SciPy. Compares original physical endpoint-branch LPs
with exhaustive integral modes, including separate arc bounds. The LP
comparisons are numerical; this finite check supplements the proof.
"""
import itertools, random
import numpy as np
from scipy.optimize import linprog
rng=random.Random(3102)
for trial in range(48):
    n=4
    ends=[tuple(rng.randrange(2) for _ in range(4)) for v in range(n)]
    caps=[rng.randrange(3) for _ in range(8)]
    pool=[rng.randrange(3) for _ in range(n)]
    arc=[rng.randrange(3) for _ in range(4*n)]
    reward=[(rng.randrange(-3,4),rng.randrange(-3,4)) for _ in range(n)]
    A=[]; b=[]; eq=[]
    for k in range(4):
        for j in range(2):
            row=np.zeros(4*n)
            for v in range(n):
                if ends[v][k]==j: row[4*v+k]=1
            A.append(row); b.append(caps[2*k+j])
    for v in range(n):
        row=np.zeros(4*n);row[4*v:4*v+2]=1; A.append(row); b.append(pool[v])
        row=np.zeros(4*n);row[4*v:4*v+4]=[1,1,-1,-1];eq.append(row)
    c=np.zeros(4*n)
    for v,(alpha,beta) in enumerate(reward): c[4*v+1]=-beta;c[4*v+2]=-alpha
    lpbest=-float('inf')
    for mode in itertools.product(range(2),repeat=n):
        bounds=[(0,x) for x in arc]
        for v,m in enumerate(mode): bounds[4*v+(1 if m==0 else 2)]=(0,0)
        sol=linprog(c,A_ub=A,b_ub=b,A_eq=eq,b_eq=np.zeros(n),bounds=bounds,method='highs')
        assert sol.success
        lpbest=max(lpbest,-sol.fun)
    intbest=0
    for selection in itertools.product(range(5),repeat=n):
        x=np.zeros(4*n)
        for v,s in enumerate(selection):
            if s in (1,2): x[4*v]=x[4*v+2]=s
            if s in (3,4): x[4*v+1]=x[4*v+3]=s-2
        if np.any(x>arc) or np.any(np.array(A)@x>np.array(b)): continue
        intbest=max(intbest,-c@x)
    assert abs(lpbest-intbest)<1e-8,(trial,lpbest,intbest)
print('48 signed weighted integer-capacity instances: original-flow endpoint branch LP optima equal exhaustive integral pure-mode optima.')
print('Included zero and restrictive arc capacities, signed rewards, and repeated mode endpoint pairs (multigraph edges).')
