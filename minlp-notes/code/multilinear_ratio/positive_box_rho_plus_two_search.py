"""Exploratory test of the unproved scalar inequality T<=rho*DI+2*DO."""
import numpy as np
from scipy.optimize import differential_evolution
from positive_box_orientation_search import values


def objective(z,counts,rho):
 xs=np.repeat(z,counts)
 C,V,O=values(xs,rho)
 I=np.prod(1+(rho-1)*xs)
 T=C-V
 if T<1e-10*C:return 0.
 return ((rho+1)*C+V-rho*I-2*O)/T

if __name__=='__main__':
 for rho in [1.1,2.,4.,10.,100.]:
  best=(1e99,None)
  for counts in [(1,2),(1,8),(2,8),(8,8),(1,2,8),(2,5,12),(10,10,10)]:
   result=differential_evolution(lambda z:objective(z,counts,rho),[(1e-5,1-1e-5)]*len(counts),seed=23,popsize=10,maxiter=150,tol=1e-7,polish=True)
   if result.fun<best[0]:best=(result.fun,(counts,result.x))
  print('rho',rho,'minimum normalized slack',best,flush=True)
