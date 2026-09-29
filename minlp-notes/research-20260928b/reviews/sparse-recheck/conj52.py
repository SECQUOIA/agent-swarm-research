"""Conjecture 5.2 and Section 5 scalings: n_IT/k versus its limit 2(1-gamma)/gamma, the largest delta
for which (1+delta)k <= n <= (1-delta) n_IT is nonempty, and alpha_IT at the scout's sizes."""
import numpy as np
snr2 = 4.0   # b/sigma = 2
print("n_IT/k = 2 log(p/k)/log(1 + k b^2/sigma^2), k = p^gamma, b/sigma = 2")
for g in [0.3, 0.5, 0.6, 0.65]:
    L = 2 * (1 - g) / g
    vals = []
    for p in [1e4, 1e8, 1e16, 1e64]:
        k = p ** g
        vals.append("p=%.0e: %.3f" % (p, 2 * np.log(p / k) / np.log1p(k * snr2)))
    print("  gamma=%.2f limit %.3f; delta_max=(2-3g)/(2-g)=%.3f | %s" % (g, L, (2 - 3 * g) / (2 - g), ", ".join(vals)))
print("alpha_IT = n_IT/(k log p) at the scout's sizes (p = 6k, b/sigma = 2)")
print("  " + ", ".join("k=%d: %.3f" % (k, 2 * k * np.log(6) / np.log1p(4 * k) / (k * np.log(6 * k))) for k in [5, 10, 15, 20]))
print("Section 5: n_IT/(k log p) vs 2(1-gamma)/(gamma log p), gamma = 0.5")
for p in [1e4, 1e8, 1e16]:
    k = p ** 0.5
    print("  p=%.0e: %.4f vs %.4f" % (p, 2 * np.log(p / k) / np.log1p(4 * k) / np.log(p), 2 * 0.5 / (0.5 * np.log(p))))
