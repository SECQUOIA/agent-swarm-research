"""Solver cross-checks for the node bounds used in Section 8.
1. HiGHS QP versus the Clarabel fallback on random boxes (tilt, diag, iso).
2. HiGHS QP versus the exact closed-form tilt bound (instances.tilt_exact).
(The closed-form kink bound versus the HiGHS LP is checked in oblivious.py.)"""
import numpy as np
import face_bb as F
import instances as I

rng = np.random.default_rng(0)
worst = 0.0
for P in (I.tilt(0.3), I.diag(), I.iso()):
    for _ in range(40):
        l = rng.uniform(0, 0.8, 2); u = l + rng.uniform(0.001, 0.2, 2)
        a = F.relax(P, l, u)[0]
        orig = F._solve; F._solve = lambda *args, **kw: None
        b = F.relax(P, l, u)[0]
        F._solve = orig
        worst = max(worst, abs(a - b))
print(f"[1] max |HiGHS - Clarabel| over 120 random QP boxes: {worst:.2e}")
rng = np.random.default_rng(3)
worst = 0.0
for th in (0.3, 0.03, 0.003):
    Pq, Px = I.tilt(th), I.tilt_exact(th)
    for _ in range(150):
        l = rng.uniform(0, 0.9, 2); u = np.minimum(l + rng.uniform(1e-4, 0.3, 2), 1)
        worst = max(worst, abs(F.relax(Pq, l, u)[0] - Px.custom_relax(l, u)[0]))
print(f"[2] max |HiGHS QP - exact tilt bound| over 450 random boxes: {worst:.2e}")
