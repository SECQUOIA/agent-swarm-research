import numpy as np
from core import bilinear_quadratic, corner_bound
from bilinear import kappa_pencil, kappa_set_A
F_ = lambda *a: np.array(a, float)
inst = {1846: (F_(1.5, 1, 3), F_(4, -2, -5), F_(1, 7, 19), F_(6, -1, 5), F_(3, 1, 3), F_(1, -3, -8)),
        2464: (F_(2.5, -2.5, -2), F_(2, -4, -5), F_(-2, 8, 11), F_(-.5, -1.5, 1.5), F_(1, -1, -1), F_(1, -3, -4)),
        2947: (F_(4, .5, 4.5), F_(9, 0, 12), F_(0, 3, 3), F_(1, 4, 9), F_(3, 2, 6), F_(3, -1, 3)),
        5184: (F_(-1.5, 3, -1), F_(2, 1, 5), F_(-7, 4, -16), F_(-2, 4, -5), F_(-1, 2, -2), F_(3, -1, 7)),
        5637: (F_(.5, 4, 3), F_(4, 2, 11), F_(-8, 6, -21), F_(-1.5, 0, 2), F_(1, 3, 3), F_(3, -1, 8)),
        8459: (F_(-4.5, 0, 1.5), F_(-1, -6, 18), F_(-5, 6, -18), F_(0, 2.5, 2.5), F_(-3, 0, 0), F_(1, -3, 9))}
Q, b, c = bilinear_quadratic('+')
for k, (sb, v1, v2, v3, t0, d) in inst.items():
    P = np.stack([v1 - sb, v2 - sb, v3 - sb], 1)
    zk, lam = corner_bound(Q, b, c, sb, P, np.ones(3), return_point=True)
    G0, G1 = kappa_pencil('+', t0, d)
    ivs = [kappa_set_A(G0, G1, '+', v) for v in (sb, v1, v2, v3)]
    print(k, 'zK', zk, 'lam', lam.round(6), 'kappa sets (sbar,v1,v2,v3):', [None if iv is None else (round(iv[0], 5), round(iv[1], 5)) for iv in ivs])
