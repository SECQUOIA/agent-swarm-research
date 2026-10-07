"""Reviewer's check of E2 with k1 = +1/2 (b^T w = -1/2), Section 4.3.
Compare: (i) the smooth KKT point (active set of the k1 = 0 optimum: u = -1
then free), (ii) the best local minimizer from multistart (chattering), and
J* = -0.1010308741.  Tests whether '0.43h below J*' is explained by the
prediction (1/4) h int(1 - u_s^2) (which is a chatter-vs-smooth quantity)."""
import numpy as np
from scipy.optimize import minimize
import importlib.util, sys
spec = importlib.util.spec_from_file_location('v4', 'v4_e2_discrete.py'); v4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v4)
Jstar = -0.1010308741
for N in (50, 100, 200, 400):
    h = 3.0/N
    H0, g0 = v4.float_qp(0.0, N)
    u0 = v4.solve_float(H0, g0, [np.zeros(N)])
    st0 = np.where(u0 < -1 + 1e-7, -1, np.where(u0 > 1 - 1e-7, 1, 0))
    Hp, gp = v4.float_qp(0.5, N)
    # smooth KKT for k1 = +1/2 with the k1 = 0 active set
    free = np.where(st0 == 0)[0]; fix = np.where(st0 != 0)[0]
    us = st0.astype(float).copy()
    us[free] = np.linalg.solve(Hp[np.ix_(free, free)], -(gp[free] + Hp[np.ix_(free, fix)] @ us[fix]))
    grs = Hp @ us + gp
    feas = np.all(np.abs(us) <= 1)
    Jfun = lambda v: 0.5*v@Hp@v + gp@v
    c0 = None
    # constant term: evaluate exactly via simulation cost for the zero control
    from fractions import Fraction as Fr
    hh, k, F, Fx = v4.build(Fr(1, 2), N)
    c0 = float(v4.cost(hh, k, F, Fx, [Fr(0)]*N))
    Js = Jfun(us) + c0
    # chattering: multistart
    rng = np.random.default_rng(1)
    starts = [us, np.where(np.arange(N) % 2 == 0, 1.0, -1.0)] + [rng.uniform(-1, 1, N) for _ in range(12)]
    uc = v4.solve_float(Hp, gp, starts)
    Jc = Jfun(uc) + c0
    ev = np.linalg.eigvalsh(Hp)
    H00 = np.linalg.eigvalsh(H0)[0]
    J0 = 0.5*u0@H0@u0 + g0@u0 + float(v4.cost(*v4.build(Fr(0), N)[:1], *v4.build(Fr(0), N)[1:], [Fr(0)]*N))
    print('N=%d h=%.4f smooth KKT feasible=%s (max|grad free|=%.1e): (J_smooth-J*)/h=%+.3f  (J_chat-J*)/h=%+.3f  '
          '(J_chat-J_smooth)/h=%+.3f  #neg eig=%d min eig=%.2e (h^2 b.w=%.2e); k1=0: (J_E-J*(0))/h=%+.3f'
          % (N, h, feas, np.max(np.abs(grs[free])), (Js - Jstar)/h, (Jc - Jstar)/h, (Jc - Js)/h,
             int(np.sum(ev < 0)), ev[0], -0.5*h*h, (J0 - 0.1489691259)/h), flush=True)
