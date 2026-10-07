"""Review round 2: independent exact check of Proposition 2.10 on S2-S5,
including the eight zero-parameter cases (note.md, Sec. 2.6).

Does not import the stream's code. Contact lists are built from the note's
table (Sec. 2.6). For each case:
  1. the family member q is in the kernel of the contact system;
  2. all ten 9 x 9 minors are computed and factored; a minor that is nonzero
     on the whole stated locus proves rank 9 there;
  3. exact rank 9 at random rational points of the locus;
  4. each contact point lies on the stated cube face (vertex or edge) for
     the stated range, and q >= 0 on a grid at the sample points
     (sanity check of the family identity; not a proof).
Minor values depend on row order and on the sign of derivative rows, so
they are compared with the note only up to a nonzero constant factor.
"""
import itertools
import random

import sympy as sp

h, d1, d2, d3, k = sp.symbols('h d1 d2 d3 k')
x, y, z = sp.symbols('x y z')
MONS = [sp.Integer(1), x, y, z, x**2, y**2, z**2, x*y, x*z, y*z]
VARS = (x, y, z)


def family(hh, a1, a2, a3, kk):
    L = hh - a1*x - a2*y + a3*z
    D = a1 + a2 - hh
    return sp.expand(L**2 + 2*a3*kk*z*(1 - x - y) + kk*(2*D + kk)*x*y)


def coeffs(p):
    P = sp.Poly(p, x, y, z)
    return sp.Matrix([P.coeff_monomial(m) for m in MONS])


def value_row(pt):
    s = dict(zip(VARS, pt))
    return [m.subs(s) for m in MONS]


def deriv_row(pt, j):
    s = dict(zip(VARS, pt))
    return [sp.diff(m, VARS[j]).subs(s) for m in MONS]


def contact_matrix(contacts):
    rows = []
    for pt, dirs in contacts:
        rows.append(value_row(pt))
        for j in dirs:
            rows.append(deriv_row(pt, j))
    return sp.Matrix(rows)


def cases():
    """(name, substitution, contact list builder, positivity assumptions)."""
    def contacts(hh, a1, a2, a3, kk, kind):
        D = a1 + a2 - hh
        b = ((0, hh/a2, 0), [1])
        c = ((1, 0, (a1 - hh)/a3), [2])
        d = ((0, 1, (a2 - hh)/a3), [2])
        e = ((1, 1, (D + kk)/a3), [2])
        v111 = ((1, 1, 1), [2])
        v0 = ((0, 0, 0), [0, 1])
        v100 = ((1, 0, 0), [0, 2])
        return {'S2': [v0, c, d, e], 'S3': [v100, b, d, e],
                'S4': [v0, c, d, v111], 'S5': [v100, b, d, v111]}[kind]
    out = []
    # generic strata
    out.append(('S2 generic', 'S2', {h: 0}))
    out.append(('S3 generic', 'S3', {h: d1}))
    out.append(('S4 generic', 'S4', {h: 0, d3: d1 + d2 + k}))
    out.append(('S5 generic', 'S5', {h: d1, d3: d2 + k}))
    # zero-parameter cases
    out.append(('S3 h=d1=0', 'S3', {h: 0, d1: 0}))
    out.append(('S5 h=d1=0', 'S5', {h: 0, d1: 0, d3: d2 + k}))
    for z0 in ({d1: 0}, {d2: 0}, {d1: 0, d2: 0}):
        out.append(('S2 ' + str(z0), 'S2', {h: 0, **z0}))
        out.append(('S4 ' + str(z0), 'S4',
                    {h: 0, d3: (d1 + d2 + k).subs(z0), **z0}))
    return out, contacts


def sample(kind, subs, rng):
    """Random rational point of the stated range (k > 0 throughout)."""
    while True:
        vals = {k: sp.Rational(rng.randint(1, 40), rng.randint(1, 40))}
        vals[d1] = sp.Rational(rng.randint(0, 40), rng.randint(1, 40))
        vals[d2] = sp.Rational(rng.randint(0, 40), rng.randint(1, 40))
        for s, v in subs.items():
            if v == 0:
                vals[s] = sp.Integer(0)
        if kind in ('S3', 'S5') and not vals[d1] < vals[d2]:
            continue
        hh = sp.sympify(subs[h]).subs(vals)
        D = vals[d1] + vals[d2] - hh
        if d3 in subs:
            vals[d3] = sp.sympify(subs[d3]).subs(vals)
        else:
            vals[d3] = D + vals[k] + sp.Rational(rng.randint(1, 40), rng.randint(1, 40))
        return vals


def on_face(pt):
    """Return 'vertex', 'edge-interior', or None if outside the cube."""
    if any(c < 0 or c > 1 for c in pt):
        return None
    frac = sum(1 for c in pt if 0 < c < 1)
    return {0: 'vertex', 1: 'edge-interior'}.get(frac, 'other')


def main():
    rng = random.Random(20261003)
    allcases, contacts = cases()
    ok = True
    for name, kind, subs in allcases:
        hh = sp.sympify(h).subs(subs)
        a1, a2, a3 = [sp.sympify(s).subs(subs) for s in (d1, d2, d3)]
        q = family(hh, a1, a2, a3, k)
        cl = contacts(hh, a1, a2, a3, k, kind)
        M = contact_matrix(cl)
        qv = coeffs(q)
        kern = all(sp.simplify(e) == 0 for e in M * qv)
        minors = []
        for j in range(10):
            cols = [c for c in range(10) if c != j]
            minors.append(sp.factor(sp.simplify(M[:, cols].det())))
        print('==', name, '| rows', M.shape[0], '| q in kernel:', kern)
        for j, mnr in enumerate(minors):
            if mnr != 0:
                print('   drop col %d (%s): %s' % (j, MONS[j], mnr))
        # rational samples: exact rank, contact faces, grid nonnegativity
        ranks, faces, gridmin = set(), set(), None
        for _ in range(25):
            vals = sample(kind, subs, rng)
            Mn = M.subs(vals)
            ranks.add(Mn.rank())
            qn = q.subs(vals)
            assert sp.expand(Mn * coeffs(qn)) == sp.zeros(M.shape[0], 1)
            for pt, dirs in cl:
                ptn = tuple(sp.sympify(c).subs(vals) for c in pt)
                f = on_face(ptn)
                faces.add((tuple(str(c) for c in pt), f))
                assert f in ('vertex', 'edge-interior'), (name, pt, ptn)
                assert qn.subs(dict(zip(VARS, ptn))) == 0
            fq = sp.lambdify((x, y, z), qn, 'math')
            g = [i / 12 for i in range(13)]
            m = min(fq(a, b, c) for a, b, c in itertools.product(g, g, g))
            gridmin = m if gridmin is None else min(gridmin, m)
        print('   exact rank at 25 rational points:', sorted(ranks),
              '| grid min of q at those points: %.3g' % gridmin)
        print('   contact faces seen:', sorted(faces))
        ok &= kern and ranks == {9} and gridmin > -1e-12
    print('ALL PASS' if ok else 'FAILURE')


if __name__ == '__main__':
    main()
