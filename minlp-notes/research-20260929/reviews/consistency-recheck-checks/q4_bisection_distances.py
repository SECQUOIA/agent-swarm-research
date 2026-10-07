"""Recheck Q4: relative distance of the kink c0 = 1/sqrt(7) to the sibling
cells discarded by dyadic bisection of [-1, 1] toward c0 (Section 5.5 of the
note claims a 'fixed relative distance'). rho is the Bernstein-ellipse
parameter of the sibling cell through the kink."""
import numpy as np
c0 = 1 / np.sqrt(7)
a, b = -1.0, 1.0
for j in range(1, 16):
    m = (a + b) / 2
    if c0 < m:
        sib = (m, b); b = m
    else:
        sib = (a, m); a = m
    h = (sib[1] - sib[0]) / 2
    t = min(abs(c0 - sib[0]), abs(c0 - sib[1])) / h
    rho = 1 + t + np.sqrt((1 + t) ** 2 - 1)
    print(f"level {j:2d}: sibling [{sib[0]:.6f}, {sib[1]:.6f}]  distance/half-width = {t:.4f}  rho = {rho:.3f}")
