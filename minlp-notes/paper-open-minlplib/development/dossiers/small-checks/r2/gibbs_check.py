"""ex6_2_7 / ex6_2_5: own parse, phase structure, scaling residual, bound assembly, primal points."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, sys
import sympy as sp
from fractions import Fraction as Fr
import mpmath
from mpmath import iv, mp
import osil

R = (_PUBLIC_REPO + '/research-20260929/reviews/wave2-small-verification/logs/')
for name in ('ex6_2_7', 'ex6_2_5'):
    m = osil.read(name + '.osil')
    X = sp.symbols('x0:9', positive=True)
    def sym(tr):
        op = tr[0]
        if op == 'num': return sp.Rational(tr[1])
        if op == 'var': return sp.Rational(tr[2]) * X[tr[1]]
        a = [sym(c) for c in tr[1:]]
        if op in ('sum', 'plus'): return sp.Add(*a)
        if op in ('product', 'times'): return sp.Mul(*a)
        if op == 'negate': return -a[0]
        if op == 'divide': return a[0] / a[1]
        if op == 'minus': return a[0] - a[1]
        if op in ('ln', 'log'): return sp.log(a[0])
        raise NotImplementedError(op)
    b = []
    for i, c in enumerate(m['cons']):
        assert c['lb'] == c['ub'] and c['nl'] is None and c['lin'] == {3*i: '1', 3*i+1: '1', 3*i+2: '1'}
        b.append(Fr(c['lb']))
    assert all(m['lb'][j] == '1e-7' and Fr(m['ub'][j]) == b[j // 3] for j in range(9))
    o = m['obj']; assert o['sense'] == 'min' and o['lin'] == {} and o['nl'][0] == 'sum'
    parts = {0: [], 1: [], 2: []}
    def vs(t, acc):
        if t[0] == 'var': acc.add(t[1])
        elif t[0] != 'num':
            for c in t[1:]: vs(c, acc)
        return acc
    kinds = set()
    for t in o['nl'][1:]:
        ph = {v % 3 for v in vs(t, set())}
        assert len(ph) == 1
        parts[ph.pop()].append(t)
    y = sp.symbols('y1:4', positive=True); tt = sp.Symbol('t', positive=True)
    G = {}
    for p in range(3):
        e = sp.Add(*[sym(t) for t in parts[p]])
        G[p] = sp.expand(e.subs({X[3*i + p]: y[i] for i in range(3)}))
    same = [sp.simplify(G[0] - G[q]) == 0 for q in (1, 2)]
    print(name, 'b =', [str(v) for v in b], 'T =', sum(b), 'terms/phase', [len(parts[p]) for p in range(3)], 'phase0==phase1,2:', same)
    # scaling residual: R_p(y) = sum over log-carrying terms of their linear prefactor coefficient
    Rp = {}
    for p in range(3):
        Gt = sp.expand(sp.expand_log(G[p].subs({y[i]: tt * y[i] for i in range(3)}, simultaneous=True), force=True))
        resid = sp.expand(Gt - tt * G[p])  # should be t ln t R(y)
        Rlin = sp.simplify(resid / (tt * sp.log(tt)))
        assert tt not in Rlin.free_symbols
        Rp[p] = [sp.Poly(Rlin, *y).coeff_monomial(y[i]) for i in range(3)]
    print('   R_p:', {p: [str(c) for c in Rp[p]] for p in range(3)})
    # bound assembly from the saved verifier certificate (tau, lambda)
    B = json.load(open(R + name + '_bound.json'))
    lam = [Fr(s) for s in B['lam']]
    lamb = sum(l * bi for l, bi in zip(lam, b))
    T = sum(b)
    tau = Fr(B['bb_type0']['tau'])
    mp.dps = 60
    if name == 'ex6_2_7':
        # all three phases identical: m_p >= -tau for each
        Rmax = max(Rp[0])
        # bound = lam.b + 3*min(0, -T tau) - 3*Rmax/e ; e > 2.718281828 => Rmax/e < Rmax/2.718281828
        e_lo = Fr(2718281828, 10**9)
        bound_lo = lamb - 3 * T * tau - 3 * Fr(Rmax.p, Rmax.q) / e_lo
    else:
        # liquids: -tau each; vapour: closed form -ln sum exp(lam_i - c) >= 0 (checked below)
        cI = iv.mpf('.156969560191053')
        iv.dps = 50
        mI = -iv.log(sum(iv.exp(iv.mpf(str(l.numerator)) / iv.mpf(str(l.denominator)) - cI) for l in lam))
        print('   vapour closed-form min enclosure:', mI)
        assert mI.a > 0
        bound_lo = lamb - 2 * T * tau
    print('   lam.b =', mpmath.nstr(mpmath.mpf(lamb.numerator) / lamb.denominator, 25))
    print('   assembled bound >= %s (lower end, exact-rational assembly with e_lo=2.718281828)' % mpmath.nstr(mpmath.mpf(bound_lo.numerator) / bound_lo.denominator, 25))
    # primal point: rows exact, objective enclosure
    xs = []
    for s in B['own_primal_point']:
        xs.append(Fr(s) if '/' not in s else Fr(int(s.split('/')[0]), int(s.split('/')[1])))
    for i in range(3):
        assert sum(xs[3*i + p] for p in range(3)) == b[i]
    assert all(Fr('1e-7') <= v <= b[j // 3] for j, v in enumerate(xs))
    iv.dps = 50
    xi = [iv.mpf(v.numerator) / v.denominator for v in xs]
    F = {'ln': iv.log}
    fo = osil.objective(m, xi, iv.mpf, F)
    print('   primal objective enclosure:', mpmath.nstr(fo.a, 22), mpmath.nstr(fo.b, 22))
    gap = mpmath.mpf(fo.b) - mpmath.mpf(bound_lo.numerator) / bound_lo.denominator
    print('   gap (primal upper - assembled bound): %s' % mpmath.nstr(gap, 6))
    for disp in {'ex6_2_7': ['-0.16084761546364905'], 'ex6_2_5': ['-70.75207783344770759', '-70.75207783344770758']}[name]:
        print('   display', disp, 'valid (<= bound):', Fr(disp) <= bound_lo)
    pdisp = {'ex6_2_7': ['-0.16084761546360086'], 'ex6_2_5': ['-70.752077833447705', '-70.752077833447706']}[name]
    for d in pdisp:
        print('   primal display', d, 'safe (>= objective upper end):', mpmath.mpf(d) >= mpmath.mpf(fo.b))
    # describe G for the paper: print phase-0 expression compactly
    if '-v' in sys.argv:
        print(sp.collect(G[0], [sp.log(y[0]), sp.log(y[1]), sp.log(y[2])]))
        print(G[2])
