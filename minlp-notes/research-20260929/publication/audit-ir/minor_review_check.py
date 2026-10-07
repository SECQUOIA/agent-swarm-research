"""Recount display digits from the stored page parse; no fetch or audit rerun."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'bound-audit/pages.json'
rows=json.loads(p.read_text()); vals=[]
for r in rows:
 for x in r['points']+r['duals']:
  v=x['value']
  if 'inf' not in v.lower():vals.append((r['name'],v))
def nz(v):return len(v.lstrip('+-').replace('.','').strip('0'))
def all_digits(v):return len(v.lstrip('+-').replace('.','').lstrip('0'))
dec=[x for x in vals if '.' in x[1] and x[1].split('.')[1] and nz(x[1])>10]
whole=[x for x in vals if nz(x[1])>10]; all_=[x for x in vals if all_digits(x[1])>10]
assert len(dec)==35 and len(whole)==38 and len(all_)==46
print('fractional-part filter:',len(dec),'range',min(nz(v) for _,v in dec),max(nz(v) for _,v in dec))
print('first through last nonzero, unfiltered:',len(whole),'range',min(nz(v) for _,v in whole),max(nz(v) for _,v in whole))
print('including trailing integer zeros:',len(all_),'range',min(all_digits(v) for _,v in all_),max(all_digits(v) for _,v in all_))
print('integer additions:',[x for x in whole if x not in dec])
print('PASS: 35/38/46 are distinct, explicitly defined counts.')
