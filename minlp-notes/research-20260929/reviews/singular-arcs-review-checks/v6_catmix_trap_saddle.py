"""Reviewer's independent check of the COPS catmix saddle (Section 5.5),
in the ORIGINAL 2-D trapezoidal form P(u_{i+1}) x_{i+1} = Q(u_i) x_i
(P = I - h/2 A(u), Q = I + h/2 A(u), A(u) = [[-u, 10u], [u, -1-9u]]),
J = x1_N + x2_N - 1, in mpmath (40 digits).  Does not use the author's
reduced model.

1. J of the stored COPS controls and of the author's saved smooth point.
2. Gradient on the free stages of the smooth point (central differences).
3. Hessian on the free stages; eigenvalues; sign pattern of the lowest
   eigenvector.
4. Rayleigh quotients of a tapered alternating direction (compare with the
   symbol f(pi)(J+1)) and of a smooth direction.
(The reduced Hessian is dense, so band sums do not estimate the symbol.)
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys
import numpy as np
import mpmath as mp
mp.mp.dps = 40
ROOT = (_PUBLIC_REPO + '/research-20260929/')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
h = mp.mpf(1)/N

def J(u):
    x1, x2 = mp.mpf(1), mp.mpf(0)
    a = h/2
    for i in range(N):
        ui, uj = u[i], u[i+1]
        # Q(u_i) x_i
        r1 = (1 - a*ui)*x1 + 10*a*ui*x2
        r2 = a*ui*x1 + (1 - a*(1 + 9*ui))*x2
        # solve P(u_{i+1}) x = r
        p11, p12, p21, p22 = 1 + a*uj, -10*a*uj, -a*uj, 1 + a*(1 + 9*uj)
        det = p11*p22 - p12*p21
        x1, x2 = (p22*r1 - p12*r2)/det, (-p21*r1 + p11*r2)/det
    return x1 + x2 - 1

uc = [mp.mpf(float(v)) for v in np.load(ROOT + 'open-instances-wave2/cops/logs/catmix%d_u.npy' % N)]
us = [mp.mpf(float(v)) for v in np.load(ROOT + 'theory-bangbang/singular/logs/catmix%d_smooth_u.npy' % N)]
Jc, Js = J(uc), J(us)
print('N=%d J(COPS stored) = %s' % (N, mp.nstr(Jc, 16)))
print('J(smooth saved)    = %s   J_smooth - J_chatter = %s' % (mp.nstr(Js, 16), mp.nstr(Js - Jc, 6)))
usf = np.array([float(v) for v in us])
free = [i for i in range(N + 1) if 1e-9 < usf[i] < 1 - 1e-9]
print('free stages: %d (%d..%d), u range [%.4f, %.4f]' % (len(free), free[0], free[-1], usf[free].min(), usf[free].max()))
e = mp.mpf(10)**-10
def shifted(u, pairs):
    v = list(u)
    for i, d in pairs:
        v[i] += d
    return v
g = [(J(shifted(us, [(i, e)])) - J(shifted(us, [(i, -e)])))/(2*e) for i in free]
print('max |grad| on free stages = %s' % mp.nstr(max(abs(x) for x in g), 3))
bnd = [i for i in range(N + 1) if i not in free]
gb = [(J(shifted(us, [(i, e)])) - J(shifted(us, [(i, -e)])))/(2*e) for i in bnd]
sgn_ok = all((usf[i] <= 1e-9 and gv >= 0) or (usf[i] >= 1 - 1e-9 and gv <= 0) for i, gv in zip(bnd, gb))
print('KKT sign conditions at bound stages hold: %s' % sgn_ok)
# Hessian on free stages
n = len(free)
E = mp.mpf(10)**-8
H = np.zeros((n, n))
J0 = Js
for a_ in range(n):
    i = free[a_]
    Jp = J(shifted(us, [(i, E)])); Jm = J(shifted(us, [(i, -E)]))
    H[a_, a_] = float((Jp - 2*J0 + Jm)/E**2)
    for b_ in range(a_ + 1, n):
        j = free[b_]
        v = (J(shifted(us, [(i, E), (j, E)])) - J(shifted(us, [(i, E), (j, -E)]))
             - J(shifted(us, [(i, -E), (j, E)])) + J(shifted(us, [(i, -E), (j, -E)])))/(4*E**2)
        H[a_, b_] = H[b_, a_] = float(v)
ev, V = np.linalg.eigh(H)
v0 = V[:, 0]
alt = np.mean(np.sign(v0[1:]) != np.sign(v0[:-1]))
print('Hessian (J units): #neg eig = %d, most negative = %.3e, next = %s' % (int(np.sum(ev < 0)), ev[0], np.array2string(ev[1:5], precision=3)))
print('lowest eigenvector: fraction of sign changes = %.3f' % alt)
# Rayleigh quotient of a tapered alternating direction on the free block
wv = np.array([(-1)**k*np.sin(np.pi*(k + 0.5)/n)**2 for k in range(n)])
print('Rayleigh quotient, tapered alternating direction: %.3e' % (wv@H@wv/(wv@wv)))
sm = np.array([np.sin(np.pi*(k + 0.5)/n) for k in range(n)])
print('Rayleigh quotient, smooth sine direction: %.3e' % (sm@H@sm/(sm@sm)))
