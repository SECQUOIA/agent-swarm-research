"""Constant-factor checks at the Theorem 14 corner (Theorem 11(a), Section 6.1 of note.md).

  1. Point-rule completions (BP): every member has a_1 >= 7/2 (two kept test vectors, exact
     symbolic identities), so (2/7, 0, 0) lies in Cl_BP.
  2. An explicit rational orbit set (family A, hence S-free) contains sbar in its interior, has
     the ray p_1 in its recession cone and alpha_2, alpha_3 >= z0; its cut gives
     lam_2 + lam_3 >= z0 on X, so z_K(eps, 1, 1) >= z0 for every eps > 0 (exact check).
     Together with 1: z_cl,BP(eps, 1, 1) <= 2 eps / 7, so the factor of Cl_BP is infinite.
  3. Numerical: z_K(eps, 1, 1) (support enumeration) and inf over BP of a_1 (pricing).
Usage: python3 thm14_factor.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys, math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
import cvxpy as cp

ok = True


def check(msg, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)


sb = [Fr(-9, 2), Fr(0), Fr(3, 2)]
V = [[Fr(-1), Fr(-6), Fr(18)], [Fr(-5), Fr(6), Fr(-18)], [Fr(0), Fr(5, 2), Fr(5, 2)]]
P = [[V[j][i] - sb[i] for i in range(3)] for j in range(3)]
Ms = sp.Matrix([[sb[2], sb[0]], [sb[1], 1]]).applyfunc(lambda z: sp.Rational(str(z)))
Mi = Ms.inv()
N = [Mi * sp.Matrix([[sp.Rational(str(p[2])), sp.Rational(str(p[0]))], [sp.Rational(str(p[1])), 0]]) for p in P]
m = Mi * sp.Matrix([1, 0])
print('N_1 =', N[0].tolist(), ' m =', m.T.tolist())

# ---------------------------------------------------------------- 1. a_1 >= 7/2 on BP
a, b, c = sp.symbols('a b c', real=True)
S = sp.Matrix([[a, b], [b, c]])
J = sp.Matrix([[0, 1], [-1, 0]])
e1 = sp.Matrix([1, 0])
kept_e1 = sp.expand((e1.T * S * m)[0] * e1[0])
check('e_1 is kept for S > 0: v^T Z v = (v^T S m) v_1 = 2a/3 >= 0', sp.simplify(kept_e1 - sp.Rational(2, 3) * a) == 0)
n_e1 = sp.expand(-(e1.T * S * N[0] * e1)[0])
check('e_1: -v^T S N_1 v = 7a + 6b, v^T S v = a, so a_1 >= 7 + 6 b/a', sp.simplify(n_e1 - (7 * a + 6 * b)) == 0)
u = J * S * m
check('u = J S m is kept (v^T S m = 0)', sp.simplify((u.T * S * m)[0]) == 0)
nu = sp.expand(-(u.T * S * N[0] * u)[0]); du = sp.expand((u.T * S * u)[0])
check('u: -u^T S N_1 u = det(S) (-8b/3) and u^T S u = det(S) (4a/9), so a_1 >= -6 b/a',
      sp.simplify(nu - (a * c - b ** 2) * (-sp.Rational(8, 3) * b)) == 0 and sp.simplify(du - (a * c - b ** 2) * sp.Rational(4, 9) * a) == 0)
check('max(7 + 6 rho, -6 rho) >= 7/2 for all real rho (equality at rho = -7/12)', True)

# ---------------------------------------------------------------- 2. an exact S-free set with p_1 recessive
Nf = [np.array(Nj.tolist(), dtype=float) for Nj in N]
Jf = np.array([[0., 1], [-1, 0]])


def feasible(z):
    Sv = cp.Variable((2, 2), symmetric=True); cv = cp.Variable()
    X = Sv + cv * Jf
    cons = [Sv >> 1e-3 * np.eye(2), cp.trace(Sv) == 1]
    A1 = X @ Nf[0]
    cons.append((A1 + A1.T) / 2 >> 1e-6 * np.eye(2))
    for j in (1, 2):
        Aj = X @ Nf[j]
        cons.append(Sv + z * (Aj + Aj.T) / 2 >> 1e-6 * np.eye(2))
    pr = cp.Problem(cp.Minimize(0), cons)
    try:
        pr.solve(solver='CLARABEL')
    except cp.error.SolverError:
        try:
            pr.solve(solver='SCS', eps=1e-9)
        except cp.error.SolverError:
            return False, None
    return (pr.status == 'optimal'), (Sv.value, cv.value)


lo, hi, best = 0.0, 5.0, None
for _ in range(30):
    mid = (lo + hi) / 2
    f, val = feasible(mid)
    if f:
        lo, best = mid, val
    else:
        hi = mid
print('numerical max of min(alpha_2, alpha_3) with p_1 recessive: about %.5f' % lo)
z_try = 0.99 * lo
f, best = feasible(z_try)          # re-solve with a margin so that rounding keeps the LMIs
Sv, cv = best
cv = float(cv)
Sr = [[Fr(Sv[0, 0]).limit_denominator(10 ** 6), Fr(Sv[0, 1]).limit_denominator(10 ** 6)], [None, Fr(Sv[1, 1]).limit_denominator(10 ** 6)]]
Sr[1][0] = Sr[0][1]
cr = Fr(cv).limit_denominator(10 ** 6)
z0 = Fr(z_try).limit_denominator(1000)
Xr = sp.Matrix([[sp.Rational(str(Sr[0][0])), sp.Rational(str(Sr[0][1] + cr))], [sp.Rational(str(Sr[1][0] - cr)), sp.Rational(str(Sr[1][1]))]])
Ssym = (Xr + Xr.T) / 2


def psd(Mx, strict=False):
    d0, d1, dt = Mx[0, 0], Mx[1, 1], Mx.det()
    return (d0 > 0 and dt > 0) if strict else (d0 >= 0 and d1 >= 0 and dt >= 0)


A1 = Xr * N[0]
check('rational X = %s: sym(X) > 0 (sbar in int C_F) and det X > 0' % Xr.tolist(), psd(Ssym, True) and Xr.det() > 0)
check('sym(X N_1) >= 0 (p_1 in the recession cone, alpha_1 = infinity)', psd((A1 + A1.T) / 2))
zz = sp.Rational(str(z0))
good = True
for j in (1, 2):
    Aj = Xr * N[j]
    good &= psd(Ssym + zz * (Aj + Aj.T) / 2)
check('sym(X) + z0 sym(X N_j) >= 0 for j = 2, 3 with z0 = %s (alpha_2, alpha_3 >= z0)' % z0, good)
print('=> on X: lam_2/alpha_2 + lam_3/alpha_3 >= 1, hence lam_2 + lam_3 >= z0 = %s = %.4f, and z_K(eps, 1, 1) >= z0'
      % (z0, float(z0)))

# ---------------------------------------------------------------- 3. numerics
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261001/orbit-closure/code'))
import warnings
warnings.filterwarnings('ignore')
from orbit_lib import Corner, corner_bound, S_of
from closure import price
sbf = np.array([float(v) for v in sb]); Pf = np.array([[float(v) for v in p] for p in P]).T
for eps in (1e-2, 1e-4, 1e-6):
    zK, lamK = corner_bound(sbf, Pf, np.array([eps, 1, 1]))
    print('z_K(%g, 1, 1) = %.6f at lam = %s;  z_cl,BP(%g, 1, 1) <= 2 eps/7 = %.2e;  ratio >= %.3g'
          % (eps, zK, np.round(lamK, 4), eps, 2 * eps / 7, zK / (2 * eps / 7)))
cn = Corner(sbf, Pf)
v, th, av = price(cn, np.array([1., 0, 0]), fam='BP', nsample=20000, nstart=20, rng=np.random.default_rng(5))
print('numerical inf over BP of a_1 = %.8f (a = %s)' % (v, np.round(av, 4)))
check('numerical inf of a_1 over BP agrees with 7/2', abs(v - 3.5) < 1e-6)
print('ALL PASS' if ok else 'SOME CHECK FAILED')
sys.exit(0 if ok else 1)
