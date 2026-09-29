"""Check the closed-form integral-convexity criterion for quadratic forms.

Claim (derived in the report): f(x) = x^T Q x (Q symmetric PSD) is integrally
convex on Z^n iff for every d in {0,+-1,+-2}^n with some |d_i| = 2,
    d^T Q d >= min_{s in {+-1}^O} s^T Q_OO s,     O = {i : |d_i| = 1}
(empty minimum = 0).  Compared here with the generic LP-based test of
Murota-Tamura Theorem 3.1 on the box {-2..2}^n (translation reduces all
pairs at l_inf distance 2 to pairs (0, d)).
"""
import itertools
import numpy as np
from dcheck import local_ext, box

rng = np.random.default_rng(5)


def criterion(Q):
    n = len(Q)
    for d in itertools.product((-2, -1, 0, 1, 2), repeat=n):
        if max(abs(t) for t in d) < 2:
            continue
        d = np.array(d)
        O = [i for i in range(n) if abs(d[i]) == 1]
        mn = 0.0
        if O:
            QO = Q[np.ix_(O, O)]
            mn = min(np.array(s) @ QO @ np.array(s) for s in itertools.product((-1, 1), repeat=len(O)))
        if d @ Q @ d < mn - 1e-9:
            return False
    return True


def lp_test(Q):
    """Murota-Tamura Thm 3.1 reduced by translation: f(z+x) = f(x) + linear + const
    for a quadratic form, and integral convexity is invariant under adding affine
    functions, so it suffices to test pairs (0, d) with ||d||_inf = 2."""
    n = len(Q)
    f = {p: float(np.array(p) @ Q @ np.array(p)) for p in box(-2, 2, n)}
    for d in itertools.product((-2, -1, 0, 1, 2), repeat=n):
        if max(abs(t) for t in d) < 2:
            continue
        m = tuple(t / 2 for t in d)
        if local_ext(f, m) > f[d] / 2 + 1e-9 * (1 + abs(f[d])):
            return False
    return True


agree = disagree = 0
counts = {True: 0, False: 0}
dd_count = 0
for n in (3, 4):
    for t in range(60 if n == 3 else 25):
        k = rng.integers(1, n + 2)
        A = rng.integers(-2, 3, size=(k, n))
        Q = A.T @ A + np.diag(rng.integers(0, 2, size=n))
        c1, c2 = criterion(Q), lp_test(Q)
        counts[c1] += 1
        dd_count += all(Q[i, i] >= sum(abs(Q[i, j]) for j in range(n) if j != i) for i in range(n))
        if c1 == c2:
            agree += 1
        else:
            disagree += 1
            print("DISAGREE", n, Q.tolist(), c1, c2)
print(f"agree={agree} disagree={disagree}; IC by criterion: {counts[True]}, not IC: {counts[False]}; DD: {dd_count}")
