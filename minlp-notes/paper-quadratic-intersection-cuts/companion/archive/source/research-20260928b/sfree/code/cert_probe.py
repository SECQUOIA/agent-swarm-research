import numpy as np
from core import Mmat
from bilinear import kappa_pencil, kappa_set_A, symm, EW, in_B
F_ = lambda *a: np.array(a, float)
sb, v1, v2, v3, t0, d = F_(-4.5, 0, 1.5), F_(-1, -6, 18), F_(-5, 6, -18), F_(0, 2.5, 2.5), F_(-3, 0, 0), F_(1, -3, 9)
G0, G1 = kappa_pencil('+', t0, d)
E = Mmat('+', EW, h=0.0)
def AZ(v, k):
    FT = G0 + k * G1
    return symm(FT @ Mmat('+', v)), symm(FT @ E)      # (B): exists tau>=0 : A - tau Z >= 0 ; certificate u: u'Zu >= 0 > u'Au
ks = kappa_set_A(G0, G1, '+', sb)[0]; k3 = kappa_set_A(G0, G1, '+', v3)[1]
print('kappa_s', ks, '3-2sqrt2', 3 - 2 * np.sqrt(2), 'kappa_3', k3)
for (v, kc, side_) in [(sb, ks, 'below'), (v3, k3, 'above')]:
    A, Z = AZ(v, kc)
    ev, U = np.linalg.eigh(A); u = U[:, 0]
    print('at critical kappa: eig', ev, 'kernel u', u, "u'Zu", u @ Z @ u)
    # does this u certify on the whole half-line?
    grid = kc - np.logspace(-8, 6, 400) if side_ == 'below' else kc + np.logspace(-8, 6, 400)
    worst = []
    for k in grid:
        A, Z = AZ(v, k)
        worst.append((u @ Z @ u >= -1e-12) and (u @ A @ u < 0))
    print('   fixed-u certificate valid on sampled half-line:', all(worst))
    # slopes
    A0, Z0 = AZ(v, 0.0); A1, Z1 = AZ(v, 1.0)
    print("   u'A u affine: value at kc", u @ AZ(v, kc)[0] @ u, 'slope', u @ (A1 - A0) @ u, "; u'Zu affine: value", u @ AZ(v, kc)[1] @ u, 'slope', u @ (Z1 - Z0) @ u)
