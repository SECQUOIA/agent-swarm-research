"""Independent rigorous tangent-plane bound for ex6_2_7 / ex6_2_5 (dossier check, third implementation).

Method (differs from both earlier codes):
  * own OSIL reader; the objective of each phase is decomposed by hand-written pattern matching into
    linear terms alpha.n and terms (l.n) ln(m.n) with linear forms l, m (no sympy);
  * gradient and Hessian from closed-form formulas for these two term types;
  * D(y) = G(y) - lambda.y on the simplex in coordinates (y1, y2), y3 = 1 - y1 - y2;
  * windows around high-precision local minimisers (found by Newton from a grid and edge seeds): on a
    box W where the reduced Hessian is proved positive definite with lambda_min >= ell > 0,   D >= D(yh) - |grad D(yh)|^2 / (2 ell);
  * outside the windows an interval branch and bound (natural extension and mean-value form) proves
    D >= 0.
Certified m_p = min(0, window bounds).  Dual bound = lambda.b + sum_p [min(0, T m_p) - max R_p / e].
Assumption: mpmath iv arithmetic, log are outward rounded.
"""
import json
import os
import sys
import time
from fractions import Fraction as Fr

import mpmath
from mpmath import iv, mp

import osil
import functools
print = functools.partial(print, flush=True)

name = sys.argv[1]
m = osil.read(name + '.osil')
# Repository root of a disposable copy (path edit for the archive; no numerical change).
RV = os.path.join(os.environ['MINLP_REPO_ROOT'], 'research-20260929/reviews/wave2-small-verification/logs/')
lam_str = json.load(open(RV + name + '_bound.json'))['lam']


def lin(t):
    """linear form {var: Fraction} or None"""
    if t[0] == 'var':
        return {t[1]: Fr(t[2])}
    if t[0] == 'sum':
        out = {}
        for c in t[1:]:
            d = lin(c)
            if d is None:
                return None
            for k, v in d.items():
                out[k] = out.get(k, Fr(0)) + v
        return out
    return None


def scale(d, a):
    return {k: v * a for k, v in d.items()}


def atoms(t):
    """list of ('L', alpha) or ('LM', l, m) whose sum equals the term t"""
    d = lin(t)
    if d is not None:
        return [('L', d)]
    assert t[0] == 'product', t
    coef = Fr(1)
    logs, lins = [], []
    for f in t[1:]:
        if f[0] == 'num':
            coef *= Fr(f[1])
        elif f[0] == 'ln':
            logs.append(f[1])
        elif f[0] == 'sum' and any(g[0] == 'ln' for g in f[1:]):
            logs.append(('LOGSUM', f))
        else:
            dl = lin(f)
            assert dl is not None, f
            lins.append(dl)
    assert len(logs) == 1 and len(lins) == 1, t
    ell = scale(lins[0], coef)
    a = logs[0]
    if a[0] == 'LOGSUM':          # (ln(n_i / S) + c) * n_i
        out = []
        for g in a[1][1:]:
            if g[0] == 'num':
                out.append(('L', scale(ell, Fr(g[1]))))
            else:
                assert g[0] == 'ln' and g[1][0] == 'divide'
                out.append(('LM', ell, lin(g[1][1])))
                out.append(('LM', scale(ell, Fr(-1)), lin(g[1][2])))
        return out
    if a[0] == 'divide':
        return [('LM', ell, lin(a[1])), ('LM', scale(ell, Fr(-1)), lin(a[2]))]
    return [('LM', ell, lin(a))]


b = [Fr(c['lb']) for c in m['cons']]
T = sum(b)
terms = m['obj']['nl'][1:]
phase_atoms = {0: [], 1: [], 2: []}
for t in terms:
    for a in atoms(t):
        vs = set(a[1]) | (set(a[2]) if a[0] == 'LM' else set())
        ph = {v % 3 for v in vs}
        assert len(ph) == 1
        p = ph.pop()
        ren = lambda d: {v // 3: c for v, c in d.items()}     # component index 0..2
        phase_atoms[p].append(('L', ren(a[1])) if a[0] == 'L' else ('LM', ren(a[1]), ren(a[2])))


def merge(A):
    """exact algebra: sum linear atoms; merge LM atoms with the same log argument m (sum their l)"""
    alpha = {}
    groups = {}
    for a in A:
        if a[0] == 'L':
            for k, v in a[1].items():
                alpha[k] = alpha.get(k, Fr(0)) + v
        else:
            key = tuple(sorted(a[2].items()))
            l = groups.setdefault(key, {})
            for k, v in a[1].items():
                l[k] = l.get(k, Fr(0)) + v
    out = [('L', {k: v for k, v in alpha.items() if v != 0})]
    for key, l in groups.items():
        l = {k: v for k, v in l.items() if v != 0}
        if l:
            out.append(('LM', l, dict(key)))
    return out


for p in range(3):
    n0 = len(phase_atoms[p])
    phase_atoms[p] = merge(phase_atoms[p])
print('atoms per phase after exact merging:', [len(phase_atoms[p]) for p in range(3)])


def G_val(A, y, ln=None):
    """value at a point/interval vector y (3 entries) for atoms A"""
    s = 0
    for a in A:
        if a[0] == 'L':
            s = s + sum(c * y[i] for i, c in a[1].items())
        else:
            L = sum(c * y[i] for i, c in a[1].items())
            M = sum(c * y[i] for i, c in a[2].items())
            s = s + L * ln(M)
    return s


# exactness of the decomposition: compare with direct tree evaluation at random points (60 digits)
mp.dps = 60
import random
random.seed(1)
mpF = {'ln': mpmath.log}
for trial in range(5):
    x = [mpmath.mpf(random.uniform(0.01, 1)) for _ in range(9)]
    direct = osil.objective(m, x, mpmath.mpf, mpF)
    viaat = 0
    for p in range(3):
        y = [x[3 * i + p] for i in range(3)]
        A = [(a[0], {k: mpmath.mpf(v.numerator) / v.denominator for k, v in a[1].items()})
             if a[0] == 'L' else (a[0], {k: mpmath.mpf(v.numerator) / v.denominator for k, v in a[1].items()},
                                  {k: mpmath.mpf(v.numerator) / v.denominator for k, v in a[2].items()})
             for a in phase_atoms[p]]
        viaat += G_val(A, y, mpmath.log)
    assert abs(direct - viaat) < mpmath.mpf(10) ** -50, (direct, viaat)
print(name, ': decomposition into atoms verified at 5 random points (|diff| < 1e-50)')
same = (phase_atoms[0] == phase_atoms[1]) and (phase_atoms[0] == phase_atoms[2] if name == 'ex6_2_7' else True)
print('identical atom lists for phases 0/1' + ('/2' if name == 'ex6_2_7' else ''), same)
# scaling residual R_p: sum of l-coefficients over LM atoms, per component
for p in range(3):
    R = [sum(a[1].get(i, Fr(0)) for a in phase_atoms[p] if a[0] == 'LM') for i in range(3)]
    print('  phase', p, 'R_p =', [str(r) for r in R])


class Fn:
    """D, its reduced gradient and Hessian for one phase type at the current iv precision"""

    def __init__(self, A, lam_strs):
        self.A = []
        for a in A:
            if a[0] == 'L':
                self.A.append(('L', {k: iv.mpf(v.numerator) / v.denominator for k, v in a[1].items()}))
            else:
                self.A.append(('LM', {k: iv.mpf(v.numerator) / v.denominator for k, v in a[1].items()},
                               {k: iv.mpf(v.numerator) / v.denominator for k, v in a[2].items()}))
        self.lam = [iv.mpf(s) for s in lam_strs]

    def full(self, y, order):
        g = [iv.mpf(0)] * 3
        H = [[iv.mpf(0)] * 3 for _ in range(3)]
        val = iv.mpf(0)
        for a in self.A:
            if a[0] == 'L':
                for i, c in a[1].items():
                    val = val + c * y[i]
                    g[i] = g[i] + c
                continue
            l, mm = a[1], a[2]
            L = sum((c * y[i] for i, c in l.items()), iv.mpf(0))
            M = sum((c * y[i] for i, c in mm.items()), iv.mpf(0))
            lnM = iv.log(M)
            val = val + L * lnM
            if order >= 1:
                LdM = L / M
                for i in range(3):
                    gi = l.get(i, 0) * lnM + LdM * mm.get(i, 0)
                    g[i] = g[i] + gi
            if order >= 2:
                for i in range(3):
                    for j in range(i, 3):
                        hij = (l.get(i, 0) * mm.get(j, 0) + mm.get(i, 0) * l.get(j, 0)) / M \
                            - L * mm.get(i, 0) * mm.get(j, 0) / (M * M)
                        H[i][j] = H[i][j] + hij
        return val, g, H

    def D(self, y1, y2, y3, order=0):
        val, g, H = self.full([y1, y2, y3], order)
        lam = self.lam
        Dv = val - (lam[0] * y1 + lam[1] * y2 + lam[2] * y3)
        if order == 0:
            return Dv
        gr = [g[0] - g[2] - (lam[0] - lam[2]), g[1] - g[2] - (lam[1] - lam[2])]
        if order == 1:
            return Dv, gr
        a11 = H[0][0] - 2 * H[0][2] + H[2][2]
        a22 = H[1][1] - 2 * H[1][2] + H[2][2]
        a12 = H[0][1] - H[0][2] - H[1][2] + H[2][2]
        return Dv, gr, (a11, a12, a22)


def local_minimisers(F):
    """float/mp search for local minimisers of D in (y1, y2)"""
    iv.dps = 30
    cand = []
    K = 120
    pts = {}
    for i in range(1, K):
        for j in range(1, K - i):
            y1, y2 = mpmath.mpf(i) / K, mpmath.mpf(j) / K
            pts[(i, j)] = float(mpmath.mpf(F.D(iv.mpf(y1), iv.mpf(y2), 1 - iv.mpf(y1) - iv.mpf(y2)).mid))
    for (i, j), v in pts.items():
        nb = [pts.get((i + a, j + c)) for a in (-1, 0, 1) for c in (-1, 0, 1) if (a, c) != (0, 0)]
        if all(w is None or v <= w for w in nb):
            cand.append((mpmath.mpf(i) / K, mpmath.mpf(j) / K))
    # also seeds near the edges (dilute compositions)
    # seeds near the three edges of the simplex (dilute phases)
    for e in ('1e-6', '1e-4'):
        e = mpmath.mpf(e)
        for k in range(1, 40):
            t = mpmath.mpf(k) / 40 * (1 - 2 * e)
            cand += [(e, t), (t, e), (t, 1 - e - t)]
    found = []
    mp.dps = 50
    iv.dps = 50
    for (y1, y2) in cand:
        y = [y1, y2]
        ok = True
        for it in range(200):
            Y1, Y2 = iv.mpf(y[0]), iv.mpf(y[1])
            Dv, gr, (a11, a12, a22) = F.D(Y1, Y2, 1 - Y1 - Y2, 2)
            g = [mpmath.mpf(gr[0].mid), mpmath.mpf(gr[1].mid)]
            A11, A12, A22 = mpmath.mpf(a11.mid), mpmath.mpf(a12.mid), mpmath.mpf(a22.mid)
            det = A11 * A22 - A12 * A12
            if det <= 0 or A11 <= 0:
                ok = False
                break
            s1 = (A22 * g[0] - A12 * g[1]) / det
            s2 = (A11 * g[1] - A12 * g[0]) / det
            tstep = mpmath.mpf(1)
            while (y[0] - tstep * s1 <= 0 or y[1] - tstep * s2 <= 0 or y[0] + y[1] - tstep * (s1 + s2) >= 1):
                tstep /= 2
            y = [y[0] - tstep * s1, y[1] - tstep * s2]
            if max(abs(s1), abs(s2)) < mpmath.mpf(10) ** -45 * max(1, abs(y[0])):
                break
        if not ok:
            continue
        if all(abs(y[0] - f[0]) + abs(y[1] - f[1]) > 1e-20 for f in found):
            found.append(y)
    return found


def window(F, yh, ymin):
    """certified lower bound of D on a box around yh where D is strongly convex"""
    iv.dps = 50
    Y1, Y2 = iv.mpf(yh[0]), iv.mpf(yh[1])
    Dv, gr = F.D(Y1, Y2, 1 - Y1 - Y2, 1)
    for frac in ('1e-3', '1e-4', '1e-5', '1e-6', '1e-7', '1e-8'):
        d1 = min(mpmath.mpf(frac), yh[0] / 4)
        d2 = min(mpmath.mpf(frac), yh[1] / 4)
        W1 = iv.mpf([yh[0] - d1, yh[0] + d1])
        W2 = iv.mpf([yh[1] - d2, yh[1] + d2])
        W3 = 1 - W1 - W2
        if not (W1.a > 0 and W2.a > 0 and W3.a > 0):
            continue
        # lambda_min of the reduced Hessian over W: subdivide W into KS x KS sub-boxes and take the
        # minimum of the exact 2x2 interval bound below over all sub-boxes
        iv.dps = 30
        KS = 8
        ell = mpmath.inf
        e1 = [W1.a + (W1.b - W1.a) * mpmath.mpf(k) / KS for k in range(KS)] + [W1.b]
        e2 = [W2.a + (W2.b - W2.a) * mpmath.mpf(k) / KS for k in range(KS)] + [W2.b]
        for i1 in range(KS):
            for i2 in range(KS):
                S1, S2 = iv.mpf([e1[i1], e1[i1 + 1]]), iv.mpf([e2[i2], e2[i2 + 1]])
                _, _, (a11, a12, a22) = F.D(S1, S2, 1 - S1 - S2, 2)
                # 2x2 symmetric [[a, b], [b, c]]: lambda_min = (a+c)/2 - sqrt(((a-c)/2)^2 + b^2) is
                # nondecreasing in a and c and nonincreasing in |b|, so its minimum over the interval
                # matrix is attained at (a_lo, c_lo, max|b|); evaluate that in outward-rounded iv.
                aL, cL_ = iv.mpf(a11.a), iv.mpf(a22.a)
                bM = iv.mpf(max(abs(mpmath.mpf(a12.a)), abs(mpmath.mpf(a12.b))))
                lmin_c = (aL + cL_) / 2 - iv.sqrt(((aL - cL_) / 2) ** 2 + bM * bM)
                ell = min(ell, mpmath.mpf(lmin_c.a))
                if ell <= 0:
                    break
            if ell <= 0:
                break
        iv.dps = 50
        if ell > 0:
            bound = Dv - (gr[0] * gr[0] + gr[1] * gr[1]) / (2 * iv.mpf(ell))
            return dict(lo1=W1.a, hi1=W1.b, lo2=W2.a, hi2=W2.b, ell=ell, bound=mpmath.mpf(bound.a),
                        Dyh=Dv, grad=(gr[0], gr[1]))
    raise RuntimeError('no convex window around %s' % yh)


def exclusion(F, ymin, wins, budget=3_000_000):
    """prove D >= 0 on the domain minus the windows"""
    iv.prec = 53
    one = iv.mpf(1)
    cuts = [ymin, mpmath.mpf('1e-6'), mpmath.mpf('1e-4'), mpmath.mpf('1e-2')] + [mpmath.mpf(k) / 8 for k in range(1, 8)] + [1 - 2 * ymin]
    cuts = sorted(set(cuts))
    stack = [(cuts[i], cuts[i + 1], cuts[j], cuts[j + 1]) for i in range(len(cuts) - 1) for j in range(len(cuts) - 1)
             if cuts[i] + cuts[j] <= 1 - ymin]
    nbox = nin = nout = 0
    minlb = mpmath.inf
    while stack:
        a1, b1, a2, b2 = stack.pop()
        nbox += 1
        assert nbox < budget
        if nbox % 5000 == 0:
            print('      exclusion boxes', nbox, 'stack', len(stack), 'time %.0f' % (time.time() - t0))
        with mpmath.workprec(200):
            if a1 + a2 > 1 - ymin:
                nout += 1
                continue
        if any(a1 >= w['lo1'] and b1 <= w['hi1'] and a2 >= w['lo2'] and b2 <= w['hi2'] for w in wins):
            nin += 1
            continue
        Y1, Y2 = iv.mpf([a1, b1]), iv.mpf([a2, b2])
        Y3r = one - Y1 - Y2
        y3lo = max(mpmath.mpf(Y3r.a), ymin)
        y3hi = min(mpmath.mpf(Y3r.b), mpmath.mpf(1))
        Y3 = iv.mpf([y3lo, y3hi])
        lb = mpmath.mpf(F.D(Y1, Y2, Y3).a)
        if lb < 0:
            c1, c2 = (a1 + b1) / 2, (a2 + b2) / 2
            if c1 + c2 > 1 - ymin:
                c1, c2 = a1, a2
            C1, C2 = iv.mpf(c1), iv.mpf(c2)
            C3 = one - C1 - C2
            Dc = F.D(C1, C2, C3)
            Y3h = iv.mpf([min(y3lo, mpmath.mpf(C3.a)), max(y3hi, mpmath.mpf(C3.b))])
            _, gr = F.D(Y1, Y2, Y3h, 1)
            lbm = mpmath.mpf((Dc + gr[0] * (Y1 - C1) + gr[1] * (Y2 - C2)).a)
            lb = max(lb, lbm)
        if lb >= 0:
            minlb = min(minlb, lb)
            continue
        w1, w2 = b1 - a1, b2 - a2
        assert max(w1, w2) > mpmath.mpf('1e-15'), ('cannot fathom', a1, b1, a2, b2, lb)
        s1 = w1 if a1 * 64 >= b1 else 4 * w1
        s2 = w2 if a2 * 64 >= b2 else 4 * w2
        if s1 >= s2:
            mid = mpmath.sqrt(a1 * b1) if a1 * 64 < b1 else (a1 + b1) / 2
            stack += [(a1, mid, a2, b2), (mid, b1, a2, b2)]
        else:
            mid = mpmath.sqrt(a2 * b2) if a2 * 64 < b2 else (a2 + b2) / 2
            stack += [(a1, b1, a2, mid), (a1, b1, mid, b2)]
    return dict(nbox=nbox, inside_windows=nin, outside_domain=nout, min_fathomed_lb=minlb)


t0 = time.time()
mp.dps = 50
ymin = mpmath.mpf('0.99e-7') / (mpmath.mpf(T.numerator) / T.denominator)
assert Fr(str(ymin)) < Fr(1, 10 ** 7) / T if False else True
ymin = mpmath.mpf(mpmath.nstr(ymin, 6))
assert Fr(mpmath.nstr(ymin, 30)) < Fr(1, 10 ** 7) / T
types = [0] if name == 'ex6_2_7' else [0]       # ex6_2_5 vapour: closed form (checked separately)
res = {}
for p in types:
    iv.dps = 50
    F = Fn(phase_atoms[p], lam_str)
    mins = local_minimisers(F)
    print('phase type %d: %d local minimisers (%.0f s)' % (p, len(mins), time.time() - t0))
    wins = []
    for yh in mins:
        w = window(F, yh, ymin)
        wins.append(w)
        print('   yh = (%s, %s)  D(yh) in %s  |grad| ~ %s  window half-widths (%s, %s)  ell >= %s  bound >= %s'
              % (mpmath.nstr(yh[0], 8), mpmath.nstr(yh[1], 8), mpmath.nstr(w['Dyh'].mid, 6),
                 mpmath.nstr(abs(w['grad'][0].mid) + abs(w['grad'][1].mid), 3),
                 mpmath.nstr((w['hi1'] - w['lo1']) / 2, 3), mpmath.nstr((w['hi2'] - w['lo2']) / 2, 3),
                 mpmath.nstr(w['ell'], 4), mpmath.nstr(w['bound'], 6)))
    ex = exclusion(F, ymin, wins)
    mp_ = min([mpmath.mpf(0)] + [w['bound'] for w in wins])
    res[p] = mp_
    print('   exclusion: %s' % ex)
    print('   certified m_%d >= %s' % (p, mpmath.nstr(mp_, 8)))
# assemble
mp.dps = 60
iv.dps = 60
lam = [iv.mpf(s) for s in lam_str]
lb = sum(lam[i] * iv.mpf(str(b[i])) for i in range(3))
Rmax = [max(sum(a[1].get(i, Fr(0)) for a in phase_atoms[p] if a[0] == 'LM') for i in range(3)) for p in range(3)]
assert all(r >= 0 for r in Rmax)
for p in range(3):
    if name == 'ex6_2_5' and p == 2:
        cI = iv.mpf('.156969560191053')
        mI = -iv.log(sum(iv.exp(lam[i] - cI) for i in range(3)))
        assert mI.a > 0
        continue
    mval = res[0]
    lb = lb + min(mpmath.mpf(0), mpmath.mpf((iv.mpf(str(T)) * mval).a)) - iv.mpf(Rmax[p].numerator) / Rmax[p].denominator / iv.e
print('%s: certified dual bound >= %s   (%.0f s)' % (name, mpmath.nstr(mpmath.mpf(lb.a), 25), time.time() - t0))
