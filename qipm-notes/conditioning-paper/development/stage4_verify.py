"""Targeted author checks for Stage 4; the manuscript supplies the proofs.

Run with the repository qipm Python environment. No external data or writes.
"""
from decimal import Decimal, localcontext
import json
import math

import numpy as np
from numpy.polynomial.chebyshev import chebval


def derivatives(x, y, direction):
    u, v = direction
    s, t = np.sin(np.log(y)), np.cos(np.log(y))
    a = 2 * (1 + x*x) / (1 - x*x)**2
    b = y**-2 + (1-y)**-2
    grad = np.array([2*x/(1-x*x), -1/y+1/(1-y)])
    hess = np.diag([a, b])
    third = (2/(1-x)**3 - 2/(1+x)**3)*u**3
    third += (-2/y**3 + 2/(1-y)**3)*v**3
    pg = np.array([s, x*t/y])
    ph = np.array([[0, t/y], [t/y, -x*(s+t)/y**2]])
    pt = -3*(s+t)*u*v*v/y**2+x*(3*s+t)*v**3/y**3
    return 4*(grad+.01*pg), 4*(hess+.01*ph), 4*(third+.01*pt)


def derivative_checks():
    rng = np.random.default_rng(4062026)
    max_sc, max_gradient, max_third_fd = 0., 0., 0.
    for _ in range(2000):
        x = rng.uniform(-.999, .999)
        y = 10**rng.uniform(-8, -.01)
        if rng.random() < .5:
            y = 1-y
        a = 2*(1+x*x)/(1-x*x)**2
        b = y**-2+(1-y)**-2
        h = rng.normal(size=2)/np.sqrt([a,b])
        h /= np.sqrt(a*h[0]**2+b*h[1]**2)
        grad, hess, third = derivatives(x, y, h)
        second = h@hess@h
        assert second > 0
        max_sc = max(max_sc, abs(third)/(2*second**1.5))
        max_gradient = max(max_gradient, grad@np.linalg.solve(hess, grad))
        step = 1e-4
        hp = derivatives(*(np.array([x,y])+step*h), h)[1]
        hm = derivatives(*(np.array([x,y])-step*h), h)[1]
        third_fd = h@((hp-hm)/(2*step))@h
        max_third_fd = max(max_third_fd, abs(third_fd-third)/(1+abs(third)))
    assert max_sc < 1
    assert max_gradient < 20
    # Finite differences near y=1 have coordinate cancellation at tiny slacks.
    assert max_third_fd < 2e-4
    return dict(samples=2000, seed=4062026, max_sc_ratio=max_sc,
                max_gradient_parameter=max_gradient,
                max_scaled_third_difference=max_third_fd)


def subsequence_checks():
    results = []
    with localcontext() as ctx:
        ctx.prec = 80
        D = Decimal
        pi = D('3.141592653589793238462643383279502884197169399375105820974944592307816406286')
        eps = D('0.01')
        for k in (1, 2, 4, 6):
            g = (-2*pi*k).exp()
            a, b, d = D(2), eps/g, g**-2+(1-g)**-2
            lp = (a+d+((a-d)**2+4*b*b).sqrt())/2
            lm = (a*d-b*b)/lp
            slope = -b/(d-lm)
            weak_rhs = abs(slope)/(1+slope*slope).sqrt()
            strong_rhs = 1/(1+slope*slope).sqrt()
            weak_solution, strong_solution = weak_rhs/(4*lm), strong_rhs/(4*lp)
            relative_error = weak_solution/(weak_solution**2+strong_solution**2).sqrt()
            results.append(dict(k=k, gap=float(g), lambda_weak=float(4*lm),
                                weak_rhs_over_gap=float(weak_rhs/g),
                                weak_solution_over_gap=float(weak_solution/g),
                                strong_solution_over_gap_squared=float(strong_solution/g**2),
                                relative_solution_error=float(relative_error)))
        assert abs(4*lm - 4*(2-eps**2)) < D('1e-28')
        assert abs(weak_rhs/g-eps) < D('1e-28')
        assert abs(relative_error-1) < D('1e-27')
    return results


def log_chebyshev_abs(x, degree):
    x = np.asarray(x)
    result = np.empty_like(x)
    inside = np.abs(x) <= 1
    coefficients = np.zeros(degree+1)
    coefficients[-1] = 1
    with np.errstate(divide='ignore'):
        result[inside] = np.log(np.abs(chebval(x[inside], coefficients)))
    z = degree*np.arccosh(np.abs(x[~inside]))
    result[~inside] = z + np.log1p(np.exp(-2*z))-np.log(2.)
    return result


def log_residual(x, a, b, degree):
    if a == b:
        with np.errstate(divide='ignore'):
            return np.log(np.abs(1-x/a))
    mapped = (a+b-2*x)/(b-a)
    denominator = log_chebyshev_abs(np.array([(a+b)/(b-a)]), degree)[0]
    return log_chebyshev_abs(mapped, degree)-denominator


def polynomial_checks():
    rows = []
    delta = 1e-8
    for a1,b1,a2,b2 in ((1,2,100,400), (1,1,2,2), (1,1.001,1e8,4e8), (1,1.01,1.02,1.03)):
        rho1,rho2,cap = b1/a1,b2/a2,b2/a1
        m1 = math.ceil(.5*math.sqrt(rho1)*math.log(2/delta)) if a1 != b1 else 1
        m2 = math.ceil(math.sqrt(rho2)) if a2 != b2 else 1
        j = math.ceil(m1*math.log2(4*cap)+math.log2(1/delta))
        x = np.r_[np.linspace(a1,b1,1001),np.linspace(a2,b2,1001)]
        logq = log_residual(x,a1,b1,m1)+j*log_residual(x,a2,b2,m2)
        maximum = float(np.exp(np.max(logq)))
        assert maximum <= delta*(1+1e-10)
        rows.append(dict(intervals=[a1,b1,a2,b2],degree=m1+j*m2,sampled_supremum=maximum))
    return rows


def schur_checks():
    rng = np.random.default_rng(4062026)
    a = rng.normal(size=(2,5))
    lam = .2
    g = np.eye(5)
    g[:2,:2] = [[(lam+1/lam)/2,(lam-1/lam)/2],[(lam-1/lam)/2,(lam+1/lam)/2]]
    b = 2*np.eye(5)
    gi = np.linalg.inv(g)
    bt = gi.T@b@gi
    at = a@gi
    original = a@np.linalg.solve(b,a.T)
    transformed = at@np.linalg.solve(bt,at.T)
    error = np.linalg.norm(original-transformed)/np.linalg.norm(original)
    assert error < 1e-12
    assert abs(np.linalg.cond(bt)*lam**4-1) < 1e-12
    return dict(relative_schur_error=error, ambient_condition=np.linalg.cond(bt))


if __name__ == '__main__':
    print(json.dumps(dict(derivatives=derivative_checks(),
                          subsequence=subsequence_checks(),
                          polynomials=polynomial_checks(),
                          schur=schur_checks()), indent=2))
