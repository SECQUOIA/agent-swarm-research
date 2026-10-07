"""Reviewer r2: structural comparison of ann_cumene_tanh and ann_cumene_exp OSIL (exact strings/rationals)."""
import xml.etree.ElementTree as ET
from fractions import Fraction as F
import os
D = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
ns = {'o': 'os.optimizationservices.org'}
def load(n):
    r = ET.parse(D + n + '.osil').getroot()
    return r
A, B = load('ann_cumene_tanh'), load('ann_cumene_exp')
def strip(e): return ET.tostring(e)
for tag in ['variables', 'objectives', 'linearConstraintCoefficients', 'quadraticCoefficients']:
    a = A.find('.//o:' + tag, ns); b = B.find('.//o:' + tag, ns)
    print(tag, 'identical' if (a is None and b is None) or (a is not None and b is not None and strip(a) == strip(b)) else 'DIFFERENT')
ca = A.findall('.//o:constraints/o:con', ns); cb = B.findall('.//o:constraints/o:con', ns)
print('rows', len(ca), len(cb))
na = {int(e.get('idx')): e for e in A.findall('.//o:nonlinearExpressions/o:nl', ns)}
nb = {int(e.get('idx')): e for e in B.findall('.//o:nonlinearExpressions/o:nl', ns)}
print('nl rows', len(na), len(nb), set(na) == set(nb))
def bnd(c, k):
    v = c.get(k); return None if v is None else F(v)
shift_ok = 0; same_ok = 0; bad = []
for i, (x, y) in enumerate(zip(ca, cb)):
    if i in na:
        ea, eb = na[i][0], nb[i][0]
        # tanh model: negate(tanh(v)); exp model: divide(2, plus(exp(times(2,v)),1)) in some form
        ta = ET.tostring(ea).decode(); tb = ET.tostring(eb).decode()
        ok_a = ea.tag.endswith('negate') and ea[0].tag.endswith('tanh')
        v_a = ET.tostring(ea[0][0])
        # find inner v in exp model by locating the exp node's argument and check it is times(2, v)
        exps = [n for n in eb.iter() if n.tag.endswith('}exp')]
        ok_b = len(exps) == 1
        inner = exps[0][0] if ok_b else None
        # every tanh argument is a single <variable idx=j> (coef 1); exp argument must be <variable idx=j coef=2>
        va = ea[0][0]
        ok_v = (va.tag.endswith('variable') and len(list(va)) == 0 and F(va.get('coef', '1')) == 1
                and inner is not None and inner.tag.endswith('variable') and len(list(inner)) == 0
                and inner.get('idx') == va.get('idx') and F(inner.get('coef', '1')) == 2)
        # outer form of exp model: divide(number 2, plus(exp(...), number 1))
        ok_outer = eb.tag.endswith('divide') and eb[0].tag.endswith('number') and F(eb[0].get('value')) == 2 and (eb[1].tag.endswith('plus') or eb[1].tag.endswith('sum')) and len(list(eb[1])) == 2 and eb[1][0].tag.endswith('exp') and eb[1][1].tag.endswith('number') and F(eb[1][1].get('value')) == 1
        ok_bnd = all((bnd(x, k) is None and bnd(y, k) is None) or (bnd(x, k) is not None and bnd(y, k) == bnd(x, k) + 1) for k in ('lb', 'ub'))
        if ok_a and ok_b and ok_v and ok_outer and ok_bnd: shift_ok += 1
        else: bad.append((i, ok_a, ok_b, ok_v, ok_outer, ok_bnd, tb[:200]))
    else:
        if ET.tostring(x) == ET.tostring(y): same_ok += 1
        else: bad.append((i, 'linear row differs'))
print('nonlinear rows -tanh(v) vs 2/(exp(2v)+1) with bounds +1:', shift_ok, '; other rows identical:', same_ok, '; bad:', len(bad))
for b in bad[:3]: print(b)
