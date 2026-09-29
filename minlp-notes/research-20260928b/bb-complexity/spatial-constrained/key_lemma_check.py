"""Numerical checks of the key lemma (Lemma 4.1 of the note).

(a) Unit circle S in R^2 (d = 1, n = 2).  Lemma 4.1 gives, for every box B,
      I(B) = int_{S ∩ B} q_B^{-1/2} ds <= pi * sqrt(2) * sum_I M^I(S) = pi sqrt(2) * 4.
    We search for large I(B) over random boxes (log-uniform widths, random
    aspect ratios, centres near the circle), then refine the best boxes by
    Nelder-Mead.  Reports the largest value found.
    The refinement also starts from the bounding square [-1,1]^2 (value 2 pi).
(b) Comb: k horizontal unit segments at heights (j - 1/2)/k inside B = [0,1]^2.
    Exact: I(B) = sum_j 2 arcsin(1/sqrt(1 + 4 h_j (1 - h_j))).  The lemma bound
    is pi sqrt(2) k (multiplicity k).  I(B)/k tends to a positive constant,
    so the multiplicity factor in the lemma cannot be dropped.
(c) Connected spiral rho(t) = 1 + 1/(1+t), t > 0 (curvature <= 10, embedded,
    infinite length) inside B = [-2,2]^2: int over t in (0, T] of q_B^{-1/2} ds
    grows linearly in T, so the integral over the whole spiral is infinite.
Usage: python3 key_lemma_check.py
"""
import math
import numpy as np
from scipy import integrate
from scipy.optimize import minimize

rng = np.random.default_rng(1)


def circle_integral(l1, u1, l2, u2):
    if not (l1 < u1 and l2 < u2):
        return 0.0
    cand = [0.0, 2 * math.pi]
    for v in (l1, u1):
        if -1 < v < 1:
            a = math.acos(v)
            cand += [a, 2 * math.pi - a]
    for v in (l2, u2):
        if -1 < v < 1:
            a = math.asin(v)
            cand += [a % (2 * math.pi), (math.pi - a) % (2 * math.pi)]
    cand = sorted(set(cand))

    def q(t):
        x, y = math.cos(t), math.sin(t)
        return (x - l1) * (u1 - x) + (y - l2) * (u2 - y)

    total = 0.0
    for a, b in zip(cand[:-1], cand[1:]):
        if b - a < 1e-15:
            continue
        m = 0.5 * (a + b)
        x, y = math.cos(m), math.sin(m)
        if l1 <= x <= u1 and l2 <= y <= u2:
            val, _ = integrate.quad(lambda t: max(q(t), 1e-300) ** -0.5, a, b, limit=200)
            total += val
    return total


def params_to_box(p):
    cx, cy, lw, la = p
    w = math.exp(lw)
    r = math.exp(la)
    w1, w2 = w * math.sqrt(r), w / math.sqrt(r)
    return cx - w1 / 2, cx + w1 / 2, cy - w2 / 2, cy + w2 / 2


def main():
    bound = math.pi * math.sqrt(2) * 4
    trials = []
    for _ in range(4000):
        th = rng.uniform(0, 2 * math.pi)
        rad = 1 + rng.normal(0, 0.3)
        p = [rad * math.cos(th), rad * math.sin(th), rng.uniform(math.log(1e-3), math.log(3.0)),
             rng.uniform(math.log(1e-2), math.log(1e2))]
        trials.append((circle_integral(*params_to_box(p)), p))
    trials.sort(key=lambda t: -t[0])
    best = trials[0][0]
    print(f"(a) circle: best random I(B) = {best:.4f}")
    starts = [p for _, p in trials[:10]] + [[0.0, 0.0, math.log(2.0), 0.0],
                                             [0.0, 0.0, math.log(1.98), 0.0]]
    for p in starts:
        r = minimize(lambda z: -circle_integral(*params_to_box(z)), p, method="Nelder-Mead",
                     options={"maxiter": 400, "xatol": 1e-6, "fatol": 1e-8})
        best = max(best, -r.fun)
    print(f"(a) circle: best after refinement I(B) = {best:.4f}; "
          f"full bounding square gives {circle_integral(-1, 1, -1, 1):.4f} (= 2 pi); "
          f"lemma bound = {bound:.4f}")
    cinf, _ = integrate.quad(lambda h: 2 * math.asin(1 / math.sqrt(1 + 4 * h * (1 - h))), 0, 1)
    for k in (1, 2, 4, 8, 16, 64, 256):
        hs = (np.arange(1, k + 1) - 0.5) / k
        I = float(np.sum(2 * np.arcsin(1 / np.sqrt(1 + 4 * hs * (1 - hs)))))
        print(f"(b) comb k={k:4d}: I(B) = {I:9.3f}, I/k = {I / k:.4f}, lemma bound pi*sqrt2*k = "
              f"{math.pi * math.sqrt(2) * k:9.3f}")
    print(f"(b) limit I/k -> {cinf:.4f}")

    def spiral(T):
        def g(t):
            rho, drho = 1 + 1 / (1 + t), -1 / (1 + t) ** 2
            x, y = rho * math.cos(t), rho * math.sin(t)
            q = (x + 2) * (2 - x) + (y + 2) * (2 - y)
            return q ** -0.5 * math.sqrt(rho * rho + drho * drho)
        pts = [2 * math.pi * k for k in range(1, int(T / (2 * math.pi)) + 1)]
        return integrate.quad(g, 0, T, points=pts[:500], limit=5000)[0]
    for T in (10.0, 100.0, 1000.0):
        v = spiral(T)
        print(f"(c) spiral T={T:7.1f}: integral = {v:10.3f}, integral/T = {v / T:.4f}")


if __name__ == "__main__":
    main()
