#!/usr/bin/env python3
"""Finite exact stress checks for the quaternion signal estimates.

This is an independent check of selected cases, not a proof of the universal
bounds or of the circuit reduction. Fractions retain all arithmetic exactly.
"""

from fractions import Fraction as F
from itertools import product


def mul(q, r):
    w, x, y, z = q
    a, b, c, d = r
    return (w*a-x*b-y*c-z*d, w*b+x*a+y*d-z*c,
            w*c-x*d+y*a+z*b, w*d+x*c-y*b+z*a)


def inv(q):
    return (q[0], -q[1], -q[2], -q[3])


def rotate(q):
    return (q[0], q[3], q[1], q[2])


def project(q):
    return mul(q, (q[0], q[1], -q[2], -q[3]))


def comm(q, r):
    return mul(mul(mul(q, r), inv(q)), inv(r))


def multiply_signal(q, r):
    return project(rotate(comm(q, rotate(r))))


def norm2(v):
    return sum(a*a for a in v)


def sphere(a):
    aa = norm2(a)
    return ((1-aa)/(1+aa), *(2*b/(1+aa) for b in a))


def error2(q, coefficient, delta, order):
    return norm2((q[1]-coefficient*delta**order, q[2], q[3]))


def assert_unit(q):
    assert norm2(q) == 1


def generator_checks():
    count = 0
    transverse_directions = [(F(1), F(0)), (F(0), F(1)),
                             (F(3, 5), F(4, 5)),
                             (F(3, 5), -F(4, 5))]
    for exponent, amplitude, direction in product(
        [17, 20, 30], [F(0), F(64), F(127999, 1000)],
        transverse_directions,
    ):
        a = F(1, 2**exponent)
        q = sphere((a, amplitude*a*a*direction[0],
                    amplitude*a*a*direction[1]))
        assert_unit(q)
        x = q[1]
        assert q[0] > 0 and 0 < x <= F(1, 2**16)
        assert norm2(q[2:]) <= 64**2*x**4
        u = rotate(comm(q, rotate(q)))
        assert abs(u[1]-2*x*x) <= 65*x**3
        assert x*x <= u[1] <= 3*x*x
        assert norm2(u[1:]) <= 64*x**4
        assert u[0] >= 1-8*x*x > F(1, 2)
        out = project(u)
        assert_unit(out)
        assert x*x <= out[1] <= 6*x*x <= x
        assert norm2(out[2:]) <= 64**2*out[1]**4
        assert out[0] > 0
        count += 1
    return count


def make_signal(c, b, delta, order, direction):
    # Stereographic parametrization; check the signal promise independently.
    target = [c*delta**order, F(0), F(0)]
    for j in range(3):
        target[j] += b*delta**(order+1)*direction[j]/4
    q = sphere(tuple(t/2 for t in target))
    assert_unit(q)
    assert q[0] > 0 and abs(c) <= b
    assert error2(q, c, delta, order) <= (b*delta**(order+1))**2
    return q


def gate_checks():
    count = cancellation_count = 0
    directions = [(F(0), F(0), F(0)), (F(1), F(0), F(0)),
                  (F(0), F(1), F(0)), (F(0), F(0), F(-1)),
                  (F(-1, 3), F(2, 3), F(2, 3))]
    for b in [1, 2, 128, 2**20, 2**40]:
        delta = F(1, 2**max(30, b.bit_length()+10)*b)
        for c, d, a, order_b, direction in product(
            [-b, 0, b], [-b, 0, b], [1, 2], [1, 3], directions,
        ):
            q = make_signal(c, b, delta, a, direction)
            r = make_signal(d, b, delta, order_b,
                            (direction[2], -direction[0], direction[1]))
            out = multiply_signal(q, r)
            assert_unit(out)
            assert out[0] > 0
            assert error2(out, 4*c*d, delta, a+order_b) <= (
                396*b**4*delta**(a+order_b+1))**2
            count += 1
            r_same = make_signal(d, b, delta, a,
                                 (direction[2], -direction[0], direction[1]))
            added = project(mul(q, r_same))
            assert_unit(added)
            assert added[0] > 0
            assert error2(added, 2*(c+d), delta, a) <= (
                144*b**3*delta**(a+1))**2
            if c+d == 0 and added[1] != 0:
                cancellation_count += 1
            projected = project(q)
            assert error2(projected, 2*c, delta, a) <= (
                18*b*b*delta**(a+1))**2
            assert error2(inv(q), -c, delta, a) == error2(q, c, delta, a)
    assert cancellation_count > 0
    return count, cancellation_count


if __name__ == "__main__":
    generators = generator_checks()
    gates, cancellations = gate_checks()
    for t in range(30):
        log_b = (41*4**t-20)//3
        assert log_b == F(41*4**t-20, 3)
        assert 64*4**t >= 30+log_b
    print(f"PASS: {generators} generator cases; {gates} gate cases; "
          f"{cancellations} nonzero residuals after leading-coefficient "
          "cancellation; 30 parameter comparisons.")
