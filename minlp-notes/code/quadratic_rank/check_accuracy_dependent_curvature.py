"""Exact Taylor/midpoint identities and numerical truncated-metric checks.

The numerical integrals support, but do not replace, the analytic proof.
"""
from fractions import Fraction as Q
from math import comb, sqrt
import random
from scipy.integrate import quad
from scipy.optimize import brentq

rng = random.Random(9092026)
exact = numeric = 0
for degree in range(7):
    # f''=(1+x)^degree; integrate twice with zero affine terms.
    coeffs = [Q(comb(degree,k),(k+1)*(k+2)) for k in range(degree+1)]
    f = lambda x: sum(c*x**(k+2) for k,c in enumerate(coeffs))
    derivative = lambda x: sum(c*(k+2)*x**(k+1) for k,c in enumerate(coeffs))
    for _ in range(20):
        aa,bb = sorted(rng.sample(range(33),2))
        a,b = Q(aa,32),Q(bb,32)
        remainder = f(b)-f(a)-derivative(a)*(b-a)
        gap = (f(a)+f(b))/2-f((a+b)/2)
        assert 0 <= remainder <= 8*gap
        exact += 1
        for eps in [0.02,0.2,2.0]:
            A = lambda x: sqrt((1+x)**degree/eps)
            rho = lambda x: min(A(x),(1-x)*A(x)**2)
            threshold = lambda x: (1-x)**2*(1+x)**degree-eps
            peak = max(0.0,(degree-2)/(degree+2))
            segments = sorted(set([float(a),float(b),0.0,peak,1.0]))
            roots = []
            for lo,hi in zip(segments,segments[1:]):
                if threshold(lo)*threshold(hi) < 0:
                    root = brentq(threshold,lo,hi)
                    if float(a)<root<float(b):
                        roots.append(root)
            m = quad(rho,float(a),float(b),points=roots,epsabs=1e-11,epsrel=1e-11)[0]
            E = float(remainder)/eps
            assert E <= m*m+1.5*m+1e-8
            potential = (1-float(b))*A(float(b))-(1-float(a))*A(float(a))
            assert m <= potential+2*E+2*sqrt(2*E)+1e-8
            numeric += 1
print(f'PASS: {exact} exact monotone-curvature Taylor/midpoint bounds; {numeric} branch-split numerical interval-mass and potential checks')
