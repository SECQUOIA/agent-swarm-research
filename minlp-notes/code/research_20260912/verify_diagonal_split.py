"""Independent dense-formulation checks for diagonal-split certificates.

Written by the implementing researcher. Fresh-agent review is still required.
"""

from fractions import Fraction as Q
import json
from pathlib import Path
import random
import sys

import numpy as np
import sympy as sp

from certify_dense_design import Problem
from certify_diagonal_split import exact_diagonal_point, psd_dual_certificate
from certify_noisy_markov import fraction


def main():
    sys.set_int_max_str_digits(0)
    rng = random.Random(9182)
    counts = {"dense_point_gradient": 0, "psd_dual_construction": 0,
              "exact_toy": 0, "exact_convex_tangents": 0}
    for n in (1, 2, 3, 5):
        for rho in (Q(0), Q(2, 5), Q(-3, 7)):
            for latent in (Q(0), Q(3, 2)):
                p = 2
                F = tuple(tuple(Q(rng.randrange(-9, 10), 3) for _ in range(p)) for _ in range(n))
                prior = ((Q(3, 2), Q(1, 4)), (Q(1, 4), Q(5, 4)))
                problem = Problem(F, prior, rho, latent, Q(3, 4), min(n, 2))
                R = sp.Matrix([[latent*rho**abs(i-j)+(problem.nugget if i == j else 0)
                                for j in range(n)] for i in range(n)])
                for _ in range(4):
                    z = tuple(Q(rng.randrange(5), 4) for _ in range(n))
                    a = tuple(Q(rng.randrange(1, 20), 5) for _ in range(n))
                    J, gradient, determinant = exact_diagonal_point(problem, z, a)
                    selected = [i for i in range(n) if z[i]]
                    if selected:
                        S = R.extract(selected, selected)+sp.diag(*[a[i]*(1-z[i])/z[i] for i in selected])
                        V = S.inv()*sp.Matrix(F).extract(selected, range(p))
                        expected = sp.Matrix(prior)+sp.Matrix(F).extract(selected, range(p)).T*V
                        expected_gradient = [Q(0)]*n
                        for t, i in enumerate(selected):
                            expected_gradient[i] = fraction(-(1-z[i])/z[i]*(V[t, :]*expected.inv()*V[t, :].T)[0])
                    else:
                        expected, expected_gradient = sp.Matrix(prior), [Q(0)]*n
                    assert sp.Matrix(J) == expected
                    assert gradient == tuple(expected_gradient)
                    assert determinant == expected.det()
                    counts["dense_point_gradient"] += 1
                    # Deliberately indefinite numerical Y proposals must still yield exact PSD factors.
                    approximate = np.array([[rng.randrange(-4, 5) for _ in range(n)] for _ in range(n)], dtype=float)
                    dual = psd_dual_certificate(problem, gradient, approximate, grid=1000)
                    B = sp.Matrix(dual["factor"])
                    Y = B*B.T+sp.diag(*dual["diagonal_correction"])
                    assert all(x >= 0 for x in dual["diagonal_correction"])
                    assert all(Y[i, i] >= -gradient[i] for i in range(n))
                    assert (R*Y).trace() == dual["trace_RY"]
                    counts["psd_dual_construction"] += 1
                    # Convexity of the logdet function implies a tangent inequality.
                    # Verify its stronger determinant/exponential form numerically at high precision.
                    b = tuple(Q(rng.randrange(1, 20), 5) for _ in range(n))
                    _, _, determinant_b = exact_diagonal_point(problem, z, b)
                    difference = sp.log(sp.Rational(determinant_b))-sp.log(sp.Rational(determinant))
                    difference -= sum(gradient[i]*(b[i]-a[i]) for i in range(n))
                    assert difference == 0 or difference.evalf(60) > -sp.Float("1e-55")
                    counts["exact_convex_tangents"] += 1
    toy = Problem(((Q(1),), (Q(-1),)), ((Q(1),),), Q(2, 3), Q(3, 2), Q(1, 2), 1)
    J, g, det = exact_diagonal_point(toy, (Q(1, 2),)*2, (Q(1),)*2)
    assert J == ((Q(2),),) and g == (Q(-1, 8),)*2
    R = sp.Matrix([[2, 1], [1, 2]])
    Y = sp.Matrix([[Q(1, 8), Q(-1, 8)], [Q(-1, 8), Q(1, 8)]])
    assert Y.eigenvals() == {sp.Rational(1, 4): 1, sp.Rational(0): 1}
    assert -sum(g)-(R*Y).trace() == 0
    counts["exact_toy"] += 1
    report = {"status": "passed", "scope": "Implementer checks with a separate dense exact formulation", "counts": counts}
    output = Path(__file__).parent/"results/diagonal-split-validation.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
