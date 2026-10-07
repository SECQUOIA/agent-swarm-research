"""Critic: own regex/tokenizer parser for the QPLIB camshape .gms copies; template match; constants;
copy optimum via Theorem 1 + Lemma 3 hypotheses (C1-C5) and directed-rounding enclosure; exact row
evaluation of the copy envelope for n=100/200; evaluation of QPLIB .sol reference points."""
import re, sys, json
from fractions import Fraction as Fr
sys.set_int_max_str_digits(0)
sys.path.insert(0, '/tmp/camcrit')
from mine import enclosure, envelope_exact, digits

def parse_gms(path):
    s = open(path).read()
    body = s[s.find('Equations'):]
    eqs = {}
    for m in re.finditer(r'\n(e\d+)\.\.(.*?)=([ELG])=\s*([-0-9.eE+]+)\s*;', body, re.S):
        name, expr, sense, rhs = m.group(1), m.group(2), m.group(3), Fr(m.group(4))
        expr = re.sub(r'\s+', '', expr)
        # remove grouping parentheses of the form (-x3*x2), keep sqr(...)
        expr = re.sub(r'(?<!sqr)\((-?[\w.*]+)\)', r'\1', expr)
        terms = re.findall(r'([+-]?)([0-9.eE]+\*)?((?:sqr\(\w+\))|(?:\w+(?:\*\w+)?))', expr)
        rebuilt = ''.join(a + (b or '') + c for a, b, c in terms)
        assert rebuilt.lstrip('+') == expr.lstrip('+'), (name, expr, rebuilt)
        lin, quad = {}, {}
        for sg, co, v in terms:
            k = Fr(co[:-1]) if co else Fr(1)
            if sg == '-': k = -k
            if v.startswith('sqr('):
                x = v[4:-1]; key = (x, x); quad[key] = quad.get(key, 0) + k
            elif '*' in v:
                a, b = sorted(v.split('*')); quad[(a, b)] = quad.get((a, b), 0) + k
            else:
                lin[v] = lin.get(v, 0) + k
        eqs[name] = (lin, quad, sense, rhs)
    lo, up = {}, {}
    for v, a, val in re.findall(r'(\w+)\.(lo|up|fx)\s*=\s*([-0-9.eE+]+)\s*;', s):
        if a in ('lo', 'fx'): lo[v] = Fr(val)
        if a in ('up', 'fx'): up[v] = Fr(val)
    assert 'Positive Variables' not in s and 'Binary' not in s and 'Integer' not in s
    return eqs, lo, up

def to_model(path, n):
    eqs, lo, up = parse_gms(path)
    assert len(eqs) == 2 * n + 1, len(eqs)
    r = [None] + [f'x{j + 1}' for j in range(1, n + 1)]      # r_j = x_{j+1}
    d = [None] + [f'x{n + 1 + i}' for i in range(1, n)]       # d_i = x_{n+1+i}
    lin, quad, sense, rhs = eqs['e1']
    assert sense == 'E' and rhs == 0 and quad == {} and lin['objvar'] == -1
    c0s = {lin[r[j]] for j in range(1, n + 1)}; assert len(c0s) == 1 and len(lin) == n + 1
    c0 = -c0s.pop()
    for i in range(1, n):
        assert eqs[f'e{i + 1}'] == ({r[i]: 1, r[i + 1]: -1, d[i]: 1}, {}, 'E', 0), i
    lin, quad, sense, rhs = eqs[f'e{n + 1}']   # G_1
    c = lin[r[2]]
    assert (lin, quad, sense, rhs) == ({r[1]: -1, r[2]: c}, {tuple(sorted((r[1], r[2]))): -1}, 'L', 0)
    lin, quad, sense, rhs = eqs[f'e{n + 2}']   # G_n
    c2 = lin[r[n - 1]]
    assert (lin, quad, sense, rhs) == ({r[n - 1]: c2, r[n]: -2}, {tuple(sorted((r[n - 1], r[n]))): -1}, 'L', 0)
    lin, quad, sense, rhs = eqs[f'e{n + 3}']   # H
    cH = quad[(r[n], r[n])]
    assert (lin, quad, sense, rhs) == ({r[n]: -4}, {(r[n], r[n]): cH}, 'L', 0)
    for j in range(2, n):
        lin, quad, sense, rhs = eqs[f'e{n + 2 + j}']
        want = {tuple(sorted((r[j - 1], r[j + 1]))): c, tuple(sorted((r[j - 1], r[j]))): -1, tuple(sorted((r[j], r[j + 1]))): -1}
        assert (lin, quad, sense, rhs) == ({}, want, 'L', 0), j
    assert lo.get(r[1]) == 1 and lo.get(r[n]) is not None and up[r[n]] == 2
    ub1 = up[r[1]]; lbn = lo[r[n]]
    for j in range(2, n): assert lo[r[j]] == 1 and up[r[j]] == 2
    assert d[1] not in lo and d[1] not in up and 'objvar' not in lo and 'objvar' not in up
    al = up[d[2]]
    for i in range(2, n): assert lo[d[i]] == -al and up[d[i]] == al
    assert set(lo) == set(r[1:]) | set(d[2:]) and set(up) == set(r[1:]) | set(d[2:])
    return dict(c0=c0, c=c, c2=c2, cH=cH, ub1=ub1, lbn=lbn, alpha=al), r, d

def lemma3_hyp(K, n):
    U, S, B, E = (None,) * 4
    c, ub1, al = K['c'], K['ub1'], K['alpha']
    U = [Fr(1), c]
    while len(U) < n: U.append(c * U[-1] - U[-2])
    Sx = [Fr(1), 1 / ub1]
    while len(Sx) < n + 1: Sx.append(c * Sx[-1] - Sx[-2])
    return dict(C1=all(u >= 0 for u in U), C2=all(0 < s <= 1 for s in Sx[1:]), C4=ub1 <= 1 + al,
                C5=K['c0'] > 0 and 1 <= ub1 <= 2 and 0 < c < 2 and K['c2'] <= 4 and 0 < K['lbn'] <= 2 and K['cH'] <= 2)

if __name__ == '__main__':
    VN = {100: Fr('-4.2841471217467438034410071'), 200: Fr('-4.2785002329927222918988259'), 400: Fr('-4.2756884789255432151508246'), 800: Fr('-4.2742741419541941011244678')}
    for name, n in (('QPLIB_2738', 100), ('QPLIB_2480', 200), ('QPLIB_2703', 400), ('QPLIB_3177', 800)):
        K, r, d = to_model(f'/tmp/camcrit/q/{name}.gms', n)
        H = lemma3_hyp(K, n)
        slo, shi, Elo, Ehi = enclosure(K, n)
        C3 = (Elo[n] == Ehi[n] == 2 * 10**120) and (Elo[n - 1] == Ehi[n - 1] == 2 * 10**120)
        vlo = -K['c0'] * shi; vhi = -K['c0'] * slo
        rec = dict(name=name, consts={k: str(v) for k, v in K.items()}, hyp=H, C3=C3,
                   opt_floor16=digits(vlo, 16), opt_ceil16=digits(vhi, 16, True), minus_vn=float(vlo - VN[n]))
        # QPLIB reference point
        if name.startswith('QPLIB'):
            vals = {}
            for line in open(f'/tmp/camcrit/q/{name}.sol'):
                p = line.split()
                if len(p) == 2: vals[p[0]] = Fr(p[1])
            missing = [v for v in r[1:] + d[1:] if v not in vals]
            x = {v: vals.get(v, Fr(0)) for v in r[1:] + d[1:]}
            eqs, lo, up = parse_gms(f'/tmp/camcrit/q/{name}.gms')
            worst = (Fr(0), None)
            for en, (lin, quad, sense, rhs) in eqs.items():
                if en == 'e1': continue
                val = sum(k * x[v] for v, k in lin.items()) + sum(k * x[a] * x[b] for (a, b), k in quad.items()) - rhs
                vio = max(val, 0) if sense == 'L' else abs(val)
                if vio > worst[0]: worst = (vio, en)
            bv = max([lo[v] - x[v] for v in lo] + [x[v] - up[v] for v in up] + [Fr(0)])
            obj = -K['c0'] * sum(x[v] for v in r[1:])
            rec.update(sol_obj=float(obj), sol_minus_copyopt=float(obj - vlo), sol_row_viol=float(worst[0]), sol_row=worst[1],
                       sol_bnd_viol=float(bv), missing_r=[v for v in missing if v in r], n_missing_d=len([v for v in missing if v in d]),
                       objvar_listed=float(vals['objvar']))
        print(json.dumps(rec), flush=True)
