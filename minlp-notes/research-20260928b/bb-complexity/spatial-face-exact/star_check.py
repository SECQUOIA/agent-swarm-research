"""Theorem 4.5 (star forests), tight 3D cases.  Center x, leaves y, z:
f = L+ (x-a)_+ + L- (a-x)_+ + (x-a)(c1 y + c2 z) on [0,1]^3, with the smallest L+- that keep
f >= 0:  L+ = max(0,-c1) + max(0,-c2),  L- = max(0,c1) + max(0,c2).  Optimal face {x = a}.
The transverse rates vanish at box corners, so the certificate {x<=a},{x>=a} has no slack.
Check: exact node bound (HiGHS LP) of both boxes >= -1e-9 for random (a, c1, c2).
Also a 4D double star (centers x1, x2 with leaves y1, y2), orthant certificate with 4 boxes."""
import itertools
import numpy as np
from face_bb import Problem, relax

rng = np.random.default_rng(7)
worst = np.inf
for _ in range(200):
    a = rng.uniform(0.1, 0.9); c1, c2 = rng.normal(size=2)
    Lp = max(0, -c1) + max(0, -c2); Lm = max(0, c1) + max(0, c2)
    # (x-a)_+ and (a-x)_+ with different slopes: Lp (x-a)_+ + Lm (a-x)_+ = ((Lp+Lm)/2)|x-a| + ((Lp-Lm)/2)(x-a)
    P = Problem("star3", [0, 0, 0], [1, 1, 1], c=[(Lp - Lm) / 2, -c1 * a, -c2 * a],
                terms=[(0, 1, c1), (0, 2, c2)], absterms=[([1, 0, 0], a, (Lp + Lm) / 2)],
                const=-(Lp - Lm) / 2 * a)
    for (lx, ux) in ((0.0, a), (a, 1.0)):
        worst = min(worst, relax(P, np.array([lx, 0, 0.]), np.array([ux, 1, 1.]))[0])
print(f"3D star, 200 random tight instances: min node bound over the 2 certificate boxes = {worst:.2e}")

worst = np.inf
for _ in range(100):
    a1, a2 = rng.uniform(0.1, 0.9, 2); c = rng.normal(size=2)
    # centers x1 (idx0), x2 (idx1); leaves y1 (idx2) of x1, y2 (idx3) of x2
    L1p, L1m = max(0, -c[0]), max(0, c[0]); L2p, L2m = max(0, -c[1]), max(0, c[1])
    P = Problem("star4", [0] * 4, [1] * 4,
                c=[(L1p - L1m) / 2, (L2p - L2m) / 2, -c[0] * a1, -c[1] * a2],
                terms=[(0, 2, c[0]), (1, 3, c[1])],
                absterms=[([1, 0, 0, 0], a1, (L1p + L1m) / 2), ([0, 1, 0, 0], a2, (L2p + L2m) / 2)],
                const=-(L1p - L1m) / 2 * a1 - (L2p - L2m) / 2 * a2)
    for s1, s2 in itertools.product((0, 1), repeat=2):
        l = np.array([a1 if s1 else 0, a2 if s2 else 0, 0, 0.]); u = np.array([1 if s1 else a1, 1 if s2 else a2, 1, 1.])
        worst = min(worst, relax(P, l, u)[0])
print(f"4D double star, 100 random tight instances: min node bound over the 4 orthant boxes = {worst:.2e}")
# control: without the face split the root is not valid
P = Problem("star3", [0, 0, 0], [1, 1, 1], c=[0, -0.5, 0.5], terms=[(0, 1, 1.0), (0, 2, -1.0)],
            absterms=[([1, 0, 0], 0.5, 1.0)], const=0.0)
print(f"control (a=0.5, c1=1, c2=-1): root node bound = {relax(P, np.zeros(3), np.ones(3))[0]:.4f} (< 0: root not valid)")
