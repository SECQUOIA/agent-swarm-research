"""Separate exact verification of a box certificate written by box_cert.py.

The instance data (sbar, rays, lam_hat) are read from the certificate; everything else is
recomputed here with separate code (exact rational arithmetic; sympy for one polynomial division):

  0. lam_hat has exactly one nonnegative entry per ray;
  1. the certificate is complete (status 'complete', empty queue, no unresolved leaf);
  2. coverage: for every chart, recursive bisection of the root box (longest side, ties to the
     lowest index) reaches exactly the listed leaves of that chart, so they cover the chart;
     the charts cover the parameter domain of the family (BP: one chart containing the closed
     disk of trace-one positive semidefinite matrices; B: the seven facets of [-1, 1]^4 with
     t1 >= 0, which contain a positive multiple of every 2x2 matrix with u^T sym(X) u >= 0);
  3. every 'skip' box misses the open disk of positive definite trace-one matrices;
  4. every 'excl' box: the listed vector v is kept (v^T X N_E v >= 0) and v^T X v < 0 at every
     vertex (so sbar is outside B_F for every X in the box);
  5. every 'cut' box: for each listed ray j and vector v, v is kept and n = -v^T X N_j v > 0 at
     every vertex, mu_j = max over the vertices of v^T X v / n; for each 'kb' ray (family BP) the
     linear form L_j with -(J S m)^T S N_j (J S m) = det(S) L_j(S) is recomputed, m^T S m > 0 at
     every vertex and b_j = min over the vertices of L_j(S) / m^T S m > 0; finally
     sum_j lam_j * (1/mu_j or b_j) >= 1, counting each listed ray exactly once.
Exit status 0 if every check passes, 1 otherwise.
Usage: python3 verify_box_cert.py CERT.json
"""
import sys, json
from fractions import Fraction as Fr


def F(*x):
    return Fr(*x)


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def mat_inv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    assert d != 0
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def bil(v, A, w):
    return sum(v[i] * A[i][k] * w[k] for i in range(2) for k in range(2))


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: %s' % key)
        result[key] = value
    return result


def ray_index(key, n):
    j = int(key)
    if not isinstance(key, str) or key != str(j) or not 0 <= j < n:
        raise ValueError('non-canonical or out-of-range ray key: %r' % key)
    return j


def main(path):
    ok = True

    def check(msg, cond):
        nonlocal ok
        ok &= bool(cond)
        print(('PASS ' if cond else 'FAIL ') + msg, flush=True)

    try:
        with open(path) as fh:
            d = json.load(fh, object_pairs_hook=unique_keys)
    except ValueError as e:
        check(str(e), False)
        print('SOME CHECK FAILED')
        return 1
    fam = d['family']
    sb = [F(x) for x in d['sbar']]
    P = [[F(x) for x in p] for p in d['rays']]
    lam = [F(x) for x in d['lam']]
    n = len(P)
    check('lam_hat has exactly one entry per ray', len(lam) == n)
    check('lam_hat is nonnegative', all(x >= 0 for x in lam))
    if not ok:
        print('SOME CHECK FAILED')
        return 1
    q = sb[2] - sb[0] * sb[1]
    check('q(sbar) = %s > 0' % q, q > 0)
    print('family %s, lam_hat = %s, sum = %s' % (fam, [str(x) for x in lam], sum(lam)))
    check('certificate status complete, queue empty', d.get('status') == 'complete' and len(d.get('queue', [1])) == 0)
    Ms = [[sb[2], sb[0]], [sb[1], F(1)]]
    Mi = mat_inv(Ms)
    Nj = [mat_mul(Mi, [[p[2], p[0]], [p[1], F(0)]]) for p in P]
    NE = mat_mul(Mi, [[F(1), F(0)], [F(0), F(0)]])
    m = [Mi[0][0], Mi[1][0]]                       # M(sbar)^{-1} e_1

    # ---- charts, rebuilt here
    half = F(1, 2)
    if fam == 'BP':
        kind = d.get('bpchart', 'pq')
        if kind == 'u':
            # S(u) = [[(1 + u1)/2, u2/2], [u2/2, (1 - u1)/2]], u in [-1, 1]^2 contains the closed unit disk
            charts = [dict(lo=[F(-1)] * 2, hi=[F(1)] * 2,
                           X=lambda t: [[(1 + t[0]) / 2, t[1] / 2], [t[1] / 2, (1 - t[0]) / 2]],
                           disk=lambda t: t[0] ** 2 + t[1] ** 2)]
        else:
            # u1 = t1 - t2, u2 = t1 + t2 - 1; the closed unit disk in u lies in t in [(1-sqrt2)/2, (1+sqrt2)/2]^2
            charts = [dict(lo=[F(-1, 2)] * 2, hi=[F(3, 2)] * 2,
                           X=lambda t: [[(1 + t[0] - t[1]) / 2, (t[0] + t[1] - 1) / 2],
                                        [(t[0] + t[1] - 1) / 2, (1 - t[0] + t[1]) / 2]],
                           disk=lambda t: (t[0] - t[1]) ** 2 + (t[0] + t[1] - 1) ** 2)]
            # the open disk is {2 (t1 - 1/2)^2 + 2 (t2 - 1/2)^2 < 1}: radius^2 1/2 around (1/2, 1/2);
            # the distance from the centre to the chart boundary is 1, so the chart contains it
            check('pq chart contains the disk (identity of the quadratic)',
                  all(((t1 - t2) ** 2 + (t1 + t2 - 1) ** 2) == 2 * (t1 - half) ** 2 + 2 * (t2 - half) ** 2
                      for t1 in (F(0), F(1, 3), F(2)) for t2 in (F(-1), F(1, 7), F(5, 2))))
    else:
        sy = sb[1]
        U = [[F(1), F(0)], [-sy, F(1)]]           # columns u = (1, -sy) and e_2
        Ui = mat_inv(U)
        UiT = [[Ui[0][0], Ui[1][0]], [Ui[0][1], Ui[1][1]]]

        def mkX(i, sg):
            free = [k for k in range(4) if k != i]

            def X(t):
                e = [F(0)] * 4
                e[i] = F(sg)
                for k, tk in zip(free, t):
                    e[k] = tk
                Xt = [[e[0], e[1]], [e[2], e[3]]]
                return mat_mul(mat_mul(UiT, Xt), Ui)
            return X
        charts = []
        for i in range(4):
            for sg in ((1,) if i == 0 else (1, -1)):
                free = [k for k in range(4) if k != i]
                charts.append(dict(lo=[F(0) if k == 0 else F(-1) for k in free], hi=[F(1)] * 3, X=mkX(i, sg)))
        # domain check (by construction): any X with t1 = u^T sym(X) u >= 0, X != 0, has a positive multiple
        # with max_k |t_k| = 1, lying on one of these facets
        # sanity: t1 of the chart map equals u^T sym(X) u
        u = [F(1), -sy]
        Xs = charts[3]['X']([F(1, 3), F(-1, 5), F(2, 7)])
        check('chart sanity: t1 = u^T sym(X) u', bil(u, Xs, u) == F(1, 3))
    check('number of charts %d matches the certificate (%d)' % (len(charts), len(d['charts'])), len(charts) == len(d['charts']))

    # ---- coverage by tree reconstruction
    leaves_by_chart = {}
    for lf in d['leaves']:
        key = (tuple(F(x) for x in lf['lo']), tuple(F(x) for x in lf['hi']))
        leaves_by_chart.setdefault(lf['chart'], {})[key] = lf
    check('no unresolved leaves', all(lf['type'] in ('cut', 'excl', 'skip') for lf in d['leaves']))
    used = d.get('used_charts', list(range(len(charts))))
    check('all charts used', sorted(used) == list(range(len(charts))))
    cover_ok = True
    for c in range(len(charts)):
        lv = leaves_by_chart.get(c, {})
        found = set()
        stack = [(tuple(charts[c]['lo']), tuple(charts[c]['hi']), 0)]
        while stack:
            lo, hi, dep = stack.pop()
            if (lo, hi) in lv:
                found.add((lo, hi))
                continue
            if dep > 80:
                cover_ok = False
                break
            w = [b - a for a, b in zip(lo, hi)]
            k = 0
            for i in range(1, len(w)):
                if w[i] > w[k]:
                    k = i
            mid = (lo[k] + hi[k]) / 2
            hi1 = list(hi); hi1[k] = mid
            lo2 = list(lo); lo2[k] = mid
            stack.append((lo, tuple(hi1), dep + 1))
            stack.append((tuple(lo2), hi, dep + 1))
        cover_ok &= (found == set(lv.keys()))
    check('coverage: bisection trees reach exactly the %d listed leaves' % len(d['leaves']), cover_ok)

    # ---- kept-boundary forms (BP), recomputed
    kbforms = None
    if fam == 'BP':
        import sympy as sp
        a_, b_, c_ = sp.symbols('a b c')
        S_ = sp.Matrix([[a_, b_], [b_, c_]])
        Jm = sp.Matrix([[0, 1], [-1, 0]])
        msym = sp.Matrix([sp.Rational(str(m[0])), sp.Rational(str(m[1]))])
        v_ = Jm * S_ * msym
        kbforms = []
        for N in Nj:
            Ns = sp.Matrix([[sp.Rational(str(x)) for x in r] for r in N])
            num = sp.expand(-(v_.T * S_ * Ns * v_)[0])
            quo, rem = sp.div(sp.Poly(num, a_, b_, c_), sp.Poly(a_ * c_ - b_ ** 2, a_, b_, c_))
            assert rem.is_zero
            Q = sp.Poly(quo.as_expr(), a_, b_, c_)
            kbforms.append(tuple(F(str(Q.coeff_monomial(z))) for z in (a_, b_, c_)))
        den = sp.Poly(sp.expand((msym.T * S_ * msym)[0]), a_, b_, c_)
        kbden = tuple(F(str(den.coeff_monomial(z))) for z in (a_, b_, c_))

    def verts(lo, hi):
        dd = len(lo)
        for mask in range(1 << dd):
            yield [hi[k] if (mask >> k) & 1 else lo[k] for k in range(dd)]

    nbad = 0
    counts = {'cut': 0, 'excl': 0, 'skip': 0}
    for lf in d['leaves']:
        ch = charts[lf['chart']]
        lo = [F(x) for x in lf['lo']]; hi = [F(x) for x in lf['hi']]
        typ = lf['type']
        counts[typ] = counts.get(typ, 0) + 1
        if typ == 'skip':
            # minimum of the convex quadratic disk(t) over the box: check all candidate points
            # (interior critical point, critical points on edges, vertices)
            cands = list(verts(lo, hi))
            for k in range(2):
                for fx in (lo[k], hi[k]):
                    o = 1 - k
                    # restrict to the edge t_k = fx: quadratic g(x); minimize via derivative (exact)
                    def g(x):
                        t = [None, None]; t[k] = fx; t[o] = x
                        return ch['disk'](t)
                    g0, g1, g2 = g(F(0)), g(F(1)), g(F(2))
                    A2 = (g2 - 2 * g1 + g0) / 2
                    B1 = g1 - g0 - A2
                    if A2 > 0:
                        x = -B1 / (2 * A2)
                        if lo[o] <= x <= hi[o]:
                            t = [None, None]; t[k] = fx; t[o] = x
                            cands.append(t)
            # interior critical point of the quadratic: solve grad = 0 by finite differences (exact for quadratics)
            f00 = ch['disk']([F(0), F(0)]); f10 = ch['disk']([F(1), F(0)]); f01 = ch['disk']([F(0), F(1)])
            f20 = ch['disk']([F(2), F(0)]); f02 = ch['disk']([F(0), F(2)]); f11 = ch['disk']([F(1), F(1)])
            H11 = f20 - 2 * f10 + f00; H22 = f02 - 2 * f01 + f00; H12 = f11 - f10 - f01 + f00
            g1_ = f10 - f00 - H11 / 2; g2_ = f01 - f00 - H22 / 2
            det = H11 * H22 - H12 * H12
            if det != 0:
                x1 = (-g1_ * H22 + g2_ * H12) / det
                x2 = (-g2_ * H11 + g1_ * H12) / det
                if lo[0] <= x1 <= hi[0] and lo[1] <= x2 <= hi[1]:
                    cands.append([x1, x2])
            good = min(ch['disk'](t) for t in cands) >= 1
        elif typ == 'excl':
            v = [F(x) for x in lf['v']]
            good = True
            for t in verts(lo, hi):
                X = ch['X'](t)
                good &= bil(v, mat_mul(X, NE), v) >= 0 and bil(v, X, v) < 0
        else:
            total = F(0)
            good = True
            # Missing rays contribute zero because lam_hat is nonnegative.
            # Every listed ray contributes once,
            # using either a fixed vector or a kept-boundary bound.
            try:
                ray_ids = [ray_index(js, n) for js in lf['v']]
                ray_ids += [ray_index(js, n) for js in lf.get('kb', [])]
                if len(ray_ids) != len(set(ray_ids)):
                    raise ValueError('ray counted more than once')
            except (ValueError, TypeError):
                nbad += 1
                continue
            for js, vv in lf['v'].items():
                j = int(js)
                v = [F(x) for x in vv]
                mu = None
                for t in verts(lo, hi):
                    X = ch['X'](t)
                    kept = bil(v, mat_mul(X, NE), v)
                    nn = -bil(v, mat_mul(X, Nj[j]), v)
                    if kept < 0 or nn <= 0:
                        good = False
                        break
                    r = bil(v, X, v) / nn
                    mu = r if mu is None or r > mu else mu
                if not good or mu is None or mu <= 0:
                    good = False
                    break
                total += lam[j] / mu
            for js in lf.get('kb', []):
                j = int(js)
                if kbforms is None:
                    good = False
                    break
                vals = []
                for t in verts(lo, hi):
                    S = ch['X'](t)
                    dn = kbden[0] * S[0][0] + kbden[1] * S[0][1] + kbden[2] * S[1][1]
                    if dn <= 0:
                        good = False
                        break
                    vals.append((kbforms[j][0] * S[0][0] + kbforms[j][1] * S[0][1] + kbforms[j][2] * S[1][1]) / dn)
                if not good or min(vals) <= 0:
                    good = False
                    break
                total += lam[j] * min(vals)
            good &= total >= 1
        if not good:
            nbad += 1
    check('leaf certificates: %s, %d failures' % (counts, nbad), nbad == 0)
    print('ALL PASS' if ok else 'SOME CHECK FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
