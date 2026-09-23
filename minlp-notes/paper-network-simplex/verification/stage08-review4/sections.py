import sys,json
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sympy as s
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'code'))
from network_simplex import Point
from network_simplex.flat_chain import FlatChainSimplex

def family(K,alpha,r,last):
 N=K.rows; a=F(1,2*N); c=a/4; Ki=K.inv(); beta=(K.T*alpha)[0]
 assert K.T*alpha==s.ones(N,1)*beta and beta>0
 x=[];obs=[]
 for i in range(N):
  n=sum(K[i,j] for j in range(N));xa=n*a+(N-n)*c;x.extend([xa,F(1,2)-xa])
  obs.extend((2*i,j) for j in range(N) if not K[i,j])
 x.append(F(1,2));R=alpha[r]/alpha[last]
 epsilon=s.Rational(a)/(16*(1+R)*(1+max(sum(abs(v) for v in Ki.row(i)) for i in range(N))))
 count=0
 for k,l in product(range(-3,4),repeat=2):
  dr,ds=epsilon*k/4,epsilon*l/4
  if alpha[r]*dr+alpha[last]*ds<0:continue
  delta=s.zeros(N,1);delta[r]=dr;delta[last]=ds;tau=s.zeros(N,1);tau[last]=R*dr+ds
  w=s.ones(N,1)*a+Ki*(-delta+tau)
  assert sum(w)==F(1,2) and all(0<=wj<=2*a for wj in w)
  entries=[]
  for i in range(N):
   row=[w[j] if K[i,j] else c for j in range(N)]
   if i in (r,last):row[next(j for j in range(N) if not K[i,j])]+=delta[i]
   if i==last:row[next(j for j in range(N) if K[i,j])]-=tau[last]
   assert sum(row)==x[2*i] and all(0<=row[j]<=w[j] for j in range(N))
   entries.append(row)
  count+=1
 return count
K=s.Matrix([[1,1,1,0],[1,0,0,1],[0,1,0,1],[0,0,1,1]])
out={'four_label_exact_section_witnesses':family(K,s.Matrix([2,1,1,1]),0,1),'fibonacci':[]}
for q in range(3,13):
 rows=[f'P{i}' for i in range(1,q+1)]+['H0']+[f'H{i}' for i in range(3,q+1)]
 cols=[['H0','P1'],['H0','P2']]
 for i in range(3,q+1):cols.extend([[f'H{i}',f'P{i}'],[f'H{i}',f'P{i-1}',f'P{i-2}']])
 cols.append([f'P{q}',f'P{q-1}'])
 D=s.Matrix([[int(row in col) for col in cols] for row in rows]);N=2*q-1
 fib=[0,1,1]
 for i in range(3,q+2):fib.append(fib[-1]+fib[-2])
 alpha=s.Matrix(fib[1:q+1]+[fib[q+1]-1]+[fib[q+1]-fib[i] for i in range(3,q+1)])
 assert D.det()!=0 and sum(D)==5*q-4 and D.T*alpha==s.ones(N,1)*fib[q+1]
 count=family(s.ones(N,N)-D,alpha,q-1,0)
 out['fibonacci'].append({'q':q,'ratio':fib[q],'witnesses':count})
# Both exceptional circuits: independent literal query, verify returned cut on every path-state vertex.
for repair in (-2,2):
 L=3;m=3
 if repair==-2:
  x=(F(2,5),F(1,10))*3+(F(1,2),);y=(F(1,3),)*3;z={(2*i,i):F(0) for i in range(3)}
 else:
  x=(F(1,20),F(9,20))*3+(F(1,2),);y=(F(1,4),)*3;z={(2*i+1,j):F(1,20) for i,pair in enumerate(((0,1),(0,2),(1,2))) for j in pair}
 p=Point(x,y,z);cut=FlatChainSimplex(L,m,z).separate(p).cut
 assert cut and cut.evaluate(p)>0 and all(abs(v)<=1 for key,v in cut.coefficients.items() if key[0] in ('x','z'))
 for j in range(4):
  for choice in [None,*product((0,1),repeat=3)]:
   xx=[0]*7
   if choice is None:xx[-1]=1
   else:
    for i,a in enumerate(choice):xx[2*i+a]=1
   pp=Point(xx,[int(i==j) for i in range(3)],{(e,h):xx[e]*int(j==h) for e,h in z})
   assert cut.evaluate(pp)<=0
 out[f'repair_{repair}']={'exact_violation':str(cut.evaluate(p)),'cut':str(cut)}
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
