"""Exact dense-regression check of count/history/cooldown path pricing."""
import itertools,json
from pathlib import Path
from functools import lru_cache
import sympy as sp

n=7
rho=sp.Rational(3,5)
r=sp.Rational(2,3)
R=sp.Matrix(n,n,lambda i,j:rho**abs(i-j)+(r if i==j else 0))
F=sp.Matrix([[1,sp.Rational(i-3,5)] for i in range(n)])
W=sp.diag(1,2)
@lru_cache(None)
def weight(t,history):
 if not history:
  residual=F[t,:]; variance=R[t,t]
 else:
  cross=R.extract([t],history)
  inverse=R.extract(history,history).inv()
  residual=F[t,:]-cross*inverse*F.extract(history,[0,1])
  variance=R[t,t]-(cross*inverse*cross.T)[0]
 return sp.trace(W*residual.T*residual)/variance

def explicit(window,gap,mandatory,forbidden):
 best={}
 for bits in itertools.product([0,1],repeat=n):
  selected=tuple(t for t,b in enumerate(bits) if b)
  if not set(mandatory)<=set(selected) or set(forbidden)&set(selected):continue
  if any(j-i<gap for i,j in zip(selected,selected[1:])):continue
  value=sum((weight(t,tuple(j for j in selected if t-window<=j<t)) for t in selected),sp.Rational(0))
  k=len(selected)
  if k not in best or value>best[k]:best[k]=value
 return best

def automaton(window,gap,mandatory,forbidden):
 states={(0,0,0):sp.Rational(0)}
 limit=(1<<window)-1
 for t in range(n):
  nxt={}
  for (mask,cool,count),value in states.items():
   history=tuple(j for j in range(max(0,t-window),t) if mask>>(t-j-1)&1)
   for selected in [0,1]:
    if (selected and (cool or t in forbidden)) or (not selected and t in mandatory):continue
    key=(((mask<<1)|selected)&limit,gap-1 if selected else max(cool-1,0),count+selected)
    candidate=value+(weight(t,history) if selected else 0)
    if key not in nxt or candidate>nxt[key]:nxt[key]=candidate
  states=nxt
 best={}
 for (_,_,k),value in states.items():
  if k not in best or value>best[k]:best[k]=value
 return best

families=[((),()),((0,),()),((0,6),(3,)),((2,3),()),((2,),(2,)),((),tuple(range(n)))]
cases=0
for window in range(4):
 for gap in range(1,n+3):
  for mandatory,forbidden in families:
   a=automaton(window,gap,mandatory,forbidden)
   b=explicit(window,gap,mandatory,forbidden)
   assert a==b,(window,gap,mandatory,forbidden,a,b)
   cases+=1
report={'status':'pass','arithmetic':'exact rational SymPy','cases':cases,'candidate_times':n,'windows':[0,1,2,3],'gaps':list(range(1,n+3)),'checks':'All cardinality optimum values and infeasibility, mandatory/forbidden conflicts, gap larger than history/horizon.'}
Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
