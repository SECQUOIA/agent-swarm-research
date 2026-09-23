"""Exact checks of manuscript identities and the bundled complete interface.

Run from the repository root with the solver-lab Python environment. This is
paper validation, not a proof of all checker executions or benchmark results.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'code/minlp_solver_lab'
sys.path.insert(0, str(LAB))
import sympy as sp
from certify.driver import check_certificate

x = sp.symbols('x', real=True)
assert sp.expand(x*x-sp.Rational(1,9) - (sp.Rational(67,100)*x-sp.Rational(203,900))
                 - ((x-sp.Rational(67,200))**2+sp.Rational(799,360000))) == 0
z, a = Q(1,3), Q(67,100)
assert a*z-Q(2,9) == Q(1,900)
d = 2*z-a
W = max(d*z,d*(z-1))
assert d == -Q(1,300) and W == Q(1,450)
assert -a*z-W == -Q(203,900)
assert -Q(3,5)*z-(2*z-Q(3,5))*z == -Q(2,9)

alpha,beta,gamma,delta = sp.symbols('alpha beta gamma delta', nonzero=True)
fraction = (alpha*x+beta)/(gamma*x+delta)
k = beta-alpha*delta/gamma
assert sp.factor(sp.diff(fraction,x,2)-2*k*gamma**2/(gamma*x+delta)**3)==0
v = sp.symbols('v0:3', positive=True)
exponents = sp.symbols('a0:3', real=True)
m = sp.prod(vv**aa for vv,aa in zip(v,exponents))
a_vec = sp.Matrix(exponents)
D = sp.diag(*(1/vv for vv in v))
assert all(sp.simplify(entry)==0 for entry in sp.hessian(m,v)-m*D*(a_vec*a_vec.T-sp.diag(*exponents))*D)

example = LAB / 'certify/examples/quadratic'
result = check_certificate(str(example/'instance.py'),str(example),verbose=False)
assert result['ok'] and Q(result['certified_bound_original_sense'])==Q(1,4),result
assert (Q(0)-Q(1,2))**2 == Q(1,4)
files = ['exact_model.py','convexity.py','safecut.py','driver.py','vipr.py','run_all.py','recheck.py']
output = {
    'exact_checks': ['rounding_example_identity','excluded_feasible_point','finite_box_correction',
                     'halfline_correction','linear_fractional_second_derivative','monomial_hessian_identity'],
    'bundled_replay': result,
    'checker_sources': {name:hashlib.sha256((LAB/'certify'/name).read_bytes()).hexdigest() for name in files},
    'scope':'Exact formula identities and one complete existing bundle; no full benchmark replay or software theorem.'
}
print(json.dumps(output,indent=2))
