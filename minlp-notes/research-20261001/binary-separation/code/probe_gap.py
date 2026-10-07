"""Numerical probe (box search, NOT a proof): are general gap inequalities violated at the
scaled hard points eps*d of Theorem 1 (eps = 1/(8n+2p+1) since revision r1) for instances WITHOUT an exact cover?

Gap inequality in +-1 form: b^T Z b >= gamma(b)^2 with Z = J - 2 eps D (D = distance matrix of d).
Equivalently sigma(b)^2 - 4 eps Q(b, d) >= gamma(b)^2. We search all b in [-B, B]^V (V = n+2 points),
exactly (integers and Fractions), for X3C-type and random exact-cover instances with small n.
"""
import itertools
import random
import sys
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_binary_separation import binary_point, build_M, distances, exact_covers, random_exact_cover  # noqa: E402

random.seed(99)


def gaps(Bmat):
    """gamma(b) = min_s |s^T b| over s in {+-1}^V, for each row b of Bmat (vectorized)."""
    V = Bmat.shape[1]
    S = np.array(list(itertools.product((1, -1), repeat=V - 1)), dtype=np.int64)
    S = np.hstack([np.ones((S.shape[0], 1), dtype=np.int64), S])
    return np.abs(Bmat @ S.T).min(axis=1)


def probe(sets, p, B):
    M = build_M(sets, p, F(p - 1, 4))
    D = distances(M)
    _, eps, _ = binary_point(M, p)  # eps = 1/(8n+2p+1) since revision r1
    V = len(D)
    D4 = np.array([[int(4 * x) for x in row] for row in D], dtype=np.int64)
    worst = None
    count = 0
    rng = range(-B, B + 1)
    for chunk_start in range(-B, B + 1):
        pts = np.array([(chunk_start,) + t for t in itertools.product(rng, repeat=V - 1)], dtype=np.int64)
        sig = pts.sum(axis=1)
        Q4 = np.einsum("ij,jk,ik->i", pts, D4, pts) // 2  # Q(b, 4d) = b^T D4 b / 2
        g = gaps(pts)
        # violation iff sigma^2 - eps*Q(b,4d) < gamma^2; exact integer form with eps = P/R:
        # R*sigma^2 - P*Q(b,4d) < R*gamma^2   (all terms fit in int64 for these sizes)
        P, R = eps.numerator, eps.denominator
        assert P * int(np.abs(Q4).max()) < 2 ** 62 and R * (V * B) ** 2 < 2 ** 62
        viol = np.nonzero(R * sig ** 2 - P * Q4 < R * g ** 2)[0]
        count += len(viol)
        for i in viol:
            if worst is None:
                worst = (tuple(int(t) for t in pts[i]), int(sig[i]), int(g[i]))
    return count, worst, eps


if __name__ == "__main__":
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    nmin = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    trials = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    tested = viol_inst = 0
    for trial in range(trials):
        p = random.randint(3, 6)
        sets = random_exact_cover(p, nmin=nmin, nmax=nmax, plant=False)
        if not (nmin <= len(sets) <= nmax):
            continue
        if exact_covers(sets, p):
            continue
        tested += 1
        count, worst, eps = probe(sets, p, B)
        viol_inst += count > 0
        print(f"n={len(sets)} p={p} eps={eps} violated gap inequalities in box [-{B},{B}]^{len(sets)+2}: "
              f"{count}{'  example b=' + str(worst) if worst else ''}")
    print(f"[gap probe] {tested} no-instances, box B={B}: {viol_inst} with a violated gap inequality")
