"""Independent exact diagnostics for response-constrained accuracy-bit results.

This is not an implementation of algebraic global optimization. The moving
resource examples solve their followers exactly, and all checks use rationals.
"""
from fractions import Fraction as Q


def clip(t):
    return max(Q(0), min(Q(1), t))


def fixed_sum_response(ell, total):
    """Exact water filling, independently solved over multiplier intervals."""
    if total == 0:
        return tuple(Q(0) for _ in ell)
    if total == len(ell):
        return tuple(Q(1) for _ in ell)
    breaks = sorted(set([v for e in ell for v in (e - 1, e)]))
    for left, right in zip(breaks, breaks[1:]):
        mid = (left + right) / 2
        free = [e for e in ell if 0 < e - mid < 1]
        full = sum(e - mid >= 1 for e in ell)
        if free:
            lam = (sum(free) + full - total) / len(free)
            if left <= lam <= right:
                result = tuple(clip(e - lam) for e in ell)
                assert sum(result) == total
                return result
        elif full == total:
            return tuple(clip(e - mid) for e in ell)
    raise AssertionError((ell, total))


def response(x, model):
    ell = (2*x, 2 - 2*x)
    unconstrained = tuple(clip(e) for e in ell)
    if model == 'upper':
        total = min(sum(unconstrained), Q(1, 4) + x)
    elif model == 'equality':
        total = x
    elif model == 'lower':
        total = max(sum(unconstrained), 1 + x)
    else:
        raise AssertionError(model)
    return fixed_sum_response(ell, total)


def infinity(values):
    return max(map(abs, values))


def main():
    counts = {}
    # These three models include changing active box/resource faces, resource
    # equalities, and resource lower bounds. K=1 is a valid infinity-norm repair
    # bound for their single sum (or opposite equal sum) rows. L=4, B_b=1,
    # B_ell=4, mu=1/2 give T=12 and C_z=25, q=2.
    n = 0
    leaders = [Q(i, 40) for i in range(41)]
    for model in ('upper', 'equality', 'lower'):
        values = {x: response(x, model) for x in leaders}
        for x in leaders:
            z = values[x]
            assert all(0 <= zi <= 1 for zi in z)
            if model == 'upper':
                assert sum(z) <= Q(1, 4) + x
            elif model == 'equality':
                assert sum(z) == x
            else:
                assert sum(z) >= 1 + x
            # Check the variational inequality at all rational grid competitors,
            # without reusing the water-filling multiplier classification.
            for a in range(9):
                for b in range(9):
                    y = (Q(a, 8), Q(b, 8))
                    feasible = (sum(y) <= Q(1, 4)+x if model == 'upper'
                                else sum(y) == x if model == 'equality'
                                else sum(y) >= 1+x)
                    if feasible:
                        ell = (2*x, 2-2*x)
                        assert sum((zi-e)*(yi-zi)
                                   for zi, e, yi in zip(z, ell, y)) >= 0
            for xp in leaders:
                zp = values[xp]
                h = abs(x-xp)
                distance = infinity(a-b for a, b in zip(z, zp))
                assert distance**2 <= 25**2*h
                # Check the sharper intermediate repair-plus-growth bound too.
                assert max(Q(0), distance-h)**2 <= 24*h
                # Signed affine upper objective; C_H=3+12*25=303.
                H = lambda u, v: 3*u+5*v[0]-7*v[1]
                assert abs(H(x,z)-H(xp,zp))**2 <= 303**2*h
                n += 1
    counts['moving_resource_response_and_objective_moduli'] = n

    # Nonlinear inverse with zero curvature in the interior. Use exact points
    # x=g(z); no numerical root oracle or positive-coefficient assumption.
    # g(z)=z^3-3z^2/2+3z/4, G=1/4. The signed-polynomial mu is 1/27648.
    n = 0
    g = lambda z: (z-Q(1,2))**3+Q(1,8)
    mu = Q(1, 4)/(4*12**3)
    for z in leaders:
        for zp in leaders:
            assert mu*abs(z-zp)**4 <= abs(g(z)-g(zp))
            n += 1
    counts['interior_zero_curvature_modulus'] = n

    # Convex reduced service constraint a-sqrt(x)<=0 and a signed, nonconvex
    # reduced objective H=-x+2sqrt(x). The exact optimum is H(a^2), and the
    # tightening value is H((a+t)^2) when a+t<=1. This verifies the value modulus
    # against a globally known optimizer, not only a local interpolation point.
    n = 0
    for a in (Q(1,8), Q(1,3), Q(3,4)):
        sigma = 1-a
        H = lambda z: -z*z+2*z
        for j in range(1,41):
            t = sigma*Q(j,40)
            loss = H(a+t)-H(a)
            assert loss >= 0
            assert loss**3 <= 5**3*t/sigma
            n += 1
    counts['convex_service_global_value_modulus'] = n

    # Independently verify the gap obstruction through g(z)-z=z^2(z-1/2).
    # Tightening by t means z>=1/2 and z^2(z-1/2)>=t. Choose a rational z
    # directly: x=g(z) is its exact tightened minimizer by strict monotonicity.
    # For z approaching 1/2, x approaches 1/2 while V(0)=0.
    n = 0
    g_gap = lambda z: z+z*z*(z-Q(1,2))
    previous = Q(2)
    for bits in range(2,101):
        z = Q(1,2)+Q(1,2**bits)
        t = z*z*(z-Q(1,2))
        x = g_gap(z)
        assert 0 < t and Q(1,2) < x <= 1
        assert z-x == -t
        assert x < previous
        assert x-Q(1,2) <= 2*Q(1,2**bits)
        previous = x
        n += 1
    counts['strict_feasibility_global_gap_sequence'] = n

    # Posterior interval with independent extremal signs. Exact outer optimum
    # a may lie far below V, but a<=V+e is sufficient. Inner h differs from a
    # truly feasible objective by at most e. The resulting lower/upper interval
    # must contain V even under adverse rounding signs.
    n = 0
    for V in (Q(-100), Q(0), Q(17,3)):
        for e in (Q(0), Q(1,2**80), Q(7,3)):
            for omega in (Q(1,2**60), Q(1,4), Q(5)):
                for outer_deficit in (Q(0), Q(1), Q(1000)):
                    a = V+e-outer_deficit
                    for rounding_sign in (-1,1):
                        h_out = a+rounding_sign*omega
                        for feasible_loss in (Q(0),Q(13,7)):
                            achieved = V+feasible_loss
                            for response_sign in (-1,1):
                                h_in = achieved+response_sign*e
                                lower = h_out-omega-e
                                upper = h_in+e
                                assert lower <= V <= achieved <= upper
                                n += 1
    counts['posterior_interval_extreme_signs'] = n

    # Polynomial upper rows must be controlled on the enlarged inverse box,
    # including negative surrogate responses and responses above one. Exercise
    # signed mixed monomials and independent leader/response displacements.
    terms = [(Q(3,7), (2,1), (0,0)),
             (Q(-11,3), (1,0), (1,2)),
             (Q(5,2), (0,0), (4,0)),
             (Q(-7,5), (0,3), (2,3)),
             (Q(1,2**30), (2,2), (1,1))]
    Lx = sum(abs(c)*sum(a)*2**sum(b) for c,a,b in terms)
    Lz = sum(abs(c)*sum(b)*2**sum(b) for c,a,b in terms)
    def evaluate(x, z):
        value = Q(0)
        for c, a, b in terms:
            term = c
            for v, exponent in zip(x, a):
                term *= v**exponent
            for v, exponent in zip(z, b):
                term *= v**exponent
            value += term
        return value
    points = [((Q(i % 11,10), Q((3*i) % 11,10)),
               (Q((7*i) % 31,10)-1, Q((11*i) % 31,10)-1))
              for i in range(50)]
    n = 0
    for x,z in points:
        for xp,zp in points:
            difference = abs(evaluate(x,z)-evaluate(xp,zp))
            bound = (Lx*infinity(a-b for a,b in zip(x,xp))
                     + Lz*infinity(a-b for a,b in zip(z,zp)))
            assert difference <= bound
            n += 1
    counts['polynomial_upper_enlarged_box_lipschitz'] = n
    print(counts)
    print('PASS:', sum(counts.values()), 'independent exact cases')


if __name__ == '__main__':
    main()
