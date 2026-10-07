"""Check of Lemma 2 (kink concentration in one dimension).

U = min of quadratics with curvature <= M (so U is M-semiconcave; very
negative curvatures and crossings give strong concavity and concave kinks),
L = max of quadratics with curvature >= -M (M-semiconvex), shifted so that
L <= U with contact.  For random c, h with [c-h, c+h] in [-1, 1]:

  Delta_U = U'((c-h/2)+) - U'((c+h/2)-) + M h   (slope drop of U - M s^2/2)
  Delta_L = L'((c+h/2)-) - L'((c-h/2)+) + M h   (slope rise of L + M s^2/2)

Lemma 2 claims Delta_U + Delta_L <= 8 w(c)/h + 8 M h, w = U - L.
One-sided derivatives are exact (active pieces of the min / max).
Also prints the explicit family U = -J|s|, L = -J^2/(2M) - M s^2/2, and
(added after review) a two-kink family whose ratio tends to 1/2 and a
w = 0 example.

Added in revision round 2: the sharp form
Delta_U + Delta_L <= 4 w(c)/h + 4 M h.  The random pairs are compared with
it as well (same random numbers, so the earlier lines do not change), and
an explicit family approaches equality for every (w(c), M, h): with
phi = L_v - U_c convex (L_v = L + (M/2)(s-c)^2, U_c = U - (M/2)(s-c)^2),
U = (M/2)(s-c)^2 and phi = -W on [c-a, c+a], a = h/2 - delta, rising
with slope k outside.  w = M (s-c)^2 - phi >= 0 on [c-h, c+h] needs the line
-W + k (v - a) (v = |s - c|) to stay below M v^2 on [a, h]:
k = (M h^2 + W)/(h/2 + delta) (the line through (h, M h^2)) if that is
>= 2 M h, otherwise the tangent slope 2 M a + 2 sqrt(M^2 a^2 + M W).
The first case applies for small delta when W > 0, the second when W = 0.
"""
import numpy as np


def make_pieces(rng, k, M, sign):
    # sign = +1: pieces for U (curvature <= M); -1: pieces for L (>= -M)
    a = rng.uniform(-1, 1, k)
    b = rng.uniform(-3, 3, k)
    c = np.where(rng.uniform(size=k) < 0.5,
                 rng.uniform(-60, M, k), rng.uniform(-M, M, k))
    if sign < 0:
        c = -c
    return a, b, c


def ev(p, x):
    a, b, c = p
    return a + b * x + 0.5 * c * x ** 2, b + c * x


def env(p, x, mode):
    v, d = ev(p, x)
    return v.min() if mode == "min" else v.max()


def one_sided(p, x, mode, side):
    v, d = ev(p, x)
    best = v.min() if mode == "min" else v.max()
    act = np.abs(v - best) <= 1e-12 * (1 + abs(best))
    ds = d[act]
    # right derivative of min = min of active derivatives; left = max
    if mode == "min":
        return ds.min() if side == "+" else ds.max()
    return ds.max() if side == "+" else ds.min()


def main():
    rng = np.random.default_rng(7)
    worst = 0.0
    worst_info = None
    worst4 = 0.0
    count = 0
    xs = np.linspace(-1, 1, 20001)
    for trial in range(300):
        M = float(rng.choice([0.1, 1.0, 5.0]))
        pu = make_pieces(rng, int(rng.integers(1, 6)), M, +1)
        pl = make_pieces(rng, int(rng.integers(1, 6)), M, -1)
        Uv = np.min(ev(pu, xs[:, None])[0], axis=1)
        Lv = np.max(ev(pl, xs[:, None])[0], axis=1)
        shift = np.max(Lv - Uv)
        # exact shift: refine the contact with a local search
        pl = (pl[0] - shift, pl[1], pl[2])
        for rep in range(200):
            h = float(rng.uniform(1e-3, 1.0))
            c = float(rng.uniform(-1 + h, 1 - h))
            w = env(pu, c, "min") - env(pl, c, "max")
            if w < -1e-9:
                continue
            w = max(w, 0.0)
            dU = (one_sided(pu, c - h / 2, "min", "+")
                  - one_sided(pu, c + h / 2, "min", "-") + M * h)
            dL = (one_sided(pl, c + h / 2, "max", "-")
                  - one_sided(pl, c - h / 2, "max", "+") + M * h)
            lhs = dU + dL
            rhs = 8 * w / h + 8 * M * h
            count += 1
            worst4 = max(worst4, lhs / (4 * w / h + 4 * M * h))
            if lhs / rhs > worst:
                worst = lhs / rhs
                worst_info = (trial, M, c, h, w, dU, dL)
    print("Lemma 2 (kink concentration): random semiconcave/semiconvex pairs")
    print(f"cases: {count}; max (Delta_U + Delta_L)/(8 w(c)/h + 8 M h) = "
          f"{worst:.4f}")
    print(f"  worst case: trial={worst_info[0]}, M={worst_info[1]}, "
          f"c={worst_info[2]:.3f}, h={worst_info[3]:.3f}, w(c)={worst_info[4]:.3e}, "
          f"Delta_U={worst_info[5]:.3f}, Delta_L={worst_info[6]:.3f}")
    print("Explicit family U=-J|s|, L=-J^2/(2M)-M s^2/2 at c=0 "
          "(ratio as a function of x = M h/J):")
    for x in [0.25, 0.5, 1.0, 2.0, 4.0]:
        J, M = 1.0, 1.0
        h = x * J / M
        lhs = 2 * J + M * h
        rhs = 8 * (J ** 2 / (2 * M)) / h + 8 * M * h
        print(f"  x={x:4.2f}: ratio {lhs / rhs:.4f}")
    # Added after review (R1): a family with ratio -> 1/2, so the
    # coefficient of w(c)/h cannot be lowered below 4.  I = [-1, 1], c = 0,
    # h = 1, U = -J (s - p)_+ with p = 1/2 - delta (concave), and
    # L = J (q - s)_+ - J (1/2 + delta) with q = -1/2 + delta (convex).
    # Both kinks lie inside [-1/2, 1/2], so Delta_U = Delta_L = J + M.
    print("Two-kink family (after review): U = -J(s-p)_+, "
          "L = J(q-s)_+ - J(1/2+delta), c = 0, h = 1, J = 1")
    xs2 = np.linspace(-1, 1, 200001)
    fam_ok = True
    for M, delta in [(1e-2, 1e-2), (1e-4, 1e-3), (1e-6, 1e-4), (0.0, 1e-6)]:
        J, c, h = 1.0, 0.0, 1.0
        p, q = 0.5 - delta, -0.5 + delta
        pu = (np.array([0.0, J * p]), np.array([0.0, -J]),
              np.array([0.0, 0.0]))
        pl = (np.array([J * q - J * (0.5 + delta), -J * (0.5 + delta)]),
              np.array([-J, 0.0]), np.array([0.0, 0.0]))
        Uv = np.min(ev(pu, xs2[:, None])[0], axis=1)
        Lv = np.max(ev(pl, xs2[:, None])[0], axis=1)
        gap_min = np.min(Uv - Lv)
        w = env(pu, c, "min") - env(pl, c, "max")
        dU = (one_sided(pu, c - h / 2, "min", "+")
              - one_sided(pu, c + h / 2, "min", "-") + M * h)
        dL = (one_sided(pl, c + h / 2, "max", "-")
              - one_sided(pl, c - h / 2, "max", "+") + M * h)
        ratio = (dU + dL) / (8 * w / h + 8 * M * h)
        fam_ok = fam_ok and gap_min >= -1e-12
        print(f"  M={M:g}, delta={delta:g}: min(U - L) on grid = "
              f"{gap_min:.1e}, w(0) = {w:.6f}, Delta_U = {dU:.6f}, "
              f"Delta_L = {dL:.6f}, ratio {ratio:.4f}, "
              f"(Delta_U + Delta_L)/(w/h) = {(dU + dL) / (w / h):.4f}")
    # w = 0 example: U = L = -M s^2/2 gives Delta_U + Delta_L = 2 M h, so
    # the coefficient of M h cannot be lowered below 2.
    M, h, c = 1.0, 0.5, 0.0
    pu = (np.array([0.0]), np.array([0.0]), np.array([-M]))
    dU = (one_sided(pu, c - h / 2, "min", "+")
          - one_sided(pu, c + h / 2, "min", "-") + M * h)
    dL = (one_sided(pu, c + h / 2, "max", "-")
          - one_sided(pu, c - h / 2, "max", "+") + M * h)
    print(f"w = 0 example U = L = -M s^2/2 (M = 1, h = 0.5): Delta_U + "
          f"Delta_L = {dU + dL:.4f} = {(dU + dL) / (M * h):.2f} M h")
    # Added in revision round 2: the sharp constants (4, 4).
    print("Sharp form (revision round 2): Delta_U + Delta_L <= "
          "4 w(c)/h + 4 M h")
    print(f"  random pairs above: max ratio to 4 w/h + 4 M h = {worst4:.4f}")
    print("  family approaching equality (U = (M/2)(s-c)^2, "
          "L = phi - (M/2)(s-c)^2, phi flat on [c-a, c+a], a = h/2 - delta, "
          "then slope k; see docstring):")
    sharp_ok = worst4 <= 1 + 1e-9
    for W, M, h, c in [(1.0, 0.0, 1.0, 0.0), (0.0, 1.0, 1.0, 0.0),
                       (1.0, 1.0, 1.0, 0.0), (0.05, 2.0, 0.4, 0.3),
                       (2.0, 0.1, 0.8, -0.1)]:
        for delta in [1e-2, 1e-4, 1e-6]:
            a = h / 2 - delta
            k_end = (M * h ** 2 + W) / (h / 2 + delta)
            if k_end >= 2 * M * h:
                k = k_end
            else:
                k = 2 * M * a + 2 * np.sqrt(M ** 2 * a ** 2 + M * W)
            # pieces a0 + b x + 0.5 c2 x^2 in the variable x (not centred)
            pu = (np.array([0.5 * M * c ** 2]), np.array([-M * c]),
                  np.array([M]))
            # phi pieces: -W, -W + k (x - c - a), -W + k (c - a - x);
            # L = phi - (M/2)(x - c)^2
            base = (-0.5 * M * c ** 2, M * c, -M)
            pl = (np.array([-W + base[0], -W - k * (c + a) + base[0],
                            -W + k * (c - a) + base[0]]),
                  np.array([base[1], k + base[1], -k + base[1]]),
                  np.array([base[2]] * 3))
            xs3 = np.linspace(c - h, c + h, 200001)
            Uv = np.min(ev(pu, xs3[:, None])[0], axis=1)
            Lv = np.max(ev(pl, xs3[:, None])[0], axis=1)
            gap_min = np.min(Uv - Lv)
            w = env(pu, c, "min") - env(pl, c, "max")
            dU = (one_sided(pu, c - h / 2, "min", "+")
                  - one_sided(pu, c + h / 2, "min", "-") + M * h)
            dL = (one_sided(pl, c + h / 2, "max", "-")
                  - one_sided(pl, c - h / 2, "max", "+") + M * h)
            ratio = (dU + dL) / (4 * w / h + 4 * M * h)
            sharp_ok = sharp_ok and gap_min >= -1e-12 and ratio <= 1 + 1e-12
            print(f"    W={W:g}, M={M:g}, h={h:g}, c={c:g}, delta={delta:g}: "
                  f"min(U - L) = {gap_min:.1e}, w(c) = {w:.6f}, "
                  f"Delta_U + Delta_L = {dU + dL:.6f}, "
                  f"ratio to 4 w/h + 4 M h = {ratio:.6f}")
    return 0 if (worst <= 1 + 1e-9 and fam_ok and sharp_ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
