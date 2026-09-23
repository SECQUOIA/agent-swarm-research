"""Survey of vertices of P_BH(6) outside BQP_6: minimise permuted/switched copies of the paper's
non-BH facets (13)-(15) plus small random perturbations over P_BH(6); rationalise each optimal
vertex, certify membership in P_BH exactly, and record invariants (denominator, rank and det of
M(z), number of tight BH lattice points)."""
import itertools, sys
import numpy as np
import sympy as sp
from fractions import Fraction as Fr
from bh import PBH, pairs, rationalize
from facets import F13, F14, F15, parse
from verify import exact_bh_separation_general, moment_matrix_exact


def transform_ineq(n, a, c, perm, S):
    """Coefficients of the inequality a.z + c >= 0 after permuting variables and switching S."""
    P = pairs(n)
    ax = {perm[i]: a[i] for i in range(n)}
    aX = {tuple(sorted((perm[i], perm[j]))): a[n + k] for k, (i, j) in enumerate(P)}
    # switching x_i -> 1 - x_i for i in S: substitute in the polynomial sum ax x + sum aX x x + c
    poly = {(): Fr(c)}
    def add(key, val):
        key = tuple(sorted(key))
        poly[key] = poly.get(key, 0) + val
    for i, v in ax.items():
        if i in S:
            add((), v); add((i,), -v)
        else:
            add((i,), v)
    for (i, j), v in aX.items():
        ti = [((), 1), ((i,), -1)] if i in S else [((i,), 1)]
        tj = [((), 1), ((j,), -1)] if j in S else [((j,), 1)]
        for ki, si in ti:
            for kj, sj in tj:
                add(ki + kj, v * si * sj)
    na = [poly.get((i,), 0) for i in range(n)] + [poly.get((i, j), 0) for (i, j) in P]
    return [int(t) for t in na], int(poly.get((), 0))


if __name__ == "__main__":
    n = 6
    trials = int(sys.argv[1])
    rng = np.random.default_rng(1)
    P = PBH(n, W0=1, exact=True)
    facets = [parse(F) for F in (F13, F14, F15)]
    seen = {}
    for t in range(trials):
        a, c = facets[rng.integers(3)]
        perm = list(rng.permutation(n))
        S = {i for i in range(n) if rng.random() < 0.5}
        na, nc = transform_ineq(n, a, c, perm, S)
        obj = np.array(na, float) + 1e-3 * rng.standard_normal(len(na))
        val, z = P.minimize(list(obj))
        zr = rationalize(z, maxden=10 ** 4)
        if zr is None or all(t.denominator == 1 for t in zr):
            continue
        key = tuple(zr)
        if key in seen:
            continue
        w, info = exact_bh_separation_general(n, zr)
        M = sp.Matrix(moment_matrix_exact(n, zr)).applyfunc(lambda q: sp.Rational(q.numerator, q.denominator))
        den = max(q.denominator for q in zr)
        seen[key] = (w is None, den, M.rank(), M.det(), info.get("tight_count") if w is None else None,
                     float(np.dot(na, [float(q) for q in zr]) + nc))
    from collections import Counter
    print("distinct fractional vertices:", len(seen))
    print(Counter((v[0], v[1], v[2], str(v[3]), v[4]) for v in seen.values()))
    print("facet values at them:", Counter(round(v[5], 6) for v in seen.values()))
    import json
    json.dump([[str(q) for q in k] for k in seen], open("pbh6_fractional_vertices.json", "w"))
