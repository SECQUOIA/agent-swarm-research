from fractions import Fraction as F
import osilx, osilmini
import xml.etree.ElementTree as ET
NS = '{os.optimizationservices.org}'
for T in [6, 9, 12, 18, 24]:
    p = f'waterno2_{T:02d}.osil'
    a = osilx.read(p); b = osilmini.read(p)
    ok = True
    for j, v in enumerate(b['vars']):
        la = None if osilx.isinf(a['lb'][j]) else F(a['lb'][j]); ua = None if osilx.isinf(a['ub'][j]) else F(a['ub'][j])
        if (la, ua) != (v['lb'], v['ub']) or a['vt'][j] != v['type'] or a['names'][j] != v['name']: ok = False; print('var', j)
    for i, c in enumerate(b['cons']):
        ca = a['cons'][i]
        la = None if osilx.isinf(ca['lb']) else F(ca['lb']); ua = None if osilx.isinf(ca['ub']) else F(ca['ub'])
        if (la, ua) != (c['lb'], c['ub']) or ca['constant'] != '0' or ca['name'] != c['name']: ok = False; print('con', i)
        if {j: F(s) for j, s in ca['lin'].items()} != {j: v for j, v in b['rows'][i].items() if v != 0}: ok = False; print('lin', i)
    # quadratic and nonlinear: compare against raw XML independently
    root = ET.parse(p).getroot(); d = root.find(NS + 'instanceData')
    q = {}
    for t in d.find(NS + 'quadraticCoefficients').findall(NS + 'qTerm'):
        q.setdefault(int(t.get('idx')), []).append((int(t.get('idxOne')), int(t.get('idxTwo')), F(t.get('coef'))))
    for i, ca in enumerate(a['cons']):
        if sorted((x, y, F(c)) for x, y, c in ca['quad']) != sorted(q.get(i, [])): ok = False; print('quad', i)
    nl = {int(e.get('idx')): e for e in d.find(NS + 'nonlinearExpressions').findall(NS + 'nl')}
    for i, ca in enumerate(a['cons']):
        if i in nl:
            pw = nl[i].find(NS + 'power'); v = int(pw.find(NS + 'variable').get('idx')); e = pw.find(NS + 'number').get('value')
            if ca['nl'] != ('power', ('var', v, '1'), ('num', e)): ok = False; print('nl', i, ca['nl'])
        elif ca['nl'] is not None: ok = False; print('nl extra', i)
    objok = {j: F(s) for j, s in a['obj']['lin'].items()} == b['obj'] and a['obj']['constant'] == '0' and not a['obj']['quad'] and a['obj']['nl'] is None
    print(T, 'osilx agrees with independent parse:', ok, 'objective:', objok, 'rows', len(b['cons']), 'vars', len(b['vars']))
