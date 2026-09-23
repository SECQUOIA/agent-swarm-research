from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json
base=Path('paper-switching-control/process/snapshots/stage02-round02')
manifest=json.loads((base/'snapshot-manifest.json').read_text())
assert all(hashlib.sha256((base/f).read_bytes()).hexdigest()==h for f,h in manifest.items())
print('PASS snapshot integrity:',len(manifest))

# Independently project each switching-time cell onto the error coordinate,
# obtaining an exact optimum for all words, rather than testing a threshold.
def eliminate(rows,index):
 positive=[];negative=[];out=[]
 for row in rows:
  coeff=row[index]
  if coeff>0:positive.append(row)
  elif coeff<0:negative.append(row)
  else:out.append(row[:index]+row[index+1:])
 for p in positive:
  for m in negative:
   row=tuple(-m[index]*a+p[index]*b for a,b in zip(p,m))
   out.append(row[:index]+row[index+1:])
 return list(set(out))
raw=[(0,0,0,0),(146,98,48,0),(194,110,48,36),(256,110,78,68),(408,224,116,68),(516,224,178,114),(580,240,178,162),(971,417,309,245)]
knots=[(Q(row[0],146),tuple(Q(x,146) for x in row[1:])) for row in raw]
L=Q(57,8); tstar,aa=knots[-1]
terminal=tuple(a+(L-tstar)/3 for a in aa)
knots.append((L,terminal));segments=[]
for (lo,a),(hi,b) in zip(knots,knots[1:]):
 slopes=tuple((bi-ai)/(hi-lo) for ai,bi in zip(a,b))
 intercepts=tuple(ai-s*lo for ai,s in zip(a,slopes))
 assert min(slopes)>=0 and max(slopes)<=Q(3,4) and sum(slopes)==1
 segments.append((lo,hi,slopes,intercepts))
word_min={}; count=0
for word in product(range(3),repeat=3):
 best=None
 for first in range(len(segments)):
  for second in range(first,len(segments)):
   lo,hi,s,b=segments[first]; vlo,vhi,ss,bb=segments[second]
   rows=[(-1,0,0,-lo),(1,0,0,hi),(0,-1,0,-vlo),(0,1,0,vhi),(1,-1,0,0),(0,0,-1,0)]
   for i in range(3):
    p,q,r=[Q(mode==i) for mode in word]
    rows.extend([(p-s[i],0,-1,b[i]),(p-q,q-ss[i],-1,bb[i]),(p-q,q-r,-1,terminal[i]-r*L)])
   rows=[tuple(map(Q,row)) for row in rows]
   projection=eliminate(eliminate(rows,0),0)
   assert all(a<=0 for a,rhs in projection)
   if any(a==0 and rhs<0 for a,rhs in projection):continue
   minimum=max(rhs/a for a,rhs in projection if a<0)
   best=minimum if best is None else min(best,minimum)
   count+=1
 word_min[word]=best
E=min(word_min.values()); expected=Q(18673,18396)
assert E==expected
print('PASS exact Fourier-Motzkin projected switching-time cells:',count)
print('Global minimum:',E)
print('Attaining words:',[word for word,val in word_min.items() if val==E])
print('Repeated-mode-word minimum:',min(val for word,val in word_min.items() if len(set(word))<3))

u,v=Q(8341,4599),Q(17639,4599)
def allocation(t):
 for lo,hi,s,b in segments:
  if lo<=t<=hi:return tuple(si*t+bi for si,bi in zip(s,b))
 raise AssertionError(t)
err=Q(0)
for t in sorted({x for x,_ in knots}|{u,v}):
 W=(min(t,u),max(Q(0),t-v),max(Q(0),min(t,v)-u))
 err=max(err,max(w-a for w,a in zip(W,allocation(t))))
assert err==E
assert E/L==Q(37346,262143)>Q(8,57)
delta=E-1
assert L-tstar==Q(63,2)*delta
for p,R,gap in ((0,Q(128,73),Q(2923,4599)),(1,Q(97,73),Q(4372,4599))):
 assert terminal[p]>2*E
 assert L-terminal[p]-E-(Q(290,73)-R+16*delta)==gap
print('PASS matching schedule, scale coefficient, sensitivity arithmetic and repeated margins')
