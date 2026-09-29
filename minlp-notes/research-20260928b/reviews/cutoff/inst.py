"""Reviewer's instances (re-derived from the note's text, not imported)."""
import sympy as sp
from ifbbt import DAG


def h(c, s):
    return (s - 1) ** 2 * ((s + 1) ** 2 + c)


def expanded(expr, syms):
    """Flat sum of monomials; each monomial a product of powers (single use)."""
    d = DAG(len(syms))
    poly = sp.Poly(sp.expand(expr), *syms)
    ch, co, b = [], [], 0.0
    for mon, coef in poly.terms():
        facs = []
        for i, e in enumerate(mon):
            if e == 1:
                facs.append(i)
            elif e > 1:
                facs.append(d.pow(i, e))
        if not facs:
            b += float(coef)
            continue
        node = facs[0]
        for fct in facs[1:]:
            node = d.mul(node, fct)
        ch.append(node); co.append(float(coef))
    d.sum(ch, co, b)
    return d


def univariate_in(d, base, expr, s):
    """Terms s^k of a polynomial in the node `base` (returns ch, co, const)."""
    poly = sp.Poly(sp.expand(expr), s)
    ch, co, b = [], [], 0.0
    for (k,), coef in poly.terms():
        if k == 0:
            b += float(coef)
        elif k == 1:
            ch.append(base); co.append(float(coef))
        else:
            ch.append(d.pow(base, k)); co.append(float(coef))
    return ch, co, b


S = sp.Symbol('s')
X = sp.symbols('x0:3')


def make(name):
    x, y, z = X
    if name == 'nondeg1':
        f = x ** 2 - 2 * x ** 4
        du = DAG(1); u = du.pow(0, 2); v = du.pow(u, 2); du.sum([u, v], [1, -2])
        return dict(f=f, syms=[x], box=[(-1 / 3, 2 / 3)], alpha=13 / 3,
                    reps={'u': du, 'mono': expanded(f, [x])})
    if name == 'nondeg1s':
        t = x - sp.Rational(1, 3)
        f = t ** 2 - 2 * t ** 4
        dc = DAG(1); tt = dc.sum([0], [1], -1 / 3); u = dc.pow(tt, 2); v = dc.pow(u, 2)
        dc.sum([u, v], [1, -2])
        return dict(f=f, syms=[x], box=[(0.0, 1.0)], alpha=13 / 3,
                    reps={'centered': dc, 'exp': expanded(f, [x])})
    if name == 'h1':
        f = h(sp.Rational(1, 2), x)
        return dict(f=f, syms=[x], box=[(-2.0, 2.2)], alpha=1.5, reps={'exp': expanded(f, [x])})
    if name == 'linediag':
        f = h(sp.Rational(1, 2), x - y)
        d = DAG(2); s = d.sum([0, 1], [1, -1])
        ch, co, b = univariate_in(d, s, h(sp.Rational(1, 2), S), S); d.sum(ch, co, b)
        return dict(f=f, syms=[x, y], box=[(-2.0, 2.2), (-1.9, 2.1)], alpha=3.0,
                    reps={'s': d, 'exp': expanded(f, [x, y])})
    if name == 'iso2':
        f = h(sp.Rational(1, 2), x) + h(sp.Rational(7, 10), y)
        return dict(f=f, syms=[x, y], box=[(-2.0, 2.2), (-1.9, 2.3)], alpha=1.5,
                    reps={'exp': expanded(f, [x, y])}, xstar=[1.0, 1.0])
    if name.startswith('rot'):
        kap = sp.nsimplify(name[3:])
        f = h(sp.Rational(1, 2), x - y) + kap * (x + y - 1) ** 2
        d = DAG(2); s = d.sum([0, 1], [1, -1]); t = d.sum([0, 1], [1, 1], -1.0)
        ch, co, b = univariate_in(d, s, h(sp.Rational(1, 2), S), S)
        d.sum(ch + [d.pow(t, 2)], co + [float(kap)], b)
        return dict(f=f, syms=[x, y], box=[(-2.0, 2.2), (-1.9, 2.1)], alpha=3.0,
                    reps={'st': d, 'exp': expanded(f, [x, y])}, xstar=[1.0, 0.0])
    if name == 'nd2':
        f = x ** 2 - 2 * x ** 4 + y ** 2 - sp.Rational(3, 2) * y ** 4
        return dict(f=f, syms=[x, y], box=[(-0.6, 0.55), (-0.55, 0.62)], alpha=4.5,
                    reps={'mono': expanded(f, [x, y])})
    if name == 'line3':
        f = h(sp.Rational(1, 2), x - y) + (y + z - 1) ** 2
        d = DAG(3); s = d.sum([0, 1], [1, -1]); t = d.sum([1, 2], [1, 1], -1.0)
        ch, co, b = univariate_in(d, s, h(sp.Rational(1, 2), S), S)
        d.sum(ch + [d.pow(t, 2)], co + [1.0], b)
        return dict(f=f, syms=[x, y, z], box=[(-1.0, 2.2), (-1.9, 1.1), (-0.2, 2.9)], alpha=3.0,
                    reps={'st': d, 'exp': expanded(f, [x, y, z])})
    raise KeyError(name)
