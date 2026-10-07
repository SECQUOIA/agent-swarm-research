"""Targeted checks for the revision after review (Section 8 of decomposition-certificates.md).

1. (leaf, cell) pair counts for an interior bag (theta = 1/16).
2. The n = 9 certificate at eps = 1e-4 (theta = 1/16, h = 2^-8).
3. Face-exact Theorem 1 bound for the note's relaxation, and crossovers with
   the computed certificate sizes and with Theorem 4.1(b).
4. Uniform ratio: min over n in [3, 300] and eps in [1e-40, 1e-4] of
   max(Cor 2.1 closed form, face-exact bound) / Theorem 4.1(b), divided by 1.3155^n/sqrt(n).
5. Corollary 2.1 bases for other factorizations of the same objective.
"""
import math
import numpy as np
from dp_certificate import shells, certificate

B, KAPPA = 0.8, 0.1


def pairs(h, mu):
    L, U = shells(np.zeros(2), h, mu, 2)
    Pl, Pu = shells(np.zeros(1), h, mu, 1)
    meet = (Pl[None, :, 0] <= U[:, None, 0]) & (Pu[None, :, 0] >= L[:, None, 0])
    return len(L), len(Pl), int(meet.sum()), int(meet.sum(axis=1).max())


def face_exact(n, eps):
    return (5 / 3) ** n * math.exp(-(5 / 9) * (1 + 1.25 * eps))


def cor21_closed(n, eps):
    v = 0.068 * math.sqrt(n) * (2 * math.e / math.pi) ** (n / 2) * math.log(0.2 / (n * eps))
    return max(v, 0.0)


def thm41b(n, eps):
    return 3.36e7 * (n - 1) * (0.5 * math.log2(1.96e6 * (n - 1) / eps) + 2)


def main():
    print("# 1. pair counts, interior bag, theta = 1/16")
    print("# h  leaves  cells  pairs  pairs/leaves  max cells per leaf")
    for j in [4, 8, 12, 14]:
        l, c, p, m = pairs(2.0 ** -j, 4)
        print("2^-%d %6d %4d %7d %.2f %d" % (j, l, c, p, p / l, m))
    print("# 2. n = 9, eps = 1e-4, theta = 1/16, h = 2^-8")
    r, size, _, _ = certificate(9, B, KAPPA, np.zeros(9), np.zeros(9), 2.0 ** -8, 4)
    print("gap %.3e size %d" % (-r, size))
    print("# 3. face-exact bound (5/3)^n exp(-(5/9)(1+1.25 eps)); crossovers")
    print("exp(-5/9) = %.4f; bound at n=20,40, eps=1e-6: %.3e %.3e" % (
        math.exp(-5 / 9), face_exact(20, 1e-6), face_exact(40, 1e-6)))
    for eps, per_bag in [(1e-4, 27937), (1e-6, 37248), (1e-8, 46551)]:
        n1 = next(n for n in range(3, 400) if face_exact(n, eps) > per_bag * (n - 1))
        n2 = next(n for n in range(3, 400) if face_exact(n, eps) > thm41b(n, eps))
        n3 = next(n for n in range(3, 400) if cor21_closed(n, eps) > thm41b(n, eps))
        print("eps=%.0e: face-exact > computed certificate from n=%d; face-exact > Thm 4.1(b) from n=%d; Cor 2.1 closed form > Thm 4.1(b) from n=%d" % (eps, n1, n2, n3))
    print("# 4. uniform ratio constant")
    worst = (float("inf"), None, None)
    for n in range(3, 301):
        for le in np.linspace(4, 40, 721):
            eps = 10.0 ** (-le)
            lb = max(cor21_closed(n, eps), 0.57 * (5 / 3) ** n)
            ratio = lb / thm41b(n, eps) / ((2 * math.e / math.pi) ** (n / 2) / math.sqrt(n))
            if ratio < worst[0]:
                worst = (ratio, n, eps)
    print("min over grid of ratio/(1.3155^n/sqrt n) = %.3e at n=%d eps=%.1e" % worst)
    print("# 5. Corollary 2.1 base sqrt(4e/pi * weight/lambda_geo), lambda_geo = 1.6")
    def amin(Hs):
        return max(0.0, -min(np.linalg.eigvalsh(H).min() for H in Hs) / 2)
    gpp = lambda t: 2 - 12 * KAPPA * t * t
    ts = np.linspace(-1, 1, 201)
    near = np.linspace(-0.05, 0.05, 11)
    cases = {
        "bilinear alone": amin([np.array([[0, B], [B, 0]])]),
        "g_i + b x_i x_{i+1}, root box": amin([np.array([[gpp(t), B], [B, 0]]) for t in ts]),
        "g_i + b x_i x_{i+1}, near 0": amin([np.array([[gpp(t), B], [B, 0]]) for t in near]),
        "balanced, root box": amin([np.array([[gpp(s) / 2, B], [B, gpp(t) / 2]]) for s in ts for t in ts]),
        "balanced, near 0": amin([np.array([[gpp(s) / 2, B], [B, gpp(t) / 2]]) for s in near for t in near]),
    }
    for k, a in cases.items():
        w = 2 * a
        base = math.sqrt(4 * math.e / math.pi * w / 1.6) if w > 0 else 0.0
        print("%-32s alpha=%.4f weight=%.4f base=%.4f" % (k, a, w, base))
    # balanced factor convex on the cube |x|_inf <= t iff (1 - 0.6 t^2)^2 >= b^2
    print("balanced factor convex on |x|_inf <= %.4f" % math.sqrt((1 - B) / (6 * KAPPA)))


if __name__ == "__main__":
    main()
