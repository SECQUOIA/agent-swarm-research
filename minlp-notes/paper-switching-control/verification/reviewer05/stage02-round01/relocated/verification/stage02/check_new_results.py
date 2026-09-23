"""Exact independent checks for new manuscript consequences and counterexamples.

The n=3 check enumerates all 27 words and all affine cells for their two
switching times. It uses rational polygon feasibility, not a greedy assumption
about repeated modes. This verifies a particular counterexample, not a universal
minimax theorem. The aggregate identities and plateau checks support analytic
proofs in the manuscript.
"""
from fractions import Fraction as F
from itertools import combinations, product


def polygon_feasible(rows):
    """The bounded polygon a*u+b*v<=c is nonempty iff it has a vertex."""
    for (a, b, c), (d, e, f) in combinations(rows, 2):
        det = a * e - b * d
        if not det:
            continue
        u, v = (c * e - b * f) / det, (a * f - c * d) / det
        if all(x * u + y * v <= z for x, y, z in rows):
            return u, v
    return None


def check_n3():
    data = [(0, 0, 0, 0), (146, 98, 48, 0), (194, 110, 48, 36),
            (256, 110, 78, 68), (408, 224, 116, 68),
            (516, 224, 178, 114), (580, 240, 178, 162),
            (971, 417, 309, 245)]
    knots = [(F(row[0], 146), tuple(F(x, 146) for x in row[1:])) for row in data]
    L = F(57, 8)
    t, mass = knots[-1]
    terminal = tuple(m + (L-t)/3 for m in mass)
    knots.append((L, terminal))
    assert terminal == tuple(F(x, 1752) for x in (5281, 3985, 3217))
    assert terminal[0] > 2 and terminal[1] > 2
    segments = []
    for (lo, aa), (hi, bb) in zip(knots, knots[1:]):
        slopes = tuple((b-a)/(hi-lo) for a, b in zip(aa, bb))
        intercepts = tuple(a-m*lo for a, m in zip(aa, slopes))
        assert sum(slopes) == 1 and all(0 <= m <= F(3,4) for m in slopes)
        segments.append((lo, hi, slopes, intercepts))

    # Cross-check the polygon routine on a point, segment, and infeasible box.
    assert polygon_feasible([(F(1), F(0), F(0)), (F(-1), F(0), F(0)),
                             (F(0), F(1), F(0)), (F(0), F(-1), F(0))]) == (0, 0)
    assert polygon_feasible([(F(1), F(0), F(0)), (F(-1), F(0), F(0)),
                             (F(0), F(1), F(1)), (F(0), F(-1), F(0))]) is not None
    assert polygon_feasible([(F(1), F(0), F(0)), (F(-1), F(0), F(-1)),
                             (F(0), F(1), F(1)), (F(0), F(-1), F(0))]) is None
    cells = 0
    for word in product(range(3), repeat=3):
        for first in segments:
            for second in segments:
                lo, hi, mu, bu = first
                vlo, vhi, mv, bv = second
                if vlo < lo:
                    # Only chronological segment indices are needed; common
                    # endpoints occur in the neighboring closed cells as well.
                    continue
                rows = [(F(-1), F(0), -lo), (F(1), F(0), hi),
                        (F(0), F(-1), -vlo), (F(0), F(1), vhi),
                        (F(1), F(-1), F(0))]
                for i in range(3):
                    a, b, c = (int(p == i) for p in word)
                    rows.extend([(a-mu[i], F(0), 1+bu[i]),
                                 (F(a-b), b-mv[i], 1+bv[i]),
                                 (F(a-b), F(b-c), 1+terminal[i]-c*L)])
                assert polygon_feasible(rows) is None, (word, first, second)
                cells += 1
    # Independent exact arithmetic for the middle-service proof in the text.
    for p, Rp, gap in ((0, F(128,73), F(781,876)),
                      (1, F(97,73), F(1057,876))):
        assert L-terminal[p]-1-(F(290,73)-Rp) == gap > 0
    print(f"No error-one schedule: all 27 words, {cells} rational switching-time cells.")
    print("Terminal support and both middle-service contradictions verified exactly.")


def check_identities():
    for n in range(4, 101):
        r = F(n, n-1)
        B2 = n*(r**2-1)
        value = (n-2-F(2,n-2))*B2 + (2*n+F(2*n*n,n-1))/(n-2)
        assert value == n*B2
        if n >= 5:
            B3 = n*(r**3-1)
            value = (n-3-F(3,n-2))*B3 + (3*n+3*n*B2)/(n-2)
            assert value == n*B3
        c2 = 1/(n*(r**3-1))
        assert (c2 < F(1,4)) == (n <= 7)
        if n >= 5:
            c3 = 1/(n*(r**4-1))
            assert (c3 < F(1,5)) == (n <= 11)
            assert (max(F(1,n), c2) < max(F(1,4), c2)) == (5 <= n <= 7)
            assert (max(F(1,n), c3) < max(F(1,5), c3)) == (6 <= n <= 11)
    # Exact coefficient convolution verifies the claimed two asymptotic terms.
    # Numerators and denominators are normalized in x=1/n.
    for numerator, denominator, expansion in [
        ([1,-3,3,-1], [3,-3,1], [F(1,3), F(-2,3), F(2,9)]),
        ([1,-4,6,-4,1], [4,-6,4,-1], [F(1,4), F(-5,8), F(5,16)])]:
        for degree in range(3):
            assert sum(denominator[j]*expansion[degree-j]
                       for j in range(degree+1)) == numerator[degree]
    print("Aggregate substitutions, plateau transitions, equal-mass refinements, and expansions checked.")


def check_pair_counterexamples():
    examples = [
        ([[F(7,15),0,0,0], [F(2,15),F(1,2),0,F(4,5)],
          [F(2,5),F(1,2),1,F(1,5)]], 1, None, [(0,2,2,1),(0,1,2,2)]),
        ([[F(3,5),0,F(1,10),F(2,5),1],
          [F(3,10),F(3,5),F(11,20),F(3,5),0],
          [F(1,10),F(2,5),F(7,20),0,0]], 0, 2, [(0,1,1,0,0)])]
    for rates, forced_mode, forced_position, witnesses in examples:
        M = len(rates[0])
        assert all(sum(rates[i][j] for i in range(3)) == 1 for j in range(M))
        def error(word):
            counts = [0]*3
            cumulative = [F(0)]*3
            value = F(0)
            for j, q in enumerate(word):
                counts[q] += 1
                for i in range(3):
                    cumulative[i] += rates[i][j]
                    value = max(value, abs(cumulative[i]-counts[i]))
            return value
        for word in product(range(3), repeat=M):
            positions = range(M-1) if forced_position is None else [forced_position]
            if any(word[j] == word[j+1] == forced_mode for j in positions):
                assert error(word) > 1
        assert all(error(word) <= 1 for word in witnesses)
    print("Both prescribed-adjacent-pair counterexamples verified by exhaustive word enumeration.")


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run without -O: exact checks require assertions")
    check_n3()
    check_identities()
    check_pair_counterexamples()
