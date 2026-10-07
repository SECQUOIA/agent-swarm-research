"""Independent check of Proposition 6 of adaptive-matching.md (rule bd of covering-upper-half.md on the
quadratic path F = sum_t s_t^2 + b sum_t s_t s_{t+1}, exact-bag model), written without the authors'
check_bd_qg.py.

* Value-function coefficients from linear algebra (Schur complements), not from the Riccati
  recursion: U_t(s) = u_t s^2 (min over s_{t+1..n} of the bags below edge t), w_t(s) = q_t s^2 with
  q_t = 1/(2 (H^{-1})_{tt}), H = Hessian of F; these are compared with the Riccati values of the note.
* Bracket g(D) of Theorem 1(c) of the covering note for the affine class, by bounded Brent search over
  the slope (the constant cancels), cross-checked on random cells by a dense slope grid.
* The inequality g(D) >= |p| r^2 - (q/(2n))(2 d^2 + r^2) of the proof is checked on every cell tested.
* Rule bd: split a dyadic cell of [-1,1] while g(D) > eps/n. Cells per edge and the bound
  floor((1/2) log2(q_t/eps)) sqrt((n-5)/2)/12 for edges t <= (n+1)/2 (n >= 25).
"""
import sys
import numpy as np
from scipy.optimize import minimize_scalar

B = 0.8


def coeffs(n, b):
    H = 2 * np.eye(n) + b * (np.eye(n, k=1) + np.eye(n, k=-1))
    Hi = np.linalg.inv(H)
    q = 1.0 / (2.0 * np.diag(Hi))          # w_t = min{F : s_t = s} = s^2 / (2 (H^-1)_tt)
    u = np.zeros(n)
    for t in range(n):                      # U_t: F restricted to the bags below edge t:
        # sum_{u=t}^{n-1} (b s_u s_{u+1} + s_{u+1}^2) (1-indexed); here 0-indexed variables t..n-1
        m = n - t
        if m == 1:
            u[t] = 0.0
            continue
        Hs = np.zeros((m, m))
        for a in range(m - 1):
            Hs[a, a + 1] += b
            Hs[a + 1, a] += b
            Hs[a + 1, a + 1] += 2
        # min over y = s_{t+1..} of [s, y] Hs [s, y]/2 with s fixed: s^2 (Hss - Hsy Hyy^-1 Hys)/2
        Hyy = Hs[1:, 1:]
        Hsy = Hs[0, 1:]
        u[t] = 0.5 * (Hs[0, 0] - Hsy @ np.linalg.solve(Hyy, Hsy))
    return u, q


def riccati(n, b):
    u = np.zeros(n + 1)
    v = np.zeros(n + 1)
    for t in range(n - 1, 0, -1):
        u[t] = -b * b / (4 * (1 + u[t + 1]))
    v[1] = 1.0
    for t in range(1, n):
        v[t + 1] = 1 - b * b / (4 * v[t])
    return u[1:], (u + v)[1:]


def G(m, a1, a2, lo, hi):
    A = max(m * lo + a1 * lo * lo, m * hi + a1 * hi * hi)
    s = min(max(-m / (2 * a2), lo), hi)
    return A + (-a2 * s * s - m * s)


def bracket(p, q, n, lo, hi):
    a1, a2 = abs(p) - q / (2 * n), abs(p) + q / (2 * n)
    assert p < 0 and a1 > -1e-14   # a1 = 0 on the last edge (u_n = 0, theta_n = 1/(2n))
    r = minimize_scalar(lambda m: G(m, a1, a2, lo, hi), bounds=(-20, 20), method="bounded",
                        options={"xatol": 1e-15, "maxiter": 2000})
    return r.fun


def bracket_grid(p, q, n, lo, hi):
    a1, a2 = abs(p) - q / (2 * n), abs(p) + q / (2 * n)
    ms = np.linspace(-20, 20, 400001)
    s = np.linspace(lo, hi, 2001)
    A = np.maximum(ms * lo + a1 * lo * lo, ms * hi + a1 * hi * hi)
    Bm = np.max(-a2 * s[None, :] ** 2 - ms[:, None] * s[None, :], axis=1) if len(ms) < 0 else None
    # exact inner max of the concave quadratic
    sc = np.clip(-ms / (2 * a2), lo, hi)
    Bm = -a2 * sc * sc - ms * sc
    return float(np.min(A + Bm))


def bd(p, q, n, eps):
    tol = eps / n
    out = []
    stack = [(-1.0, 1.0)]
    worst_ineq = np.inf
    while stack:
        lo, hi = stack.pop()
        g = bracket(p, q, n, lo, hi)
        d, r = 0.5 * (lo + hi), 0.5 * (hi - lo)
        lbg = abs(p) * r * r - (q / (2 * n)) * (2 * d * d + r * r)
        worst_ineq = min(worst_ineq, g - lbg)
        if g > tol:
            mid = 0.5 * (lo + hi)
            stack += [(lo, mid), (mid, hi)]
        else:
            out.append((lo, hi))
    return out, worst_ineq


def main():
    eps = float(sys.argv[1])
    ns = [int(a) for a in sys.argv[2:]]
    rng = np.random.default_rng(1)
    # cross-check the bracket on random cells
    n = 32
    u, q = coeffs(n, B)
    th = np.array([(2 * (n - t) + 1) / (2 * n) for t in range(1, n + 1)])
    p = u - th * q
    dev = 0.0
    for _ in range(30):
        t = rng.integers(0, n)
        lo = rng.uniform(-1, 0.9)
        hi = lo + rng.uniform(1e-3, 1 - lo) * 0.5
        dev = max(dev, abs(bracket(p[t], q[t], n, lo, hi) - bracket_grid(p[t], q[t], n, lo, hi)))
    print("bracket: Brent vs slope grid (30 random cells, n = 32): max |diff| = %.2e" % dev)
    for n in ns:
        u, q = coeffs(n, B)
        ur, qr = riccati(n, B)
        th = np.array([(2 * (n - t) + 1) / (2 * n) for t in range(1, n + 1)])
        p = u - th * q
        tot = 0
        minratio = np.inf
        worst = np.inf
        per_edge = []
        for t in range(1, n + 1):
            cells, wi = bd(p[t - 1], q[t - 1], n, eps)
            worst = min(worst, wi)
            tot += len(cells)
            per_edge.append(len(cells))
            if n >= 25 and t <= (n + 1) / 2:
                I = int(np.floor(0.5 * np.log2(q[t - 1] / eps)))
                lb = I * np.sqrt((n - 5) / 2) / 12
                minratio = min(minratio, len(cells) / lb)
        print("n=%4d bd cells=%7d per edge=%7.1f per edge/sqrt(n)=%5.2f  min/max per edge=%d/%d  "
              "max|u-u_ric|=%.1e max|q-q_ric|=%.1e  min_t q_t=%.4f (c_g=%.2f)  min cells/LB(edges t<=(n+1)/2)=%s  "
              "min[g - (|p|r^2 - q(2d^2+r^2)/2n)]=%.2e" % (
                  n, tot, tot / n, tot / n / np.sqrt(n), min(per_edge), max(per_edge),
                  np.abs(u - ur).max(), np.abs(q - qr).max(), q.min(), 1 - B,
                  ("%.2f" % minratio) if np.isfinite(minratio) else "n/a", worst), flush=True)


if __name__ == "__main__":
    main()
