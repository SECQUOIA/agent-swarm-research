"""Instances and DAG representations for the cutoff-propagation experiments.

Each instance: sympy objective, root box, f*, a uniform alphaBB constant
alpha (at least half the most negative Hessian eigenvalue on the root box),
and several DAG representations of the *same* function.

  h_c(s) = (s-1)^2 ((s+1)^2 + c) = s^4 + (c-2) s^2 - 2 c s + (1+c)   (min 0 at s=1)
"""
import sympy as sp
import numpy as np
from fbbt import Builder, evaluate


def poly_terms(expr, syms):
    """Flat monomial list of an expanded polynomial: [(coef, {i: e})], const."""
    P = sp.Poly(sp.expand(expr), *syms)
    terms, const = [], 0.0
    for mon, coef in P.terms():
        if all(e == 0 for e in mon):
            const += float(coef)
        else:
            terms.append((float(coef), {i: e for i, e in enumerate(mon) if e}))
    return terms, const


def rep_expanded(expr, syms):
    b = Builder(len(syms))
    terms, const = poly_terms(expr, syms)
    b.poly(terms, const)
    return b.dag()


def rep_univariate_in(b, s_node, expr_in_s, s_sym):
    """Flat monomial sum in an intermediate node s (terms s^k)."""
    P = sp.Poly(sp.expand(expr_in_s), s_sym)
    ch, co, const = [], [], 0.0
    for (k,), coef in P.terms():
        if k == 0:
            const += float(coef)
        elif k == 1:
            ch.append(s_node); co.append(float(coef))
        else:
            ch.append(b.pow(s_node, k)); co.append(float(coef))
    return ch, co, const


S = sp.Symbol('s')


def h(c, s):
    return (s - 1) ** 2 * ((s + 1) ** 2 + c)


def make(name):
    x = sp.symbols('x0:3')
    if name == 'nondeg1':
        # reviewer's instance t^2 - 2 t^4, t in [-1/3, 2/3]
        t = x[0]
        f = t ** 2 - 2 * t ** 4
        box = [(-1 / 3, 2 / 3)]
        reps = {}
        b = Builder(1)                       # u = t^2, v = u^2, f = u - 2v
        u = b.pow(0, 2); v = b.pow(u, 2); b.lin([u, v], [1, -2])
        reps['u'] = b.dag()
        reps['mono'] = rep_expanded(f, [t])  # t^2 and t^4 as separate powers
        return dict(name=name, syms=[t], f=f, box=box, fstar=0.0, alpha=13 / 3, reps=reps,
                    xstar=[0.0])
    if name == 'nondeg1s':
        # same function shifted: y = t + 1/3 in [0, 1]
        y = x[0]
        tt = y - sp.Rational(1, 3)
        f = tt ** 2 - 2 * tt ** 4
        box = [(0.0, 1.0)]
        reps = {}
        b = Builder(1)
        t = b.lin([0], [1], -1 / 3); u = b.pow(t, 2); v = b.pow(u, 2); b.lin([u, v], [1, -2])
        reps['centered'] = b.dag()
        reps['exp'] = rep_expanded(f, [y])
        return dict(name=name, syms=[y], f=f, box=box, fstar=0.0, alpha=13 / 3, reps=reps,
                    xstar=[1 / 3])
    if name.startswith('quad1'):
        # (s-a)^2 expanded, a = 1, s in [0.2, 2.2]: one-sided representation
        s = x[0]
        f = (s - 1) ** 2
        return dict(name=name, syms=[s], f=f, box=[(0.2, 2.2)], fstar=0.0, alpha=0.0,
                    reps={'exp': rep_expanded(f, [s])}, xstar=[1.0])
    if name == 'h1':
        # double well h_{1/2}(s) on s in [0.2, 2.2] (s>0: one-sided), and on [-2, 2.2]
        s = x[0]
        f = h(0.5, s)
        return dict(name=name, syms=[s], f=f, box=[(-2.0, 2.2)], fstar=0.0, alpha=1.5,
                    reps={'exp': rep_expanded(f, [s])}, xstar=[1.0])
    if name == 'linediag':
        X, Y = x[0], x[1]
        f = h(0.5, X - Y)
        box = [(-2.0, 2.2), (-1.9, 2.1)]
        reps = {}
        b = Builder(2)
        s = b.lin([0, 1], [1, -1])
        ch, co, const = rep_univariate_in(b, s, h(0.5, S), S)
        b.lin(ch, co, const)
        reps['s'] = b.dag()
        reps['exp'] = rep_expanded(f, [X, Y])
        return dict(name=name, syms=[X, Y], f=f, box=box, fstar=0.0, alpha=3.0, reps=reps,
                    xstar=None)
    if name == 'iso2':
        X, Y = x[0], x[1]
        f = h(0.5, X) + h(0.7, Y)
        box = [(-2.0, 2.2), (-1.9, 2.3)]
        return dict(name=name, syms=[X, Y], f=f, box=box, fstar=0.0, alpha=1.5,
                    reps={'exp': rep_expanded(f, [X, Y])}, xstar=[1.0, 1.0])
    if name.startswith('rot'):
        # h(x-y) + kappa (x+y-1)^2, isolated minimizer (1,0); name 'rot0.01' etc.
        kappa = float(name[3:])
        X, Y = x[0], x[1]
        f = h(0.5, X - Y) + kappa * (X + Y - 1) ** 2
        box = [(-2.0, 2.2), (-1.9, 2.1)]
        reps = {}
        b = Builder(2)
        s = b.lin([0, 1], [1, -1]); t = b.lin([0, 1], [1, 1], -1.0)
        ch, co, const = rep_univariate_in(b, s, h(0.5, S), S)
        t2 = b.pow(t, 2)
        b.lin(ch + [t2], co + [kappa], const)
        reps['st'] = b.dag()
        reps['exp'] = rep_expanded(f, [X, Y])
        return dict(name=name, syms=[X, Y], f=f, box=box, fstar=0.0, alpha=3.0, reps=reps,
                    xstar=[1.0, 0.0])
    if name == 'nd2':
        # review's t^2 - 2t^4 in 2D (solver-validation isofbbt2): x0^2 - 2x0^4 + x1^2 - 1.5 x1^4
        X, Y = x[0], x[1]
        f = X ** 2 - 2 * X ** 4 + Y ** 2 - 1.5 * Y ** 4
        box = [(-0.6, 0.55), (-0.55, 0.62)]
        return dict(name=name, syms=[X, Y], f=f, box=box, fstar=0.0, alpha=4.5,
                    reps={'mono': rep_expanded(f, [X, Y])}, xstar=[0.0, 0.0])
    if name == 'iso3':
        X = x
        f = h(0.5, X[0]) + h(0.7, X[1]) + h(0.6, X[2])
        box = [(-2.0, 2.2), (-1.9, 2.3), (-2.1, 2.05)]
        return dict(name=name, syms=list(X), f=f, box=box, fstar=0.0, alpha=1.5,
                    reps={'exp': rep_expanded(f, list(X))}, xstar=[1.0, 1.0, 1.0])
    if name == 'line3':
        # h(x0-x1) + (x1+x2-1)^2: optimal line {x0-x1=1, x1+x2=1}, transversal to all axes
        X = x
        f = h(0.5, X[0] - X[1]) + (X[1] + X[2] - 1) ** 2
        box = [(-1.0, 2.2), (-1.9, 1.1), (-0.2, 2.9)]
        reps = {}
        b = Builder(3)
        s = b.lin([0, 1], [1, -1]); t = b.lin([1, 2], [1, 1], -1.0)
        ch, co, const = rep_univariate_in(b, s, h(0.5, S), S)
        b.lin(ch + [b.pow(t, 2)], co + [1.0], const)
        reps['st'] = b.dag()
        reps['exp'] = rep_expanded(f, list(X))
        return dict(name=name, syms=list(X), f=f, box=box, fstar=0.0, alpha=3.0, reps=reps,
                    xstar=None)
    raise KeyError(name)


def lambdas(inst):
    syms, f = inst['syms'], inst['f']
    grad = [sp.diff(f, v) for v in syms]
    hess = [[sp.diff(g, v) for v in syms] for g in grad]
    F = sp.lambdify(syms, f, 'numpy')
    G = sp.lambdify(syms, grad, 'numpy')
    H = sp.lambdify(syms, hess, 'numpy')
    return F, G, H


def check_reps(inst, trials=200, seed=0):
    """Max |DAG value - f| over random points of the root box, per representation."""
    rng = np.random.default_rng(seed)
    F, _, _ = lambdas(inst)
    out = {}
    for rname, dag in inst['reps'].items():
        err = 0.0
        for _ in range(trials):
            p = [rng.uniform(lo, hi) for lo, hi in inst['box']]
            err = max(err, abs(evaluate(dag, p) - float(F(*p))))
        out[rname] = err
    return out


def min_hessian_eig(inst, grid=81):
    _, _, H = lambdas(inst)
    axes = [np.linspace(lo, hi, grid) for lo, hi in inst['box']]
    best = np.inf
    for p in np.array(np.meshgrid(*axes)).reshape(len(axes), -1).T:
        Hm = np.array(H(*p), dtype=float)
        best = min(best, np.linalg.eigvalsh(Hm).min())
    return best
