"""Independent reconstruction from printed event equations and exact dual audit.
Author quotient is read only for matching coordinate ordering to certificate arrays.
The quotient row sets/objective and all symbolic multiplicities are rebuilt here.
"""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import defaultdict
from fractions import Fraction as F
import hashlib,json,importlib.util
import sympy as sp
import numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).resolve().parent
SNAP=BASE.parents[2]/'process/snapshots/stage02-round01'
REF=SNAP/'verification/reference'
spec=importlib.util.spec_from_file_location('author',REF/'verify_general_four_block.py')
author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
results={}
for directory,manifest in ((SNAP,'snapshot-manifest.json'),(REF,'origin-manifest.json')):
 records=json.loads((directory/manifest).read_text())
 for filename,item in records.items():
  digest=item if isinstance(item,str) else item['sha256']
  assert hashlib.sha256((directory/filename).read_bytes()).hexdigest()==digest
 results[manifest]=len(records)

def ev(v,K):return (v[0],)+tuple(i if i in K else '*' for i in v[1:])
def cv(kind,v,K,i=None):
 if kind=='r':return ('r',v if v in K else '*')
 e=ev(v,K)
 if kind=='t':return ('t',e)
 if i in K:lab=i
 elif '*' in e:lab='same' if i in v[1:] else 'other'
 else:lab='*'
 return ('a',e,lab)
def from_author(key):
 def idx(x):return x[1] if x[0]=='s' else '*'
 if key[0]=='r':return ('r',idx(key[1]))
 e=(key[1][0],)+tuple(idx(x) for x in key[1][1:])
 if key[0]=='t':return ('t',e)
 if key[2][0]=='s':lab=key[2][1]
 elif '*' in e:lab='same' if key[2][1]==0 else 'other'
 else:lab='*'
 return ('a',e,lab)
def row(terms):
 d=defaultdict(int)
 for k,v in terms:d[k]+=v
 return frozenset((k,v) for k,v in d.items() if v)

def build(n,pair,z):
 S=set(range(3));K=S|set(pair)|{z}
 pairs=[p for p in combinations(range(n),2) if S&set(p)]
 events=[('g',)]+[('p',i) for i in S]+[('q',)+p for p in pairs]
 A=set();B=set();c=defaultdict(int)
 for v in events:
  B.add((row([(cv('t',v,K),-1)]+[(cv('a',v,K,i),1) for i in range(n)]),0))
  for j,k in permutations(set(range(n))-set(v[1:]),2):
   A.add((row([(cv('r',j,K),1),(cv('t',v,K),-1),(cv('a',v,K,k),1)]),-1))
 def precede(v,w):
  for i in range(n):A.add((row([(cv('a',v,K,i),1),(cv('a',w,K,i),-1)]),0))
 for v in events:
  if v[0]!='g':precede(v,('g',))
  if v[0]=='p' and v[1] not in pair:precede(('g',),v)
  if v[0]=='q':
   for i in set(v[1:])&S:precede(v,('p',i))
   if not set(v[1:])&set(pair):precede(('g',),v)
 for i in S:c[cv('t',('p',i),K)]+=(n-1)**2
 for p in pairs:c[cv('t',('q',)+p,K)]+=len(S&set(p))*(n-1)**2
 for i in range(n):
  if i!=z:c[cv('r',i,K)]-=3*n*n
 return A,B,dict(c)

# Compare independent full-row projection with bundled quotient: no row order assumption.
checks=0;counts=[]
for pair,z in author.CASES:
 for n in (5,6,9,12,23):
  if z>=n:continue
  V,A,b,B,d,c=author.quotient(n,pair,z);keys=list(map(from_author,V))
  assert len(set(keys))==len(keys)
  ia,ib,ic=build(n,pair,z)
  assert ia=={(row([(keys[j],v) for j,v in r]),rhs) for r,rhs in zip(A,b)}
  assert ib=={(row([(keys[j],v) for j,v in r]),rhs) for r,rhs in zip(B,d)}
  assert {key:value for key,value in zip(keys,c) if value}==ic
  checks+=1
  if n==9:counts.append((len(V),len(A),len(B)))
results['independent_event_matrix_cases']=checks;results['stable_quotient_dimensions']=counts

# Build symbolic mass coefficients/objective directly from the combinatorial counts.
x=sp.Symbol('n',integer=True)
def symbolic_mass(e,K):
 terms=[(('t',e),-1)]+[(('a',e,i),1) for i in K]
 if '*' in e:terms.extend([(('a',e,'same'),1),(('a',e,'other'),x-len(K)-1)])
 else:terms.append((('a',e,'*'),x-len(K)))
 return dict(terms)
def symbolic_objective(key,K,z):
 if key[0]=='a':return 0
 if key[0]=='r':return -3*x*x*(x-len(K) if key[1]=='*' else int(key[1]!=z))
 e=key[1]
 if e[0]=='g':return 0
 if e[0]=='p':return (x-1)**2
 multiplicity=x-len(K) if '*' in e else 1
 weight=sum(i in (0,1,2) for i in e[1:])
 return weight*multiplicity*(x-1)**2

def poly(v):return sum(c*x**j for j,c in enumerate(v))
data=json.loads((REF/'certificates_general_four_block.json').read_text())
# Finite data exact equalities on already independently checked row-construction algorithm.
for cert in data['finite']:
 n=cert['n'];p=tuple(cert['pair']);z=cert['distinguished']
 V,A,b,B,d,c=author.quotient(n,p,z)
 D=cert['denominator'];Y={int(i):v for i,v in cert['inequality'].items()};Z={int(i):v for i,v in cert['equality'].items()}
 assert D>0 and all(v<=0 for v in Y.values())
 lhs=[0]*len(V)
 for rows,mults in ((A,Y),(B,Z)):
  for r,w in mults.items():
   for j,v in rows[r]:lhs[j]+=w*v
 assert lhs==[D*v for v in c]
 assert sum(b[i]*v for i,v in Y.items())==D*3*n*n*(n-1)
results['finite_dual_certificates']=len(data['finite'])
for cert in data['symbolic']:
 pair=tuple(cert['pair']);z=cert['distinguished'];K=set(range(3))|set(pair)|{z}
 V,A,b,B,d,c=author.quotient(9,pair,z);keys=list(map(from_author,V));lookup={v:i for i,v in enumerate(keys)}
 D=poly(cert['denominator']);D0=poly(cert['denominator_div_n_minus_one_squared'])
 Y={int(i):poly(v) for i,v in cert['inequality'].items()};Z={int(i):poly(v) for i,v in cert['equality'].items()}
 assert sp.expand(D-(x-1)**2*D0)==0
 shifted=sp.Poly(D.subs(x,x+23),x)
 assert shifted.eval(0)>0 and all(v>=0 for v in shifted.all_coeffs())
 assert all(all(v>=0 for v in sp.Poly(-w.subs(x,x+23),x).all_coeffs()) for w in Y.values())
 lhs=[0]*len(V)
 for r,w in Y.items():
  for j,v in A[r]:lhs[j]+=w*v
 for r,w in Z.items():
  # Each mass row is uniquely identified by its negative time coefficient.
  timekeys=[keys[j] for j,v in B[r] if keys[j][0]=='t' and v==-1]
  assert len(timekeys)==1
  mass=symbolic_mass(timekeys[0][1],K)
  for key,v in mass.items():lhs[lookup[key]]+=w*v
 assert all(sp.expand(value-D0*symbolic_objective(key,K,z))==0 for value,key in zip(lhs,keys))
 assert sp.expand(sum(b[i]*v for i,v in Y.items())-3*x*x*(x-1)*D0)==0
results['symbolic_direct_count_certificates']=len(data['symbolic'])

# Boundary n=k=3: minimize actual one-sided error over all 27 words and all
# affine cells of the two switch times. No repeated-word greedy assumption.
raw=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[(F(t,146),tuple(F(v,146) for v in a)) for t,*a in raw]
L=F(57,8);last,m=knots[-1];terminal=tuple(a+(L-last)/3 for a in m);knots.append((L,terminal))
segments=[]
for (lo,aa),(hi,bb) in zip(knots,knots[1:]):
 slopes=tuple((b-a)/(hi-lo) for a,b in zip(aa,bb));intercepts=tuple(a-s*lo for a,s in zip(aa,slopes))
 assert sum(slopes)==1 and all(0<=s<=F(3,4) for s in slopes)
 segments.append((lo,hi,slopes,intercepts))
best=10.;bestword=None;lps=0
for word in product(range(3),repeat=3):
 for j,first in enumerate(segments):
  for second in segments[j:]:
   lo,hi,mu,bu=first;vlo,vhi,mv,bv=second
   rows=[[1,-1,0]];rhs=[0]
   for i in range(3):
    a,b,c=[int(p==i) for p in word]
    rows.extend([[a-mu[i],0,-1],[a-b,b-mv[i],-1],[a-b,b-c,-1]])
    rhs.extend([bu[i],bv[i],terminal[i]-c*L])
   sol=linprog([0,0,1],A_ub=np.array(rows,dtype=float),b_ub=np.array(rhs,dtype=float),bounds=[(float(lo),float(hi)),(float(vlo),float(vhi)),(0,None)],method='highs')
   assert sol.success
   if sol.fun<best:best=sol.fun;bestword=word
   lps+=1
assert best>1.0001
results['n3_word_cell_LPs']=lps;results['n3_minimum_numeric']=best;results['n3_minimizing_word_numeric']=bestword
(BASE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
