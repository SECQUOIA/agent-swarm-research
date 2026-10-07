"""Independent check of the sharp Lemma 2 (confirmation review, round 2).

Reduction (checked by hand): Delta_U + Delta_L over [c-h/2, c+h/2] equals the
slope rise of the convex function phi = L_v - U_c, and admissibility is
phi <= M (s-c)^2 on [c-h, c+h], w(c) = -phi(c).  Conversely every such phi is
admissible (U = (M/2)(s-c)^2).  So the sharp claim is

    sup { phi'(c+h/2 -) - phi'(c-h/2 +) } = 4 w(c)/h + 4 M h.

Here phi = max_k (a_k + b_k s) (convex piecewise linear), shifted down so that
max_{[c-h, c+h]} (phi - M (s-c)^2) = 0 exactly (piecewise: each affine piece
minus the parabola is a concave quadratic, maximized in closed form).  One-
sided derivatives of a max of affine functions are exact (min / max of the
active slopes).  Parts:
  (1) random phi: ratio (rise)/(4 w/h + 4 M h) must be <= 1;
  (2) differential evolution over 2-4 pieces: sup should approach 1, not exceed;
  (3) with the same phi, the pairs (a, b) = (3.9, 4) and (4, 3.9) must be
      violated by some admissible phi (so neither coefficient can be lowered).
This code does not use the note's scripts.
"""
import numpy as np
from scipy.optimize import differential_evolution


def shift_below(a, b, M, c, h):
    # max over s in [c-h, c+h] of a_k + b_k s - M (s-c)^2, over k
    lo, hi = c - h, c + h
    best = -np.inf
    for ak, bk in zip(a, b):
        cands = [lo, hi]
        if M > 0:
            v = c + bk / (2 * M)
            if lo < v < hi:
                cands.append(v)
        for s in cands:
            best = max(best, ak + bk * s - M * (s - c) ** 2)
    return a - best


def rise_and_w(a, b, c, h):
    def active(s):
        v = a + b * s
        mx = v.max()
        return np.abs(v - mx) <= 1e-12 * (1 + abs(mx))
    al, be = c - h / 2, c + h / 2
    left_at_beta = b[active(be)].min()   # left derivative of a max = min slope
    right_at_alpha = b[active(al)].max()  # right derivative = max slope
    w = -(a + b * c).max()
    return left_at_beta - right_at_alpha, w


def ratio(params, M, c, h, K, A=4.0, Bc=4.0):
    a = np.array(params[:K]); b = np.array(params[K:2 * K])
    a = shift_below(a, b, M, c, h)
    rise, w = rise_and_w(a, b, c, h)
    assert w >= -1e-12
    w = max(w, 0.0)
    den = A * w / h + Bc * M * h
    return rise / den if den > 0 else (0.0 if rise <= 1e-12 else np.inf)


def main():
    rng = np.random.default_rng(20260930)
    worst = 0.0
    n = 0
    for _ in range(20000):
        K = int(rng.integers(1, 7))
        M = float(rng.choice([0.0, 0.1, 1.0, 5.0]))
        h = float(rng.uniform(0.05, 1.0))
        c = float(rng.uniform(-1, 1))
        a = rng.normal(size=K) * rng.choice([0.01, 0.1, 1.0])
        b = rng.normal(size=K) * rng.choice([0.1, 1.0, 10.0])
        r = ratio(np.r_[a, b], M, c, h, K)
        if np.isfinite(r):
            worst = max(worst, r); n += 1
    print(f"(1) random convex piecewise-linear phi: {n} cases, "
          f"max rise/(4w/h + 4Mh) = {worst:.6f}")
    ok = worst <= 1 + 1e-9

    print("(2) differential evolution (maximize ratio):")
    for (M, h, c, K) in [(0.0, 1.0, 0.0, 3), (1.0, 1.0, 0.0, 3),
                         (1.0, 0.5, 0.2, 4), (5.0, 0.3, -0.4, 4),
                         (0.1, 0.8, 0.1, 2)]:
        bounds = [(-3, 3)] * K + [(-30, 30)] * K
        res = differential_evolution(lambda p: -ratio(p, M, c, h, K), bounds,
                                     seed=1, maxiter=600, tol=1e-12,
                                     polish=True)
        best = -res.fun
        ok = ok and best <= 1 + 1e-9
        print(f"    M={M}, h={h}, c={c}, pieces={K}: max ratio {best:.10f} (ratio - 1 = {best - 1:.2e})")

    print("(3) lowered coefficients are violated by the note's family "
          "(phi = -W + k(|s-c| - a)_+, a = h/2 - 1e-6):")
    for (W, M, h, A, Bc) in [(1.0, 0.0, 1.0, 3.9, 4.0), (0.0, 1.0, 1.0, 4.0, 3.9),
                             (0.3, 2.0, 0.5, 3.9, 4.0), (0.3, 2.0, 0.5, 4.0, 3.9)]:
        c, dl = 0.0, 1e-6
        a0 = h / 2 - dl
        k = (M * h * h + W) / (h / 2 + dl)
        if k < 2 * M * h:
            k = 2 * M * a0 + 2 * np.sqrt(M * M * a0 * a0 + M * W)
        # phi as a max of three affine pieces
        av = np.array([-W, -W - k * (c + a0), -W + k * (c - a0)])
        bv = np.array([0.0, k, -k])
        # admissibility: max(phi - M s^2) <= 0 exactly
        sh = shift_below(av, bv, M, c, h)
        slack = (av - sh)[0]   # amount by which phi could be raised
        rise, w = rise_and_w(av, bv, c, h)
        viol = rise > A * w / h + Bc * M * h
        print(f"    W={W}, M={M}, h={h}: admissible (max(phi - M s^2) = "
              f"{-slack:.1e}), rise {rise:.6f} vs {A} w/h + {Bc} M h = "
              f"{A * w / h + Bc * M * h:.6f}: violated {viol}")
        ok = ok and viol and -slack <= 1e-12
    print("all checks as claimed:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
