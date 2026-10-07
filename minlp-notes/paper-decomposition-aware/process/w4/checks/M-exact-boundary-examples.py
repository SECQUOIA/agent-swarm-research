"""M-exact check 3: identities and constants of Example ex:polylimits and of
Propositions prop:margin and prop:weakcompl (Appendix B.2), with sympy."""
import itertools
import random

import sympy as sp

ok = True


def check(name, cond):
    global ok
    print(('ok   ' if cond else 'FAIL ') + name)
    ok &= bool(cond)


# ex:polylimits (a)
x = sp.symbols('x')
F = x**3 - 6 * x
r2 = sp.sqrt(2)
check('polylimits(a) factorization', sp.expand(F + 4 * r2 - (x - r2)**2 * (x + 2 * r2)) == 0)
check('polylimits(a) x+2sqrt2 >= 3 on [1,2]', float(1 + 2 * r2) >= 3)
# (c) denominators of F(1/2,0)
for k in range(1, 7):
    v = sp.Rational(1, 4) - sp.Rational(1, 2) * sp.Rational(1, 2)**(2**k)
    check(f'polylimits(c) k={k} denominator 2^(2^k+1)', sp.fraction(v)[1] == 2**(2**k + 1))
    xx = sp.symbols('xx')
    d2 = sp.diff(xx**2 - sp.Rational(1, 2) * xx**(2**k), xx, 2)
    check(f'polylimits(c) k={k} d_xx F <= 2 on [0,1]', all(d2.subs(xx, sp.Rational(t, 50)) <= 2 for t in range(51)))

# prop:margin
for n in (1, 2, 3):
    X = sp.symbols(f'x0:{n + 1}')
    y = sp.symbols('y')
    rho = [X[0] - sp.Rational(1, 4)] + [X[i] - sp.Rational(1, 4) * X[i - 1]**2 for i in range(1, n + 1)]
    chi = X[n] - sp.Rational(1, 8) * X[n - 1]**2
    Phi = sum(r**2 for r in rho)
    G = Phi + y**2 + 3 * y * chi
    ident = sp.Rational(1, 4) * (Phi + y**2) + sp.Rational(3, 4) * (Phi - rho[n]**2) + \
        sp.Rational(3, 4) * (rho[n] + y)**2 + sp.Rational(3, 2) * y * X[n]
    check(f'margin n={n} identity', sp.expand(G - ident) == 0)
    a = [sp.Rational(1, 4)]
    for i in range(1, n + 1):
        a.append(a[-1]**2 / 4)
    check(f'margin n={n} a_i formula', all(a[i] == sp.Rational(1, 2**(4 * 2**i - 2)) for i in range(n + 1)))
    sub = {X[i]: a[i] for i in range(n + 1)}
    sub[y] = 0
    check(f'margin n={n} G(a,0)=0', G.subs(sub) == 0)
    check(f'margin n={n} d_y G(a,0) = 3a_n/2', sp.diff(G, y).subs(sub) == sp.Rational(3, 2) * a[n])
    # diagonal second derivatives: max over the box (vertices suffice: each is affine in
    # the squared/linear variables with the signs used in the text) -- sample a fine grid
    diag = [sp.diff(G, v, 2) for v in list(X) + [y]]
    pts = [sp.Rational(t, 8) for t in range(5)]
    mx = max(max(d.subs(dict(zip(list(X) + [y], p))) for p in itertools.product(pts, repeat=n + 2))
             for d in diag)
    check(f'margin n={n} max diagonal second derivative = 35/16 (grid of step 1/8)', mx == sp.Rational(35, 16))
    Hs = sp.hessian(G, list(X) + [y]).subs(sub)
    m2 = Hs.extract([n, n + 1], [n, n + 1])
    check(f'margin n={n} minor on (x_n,y) = -5', m2.det() == -5)
    # growth 9/64: random check of G - 9/64 (|x-a|^2 + y^2) >= 0
    rnd = random.Random(n)
    f = sp.lambdify(list(X) + [y], G - sp.Rational(9, 64) * (sum((X[i] - a[i])**2 for i in range(n + 1)) + y**2))
    mn = min(f(*[rnd.random() / 2 for _ in range(n + 2)]) for _ in range(20000))
    check(f'margin n={n} growth 9/64 (random sample min {mn:.2e})', mn >= -1e-12)

# prop:weakcompl
x, w1, w2 = sp.symbols('x w1 w2')
u = x**2 - sp.Rational(1, 2)
Psi = u**2 + w1**2 + w2**2 + 3 * w1 * w2 + u * (w1 - w2)
check('weakcompl identity', sp.expand(Psi - (sp.Rational(1, 2) * (u**2 + w1**2 + w2**2)
                                             + sp.Rational(1, 2) * (u + w1 - w2)**2 + 4 * w1 * w2)) == 0)
xs = {x: 1 / sp.sqrt(2), w1: 0, w2: 0}
Hs = sp.hessian(Psi, [x, w1, w2]).subs(xs)
v = sp.Matrix([0, 1, -1])
check('weakcompl v^T H v = -2', sp.simplify((v.T * Hs * v)[0]) == -2)
check('weakcompl grad_w = 0 at x*', [sp.simplify(sp.diff(Psi, s).subs(xs)) for s in (w1, w2)] == [0, 0])
check('weakcompl d_xx Psi = 12x^2-2+2(w1-w2)', sp.expand(sp.diff(Psi, x, 2) - (12 * x**2 - 2 + 2 * (w1 - w2))) == 0)

# boundary example (x^2-1/2)^2 + y + x y^2 on [0,1]^2
yy = sp.symbols('yy')
E = (x**2 - sp.Rational(1, 2))**2 + yy + x * yy**2
check('boundary example d_y > 0 on box', sp.simplify(sp.diff(E, yy) - (1 + 2 * x * yy)) == 0)
print('ALL PASS' if ok else 'SOME FAIL')
