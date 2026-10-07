"""Numerical probe: is the hard distance d of Theorem 1 (no-instances) in the cut cone, and is
eps*d in the cut polytope? (LP with scipy/HiGHS, floating point; interpretation aid for probe_gap.py.)

d in CUT-cone  <=>  d = sum_S lambda_S delta(S), lambda >= 0.  eps*d in CUT polytope  <=>  additionally
sum_S eps*lambda_S <= 1 is achievable (minimize sum lambda).  If eps*d is in the cut polytope, no valid
inequality for the cut polytope (in particular no gap inequality) can be violated there.
"""
import itertools
import random
import sys
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_binary_separation import binary_point, build_M, distances, exact_covers, random_exact_cover, random_x3c  # noqa: E402

random.seed(2026)


def cut_cone_lp(D):
    V = len(D)
    pairs = list(itertools.combinations(range(V), 2))
    cuts = []
    for mask in range(1, 2 ** (V - 1)):  # S contains vertex V-1 never; nonempty
        S = {i for i in range(V - 1) if mask >> i & 1}
        cuts.append([1.0 if ((i in S) != (j in S)) else 0.0 for i, j in pairs])
    A = np.array(cuts).T
    b = np.array([float(D[i][j]) for i, j in pairs])
    res = linprog(np.ones(A.shape[1]), A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    return res.status == 0, (res.fun if res.status == 0 else None)


if __name__ == "__main__":
    rows = []
    for trial in range(60):
        if trial < 30:
            p = random.randint(3, 6)
            sets = random_exact_cover(p, nmin=5, nmax=8, plant=False)
        else:
            sets, p = random_x3c(3, extra=random.randint(5, 8))
        if exact_covers(sets, p):
            continue
        M = build_M(sets, p, F(p - 1, 4))
        D = distances(M)
        _, eps, _ = binary_point(M, p)  # eps = 1/(8n+2p+1) since revision r1
        inside, lam = cut_cone_lp(D)
        rows.append((len(sets) + 2, inside, None if lam is None else float(eps) * lam))
        print(f"points={len(sets) + 2} p={p} d in cut cone: {inside}"
              + (f"; min sum lambda * eps = {float(eps) * lam:.4f} (<= 1 means eps*d in CUT polytope)" if inside else ""))
    n_in = sum(r[1] for r in rows)
    n_poly = sum(1 for r in rows if r[1] and r[2] <= 1 + 1e-9)
    print(f"[cut cone probe] {len(rows)} no-instances with 7-10 points: d in cut cone for {n_in}; "
          f"eps*d in cut polytope for {n_poly}")
