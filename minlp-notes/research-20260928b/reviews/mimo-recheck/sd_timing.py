"""Wall-clock time of the two searches of sd_vs_box.py (single thread, this
Python implementation; indicative only)."""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import time
import numpy as np
from rc_common import make_instance
from sd_vs_box import fp_count, box_static

for N in (32, 64):
    rho = 4 * np.log(N)
    tf = tb = 0.0
    for s in range(6):
        A, y, xs = make_instance(N, N, rho, s)
        w = y - A @ xs; W = float(w @ w); B = A * xs
        t0 = time.perf_counter(); fp_count(A, y, W); t1 = time.perf_counter()
        box_static(B, w, W); t2 = time.perf_counter()
        tf += t1 - t0; tb += t2 - t1
    print("N=%d: total over 6 seeds  FP %.2f s  box static %.2f s" % (N, tf, tb))
