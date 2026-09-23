"""Independent finite audit: bounded exact integer quadratic evaluation."""
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction
import json
import numpy as np

root = Path(__file__).resolve().parents[3]
snapshot = root / 'process/snapshots/stage01-round02'
printed = (snapshot / 'sections/appendix-finite-signings.tex').read_text().split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0]
namespace = {}
exec(printed, namespace)
rows=[]
witnesses={3:[],4:[],5:[(1,2),(1,4),(2,3)],6:[(1,4),(1,5),(2,3),(2,5),(3,4)],7:[(1,2),(1,3),(1,6),(2,3),(2,5),(3,4)]}
for n in range(2,8):
 edges=list(combinations(range(n),2))
 free=[k for k,(i,j) in enumerate(edges) if i>0]
 vertex=np.array(list(product([-1,1],repeat=n)),dtype=np.int64)
 characters=np.array([vertex[:,i]*vertex[:,j] for i,j in edges],dtype=np.int64)
 weights=np.ones((1<<len(free),len(edges)),dtype=np.int64)
 for row,assignment in enumerate(product([-1,1],repeat=len(free))):
  weights[row,free]=assignment
 q=weights @ characters
 # Absolute Q <=21, so int64 arithmetic is exact without overflow.
 spans=q.max(axis=1)-q.min(axis=1)
 assert np.all(spans%2==0)
 ranges=spans//2
 best=int(ranges.min())
 assert best==namespace['result'][n-2]
 hist={str(int(k)):int(v) for k,v in zip(*np.unique(ranges,return_counts=True))}
 stored=json.loads((snapshot/'verification/complete_signings.json').read_text())['rows'][n-2]
 assert hist==stored['cut_range_histogram']
 item={'n':n,'representatives':len(weights),'min_range':best,'center':str(Fraction(len(edges),best)),'histogram':hist}
 if n in witnesses:
  a=np.array([-1 if e in witnesses[n] else 1 for e in edges],dtype=np.int64)
  values=a@characters
  item['witness_Q']=[int(values.min()),int(values.max())]
  assert int(values.max()-values.min())==2*best
 if n<=5:
  allweights=np.array(list(product([-1,1],repeat=len(edges))),dtype=np.int64)
  allq=allweights@characters
  assert int((allq.max(axis=1)-allq.min(axis=1)).min())==2*best
  item['unreduced_signings_checked']=len(allweights)
 rows.append(item)
# Independently check every face of the extended K6 witness, using scalar integers.
a=witnesses[6]
face_best=Fraction(0)
for k in range(2,8):
 for W in combinations(range(7),k):
  q=[sum((-1 if (i,j) in a else 1)*s[W.index(i)]*s[W.index(j)] for i,j in combinations(W,2)) for s in product([-1,1],repeat=k)]
  ratio=Fraction(k*(k-1),max(q)-min(q))
  face_best=max(face_best,ratio)
  if k==7: center={'min_Q':min(q),'max_Q':max(q),'ratio':str(ratio)}
assert face_best==3 and center=={'min_Q':-9,'max_Q':11,'ratio':'21/10'}
report={'arithmetic':'Exact int64 products with |Q|<=21; exact Python integers/Fraction for faces','rows':rows,'extended_K6':center,'extended_K6_best_face':str(face_best),'printed_code_reproduced':namespace['result']}
Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'ranges':[r['min_range'] for r in rows],'centers':[r['center'] for r in rows],'extended':center,'face':str(face_best)}))
