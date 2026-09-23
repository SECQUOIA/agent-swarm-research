"""Reviewer 1: independent finite algebra checks; these are not general proofs."""
from itertools import combinations, product
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import json
import sympy as S
import numpy as np
from scipy.optimize import linprog

out = {}
C = S.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[-1,0,1],[0,-1,-1]])
arcs = [(1,2),(1,3),(2,3),(0,1),(0,2),(0,3)]
A=S.zeros(4,6)
for e,(u,v) in enumerate(arcs): A[u,e]=-1; A[v,e]=1
assert A*C == S.zeros(4,3)
minor_count=pivot_count=rank_count=0
for d in range(4):
 for rows in combinations(range(6),d):
  D=C[list(rows),:]
  for cols in combinations(range(3),d):
   B=D[:,list(cols)]
   assert B.det() in (-1,0,1)
   minor_count+=1
   if not B.det(): continue
   free=[i for i in range(3) if i not in cols]
   for e in range(6):
    W=C[e,list(cols)]*B.inv()
    R=C[e,free]-W*D[:,free]
    assert all(t in (-1,0,1) for t in [*W,*R])
    pivot_count+=1
for mask in range(64):
 observed=[e for e in range(6) if mask>>e&1]
 unobserved=[e for e in range(6) if e not in observed]
 parent=list(range(4))
 def root(a):
  while parent[a]!=a: a=parent[a]
  return a
 for e in unobserved:
  u,v=arcs[e]; parent[root(u)]=root(v)
 components=len({root(a) for a in range(4)})
 rho=len(unobserved)-4+components
 assert 3-C[observed,:].rank()==rho==len(unobserved)-A[:,unobserved].rank()
 rank_count+=1
out['k4_unit_minors']=minor_count
out['k4_pivot_row_checks']=pivot_count
out['k4_all_observation_masks']=rank_count

def primitive(v):
 den=lcm(*[int(x.q) for x in v]); a=[int(x*den) for x in v]
 g=reduce(gcd,[abs(x) for x in a]); a=tuple(x//g for x in a)
 return a if next(x for x in a if x)>0 else tuple(-x for x in a)

M=S.Matrix(sorted(set(tuple(sign*C[e,i] for i in range(3)) for e in range(6) for sign in (-1,1))))
directions=set()
for inds in combinations(range(M.rows),2):
 D=M[list(inds),:]
 if D.rank()==2: directions.add(primitive(D.nullspace()[0]))
for d in directions: assert all(x in (-1,0,1) for x in M*S.Matrix(d))
rays=set()
for ds in combinations(sorted(directions),2):
 D=S.Matrix(ds)
 if D.rank()==2:
  h=primitive(D.nullspace()[0]); rays|={h,tuple(-x for x in h)}
maxq=0; bases=0
for inds in combinations(range(M.rows),3):
 B=M[list(inds),:]
 if not B.det(): continue
 bases+=1
 for h in rays:
  q=B.T.inv()*S.Matrix(h)
  assert all(x.q==1 and abs(x)<=2 for x in q)
  if all(x>=0 for x in q): maxq=max(maxq,max(q))
assert maxq==2
out['k4_libraries']={'directions':len(directions),'signed_rays':len(rays),'bases':bases,'largest_nonnegative_multiplier':int(maxq)}

counts=[]
for m in (1,2,3):
 normals=sorted(set([tuple(int(mask>>j&1) for j in range(m)) for mask in range(1,2**m)] + [tuple(-int(i==j) for j in range(m)) for i in range(m)]+[(-1,)*m]))
 circuits=[]
 for k in range(2,m+2):
  for inds in combinations(range(len(normals)),k):
   Q=S.Matrix([normals[i] for i in inds]).T
   ns=Q.nullspace()
   if len(ns)!=1: continue
   v=primitive(ns[0])
   if all(x>0 for x in v): circuits.append((inds,v))
 counts.append((len(normals),len(circuits),max(max(w) for _,w in circuits)))
assert counts==[(2,1,1),(6,5,1),(11,16,2)]
out['reduced_chain_libraries']=counts

# Independent full-state LP for the five-product K4 coordinate section.
v=S.Matrix([S.Rational(1,2)]*3+[S.Rational(1,4),S.Rational(1,2),S.Rational(1,2)])
b=A*v
x=S.Matrix([S.Rational(2,3),S.Rational(13,24),S.Rational(5,8),S.Rational(11,24),S.Rational(11,24),S.Rational(1,3)])
assert list(b)==[-S.Rational(5,4),-S.Rational(3,4),S.Rational(1,2),S.Rational(3,2)]
Q=np.zeros((18,18)); rhs=np.zeros(18)
for j in range(3): Q[4*j:4*j+4,6*j:6*j+6]=np.array(A,float);rhs[4*j:4*j+4]=np.array(b,float).ravel()/3
for e in range(6): Q[12+e,[e,6+e,12+e]]=1;rhs[12+e]=float(x[e])
n=0
for pp,qq in product(range(-4,5),repeat=2):
 p,q=S.Rational(pp,1000),S.Rational(qq,1000)
 obs=[(0,0,S.Rational(1,6)+p),(1,0,S.Rational(1,6)+q),(4,0,S.Rational(1,6)),(2,1,S.Rational(1,6)),(3,1,S.Rational(1,12))]
 eq=np.zeros((5,18)); er=[]
 for k,(e,j,z) in enumerate(obs): eq[k,6*j+e]=1;er.append(float(z))
 lp=linprog(np.zeros(18),A_eq=np.vstack([Q,eq]),b_eq=np.r_[rhs,er],bounds=(0,1/3),method='highs')
 assert lp.status==(0 if 2*p+q>=0 else 2),(p,q,lp.message)
 if 2*p+q>=0:
  ts=[S.Matrix([p,q,p]),S.Matrix([q/2,-q/2,0]),S.Matrix([S.Rational(1,6)-p-q/2,S.Rational(1,24)-q/2,S.Rational(1,8)-p])]
  fs=[v/3+C*t for t in ts]
  assert sum(fs,S.zeros(6,1))==x
  assert all(all(0<=a<=S.Rational(1,3) for a in f) and A*f==b/3 for f in fs)
 n+=1
out['k4_section_grid_numerical_tests_and_exact_inside_witnesses']=n

fib=[0,1,1]
for i in range(3,14):fib.append(fib[-1]+fib[-2])
for q in range(3,12):
 rows=[('P',i) for i in range(1,q+1)]+[('H',0)]+[('H',i) for i in range(3,q+1)]
 cols=[[('H',0),('P',1)],[('H',0),('P',2)]]
 for i in range(3,q+1):cols.extend([[('H',i),('P',i)],[('H',i),('P',i-1),('P',i-2)]])
 cols.append([('P',q),('P',q-1)])
 D=S.Matrix([[int(row in col) for col in cols] for row in rows]);N=2*q-1;gamma=fib[q+1]
 alpha=S.Matrix([fib[i] if kind=='P' else gamma-(1 if i==0 else fib[i]) for kind,i in rows])
 K=S.ones(N)-D
 assert sum(D)==5*q-4 and D.det()!=0 and K.det()!=0
 assert D.T*alpha==gamma*S.ones(N,1)
 assert K.T*alpha==((q-2)*gamma+1)*S.ones(N,1)
 assert sum(alpha)==(q-1)*gamma+1
out['fibonacci_exact_instances']=9
out['status']='PASS'
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
