"""Check source-point bounds and gap conventions only; no primal construction."""
import json,xml.etree.ElementTree as E
from pathlib import Path
from fractions import Fraction as Q
import gaps
p=Path(__file__).resolve().parents[1];r=p.parents[2];ns='{os.optimizationservices.org}'
for n in [9,12,18,24]:
 name=f'waterno2_{n:02}';v=json.loads((r/f'open-instances-wave2/waterno2/logs/primal_{n:02}_w2.json').read_text())
 vars=E.parse(Path.home()/f'.cache/minlplib/minlplib/osil/{name}.osil').getroot().find('.//'+ns+'variables');worst=Q(0);where=None
 for j,(var,s) in enumerate(zip(vars,v['x'])):
  x=Q(s)
  for side in ['lb','ub']:
   b=var.get(side,'0' if side=='lb' else 'INF')
   if 'INF' in b:continue
   violation=Q(b)-x if side=='lb' else x-Q(b)
   if violation>worst:worst=violation;where=var.get('name')+' '+side
 print(name,'old max bound violation',float(worst),where)
 exact=Q(json.loads((p/f'points/{name}.exact.json').read_text())['objective']);old=Q(str(v['obj']))
 print(name,'relative primal change',float((exact-old)/old))
for name,lo,hi,d in gaps.rows():
 print(name,'gap/abs(dual)',float((hi-d)/abs(d)),'gap/abs(primal)',float((hi-d)/min(abs(lo),abs(hi))))
for f in sorted((p/'points').glob('*.point.json')):
 v=json.loads(f.read_text());assert '{lo, hi}' in v['construction'] and '(mid, rad)' not in v['construction'];assert any(isinstance(x,dict) and 'lo' in x and 'hi' in x for x in v['x'].values())
print('PASS: old bound violations, conservative gap rounding and lo/hi metadata checked.')
