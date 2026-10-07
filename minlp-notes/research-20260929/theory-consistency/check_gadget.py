"""Cross-check with the robust-lower-bound note, Proposition 3.3: the gadget gap
for class b_d is the band gap with L = -h1 and U = h2 + c y^2 (y1 = 0.38,
eta = 0.05, eps_v = 0.02).  The note reports gamma_2 = gamma_3 = 0.07612,
gamma_4 = 0.00777, gamma_6 = 0.00237, gamma_8 = 0.00078."""
import numpy as np
from consistency_lib import poly_gap

y1, eta, ev = 0.38, 0.05, 0.02
c = 1 + eta + ev
h1 = lambda y: np.where(np.abs(y) <= y1, -y ** 2, y1 ** 2 - 2 * y1 * np.abs(y))
h2 = lambda y: -eta * y ** 2 - (1 - eta) * np.maximum(np.abs(y) - y1, 0) ** 2
U = lambda y: h2(y) + c * y ** 2
L = lambda y: -h1(y)
with open("logs/check_gadget.log", "w") as fh:
    for d in [2, 3, 4, 6, 8]:
        g, gu = poly_gap(U, L, d, extra=(y1, -y1, 0.0))
        msg = f"d={d}: band gap = {g:.5f} (fine-grid re-evaluation {gu:.5f})"
        print(msg); fh.write(msg + "\n")
