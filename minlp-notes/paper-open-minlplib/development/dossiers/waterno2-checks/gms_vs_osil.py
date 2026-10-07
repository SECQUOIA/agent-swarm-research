"""Exact comparison of a waterno2 GAMS file (decimal text) with the cached OSIL (dossier check).
usage: python3 gms_vs_osil.py waterno2_TT.gms waterno2_TT.osil"""
import re, sys
from fractions import Fraction as F
import xml.etree.ElementTree as ET
import osilmini
NS = '{os.optimizationservices.org}'
gtxt = open(sys.argv[1]).read()
# --- GAMS variables
decl = {}
for kind, body in re.findall(r'^(Positive Variables|Binary Variables|Variables|Negative Variables|Free Variables)\s+(.*?);', gtxt, re.S | re.M):
    for v in re.split(r'[\s,]+', body.strip()):
        if v: decl[v] = kind
lb, ub = {}, {}
for v, k in decl.items():
    lb[v] = {'Variables': None, 'Free Variables': None, 'Positive Variables': F(0), 'Binary Variables': F(0)}[k]
    ub[v] = F(1) if k == 'Binary Variables' else None
for v, att, val in re.findall(r'(\w+)\.(lo|up|fx)\s*=\s*([-+0-9.eE]+)\s*;', gtxt):
    val = F(val)
    if att in ('lo', 'fx'): lb[v] = val
    if att in ('up', 'fx'): ub[v] = val
# --- GAMS equations
eqs = {}
for name, body in re.findall(r'^(e\d+)\.\.(.*?);', gtxt, re.S | re.M):
    body = ' '.join(body.split())
    m = re.match(r'(.*)=([EGL])=\s*([-+0-9.eE]+)$', body)
    lhs, sense, rhs = m.group(1), m.group(2), F(m.group(3))
    poly = {}
    lhs = lhs.replace('- ', '-').replace('+ ', '+')
    for term in re.findall(r'[-+]?[^-+\s][^\s]*', lhs):
        sign = -1 if term.startswith('-') else 1
        term = term.lstrip('+-')
        coef = F(sign); facs = []
        for f in term.split('*'):
            if re.fullmatch(r'[0-9.]+(e[-+]?\d+)?', f): coef *= F(f)
            elif f.startswith('sqr('): facs += [f[4:-1]] * 2
            elif f.startswith('POWER('):
                v, p = f[6:-1].split(','); facs += [v] * int(p)
            else: facs.append(f)
        key = tuple(sorted(facs))
        poly[key] = poly.get(key, 0) + coef
    eqs[name] = (poly, sense, rhs)
# --- OSIL
m = osilmini.read(sys.argv[2])
names = [v['name'] for v in m['vars']]
root = ET.parse(sys.argv[2]).getroot(); d = root.find(NS + 'instanceData')
opoly = [dict() for _ in m['cons']]
for i, r in enumerate(m['rows']):
    for j, v in r.items(): opoly[i][(names[j],)] = opoly[i].get((names[j],), 0) + v
for q in d.find(NS + 'quadraticCoefficients').findall(NS + 'qTerm'):
    i = int(q.get('idx')); key = tuple(sorted([names[int(q.get('idxOne'))], names[int(q.get('idxTwo'))]]))
    opoly[i][key] = opoly[i].get(key, 0) + F(q.get('coef'))
for nl in d.find(NS + 'nonlinearExpressions').findall(NS + 'nl'):
    i = int(nl.get('idx')); p = nl.find(NS + 'power')
    v = names[int(p.find(NS + 'variable').get('idx'))]; e = int(F(p.find(NS + 'number').get('value')))
    coef = F(p.find(NS + 'variable').get('coef', '1'))
    assert coef == 1
    key = tuple([v] * e); opoly[i][key] = opoly[i].get(key, 0) + 1
diff_rows = 0; diff_bounds = 0; ncmp = 0
for i, c in enumerate(m['cons']):
    gp, sense, rhs = eqs[c['name']]
    gp = {k: v for k, v in gp.items() if v != 0}; op = {k: v for k, v in opoly[i].items() if v != 0}
    lo = rhs if sense in 'EG' else None; hi = rhs if sense in 'EL' else None
    ncmp += 1
    if gp != op or lo != c['lb'] or hi != c['ub']:
        diff_rows += 1
        if diff_rows <= 5: print('row differs', c['name'], sense, rhs, c['lb'], c['ub'], {k: (gp.get(k), op.get(k)) for k in set(gp) | set(op) if gp.get(k) != op.get(k)})
for j, v in enumerate(m['vars']):
    n = v['name']
    if (lb[n], ub[n]) != (v['lb'], v['ub']) or (decl[n] == 'Binary Variables') != (v['type'] == 'B'):
        diff_bounds += 1
        if diff_bounds <= 5: print('var differs', n, lb[n], ub[n], v)
# objective: GAMS e1: objvar - sum = 0, minimize objvar
gp, sense, rhs = eqs['e1']
gobj = {k[0]: -v for k, v in gp.items() if k != ('objvar',)}
oobj = {names[j]: v for j, v in m['obj'].items()}
print('rows compared', ncmp, 'rows differing', diff_rows, 'variables differing', diff_bounds,
      'objective identical', gobj == oobj and gp[('objvar',)] == 1 and rhs == 0 and sense == 'E',
      'GAMS vars', len(decl), 'OSIL vars', len(names))
