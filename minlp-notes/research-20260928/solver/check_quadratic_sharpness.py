"""Targeted exact identities for the fixed quadratic separator obstruction.

These finite checks supplement the all-order proof. They do not establish
the asymptotic theorem, functional-analytic duality, or publication priority.
"""

from fractions import Fraction as F
import sympy as s


def main():
    x, y, z = s.symbols("x y z", real=True)
    f = x*x - 2*x*y + y*y + z*z + 2*y*z
    assert s.expand(f - (y-x+z)**2 - 2*x*z) == 0
    gx, gz = x*(1-x), z*(1-z)
    assert s.expand(x*z - ((x*z)**2 + z*z*gx + x*x*gz + gx*gz)) == 0
    assert s.expand(f.subs({x: y, z: 0})) == 0
    assert s.expand(f.subs({x: 0, z: -y})) == 0

    theta = s.symbols("theta", real=True)
    for k in range(1, 18, 2):
        ck = 2/s.pi * s.integrate(
            s.cos(theta)**2*s.cos(k*theta), (theta, 0, s.pi/2)
        )
        expected = -4*s.sin(k*s.pi/2)/(s.pi*k*(k*k-4))
        assert s.simplify(ck-expected) == 0

    counts = 0
    for n in range(1, 129):
        N = 2*((n+2)//2)
        assert n+1 <= N <= n+2 and N % 2 == 0
        weights = {k: 1-F(abs(k-2*N), N) for k in range(N+1, 3*N)}
        assert all(k > n and w > 0 for k, w in weights.items())
        assert sum(w for k, w in weights.items() if k % 2) == F(N, 2)
        # Integral in the proof multiplied by pi; all its terms are rational.
        integral_times_pi = sum(
            2*w/F(k*(k*k-4)) for k, w in weights.items() if k % 2
        )
        assert integral_times_pi >= F(1, 27*N*N)
        assert integral_times_pi >= F(1, 27*(n+2)**2)
        counts += 1

    # Independently convolve the Fourier coefficients of sin(2Nt) F_N(t).
    # Store each coefficient divided by i, hence rational rather than complex.
    for N in range(2, 34, 2):
        actual = {}
        for j in range(-N+1, N):
            weight = 1-F(abs(j), N)
            actual[j+2*N] = actual.get(j+2*N, F(0)) - weight/2
            actual[j-2*N] = actual.get(j-2*N, F(0)) + weight/2
        expected = {}
        for k in range(N+1, 3*N):
            weight = 1-F(abs(k-2*N), N)
            expected[k], expected[-k] = -weight/2, weight/2
        assert actual == expected
        assert all(abs(k) > N for k in actual)

    print(f"PASS: polynomial identities; 9 exact Fourier coefficients; "
          f"{counts} lower-bound cases; 16 independent Fourier convolutions")


if __name__ == "__main__":
    main()
