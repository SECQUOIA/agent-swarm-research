"""Demonstrate indexed-dual sensitivity to unspecified set traversal order.
This is a controlled portability probe, not a claimed failure on CPython today.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json
OUT=Path(__file__).resolve().parent
SNAP=OUT.parents[2]/'process/snapshots/stage03-round01'
p=SNAP/'verification/reference/general_reach_research.py'
source=p.read_text()
normal={'__name__':'normal','__file__':str(p)}
reverse={'__name__':'reverse','__file__':str(p)}
exec(compile(source,str(p),'exec'),normal)
# Preserve all mathematics/variables, permute only available-mode iteration.
modified=source.replace('for i in available:', 'for i in sorted(available, reverse=True):')
assert modified!=source
exec(compile(modified,'controlled-order-probe','exec'),reverse)
n,A,B,c=normal['weighted_triple_relaxation']()
n2,Ar,Br,cr=reverse['weighted_triple_relaxation']()
canon=lambda rows:Counter((tuple(sorted(row.items())),rhs) for row,rhs in rows)
assert n==n2 and B==Br and c==cr and canon(A)==canon(Ar)
cert=json.loads((SNAP/'verification/stage03/chronological_chamber_certificate.json').read_text())
for a,b in zip(cert['order'],cert['order'][1:]):
 for i in range(6):Ar.append(({7+7*a+i:1,7+7*b+i:-1},0))
y=[F(v) for v in cert['inequality_dual']];z=[F(v) for v in cert['equality_dual']]
r=[F(c.get(i,0)) for i in range(n)]
for rows,w in ((Ar,y),(Br,z)):
 for (row,rhs),v in zip(rows,w):
  for i,a in row.items():r[i]-=v*a
assert min(r)<0
result={'same_row_multiset':True,'same_variable_coordinates':True,'changed_traversal_only':'available modes reversed','minimum_residual':str(min(r)),'negative_residual_coordinates':sum(v<0 for v in r)}
(OUT/'order-probe-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
