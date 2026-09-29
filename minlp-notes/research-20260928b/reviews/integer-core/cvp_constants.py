"""Reviewer checks for Section 3 (random CVP): algebra, constants and the covering lemma.

(a) Symbolic algebra of the proof of Theorem 3.4 (sympy): the averaging identity
    (1-th)|z|^2 + th|z-x|^2 = |z - th x|^2 + th(1-th)|x|^2, the choice 1-th = s1^2/(2R^2),
    A - bR^2 = 4(rho-1) r0^2/rho, and the monotonicity condition bR^2 <= (1-1/n)a^2 <=> rho >= 2/n.
(b) Parameter ranges where Theorems 3.4 / 3.5 are non-vacuous (V > 1 possible).
(c) Exponents: 0.5 log2(4/3), 0.5 log2(3/2); Kabatiansky-Levenshtein crossing rho*, e_+ (own
    implementation, scipy brentq); R_KL(60 deg); Remark 3.5a value.
(d) Covering lemma of Proposition 3.6(b): exact normalized cap measure
    sigma(phi) = (1/2) I_{sin^2 phi}((n-1)/2, 1/2) versus the claimed lower bound
    (1/(pi n)) sin^{n-2}(phi - 1/n) at phi = pi/4 - pi/(2n); growth of the cap count M.
"""
import math
import sympy as sp
from scipy.optimize import brentq
from scipy.special import betainc


def part_a():
    rho, r0, n = sp.symbols("rho r0 n", positive=True)
    R2 = rho * r0 ** 2
    s12 = 4 * (R2 - r0 ** 2)
    one_m_th = s12 / (2 * R2)
    th = 1 - one_m_th
    A = (1 - th) * R2 + th * s12
    b = th * (1 - th)
    a2 = 4 * (rho - 1) * r0 ** 2 / rho
    print("(a) theta =", sp.simplify(th), "; A - bR^2 - 4(rho-1)r0^2/rho =", sp.simplify(A - b * R2 - a2))
    diff = sp.factor(sp.simplify((1 - 1 / n) * a2 - b * R2))
    print("    (1-1/n)a^2 - bR^2 =", diff, " -> nonnegative iff rho >= 2/n")
    x1, x2, x3, z1, z2, z3, t = sp.symbols("x1 x2 x3 z1 z2 z3 t", real=True)
    X, Z = sp.Matrix([x1, x2, x3]), sp.Matrix([z1, z2, z3])
    nrm = lambda v: (v.T * v)[0]
    print("    averaging identity residual:", sp.expand((1 - t) * nrm(Z) + t * nrm(Z - X) - nrm(Z - t * X) - t * (1 - t) * nrm(X)))


def part_b():
    d34 = brentq(lambda d: (4 / 3) * ((1 - d) ** 2 - d) - 1, 0, 0.5)
    d35 = brentq(lambda d: 1.5 * (1 - d) ** 2 - d - 1, 0, 0.5)
    print(f"(b) Theorem 3.4 can give V > 1 only for delta < {d34:.4f} (statement allows delta < 0.1)")
    print(f"    Theorem 3.5 gives V_c > 1 only for delta < {d35:.4f}")


def RKL(theta):
    s = math.sin(theta)
    a, b = (1 + s) / (2 * s), (1 - s) / (2 * s)
    return a * math.log2(a) - (b * math.log2(b) if b > 0 else 0.0)


def part_c():
    print(f"(c) 0.5 log2(4/3) = {0.5*math.log2(4/3):.6f}; 0.5 log2(3/2) = {0.5*math.log2(1.5):.6f}; R_KL(60deg) = {RKL(math.pi/3):.5f}")
    f = lambda r: 0.5 * math.log2(r) - RKL(math.acos((2 - r) / r))
    rs = brentq(f, 1.2, 1.9)
    th = math.degrees(math.acos((2 - rs) / rs))
    print(f"    KL crossing rho* = {rs:.6f} (angle {th:.2f} deg), e_+ = {0.5*math.log2(rs):.6f}; separation 0.5log2(1.5) - e_+ = {0.5*math.log2(1.5)-0.5*math.log2(rs):.5f}")
    # Remark 3.5a: points of a cap ball of radius a (a^2 = rho - 1) with mutual distance >= 1, lifted to a
    # hemisphere of radius a in R^{n+1}: angular separation theta with 2 a sin(theta/2) = 1.
    best = max(((0.5 * math.log2(r) - RKL(2 * math.asin(1 / (2 * math.sqrt(r - 1)))), r)
                for r in [1.5 + i / 20000 for i in range(1, 10000)]), key=lambda t: t[0])
    print(f"    Remark 3.5a: max_rho 0.5 log2 rho - R_KL(theta(rho)) = {best[0]:.5f} at rho = {best[1]:.4f}")


def part_d():
    worst = float("inf")
    rows = []
    for n in range(4, 401):
        phi1 = math.pi / 4 - math.pi / (2 * n)
        exact = 0.5 * betainc((n - 1) / 2, 0.5, math.sin(phi1) ** 2)
        lower = math.sin(phi1 - 1 / n) ** (n - 2) / (math.pi * n)
        worst = min(worst, exact / lower)
        if n in (4, 10, 50, 100, 200, 400):
            M = math.ceil(math.pi * n * n * math.log(1 + 2 * n) / math.sin(math.pi / 4 - (math.pi / 2 + 1) / n) ** (n - 2))
            rows.append((n, exact, lower, M / (n * n * math.log(n) * 2 ** (n / 2))))
    print(f"(d) min over n=4..400 of sigma_exact/claimed_lower = {worst:.3f} (>= 1 required)")
    for n, e, l, ratio in rows:
        print(f"    n={n:3d}: sigma={e:.3e} lower={l:.3e}  M/(n^2 log n 2^(n/2)) = {ratio:.3f}")
    # chord 1/n -> angle <= pi/(2n)
    print("    chord 1/n => angle 2 asin(1/(2n)) <= pi/(2n):", all(2 * math.asin(1 / (2 * n)) <= math.pi / (2 * n) for n in range(1, 1000)))


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
    part_d()
