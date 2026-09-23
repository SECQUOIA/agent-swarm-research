"""Independent exact checks of signed-marginal core proof boundaries.

No solver, floating point, or repository implementation is imported. The
quintic marginals have both a repeated real critical point and a conjugate
pair of nonreal critical points. Finite checks supplement the written audit.
"""

from fractions import Fraction as F
from itertools import product
import json


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def val(p, x):
    out = F(0)
    for a in reversed(p):
        out = out * x + a
    return out


def cval(p, z):
    """Evaluate with exact Gaussian-rational arithmetic."""
    re = im = F(0)
    x, y = z
    for a in reversed(p):
        re, im = re * x - im * y + a, re * y + im * x
    return re, im


def integrate(p):
    return [F(0)] + [a / (i + 1) for i, a in enumerate(p)]


def merged(intervals):
    out = []
    for a, b in sorted(intervals):
        a, b = max(F(0), a), min(F(1), b)
        if a > b:
            continue
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(b, out[-1][1]))
        else:
            out.append((a, b))
    return out


def run():
    counts = dict(models=0, directed_bregman=0, inverse_modulus=0,
                  critical_points=0, bad_components=0, analytic_panels=0)
    eta = F(1, 8)
    e = eta / 4
    delta = (e / 10) ** 5 / 4
    rho = F(1)
    while rho > min(delta / 24, F(1, 16)):
        rho /= 2
    grid = [F(i, 8) for i in range(9)]
    for a, b, c in product([F(0), F(1, 3), F(1, 2), F(1)],
                           [F(1, 4), F(3, 4)],
                           [F(1, 8), F(1, 1024)]):
        deriv = mul([a*a, -2*a, F(1)], [b*b+c*c, -2*b, F(1)])
        primitive = integrate(deriv)
        scale = val(primitive, F(1))
        assert scale > 0
        g = [x / scale for x in primitive]
        cost = integrate(g)
        counts['models'] += 1
        assert val(g, F(0)) == 0 and val(g, F(1)) == 1
        for u, v in product(grid, repeat=2):
            if u == v:
                continue
            s = abs(u-v)
            increment = abs(val(g, u)-val(g, v))
            assert increment >= (s/10)**5 / 2
            counts['inverse_modulus'] += 1
            divergence = val(cost, u)-val(cost, v)-val(g, v)*(u-v)
            assert divergence >= s**6 / (4*20**5)
            counts['directed_bregman'] += 1

        critical_points = [(a, F(0)), (b, c), (b, -c)]
        critical_values = []
        for z in critical_points:
            assert cval(deriv, z) == (0, 0)
            critical_values.append(cval(g, z))
            counts['critical_points'] += 1
        intervals = [(-rho, rho), (1-rho, 1+rho)]
        intervals += [(re-rho, re+rho) for re, _ in critical_values
                      if -1 <= re <= 2]
        components = merged(intervals)
        for lo, hi in components:
            assert hi-lo <= delta
            counts['bad_components'] += 1
        for (_, lo), (hi, _) in zip(components, components[1:]):
            mid = (lo+hi)/2
            # The reflected half has the same geometric formula; check both.
            for reflect in [False, True]:
                left = lo
                while left < mid:
                    right = min(mid, left+(left-lo+rho)/32)
                    p, q = ((lo+hi-right, lo+hi-left) if reflect
                            else (left, right))
                    tau = (p+q)/2
                    d = min(tau-lo+rho, hi-tau+rho)
                    assert (q-p)/2 <= d/64
                    for re, im in critical_values:
                        assert abs(tau-re) >= d
                        # Every permitted rational-center error retains the
                        # advertised clearance, even toward a critical value.
                        for center in [tau-d/64, tau+d/64]:
                            assert (center-re)**2+im**2 >= (63*d/64)**2
                    assert (q-p)/2+d/64 <= d/32
                    counts['analytic_panels'] += 1
                    left = right
    print(json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    run()
