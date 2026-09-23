"""Exact target recovery with correlated, nonodd, C0 polynomial laws."""
from fractions import Fraction as F
from random import Random


def run():
    rng = Random(904285)
    vertices = [(F(0), F(0)), (F(2), F(0)), (F(1), F(3))]
    roots_checked = recovered = breakpoints_checked = 0
    for case in range(24):
        offsets = [F(0), F(-rng.randrange(1, 4)), F(rng.randrange(1, 4))]
        degree = [1+2*rng.randrange(4) for _ in range(3)]
        breaks = [F(rng.randrange(-3, 4), 2) for _ in range(3)]

        def law(x, theta, edge):
            alpha, gamma = theta
            hinge = max(F(0), x-breaks[edge])-max(F(0), -breaks[edge])
            return x**degree[edge]+(1+alpha)*x+(edge+1)*gamma*hinge

        def h(q, theta):
            return sum(law(q+d, theta, edge) for edge, d in enumerate(offsets))

        for edge in range(3):
            for theta in vertices:
                assert law(F(0), theta, edge) == 0
                x = breaks[edge]
                eps = F(1, 2**40)
                assert law(x-eps, theta, edge) < law(x, theta, edge) < law(x+eps, theta, edge)
                breakpoints_checked += 1
        intervals = []
        for theta in vertices:
            left, right = -max(offsets), -min(offsets)
            while right-left > F(1, 2**45):
                mid = (left+right)/2
                if h(mid, theta) < 0:
                    left = mid
                else:
                    right = mid
            assert h(left, theta) <= 0 <= h(right, theta)
            intervals.append((left, right))
            roots_checked += 1
        max_lower, max_upper = max(a for a, _ in intervals), max(b for _, b in intervals)
        min_lower, min_upper = min(a for a, _ in intervals), min(b for _, b in intervals)
        assert min(h(max_lower, v) for v in vertices) <= 0 <= min(h(max_upper, v) for v in vertices)
        assert max(h(min_lower, v) for v in vertices) <= 0 <= max(h(min_upper, v) for v in vertices)
        for numerator in range(-48, 49):
            q = F(numerator, 32)
            values = [h(q, vertex) for vertex in vertices]
            low_i, high_i = min(range(3), key=values.__getitem__), max(range(3), key=values.__getitem__)
            low, high = values[low_i], values[high_i]
            if low <= 0 <= high:
                lam = -low/(high-low) if high != low else F(0)
                theta = tuple((1-lam)*a+lam*b for a, b in zip(vertices[low_i], vertices[high_i]))
                assert h(q, theta) == 0
                alpha, gamma = theta
                assert gamma >= 0 and gamma <= 3*alpha and gamma <= 3*(2-alpha)
                for edge, d in enumerate(offsets):
                    assert law(F(0), theta, edge) == 0
                recovered += 1
    assert recovered > 20
    print(f'PASS: {roots_checked} exact polynomial root brackets, '
          f'{breakpoints_checked} zero/hinge controls, {recovered} rational target-profile recoveries; degrees1..7')


if __name__ == '__main__':
    run()
