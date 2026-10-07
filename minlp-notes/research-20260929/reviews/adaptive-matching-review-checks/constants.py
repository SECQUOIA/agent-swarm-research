"""Constants of Lemma 1 / Theorem 2 of adaptive-matching.md for the path family of Theorem 4.1 of [D]
(k = 2, w = 1, M_a = 2.8, c_g = 0.1, alpha' = 0.4, A = 2), evaluated from the note's formulas."""
import math
k, w, Ma, cg, alpha, A = 2, 1, 2.8, 0.1, 0.4, 2
kap = Ma / cg
a = alpha * A / cg
eta = (16 * k * (k + 1) * (w + 1) * kap) ** -0.5
th1 = min(1 / (32 * k * k), eta / (8 * k), 1 / (648 * k ** 4 * (w + 1) * kap), 1 / (k ** 1.5 * math.sqrt(108 * a)))
cth = 18432 * k ** 4 * (2 * k + 1) * (k + 1) * w * (w + 1)
th2 = eta / (2 * kap * math.sqrt(cth))
Q0 = (w + 1) * (k - 1) ** 2 * kap * (144 * k ** 3 * (w + 1) * kap + 12) + a / 2
Ks = max(32 * k * k / eta, math.sqrt(128 * k * (2 * k + 1) * Q0 / 3) / eta,
         (512 / 3) * k * k * (2 * k + 1) * kap * math.sqrt(w * (w + 1)) / eta ** 2)
ths = min(th1, th2)
R = 3 * Ks
base = 4 * R + 4 / ths + 4
print("kappa=%.1f a=%.1f eta=%.4g theta_1=%.3g theta_2=%.3g theta*=%.3g (2^%.1f) K*=%.3g R=3K*=%.3g base=%.3g"
      % (kap, a, eta, th1, th2, ths, math.log2(ths), Ks, R, base))
# K_1(0,0) for exact slopes (Corollary 4)
Q00 = Q0
K100 = max(32 * k * k / eta, math.sqrt(16 * k * (2 * k + 1) * Q00) / eta)
print("K_1(0,0) (exact-slope localization constant of Corollary 4) = %.3g; observed LS ratio 3-6" % K100)
