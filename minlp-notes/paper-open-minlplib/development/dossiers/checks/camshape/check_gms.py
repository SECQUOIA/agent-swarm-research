"""Dossier check (camshape): exact parse of GAMS scalar files (MINLPLib camshape*.gms and the QPLIB copies),
comparison with the OSIL data, and the comparison bound + envelope feasibility for each file.

Own recursive-descent parser for the restricted GAMS expression grammar used in these files
(numbers, variables, + - *, parentheses, sqr()). Everything exact (Fraction). No floating point in decisions.
Usage: python3 check_gms.py file.gms [file.gms ...]
"""
import json
import re
import sys
from fractions import Fraction as Fr

sys.set_int_max_str_digits(0)
from check_exact import certificate, dec, dec_up  # same directory (scratch copy)

TOK = re.compile(r"\s*(?:(\d+\.\d*(?:[eE][-+]?\d+)?|\d+(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(.))")


def tokenize(s):
    out = []
    pos = 0
    s = s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if m is None:
            raise ValueError(s[pos:])
        pos = m.end()
        if m.group(1):
            out.append(('num', Fr(m.group(1))))
        elif m.group(2):
            out.append(('id', m.group(2)))
        elif m.group(3) and not m.group(3).isspace():
            out.append(('op', m.group(3)))
    return out


def padd(a, b, s=1):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + s * v
        if r[k] == 0:
            del r[k]
    return r


def pmul(a, b):
    r = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(sorted(k1 + k2))
            r[k] = r.get(k, 0) + v1 * v2
            if r[k] == 0:
                del r[k]
    return r


class P:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self):
        x = self.t[self.i]
        self.i += 1
        return x

    def expr(self):
        sign = 1
        if self.peek() == ('op', '-'):
            self.take(); sign = -1
        elif self.peek() == ('op', '+'):
            self.take()
        acc = {k: sign * v for k, v in self.term().items()}
        while self.peek() in (('op', '+'), ('op', '-')):
            op = self.take()[1]
            acc = padd(acc, self.term(), 1 if op == '+' else -1)
        return acc

    def term(self):
        acc = self.factor()
        while self.peek() == ('op', '*'):
            self.take()
            acc = pmul(acc, self.factor())
        return acc

    def factor(self):
        k, v = self.take()
        if k == 'num':
            return {(): v}
        if k == 'id' and v == 'sqr':
            assert self.take() == ('op', '(')
            e = self.expr()
            assert self.take() == ('op', ')')
            return pmul(e, e)
        if k == 'id':
            return {(v,): Fr(1)}
        if (k, v) == ('op', '('):
            e = self.expr()
            assert self.take() == ('op', ')')
            return e
        if (k, v) == ('op', '-'):
            return {kk: -vv for kk, vv in self.factor().items()}
        raise ValueError((k, v))


def parse_gms(path):
    txt = open(path).read()
    lines = [l for l in txt.split('\n') if not l.startswith('*') and not l.startswith('$')]
    body = '\n'.join(lines)
    stmts = [s.strip() for s in body.split(';')]
    variables, positive, eqs, lo, up, fx = [], set(), {}, {}, {}, {}
    for s in stmts:
        if not s:
            continue
        m = re.match(r'^(Positive\s+Variables|Variables|Equations)\s+(.*)$', s, re.S)
        if m:
            names = [x.strip() for x in m.group(2).replace('\n', ' ').split(',') if x.strip()]
            if m.group(1) == 'Variables':
                variables += names
            elif m.group(1).startswith('Positive'):
                positive |= set(names)
            continue
        m = re.match(r'^(\w+)\.\.(.*)=([LEG])=(.*)$', s, re.S)
        if m:
            lhs = P(tokenize(m.group(2).replace('\n', ' ')))
            L = lhs.expr(); assert lhs.i == len(lhs.t)
            rhs = P(tokenize(m.group(4)))
            Rr = rhs.expr(); assert rhs.i == len(rhs.t)
            eqs[m.group(1)] = (padd(L, Rr, -1), m.group(3))  # poly (lhs - rhs) sense 0
            continue
        for part in s.split('\n'):
            part = part.strip()
            if not part:
                continue
            m = re.match(r'^(\w+)\.(lo|up|fx|l|m)\s*=\s*(.*)$', part)
            if m:
                if m.group(2) in ('l', 'm'):
                    continue
                val = Fr(m.group(3).strip())
                {'lo': lo, 'up': up, 'fx': fx}[m.group(2)][m.group(1)] = val
                continue
            if part.startswith(('Model', 'm.', 'Solve', 'option', 'Option')):
                continue
            raise ValueError('unparsed: ' + part[:80])
    for v, val in fx.items():
        lo[v] = up[v] = val
    return dict(variables=variables, positive=positive, eqs=eqs, lo=lo, up=up)


def to_model(G):
    """identify objective variable/row and map to the camshape template; returns (K, r_names, d_names, rows)."""
    eqs = G['eqs']
    # objective row: the equality containing 'objvar'
    objrows = [k for k, (p, s) in eqs.items() if any('objvar' in mono for mono in p)]
    assert len(objrows) == 1
    po, so = eqs[objrows[0]]
    assert so == 'E'
    co = po[('objvar',)]
    lin = {mono[0]: -v / co for mono, v in po.items() if mono != ('objvar',)}  # objvar = sum lin
    assert all(len(m) == 1 for m in po)
    vals = set(lin.values()); assert len(vals) == 1
    c0 = -vals.pop()
    rnames = sorted(lin, key=lambda s: int(s[1:]))
    n = len(rnames)
    rest = [k for k in eqs if k != objrows[0]]
    assert len(rest) == 2 * n
    rid = {nm: j + 1 for j, nm in enumerate(rnames)}  # 1-based r index
    # classify rows
    conv, dro, other = {}, {}, []
    c = None
    for k in rest:
        p, s = eqs[k]
        monos = set(p)
        if s == 'E':
            # D row: r_i - r_{i+1} + d = 0
            rv = [m[0] for m in monos if len(m) == 1 and m[0] in rid]
            dv = [m[0] for m in monos if len(m) == 1 and m[0] not in rid]
            assert len(rv) == 2 and len(dv) == 1 and len(monos) == 3 and () not in p
            i = min(rid[x] for x in rv)
            assert p[(rnames[i - 1],)] == 1 and p[(rnames[i],)] == -1 and p[(dv[0],)] == 1, k
            assert i not in dro
            dro[i] = dv[0]
            continue
        assert s == 'L'
        other.append(k)
    assert sorted(dro) == list(range(1, n))
    rows = {}
    for k in other:
        p, _ = eqs[k]
        idx = sorted({rid[v] for m in p for v in m})
        rows[tuple(idx)] = rows.get(tuple(idx), []) + [p]
    def q(a, b):
        return tuple(sorted((rnames[a - 1], rnames[b - 1])))
    for j in range(2, n):
        (p,) = rows[(j - 1, j, j + 1)]
        assert len(p) == 3 and p[q(j - 1, j)] == -1 and p[q(j, j + 1)] == -1
        cj = p[q(j - 1, j + 1)]
        if c is None:
            c = cj
        assert cj == c, (j, cj, c)
    (p,) = rows[(1, 2)]
    assert p == {q(1, 2): -1, (rnames[0],): -1, (rnames[1],): c}
    if (n - 1, n) in rows:
        (p,) = rows[(n - 1, n)]
    assert set(p) == {q(n - 1, n), (rnames[n - 2],), (rnames[n - 1],)} and p[q(n - 1, n)] == -1 and p[(rnames[n - 1],)] == -2
    c2 = p[(rnames[n - 2],)]
    (p,) = rows[(n,)]
    cE = p[q(n, n)]
    assert p == {q(n, n): cE, (rnames[n - 1],): -4}
    assert len(other) == n + 1
    lo, up = G['lo'], G['up']
    assert all(v not in G['positive'] for v in rnames + list(dro.values()))
    assert lo[rnames[0]] == 1 and up[rnames[-1]] == 2
    for j in range(2, n):
        assert lo[rnames[j - 1]] == 1 and up[rnames[j - 1]] == 2
    ub1, lbn = up[rnames[0]], lo[rnames[-1]]
    assert dro[1] not in lo and dro[1] not in up  # d_1 free
    al = up[dro[2]]
    for i in range(2, n):
        assert lo[dro[i]] == -al and up[dro[i]] == al
    return dict(n=n, c0=c0, c=c, c2=c2, cE=cE, ub1=ub1, lbn=lbn, alpha=al)


def feasible_envelope(K, E):
    """exact feasibility of r = E (d = diff) in the template model with this file's constants."""
    n, c, c2, cE, ub1, lbn, al = K['n'], K['c'], K['c2'], K['cE'], K['ub1'], K['lbn'], K['alpha']
    r = E
    viol = []
    viol.append(-r[1] + c * r[2] - r[1] * r[2])
    for j in range(2, n):
        viol.append(-r[j - 1] * r[j] + c * r[j - 1] * r[j + 1] - r[j] * r[j + 1])
    viol.append(c2 * r[n - 1] - 2 * r[n] - r[n - 1] * r[n])
    viol.append(cE * r[n] ** 2 - 4 * r[n])
    rowmax = max(viol)
    bv = max([1 - r[1], r[1] - ub1] + [max(1 - r[j], r[j] - 2) for j in range(2, n)] + [lbn - r[n], r[n] - 2]
             + [abs(r[i + 1] - r[i]) - al for i in range(2, n)])
    return rowmax, bv, sum(1 for v in viol[:n - 1] if v == 0)


def main(path):
    G = parse_gms(path)
    K = to_model(G)
    n = K['n']
    C = certificate(dict(c=K['c'], ub1=K['ub1'], alpha=K['alpha']), n)
    U, S, E = C['U'], C['S'], C['E']
    assert all(u >= 0 for u in U[:n])
    lb = -K['c0'] * sum(E[1:])
    rowmax, bv, nact = feasible_envelope(K, E)
    out = dict(file=path, n=n, c=str(K['c']), c2_minus_2c=float(K['c2'] - 2 * K['c']), cE_minus_c=float(K['cE'] - K['c']),
               ub1=str(K['ub1']), lbn=str(K['lbn']), alpha=str(K['alpha']), c0=str(K['c0']),
               U_nonneg=True, S_pos=all(s > 0 for s in S[1:n + 1]),
               bound_floor16=dec(lb, 16), bound_ceil16=dec_up(lb, 16),
               envelope_row_max=float(rowmax), envelope_bound_viol=float(bv), envelope_feasible=(rowmax <= 0 and bv <= 0),
               active_conv=nact)
    return out, G, K, lb


if __name__ == '__main__':
    res = []
    for a in sys.argv[1:]:
        o, *_ = main(a)
        print(json.dumps(o), flush=True)
        res.append(o)
    json.dump(res, open('check_gms.json', 'w'), indent=1)
