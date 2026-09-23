"""Sanity checks for the spatial branch-and-bound lower bound note.

1. OPT(P_n) = 1/4 by vertex enumeration for small n.
2. Chord = McCormick = alphaBB on random intervals.
3. Boxes of the explicit certificate (Proposition 2) are pruned (chord LP >= 1/4 - eps).
4. For random boxes containing a random witness w = 1_H + 1_M/(2m):
   LB(B) <= sum_{i in M} chord_i(1/(2m)), and if LB(B) >= 1/4 - eps then
   |M cap R| > m(1/2 - 2 eps).
5. Root RLT+SDP has value 0 for n >= 2k+1, or n=2k with k>=2.
   Additional exact checks below identify all failing pairs.
Run: conda activate minlp-notes; python check_lower_bound.py
"""
import itertools
import random
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import linprog


def chord(a, b, x):
    return a * b + (1 - a - b) * x


def chord_lp(box, k):
    """min sum chord_i(x_i) s.t. sum x = k + 1/2, x in box.  None if infeasible."""
    n = len(box)
    c = np.array([1 - a - b for a, b in box], dtype=float)
    const = sum(a * b for a, b in box)
    res = linprog(c, A_eq=np.ones((1, n)), b_eq=[k + 0.5], bounds=box, method="highs")
    if res.status != 0:
        return None
    return res.fun + const


def check_opt(n, k):
    best = None
    # vertices: n-1 coordinates in {0,1}, one coordinate free; enumerate
    for free in range(n):
        for bits in itertools.product((0, 1), repeat=n - 1):
            s = sum(bits)
            v = Fr(2 * k + 1, 2) - s
            if 0 <= v <= 1:
                val = v * (1 - v)
                best = val if best is None else min(best, val)
    assert best == Fr(1, 4), (n, k, best)


def check_chord_forms(rng, trials=200):
    for _ in range(trials):
        a, b = sorted(rng.random() for _ in range(2))
        x = a + (b - a) * rng.random()
        # McCormick on w = x*y, y = 1-x in [1-b, 1-a]
        yl, yu = 1 - b, 1 - a
        y = 1 - x
        mc = max(a * y + yl * x - a * yl, b * y + yu * x - b * yu)
        abb = x * (1 - x) - (x - a) * (b - x)
        assert abs(mc - chord(a, b, x)) < 1e-12 and abs(abb - chord(a, b, x)) < 1e-12


def check_certificate(n, k, eps):
    alpha = (1 - (1 - 4 * (0.25 - eps)) ** 0.5) / 2  # alpha(1-alpha) = 1/4 - eps
    assert abs(alpha * (1 - alpha) - (0.25 - eps)) < 1e-12
    target = 0.25 - eps - 1e-9
    # middle boxes at each depth with arbitrary prefix, and all final leaves
    for depth in range(n):
        for prefix in itertools.product(((0, alpha), (1 - alpha, 1)), repeat=depth):
            box = list(prefix) + [(alpha, 1 - alpha)] + [(0, 1)] * (n - depth - 1)
            lb = chord_lp(box, k)
            assert lb is None or lb >= target, (box, lb)
    for leaf in itertools.product(((0, alpha), (1 - alpha, 1)), repeat=n):
        lb = chord_lp(list(leaf), k)
        assert lb is None or lb >= target, (leaf, lb)


def check_witness_inequalities(rng, n, k, m, z, eps, trials=300):
    assert k + m + z == n
    h = m * (0.5 - 2 * eps)
    pruned_seen = 0
    for _ in range(trials):
        perm = list(range(n))
        rng.shuffle(perm)
        H, M, Z = set(perm[:k]), set(perm[k:k + m]), set(perm[k + m:])
        w = [1.0 if i in H else (1 / (2 * m) if i in M else 0.0) for i in range(n)]
        box = []
        for i in range(n):
            # random interval containing w_i, sometimes touching 0 or 1
            lo = 0.0 if rng.random() < 0.5 else rng.uniform(0, w[i])
            hi = 1.0 if rng.random() < 0.5 else rng.uniform(w[i], 1)
            box.append((lo, hi))
        lb = chord_lp(box, k)
        assert lb is not None
        rhs = sum(chord(box[i][0], box[i][1], 1 / (2 * m)) for i in M)
        assert lb <= rhs + 1e-9, (lb, rhs)
        if lb >= 0.25 - eps:
            pruned_seen += 1
            R = {i for i in range(n) if box[i][0] > 0 or box[i][1] < 1}
            assert len(M & R) > h - 1e-12, (len(M & R), h)
    return pruned_seen


def check_rlt_sdp_root(n, k):
    c = (k + 0.5) / n
    d = (k - 0.5) * c / (n - 1)
    X = d * np.ones((n, n)) + (c - d) * np.eye(n)
    x = c * np.ones(n)
    Mmat = np.block([[np.ones((1, 1)), x[None, :]], [x[:, None], X]])
    assert np.linalg.eigvalsh(Mmat).min() > -1e-12
    assert np.allclose(X.sum(axis=1), (k + 0.5) * x)
    assert (X >= -1e-12).all() and (X <= c + 1e-12).all()
    assert (X >= 2 * c - 1 - 1e-12).all()
    assert abs(x.sum() - X.trace()) < 1e-12


def main():
    rng = random.Random(0)
    for n in range(2, 8):
        for k in range(1, n):
            check_opt(n, k)
    check_chord_forms(rng)
    for n, k in [(4, 2), (5, 2), (6, 3), (7, 3)]:
        for eps in (0.125, 0.05):
            check_certificate(n, k, eps)
    seen = 0
    for (n, k, m, z) in [(6, 2, 2, 2), (9, 3, 3, 3), (8, 3, 2, 3), (10, 4, 4, 2)]:
        for eps in (0.125, 0.02):
            seen += check_witness_inequalities(rng, n, k, m, z, eps)
    for n, k in [(4, 2), (6, 2), (6, 3), (9, 3), (12, 5)]:
        check_rlt_sdp_root(n, k)
    print("all checks passed; pruned random boxes encountered:", seen)


if __name__ == "__main__":
    main()


def check_remark3_condition_exact():
    """X_ij >= x_i + x_j - 1 at the Remark 3 point, exact rationals, under the stated condition."""
    failures = []
    for n in range(2, 13):
        for k in range(1, n):
            c = Fr(2 * k + 1, 2 * n)
            d = (Fr(2 * k - 1, 2) * c) / (n - 1)
            holds = d >= 2 * c - 1
            stated = (n >= 2 * k + 1) or (n == 2 * k and k >= 2)
            assert holds or not stated, (n, k)
            if not holds:
                failures.append((n, k))
    # the condition fails exactly for k = n-1 (which includes (2,1)); record it
    assert failures == [(n, n - 1) for n in range(2, 13)], failures


def remark7_tree_leaves(n, k):
    """Leaves of the Remark 7 tree: branch each coordinate at 1/2, prune at c=k+1 or d=n-k."""
    leaves = []

    def rec(i, c, d, box):
        if c >= k + 1 or d >= n - k:
            leaves.append(list(box))
            return
        assert i < n, "unpruned leaf at full depth"
        rec(i + 1, c, d + 1, box + [(0, 0.5)])
        rec(i + 1, c + 1, d, box + [(0.5, 1)])

    rec(0, 0, 0, [])
    return [leaf + [(0, 1)] * (n - len(leaf)) for leaf in leaves]


def check_remark7(n, k):
    leaves = remark7_tree_leaves(n, k)
    for leaf in leaves:
        lb = chord_lp(leaf, k)
        assert lb is None or lb >= 0.25 - 1e-9, (leaf, lb)
    # Theorem 1's min bound with z = n - k - m for m = 1..n-k-1 never exceeds the leaf count
    eps = 0.0
    for m in range(1, n - k):
        z = n - k - m
        h = m * (0.5 - 2 * eps)
        bound = min((n / (n - k)) ** (h / 2), (n / (n - z)) ** (h / 2))
        assert bound <= len(leaves) + 1e-9, (n, k, m, bound, len(leaves))
    return len(leaves)


if __name__ == "__main__":
    check_remark3_condition_exact()
    counts = {(n, k): check_remark7(n, k) for (n, k) in [(6, 1), (8, 1), (10, 2), (12, 3), (20, 1), (9, 3), (12, 4)]}
    print("remark 3 exact condition ok under the stated (n,k) condition, fails exactly for k=n-1; remark 7 leaf counts:", counts)
