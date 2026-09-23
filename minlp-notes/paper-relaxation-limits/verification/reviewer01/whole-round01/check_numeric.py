from pathlib import Path
import json, math
import numpy as np
from scipy.optimize import linprog
from scipy.integrate import quad
records=[]
for L in (2,3):
 m=2**L;n=m+L
 states=((np.arange(2**n)[:,None]>>np.arange(n))&1).astype(float)
 vals=np.zeros(len(states));means=np.r_[np.full(m,1-1/m),[2.**(-j) for j in range(1,L+1)]]
 for j in range(1,L+1):
  k=m//(2**j)
  for start in range(0,m,k):vals+=states[:,m+j-1]*np.prod(states[:,start:start+k],axis=1)
 A=np.vstack([np.ones(len(states)),states.T]);b=np.r_[1,means]
 lo=linprog(vals,A_eq=A,b_eq=b,bounds=(0,None),method='highs');hi=linprog(-vals,A_eq=A,b_eq=b,bounds=(0,None),method='highs')
 assert lo.success and hi.success
 s=next(s for s in range(1,L) if (L-s+1)*2**(-s-1)<=1<=(L-s+2)*2**(-s))
 exact=s+(L-s)*2**(-s);gap=-hi.fun-lo.fun
 assert abs(gap-exact)<1e-9
 records.append({'L':L,'states':len(states),'computed_H':gap,'formula_H':exact,'max_equality_residual':max(abs(A@lo.x-b))})
errors=[]
for M in [1,2,10,1000]:
 for p in [.00001,.01,.25,.49]:
  h=min(M*p,1);a=1+math.log(h/p)
  integral=quad(lambda t:min(1,p/t)/a,0,h,points=[p],epsabs=1e-12)[0]
  errors.append(abs(integral-p))
res={'numerical_only':True,'dyadic_vertex_LPs':records,'harmonic_marginal_integrals':len(errors),'max_integral_error':max(errors),'limits':'Floating-point checks only, no universal theorem or exact numerical certification.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2));print(res)
