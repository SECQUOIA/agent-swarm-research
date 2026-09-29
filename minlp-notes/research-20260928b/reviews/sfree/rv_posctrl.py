"""Positive control for rv_zk_check: S = ball {|s - c|^2 <= r^2} (Q = I, rho = 4) with its centre inside
the cone, so 3-ray corner minimizers should occur; the support<=2 scan must then exceed SCIP.
Also signature (2,1): q = s1^2 + s2^2 - (s3 - 3)^2 (a double cone around the s3-axis), sbar = 0, rays around
the axis (rho = 3), where 3-ray minimizers are possible."""
import numpy as np, rv_zk_check as zc
rng = np.random.default_rng(5)
for fam in ('ball', 'cone21'):
    n = cnt = 0
    while n < 15:
        if fam == 'ball':
            Q = np.eye(3); cen = rng.uniform(1, 3, 3); r = rng.uniform(.3, .9)
            b = -2 * cen; c = cen @ cen - r * r; sbar = np.zeros(3)
            P = np.eye(3) + 0.2 * rng.standard_normal((3, 3))
        else:
            Q = np.diag([1., 1., -1.]); b = np.array([0, 0, 6.]); c = -9.0 + 0.0; sbar = np.array([0, 0, 0.])
            # q(0) = -9 < 0 -> shift: use S = {s1^2+s2^2 - (s3-3)^2 >= ...}; instead q = -(...) : S = inside of cone
            Q, b, c = -Q, -b, -c        # q = -(s1^2+s2^2) + (s3-3)^2 ; q(0) = 9 > 0; S = {(s3-3)^2 <= s1^2+s2^2}
            P = np.array([[1, -.5, -.5], [0, .87, -.87], [1., 1., 1.]]) + 0.2 * rng.standard_normal((3, 3))
        w = rng.uniform(.5, 1.5, 3)
        if zc.qv(Q, b, c, sbar) <= 0:
            continue
        m2 = zc.my_supp2(Q, b, c, sbar, P, w); sc, lam = zc.scip(Q, b, c, sbar, P, w, m2)
        n += 1
        if m2 - sc > 1e-5 * abs(sc):
            cnt += 1
    print('%s: %d / %d instances where SCIP (all supports) beats the support<=2 value (3-ray minimizer detected)' % (fam, cnt, n))
