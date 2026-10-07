#!/usr/bin/env python3
"""Independent check (lit-control review r2): compare MINLPLib camshapeN.gms with
the QPLIB copy QPLIB_q.gms in exact rational arithmetic, and evaluate points.

Usage: cmp_camshape.py N q
Reads web/minlplib/camshapeN.gms, web/minlplib/camshapeN.p1.sol,
      web/qplib/QPLIB_q.gms, web/qplib/QPLIB_q.sol.
Variable map: QPLIB x(k+1) <-> MINLPLib xk (checked, not assumed: rows are
matched by mapped monomial support and sense, and a mismatch is reported).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import re, sys
from fractions import Fraction as F

D = (_PUBLIC_REPO + '/research-20260929/publication/reviews/lit-control-r2/web/')


def parse_gms(path):
    txt = open(path).read()
    lines = [l for l in txt.split('\n') if not l.startswith('*')]
    txt = '\n'.join(lines)
    eqs = {}
    for m in re.finditer(r'^(e\d+)\.\.(.*?);', txt, re.S | re.M):
        name, body = m.group(1), ' '.join(m.group(2).split())
        mm = re.match(r'(.*)=([ELG])=(.*)', body)
        lhs, sense, rhs = mm.group(1), mm.group(2), mm.group(3)
        terms = parse_expr(lhs)
        for k, v in parse_expr(rhs).items():
            terms[k] = terms.get(k, F(0)) - v
        const = -terms.pop((), F(0))  # move constant to rhs
        eqs[name] = (terms, sense, const)
    lo, up = {}, {}
    for m in re.finditer(r'^(\w+)\.(lo|up|fx)\s*=\s*([-+0-9.eE]+)\s*;', txt, re.M):
        v, kind, val = m.group(1), m.group(2), F(m.group(3))
        if kind in ('lo', 'fx'):
            lo[v] = val
        if kind in ('up', 'fx'):
            up[v] = val
    # also handle "x.lo = a; x.up = b;" on one line
    for m in re.finditer(r'(\w+)\.(lo|up|fx)\s*=\s*([-+0-9.eE]+)\s*;', txt):
        v, kind, val = m.group(1), m.group(2), F(m.group(3))
        if kind in ('lo', 'fx'):
            lo[v] = val
        if kind in ('up', 'fx'):
            up[v] = val
    pos = re.search(r'Positive Variables(.*?);', txt, re.S)
    if pos:
        for v in re.findall(r'\w+', pos.group(1)):
            lo.setdefault(v, F(0))
    return eqs, lo, up


def parse_expr(s):
    s = s.replace('(', ' ( ').replace(')', ' ) ')
    # sqr(x) -> x*x
    s = re.sub(r'sqr\s*\(\s*(\w+)\s*\)', r'\1*\1', s)
    s = s.replace('(', '').replace(')', '')
    s = s.replace(' ', '')
    out = {}
    for sign, body in re.findall(r'([+-]?)([^+-]+(?:[eE][+-]\d+[^+-]*)*)', s):
        if not body:
            continue
        coef = F(-1) if sign == '-' else F(1)
        facs = []
        for f in body.split('*'):
            if re.fullmatch(r'[0-9.]+(?:[eE][+-]?\d+)?', f):
                coef *= F(f)
            else:
                facs.append(f)
        key = tuple(sorted(facs))
        out[key] = out.get(key, F(0)) + coef
    return out


def read_sol(path):
    d = {}
    for l in open(path):
        p = l.split()
        if len(p) >= 2:
            d[p[0]] = F(p[1])
    return d


def viol(eqs, lo, up, x, skip=()):
    """max violation over rows (excluding rows in skip) and bounds; missing vars = 0."""
    worst = (F(0), None)
    for name, (terms, sense, rhs) in eqs.items():
        if name in skip:
            continue
        a = F(0)
        for key, c in terms.items():
            t = c
            for v in key:
                t *= x.get(v, F(0))
            a += t
        r = a - rhs
        v = max(r, 0) if sense == 'L' else (max(-r, 0) if sense == 'G' else abs(r))
        if v > worst[0]:
            worst = (v, name)
    for v in set(lo) | set(up):
        val = x.get(v, F(0))
        if v in lo and lo[v] - val > worst[0]:
            worst = (lo[v] - val, v + '.lo')
        if v in up and val - up[v] > worst[0]:
            worst = (val - up[v], v + '.up')
    return worst


def main():
    N, q = sys.argv[1], sys.argv[2]
    A, loA, upA = parse_gms(D + f'minlplib/camshape{N}.gms')
    B, loB, upB = parse_gms(D + f'qplib/QPLIB_{q}.gms')
    nA = len(A); nB = len(B)
    # map QPLIB var -> MINLPLib var
    def mapB(v):
        if v == 'objvar':
            return 'objvar'
        return 'x%d' % (int(v[1:]) - 1)
    def mapA(v):
        return v
    # objective rows: the row containing objvar
    objA = [n for n, (t, s, r) in A.items() if any('objvar' in k for k in t)]
    objB = [n for n, (t, s, r) in B.items() if any('objvar' in k for k in t)]
    print(f'camshape{N} vs QPLIB_{q}: rows {nA} vs {nB}; objective rows {objA} {objB}')
    # normalize each row: map vars, key = (sense, frozenset(monomials))
    def norm(eqs, mp):
        out = {}
        for name, (t, s, r) in eqs.items():
            tt = {tuple(sorted(mp(v) for v in k)): c for k, c in t.items() if c != 0}
            key = (s, frozenset(tt))
            out.setdefault(key, []).append((name, tt, r))
        return out
    nA_, nB_ = norm(A, mapA), norm(B, mapB)
    unmatched = 0
    maxrel = F(0); worst = None
    for key, la in nA_.items():
        lb = nB_.get(key)
        if lb is None or len(lb) != len(la):
            unmatched += 1
            continue
        for (na, ta, ra), (nb, tb, rb) in zip(la, lb):
            # scale: compare coefficients; objective rows may differ in objvar sign/scale
            for mono in ta:
                ca, cb = ta[mono], tb[mono]
                if ca != cb:
                    rel = abs(ca - cb) / abs(ca)
                    if rel > maxrel:
                        maxrel, worst = rel, (na, nb, mono, float(ca), float(cb))
            if ra != rb:
                rel = abs(ra - rb) / max(abs(ra), F(1))
                if rel > maxrel:
                    maxrel, worst = rel, (na, nb, 'rhs', float(ra), float(rb))
    print(f'  unmatched row classes: {unmatched}; max rel coef/rhs diff {float(maxrel):.3e} at {worst}')
    # bounds
    allv = set(loA) | set(upA) | {mapB(v) for v in set(loB) | set(upB)}
    loBm = {mapB(v): c for v, c in loB.items()}; upBm = {mapB(v): c for v, c in upB.items()}
    maxb = F(0); wb = None; bmismatch = []
    for v in allv:
        for da, db, kind in ((loA, loBm, 'lo'), (upA, upBm, 'up')):
            if (v in da) != (v in db):
                bmismatch.append((v, kind, da.get(v), db.get(v)))
            elif v in da and da[v] != db[v]:
                rel = abs(da[v] - db[v]) / max(abs(da[v]), F(1))
                if rel > maxb:
                    maxb, wb = rel, (v, kind, float(da[v]), float(db[v]))
    print(f'  bound presence mismatches: {bmismatch[:5]} (count {len(bmismatch)}); max rel bound diff {float(maxb):.3e} at {wb}')
    # points
    pA = read_sol(D + f'minlplib/camshape{N}.p1.sol')
    pB = read_sol(D + f'qplib/QPLIB_{q}.sol')
    pB_in_A = {mapB(v): c for v, c in pB.items()}
    pA_in_B = {('objvar' if v == 'objvar' else 'x%d' % (int(v[1:]) + 1)): c for v, c in pA.items()}
    print(f'  objvar: MINLPLib p1 {float(pA["objvar"]):.13f}, QPLIB sol {float(pB["objvar"]):.13f}')
    for lab, eqs, lo, up, x, skip in (
            ('MINLPLib p1 in MINLPLib model', A, loA, upA, pA, objA),
            ('MINLPLib p1 in QPLIB model', B, loB, upB, pA_in_B, objB),
            ('QPLIB sol in QPLIB model', B, loB, upB, pB, objB),
            ('QPLIB sol in MINLPLib model', A, loA, upA, pB_in_A, objA)):
        v, where = viol(eqs, lo, up, x, skip)
        # objective value from the r variables: -(pi/N)*sum r  using MINLPLib coefficient
        print(f'  {lab}: max violation (objective row excluded) {float(v):.3e} at {where}')
    # objective recomputed from the MINLPLib objective row on each point
    tA, sA, rA = A[objA[0]]
    def objval(x):
        # row: sum c*x - objvar = rhs  or similar -> solve for objvar
        cobj = tA[('objvar',)]
        rest = sum(c * x.get(k[0], F(0)) for k, c in tA.items() if k != ('objvar',))
        return (rA - rest) / cobj
    print(f'  MINLPLib objective row: p1 -> {float(objval(pA)):.15f}; QPLIB point -> {float(objval(pB_in_A)):.15f}')


if __name__ == '__main__':
    main()
