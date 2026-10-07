"""coreA checks for Lemma lem:growthcert (setting-growthcert.tex) after W3.

Part (a) on mixed boxes, exact arithmetic: random quadratics, random x* with
gradient zeta = grad F(x*) satisfying zeta_i = 0 on J_0 (continuous, strictly
inside) and the inward sign on continuous active coordinates; integer
coordinates get arbitrary gradients.  mu_i = 0 on J_0, |zeta_i|/s_i for an
inward gradient at a bound, -|zeta_i| otherwise (integer coordinates only).
Checks F(x)-F(x*) >= 1/2 d^T (H+2M) d at all integer combinations and sampled
continuous values, and the growth conclusion when H+2M-2 g0 I is PSD (exact
elimination test).

Also checks the two-variable example of setting.tex:
F = (x1-x2)^2 + 2^-k x1^2 on [0,1]^2 has kappa >= 2^(k+2) and kappa-bar >= 2^(k+2).
Usage: python3 coreA-growthcert.py [seed] [count]
"""
import itertools
import random
import sys
from fractions import Fraction as Fr


def F(H, b, x):
    n = len(x)
    return sum(Fr(1, 2) * H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(
        b[i] * x[i] for i in range(n)
    )


def grad(H, b, x):
    n = len(x)
    return [sum(H[i][j] * x[j] for j in range(n)) + b[i] for i in range(n)]


def is_psd(A):
    """Exact PSD test by symmetric Gaussian elimination with pivoting on zero pivots."""
    A = [row[:] for row in A]
    n = len(A)
    idx = list(range(n))
    while idx:
        # choose a positive diagonal pivot
        piv = None
        for k in idx:
            if A[k][k] < 0:
                return False
            if A[k][k] > 0 and piv is None:
                piv = k
        if piv is None:
            # all remaining diagonals zero: PSD iff remaining block is zero
            return all(A[i][j] == 0 for i in idx for j in idx)
        idx.remove(piv)
        for i in idx:
            f = A[i][piv] / A[piv][piv]
            for j in idx:
                A[i][j] -= f * A[piv][j]
    return True


def part_a(rng):
    n = rng.randint(1, 4)
    kinds = [rng.choice("CZ") for _ in range(n)]
    lo = [Fr(rng.randint(-2, 0)) for _ in range(n)]
    hi = [lo[i] + rng.randint(1, 3) for i in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = Fr(rng.randint(-3, 6))
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = Fr(rng.randint(-3, 3), rng.randint(1, 2))
    xs = []
    for i in range(n):
        if kinds[i] == "Z":
            xs.append(Fr(rng.randint(int(lo[i]), int(hi[i]))))
        else:
            xs.append(rng.choice([lo[i], hi[i], lo[i] + (hi[i] - lo[i]) * Fr(rng.randint(1, 5), 6)]))
    # choose desired gradient zeta, then b = zeta - H x*
    zeta = []
    for i in range(n):
        if kinds[i] == "C" and lo[i] < xs[i] < hi[i]:
            zeta.append(Fr(0))
        elif kinds[i] == "C" and xs[i] == lo[i]:
            zeta.append(Fr(rng.randint(0, 6), 2))
        elif kinds[i] == "C":
            zeta.append(-Fr(rng.randint(0, 6), 2))
        else:
            zeta.append(Fr(rng.randint(-6, 6), 2))
    Hx = [sum(H[i][j] * xs[j] for j in range(n)) for i in range(n)]
    b = [zeta[i] - Hx[i] for i in range(n)]
    assert grad(H, b, xs) == zeta
    mu = []
    for i in range(n):
        s = hi[i] - lo[i]
        if kinds[i] == "C" and lo[i] < xs[i] < hi[i]:
            mu.append(Fr(0))
        elif (xs[i] == lo[i] and zeta[i] >= 0) or (xs[i] == hi[i] and zeta[i] <= 0):
            mu.append(abs(zeta[i]) / s)
        else:
            assert kinds[i] == "Z"
            mu.append(-abs(zeta[i]))
    HM = [[H[i][j] + (2 * mu[i] if i == j else 0) for j in range(n)] for i in range(n)]
    pts = []
    for i in range(n):
        if kinds[i] == "Z":
            pts.append([Fr(v) for v in range(int(lo[i]), int(hi[i]) + 1)])
        else:
            pts.append([lo[i] + (hi[i] - lo[i]) * Fr(k, 6) for k in range(7)])
    f0 = F(H, b, xs)
    for x in itertools.product(*pts):
        dlt = [x[i] - xs[i] for i in range(n)]
        lhs = F(H, b, x) - f0
        rhs = Fr(1, 2) * sum(dlt[i] * HM[i][j] * dlt[j] for i in range(n) for j in range(n))
        assert lhs >= rhs, ("minorant fails", lhs, rhs)
    # growth conclusion
    g0 = Fr(1, 8)
    shifted = [[HM[i][j] - (2 * g0 if i == j else 0) for j in range(n)] for i in range(n)]
    if is_psd(shifted):
        for x in itertools.product(*pts):
            dlt = [x[i] - xs[i] for i in range(n)]
            assert F(H, b, x) - f0 >= g0 * sum(t * t for t in dlt)
        return 1
    return 0


def two_variable_example():
    for k in range(1, 12):
        dk = Fr(1, 2**k)
        H = [[2 + 2 * dk, Fr(-2)], [Fr(-2), Fr(2)]]
        b = [Fr(0), Fr(0)]
        # unique minimizer 0: F >= 0 with equality only at 0 (checked on a grid)
        for x in itertools.product([Fr(i, 8) for i in range(9)], repeat=2):
            v = F(H, b, x)
            assert v >= 0 and (v > 0 or x == (0, 0))
        # g <= F(t,t)/(2t^2) = dk/2; L >= H_22 = 2
        t = Fr(1)
        gmax = F(H, b, (t, t)) / (2 * t * t)
        assert gmax == dk / 2
        kappa_lb = Fr(2) / gmax
        assert kappa_lb == 2 ** (k + 2)
        # weighted: L1 = 2+2dk, L2 = 2 are the smallest valid bounds
        L1, L2 = 2 + 2 * dk, Fr(2)
        gam_max = F(H, b, (t, t)) / (L1 * t * t + L2 * t * t)
        assert 1 / gam_max > 2 ** (k + 2)
    return True


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = random.Random(seed)
    grow = 0
    for _ in range(count):
        grow += part_a(rng)
    two_variable_example()
    print(f"seed {seed}: {count} minorant checks passed ({grow} with growth certificate g0=1/8); "
          f"two-variable example passed")


if __name__ == "__main__":
    main()
