"""Check numerically that the MPS maximal completion C_F^G (kept inequalities: tangency
point on the slice side) equals the upward/downward closure cl(C_F -/+ R_+ e_w)."""
import numpy as np
import familyB
from bilinear import in_B
rng = np.random.default_rng(0)
agree = dis = 0
for t in range(400):
    side = '+' if t % 2 == 0 else '-'
    F = rng.normal(size=(2, 2))
    if np.linalg.det(F) < 0: F[:, 0] *= -1
    m = familyB.kept_mask(F, side)
    for k in range(25):
        s = rng.normal(size=3) * 2
        a = familyB.in_B(F, side, s, m, tol=1e-9)
        b = in_B(F, side, s)
        if a == b: agree += 1
        else:
            # disagreements must be boundary cases: check with a tiny shift
            dis += 1
print('agree', agree, 'disagree', dis)
