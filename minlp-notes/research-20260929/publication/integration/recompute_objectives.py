"""Independently recompute cheap objectives from saved exact points and OSIL."""
import gzip,json,re,xml.etree.ElementTree as ET
from fractions import Fraction as Q
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
CACHE=Path.home()/'.cache/minlplib/minlplib/osil'
def model(name):
    root=ET.parse(CACHE/(name+'.osil')).getroot()
    # Strip namespaces in memory only.
    for e in root.iter():e.tag=e.tag.rsplit('}',1)[-1]
    return root.find('instanceData')
m=model('dtoc5');names=[e.attrib['name'] for e in m.find('variables')]
with gzip.open(BASE/'publication/primal/dtoc5-lukvle10/points/dtoc5_point.txt.gz','rt') as f:
    x={k:Q(v) for line in f if line.strip() and not line.startswith('#') for k,v in [line.split()]}
f=Q(0);n=0
for term in m.find('quadraticCoefficients'):
    if term.attrib['idx']=='-1':
        a=term.attrib;f+=Q(a['coef'])*x[names[int(a['idxOne'])]]*x[names[int(a['idxTwo'])]];n+=1
assert f==Q((BASE/'publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt').read_text().strip())
print('PASS dtoc5 exact OSIL objective:',n,'quadratic terms; stored rational agrees')
for suffix in ('06','09','12','18','24'):
    name='waterno2_'+suffix;m=model(name);names=[e.attrib['name'] for e in m.find('variables')]
    v=json.loads((BASE/f'publication/primal/water-ann-kan/points/{name}.exact.json').read_text())
    obj=m.find('objectives/obj');f=Q(obj.attrib.get('constant','0'))
    for c in obj:f+=Q(c.text)*Q(v['x'][names[int(c.attrib['idx'])]])
    for nonlinear in m.findall('nonlinearExpressions/nl'):assert nonlinear.attrib['idx']!='-1'
    for q in m.findall('quadraticCoefficients/qTerm'):assert q.attrib['idx']!='-1'
    assert f==Q(v['objective'])
    print('PASS',name,'exact OSIL objective:',f)
