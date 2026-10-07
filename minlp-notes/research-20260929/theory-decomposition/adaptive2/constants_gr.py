"""Constants of Lemma 1, Theorem 2 and Corollary 4 of adaptive-matching.md (revision after review).

  python3 constants_gr.py

Evaluates the formulas of Sections 2 and 3.2 on the path family of Theorem 4.1 of the decomposition
note (k = 2, w = 1, M_a = 2.8, c_g = 0.1, alpha' = 0.4, A = 2), checks the fixed-point inequality
K_1(gamma(K*), theta*) <= K* used in the induction of Theorem 2(a), computes K_LS of Corollary 4,
and prints the exponents of k and kappa in K* and 1/theta* by finite differences of logarithms.
Double precision; the formulas are those of the note, not new bounds.
"""
import math


def consts(k, w, Ma, cg, alpha, A):
    kap, a = Ma / cg, alpha * A / cg
    eta = (16 * k * (k + 1) * (w + 1) * kap) ** -0.5
    th1_terms = [1 / (32 * k * k), eta / (8 * k), 1 / (648 * k ** 4 * (w + 1) * kap)]
    if a > 0:
        th1_terms.append(1 / (k ** 1.5 * math.sqrt(108 * a)))
    th1 = min(th1_terms)
    cth = 18432 * k ** 4 * (2 * k + 1) * (k + 1) * w * (w + 1)
    th2 = eta / (2 * kap * math.sqrt(cth))
    Q0 = (w + 1) * (k - 1) ** 2 * kap * (144 * k ** 3 * (w + 1) * kap + 12) + a / 2

    def Q(g, th):
        return Q0 + 2 * g * kap * math.sqrt(w) + 288 * k * (k + 1) * w * g * g * th * th * kap * kap

    def K1(g, th):
        return max(32 * k * k / eta, math.sqrt(16 * k * (2 * k + 1) * Q(g, th)) / eta)

    Ks = max(32 * k * k / eta, math.sqrt(128 * k * (2 * k + 1) * Q0 / 3) / eta,
             (512 / 3) * k * k * (2 * k + 1) * kap * math.sqrt(w * (w + 1)) / eta ** 2)
    ths = min(th1, th2)
    gam = 2 * k * math.sqrt(w + 1) * Ks
    # K_LS of Corollary 4: least K >= 1 with K >= K_1(2 (k-1) sqrt(w+1) K, 0)  (bisection; K_1^2 is affine in K)
    lo, hi = 1.0, 1e30
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if mid >= K1(2 * (k - 1) * math.sqrt(w + 1) * mid, 0.0):
            hi = mid
        else:
            lo = mid
    return dict(kappa=kap, a=a, eta=eta, theta1=th1, theta2=th2, thetastar=ths, Kstar=Ks,
                base=4 * 3 * Ks + 4 / ths + 4, K100=K1(0, 0), KLS=hi,
                fixed_point_ratio=K1(gam, ths) / Ks)


def main():
    c = consts(2, 1, 2.8, 0.1, 0.4, 2)
    print("path family of Theorem 4.1 of [D]: k=2, w=1, M_a=2.8, c_g=0.1, alpha'=0.4, A=2")
    print("  kappa = %.1f, a = %.1f, eta = %.4g" % (c["kappa"], c["a"], c["eta"]))
    print("  theta_1 = %.3g, theta_2 = %.3g, theta* = %.3g (= 2^%.2f)" % (
        c["theta1"], c["theta2"], c["thetastar"], math.log2(c["thetastar"])))
    print("  K* = %.3g, R = 3K* = %.3g, base 4R + 4/theta* + 4 = %.3g" % (c["Kstar"], 3 * c["Kstar"], c["base"]))
    print("  check of Theorem 2(a): K_1(gamma(K*), theta*)/K* = %.4f (must be <= 1)" % c["fixed_point_ratio"])
    print("  K_1(0, 0) = %.3g (Corollary 4, exact slopes); K_LS (LS slopes) = %.3g" % (c["K100"], c["KLS"]))
    print("orders (finite differences of logs; a = 0, so the sqrt(a) terms are absent):")
    for lab, f in (("k     (w=1, kappa=100)", lambda s: consts(s, 1, 100.0, 1.0, 0.0, 0.0)),
                   ("kappa (k=4, w=1)", lambda s: consts(4, 1, s, 1.0, 0.0, 0.0)),
                   ("w     (k=4, kappa=100)", lambda s: consts(4, s, 100.0, 1.0, 0.0, 0.0))):
        s1, s2 = 64.0, 128.0
        if lab.startswith("kappa"):
            s1, s2 = 1e4, 2e4
        c1, c2 = f(s1), f(s2)
        print("  exponent in %s: K* %.3f, 1/theta* %.3f" % (
            lab, math.log(c2["Kstar"] / c1["Kstar"]) / math.log(s2 / s1),
            math.log(c1["thetastar"] / c2["thetastar"]) / math.log(s2 / s1)))
    # small kappa (kappa near its minimum 2/k): the theta_1 term 1/(648 k^4 (w+1) kappa) can be binding
    for kk in (8, 32):
        c3 = consts(kk, 1, 2.0 / kk * 1.0001, 1.0, 0.0, 0.0)
        print("  k=%d, w=1, kappa=2/k: binding term of theta*: %s (theta_1=%.3g, theta_2=%.3g)" % (
            kk, "theta_1" if c3["theta1"] < c3["theta2"] else "theta_2", c3["theta1"], c3["theta2"]))


if __name__ == "__main__":
    main()
