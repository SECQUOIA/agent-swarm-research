"""Critic check: polynomials used by vmodel (vbb/vbb2 line) and wmodel (rbb line) vs an independent parse of the GAMS text."""
import re, sys
from fractions import Fraction as F
import osilx, vmodel, wmodel

def gams(path):
    g = open(path).read()
    eqs = {}
    for name, body in re.findall(r'^(e\d+)\.\.(.*?);', g, re.S | re.M):
        body = ' '.join(body.split())
        m = re.match(r'(.*)=([EGL])=\s*([-+0-9.eE]+)$', body)
        lhs, sense, rhs = m.group(1), m.group(2), F(m.group(3))
        lhs = lhs.replace('- ', '-').replace('+ ', '+')
        poly = {}
        for term in re.findall(r'[-+]?[^-+\s][^\s]*', lhs):
            sign = -1 if term.startswith('-') else 1
            term = term.lstrip('+-'); coef = F(sign); facs = []
            for f in term.split('*'):
                if re.fullmatch(r'[0-9.]+(e[-+]?\d+)?', f): coef *= F(f)
                elif f.startswith('sqr('): facs += [f[4:-1]] * 2
                elif f.startswith('POWER('):
                    v, p = f[6:-1].split(','); facs += [v] * int(p)
                else: facs.append(f)
            key = tuple(sorted(facs)); poly[key] = poly.get(key, 0) + coef
        eqs[name] = ({k: v for k, v in poly.items() if v != 0}, sense, rhs)
    return eqs

for T in [6, 9, 12, 18, 24]:
    eqs = gams(f'waterno2_{T:02d}.gms')
    I = vmodel.instance(T); m = I['m']; names = m['names']
    W = wmodel.load(T)
    nv = nw = 0
    for i, c in enumerate(m['cons']):
        gp, sense, rhs = eqs[c['name']]
        vp = {tuple(sorted(names[j] for j in k)): a for k, a in vmodel.poly(c).items()}
        wp = {tuple(sorted(W['names'][j] for j in k)): F(a) for k, a in W['rows'][i]['poly'].items()}
        wp = {k: a for k, a in wp.items() if a != 0}
        lo = rhs if sense in 'EG' else None; hi = rhs if sense in 'EL' else None
        clo = None if c['lb'].upper() == '-INF' else F(c['lb']); chi = None if c['ub'].upper() in ('INF', '+INF') else F(c['ub'])
        if vp != gp or (clo, chi) != (lo, hi): nv += 1
        wlo = None if W['rows'][i]['lb'].upper() == '-INF' else F(W['rows'][i]['lb']); whi = None if W['rows'][i]['ub'].upper() in ('INF', '+INF') else F(W['rows'][i]['ub'])
        if wp != gp or (wlo, whi) != (lo, hi) or W['rows'][i]['name'] != c['name']: nw += 1
    print(T, 'rows', len(m['cons']), 'vmodel rows differing from GAMS', nv, 'wmodel rows differing from GAMS', nw, 'periods', len(I['per_vars']), 'links', sum(len(l) for l in I['links']))
