"""Independent constraint checks for the SDP-RLT spatial-box construction.

Uses exact rational arithmetic for every affine/RLT constraint and numerical
PSD checks only for the moment matrix. The proof in the note supplies its
exact eigenvalues. No SDP optimization is needed for these certificates.
"""
from fractions import Fraction as Q
from itertools import combinations
import random

import numpy as np


def make_point(k, m, z, restricted):
    n = k + m + z
    w = [Q(1)] * k + [Q(1, 2*m)] * m + [Q(0)] * z
    R = set(restricted)
    U = sorted(set(range(n)) - R)
    assert len(R) < min(k, z)
    s = len(U)
    t = Q(2*k + 1, 2) - sum(w[i] for i in R)
    assert 1 <= t <= s - 1
    c = t/s
    d = t*(t-1)/(s*(s-1))
    x = [w[i] if i in R else c for i in range(n)]
    X = [[x[i]*x[j] if i in R or j in R else c if i == j else d
          for j in range(n)] for i in range(n)]
    return w, x, X


def verify(k, m, z, restricted, rng):
    n = k + m + z
    R = set(restricted)
    w, x, X = make_point(k, m, z, R)
    K = Q(2*k + 1, 2)
    # Every generated restricted interval includes its witness coordinate,
    # and excludes an endpoint; degenerate intervals are included sometimes.
    bounds = []
    for i in range(n):
        if i not in R:
            bounds.append((Q(0), Q(1)))
        else:
            a = w[i]*Q(rng.randint(1, 10), 10)
            b = w[i]+(1-w[i])*Q(rng.randint(0, 9), 10)
            bounds.append((a, b))
    assert sum(x) == K
    assert all(a <= xi <= b for xi, (a,b) in zip(x,bounds))
    for i in range(n):
        assert sum(X[i]) == K*x[i]
        ai, bi = bounds[i]
        for j in range(n):
            aj, bj = bounds[j]
            assert X[i][j] - ai*x[j] - aj*x[i] + ai*aj >= 0
            assert bj*x[i] - X[i][j] - ai*bj + ai*x[j] >= 0
            assert bi*x[j] - X[i][j] - bi*aj + aj*x[i] >= 0
            assert bi*bj - bi*x[j] - bj*x[i] + X[i][j] >= 0
    obj = sum(x[i]-X[i][i] for i in range(n))
    p = Q(1, 2*m)
    assert obj == len(R & set(range(k,k+m)))*p*(1-p)
    moment = np.array([[Q(1)] + x] + [[x[i]]+X[i] for i in range(n)], dtype=float)
    assert np.linalg.eigvalsh(moment).min() >= -1e-10
    return 1


def main():
    rng = random.Random(68417)
    count = 0
    for n in range(3, 10):
        for k in range(1,n-1):
            for m in range(1,n-k):
                z = n-k-m
                for size in range(min(k,z)):
                    for R in combinations(range(n),size):
                        count += verify(k,m,z,R,rng)
    # Larger, randomly restricted balanced and asymmetric instances.
    for k,m,z in [(12,12,12),(20,30,25),(2,70,3),(50,1,50)]:
        for _ in range(10):
            r = rng.randrange(min(k,z))
            R = rng.sample(range(k+m+z),r)
            count += verify(k,m,z,R,rng)
    print(f"Passed {count} SDP-RLT point checks, including degenerate intervals: "
          "exact rational affine, RLT, equality and objective identities; "
          "floating-point PSD eigenvalue check (tolerance 1e-10).")


if __name__ == '__main__':
    main()
