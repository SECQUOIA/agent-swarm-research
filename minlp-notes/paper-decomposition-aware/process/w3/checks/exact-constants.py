"""Targeted checks for Section 6 and Appendix B (exact group, W3).

1. Numerical constants used in the proofs of Corollary cor:local (App. B.1)
   and of Lemma lem:labelfilter / Theorem thm:boundary (App. B.2).
2. Identities and derivative claims of Propositions prop:margin, prop:weakcompl.
3. Height claims on random small mixed box QPs with a unique minimizer:
   x* in rho^{-1}Z with Delta | rho <= R, W <= Omega, delta_X >= 1/R,
   lambda_A >= 1/(Delta R)  (eq:exact-constants, Cor cor:height, Cor cor:local).
"""
import sys
from fractions import Fraction as F
from math import lcm, sqrt
from pathlib import Path
from random import Random

EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
from oracle import exact_minimum  # noqa: E402

ok = True


def check(name, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name)
    ok &= bool(cond)


# 1. constants ------------------------------------------------------------
c17 = sqrt(17 / 15)
check('B.1 integer: 1 > sqrt(17/15)/2', 1 > c17 / 2)
check('B.1 integer: steps h+theta*t <= 1/2+5/4 < 2', F(1, 2) + F(5, 4) < 2)
check('B.1 integer: 1+5.2*(1/2) <= 3.6 and 3.6+1 <= 5', 1 + 5.2 * 0.5 <= 3.6 and 3.6 + 1 <= 5)
check('B.1 delta_X: 5.2/6 < 1 and 6 > sqrt(17/15)', 5.2 / 6 < 1 and 6 > c17)
check('B.1 mu: 5/5.2 >= 1/2', 5 / 5.2 >= 0.5)
check('B.2 labelfilter: 1+10*(1/10) <= 2', 1 + 10 * F(1, 10) <= 2)
check('B.2 labelfilter: 1/10+1/2 < 1', F(1, 10) + F(1, 2) < 1)
check('B.2 labelfilter: (17/15)/100 < 1', F(17, 15) / 100 < 1)
# thm:boundary(b): 2C3 r <= L/(4*4^mu) <= g/32 when 4^mu >= 8 kappa >= 8 L/g
for kappa in [1, 1.5, 2, 7.9, 8, 100, 1e6]:
    mu = 2
    while 4 ** mu < 8 * kappa:
        mu += 1
    check(f'B.2 mu*={mu} for kappa={kappa}: 4^mu <= 32 kappa', 4 ** mu <= 32 * kappa)
check('B.2 patch: 2g - g/32 - g/32 > 0', 2 - 1 / 32 - 1 / 32 > 0)

# 2. polynomial examples ---------------------------------------------------
try:
    import sympy as sp
    for n in (1, 2, 3):
        xs = sp.symbols(f'x0:{n + 1}')
        y = sp.Symbol('y')
        rho = [xs[0] - sp.Rational(1, 4)] + [xs[i] - xs[i - 1] ** 2 / 4 for i in range(1, n + 1)]
        chi = xs[n] - xs[n - 1] ** 2 / 8
        G = sum(r ** 2 for r in rho) + y ** 2 + 3 * y * chi
        Phi = sum(r ** 2 for r in rho)
        ident = (Phi + y ** 2) / 4 + 3 * (Phi - rho[n] ** 2) / 4 + 3 * (rho[n] + y) ** 2 / 4 \
            + sp.Rational(3, 2) * y * xs[n]
        check(f'prop:margin identity n={n}', sp.expand(G - ident) == 0)
        check(f'prop:margin chi=(x_n+rho_n)/2 n={n}', sp.expand(chi - (xs[n] + rho[n]) / 2) == 0)
        a = [sp.Rational(1, 4)]
        for i in range(1, n + 1):
            a.append(a[-1] ** 2 / 4)
        check(f'prop:margin a_i formula n={n}',
              all(a[i] == sp.Rational(1, 2 ** (4 * 2 ** i - 2)) for i in range(n + 1)))
        sub = {xs[i]: a[i] for i in range(n + 1)}
        sub[y] = 0
        check(f'prop:margin grad_y at (a,0) = 3a_n/2 n={n}',
              sp.simplify(sp.diff(G, y).subs(sub) - sp.Rational(3, 2) * a[n]) == 0)
        if n >= 2:
            d2 = sp.diff(G, xs[0], 2)
            check(f'prop:margin d2 x0 = 2+3/4x0^2-x1 n={n}',
                  sp.expand(d2 - (2 + sp.Rational(3, 4) * xs[0] ** 2 - xs[1])) == 0)
        d2 = sp.diff(G, xs[n - 1], 2)
        check(f'prop:margin d2 x_(n-1) = 2+3/4x^2-x_n-3/4y n={n}',
              sp.expand(d2 - (2 + sp.Rational(3, 4) * xs[n - 1] ** 2 - xs[n] - sp.Rational(3, 4) * y)) == 0)
        check(f'prop:margin mixed x_n,y = 3 n={n}', sp.diff(G, xs[n], y) == 3)
    x, w1, w2 = sp.symbols('x w1 w2')
    u = x ** 2 - sp.Rational(1, 2)
    Psi = u ** 2 + w1 ** 2 + w2 ** 2 + 3 * w1 * w2 + u * (w1 - w2)
    ident = (u ** 2 + w1 ** 2 + w2 ** 2) / 2 + (u + w1 - w2) ** 2 / 2 + 4 * w1 * w2
    check('prop:weakcompl identity', sp.expand(Psi - ident) == 0)
    check('prop:weakcompl d2x', sp.expand(sp.diff(Psi, x, 2) - (12 * x ** 2 - 2 + 2 * (w1 - w2))) == 0)
    Hs = sp.hessian(Psi, (x, w1, w2)).subs({x: 1 / sp.sqrt(2), w1: 0, w2: 0})
    v = sp.Matrix([0, 1, -1])
    check('prop:weakcompl v^T H v = -2', sp.simplify((v.T * Hs * v)[0]) == -2)
except ImportError:
    print('sympy missing; skipped part 2')

# 3. heights on random instances ---------------------------------------------


def dens_lcm(vals):
    return lcm(*[F(v).denominator for v in vals])


rng = Random(20261003)
tested = 0
for trial in range(400):
    n = rng.randint(2, 4)
    H = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = F(rng.randint(-6, 6), rng.choice((1, 2, 3)))
        for j in range(i):
            if rng.random() < 0.6:
                H[i][j] = H[j][i] = F(rng.randint(-5, 5), rng.choice((1, 2, 3, 4)))
    b = [F(rng.randint(-6, 6), rng.choice((1, 2, 3, 5))) for _ in range(n)]
    ints = set(rng.sample(range(n), rng.randint(0, 1)))
    bounds = []
    for i in range(n):
        if i in ints:
            lo = rng.randint(-2, 0)
            bounds.append((F(lo), F(lo + rng.randint(1, 2))))
        else:
            lo = F(rng.randint(-3, 0), rng.choice((1, 2, 3)))
            bounds.append((lo, lo + F(rng.randint(1, 3), rng.choice((1, 2)))))
    cst = F(rng.randint(-3, 3), rng.choice((1, 7)))
    val, pts = exact_minimum(H, b, cst, bounds, ints)
    if len(pts) != 1:
        continue
    xs = pts[0]
    tested += 1
    Delta = dens_lcm([H[i][i] / 2 for i in range(n)] + [H[i][j] for i in range(n) for j in range(i + 1, n)]
                     + b + [cst] + [v for bd in bounds for v in bd])
    R = Delta
    for i in range(n):
        if i not in ints and H[i][i] > 0:
            R *= int(Delta * H[i][i])
    Omega = Delta * R * R
    rho = lcm(Delta, dens_lcm(xs))
    check_ok = rho <= R and F(val).denominator <= Omega
    # delta_X over continuous coordinates and coordinates with L_i = 0
    dX = None
    for i in range(n):
        if i not in ints or H[i][i] <= 0:
            for e in bounds[i]:
                if e != xs[i]:
                    d = abs(xs[i] - e)
                    dX = d if dX is None else min(dX, d)
    if dX is not None:
        check_ok &= dX >= F(1, R)
    grad = [sum(H[i][j] * xs[j] for j in range(n)) + b[i] for i in range(n)]
    for i in range(n):
        if i not in ints and H[i][i] > 0 and xs[i] in bounds[i] and grad[i] != 0:
            check_ok &= abs(grad[i]) >= F(1, Delta * R)
    if not check_ok:
        check(f'heights instance {trial}', False)
check(f'heights: rho<=R, W<=Omega, delta_X>=1/R, lambda>=1/(Delta R) on {tested} unique-minimizer instances',
      ok and tested > 50)
print('ALL PASS' if ok else 'SOME FAIL')
