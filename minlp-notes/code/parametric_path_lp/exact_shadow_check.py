"""Exact checks of the cited Klee--Minty path support obstruction.

No floating-point hull or LP tolerances: vertices, parameter witnesses,
backward elimination, and envelope breakpoints all use Fraction arithmetic.
"""
from fractions import Fraction as F
from itertools import product


def instance(n):
    eps = F(1, 4)
    coefficients = [eps ** (3 * (n - 1 - i)) for i in range(n - 1)] + [F(0)]
    return eps, coefficients


def vertex(bits, eps):
    previous = F(0)
    values = []
    for bit in bits:
        previous = bit + (1 - 2 * bit) * eps * previous
        values.append(previous)
    return values


def witness(bits, eps):
    n = len(bits)
    suffix = 1
    parameter = F(0)
    for i in range(n - 1, -1, -1):
        suffix *= 1 - 2 * bits[i]
        parameter -= suffix * eps ** (2 * (n - i))
    return parameter


def eliminate(coefficients, parameter, eps):
    effective = coefficients[:]
    effective[-1] += parameter
    for i in range(len(effective) - 2, -1, -1):
        effective[i] -= eps * abs(effective[i + 1])
    return sum(max(F(0), value) for value in effective), effective


def main():
    total_vertices = total_edges = 0
    for n in range(1, 13):
        eps, coefficients = instance(n)
        lines = []
        for bits in product((0, 1), repeat=n):
            x = vertex(bits, eps)
            lam = witness(bits, eps)
            intercept = sum(c * value for c, value in zip(coefficients, x))
            value, effective = eliminate(coefficients, lam, eps)
            assert all(a != 0 and (a > 0) == bool(bit)
                       for a, bit in zip(effective, bits))
            assert value == intercept + lam * x[-1]
            assert -F(1, 15) < lam < F(1, 15)
            lines.append((x[-1], intercept, lam))
        lines.sort()
        assert len({slope for slope, _, _ in lines}) == 2**n
        breaks = [(left[1] - right[1]) / (right[0] - left[0])
                  for left, right in zip(lines, lines[1:])]
        endpoints = [-F(1, 15)] + breaks + [F(1, 15)]
        assert all(a < b for a, b in zip(endpoints, endpoints[1:]))
        for i, (_, _, lam) in enumerate(lines):
            assert endpoints[i] < lam < endpoints[i + 1]
        # The same projected points give a strictly concave scalar-state
        # message F(t), with one segment between every consecutive pair.
        slopes = [(right[1] - left[1]) / (right[0] - left[0])
                  for left, right in zip(lines, lines[1:])]
        assert all(a > b for a, b in zip(slopes, slopes[1:]))
        total_vertices += len(lines)
        total_edges += len(breaks)
        print(f'n={n}: {len(lines)} exposed support pieces, '
              f'{len(breaks)} scalar-state message segments; exact PASS')
    print(f'PASS: {total_vertices} vertex witnesses and {total_edges} ordered breakpoints.')


if __name__ == '__main__':
    main()
