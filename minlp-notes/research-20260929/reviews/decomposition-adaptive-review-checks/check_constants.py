"""Reviewer recomputation of the constants quoted in Section A.3 of extension-adaptive.md
(path family: k = 2, w = 1, M_a = 2.8, c_g = 0.1, alpha' = 0.4, A = 2, s0 = 2) and of i* / size bound."""
import math
k, w, Ma, cg, al, A, s0 = 2, 1, 2.8, 0.1, 0.4, 2, 2.0
Lam = 2 * (k - 1) ** 2 * (k * Ma ** 2 * w / cg + Ma * w) + al * A / 4
gamma = 8 * k ** 1.5 * Ma * math.sqrt(w) / cg
astar = (gamma + math.sqrt(gamma ** 2 + 8 * Lam / cg)) / 2
print("Lambda = %.2f, gamma = %.1f, a* = %.1f" % (Lam, gamma, astar))
print("exact slopes (nu = 0): rho = 2 + %.1f sqrt|T|" % math.sqrt(6 * Lam / cg))
for n in (8, 32, 64):
    T = n - 1
    abar = max(astar, math.sqrt(n / T) / 2)
    PsiA = Lam + 4 * k ** 1.5 * Ma * math.sqrt(w) * abar
    rho = 2 * (k - 1) + math.sqrt(6 * PsiA * T / cg)
    for eps in (1e-4, 1e-6):
        istar = max(0, math.ceil(math.log2(s0 * math.sqrt(3 * PsiA * T / eps))))
        size = 2 * T * (1 + istar * (4 * rho + 4) ** (w + 1))
        print("n=%d eps=%.0e: Psi_A = %.4g, rho = %.4g (= 2 + %.1f sqrt|T|), i* = %d, size bound = %.3g" % (
            n, eps, PsiA, rho, (rho - 2) / math.sqrt(T), istar, size))
# order-of-constants inequality check: Psi_A <= 2 Lambda + 40 k^3 Ma^2 w/cg + 2 k^1.5 Ma (w+1)
for (k, w, Ma, cg, al, A) in ((2, 1, 2.8, 0.1, 0.4, 2), (3, 4, 1.0, 0.5, 1.0, 5), (5, 2, 10.0, 0.01, 2.0, 3)):
    Lam = 2 * (k - 1) ** 2 * (k * Ma ** 2 * w / cg + Ma * w) + al * A / 4
    gamma = 8 * k ** 1.5 * Ma * math.sqrt(w) / cg
    astar = (gamma + math.sqrt(gamma ** 2 + 8 * Lam / cg)) / 2
    abar = max(astar, math.sqrt(w + 1) / 2)
    PsiA = Lam + 4 * k ** 1.5 * Ma * math.sqrt(w) * abar
    rhs = 2 * Lam + 40 * k ** 3 * Ma ** 2 * w / cg + 2 * k ** 1.5 * Ma * (w + 1)
    print("k=%d w=%d: Psi_A = %.4g <= %.4g : %s" % (k, w, PsiA, rhs, PsiA <= rhs))
