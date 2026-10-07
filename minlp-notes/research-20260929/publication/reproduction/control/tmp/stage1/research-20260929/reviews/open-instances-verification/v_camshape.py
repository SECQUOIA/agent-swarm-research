"""Independent verification of the camshape bounds, fully in exact rational arithmetic.

Model (checked from the OSIL, exact strings), r_1..r_n = x[0..n-1], d_i = x[n+i-1]:
  min -c0 sum r
  G_1: -r_1 + c r_2 - r_1 r_2 <= 0
  G_j: -r_{j-1} r_j + c r_{j-1} r_{j+1} - r_j r_{j+1} <= 0      j=2..n-1
  G_n: c2 r_{n-1} - 2 r_n - r_{n-1} r_n <= 0
  E  : c r_n^2 - 4 r_n <= 0
  D_i: r_i - r_{i+1} + d_i = 0                                 i=1..n-1
  r_1 in [1,ub1], r_j in [1,2], r_n in [lbn,2], d_1 free, |d_i| <= alpha (i>=2)

Bound: u = 1/r, S_0 = 1, S_1 = 1/ub1, S_{j+1} = c S_j - S_{j-1} (exact rationals);
Chebyshev U_m(c/2) >= 0 for m <= n-1 checked exactly; R_j = 1/S_j;
B_j = min(R_j, ub_j); E_j = min over k of B_k + alpha*|j-k| over the
slope-constrained part j,k >= 2 (the pair (1,2) is unconstrained, so E_1 = B_1).
Bound = -c0 * sum E (exact rational).  Feasibility of E checked exactly.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import json, sys
from fractions import Fraction as Fr
import osilx
from mpmath import iv, mp, mpf

PREC = 400


def enc(q):
    """outward enclosure of an exact rational in a 400-bit mpmath interval"""
    p, d = q.numerator, q.denominator
    lo = (p << PREC) // d
    hi = lo if lo * d == (p << PREC) else lo + 1
    mp.prec = 2 * PREC + 64
    iv.prec = PREC + 64
    a = mpmath.ldexp(mpf(lo), -PREC); b = mpmath.ldexp(mpf(hi), -PREC)
    return iv.mpf([a, b])


def encsum(qs):
    iv.prec = PREC + 64
    s = iv.mpf(0)
    for q in qs:
        s += enc(q)
    return s


import mpmath

P = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/')
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))
AUTH = _REPO + '/research-20260929/open-instances/'


def extract(I, n):
    assert len(I['names']) == 2 * n - 1 and len(I['cons']) == 2 * n
    o = I['obj']
    assert o['sense'] == 'min' and not o['quad'] and o['nl'] is None and o['constant'] == '0'
    assert sorted(o['lin']) == list(range(n)) and len(set(o['lin'].values())) == 1
    c0s = o['lin'][0]
    assert c0s.startswith('-')
    c0 = -Fr(c0s)
    cons = I['cons']
    c = cons[0]['quad'][1][2]
    # interior rows
    for i in range(n - 2):
        r = cons[i]
        assert (r['lb'], r['ub'], r['lin'], r['nl'], r['constant']) == ('-INF', '0', {}, None, '0'), i
        assert r['quad'] == [(i, i + 1, '-1'), (i, i + 2, c), (i + 1, i + 2, '-1')], i
    r = cons[n - 2]
    assert (r['lb'], r['ub'], r['nl']) == ('-INF', '0', None)
    assert r['lin'] == {0: '-1', 1: c} and r['quad'] == [(0, 1, '-1')]
    r = cons[n - 1]
    assert (r['lb'], r['ub'], r['nl']) == ('-INF', '0', None)
    assert set(r['lin']) == {n - 2, n - 1} and r['lin'][n - 1] == '-2' and r['quad'] == [(n - 2, n - 1, '-1')]
    c2 = r['lin'][n - 2]
    r = cons[n]
    assert (r['lb'], r['ub'], r['nl'], r['lin'], r['quad']) == ('-INF', '0', None, {n - 1: '-4'}, [(n - 1, n - 1, c)])
    for i in range(n - 1):
        r = cons[n + 1 + i]
        assert (r['lb'], r['ub'], r['nl'], r['quad']) == ('0', '0', None, [])
        assert r['lin'] == {i: '1', i + 1: '-1', n + i: '1'}, i
    lb, ub = I['lb'], I['ub']
    assert lb[0] == '1' and ub[n - 1] == '2'
    ub1, lbn = ub[0], lb[n - 1]
    for j in range(1, n - 1):
        assert (lb[j], ub[j]) == ('1', '2')
    assert (lb[n], ub[n]) == ('-INF', 'INF')
    al = ub[n + 1]
    for i in range(n + 1, 2 * n - 1):
        assert (lb[i], ub[i]) == ('-' + al, al), i
    assert all(t == 'C' for t in I['vt'])
    return dict(c0=c0, c=Fr(c), c2=Fr(c2), ub1=Fr(ub1), lbn=Fr(lbn), alpha=Fr(al),
                strings=dict(c0=c0s, c=c, c2=c2, ub1=ub1, lbn=lbn, alpha=al))


def bound(K, n):
    c, ub1, al = K['c'], K['ub1'], K['alpha']
    # Chebyshev U_m(c/2), m = 0..n-1, exactly
    U = [Fr(1), c]
    for m in range(2, n):
        U.append(c * U[-1] - U[-2])
    Umin = min(U[:n])
    assert Umin >= 0
    # S_j, j = 0..n
    S = [Fr(1), 1 / ub1]
    for j in range(1, n):
        S.append(c * S[j] - S[j - 1])
    assert all(s > 0 for s in S[1:n + 1])
    R = [None] + [1 / S[j] for j in range(1, n + 1)]
    ubv = [None, ub1] + [Fr(2)] * (n - 1)
    B = [None] + [min(R[j], ubv[j]) for j in range(1, n + 1)]
    E = [None] * (n + 1)
    E[1] = B[1]
    F = [None] * (n + 1)
    F[2] = B[2]
    for j in range(3, n + 1):
        F[j] = min(B[j], F[j - 1] + al)
    E[n] = F[n]
    for j in range(n - 1, 1, -1):
        E[j] = min(F[j], E[j + 1] + al)
    total = encsum(E[1:])
    bnd = -(enc(K['c0']) * total)
    return dict(U=U, Umin=Umin, S=S, R=R, B=B, E=E, bound=bnd)


def check_point(K, n, r, d=None, exact=True):
    """max violations (rows, bounds) and objective for r (list of Fractions, 1-based r[1..n])."""
    c, c2, al = K['c'], K['c2'], K['alpha']
    if d is None:
        d = [None] + [r[i + 1] - r[i] for i in range(1, n)]
    G = [None] * (n + 1)
    G[1] = -r[1] + c * r[2] - r[1] * r[2]
    for j in range(2, n):
        G[j] = -r[j - 1] * r[j] + c * r[j - 1] * r[j + 1] - r[j] * r[j + 1]
    G[n] = c2 * r[n - 1] - 2 * r[n] - r[n - 1] * r[n]
    Erow = c * r[n] ** 2 - 4 * r[n]
    rowv = max([max(G[j], 0) for j in range(1, n + 1)] + [max(Erow, 0)])
    eqv = max(abs(r[i] - r[i + 1] + d[i]) for i in range(1, n))
    bl = [None, Fr(1)] + [Fr(1)] * (n - 2) + [K['lbn']]
    bu = [None, K['ub1']] + [Fr(2)] * (n - 1)
    bv = max(max(bl[j] - r[j], r[j] - bu[j], 0) for j in range(1, n + 1))
    bv = max(bv, max(max(abs(d[i]) - al, 0) for i in range(2, n)))
    obj = -(enc(K['c0']) * encsum(r[1:]))
    minslackG = min(-G[j] for j in range(1, n + 1))
    return dict(obj=obj, rowviol=max(rowv, eqv), bndviol=bv, G=G, minslackG=minslackG)


def read_sol(I, path, n):
    idx = {nm: j for j, nm in enumerate(I['names'])}
    x = [Fr(0)] * len(I['names'])
    seen = set(); objv = None
    for line in open(path):
        nm, val = line.split()
        if nm == 'objvar':
            objv = val; continue
        x[idx[nm]] = Fr(val); seen.add(nm)
    missing = [I['names'][j] for j in range(len(I['names'])) if I['names'][j] not in seen]
    r = [None] + x[:n]
    d = [None] + x[n:2 * n - 1]
    return r, d, missing, objv


def ivs(x, k=16):
    """lower end of an interval, rounded down in the printed digits"""
    return mpmath.nstr(mp.make_mpf(x._mpi_[0]), k)


def fl(q, k=16):
    from mpmath import mp, mpf, nstr
    mp.dps = 60
    return nstr(mpf(q.numerator) / q.denominator, k)


def main(n):
    import numpy as np
    I = osilx.read(P + f'camshape{n}.osil')
    K = extract(I, n)
    res = bound(K, n)
    out = dict(n=n, constants=K['strings'], c2_minus_2c=fl(K['c2'] - 2 * K['c'], 3), Umin=fl(res['Umin'], 5),
               Smin=fl(min(res['S'][1:n + 1]), 6), bound=ivs(res['bound'], 20),
               bound_width=mpmath.nstr(mp.make_mpf(res['bound'].delta._mpi_[1]), 3))
    E = res['E']
    # phases of the envelope
    onR = [j for j in range(1, n + 1) if E[j] == res['R'][j]]
    at2 = [j for j in range(1, n + 1) if E[j] == 2]
    out['phase'] = dict(onR_last=max(onR), n_onR=len(onR), first_at2=min(at2) if at2 else None,
                        n_at2=len(at2), n_slope=n - len(onR) - len(at2))
    # exact feasibility of E itself (d_1 = r_2 - r_1 free)
    ch = check_point(K, n, E)
    out['envelope_exact'] = dict(obj=ivs(ch['obj'], 20), rowviol=str(ch['rowviol']), bndviol=str(ch['bndviol']),
                                 minslackG=fl(ch['minslackG'], 5),
                                 n_active_G=sum(1 for j in range(1, n + 1) if ch['G'][j] == 0))
    assert ch['obj'].a == res['bound'].a and ch['obj'].b == res['bound'].b
    # E rounded to doubles, evaluated exactly
    Ed = [None] + [Fr(float(E[j])) for j in range(1, n + 1)]
    ch = check_point(K, n, Ed)
    out['envelope_double'] = dict(obj=ivs(ch['obj']), rowviol=fl(ch['rowviol'], 3), bndviol=fl(ch['bndviol'], 3))
    # authors' envelope
    Ea = np.load(AUTH + f'logs/camshape{n}_envelope.npy')
    Ea = [None] + [Fr(float(v)) for v in Ea[:n]] if len(Ea) >= n else None
    ch = check_point(K, n, Ea)
    out['authors_envelope'] = dict(obj=ivs(ch['obj']), rowviol=fl(ch['rowviol'], 3), bndviol=fl(ch['bndviol'], 3),
                                   max_absdiff_vs_own=fl(max(abs(Ea[j] - E[j]) for j in range(1, n + 1)), 3))
    for p in ['p1', 'p2']:
        try:
            r, d, miss, objv = read_sol(I, AUTH + f'minlplib_sol/camshape{n}.{p}.sol', n)
        except FileNotFoundError:
            continue
        ch = check_point(K, n, r, d)
        out['minlplib_' + p] = dict(file_objvar=objv, obj=ivs(ch['obj']), rowviol=fl(ch['rowviol'], 3),
                                    bndviol=fl(ch['bndviol'], 3), missing_vars=len(miss),
                                    missing_sample=miss[:5],
                                    obj_minus_bound=ivs(ch['obj'] - res['bound'], 3))
    print(json.dumps(out, indent=1), flush=True)
    return out, res


if __name__ == '__main__':
    allout = [main(int(a))[0] for a in sys.argv[1:]]
    json.dump(allout, open('logs/camshape_verify.json', 'w'), indent=1)
