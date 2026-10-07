"""Review r2: check the scope statement of note Section 4 (minor issue 3) against SCIP 10.0.3's Case-4 formulas,
transcribed by hand from nlhdlr_quadratic.c (intercutsComputeCommonQuantities, lines 1144-1209; Case-4 coefficients,
lines 1583-1720):
  kappa = constant - (1/4) sum_{lambda_i != 0} (v_i.b)^2 / lambda_i ,  (constant of the quadratic written as <= 0)
  w(z)  = linear part (coefficient of w included),   xextra = w + kappa + sqrt(1 + kappa^2),  yextra = w + kappa - sqrt(..)
  ||xhat||^2 = sum_{lambda_i > 0} lambda_i dot_i^2 + xextra^2 / (4 norm),  dot_i = v_i.z + v_i.b/(2 lambda_i)
  ||yhat||^2-part: sum_{lambda_i < 0} |lambda_i| dot_i^2 + yextra^2 / (4 norm)
We read off xhat, yhat as vectors (sqrt(lambda) dot, xextra/(2 sqrt(norm))) etc. and check:
  (1) w - xy <= 0 gives xhat = ((x-y)/2, (w+1)/2), yhat = ((x+y)/2, (w-1)/2) up to component signs;
  (2) 2w - 2xy <= 0 gives the formulas of (1) evaluated at (sqrt2 x, sqrt2 y, 2w);
  (3) w - xy - c <= 0 gives kappa = -c (so kappa != 0 for c != 0).
Also: (4) the relative discriminant of (x0 - s)^2 + 1 is -4/(8 x0^2 + 4) (note Section 4, remark on sfree Prop. 6)."""
import sympy as sp

x, y, w, c, x0, s = sp.symbols('x y w c x0 s', real=True)


def scip_quantities(qcoef, wcoef, const):
    """constraint qcoef*(-x*y) + wcoef*w + const <= 0"""
    A = sp.Matrix([[0, -sp.Rational(qcoef, 2)], [-sp.Rational(qcoef, 2), 0]])
    ev = A.eigenvects()
    z = sp.Matrix([x, y])
    xh, yh = [], []
    kappa = const  # no linear terms in x, y: v.b = 0
    norm = sp.sqrt(1 + kappa ** 2)
    for lam, mult, vecs in ev:
        v = vecs[0] / vecs[0].norm()
        dot = (v.T * z)[0]
        if lam > 0:
            xh.append(sp.sqrt(lam) * dot)
        else:
            yh.append(sp.sqrt(-lam) * dot)
    W = wcoef * w
    xh.append((W + kappa + norm) / (2 * sp.sqrt(norm)))
    yh.append((W + kappa - norm) / (2 * sp.sqrt(norm)))
    return [sp.simplify(t) for t in xh], [sp.simplify(t) for t in yh], kappa


def same_up_to_sign(u, v):
    return all(sp.simplify(a - b) == 0 or sp.simplify(a + b) == 0 for a, b in zip(u, v))


ok = True
xh1, yh1, k1 = scip_quantities(1, 1, 0)
t1 = same_up_to_sign(xh1, [(x - y) / 2, (w + 1) / 2]) and same_up_to_sign(yh1, [(x + y) / 2, (w - 1) / 2])
print('(1) w - xy <= 0: xhat =', xh1, ' yhat =', yh1, ' kappa =', k1, ':', 'PASS' if t1 else 'FAIL')
xh2, yh2, k2 = scip_quantities(2, 2, 0)
sub = {x: sp.sqrt(2) * x, y: sp.sqrt(2) * y, w: 2 * w}
t2 = same_up_to_sign(xh2, [t.subs(sub, simultaneous=True) for t in xh1]) and \
    same_up_to_sign(yh2, [t.subs(sub, simultaneous=True) for t in yh1])
print('(2) 2w - 2xy <= 0: xhat =', xh2, ' = (1) at (sqrt2 x, sqrt2 y, 2w):', 'PASS' if t2 else 'FAIL')
xh3, yh3, k3 = scip_quantities(1, 1, -c)
t3 = sp.simplify(k3 + c) == 0
print('(3) w - xy - c <= 0: kappa =', k3, ':', 'PASS' if t3 else 'FAIL')
g = sp.expand((x0 - s) ** 2 + 1)
A_, B_, C_ = g.coeff(s, 2), g.coeff(s, 1), g.coeff(s, 0)
rel = sp.simplify((B_ ** 2 - 4 * A_ * C_) / (B_ ** 2 + sp.Abs(4 * A_ * C_)))
t4 = sp.simplify(rel - (-4 / (8 * x0 ** 2 + 4))) == 0
print('(4) relative discriminant of (x0 - s)^2 + 1 =', rel, ':', 'PASS' if t4 else 'FAIL')
ok = t1 and t2 and t3 and t4
print('ALL PASS' if ok else 'SOME FAIL')
