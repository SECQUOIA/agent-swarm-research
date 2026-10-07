"""Exact checks of the core-mode height bound D_0 = T_0 (k! H_0^k)^2.

For random rational instances (core [0,1]^k, k<=2; residual endpoints with
rational boxes) we check, for EVERY residual endpoint label:
  * T_0 F is an integer-coefficient polynomial in the core, for
    T_0 = lcm(coef dens) * lcm(endpoint dens)^2   (sharper choice), and
    T_0 = S_0^3 with S_0 = product of distinct denominators (report choice);
  * the exact core optimum (face enumeration) has value denominator <= D_0;
and we exhibit an instance where S_0^2 (S_0 = lcm of all denominators) fails
to clear denominators, which is why a cube (or lcm_c * lcm_e^2) is used.
"""
import random
from fractions import Fraction as Fr
from itertools import product
from math import lcm, factorial

def rnd(rng):
    return Fr(rng.randint(-12, 12), rng.choice((1, 2, 3, 4, 6, 5)))

def instance(rng, k, r):
    n = k + r
    A = [[Fr(0)] * n for _ in range(n)]  # objective 1/2 x'Ax + b'x + c0 ; Hessian A
    for i in range(n):
        for j in range(i, n):
            w = rnd(rng)
            if i >= k and j >= k:
                w = -abs(w)  # residual: nonpositive diagonal and (orientation +1) nonpositive edges
            A[i][j] = A[j][i] = w
    b = [rnd(rng) for _ in range(n)]
    c0 = rnd(rng)
    lo = [Fr(0)] * k + [rnd(rng) for _ in range(r)]
    hi = [Fr(1)] * k + [lo[k + t] + abs(rnd(rng)) for t in range(r)]
    return A, b, c0, lo, hi

def coeff_list(A, b, c0):
    n = len(b)
    # monomial coefficients: x_i^2 -> A_ii/2, x_i x_j -> A_ij, x_i -> b_i
    cs = [c0] + b + [A[i][i] / 2 for i in range(n)] + [A[i][j] for i in range(n) for j in range(i + 1, n)]
    return cs

def label_quad(A, b, c0, k, xR):
    n = len(b); r = n - k
    P = [[A[i][j] for j in range(k)] for i in range(k)]
    p = [b[i] + sum(A[i][k + t] * xR[t] for t in range(r)) for i in range(k)]
    const = c0 + sum(b[k + t] * xR[t] for t in range(r)) + sum(A[k + s][k + t] * xR[s] * xR[t] for s in range(r) for t in range(r)) / 2
    return P, p, const

def qp_min_box(P, p, const, k):
    best = None
    for face in product((0, 1, None), repeat=k):
        free = [i for i in range(k) if face[i] is None]
        v = [Fr(face[i]) if face[i] is not None else None for i in range(k)]
        fixed = [i for i in range(k) if face[i] is not None]
        rhs = [-(p[i] + sum(P[i][j] * v[j] for j in fixed)) for i in free]
        if len(free) == 1:
            i = free[0]
            if P[i][i] == 0:
                continue
            v[i] = rhs[0] / P[i][i]
        elif len(free) == 2:
            a, bb, c, d = P[0][0], P[0][1], P[1][0], P[1][1]
            det = a * d - bb * c
            if det == 0:
                continue
            v[0] = (d * rhs[0] - bb * rhs[1]) / det
            v[1] = (-c * rhs[0] + a * rhs[1]) / det
        if any(not (0 <= v[i] <= 1) for i in range(k)):
            continue
        val = const + sum(p[i] * v[i] for i in range(k)) + sum(P[i][j] * v[i] * v[j] for i in range(k) for j in range(k)) / 2
        best = val if best is None else min(best, val)
    return best

def is_int_poly(P, p, const, T):
    # monomials: v_i^2 coefficient P_ii/2, v_i v_j coefficient P_ij, v_i coefficient p_i, constant
    k = len(p)
    cs = [const] + p + [P[i][i] / 2 for i in range(k)] + [P[i][j] for i in range(k) for j in range(i + 1, k)]
    return all((T * c).denominator == 1 for c in cs)

def run(rng, trials=200):
    worst = 0.0
    for _ in range(trials):
        k = rng.randint(1, 2); r = rng.randint(1, 3)
        A, b, c0, lo, hi = instance(rng, k, r)
        cs = coeff_list(A, b, c0)
        ends = lo + hi
        lam_c = lcm(*[c.denominator for c in cs]); lam_e = lcm(*[e.denominator for e in ends])
        T_sharp = lam_c * lam_e ** 2
        distinct = set(c.denominator for c in cs) | set(e.denominator for e in ends)
        S0 = 1
        for d_ in distinct:
            S0 *= d_
        T_rep = S0 ** 3
        for T in (T_sharp, T_rep):
            H0 = max([1] + [abs(T * A[i][j]) for i in range(k) for j in range(k)])
            assert all((T * A[i][j]).denominator == 1 for i in range(k) for j in range(k))
            D0 = T * (factorial(k) * H0 ** k) ** 2
            vals = []
            for lab in product((0, 1), repeat=r):
                xR = [lo[k + t] if lab[t] == 0 else hi[k + t] for t in range(r)]
                P, p, const = label_quad(A, b, c0, k, xR)
                assert is_int_poly(P, p, const, T)
                v = qp_min_box(P, p, const, k)
                assert v.denominator <= D0
                vals.append(v)
            fstar = min(vals)
            assert fstar.denominator <= D0
            worst = max(worst, fstar.denominator / D0)
    return worst

def cube_needed_example():
    # residual pair coefficient 1/2 on x_i x_j with both endpoints 1/2 -> 1/8;
    # S0 = lcm of all denominators = 2, S0^2 = 4 does not clear 1/8, S0^3 = 8 does.
    c = Fr(1, 2); xi = xj = Fr(1, 2)
    term = c * xi * xj
    S0 = 2
    return (S0 ** 2 * term).denominator != 1 and (S0 ** 3 * term).denominator == 1

if __name__ == "__main__":
    rng = random.Random(4242)
    w = run(rng)
    print("D_0 height bound held on 200 random instances (max den(f*)/D_0 = %.3g)" % w)
    assert cube_needed_example()
    print("example: S0^2 insufficient when S0 = lcm of denominators; S0^3 suffices")
    print("ALL EXACT-MODE CHECKS PASSED")
