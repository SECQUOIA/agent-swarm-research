"""Independent root check of the five-observation, two-label K4 section."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

edges=[(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
A=[[F(int(w==t)-int(w==s)) for s,t in edges] for w in range(4)]
C=[[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]]
v=[F(1,2),F(1,2),F(1,2),F(1,4),F(1,2),F(1,2)]
weight=F(1,3)
b=[sum(a*t for a,t in zip(row,v)) for row in A]
r0=[F(1,6),F(1,24),F(1,8)]
x=[vv+sum(F(c)*t for c,t in zip(row,r0)) for vv,row in zip(v,C)]
assert b==[F(-5,4),F(-3,4),F(1,2),F(3,2)]
assert x==[F(2,3),F(13,24),F(5,8),F(11,24),F(11,24),F(1,3)]
assert all(sum(A[i][e]*C[e][j] for e in range(6))==0 for i in range(4) for j in range(3))
counts={'grid_cases':0,'exact_decompositions':0,'numerical_infeasibility_checks':0}
for ii in range(-8,9):
    for jj in range(-8,9):
        p,q=F(ii,1024),F(jj,1024)
        assert abs(p)<F(1,96) and abs(q)<F(1,96)
        obs={(0,0):F(1,6)+p,(1,0):F(1,6)+q,(4,0):F(1,6),(2,1):F(1,6),(3,1):F(1,12)}
        rows=[];rhs=[]
        for state in range(3):
            for i in range(4):
                row=[F(0)]*18
                for e in range(6): row[state*6+e]=A[i][e]
                rows.append(row);rhs.append(weight*b[i])
        for e in range(6):
            row=[F(0)]*18
            for state in range(3): row[state*6+e]=1
            rows.append(row);rhs.append(x[e])
        for (e,state),value in obs.items():
            row=[F(0)]*18;row[state*6+e]=1
            rows.append(row);rhs.append(value)
        lp=linprog(np.zeros(18),A_eq=np.array(rows,dtype=float),b_eq=np.array(rhs,dtype=float),bounds=[(0,float(weight))]*18,method='highs')
        expected=2*p+q>=0
        assert lp.status==(0 if expected else 2),(p,q,lp.status,lp.message)
        counts['grid_cases']+=1
        if not expected:
            counts['numerical_infeasibility_checks']+=1
            continue
        theta=[[p,q,p],[q/2,-q/2,F(0)],[F(1,6)-p-q/2,F(1,24)-q/2,F(1,8)-p]]
        flows=[[weight*v[e]+sum(C[e][j]*t[j] for j in range(3)) for e in range(6)] for t in theta]
        assert all(0<=value<=weight for f in flows for value in f)
        assert all(sum(A[i][e]*f[e] for e in range(6))==weight*b[i] for f in flows for i in range(4))
        assert all(sum(f[e] for f in flows)==x[e] for e in range(6))
        assert all(flows[state][e]==value for (e,state),value in obs.items())
        counts['exact_decompositions']+=1
out={'status':'PASS','candidate':'K4, two explicit simplex labels, five observed products, local section 2U+V >= 1/2','balances':[str(t) for t in b],'aggregate':[str(t) for t in x],**counts,'scope':'Finite exact feasible-witness checks and independent numerical full-state LP classifications supplement the analytical local-half-plane proof; they do not enumerate ambient facets.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
