"""Independent exact dual lower bounds for every word and switch-cell pair.

SciPy proposes sparse dual support only. SymPy solves that support exactly;
all dual signs, coordinates, and claimed lower bounds are checked rationally.
No manuscript implementation is imported.
"""
from itertools import product
from pathlib import Path
import json
from scipy.optimize import linprog
from sympy import Rational as Q, Matrix

rows=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[Q(row[0],146) for row in rows]+[Q(57,8)]
alloc=[[Q(x,146) for x in row[1:]] for row in rows]
alloc.append([a+(knots[-1]-knots[-2])/3 for a in alloc[-1]])
slopes=[[(b-a)/(y-x) for a,b in zip(aa,bb)] for x,y,aa,bb in zip(knots,knots[1:],alloc,alloc[1:])]
intercepts=[[a-s*x for a,s in zip(aa,ss)] for aa,ss,x in zip(alloc,slopes,knots)]
E=Q(18673,18396)
certs=[]; best=None; words=set()
for word in product(range(3),repeat=3):
 for first in range(len(slopes)):
  for second in range(first,len(slopes)):
   A=[[1,-1,0],[-1,0,0],[1,0,0],[0,-1,0],[0,1,0],[0,0,-1]]
   b=[0,-knots[first],knots[first+1],-knots[second],knots[second+1],0]
   for i in range(3):
    p,q,r=[int(z==i) for z in word]
    A.append([p-slopes[first][i],0,-1]);b.append(intercepts[first][i])
    A.append([p-q,q-slopes[second][i],-1]);b.append(intercepts[second][i])
    A.append([p-q,q-r,-1]);b.append(alloc[-1][i]-r*knots[-1])
   result=linprog([0,0,1],A_ub=A,b_ub=b,bounds=[(None,None)]*3,method='highs')
   assert result.success
   support=[i for i,x in enumerate(result.ineqlin.marginals) if abs(x)>1e-8]
   mat=Matrix([A[i] for i in support]).T
   yy,params=mat.gauss_jordan_solve(Matrix([0,0,1]))
   assert not params
   assert all(x<=0 for x in yy)
   assert mat*yy==Matrix([0,0,1])
   bound=sum(b[i]*x for i,x in zip(support,yy))
   assert bound>=E,(word,first,second,bound)
   if best is None or bound<best:best=bound;words={word}
   elif bound==best:words.add(word)
   certs.append({'word':word,'cells':[first,second],'rows':support,'y':[str(x) for x in yy],'lower_bound':str(bound)})
# Matching schedule: evaluate W-A independently at all input and schedule knots.
u,v=Q(8341,4599),Q(17639,4599)
def allocation(t):
 for j in range(len(slopes)):
  if knots[j]<=t<=knots[j+1]:return [a*t+c for a,c in zip(slopes[j],intercepts[j])]
 raise ValueError(t)
error=Q(0)
for t in sorted(set(knots+[u,v])):
 occ=[min(t,u),max(Q(0),t-v),max(Q(0),min(t,v)-u)]
 error=max(error,max(w-a for w,a in zip(occ,allocation(t))))
assert error==E and best==E
Path(__file__).with_name('dual_certificates.json').write_text(json.dumps(certs,indent=2)+'\n')
print('PASS exact dual identities and lower bounds for',len(certs),'word/cell LPs')
print('Minimum certificate lower bound:',best,'; words reaching it:',sorted(words))
print('PASS matching schedule direct exact error:',error)
