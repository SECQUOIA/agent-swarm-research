"""Exact data for the three points z13, z14, z15 of P_BH(6) \\ BQP_6 obtained by minimising the
paper's non-BH facets (13)-(15) over P_BH(6).  Verifies membership in P_BH exactly and the
facet values exactly."""
from fractions import Fraction as Fr
import sympy as sp
from verify import exact_bh_separation_general, moment_matrix_exact, value
from facets import F13, F14, F15, parse

Z6 = {
    "z13": [4, 2, 2, 4, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    "z14": [4, 4, 4, 4, 4, 2, 3, 3, 2, 3, 1, 3, 2, 3, 1, 3, 3, 1, 3, 1, 1],
    "z15": [4, 4, 4, 2, 4, 2, 2, 2, 1, 3, 1, 3, 1, 3, 1, 2, 2, 2, 1, 1, 1],
}
POINTS = {k: [Fr(t, 6) for t in v] for k, v in Z6.items()}

if __name__ == "__main__":
    for (k, z), (fn, F) in zip(POINTS.items(), (("(13)", F13), ("(14)", F14), ("(15)", F15))):
        w, info = exact_bh_separation_general(6, z)
        a, c = parse(F)
        M = sp.Matrix(moment_matrix_exact(6, z)).applyfunc(lambda t: sp.Rational(t.numerator, t.denominator))
        print(k, "in P_BH (exact):", w is None, info, " facet", fn, "value:", value(a, c, z),
              " rank M:", M.rank(), " det M:", M.det())
