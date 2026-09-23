"""Exact rational checks for the scalar-leader dense SPD box construction."""
from fractions import Fraction as F
from itertools import product
import sympy as sp

vertex_checks = 0
for n in range(1, 9):
    rho = F(1, 100 * 3**n)
    eta = rho**n
    for b in product([0, 1], repeat=n):
        x = sum(F(2*b[i], 3**(i+1)) for i in range(n)) + F(1, 2*3**n)
        residual = [F(b[i])-3**(i+1)*x
                    + 2*sum(3**(i-j)*b[j] for j in range(i))+1
                    for i in range(n)]
        for i in range(n):
            assert abs(residual[i]) >= F(1, 2*3**(n-i-1))
            base_gradient = rho**i*residual[i] + sum(
                2*3**(k-i)*rho**k*residual[k] for k in range(i+1, n))
            assert (1-2*b[i])*base_gradient > rho**i / 3**n
            full_gradient = base_gradient + (4*b[i]-2)*eta
            assert (1-2*b[i])*full_gradient > 0
        # Auxiliary response is p=b, q=1-b. Its gradients obey box KKT.
        for bit in b:
            rp = bit - 2*bit + 1
            rq = (1-bit) + 2*bit - 1
            assert (1-2*bit)*eta*rp >= 0
            assert (1-2*(1-bit))*eta*rq >= 0
        assert n-sum(bit+(1-bit) for bit in b) == 0
        vertex_checks += 1
    # All residuals vanish at the always-feasible midpoint response.
    for i in range(n):
        assert F(1, 2)-F(3**(i+1), 2)+sum(3**(i-j) for j in range(i))+1 == 0

# Independent expanded-Hessian check for the complete quadratic, not only base.
for n in range(1, 5):
    rho = sp.Rational(1, 100*3**n)
    x = sp.Symbol('x')
    ys = sp.symbols(f'y0:{n}')
    ps = sp.symbols(f'p0:{n}')
    qs = sp.symbols(f'q0:{n}')
    variables = ys + ps + qs
    residuals = [ys[i]-3**(i+1)*x+2*sum(3**(i-j)*ys[j] for j in range(i))+1
                 for i in range(n)]
    residuals += [ps[i]-2*ys[i]+1 for i in range(n)]
    residuals += [qs[i]+2*ys[i]-1 for i in range(n)]
    weights = [rho**i for i in range(n)] + [rho**n]*(2*n)
    objective = sum(w*r*r/2 for w, r in zip(weights, residuals))
    hessian = sp.hessian(objective, variables)
    jacobian = sp.Matrix(residuals).jacobian(variables)
    assert jacobian.det() == 1
    assert hessian == jacobian.T * sp.diag(*weights) * jacobian
    _, diagonal = hessian.LDLdecomposition(hermitian=False)
    assert all(diagonal[i, i] > 0 for i in range(3*n))

# All eight distinct-variable clauses on three variables form an unsatisfiable CNF.
# Verify the rounding gap for every feasible point of a rational test grid.
clauses = list(product([0, 1], repeat=3))
gap_checks = 0
for y in product([F(k, 8) for k in range(9)], repeat=3):
    if not all(sum(y[i] if signs[i] else 1-y[i] for i in range(3)) >= 1
               for signs in clauses):
        continue
    p = [max(F(0), 2*value-1) for value in y]
    q = [max(F(0), 1-2*value) for value in y]
    upper = 3-sum(p)-sum(q)
    assert upper == 2*sum(min(value, 1-value) for value in y)
    assert upper >= 2
    gap_checks += 1
print(f'PASS: {vertex_checks} full Boolean-response KKT checks; '
      f'4 expanded SPD Hessians; {gap_checks} unsatisfiable-clause gap checks.')
