"""Confirmation check for Sections A.5 / C.3 of extension-adaptive.md (revised): is the RC trajectory
with the widened intersection test (tol = 1e-12) reproducible under tiny perturbations?

  python3 rc_robustness.py pairs            # round-1 partition: gaps of the pairs added by tol
  python3 rc_robustness.py traj SEED JMAX   # RC trajectory, n = 16, eps = 1e-4, several variants

Variants (all use the author's rc_lib.shell_partition and ls_lib.dp; the RC loop is re-coded here
so that a perturbation can be injected):
  base      tol = 1e-12, x0 = 0                         (must reproduce logs/rc_random_n16_eps1e-4_tol.log)
  tol1e-10  tol = 1e-10
  x0pert    x0 = 1e-12 * (random signs)
  c1pert    centre of round 1 moved by 1e-9 towards 0 in coordinate 2 (at +1 for seed 0)
  c6pert    centre of round 1 moved by 1e-9 in coordinate 6 (interior for seed 0)
"""
import os
import sys
import time
import numpy as np

AD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition", "adaptive")
sys.path.insert(0, AD)
from ls_lib import dp, slopes, F, global_min, interval_pairs  # noqa: E402
from rc_lib import shell_partition  # noqa: E402

B, KAPPA, MU, N, EPS = 0.8, 0.1, 4, 16, 1e-4


def rc(c, x0, tol, jmax, pert=None, xs=None, fs=None):
    UBD = F(x0, B, KAPPA, c)
    xhat = x0.copy()
    rows = []
    for j in range(jmax + 1):
        if pert is not None and j == pert[0]:
            xhat = xhat.copy()
            xhat[pert[1]] += pert[2]
        h = 2.0 * 2.0 ** -j
        P = shell_partition(N, xhat, h, MU)
        R = dp(P, slopes(xhat, B, KAPPA, c), B, KAPPA, c, tol=tol)
        UBD = min(UBD, F(R["x"], B, KAPPA, c))
        rows.append((j, R["lr"], UBD, float(np.abs(xhat - xs).max()) / h, fs - R["lr"]))
        if R["lr"] >= UBD - EPS:
            break
        xhat = R["x"]
    return rows


def traj(seed, jmax):
    c = np.random.default_rng(seed).uniform(-0.2, 0.2, N)
    xs, fs, _ = global_min(N, B, KAPPA, c)
    print("seed %d f*=%.6f" % (seed, fs), flush=True)
    rng = np.random.default_rng(123)
    variants = [("base", 1e-12, np.zeros(N), None),
                ("tol1e-10", 1e-10, np.zeros(N), None),
                ("x0pert", 1e-12, 1e-12 * rng.choice([-1.0, 1.0], N), None),
                ("c1pert", 1e-12, np.zeros(N), (1, 2, -1e-9)),
                ("c6pert", 1e-12, np.zeros(N), (1, 6, 1e-9))]
    res = {}
    for name, tol, x0, pert in variants:
        t0 = time.time()
        res[name] = rc(c, x0, tol, jmax, pert, xs, fs)
        print("  %-8s done in %.0fs" % (name, time.time() - t0), flush=True)
    print("  j | " + " | ".join("%-30s" % v[0] for v in variants))
    for j in range(jmax + 1):
        cells = []
        for v in variants:
            r = res[v[0]]
            cells.append("%-30s" % ("gap=%.3e UBD=% .4f cen/h=%.3g" % (r[j][4], r[j][2], r[j][3]) if j < len(r) else "(stopped)"))
        print(" %2d | " % j + " | ".join(cells), flush=True)


def pairs():
    """Round-1 partition of seed 0 (as in check_rc_sensitivity.py): for every (leaf, cell) pair
    found with tol = 1e-12 but not with tol = 0, the exact-arithmetic gap between the leaf's
    S-interval and the cell (positive = disjoint in floating point)."""
    c = np.random.default_rng(0).uniform(-0.2, 0.2, N)
    P0 = shell_partition(N, np.zeros(N), 2.0, MU)
    x1 = dp(P0, slopes(np.zeros(N), B, KAPPA, c), B, KAPPA, c)["x"]
    P = shell_partition(N, x1, 1.0, MU)
    gaps = []
    nadd = 0
    for t in range(1, N - 1):
        L, S = P.leaves[t], P.cells[t]
        k0, d0 = interval_pairs(S["lo"], S["hi"], L["l1"], L["u1"], 0.0)
        k1, d1 = interval_pairs(S["lo"], S["hi"], L["l1"], L["u1"], 1e-12)
        a = set(zip(k0.tolist(), d0.tolist()))
        for k, d in zip(k1.tolist(), d1.tolist()):
            if (k, d) not in a:
                nadd += 1
                g = max(S["lo"][d] - L["u1"][k], L["l1"][k] - S["hi"][d])
                gaps.append(g)
        # also the child side: leaf of bag t-1 (second coordinate) against cell of S_t
        Lp = P.leaves[t - 1]
        k0, d0 = interval_pairs(S["lo"], S["hi"], Lp["l2"], Lp["u2"], 0.0)
        k1, d1 = interval_pairs(S["lo"], S["hi"], Lp["l2"], Lp["u2"], 1e-12)
        a = set(zip(k0.tolist(), d0.tolist()))
        for k, d in zip(k1.tolist(), d1.tolist()):
            if (k, d) not in a:
                nadd += 1
                gaps.append(max(S["lo"][d] - Lp["u2"][k], Lp["l2"][k] - S["hi"][d]))
    gaps = np.array(gaps)
    print("pairs added by tol=1e-12 at round 1 (seed 0): %d; gap min %.3e max %.3e; "
          "number with gap > 4.5e-16 (more than ~2 ulp at |x|<=1): %d" % (
              nadd, gaps.min() if nadd else 0, gaps.max() if nadd else 0, int(np.sum(gaps > 4.5e-16))))
    # are cell partitions themselves gap-free in floating point?
    worst = 0.0
    for t in range(1, N - 1):
        S = P.cells[t]
        o = np.argsort(S["lo"])
        worst = max(worst, float(np.max(S["lo"][o][1:] - S["hi"][o][:-1])))
    print("largest floating-point gap between consecutive cells of one separator: %.3e" % worst)


if __name__ == "__main__":
    if sys.argv[1] == "pairs":
        pairs()
    else:
        traj(int(sys.argv[2]), int(sys.argv[3]))
