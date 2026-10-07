"""Full-precision E2 gaps f* - l_r at h = 2^-2 and 2^-4 (n = 8, seed 0, theta = 1/8),
with PAIR_TOL = 0 (first version) and 1e-12 (current), both slopes."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition"))
import dp_certificate as dc
import run_experiments as rx
n = 8
c = rx.c_vec(n, 0)
xs, fs, _ = rx.global_min(n, rx.B, rx.KAPPA, c)
print("f* = %.15f" % fs)
for j in (2, 4):
    for slopes in ("affine", "zero"):
        row = []
        for tol in (0.0, 1e-12):
            dc.PAIR_TOL = tol
            r, size, _, _ = dc.certificate(n, rx.B, rx.KAPPA, c, xs, 2.0 ** -j, 3, slopes)
            row.append(fs - r)
        print("h=2^-%d %-6s gap(tol=0)=%.6e gap(tol=1e-12)=%.6e diff=%+.4e" % (j, slopes, row[0], row[1], row[1] - row[0]))
