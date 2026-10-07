"""Small independent display/evidence checks; never construct points or solve models."""
import collections
import hashlib
import json
import re
from fractions import Fraction as Q
from html.parser import HTMLParser
from pathlib import Path

W = Path(__file__).resolve().parent
P = W.parents[1]
R = P.parent


def read(path):
    return json.loads(path.read_text())


def interval(text):
    a, b = re.search(r'\[([^,]+), ([^\]]+)\]', text).groups()
    return Q(a), Q(b)


def display(name, shown, lo, hi, replacement=None, sense='min'):
    s = Q(shown)
    valid = s >= hi if sense == 'min' else s <= lo
    print(name, 'primal', shown, 'valid:', valid, 'display - upper:', float(s-hi))
    if replacement:
        assert not valid
        t = Q(replacement)
        assert t >= hi if sense == 'min' else t <= lo
        print('  correction:', shown, '->', replacement)
    else:
        assert valid


summary = (R/'open-instances-summary.md').read_text().replace('−','-')
rows = {v[0]: v for line in summary.splitlines() if line.startswith('| ')
        for v in [[x.strip() for x in line.strip('|').split('|')]]}

# The printed h2 has a last-digit uncertainty. Bracket it, rather than
# treating a nearest decimal as the certified real number itself.
ver = {v['name']: v for v in read(R/'reviews/open-instances-verification/logs/lnts_verify.json')}
for n in (50, 100, 200, 400):
    name = f'lnts{n}'
    lo, hi = map(Q, read(P/f'primal/lnts/points/{name}_point.json')['objective_enclosure'])
    display(name, rows[name][3], lo, hi, '0.5545954011670' if n == 100 else None)
    c = ver[name]['cert_1e-12']
    err = Q(1, 2*10**len(c['h2'].split('.')[1]))
    lower, upper = n*(Q(c['h2'])-err), n*(Q(c['h2'])+err)
    assert Q(rows[name][2]) <= lower
    safe = {50:'0.5546687649381242',100:'0.5545954011663565',
            200:'0.5545770161025290',400:'0.5545724137001325'}[n]
    assert Q(safe) <= lower
    assert hi-lower <= Q('5.55e-13')
    assert (hi-Q(safe))/Q(safe) <= Q('1.01e-12')
    assert hi-Q(rows[name][2]) <= Q('6.12e-13')
    print(name, 'summary dual valid; safe verifier display', safe,
          'old verifier display above h2 bracket:', Q(c['bound']) > upper,
          'gap to summary dual:', float(hi-Q(rows[name][2])))
    print(name,'relative gap to safe verifier display:',float((hi-Q(safe))/Q(safe)))

f = Q((P/'primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt').read_text().strip())
display('dtoc5', rows['dtoc5'][3], f, f, '5.389672119181141')
assert Q(rows['dtoc5'][2]) <= Q('5.38967211918114046742396472386') < f
assert f-Q(rows['dtoc5'][2]) < Q('1e-14')
lo, hi = Q('352.2380254064956226308712710293664647979978'), Q('352.2380254064956226308712710293664647979979')
display('lukvle10', rows['lukvle10'][3], lo, hi)
assert Q(rows['lukvle10'][2]) <= Q(float(rows['lukvle10'][2]))

for n in (50, 100, 200, 400):
    hi = Q(read(P/f'primal/chain/points/chain{n}_box.json')['objective_enclosure_decimal'][1])
    L = Q(read(R/f'open-instances-wave2/cops/logs/chain{n}_bound.json')['bnb']['bound'])
    safe = {50:'5.0722614939828627',100:'5.0697846107387505',
            200:'5.0689173417931616',400:'5.068621694604009'}[n]
    assert Q(safe) <= L
    assert hi-Q(safe) <= Q('1.01e-14')
    print(f'chain{n}', 'gap exact dual:', float(hi-L), 'safe display:', float(hi-Q(safe)))

for name, correction in [('powerflow0030p',None),('powerflow0039p','41869.0515113203'),
                         ('powerflow0039r','41869.0515113210')]:
    text = (P/f'primal/powerflow/logs/certify.{name}.log').read_text()
    lo, hi = interval(text.split('objective enclosure:')[1])
    display(name, rows[name][3], lo, hi, correction)
    if name.endswith(('0039p','0039r')):
        L = Q(read(R/f'open-instances-wave3/powerflow/ext/logs/{name}.bb3t.json')['LB_exact'])
        assert Q(rows[name][2]) <= L
        print(name, 'summary dual valid against exact LB_exact')
    else:
        L = Q(read(R/'open-instances-wave3/logs/powerflow0030p.sdpcert.json')['bound_exact'])
        assert Q(rows[name][2]) <= L
        print(name, 'summary dual valid against exact bound_exact')

for n, shown in [('06','282.888'),('09','914.012'),('12','2233.821'),('18','5023.983'),('24','6963.795')]:
    name = f'waterno2_{n}'
    f = Q(read(P/f'primal/water-ann-kan/points/{name}.exact.json')['objective'])
    correction = {'06':'282.888038','09':None,'12':'2233.821346','18':None,'24':'6963.795181'}[n]
    display(name, shown, f, f, correction)
    d = Q(read(R/'open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json')['bound_exact']) if n == '06' else Q(read(R/f'open-instances-wave2/waterno2/logs/cert_{n}_w1_impl.json')['certified_bound_exact'])
    displayed_dual = re.sub(r'\*', '', rows[name][2]).split(' ')[0]
    assert Q(displayed_dual) <= d
    percent = {'06':'1.674','09':'10.82','12':'6.90','18':'4.87','24':'5.90'}[n]
    assert Q(percent)/100 >= (f-d)/abs(d)
    print(name, 'gap percent:', float(100*(f-d)/abs(d)), '<=', percent)

v = read(P/'primal/water-ann-kan/points/ann_cumene_tanh.point.json')
display('ann_cumene_tanh', '-3379.9824', Q(v['objective_lo']), Q(v['objective_hi']), '-3379.9823940')
assert Q('-3386.5403') <= Q(v['dual_bound'])

# Other summary entries: compare stored objective enclosures/point definitions.
for name in ('ex6_2_5','ex6_2_7'):
    v = read(R/f'reviews/wave2-small-verification/logs/{name}_bound.json')
    # These stored decimal endpoints are nearest prints, so bracket their
    # last digit. That uncertainty is much smaller than the display error.
    a, b = map(Q, v['own_primal_objective_enclosure'])
    eps = Q(1, 2*10**len(v['own_primal_objective_enclosure'][0].split('.')[1]))
    display(name, rows[name][3], a-eps, b+eps, '-70.752077833447705' if name.endswith('5') else None)
    assert Q(rows[name][2]) <= Q(v['dual_bound'])
v = read(R/'reviews/bangbang-verification/logs/primal_check.json')['rigorous_primal']
a, b = interval(v['J_upper'])
display('optcdeg2', '293.87607509587509328', a, b)
assert Q(rows['optcdeg2'][2].split(' ')[0]) <= Q(read(R/'reviews/bangbang-verification/logs/qcal_exact.json')['bound_str'])/10**20
display('hvycrash', rows['hvycrash'][3], Q('-0.2185'), Q('-0.2185'))
v = read(R/'reviews/wave2-small-verification/logs/pricing050.json')
s = v['own_primal']['objective_20']; eps = Q(1,2*10**len(s.split('.')[1]))
display('pricing050 (max)', rows['pricing050 (max)'][3], Q(s)-eps, Q(s)+eps, sense='max')
assert Q(rows['pricing050 (max)'][2].split(' ')[0]) >= Q(v['certificate']['upper_bound'])
muR = Q(v['multipliers']['e5'])*Q('-788')+Q(v['multipliers']['e6'])*Q('-984')
saved_sum = Q(v['certificate']['sum_minF_certified'])
sum_error = Q(1,2*10**len(v['certificate']['sum_minF_certified'].split('.')[1]))
assert Q(rows['pricing050 (max)'][2].split(' ')[0]) >= muR-saved_sum+sum_error
print('pricing050 dual upper display valid against multiplier/rhs and bracketed saved sum')
text = (R/'reviews/pindyck-review-checks/logs/primal_check.txt').read_text()
s = re.search(r'objective \(min form\) = (\S+)', text)[1]
eps = Q(1,2*10**len(s.split('.')[1]))
display('pindyck', rows['pindyck'][3], Q(s)-eps, Q(s)+eps)
for name in ('eg_int_s','eg_disc_s','eg_disc2_s'):
    pt = dict(line.split() for line in (R/f'open-instances-wave3/eg/retry/sol/{name}.retry.sol').read_text().splitlines())
    f = Q(pt['objvar'])
    correction = {'eg_int_s':'6.4531031593842275','eg_disc_s':'5.7605396164535107','eg_disc2_s':None}[name]
    display(name, rows[name][3].split(' ')[0], f, f, correction)
    # The verifier takes the decimal CLI string directly as a Fraction;
    # these are decimal targets, not repr() displays of binary64 bounds.
    logname = {'eg_int_s':'verify_int.log','eg_disc_s':'verify_disc_p0.log',
               'eg_disc2_s':'verify_disc2_p1.log'}[name]
    log = (R/f'reviews/eg-retry-review-checks/logs/{logname}').read_text()
    assert rows[name][2] in log
    print(name, 'dual matches independently verified exact decimal target')
print('camshape primal cells name the exact attained optimum; etamac names an exactly feasible point;')
print('chain/catmix and KAN primal cells are descriptions/ranges, not numeric primal bounds.')
for v in read(R/'reviews/open-instances-verification/logs/camshape_verify.json'):
    name = 'camshape'+str(v['n'])
    s = rows[name][2].split(' ')[0]
    b = Q(v['bound']); error = Q(1,2*10**len(v['bound'].split('.')[1]))
    assert Q(s) <= b-error
    print(name,'dual display valid against bracketed saved optimum')
v = read(R/'reviews/wave2-small-verification/logs/etamac.json')
assert Q(rows['etamac'][2]) <= Q(v['bound']['dual_bound'])
assert 'exactly feasible point' in rows['etamac'][3]
assert 'claimed bound -1170.4862854360886163932 <= own bound -UB: True' in (R/'reviews/pindyck-review-checks/logs/final_bound.log').read_text()
assert Q(rows['hvycrash'][2].split(' ')[0]) == Q('-0.2185')
print('etamac, pindyck and hvycrash dual displays match or lie below saved certificates')

# Independent saved-page parser, including displayed-entry multiplicity.
class Values(HTMLParser):
    def __init__(self):
        super().__init__(); self.depth = 0; self.buf = ''; self.values = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'div' and a.get('title','').startswith(('Added on','Last updated:')):
            self.depth = 1; self.buf = ''
        elif self.depth:
            self.depth += 1
    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= 1
            if not self.depth:
                self.values.append(self.buf.split()[0])
    def handle_data(self, data):
        if self.depth: self.buf += data

values = []
for path in sorted((R/'bound-audit/pages').glob('*.html')):
    if path.name == 'instances.html': continue
    parser = Values(); parser.feed(path.read_text()); values += parser.values
numeric = [s.replace('−','-') for s in values if re.fullmatch(r'[+−-]?\d*\.\d*',s)]
A, B, C = [], [], []
for s in numeric:
    digits = s.lstrip('+-').replace('.','').lstrip('0')
    if len(digits.rstrip('0')) > 10:
        B.append(s)
        if s.split('.')[1]: A.append(s)
    if len(digits) > 10: C.append(s)
assert (len(numeric),len(A),len(B),len(C),len(set(A))) == (13847,35,38,46,18)
assert max(len(s.split('.')[1]) for s in numeric) == 8
print('audit displayed entries: 35/38/46; first group 18 distinct strings; max decimals 8')

def floor_binds(s):
    q = abs(Q(s))
    if not q: return False
    exponent = 0
    while q >= Q(10)**(exponent+1): exponent += 1
    while q < Q(10)**exponent: exponent -= 1
    places = len(s.split('.')[1]) if '.' in s else 0
    return Q(10)**(exponent-9) > Q(10)**(-places)

screen = read(R/'bound-audit/screen.json')
affected = [v for v in screen['pairs'] if floor_binds(v['d_listed'])]
ties = [v for v in screen['ties'] if floor_binds(v['d_listed'])]
assert not affected and len(screen['pairs']) == 158
assert len(ties) == 17 and {v['name'] for v in ties} == {'fac1','fac2','waternd_fosspoly0'}
print('audit slack floor: 0/158 screened pairs; 17 tie pairs on 3 instances')

# Own statement parser for upper/lower bounds, independent of compare.py.
src = P/'literature/control/sources/qplib/camshape_copies'
def bounds(path, shift):
    out = {}
    for statement in path.read_text().split(';'):
        m = re.search(r'(x\d+)\.(lo|up|fx)\s*=\s*([-+\d.eE]+)\s*$',statement)
        if not m: continue
        name, side, val = m.groups(); name = 'x'+str(int(name[1:])-shift)
        for s in (('lo','up') if side == 'fx' else (side,)): out[name,s] = Q(val)
    return out
for n,k in [(100,2738),(200,2480),(400,2703),(800,3177)]:
    a,b = bounds(src/f'camshape{n}.gms',0),bounds(src/f'QPLIB_{k}.gms',1)
    assert a.keys() == b.keys() and len(a) == 4*n-4
    key = max(a, key=lambda key: abs(a[key]-b[key])/max(abs(a[key]),1))
    delta = abs(a[key]-b[key])/max(abs(a[key]),1)
    assert delta < Q('4.708e-10')
    print('camshape',n,'bound entries',len(a),'max difference',float(delta),'at',key)

point = P/'literature/control/sources/qplib/QPLIB_8585.sol'
assert hashlib.sha256(point.read_bytes()).hexdigest() == '9d9f5c4fbfc73aa6bfa3ae94ae7a1d44832a5fd7a30927a7941e2e8dcdf455cd'
coordinates = [Q(v) for name,v in (line.split() for line in point.read_text().splitlines()) if name.startswith('x')]
assert len(coordinates) == 99998 and min(coordinates) > 0 and max(coordinates) < 100
log = (P/'literature/control/sources/mittelmann_cnconv/logs/QPLIB_8585.mnt').read_text()
assert '99983' in log and '99997' in log
assert 99997-99983 == 14
print('MINOTAUR defaults: 14 extra finite lower bounds; reference min/max',float(min(coordinates)),float(max(coordinates)))

# Verify the review's lnts reproducibility evidence without a construction rerun.
for n in (50,100,200,400):
    a = P/f'primal/lnts/points/lnts{n}_point.json'
    b = P/f'reviews/minor-fixes-review-r1/scratch-A/lnts_repro/points/lnts{n}_point.json'
    assert a.read_bytes() == b.read_bytes()
print('all four lnts points equal the reviewer scratch rerun byte for byte')

import numpy as np
total = 0; counts = collections.Counter(); processed = {}
for path in sorted((P/'eg-recheck/res').glob('p*_c*.npz')):
    with np.load(path) as v:
        total += len(v['sel']); assert v['ok'].all()
        for h in (1,3,5): counts[h] += int(((v['mg'] == np.inf) & (v['how'] == h)).sum())
        part = path.name.split('_')[0]
        processed.setdefault(part,set()).add(int(v['n_proc']))
assert all(len(v) == 1 for v in processed.values())
assert (total,counts[1],counts[3],counts[5],sum(next(iter(v)) for v in processed.values())) == (1114361,85685,373,12176,1152830)
print('eg own recount: 1114361 leaves, 1152830 processed boxes; 85685/373/12176 exclusions')

for k,expected in [(2738,'5.9096'),(2480,'13.3380'),(2703,'20.8425')]:
    text = (P/f'literature/control/sources/mittelmann_cnconv/logs/QPLIB_{k}.mnt').read_text()
    value = re.search(r'gap percentage = (\S+)',text)[1]
    assert Q(value) == Q(expected)
    print('MINOTAUR', k, 'PRINTED gap percentage',value)

text = (P/'literature/network/sources/mueller2020_arxiv1903.05521.txt').read_text()
for page,needles in [(69,['powerflow0030r','powerflow0039r']),(72,['waterno2 24'])]:
    lines = text.split('\f')[page-1].splitlines()
    for needle in needles:
        line = next(s for s in lines if needle in s)
        assert line.count('1800.0') == 3
        print('Müller PDF page',page,line)
text = (P/'literature/network/sources/goss2026_arxiv2603.16505.txt').read_text()
assert 'Adrian Gö' in text[:1000]
print('Göß front matter: one author, Adrian Göß')

# Tiny exact-model comparisons and the first recorded seed-11 witness loss.
assert Q('.2')+Q('.614125') > Q(187,270)
assert 5*Q('.343') > Q(187,270)
assert Q('.1')+2*Q(8,27) == Q(187,270)
assert Q('.8') < ((Q('.2')+Q('1.337'))/Q('1.6'))**2
text = (P/'scip-bug/logs/dbgsol_pair2236_seed11.log').read_text()
first = next(s for s in text.splitlines() if 'invalid local lower bound implication' in s)
assert '<t_b35>[0] >= 1' in first and 'SCIPBUG' not in text
print('seed 11 first recorded witness loss:',first)
print('exact minima checked: fm336 187/270; tiny2 -1337/1000')

import xml.etree.ElementTree as ET
NS = '{os.optimizationservices.org}'
def array(node, convert):
    out = []
    for el in node:
        x = convert(el.text)
        out.extend(x+i*convert(el.get('incr','0')) for i in range(int(el.get('mult','1'))))
    return out

for name,targets in [('powerflow0030p',['e215']),('powerflow0039p',['e346']),
                     ('powerflow0039r',['e306','e363','e386'])]:
    root = ET.parse(Path.home()/f'.cache/minlplib/minlplib/osil/{name}.osil').getroot()
    vs = root.find('.//'+NS+'variables')
    point = dict(line.split() for line in (R/f'open-instances-wave3/sol/{name}.p1.sol').read_text().splitlines())
    x = [Q(point.get(v.get('name'),'0')) for v in vs]
    cs = list(root.find('.//'+NS+'constraints'))
    lc = root.find('.//'+NS+'linearConstraintCoefficients')
    starts = array(lc.find(NS+'start'),int); cols = array(lc.find(NS+'colIdx'),int)
    vals = array(lc.find(NS+'value'),Q)
    for target in targets:
        i = next(i for i,c in enumerate(cs) if c.get('name') == target); c = cs[i]
        assert not any(int(n.get('idx')) == i for n in root.findall('.//'+NS+'nl'))
        value = Q(c.get('constant','0')) + sum(vals[j]*x[cols[j]] for j in range(starts[i],starts[i+1]))
        value += sum(Q(t.get('coef','1'))*x[int(t.get('idxOne'))]*x[int(t.get('idxTwo'))]
                     for t in root.findall('.//'+NS+'qTerm') if int(t.get('idx')) == i)
        margins = ([Q(c.get('ub'))-value] if c.get('ub') is not None else [value-Q(c.get('lb'))])
        expected = {'e215':Q('4.3e-4'),'e346':Q('1.08e-3'),'e306':Q('2.3e-3'),
                    'e363':Q('6.8e-13'),'e386':Q('2.1e-13')}[target]
        assert abs(margins[0]-expected) < abs(expected)/50
        print(name,target,'exact rational stored-p1 slack',float(margins[0]))
print('PASS: independent rational display, rounding, audit and saved-source checks')
