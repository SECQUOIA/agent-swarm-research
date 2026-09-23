"""Independent finite algebra/cut checks. Exact arithmetic except LP comparison oracle."""
from itertools import product
from random import Random
import json
import sympy as s
import numpy as np
from scipy.optimize import linprog
from pathlib import Path
rng=Random(3003)
checks={}
# Outlet elimination and full-vector residuals in a three-coordinate ambient space.
q,b,B,C1,C2,L=s.symbols('q b B C1 C2 L')
g1,g2=C1-q,C2-q
R=b*(B-q)
w1=g1*(R-g2*L)/(C1-C2)
assert s.factor(w1/g1+(R-w1)/g2-L)==0
checks['scalar_outlet_identity']='exact symbolic pass'
cs1=s.symbols('c10:13'); cs2=s.symbols('c20:23'); qq=s.symbols('q0:3'); bb=s.symbols('B0:3'); beta=[1,2,4]
g1=sum(a*(c-z) for a,c,z in zip(beta,cs1,qq)); g2=sum(a*(c-z) for a,c,z in zip(beta,cs2,qq)); R=b*sum(a*(c-z) for a,c,z in zip(beta,bb,qq)); w=s.symbols('w')
for h in range(3):
 a=s.expand((cs1[h]-qq[h])*g2-(cs2[h]-qq[h])*g1)
 f=s.expand(g1*(b*(bb[h]-qq[h])*g2-(cs2[h]-qq[h])*R))
 residual=(cs1[h]-qq[h])*w/g1+(cs2[h]-qq[h])*(R-w)/g2-b*(bb[h]-qq[h])
 assert s.cancel(g1*g2*residual-(a*w-f))==0
 assert s.Poly(a,*qq).total_degree()<=1
 assert s.Poly(f,*qq).total_degree()<=2
checks['vector_residuals_and_degrees']='exact symbolic pass'
q,b,B,v,W0=s.symbols('q b B v W0'); W1=b*(B-q)-W0
assert s.factor((b+W0/q-W1/(1-q)-v)*q*(1-q)-(W0-q*b*(B-1)-q*(1-q)*v))==0
checks['two_vector_outlet_identity']='exact symbolic pass'
# Signed finite bounds, including empty feasible sets; cut criteria versus an independent LP.
cut_trials=0; support_trials=0
for n in [1,2,3,4,5]:
 for trial in range(70):
  edges=[(i,i+1) if rng.randrange(2) else (i+1,i) for i in range(n-1)]
  if n>=3 and trial%2: edges.append((n-1,0))
  m=len(edges)
  ell=[rng.randint(-3,2) for _ in edges]; upp=[x+rng.randrange(4) for x in ell]
  alpha=[rng.randint(-4,1) for _ in range(n)]; bet=[x+rng.randrange(6) for x in alpha]
  subsets=[{i for i in range(n) if mask>>i&1} for mask in range(1<<n)]
  def f(S): return sum(upp[e] for e,(u,v) in enumerate(edges) if u in S and v not in S)-sum(ell[e] for e,(u,v) in enumerate(edges) if u not in S and v in S)
  def lower(S): return sum(ell[e] for e,(u,v) in enumerate(edges) if u in S and v not in S)-sum(upp[e] for e,(u,v) in enumerate(edges) if u not in S and v in S)
  cuts=all(sum(alpha[i] for i in S)<=f(S) and sum(bet[i] for i in S)>=lower(S) for S in subsets)
  M=np.zeros((n,m))
  for e,(u,v) in enumerate(edges): M[u,e]=1;M[v,e]=-1
  if m:
   lp=linprog(np.zeros(m),A_ub=np.vstack([M,-M]),b_ub=np.array(bet+[-a for a in alpha]),bounds=list(zip(ell,upp)),method='highs')
   assert cuts==lp.success
  else: assert cuts==all(a<=0<=b for a,b in zip(alpha,bet))
  cut_trials+=1
  if not cuts: continue
  g=[min(f(T)+sum(bet[i] for i in S-T)-sum(alpha[i] for i in T-S) for T in subsets) for S in subsets]
  assert g[0]==g[-1]==0
  for a in range(1<<n):
   for bmask in range(1<<n): assert g[a]+g[bmask]>=g[a|bmask]+g[a&bmask]
  cost=[rng.randint(-3,3) for _ in range(n)]; order=sorted(range(n),key=lambda i:-cost[i]); prev=0; dv=[0]*n; mask=0
  for i in order:
   mask |=1<<i; dv[i]=g[mask]-prev;prev=g[mask]
  assert sum(dv)==0
  assert all(alpha[i]<=dv[i]<=bet[i] for i in range(n))
  assert all(sum(dv[i] for i in S)<=f(S) for S in subsets)
  value=sum(a*b for a,b in zip(cost,dv))
  if m:
   opt=linprog(-np.array(cost)@M,A_ub=np.vstack([M,-M]),b_ub=np.array(bet+[-a for a in alpha]),bounds=list(zip(ell,upp)),method='highs')
   assert opt.success and abs(-opt.fun-value)<1e-8
  else: assert value==0
  support_trials+=1
checks['signed_cut_trials']=cut_trials;checks['box_rank_and_greedy_trials']=support_trials
# Exact binary dynamic programming, recurrence, and finite endpoint list against all labels.
for n in range(1,9):
 for trial in range(80):
  U=[(rng.randint(-5,5),rng.randint(-5,5)) for _ in range(n)]
  a=[0]+[rng.randrange(5) for _ in range(n-1)]; bb=[0]+[rng.randrange(5) for _ in range(n-1)]
  E0=U[0][0]; D=U[0][1]-U[0][0]; P=D; Z=0; candidates={0}
  for i in range(1,n):
   oldD=D; u=U[i][1]-U[i][0]
   E0+=U[i][0]+min(0,oldD+bb[i]);D=u+max(-bb[i],min(oldD,a[i]))
   low,high=-bb[i]-P,a[i]-P;candidates|={low,high};Z=max(low,min(Z,high));P+=u
   assert Z in candidates and D==Z+P
  brute=min(sum(U[i][x[i]] for i in range(n))+sum(a[i]*(x[i-1]==0 and x[i]==1)+bb[i]*(x[i-1]==1 and x[i]==0) for i in range(1,n)) for x in product([0,1],repeat=n))
  assert E0+min(0,D)==brute
checks['clamp_bruteforce_trials']=640
out=Path(__file__).with_name('results.json');out.write_text(json.dumps(checks,indent=2)+'\n');print(out.read_text())
