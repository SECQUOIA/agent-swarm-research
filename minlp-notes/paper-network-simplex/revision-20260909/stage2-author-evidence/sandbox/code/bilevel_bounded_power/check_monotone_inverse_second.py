"""Independent exact diagnostics for signed monotone polynomial inverses.

Tests stationary real inverses and nonreal critical values, rational panel
geometry, Taylor composition and denominators, and inverse enclosures.
All numerical certificates use Fraction arithmetic, not floating point.
"""
from fractions import Fraction as F
from math import comb, lcm


def evaluate(coeff, x):
    out = F(0)
    for a in reversed(coeff):
        out = out*x+a
    return out


def mul(a, b, degree):
    out = [F(0)]*(degree+1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b[:degree+1-i]):
            out[i+j] += ai*bj
    return out


def bracket(g, t, width):
    lo, hi = F(0), F(1)
    while hi-lo > width:
        mid = (lo+hi)/2
        if evaluate(g, mid) < t:
            lo = mid
        else:
            hi = mid
    return lo, hi


def inverse_lagrange(a, q):
    # Lagrange inversion: c_n=[u^(n-1)](u/f(u))^n/n.
    reciprocal = [1/a[1]]+[F(0)]*(q-1)
    for n in range(1, q):
        reciprocal[n] = -sum(a[j+1]*reciprocal[n-j]
                             for j in range(1, min(n, len(a)-2)+1))/a[1]
    power = [F(1)]+[F(0)]*(q-1)
    cs = [F(0)]*(q+1)
    for n in range(1, q+1):
        power = mul(power, reciprocal, q-1)
        cs[n] = power[n-1]/n
    return cs


def gaussian_mul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def gaussian_eval(coeff, z):
    out = (F(0), F(0))
    for a in reversed(coeff):
        re, im = gaussian_mul(out, z)
        out = (re+a, im)
    return out


cases = []
for degree in (3, 5):
    # ((2z-1)^D+1)/2 has an interior stationary inverse at target 1/2.
    g = [F(0)]+[F(comb(degree, k)*2**k*(-1)**(degree-k), 2)
                  for k in range(1, degree+1)]
    cases.append(g)
for s in (F(1, 4), F(1, 2**12), F(2**6)):
    a = 3*s*s
    g = [F(0), (3+4*a)/(1+4*a), -6/(1+4*a), 4/(1+4*a)]
    derivative = [k*g[k] for k in range(1, 4)]
    critical = (F(1, 2), s)
    assert gaussian_eval(derivative, critical) == (0, 0)
    value = gaussian_eval(g, critical)
    assert value[0] == F(1, 2) and value[1] != 0
    cases.append(g)

panels_count = centers = coefficient_checks = enclosures = modulus_checks = 0
for g in cases:
    D = len(g)-1
    assert evaluate(g, F(0)) == 0 and evaluate(g, F(1)) == 1
    eta = F(1, 16)
    e = eta/4
    delta = (e/(2*D))**D/4
    rho = F(1, 16)
    while 4*(D+1)*rho > delta:
        rho /= 2
    # All critical real parts in these families equal 1/2.
    gaps = [(rho, F(1, 2)-rho), (F(1, 2)+rho, 1-rho)]
    all_panels = []
    for left, right in gaps:
        middle = (left+right)/2
        half = []
        x = left
        while x < middle:
            y = min(middle, x+(x-left+rho)/32)
            half.append((x, y))
            x = y
        pieces = half+[(left+right-y, left+right-x) for x, y in reversed(half)]
        for x, y in pieces:
            tau = (x+y)/2
            d = min(tau-left+rho, right-tau+rho)
            assert (y-x)/2 <= d/64
            assert abs(tau-F(1, 2)) >= d
        panels_count += len(pieces)
        all_panels.extend((x, y, left, right) for x, y in pieces)
    for index in sorted(set((0, len(all_panels)//4, len(all_panels)//2,
                             len(all_panels)-1))):
        left, right, gap_left, gap_right = all_panels[index]
        tau = (left+right)/2
        d = min(tau-gap_left+rho, gap_right-tau+rho)
        L = max(F(1), sum(k*abs(g[k]) for k in range(1, D+1)))
        lo, hi = bracket(g, tau, d/(64*L))
        z0 = (lo+hi)/2
        t0 = evaluate(g, z0)
        R = d/4
        assert abs(t0-tau) <= d/64
        assert abs(t0-F(1, 2)) >= 63*d/64
        assert abs(t0)+R < 2
        M = 2+(2+sum(abs(a) for a in g[:-1]))/abs(g[-1])
        q = 0
        while 2**q < 4*M/eta:
            q += 1
        shifted = [sum(g[j]*comb(j, h)*z0**(j-h)
                       for j in range(h, D+1)) for h in range(D+1)]
        assert shifted[1] > 0
        cs = inverse_lagrange(shifted, q)
        power = [F(1)]+[F(0)]*q
        composition = [F(0)]*(q+1)
        for h in range(1, min(D, q)+1):
            power = mul(power, cs, q)
            for n in range(q+1):
                composition[n] += shifted[h]*power[n]
        assert composition[1] == 1
        assert all(composition[n] == 0 for n in range(2, q+1))
        Q = lcm(*(a.denominator for a in shifted[1:]))
        A1 = int(Q*shifted[1])
        for n in range(1, q+1):
            assert (cs[n]*A1**(2*n-1)/Q**n).denominator == 1
            assert abs(cs[n])*R**n <= M
            coefficient_checks += 1
        for target in (left, tau, right):
            assert abs(target-t0) <= R/8
            approximation = z0+evaluate(cs, target-t0)
            lo, hi = bracket(g, target, eta/128)
            assert max(abs(approximation-lo), abs(approximation-hi)) <= eta/2
            enclosures += 1
        centers += 1
    for j in range(16):
        h = F(1, 16)
        left = j*h
        mu = evaluate(g, left+h)-evaluate(g, left)
        assert mu >= (h/(2*D))**D/2
        modulus_checks += 1

print('PASS:', panels_count, 'exact panels;', centers, 'Taylor centers;',
      coefficient_checks, 'denominator/Cauchy checks;', enclosures,
      'certified inverse enclosures;', modulus_checks, 'modulus checks;',
      '3 nonreal critical-value pairs')
