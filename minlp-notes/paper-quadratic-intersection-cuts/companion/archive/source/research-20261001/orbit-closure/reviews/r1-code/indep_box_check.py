"""Reviewer's independent exact check of the box certificates of orbit-closure (families B and BP).

Written for review round 1; it does not import any code of the stream.  The instance data are
typed in from note.md (Section 4), not read from the certificate; the certificate is used only for
its list of leaves (box, type, test vectors).

What is checked, for a point lam_hat and the corner sbar = (-9/2, 0, 3/2), rays to v_1, v_2, v_3:
  * family B: X = F^T M(sbar) ranges over all 2x2 matrices with X_11 = u^T sym(X) u >= 0
    (u = (1, -sbar_y) = (1, 0) here).  Charts: facets of [-1, 1]^4 (entries t = (X11, X12, X21, X22)),
    t1 = +1, or t_i = +-1 (i = 2, 3, 4) with t1 in [0, 1].  Any X with X11 > 0 has a positive multiple
    on one of them.
  * family BP: S(u) = [[(1+u1)/2, u2/2], [u2/2, (1-u1)/2]], u in [-1, 1]^2; S > 0 iff |u| < 1.
  * coverage, by a method different from the stream's verifier: every leaf lies in its chart,
    the leaf volumes add up exactly to the chart volume, and leaf interiors are pairwise disjoint
    (sweep along the first coordinate).  Closed boxes with these properties cover the chart.
  * every leaf, from the definitions, with F^T = X M(sbar)^{-1} and products computed directly:
      kept(v) = v^T F^T E v,  d(v) = v^T F^T M(sbar) v,  n_j(v) = -v^T F^T M0(p_j) v   (all linear in X);
      'excl': kept >= 0 and d < 0 at every vertex;
      'skip' (BP): min over the box of u1^2 + u2^2 >= 1;
      'cut': for each ray j at most one bound is used (the larger of the listed ones):
         vector bound 1/mu_j with mu_j = max_vertices d/n_j, requiring kept >= 0, n_j > 0 at vertices;
         kept-boundary bound (BP) min_vertices L_j(S)/(m^T S m) with L_j derived here by sympy and
         checked as a polynomial identity n_j(J S m) = det(S) L_j(S);
      and sum_j lam_j * bound_j >= 1.
Usage: python3 indep_box_check.py CERT.json B|BP 'l1,l2,l3'
"""
import sys, json
from fractions import Fraction as Fr
import sympy as sp

SB = (Fr(-9, 2), Fr(0), Fr(3, 2))
VS = [(Fr(-1), Fr(-6), Fr(18)), (Fr(-5), Fr(6), Fr(-18)), (Fr(0), Fr(5, 2), Fr(5, 2))]
PS = [tuple(v[i] - SB[i] for i in range(3)) for v in VS]


def M(s, h=Fr(1)):
    x, y, w = s
    return ((w, x), (y, h))


def mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def inv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return ((A[1][1] / d, -A[0][1] / d), (-A[1][0] / d, A[0][0] / d))


def qf(v, A):
    return sum(v[i] * A[i][j] * v[j] for i in range(2) for j in range(2))


MSB = M(SB)
MSBI = inv(MSB)
E = ((Fr(1), Fr(0)), (Fr(0), Fr(0)))
M0 = [M(p, Fr(0)) for p in PS]


def quantities(X, v, j):
    FT = mul(X, MSBI)
    return qf(v, mul(FT, E)), qf(v, mul(FT, MSB)), -qf(v, mul(FT, M0[j]))


def X_B(chart_id, t):
    # chart id 'tK=+1' / 'tK=-1'; t lists the free coordinates in increasing index
    k = int(chart_id[1]) - 1
    sg = Fr(1) if chart_id[3] == '+' else Fr(-1)
    e = list(t)
    e.insert(k, sg)
    return ((e[0], e[1]), (e[2], e[3]))


def B_chart_box(chart_id):
    k = int(chart_id[1]) - 1
    lo = []
    for i in range(4):
        if i == k:
            continue
        lo.append(Fr(0) if i == 0 else Fr(-1))
    return lo, [Fr(1)] * 3


def S_BP(t):
    return (((1 + t[0]) / 2, t[1] / 2), (t[1] / 2, (1 - t[0]) / 2))


def kb_forms():
    a, b, c = sp.symbols('a b c')
    S = sp.Matrix([[a, b], [b, c]])
    Ms = sp.Matrix([[sp.Rational(str(x)) for x in r] for r in MSB])
    m = Ms.inv() * sp.Matrix([1, 0])
    J = sp.Matrix([[0, 1], [-1, 0]])
    v = J * S * m
    FT = S * Ms.inv()
    out = []
    for j in range(3):
        n = sp.expand(-(v.T * FT * sp.Matrix([[sp.Rational(str(x)) for x in r] for r in M0[j]]) * v)[0])
        # L_j by matching: n = det(S) * (la a + lb b + lc c)
        la, lb, lc = sp.symbols('la lb lc')
        res = sp.Poly(sp.expand(n - (a * c - b ** 2) * (la * a + lb * b + lc * c)), a, b, c)
        sol = sp.solve(res.coeffs(), [la, lb, lc], dict=True)
        assert len(sol) == 1, 'n_j(JSm) is not det(S) times a linear form'
        L = tuple(Fr(str(sol[0][s])) for s in (la, lb, lc))
        Ls = sp.Rational(str(L[0])) * a + sp.Rational(str(L[1])) * b + sp.Rational(str(L[2])) * c
        assert sp.expand(n - (a * c - b ** 2) * Ls) == 0
        # kept: v^T F^T E v = 0 identically
        assert sp.expand((v.T * FT * sp.Matrix([[1, 0], [0, 0]]) * v)[0]) == 0
        # d(v) = det(S) m^T S m
        assert sp.expand((v.T * FT * Ms * v)[0] - (a * c - b ** 2) * (m.T * S * m)[0]) == 0
        out.append(L)
    den = sp.Poly(sp.expand((m.T * S * m)[0]), a, b, c)
    D = tuple(Fr(str(den.coeff_monomial(z))) for z in (a, b, c))
    return out, D


def vertices(lo, hi):
    n = len(lo)
    for mask in range(1 << n):
        yield [hi[i] if mask >> i & 1 else lo[i] for i in range(n)]


def coverage(boxes, lo0, hi0):
    """boxes: list of (lo, hi) (Fractions).  True iff all inside, volumes add up, interiors disjoint."""
    vol0 = 1
    for a, b in zip(lo0, hi0):
        vol0 *= (b - a)
    tot = Fr(0)
    for lo, hi in boxes:
        if any(l < L or h > H or l >= h for l, h, L, H in zip(lo, hi, lo0, hi0)):
            return False, 'leaf outside chart or empty'
        v = 1
        for a, b in zip(lo, hi):
            v *= (b - a)
        tot += v
    if tot != vol0:
        return False, 'volume %s != %s' % (tot, vol0)
    order = sorted(range(len(boxes)), key=lambda i: boxes[i][0][0])
    active = []
    for i in order:
        lo, hi = boxes[i]
        active = [k for k in active if boxes[k][1][0] > lo[0]]
        for k in active:
            lo2, hi2 = boxes[k]
            if all(lo[d] < hi2[d] and lo2[d] < hi[d] for d in range(len(lo))):
                return False, 'overlap between leaves %d and %d' % (i, k)
        active.append(i)
    return True, 'volume %s, %d leaves, interiors disjoint' % (tot, len(boxes))


def main(path, fam, lamstr):
    lam = [Fr(x) for x in lamstr.split(',')]
    d = json.load(open(path))
    ok = True
    # the certificate's instance must be the one of the note
    same = ([Fr(x) for x in d['sbar']] == list(SB) and [[Fr(x) for x in p] for p in d['rays']] == [list(p) for p in PS]
            and [Fr(x) for x in d['lam']] == lam and d['family'] == fam)
    print('instance in certificate equals the note\'s corner, family and point:', same)
    ok &= same
    if fam == 'BP':
        assert d.get('bpchart') == 'u', 'only the u chart is handled here'
        charts = {0: ('disk', [Fr(-1)] * 2, [Fr(1)] * 2)}
        kb, D = kb_forms()
        print('kept-boundary forms L_j (a, b, c coefficients):', [[str(x) for x in L] for L in kb], 'm^T S m:', [str(x) for x in D])
    else:
        charts = {}
        for idx, cid in enumerate(d['charts']):
            lo, hi = B_chart_box(cid)
            charts[idx] = (cid, lo, hi)
        ids = sorted(c[0] for c in charts.values())
        need = sorted(['t1=+1'] + ['t%d=%s1' % (i, s) for i in (2, 3, 4) for s in '+-'])
        print('charts present:', ids == need)
        ok &= ids == need
    leaves = d['leaves']
    for ci, (cid, lo0, hi0) in charts.items():
        boxes = [([Fr(x) for x in lf['lo']], [Fr(x) for x in lf['hi']]) for lf in leaves if lf['chart'] == ci]
        good, msg = coverage(boxes, lo0, hi0)
        print('coverage of chart %s: %s (%s)' % (cid, good, msg))
        ok &= good
    ok &= all(lf['chart'] in charts for lf in leaves)
    counts = {}
    nbad = 0
    minslack = None
    for lf in leaves:
        typ = lf['type']
        counts[typ] = counts.get(typ, 0) + 1
        cid = charts[lf['chart']][0]
        lo = [Fr(x) for x in lf['lo']]; hi = [Fr(x) for x in lf['hi']]
        Xs = [S_BP(t) if fam == 'BP' else X_B(cid, t) for t in vertices(lo, hi)]
        if typ == 'skip':
            good = fam == 'BP' and sum(min(max(Fr(0), l), h) ** 2 for l, h in zip(lo, hi)) >= 1
        elif typ == 'excl':
            v = [Fr(x) for x in lf['v']]
            good = True
            for X in Xs:
                kept, dd, _ = quantities(X, v, 0)
                good &= kept >= 0 and dd < 0
        elif typ == 'cut':
            bound = {}
            good = True
            for js, vv in lf['v'].items():
                j = int(js)
                assert 0 <= j < 3 and str(j) == js
                v = [Fr(x) for x in vv]
                mu = None
                for X in Xs:
                    kept, dd, n = quantities(X, v, j)
                    if kept < 0 or n <= 0:
                        good = False
                        break
                    mu = dd / n if mu is None else max(mu, dd / n)
                if good and mu is not None and mu > 0:
                    bound[j] = max(bound.get(j, Fr(0)), 1 / mu)
                else:
                    good = False
            for js in lf.get('kb', []):
                j = int(js)
                assert fam == 'BP' and 0 <= j < 3
                vals = []
                for X in Xs:
                    dn = D[0] * X[0][0] + D[1] * X[0][1] + D[2] * X[1][1]
                    if dn <= 0:
                        good = False
                        break
                    vals.append((kb[j][0] * X[0][0] + kb[j][1] * X[0][1] + kb[j][2] * X[1][1]) / dn)
                if good and min(vals) > 0:
                    bound[j] = max(bound.get(j, Fr(0)), min(vals))
                else:
                    good = False
            tot = sum(lam[j] * b for j, b in bound.items())   # each ray counted once
            good &= tot >= 1
            if good:
                minslack = tot - 1 if minslack is None else min(minslack, tot - 1)
        else:
            good = False
        nbad += not good
    print('leaf counts:', counts, 'failures:', nbad, 'min slack of cut leaves: %.3g' % float(minslack))
    ok &= nbad == 0
    print('RESULT:', 'PASS' if ok else 'FAIL', '- lam_hat =', [str(x) for x in lam], 'sum =', sum(lam))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
