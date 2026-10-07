"""Independent exact recomputation of objectives that are cheap to evaluate:
dtoc5 (quadratic objective at the exact decimal point) and waterno2_* (linear
objective = sum of cost variables, which are rational). Reads only."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import gzip, json, re, os
from fractions import Fraction as Q
R = (_PUBLIC_REPO + '/research-20260929')
OS = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
def varnames(s):
    vs = s[s.find('<variables'):s.find('</variables>')]
    return re.findall(r'<var [^>]*name="([^"]+)"', vs)
# dtoc5
s = open(OS+'dtoc5.osil').read()
names = varnames(s)
ob = re.search(r'<obj [^>]*?(/>|>)', s).group(0); print('dtoc5 obj tag', ob)
assert 'nonlinearExpressions' not in s or 'idx="-1"' not in s[s.find('<nonlinearExpressions'):]
x = {}
for line in gzip.open(R+'/publication/primal/dtoc5-lukvle10/points/dtoc5_point.txt.gz','rt'):
    if line.startswith('#') or not line.strip(): continue
    k, v = line.split(); x[k] = Q(v)
f = Q(0)
qs = s[s.find('<quadraticCoefficients'):s.find('</quadraticCoefficients>')]
nq = 0
for m in re.finditer(r'<qTerm idx="-1" idxOne="(\d+)" idxTwo="(\d+)" coef="([^"]+)"/>', qs):
    i, j, c = int(m[1]), int(m[2]), Q(m[3]); f += c*x[names[i]]*x[names[j]]; nq += 1
print('dtoc5 objective qterms', nq, 'missing vars', [n for n in names if n not in x][:5])
fs = Q(open(R+'/publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt').read().strip())
print('dtoc5 own objective == stored exact rational:', f == fs)
print('dtoc5 f =', f'{float(f):.17g}', 'num/den digits', len(str(f.numerator)), len(str(f.denominator)))
open(R+'/publication/reviews/minor-fixes-review-r2/scratch/dtoc5_f.txt','w').write(f'{f.numerator}/{f.denominator}\n')
# water
for n in ('06','09','12','18','24'):
    s = open(OS+f'waterno2_{n}.osil').read(); names = varnames(s)
    ob = s[s.find('<objectives'):s.find('</objectives>')]
    const = re.search(r'constant="([^"]+)"', ob.split('>')[0])
    v = json.load(open(R+f'/publication/primal/water-ann-kan/points/waterno2_{n}.exact.json'))
    f = Q(const[1]) if const else Q(0)
    for m in re.finditer(r'<coef idx="(\d+)">([^<]+)</coef>', ob):
        val = v['x'][names[int(m[1])]]
        assert isinstance(val, str), (n, names[int(m[1])], val)
        f += Q(m[2])*Q(val)
    # nonlinear objective parts?
    nl = s[s.find('<nonlinearExpressions'):] if '<nonlinearExpressions' in s else ''
    qn = s[s.find('<quadraticCoefficients'):s.find('</quadraticCoefficients>')] if '<quadraticCoefficients' in s else ''
    assert 'idx="-1"' not in nl and 'idx="-1"' not in qn
    print(f'waterno2_{n}: own objective == stored:', f == Q(v['objective']), f'{float(f):.15g}')
