"""Exact finite checks of the infinite-aggregation example.

Run with Python 3; only the standard library is needed. Fractions avoid
floating-point tolerances and Gram matrices avoid numerical square roots.
The checks verify witness identities and finite-family counterexamples.
They do not establish HHC, infinite quantifiers, irreducibility, or novelty;
those assertions have mathematical proofs in the manuscript.
"""

from fractions import Fraction as F


def gram(tau, shift=F(0)):
    """Return (G11, G12, G22) of the manuscript's Gram witness."""
    return 1 - F(1, 10) / tau, F(2, 5) - shift, 1 - tau / 10


def aggregate(entries, multiplier):
    a, h, b = entries
    l1, l2, l3 = multiplier
    return l1 * (a - 1) + l2 * (b - 1) + l3 * (F(1, 2) - h)


def ray(tau):
    return tau, 1 / tau, F(2)


def check_unique_ray_witnesses():
    rays = [F(1) + F(j, 50) for j in range(51)]
    count = 0
    for tau in rays:
        entries = gram(tau)
        a, h, b = entries
        assert min(a, b) >= F(4, 5)
        assert a * b - h * h >= F(12, 25)
        assert a - 1 == -F(1, 10) / tau
        assert b - 1 == -tau / 10
        assert F(1, 2) - h == F(1, 10)
        for other in rays:
            val = aggregate(entries, ray(other))
            assert val == -(other - tau) ** 2 / (10 * tau * other)
            assert (val == 0) == (other == tau)
            count += 1
        for coordinate in ((F(1), F(0), F(0)), (F(0), F(1), F(0))):
            assert aggregate(entries, coordinate) < 0
        # A positive-definite, non-extreme multiplier also has strict slack.
        assert aggregate(entries, (F(1), F(1), F(1))) < 0
    return count


def check_finite_family_perturbations():
    count = 0
    for n in (1, 2, 4, 8, 16, 32):
        selected = [F(1) + F(j, n) for j in range(n + 1)]
        omitted = F(1) + F(1, 2 * n)
        old_entries = gram(omitted)
        slack = min(-aggregate(old_entries, ray(tau)) for tau in selected)
        assert slack > 0
        shift = min(F(1, 10), slack / 4)
        entries = gram(omitted, shift)
        a, h, b = entries
        assert a > 0 and b > 0 and a * b - h * h > 0
        assert all(aggregate(entries, ray(tau)) < 0 for tau in selected)
        assert aggregate(entries, ray(omitted)) == 2 * shift > 0
        # Coordinate inequalities remain strict after the perturbation.
        assert a < 1 and b < 1
        count += 1
    return count


def check_prior_example():
    # DMS's displayed multipliers produce two negative leading eigenvalues.
    for a in (F(1, 4), F(1, 2), F(3, 4)):
        l1, l2, l3 = a * a, (1 - a) ** 2, a * a - a + 1
        assert l1 - l3 == a - 1 < 0
        assert l2 - l3 == -a < 0
    # Compute the actual homogeneous images on y=0, then reconstruct
    # the putative midpoint's squares and product from its coordinates.
    def homogeneous_image(x, t):
        return x*x-t*t, -t*t, -(x-t)**2-(-t)**2+t*t

    first = homogeneous_image(F(1), F(0))
    second = homogeneous_image(F(0), F(1))
    assert first == (F(1), F(0), F(-1))
    assert second == (F(-1), F(-1), F(-1))
    z1, z2, z3 = ((a+b)/2 for a, b in zip(first, second))
    t_squared = -z2
    x_squared = z1+t_squared
    xt = (z3+x_squared+t_squared)/2
    assert x_squared == t_squared == F(1, 2)
    assert xt == 0
    assert x_squared*t_squared != xt*xt


if __name__ == "__main__":
    identities = check_unique_ray_witnesses()
    witnesses = check_finite_family_perturbations()
    check_prior_example()
    print(
        f"PASS: {identities} exact ray identities; {witnesses} finite-family "
        "outside witnesses; coordinate/interior slacks and prior-example algebra"
    )
