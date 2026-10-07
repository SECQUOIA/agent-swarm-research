"""Independent check of Lemma 2 of covering-upper-half.md (kink
concentration in one dimension), with a construction different from the
author's and an adversarial optimizer.

U(s) = (M/2) s^2 - (k/2) s^2 + min_i (a_i + b_i s)   (M-semiconcave, k >= 0)
L(s) = -(M/2) s^2 + (k'/2) s^2 + max_j (c_j + d_j s) - shift   (M-semiconvex)
on I = [-1, 1].  The shift making L <= U on I is computed exactly (L - U is a
maximum of concave quadratics).  One-sided derivatives are exact.

Claim 1: Delta_U(J) + Delta_L(J) <= 8 w(c)/h + 8 M h, J = [c-h/2, c+h/2],
         [c-h, c+h] in I.
Claim 2: for an interval D of radius r and theta in [0,1], some affine l has
         osc_D(psi - l) <= (r/2)(Delta_U(D) + Delta_L(D)) + (M/2) r^2,
         psi = (1-theta) U + theta L.  (min over l computed on a fine grid
         of D by exact convex minimization in the slope.)
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar


class Pair:
    def __init__(self, M, k, a, b, kp, c, d):
        self.M, self.k, self.a, self.b = M, k, np.asarray(a), np.asarray(b)
        self.kp, self.c, self.d = kp, np.asarray(c), np.asarray(d)
        # exact sup over [-1,1] of L0 - U, L0 without shift:
        # L0 - U = max_{i,j} [-(M - (k + kp)/2) s^2 + (c_j - a_i) + (d_j - b_i) s]
        # (curvature coefficient Q = M - (k + kp)/2 may be of either sign)
        Q = M - (k + kp) / 2.0
        best = -np.inf
        for i in range(len(self.a)):
            for j in range(len(self.c)):
                A0, B0 = self.c[j] - self.a[i], self.d[j] - self.b[i]
                cands = [-1.0, 1.0]
                if Q > 0:
                    cands.append(np.clip(B0 / (2 * Q), -1, 1))
                for s in cands:
                    best = max(best, -Q * s * s + A0 + B0 * s)
        self.shift = best

    def U(self, s):
        return (self.M - self.k) / 2 * s ** 2 + np.min(self.a + self.b * s)

    def L(self, s):
        return (-(self.M) + self.kp) / 2 * s ** 2 + np.max(self.c + self.d * s) - self.shift

    def dU(self, s, side):
        v = self.a + self.b * s
        act = np.abs(v - v.min()) <= 1e-12 * (1 + abs(v.min()))
        g = (self.b[act].min() if side == "+" else self.b[act].max())
        return (self.M - self.k) * s + g

    def dL(self, s, side):
        v = self.c + self.d * s
        act = np.abs(v - v.max()) <= 1e-12 * (1 + abs(v.max()))
        g = (self.d[act].max() if side == "+" else self.d[act].min())
        return (-(self.M) + self.kp) * s + g

    def deltas(self, lo, hi):
        DU = self.dU(lo, "+") - self.dU(hi, "-") + self.M * (hi - lo)
        DL = self.dL(hi, "-") - self.dL(lo, "+") + self.M * (hi - lo)
        return DU, DL

    def ratio1(self, c, h):
        w = self.U(c) - self.L(c)
        DU, DL = self.deltas(c - h / 2, c + h / 2)
        return (DU + DL) / (8 * max(w, 0.0) / h + 8 * self.M * h), DU, DL, w


def min_osc(xs, ys):
    def f(lam):
        z = ys - lam * xs
        return z.max() - z.min()
    span = 4 * (np.max(np.abs(np.diff(ys) / np.diff(xs))) + 1)
    res = minimize_scalar(f, bounds=(-span, span), method="bounded",
                          options=dict(xatol=1e-12, maxiter=500))
    return res.fun


def random_pair(rng):
    M = float(rng.choice([0.1, 1.0, 5.0]))
    K1, K2 = int(rng.integers(1, 6)), int(rng.integers(1, 6))
    k = float(rng.choice([0.0, rng.uniform(0, 20)]))
    kp = float(rng.choice([0.0, rng.uniform(0, 20)]))
    scale = float(rng.choice([0.3, 1.0, 5.0]))
    return Pair(M, k, rng.normal(size=K1), scale * rng.normal(size=K1),
                kp, rng.normal(size=K2), scale * rng.normal(size=K2))


def main():
    rng = np.random.default_rng(2718)
    worst1, cnt1 = 0.0, 0
    worst2, cnt2 = 0.0, 0
    for trial in range(2000):
        P = random_pair(rng)
        for rep in range(30):
            h = float(rng.uniform(1e-3, 1.0))
            c = float(rng.uniform(-1 + h, 1 - h))
            if P.U(c + h) < P.L(c + h) - 1e-12 or P.U(c - h) < P.L(c - h) - 1e-12:
                continue
            rt, DU, DL, w = P.ratio1(c, h)
            cnt1 += 1
            worst1 = max(worst1, rt)
        for rep in range(3):
            r = float(rng.uniform(1e-3, 0.5))
            cc = float(rng.uniform(-1 + r, 1 - r))
            th = float(rng.uniform())
            xs = np.linspace(cc - r, cc + r, 4001)
            ys = np.array([(1 - th) * P.U(x) + th * P.L(x) for x in xs])
            DU, DL = P.deltas(cc - r, cc + r)
            rhs = (r / 2) * (DU + DL) + (P.M / 2) * r ** 2
            lhs = min_osc(xs, ys)
            cnt2 += 1
            if rhs > 1e-12:
                worst2 = max(worst2, lhs / rhs)
    print("Lemma 2, random piecewise-linear-plus-quadratic pairs")
    print(f"claim 1: {cnt1} (c, h) cases, max ratio "
          f"(Delta_U + Delta_L)/(8w/h + 8Mh) = {worst1:.4f}")
    print(f"claim 2: {cnt2} cases, max ratio osc/((r/2)(DU+DL) + M r^2/2) "
          f"= {worst2:.4f}")

    # adversarial: two concave pieces for U - Ms^2/2 and two convex pieces
    # for L + Ms^2/2 (plus strong curvatures), c and h free; M = 1.
    def neg_ratio(p):
        a1, a2, b1, b2, c1, c2, d1, d2, k, kp, cpos, hh = p
        P = Pair(1.0, k, [a1, a2], [b1, b2], kp, [c1, c2], [d1, d2])
        h = hh
        c = cpos * (1 - h)
        if P.U(c + h) < P.L(c + h) - 1e-12 or P.U(c - h) < P.L(c - h) - 1e-12:
            return 0.0
        return -P.ratio1(c, h)[0]

    bounds = ([(-3, 3)] * 2 + [(-20, 20)] * 2 + [(-3, 3)] * 2 + [(-20, 20)] * 2
              + [(0, 30), (0, 30), (-1, 1), (1e-3, 1.0)])
    best = 0.0
    for seed in range(6):
        res = differential_evolution(neg_ratio, bounds, seed=seed, maxiter=400,
                                     popsize=30, tol=1e-10, polish=True)
        best = max(best, -res.fun)
    print(f"claim 1, adversarial (differential evolution, 6 seeds): max ratio "
          f"{best:.4f}")
    # analytic families
    for x in [0.5, 1.0, 2.0]:
        J, M = 0.4, 1.0
        h = x * J / M
        # U = -J|s| + (M/2)s^2 + a, L = J|s| - (M/2)s^2 - b, a + b = J^2/M
        P = Pair(M, 0.0, [0.0, 0.0], [J, -J], 0.0, [0.0, 0.0], [J, -J])
        print(f"   family U=-J|s|+Ms^2/2, L=J|s|-Ms^2/2-J^2/M at c=0, "
              f"x=Mh/J={x}: ratio {P.ratio1(0.0, h)[0]:.4f}")


if __name__ == "__main__":
    main()


def edge_kink_family():
    """U = -J (s - p)_+ (concave kink at p = h/2 - delta), L = J (q - s)_+
    - shift (convex kink at q = -h/2 + delta), c = 0, h = 1, I = [-1, 1],
    M small.  Then w(0) = J (1/2 + delta) and Delta_U + Delta_L -> 2J, so the
    ratio tends to 1/2: the constant 8 of Lemma 2 cannot be lowered below 4."""
    out = []
    for M, delta in [(1e-2, 1e-2), (1e-4, 1e-3), (1e-6, 1e-4)]:
        J, h, p, q = 1.0, 1.0, 0.5 - delta, -0.5 + delta
        P = Pair(M, M, [0.0, J * p], [0.0, -J], M, [0.0, J * q], [0.0, -J])
        r, DU, DL, w = P.ratio1(0.0, h)
        out.append((M, delta, r, DU, DL, w))
    return out


if __name__ == "__main__":
    for M, delta, r, DU, DL, w in edge_kink_family():
        print(f"   edge-kink family M={M:g}, delta={delta:g}: Delta_U={DU:.4f}, "
              f"Delta_L={DL:.4f}, w(0)={w:.4f}, ratio {r:.4f}")
