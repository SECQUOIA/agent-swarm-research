"""(1) compose the reviewer's interval stage maps along the authors' controls and compare with the
exact rational objective; (2) try to improve the authors' primal with an own adjoint L-BFGS-B /
active-set Newton polish (float), then evaluate the new controls exactly (Fractions)."""
import os
import sys
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import minimize

import v_catmix_dp as D
import v_catmix_model as vm

# research-20260929/ of this checkout (this file is in research-20260929/reviews/<dir>/)
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
base = os.path.join(R29, "open-instances-wave2/cops/logs/")
maps = D.Maps(N)
u0 = np.load(base + "catmix%d_u.npy" % N)


def compose(u):
    one = np.array([1.0])
    pv = lambda cs, uu: [(np.array([c[0]]), np.array([c[1]])) for c in cs]
    U = lambda uu: (np.array([uu]), np.array([uu]))

    def ev(cs, uu):  # interval poly at point
        r = cs[2]
        for c in (cs[1], cs[0]):
            r = D.iadd(D.imul(r, U(uu)), c)
        return r
    S = maps.init
    y1 = ev(pv(S["N11"], 0), u[0])
    y2 = ev(pv(S["N21"], 0), u[0])
    S = maps.stage
    for i in range(1, N):
        Dv = ev(pv(S["D"], 0), u[i])
        n1 = D.iadd(D.imul(ev(pv(S["N11"], 0), u[i]), y1), D.imul(ev(pv(S["N12"], 0), u[i]), y2))
        n2 = D.iadd(D.imul(ev(pv(S["N21"], 0), u[i]), y1), D.imul(ev(pv(S["N22"], 0), u[i]), y2))
        y1 = (D.dn(n1[0] / Dv[1]), D.up(n1[1] / Dv[0]))
        y2 = (D.dn(n2[0] / Dv[1]), D.up(n2[1] / Dv[0]))
        assert y1[0] >= 0 and y2[0] >= -1e-300
    S = maps.term
    Dv = ev(pv(S["D"], 0), u[N])
    t = D.iadd(D.imul(ev(pv(S["T1"], 0), u[N]), y1), D.imul(ev(pv(S["T2"], 0), u[N]), y2))
    return float(D.dn(D.dn(t[0] / Dv[1]) - 1)[0]), float(D.up(D.up(t[1] / Dv[0]) - 1)[0])


K = maps.K
Jex = lambda u: (lambda xs: xs[-1][0] + xs[-1][1] - 1)(vm.simulate_exact(K, [Fr(float(v)) for v in u]))
print("compose(authors' controls) =", compose(u0), " exact J =", float(Jex(u0)))

a, b, c, ep, em = (float(K[k]) for k in ("a", "b", "c", "ep", "em"))


def J_grad(u):
    """float objective and adjoint gradient (own derivation): x_{i+1} = P_{i+1}^{-1} Q_i x_i."""
    P = lambda v: np.array([[1 + a * v, -b * v], [-a * v, ep + c * v]])
    Q = lambda v: np.array([[1 - a * v, b * v], [a * v, em - c * v]])
    dP = np.array([[a, -b], [-a, c]])
    xs = [np.array([1.0, 0.0])]
    for i in range(N):
        xs.append(np.linalg.solve(P(u[i + 1]), Q(u[i]) @ xs[-1]))
    J = xs[-1].sum() - 1
    g = np.zeros(N + 1)
    lam = np.array([1.0, 1.0])          # dJ/dx_N
    for i in range(N - 1, -1, -1):
        # x_{i+1} = P^{-1} Q x_i ; mu = P^{-T} lam
        mu = np.linalg.solve(P(u[i + 1]).T, lam)
        g[i + 1] += -mu @ (dP @ xs[i + 1])
        g[i] += mu @ (-dP @ xs[i])       # dQ/du = -dP
        lam = Q(u[i]).T @ mu
    return J, g


J0, g0 = J_grad(u0)
eps = 1e-7
k = 40
e = np.zeros(N + 1); e[k] = eps
fd = (J_grad(np.clip(u0 + e, 0, 1))[0] - J_grad(np.clip(u0 - e, 0, 1))[0]) / (2 * eps)
print("float J(authors) =", J0, " grad check at k=40:", g0[k], fd)
best_u, best_J = u0.copy(), Jex(u0)
res = minimize(J_grad, u0, jac=True, method="L-BFGS-B", bounds=[(0, 1)] * (N + 1),
               options=dict(maxiter=50000, maxfun=100000, ftol=0, gtol=1e-16, maxcor=100))
u1 = np.clip(res.x, 0, 1)
J1 = Jex(u1)
print("L-BFGS-B from authors' point:", res.message, res.nit, " exact J =", repr(float(J1)),
      " improvement =", float(best_J - J1))
if J1 < best_J:
    best_u, best_J = u1, J1
np.save("logs/catmix%d_u_reviewer.npy" % N, best_u)
print("best exact J (reviewer) = %.20g" % float(best_J))
