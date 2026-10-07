from fractions import Fraction as F
from math import factorial
from pathlib import Path
import ast
import numpy as np

u = F(1, 2**53)
eps = F(1, 10**14)
dmax = F(1, 10**6)
def exp_upper(t):
    return sum(t**k / factorial(k) for k in range(30)) + 2*t**30/factorial(30)
alpha = (exp_upper(dmax)-1)/dmax
den = (1-u)**2*(1-eps)
assert 1/den-1 <= eps + F(201,100)*u
assert alpha/den <= F(1000001,1000000)
print('PASS: exact positive-series proof of the affine weight error bound for 0 <= dE <= 1e-6')
print('e^d / ((1-u)^2*(1-eps)) - 1 <= 1.000001*d + eps + 2.01*u')
d = F(1, 10**7)
assert d*d/2 > F(1, 10**27)
print('Counterexample to F-eg-rounding.tex:257: dE=1e-7 satisfies dE<1e-6,')
print('but e^dE - 1 - dE >= dE^2/2 = 5e-15 > 1e-27.')

# Execute only a copied function, extracted from the /tmp source copy.
source = Path(__file__).with_name('kan_bnb_rigexp.py').read_text()
tree = ast.parse(source)
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'minquad')
ns = {'np': np, 'INF': np.inf, 'dn': lambda x: np.nextafter(x, -np.inf), 'up': lambda x: np.nextafter(x, np.inf)}
exec(compile(ast.Module(body=[node], type_ignores=[]), '<copied minquad>', 'exec'), ns)
tiny = np.nextafter(0.0, 1.0)
result = float(ns['minquad'](np.array([0.0]), np.array([0.0]), np.array([-tiny]), np.array([-3.0]), np.array([3.0]))[0])
exact = -F(tiny)*9/2
print('minquad generic subnormal probe: returned bound / minsubnormal =', F(result)/F(tiny))
print('Exact minimum / minsubnormal =', exact/F(tiny))
assert F(result) > exact
print('Generic result is unsafe; this probe is outside the documented evidence for the six KAN searches.')
