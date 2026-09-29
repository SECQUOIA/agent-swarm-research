"""Instances for the recheck (independent construction).

h(s) = h_{1/2}(s) = (s-1)^2 ((s+1)^2 + 1/2) = s^4 - 1.5 s^2 - s + 1.5.
"""
import sympy as sp
from iprop import DAG, expanded, in_base, evaluate

X = sp.symbols('x0:3')
HCOEF = [1.5, -1.0, -1.5, 0.0, 1.0]          # h(s) coefficients, degree 0..4


def hpoly(s):
    return sum(c * s ** k for k, c in enumerate(HCOEF))


def endpoint():
    """x^2 as -3x^2 + 2x^2 + 2x^2 (three power nodes) on [-1, 1]."""
    d = DAG(1)
    p = [d.pow(0, 2) for _ in range(3)]
    d.sum(p, [-3, 2, 2])
    return dict(dag=d.nodes, box=[(-1.0, 1.0)], f=X[0] ** 2, syms=[X[0]], fstar=0.0)


def linediag(rep):
    x, y = X[0], X[1]
    f = sp.expand(hpoly(x - y))
    box = [(-2.0, 2.2), (-1.9, 2.1)]
    if rep == 'exp':
        dag = expanded(f, [x, y])
    else:
        d = DAG(2)
        s = d.sum([0, 1], [1, -1])
        ch, co, b = in_base(d, s, HCOEF)
        d.sum(ch, co, b)
        dag = d.nodes
    return dict(dag=dag, box=box, f=f, syms=[x, y], fstar=0.0)


def rot(kappa, rep):
    x, y = X[0], X[1]
    f = sp.expand(hpoly(x - y) + kappa * (x + y - 1) ** 2)
    box = [(-2.0, 2.2), (-1.9, 2.1)]
    if rep == 'exp':
        dag = expanded(f, [x, y])
    else:
        d = DAG(2)
        s = d.sum([0, 1], [1, -1])
        t = d.sum([0, 1], [1, 1], -1.0)
        ch, co, b = in_base(d, s, HCOEF)
        t2 = d.pow(t, 2)
        d.sum(ch + [t2], co + [kappa], b)
        dag = d.nodes
    return dict(dag=dag, box=box, f=f, syms=[x, y], fstar=0.0, xstar=(1.0, 0.0))


def line3_st():
    x0, x1, x2 = X
    f = sp.expand(hpoly(x0 - x1) + (x1 + x2 - 1) ** 2)
    d = DAG(3)
    s = d.sum([0, 1], [1, -1])
    t = d.sum([1, 2], [1, 1], -1.0)
    ch, co, b = in_base(d, s, HCOEF)
    d.sum(ch + [d.pow(t, 2)], co + [1.0], b)
    return dict(dag=d.nodes, box=[(-1.0, 2.2), (-1.9, 1.1), (-0.2, 2.9)], f=f,
                syms=list(X), fstar=0.0)


def iso2():
    x, y = X[0], X[1]
    f = sp.expand((x - 1) ** 2 * ((x + 1) ** 2 + 0.5) + (y - 1) ** 2 * ((y + 1) ** 2 + 0.7))
    return dict(dag=expanded(f, [x, y]), box=[(-2.0, 2.2), (-1.9, 2.3)], f=f,
                syms=[x, y], fstar=0.0, xstar=(1.0, 1.0))


def quad(a):
    """(s-a)^2 as s^2 - 2as + a^2 (terms s^2 and s)."""
    d = DAG(1)
    p = d.pow(0, 2)
    d.sum([p, 0], [1.0, -2.0 * a], a * a)
    return d.nodes


def nondeg1(rep):
    t = X[0]
    f = t ** 2 - 2 * t ** 4
    if rep == 'mono':
        dag = expanded(f, [t])
    else:  # u = t^2, v = u^2, f = u - 2v
        d = DAG(1)
        u = d.pow(0, 2)
        v = d.pow(u, 2)
        d.sum([u, v], [1, -2])
        dag = d.nodes
    return dict(dag=dag, box=[(-1 / 3, 2 / 3)], f=f, syms=[t], fstar=0.0)


def quad_plus_quartic():
    """(x-1)^2 + (x-1)^4 written as x^2 - 2x + 1 + r^4 with r = x - 1.
    The term r^4 is stationary at the minimizer x = 1."""
    d = DAG(1)
    p = d.pow(0, 2)
    r = d.sum([0], [1.0], -1.0)
    q = d.pow(r, 4)
    d.sum([p, 0, q], [1.0, -2.0, 1.0], 1.0)
    return d.nodes


def cnd1():
    """(s-1)^2 (s^2+1) = s^4 - 2s^3 + 2s^2 - 2s + 1 in monomial form.
    Term derivatives at s = 1: 4, -6, 4, -2, so D(1) = 16 - 12 = 4 > 0 (CND)."""
    s = X[0]
    f = sp.expand((s - 1) ** 2 * (s ** 2 + 1))
    return dict(dag=expanded(f, [s]), box=[(-1.0, 3.0)], f=f, syms=[s], fstar=0.0)


def check_rep(I, trials=200, seed=0):
    import random
    rng = random.Random(seed)
    F = sp.lambdify(I['syms'], I['f'])
    err = 0.0
    for _ in range(trials):
        p = [rng.uniform(lo, hi) for lo, hi in I['box']]
        err = max(err, abs(evaluate(I['dag'], p)[-1] - F(*p)))
    return err
