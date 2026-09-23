"""Floating search for a counterexample to the sufficient coefficient lemma."""
import numpy as np
from scipy.optimize import differential_evolution
from positive_box_coefficient_search import coefficient_slacks

for counts in [(1,2),(1,4),(2,3),(1,2,4),(2,3,5),(1,1,1,1,1)]:
 n=sum(counts)
 for degree in range(3,n+1):
  def target(vals):
   s,C,V=coefficient_slacks(np.repeat(vals,counts))
   return s[degree]/max(1e-5,C[degree])
  res=differential_evolution(target,[(1e-5,1-1e-5)]*len(counts),seed=773,maxiter=70,popsize=8,tol=1e-6,polish=True)
  print(counts,degree,res.fun,res.x,flush=True)
