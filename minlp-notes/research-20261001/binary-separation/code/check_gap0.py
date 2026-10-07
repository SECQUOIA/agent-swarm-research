"""Exact checks for the gap-0 construction (note.md, Section 6). Standard library only.

Cut-space point x on V = [n]; Z = J - 2X has unit diagonal (X_ij = x_ij, X_ii = 0).
A gap inequality reads b^T Z b >= gamma(b)^2; gap-0 inequalities are those with gamma(b) = 0.
Lemma 4: x violates a gap-0 inequality iff Z restricted to s^perp is not PSD for some s in {+-1}^n.

Construction (Theorem 4): balanced partition instance c in Z_{>=0}^n (n even, n >= 4), C = sum c > 0,
a = c + K 1 with K = 4 n C, A2 = |a|^2,
  theta_lb = (2(n-1) a_min^2 - (n+1) a_max^2) / ((n-1)(n-2)) > 0,
  nu = theta_lb / (A2 a_max^2),
  rho_i = a_i^2 (1 + nu a_i^2 / A2),  Delta = sum rho,
  theta_ij = (rho_i + rho_j)/(n-2) - Delta/((n-1)(n-2))   (i != j),
  Z = D_a^{-1} L_theta D_a^{-1} - nu a a^T / A2.
Claims checked: Z_ii = 1, Z a = -nu a, theta_ij >= theta_lb > 0, and for EVERY s in {+-1}^n:
Z|s^perp is not PSD  <=>  s^T a = 0  <=>  s is a balanced partition of c.
Also: x = (J - Z)/2 lies in [0,1]^E and satisfies all triangle inequalities when n >= 6.
"""
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product

random.seed(424242)


def is_psd(S):
    """Exact PSD test by symmetric elimination with diagonal pivots (as in Lemma 4 of the split note)."""
    S = [[F(x) for x in row] for row in S]
    while S:
        N = len(S)
        if any(S[i][i] < 0 for i in range(N)):
            return False
        for i in range(N):
            if S[i][i] == 0 and any(S[i][j] != 0 for j in range(N)):
                return False
        piv = next((i for i in range(N) if S[i][i] > 0), None)
        if piv is None:
            return True  # S = 0
        p = S[piv][piv]
        rest = [i for i in range(N) if i != piv]
        S = [[S[i][j] - S[i][piv] * S[piv][j] / p for j in rest] for i in rest]
    return True


def construct(c):
    n = len(c)
    C = sum(c)
    K = 4 * n * C
    a = [ci + K for ci in c]
    A2 = sum(ai * ai for ai in a)
    amin, amax = min(a), max(a)
    theta_lb = F(2 * (n - 1) * amin ** 2 - (n + 1) * amax ** 2, (n - 1) * (n - 2))
    assert theta_lb > 0
    nu = theta_lb / (A2 * amax ** 2)
    rho = [ai * ai * (1 + nu * ai * ai / A2) for ai in a]
    Delta = sum(rho)
    theta = [[(rho[i] + rho[j]) / (n - 2) - Delta / ((n - 1) * (n - 2)) if i != j else F(0)
              for j in range(n)] for i in range(n)]
    Z = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            lap = sum(theta[i][k] for k in range(n) if k != i) if i == j else -theta[i][j]
            Z[i][j] = lap / (a[i] * a[j]) - nu * a[i] * a[j] / A2
    return a, nu, theta, theta_lb, Z


def restrict(Z, s):
    """Gram matrix of Z on the basis f_i = e_i - s_i s_n e_n (i < n) of s^perp."""
    n = len(Z)
    f = [[F(int(k == i)) - (s[i] * s[n - 1] if k == n - 1 else 0) for k in range(n)] for i in range(n - 1)]
    return [[sum(f[i][k] * Z[k][l] * f[j][l] for k in range(n) for l in range(n)) for j in range(n - 1)]
            for i in range(n - 1)]


def check(trials_per_n=((6, 30), (8, 10))):
    bad = total = yes = 0
    for n, T in trials_per_n:
        for _ in range(T):
            c = [random.randint(0, 6) for _ in range(n)]
            if random.random() < 0.5:  # plant a balanced partition
                half = [random.randint(0, 6) for _ in range(n // 2 - 1)]
                other = [random.randint(0, 6) for _ in range(n // 2 - 1)]
                diff = sum(half) - sum(other)
                if diff >= 0:
                    other.append(diff + 1); half.append(1)
                else:
                    half.append(-diff + 1); other.append(1)
                c = half + other
                random.shuffle(c)
            a, nu, theta, theta_lb, Z = construct(c)
            ok = all(Z[i][i] == 1 for i in range(n))
            ok &= all(sum(Z[i][j] * a[j] for j in range(n)) == -nu * a[i] for i in range(n))
            ok &= all(theta[i][j] >= theta_lb for i in range(n) for j in range(n) if i != j)
            bal = False
            for s in product((1, -1), repeat=n - 1):
                s = (1,) + s
                sa = sum(si * ai for si, ai in zip(s, a))
                sc = sum(si * ci for si, ci in zip(s, c))
                balanced = sc == 0 and sum(s) == 0
                notpsd = not is_psd(restrict(Z, s))
                ok &= (sa == 0) == balanced == notpsd
                bal |= balanced
            x = [[(1 - Z[i][j]) / 2 for j in range(n)] for i in range(n)]
            ok &= all(0 <= x[i][j] <= 1 for i in range(n) for j in range(n) if i != j)
            for i, j, k in combinations(range(n), 3):
                u, v, w = x[i][j], x[i][k], x[j][k]
                ok &= u <= v + w and v <= u + w and w <= u + v and u + v + w <= 2
            ok &= not is_psd(Z)
            total += 1
            yes += bal
            bad += not ok
    print(f"[gap-0] {total} balanced-partition instances (n in {{6,8}}, {yes} yes-instances): Z_ii = 1, "
          f"Z a = -nu a, theta >= theta_lb > 0, Z not PSD, and for every s: Z|s^perp not PSD <=> s^T a = 0 "
          f"<=> balanced partition; x in [0,1] with all triangle inequalities: {bad} failures")
    return bad == 0


def check_lemma_small(trials=200):
    """Lemma 4 sanity check on random small Z (n = 3, 4): compare the s-criterion with a direct
    search for integer b, gamma(b) = 0, b^T Z b < 0, in the box [-6, 6]^n (one direction only:
    every b found must be certified by some s; every s-certificate must be matched by some b)."""
    bad = 0
    for _ in range(trials):
        n = random.choice([3, 4])
        Z = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                Z[i][j] = Z[j][i] = F(random.randint(-9, 9), 8)
        crit = any(not is_psd(restrict(Z, (1,) + s)) for s in product((1, -1), repeat=n - 1))
        found = False
        for b in product(range(-6, 7), repeat=n):
            if any(b) and sum(b[i] * Z[i][j] * b[j] for i in range(n) for j in range(n)) < 0:
                if any(sum(si * bi for si, bi in zip(s, b)) == 0 for s in product((1, -1), repeat=n)):
                    found = True
                    break
        bad += found and not crit  # a box witness always implies the criterion
    print(f"[gap-0 lemma] {trials} random unit-diagonal Z (n = 3, 4): box witnesses without an "
          f"s-certificate: {bad}")
    return bad == 0


if __name__ == "__main__":
    r = [check(), check_lemma_small()]
    print("ALL CHECKS PASSED" if all(r) else "SOME CHECK FAILED")
    sys.exit(0 if all(r) else 1)
