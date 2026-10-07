"""Order-k relaxations: count level-j dyadic cells meeting E(s_j^k).

For relaxations with gap of order k (hypotheses (G^k), (U^k) of the note,
with tau = alpha = 1), a level-j cube can survive only if it meets
E(s_j^k), and a certificate needs about N_inf(E(eta), eta^(1/k)) cells.  This
script counts N_j = #{closed level-j cells of [-0.9, 1.3]^2 meeting
E(s_j^k)} exactly (the minimum of each m over a cell is available in closed
form), and fits the slope of log N_j against log(1/s_j), which estimates
k * e_k where e_k is the covering exponent in eta.

Three functions with the same RLCT lambda = 1/2 in n = 2:
  y^2       (Morse-Bott line, p = 1):   e_k = 1/k
  x^4 + y^4 (isolated quartic):          e_k = 2 (1/k - 1/4)_+
  x^2 y^2   (crossing lines, theta = 2): e_k = 1/k (log factor at k = 2)
At k = 2 all three have e_2 = n/2 - lambda = 1/2.
"""
import math

import numpy as np

LO, SIDE = -0.9, 2.2


def dist0(a, b):
    """distance from 0 to the interval [a, b], elementwise"""
    return np.where(a > 0, a, np.where(b < 0, -b, 0.0))


def count(name, k, j):
    s = SIDE * 2.0 ** (-j)
    a = LO + s * np.arange(2 ** j)
    d = dist0(a, a + s)                    # per-coordinate distance to 0
    eta = s ** k
    X, Y = np.meshgrid(d, d, indexing="ij")
    if name == "y2":
        mn = Y ** 2
    elif name == "x4y4":
        mn = X ** 4 + Y ** 4
    else:
        mn = (X * Y) ** 2
    return int(np.count_nonzero(mn <= eta))


def main():
    J = list(range(6, 15))
    for k in (2, 3, 4, 6):
        print(f"\nk = {k}: N_j and local slopes d log N_j / d log(1/s_j) (predicted k*e_k)")
        for name, pred in (("y2", 1.0), ("x4y4", 2 * k * max(0.0, 1 / k - 0.25)), ("x2y2", 1.0)):
            Ns = [count(name, k, j) for j in J]
            sl = [math.log(Ns[i + 1] / Ns[i]) / math.log(2) for i in range(len(J) - 1)]
            print(f"  {name:5s} N_j = {Ns}")
            print(f"        slopes = {[round(x, 3) for x in sl]}  predicted k*e_k = {pred:.3f}")


if __name__ == "__main__":
    main()
