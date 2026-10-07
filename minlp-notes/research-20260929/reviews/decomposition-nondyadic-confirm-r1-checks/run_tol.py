"""Run an experiment of run_experiments.py with dp_certificate.PAIR_TOL set from the command line.
Usage: python3 run_tol.py TOL E2|E3|E4|E4m5
E4m5 is E4 restricted to mu = 1..5 (theta = 1/2 .. 1/32, the rows quoted in Section 5.3).
The theory-decomposition files are imported unchanged; only the module constant is overridden."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition"))
import dp_certificate
import run_experiments as rx
import numpy as np

tol = float(sys.argv[1])
dp_certificate.PAIR_TOL = tol
exp = sys.argv[2]
if exp == "E4m5":
    n, seed = 3, 0
    c = rx.c_vec(n, seed)
    xs, fs, _ = rx.global_min(n, rx.B, rx.KAPPA, c)
    lam = [rx.dphi(xs[t], rx.KAPPA) + c[t] + rx.B * xs[t + 1] for t in range(1, n - 1)]
    print("# E4: n=%d seed %d, h=2^-14; slopes %s; x* = %s" % (n, seed, np.array2string(np.array(lam), precision=4), np.array2string(xs, precision=4)))
    print("# mu theta gap_affine gap_zero size")
    for mu in range(1, 6):
        ra, size, _, _ = rx.certificate(n, rx.B, rx.KAPPA, c, xs, 2.0 ** -14, mu, "affine")
        rz, _, _, _ = rx.certificate(n, rx.B, rx.KAPPA, c, xs, 2.0 ** -14, mu, "zero")
        print("%d %.4f %.3e %.3e %d" % (mu, 2.0 ** -mu, fs - ra, fs - rz, size), flush=True)
else:
    {"E2": rx.E2, "E3": rx.E3}[exp]()
