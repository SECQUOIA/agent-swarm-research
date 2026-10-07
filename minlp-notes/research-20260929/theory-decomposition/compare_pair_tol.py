"""Root bounds of the E2, E3 and E4 certificates with PAIR_TOL = 0 (first version) and 1e-12
(current dp_certificate.py), printed at full precision (Section 8.3 of
decomposition-certificates.md).

E4 at theta = 1/64 is left out: the dense pair arrays of certificate() need more than 10 GB there
(its roots are in logs/theta64_chunked.log, from a row-chunked copy; Section 8.4).
Usage: python3 compare_pair_tol.py
"""
import time
import numpy as np
import dp_certificate as dc
from run_experiments import c_vec, B, KAPPA


def cases():
    c = c_vec(8, 0)
    xs = dc.global_min(8, B, KAPPA, c)[0]
    for j in range(2, 17, 2):
        for s in ["affine", "zero"]:
            yield "E2 h=2^-%d %s" % (j, s), 8, c, xs, 2.0 ** -j, 3, s
    for n, seed, mu, j in [(4, 0, 3, 6), (6, 0, 3, 8), (6, 1, 2, 5), (5, None, 1, 4)]:
        c = c_vec(n, seed)
        xs = dc.global_min(n, B, KAPPA, c)[0]
        for s in ["affine", "zero"]:
            yield "E3 n=%d seed=%s %s" % (n, seed, s), n, c, xs, 2.0 ** -j, mu, s
    c = c_vec(3, 0)
    xs = dc.global_min(3, B, KAPPA, c)[0]
    for mu in range(1, 6):
        for s in ["affine", "zero"]:
            yield "E4 theta=2^-%d %s" % (mu, s), 3, c, xs, 2.0 ** -14, mu, s


count = {"same": 0, "higher": 0, "lower": 0}
for name, n, c, xs, h, mu, s in cases():
    t0 = time.time()
    roots = []
    for tol in [0.0, 1e-12]:
        dc.PAIR_TOL = tol
        roots.append(dc.certificate(n, B, KAPPA, c, xs, h, mu, s)[0])
    r0, r1 = roots
    tag = "same" if r0 == r1 else ("higher" if r0 > r1 else "lower")
    dyadic = not np.any(xs)
    if not dyadic:
        count[tag] += 1
    print("%-22s x*=0:%-5s root(tol=0)=%.17g root(tol=1e-12)=%.17g diff=%.3e %s %.0fs" % (
        name, dyadic, r0, r1, r0 - r1, tag, time.time() - t0), flush=True)
print("non-dyadic certificates: %d; tol=0 root identical: %d, higher: %d, lower: %d" % (
    sum(count.values()), count["same"], count["higher"], count["lower"]))
