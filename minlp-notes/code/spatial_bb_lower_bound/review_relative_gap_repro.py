"""Independent reproduction of the reviewer checks for the relative-gap bound.

Reproduces "Independent numerical and exact checks" in
notes/review-spatial-bb-relative-gap.md (reviewer program never archived) for
the result note results/spatial-bb-relative-gap-exponential-lower-bound.md.
Written 2026-09-25 from the review text and the fractional-cardinality lemma
of results/spatial-bb-higher-sos-exponential-lower-bound.md; it does not use
the committed check_relative_gap.py.

Setting from the review: order r=2, two blocks of t=3 triples (nine variables
each, 18 in total), demand K=7/2, q0=t-2r+2=1.  A block with |R_b|<q0 (R_b
empty) uses the fractional-cardinality functional E_{9,7/2}; a block with
|R_b|>=q0 is evaluated at its witness 1_H + p 1_M, p=1/(2t).  Three cases:
(fractional, fractional), (fractional, evaluation), (evaluation, evaluation).

Per case:
- exact: every demand equality times every monomial of total degree <= 3
  (repeated powers allowed) has zero moment; 2 * C(21,3) = 2,660 identities;
- the 190-index global degree-<=2 moment matrix is PSD: floating-point
  eigenvalues (as the reviewer did) and an exact rational LDL test;
- cross-block localizers (lower slack of a coordinate in block 1 times upper
  slack of a coordinate in block 2, and the mirror), with all global linear
  multipliers (19 indices): PSD by exact LDL and by eigenvalues, for every
  coordinate pair (the review describes one such localizer);
- normalization, first moments in [0,1], and the penalty bound
  sum_i (L[x_i]-L[x_i^2]) <= sum_b |R_b|/(2 q0), exactly.

Run: python review_relative_gap_repro.py
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import comb

import numpy as np

T_, R_ORDER, BLOCKS = 3, 2, 2
SIZE = 3 * T_                      # nine variables per block
N = BLOCKS * SIZE                  # 18 variables
K = Q(2 * T_ + 1, 2)               # 7/2
P = Q(1, 2 * T_)                   # 1/6
Q0 = T_ - 2 * R_ORDER + 2          # 1
WITNESS = [Q(1)] * T_ + [P] * T_ + [Q(0)] * T_   # H, M, Z in this order
# Restricted sets and boxes for evaluation blocks: every restricted interval
# contains the witness value and excludes one endpoint of [0,1].
EVAL_RESTRICTED = [0, 3, 4, 8]     # one H (0), two M (3, 4), one Z (8) coordinate
EVAL_BOX = {0: (Q(3, 4), Q(1)), 3: (P / 3, Q(2, 3)), 4: (Q(1, 12), Q(1, 2)), 8: (Q(0), Q(1, 4))}


def falling(v, a):
    out = Q(1)
    for j in range(a):
        out *= v - j
    return out


def block_moment(kind, local):
    """Moment of a block monomial given as a list of local indices (repeats allowed)."""
    if kind == "frac":
        s = len(set(local))                       # Boolean reduction u_i^2 = u_i
        return falling(K, s) / falling(Q(SIZE), s)
    val = Q(1)
    for i in local:
        val *= WITNESS[i]
    return val


def moment(kinds, mono):
    parts = [[] for _ in range(BLOCKS)]
    for i in mono:
        parts[i // SIZE].append(i % SIZE)
    val = Q(1)
    for b in range(BLOCKS):
        val *= block_moment(kinds[b], parts[b])
    return val


def monomials(deg):
    return [tuple(m) for a in range(deg + 1) for m in combinations_with_replacement(range(N), a)]


def exact_psd(M):
    """Exact PSD test by symmetric Gaussian elimination (zero pivot => zero row)."""
    A = [row[:] for row in M]
    n = len(A)
    for p in range(n):
        piv = A[p][p]
        if piv < 0:
            return False
        if piv == 0:
            if any(A[p][j] != 0 for j in range(p + 1, n)):
                return False
            continue
        rowp = A[p]
        for i in range(p + 1, n):
            if A[i][p] == 0:
                continue
            f = A[i][p] / piv
            rowi = A[i]
            for j in range(p + 1, n):
                if rowp[j]:
                    rowi[j] -= f * rowp[j]
            rowi[p] = Q(0)
    return True


def bounds(kinds):
    out = []
    for b in range(BLOCKS):
        for i in range(SIZE):
            if kinds[b] == "eval" and i in EVAL_BOX:
                out.append(EVAL_BOX[i])
            else:
                out.append((Q(0), Q(1)))
    return out


def run_case(kinds):
    mom = {}

    def L(mono):
        key = tuple(sorted(mono))
        if key not in mom:
            mom[key] = moment(kinds, key)
        return mom[key]

    # exact demand identities
    identities = 0
    for b in range(BLOCKS):
        for m in monomials(2 * R_ORDER - 1):
            lhs = sum(L(m + (b * SIZE + i,)) for i in range(SIZE)) - K * L(m)
            assert lhs == 0, (kinds, b, m, lhs)
            identities += 1
    assert identities == 2 * comb(N + 3, 3)
    # normalization, first moments, penalty
    assert L(()) == 1 and all(0 <= L((i,)) <= 1 for i in range(N))
    sizes = [len(EVAL_RESTRICTED) if k == "eval" else 0 for k in kinds]  # |R_b|
    assert all((k == "eval") == (s >= Q0) for k, s in zip(kinds, sizes))
    restricted = sum(sizes)
    penalty = sum(L((i,)) - L((i, i)) for i in range(N))
    assert penalty <= Q(restricted, 2 * Q0)
    # box membership of evaluation blocks' witness values
    box = bounds(kinds)
    for b in range(BLOCKS):
        if kinds[b] == "eval":
            assert all(box[b * SIZE + i][0] <= WITNESS[i] <= box[b * SIZE + i][1]
                       for i in range(SIZE))
    # full moment matrix
    basis = monomials(R_ORDER)
    M = [[L(I + J) for J in basis] for I in basis]
    eig_min = np.linalg.eigvalsh(np.array(M, dtype=float)).min()
    assert exact_psd(M), kinds
    # cross-block localizers: (x_i - a_i)(b_j - x_j), i in block 0, j in block 1, and mirror
    lin = monomials(1)
    loc_count, loc_eig_min = 0, None
    for i in range(SIZE):
        for j in range(SIZE, N):
            for lo_idx, up_idx in ((i, j), (j, i)):
                a, _ = box[lo_idx]
                _, bb = box[up_idx]
                # g = (x_lo - a)(bb - x_up) = bb x_lo - x_lo x_up - a bb + a x_up
                g = [((lo_idx,), bb), ((lo_idx, up_idx), Q(-1)), ((), -a * bb), ((up_idx,), a)]
                Lg = [[sum(c * L(I + J + S) for S, c in g) for J in lin] for I in lin]
                assert exact_psd(Lg), (kinds, lo_idx, up_idx)
                e = np.linalg.eigvalsh(np.array(Lg, dtype=float)).min()
                loc_eig_min = e if loc_eig_min is None else min(loc_eig_min, e)
                loc_count += 1
    print(f"case {kinds}: {identities} exact demand identities passed; moment matrix "
          f"{len(basis)}x{len(basis)} exact PSD, float min eigenvalue {eig_min:.3e}; "
          f"{loc_count} cross-block localizers {len(lin)}x{len(lin)} exact PSD, float min "
          f"eigenvalue {loc_eig_min:.3e}; penalty {penalty} <= {Q(restricted, 2 * Q0)}")
    return identities


def main():
    assert Q0 == 1 and N == 18 and K == Q(7, 2)
    # exact PSD test sanity: rejects indefinite and zero-pivot-indefinite matrices
    assert not exact_psd([[Q(1), Q(2)], [Q(2), Q(1)]]) and not exact_psd([[Q(0), Q(1)], [Q(1), Q(0)]])
    assert exact_psd([[Q(1), Q(1)], [Q(1), Q(1)]])
    assert len(monomials(2)) == 190 and len(monomials(3)) == 1330
    counts = [run_case(k) for k in (("frac", "frac"), ("frac", "eval"), ("eval", "eval"))]
    print(f"identities per case: {counts} (review reports 2,660 per case)")


if __name__ == "__main__":
    main()
