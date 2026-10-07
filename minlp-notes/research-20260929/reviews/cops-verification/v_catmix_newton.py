"""High-precision active-set Newton polish of the catmix primal (falsification test for the dual
bound): J(u) and its adjoint gradient in mpmath (40 digits); Hessian on the free controls by
central differences of the gradient; Newton steps with backtracking, keeping u in [0,1].
The final controls are rounded to doubles and evaluated exactly (Fractions)."""
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

import v_catmix_model as vm

# research-20260929/ of this checkout (this file is in research-20260929/reviews/<dir>/)
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

mp.mp.dps = 40
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
src = sys.argv[2] if len(sys.argv) > 2 else \
    os.path.join(R29, "open-instances-wave2/cops/logs/catmix%d_u.npy") % N
m, K, strs = vm.load(N)
a, b, c, ep, em = (mp.mpf(strs[k]) for k in ("a", "b", "c", "ep", "em"))


def P(v):
    return mp.matrix([[1 + a * v, -b * v], [-a * v, ep + c * v]])


def Q(v):
    return mp.matrix([[1 - a * v, b * v], [a * v, em - c * v]])


dP = mp.matrix([[a, -b], [-a, c]])


def J_grad(u):
    xs = [mp.matrix([[1], [0]])]
    for i in range(N):
        xs.append(mp.lu_solve(P(u[i + 1]), Q(u[i]) * xs[-1]))
    J = xs[-1][0] + xs[-1][1] - 1
    g = [mp.mpf(0)] * (N + 1)
    lam = mp.matrix([[1], [1]])
    for i in range(N - 1, -1, -1):
        mu = mp.lu_solve(P(u[i + 1]).T, lam)
        g[i + 1] += -(mu.T * (dP * xs[i + 1]))[0]
        g[i] += -(mu.T * (dP * xs[i]))[0]
        lam = Q(u[i]).T * mu
    return J, g


u = [mp.mpf(float(v)) for v in np.load(src)]
J, g = J_grad(u)
# gradient check at a generic point
ut = [mp.mpf(0.3 + 0.4 * ((7 * k) % 11) / 11) for k in range(N + 1)]
Jt, gt = J_grad(ut)
e = mp.mpf("1e-15")
k = 37
up_ = list(ut); up_[k] += e
dn_ = list(ut); dn_[k] -= e
print("gradient check (generic point):", mp.nstr(gt[k], 12), mp.nstr((J_grad(up_)[0] - J_grad(dn_)[0]) / (2 * e), 12))
print("start J =", mp.nstr(J, 20))
for it in range(12):
    free = [k for k in range(N + 1) if mp.mpf("1e-12") < u[k] < 1 - mp.mpf("1e-12")]
    # KKT sign check on bounds
    at0 = [float(g[k]) for k in range(N + 1) if u[k] <= mp.mpf("1e-12")]
    at1 = [float(g[k]) for k in range(N + 1) if u[k] >= 1 - mp.mpf("1e-12")]
    gf = mp.matrix([g[k] for k in free])
    print(" it %d  J=%s  free=%d  max|g_free|=%.3g  min g at 0=%.3g  max g at 1=%.3g" % (
        it, mp.nstr(J, 22), len(free), float(max(abs(v) for v in gf)), min(at0) if at0 else 0, max(at1) if at1 else 0),
        flush=True)
    H = mp.matrix(len(free), len(free))
    hstep = mp.mpf("1e-12")
    for jj, k in enumerate(free):
        u1 = list(u); u1[k] += hstep
        u2 = list(u); u2[k] -= hstep
        g1, g2 = J_grad(u1)[1], J_grad(u2)[1]
        for ii, kk in enumerate(free):
            H[ii, jj] = (g1[kk] - g2[kk]) / (2 * hstep)
    H = (H + H.T) / 2
    ev = mp.eigsy(H)[0]
    print("   Hessian eigenvalues (free): min %.3g max %.3g" % (float(min(ev)), float(max(ev))), flush=True)
    step = mp.lu_solve(H, -gf)
    t = mp.mpf(1)
    improved = False
    for _ in range(40):
        un = list(u)
        for ii, k in enumerate(free):
            un[k] = min(max(u[k] + t * step[ii], mp.mpf(0)), mp.mpf(1))
        Jn, gn = J_grad(un)
        if Jn < J:
            u, J, g = un, Jn, gn
            improved = True
            break
        t /= 2
    if not improved:
        print("   no decrease along the Newton direction", flush=True)
        break
ud = np.array([float(v) for v in u])
ud = np.clip(ud, 0, 1)
xs = vm.simulate_exact(K, [Fr(v) for v in ud])
Jx = xs[-1][0] + xs[-1][1] - 1
print("final double controls: exact J = %.20g" % float(Jx))
np.save("logs/catmix%d_u_newton.npy" % N, ud)
