"""Exact checks for degree23-linkage-negative-example.md.

The default checks use SymPy. --singular PATH additionally verifies the
projective ideals, saturation, colon operations, and the elimination polynomial.
No numerical root approximation is used.
"""

from argparse import ArgumentParser
from itertools import combinations_with_replacement, product
from pathlib import Path
import subprocess

import sympy as sp


COEFFICIENTS = [
    35322, 446281, 3018384, 11564409, 18094533, -67552532,
    -639183589, -1244475851, 5950924931, 15175261186,
    -76546491920, -166276862068, 693652544605, 1444377655494,
    -3665631274652, -7553612572726, 12542377095833, 23727902760526,
    -31667595318852, -42645028190069, 61893646405560, 24095940707001,
    -61141031978091, 22501016846117,
]


def power_mod(base, exponent, modulus):
    result = sp.Poly(1, *base.gens, modulus=293)
    while exponent:
        if exponent & 1:
            result = (result * base).rem(modulus)
        base = (base * base).rem(modulus)
        exponent >>= 1
    return result


def check_algebra():
    x0, x1, x2, x3, x4, x5 = xs = sp.symbols("x0:6")
    cube = [(1, *signs, 0, 0) for signs in product((-1, 1), repeat=3)]
    b = (0, 0, 0, 0, 1, 0)
    points = cube + [b]
    ranks = []
    quadratic_evaluation = None
    for degree in range(4):
        monomials = [sp.sympify(sp.prod(xs[j] for j in inds))
                     for inds in combinations_with_replacement(range(6), degree)]
        evaluation = sp.Matrix([
            [m.subs(dict(zip(xs, point))) for m in monomials]
            for point in points
        ])
        ranks.append(evaluation.rank())
        if degree == 2:
            quadratic_evaluation = evaluation
    assert ranks == [1, 5, 8, 9]
    kernel = quadratic_evaluation.T.nullspace()
    assert len(kernel) == 1
    assert kernel[0][-1] == 0 and all(kernel[0][j] for j in range(8))

    A = x1 + 2*x2 + 3*x3
    B = x3 + x4 + x5
    D = 17*x0 + 2*x1 + 3*x2 + 5*x3 + 7*x4 + 11*x5
    quadrics = [
        x1*x1-x0*x0+x4*x2+2*x5*x0,
        x2*x2-x0*x0+x4*x3+3*x5*x1,
        x3*x3-x0*x0+x4*x1+5*x5*x2,
        x4*x0+x5*B,
        x4*A+x5*D,
    ]
    g = sp.expand(x0*D-A*B-7*quadrics[3]+quadrics[4])
    assert sp.expand(x5*g - (x0+x5)*quadrics[4]
                     + (A+7*x5)*quadrics[3]) == 0
    for point in points:
        at = dict(zip(xs, point))
        assert all(q.subs(at) == 0 for q in quadrics)
        assert sp.Matrix(quadrics).jacobian(xs).subs(at).rank() == 5
    assert all(g.subs(dict(zip(xs, point))) > 0 for point in cube)
    assert g.subs(dict(zip(xs, b))) == 0
    mons2 = [xs[i]*xs[j] for i in range(6) for j in range(i, 6)]
    coeffs = sp.Matrix([[sp.Poly(q, *xs).coeff_monomial(m) for m in mons2]
                       for q in quadrics+[g]])
    assert coeffs.rank() == 6
    print("Hilbert ranks, quadratic dependence, nine Jacobian ranks, and extra quadric: PASS")

    t = sp.symbols("t")
    p = sp.Poly.from_list(COEFFICIENTS, t)
    f = sp.Poly(p, modulus=293).monic()
    assert p.degree() == f.degree() == 23
    z = sp.Poly(t, t, modulus=293)
    frobenius = z
    first = None
    for j in range(23):
        frobenius = power_mod(frobenius, 293, f)
        if j == 0:
            first = frobenius
    # Since 23 is prime, these are precisely the finite-field irreducibility
    # conditions: t^(293^23)=t mod f, gcd(f,t^293-t)=1.
    assert frobenius == z
    assert sp.gcd(f, first-z).degree() == 0
    assert sp.gcd(p, p.diff()).degree() == 0
    assert p.count_roots(-sp.oo, sp.oo) == 3
    print("Eliminant: irreducible modulo 293; squarefree; exactly three real roots: PASS")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--singular", help="Path to the Singular executable")
    args = parser.parse_args()
    check_algebra()
    if args.singular:
        script = Path(__file__).with_suffix(".sing")
        run = subprocess.run([args.singular, "-q", str(script)], check=True,
                             text=True, capture_output=True)
        assert "FAIL" not in run.stdout, run.stdout
        assert "DEGREE23_LINKAGE_PASS" in run.stdout, run.stdout + run.stderr
        print(run.stdout.strip())
    else:
        print("Projective CAS checks not run; supply --singular PATH to include them.")


if __name__ == "__main__":
    main()
