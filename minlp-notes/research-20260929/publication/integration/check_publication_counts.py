"""Exact saved-page counts and read-only round-3 handoff checks."""
import hashlib,json,re
from fractions import Fraction as Q
from pathlib import Path
B=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
pages=json.loads((B/'bound-audit/pages.json').read_text())
values=[x['value'] for p in pages for x in p['points']+p['duals'] if re.fullmatch(r'-?\d+(?:\.\d*)?',x['value'])]
assert len(pages)==1633 and sum(len(p['points']) for p in pages)==2816 and sum(len(p['duals']) for p in pages)==11086
assert len(values)==13847
def digits(v,trailing=False):
    a,b=(v.lstrip('-').split('.')+[''])[:2];s=(a+b).lstrip('0')
    return len(s if trailing and not b else s.rstrip('0'))
for fractional,trailing,count,distinct,low,high in [(True,False,35,18,11,17),(False,False,38,19,11,19),(False,True,46,27,11,20)]:
    found=[v for v in values if (not fractional or ('.' in v and v.split('.')[1])) and digits(v,trailing)>10]
    assert (len(found),len(set(found)),min(digits(v,trailing) for v in found),max(digits(v,trailing) for v in found))==(count,distinct,low,high)
    print('PASS displayed entry convention',count,'distinct strings',distinct,'range',low,high)
# Exact powers of ten for the half-unit slack; no logarithms or floats.
def magnitude(q):
    q=abs(q);e=0
    while q>=10:q/=10;e+=1
    while q<1:q*=10;e-=1
    return e
def slacks(s):
    value=Q(s)
    if value==0:return Q('5e-9'),Q('5e-9')
    decimals=len(s.split('.')[1]) if '.' in s else 0
    shown=Q(1,2)*Q(10)**(-decimals);floor=Q(1,2)*Q(10)**(magnitude(value)-9)
    return shown,max(shown,floor)
screen=json.loads((B/'bound-audit/screen.json').read_text())
assert len(screen['pairs'])==158
assert sum(slacks(x['d_listed'])[0]!=slacks(x['d_listed'])[1] for x in screen['pairs'])==0
print('PASS slack floor changes 0 of 158 screened pairs')
# Rebuild display ties directly, using the screen's stated feasibility limit.
ties=[]
for p in pages:
    if p['sense'] not in ('min','max'):continue
    for x in p['points']:
        try:
            if Q(x['infeas'])>Q('1e-5'):continue
            f=Q(x['value'])
        except (ValueError,ZeroDivisionError):continue
        for d in p['duals']:
            try:v=Q(d['value'])
            except ValueError:continue
            if v==f:ties.append((p['name'],d['value']))
assert len(ties)==3851 and len({n for n,d in ties})==1133
changed=[(n,d) for n,d in ties if slacks(d)[0]!=slacks(d)[1]]
assert len(changed)==17 and {n for n,d in changed}=={'fac1','fac2','waternd_fosspoly0'}
print('PASS slack floor changes 17 tie pairs on exactly three named instances')
# Update from the parent: inspect, never mutate, protected originals.
edits=json.loads((B/'publication/reviews/minor-fixes/integration-r2.json').read_text());status=[]
for i,e in enumerate(edits,1):
    if i<=33:continue
    txt=(B/e['target']).read_text()
    old,new=txt.count(e['old']),txt.count(e['new'])
    status.append({'index':i,'target':e['target'],'old_count':old,'new_count':new,'status':'already corrected by round-3 owner' if not old and new else 'protected historical solver-runs correction remains with its owner'})
    print('PROTECTED READ ONLY',i,e['target'],old,new)
assert all(x['old_count']==0 and x['new_count']>0 for x in status[:6])
(O/'protected-handoff.json').write_text(json.dumps(status,indent=2)+'\n')
scip=(B/'publication/scip-bug/report.md').read_text();section=scip.split('### 5.3',1)[1].split('### 5.4',1)[0]
rows=[x for x in section.splitlines() if x.startswith('| dbgsol ') or x.startswith('| master dbgsol ')]
assert len(rows)==14 and sum('p5, 0 and 2' in x for x in rows)==1
assert 'Of these five examined solutions, three are refuted wrong claims' in scip
print('PASS SCIP Section 5.3: 14 rows, 15 runs; three of five examined claims refuted')
print('ALL PUBLICATION COUNT AND HANDOFF CHECKS PASSED')
