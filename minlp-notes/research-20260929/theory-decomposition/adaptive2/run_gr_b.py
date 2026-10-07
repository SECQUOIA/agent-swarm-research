"""GR on the path family with another coupling b (adaptive-matching.md, Section 8.3).

  python3 run_gr_b.py B THETA_INV EPS     # c = 0, kappa = 0.1, n = 8, 16, 32, 64, R = 4, x0 = 0.5*ones

Reuses run_gr.run with the module constant B replaced; (QG) holds with c_g = 1 - kappa - |b|.
The logged run (logs/gr_path_b088_eps1e-3.log) used a copy of this script with the same code at
/tmp/path_b.py.
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_gr  # noqa: E402

b = float(sys.argv[1])
theta = 1.0 / float(sys.argv[2])
eps = float(sys.argv[3])
run_gr.B = b
for n in (8, 16, 32, 64):
    run_gr.run(n, np.zeros(n), eps, np.full(n, 0.5), theta, 4.0, np.zeros(n), 0.0, "zero-b%.2f" % b)
