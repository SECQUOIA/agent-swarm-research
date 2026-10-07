"""Referee check R6: E4 has an explicit quadratic band element, so gap(P_n) = 0 for n >= 2 exactly."""
import numpy as np
s = np.linspace(-1, 1, 2000001)
U = 0.7 * s - s ** 2 - 0.5 * np.abs(s + 0.5)
T = -0.28 - 0.4 * (s - 0.3)
L = T - 1.5 * (s - 0.3) ** 2
print("U(0.3) =", 0.7 * 0.3 - 0.09 - 0.5 * 0.8, " (tangent value -0.28), min(U - L) =", (U - L).min())
for kappa in [1.3, 1.4, 1.5]:
    q = T - kappa * (s - 0.3) ** 2
    print(f"kappa={kappa}: min(U - q) = {np.min(U - q):.4f}, min(q - L) = {np.min(q - L):.4f}")
