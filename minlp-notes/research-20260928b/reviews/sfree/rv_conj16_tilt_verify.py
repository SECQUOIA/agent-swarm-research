"""Exact z_K / uniqueness and two-method z_A for tilted instance 13 (eps = 1e-3, 1e-2)."""
import json, numpy as np, sympy as sp, warnings
warnings.filterwarnings('ignore')
from scipy.optimize import minimize
import cvxpy as cp
import rv_orbit_numeric as on
from rv_thm14_exact import face_min
R = lambda x: sp.Rational(x).limit_denominator(10**6)
d = [json.loads(l) for l in open('rv_conj16_instances.jsonl') if json.loads(l)['n'] == 13][0]
sb0 = np.array(d['sbar']); V0 = [np.array(v) for v in d['V']]
t0 = V0[0]; dv = V0[1] - t0; gq = np.array([-t0[1], -t0[0], 1.0])
q = lambda s: s[2] - s[0] * s[1]
for eps in (1e-3, 1e-2):
    x0, y0 = R(t0[0]), R(t0[1]); t = sp.Matrix([x0, y0, x0 * y0])
    v2 = t0 + dv + eps * np.linalg.norm(dv) * gq / np.linalg.norm(gq)
    sbq = sp.Matrix([R(z) for z in sb0 - t0]) + t
    Vq = [t, sp.Matrix([R(z) for z in v2 - t0]) + t, sp.Matrix([R(z) for z in V0[2] - t0]) + t]
    P = sp.Matrix.hstack(*[v - sbq for v in Vq]); lam = sp.symbols('l1:4', real=True)
    g = sp.expand(q(sbq + P * sp.Matrix(lam)))
    cands, sing = face_min(g, lam)
    gmin = min(c[0] for c in cands); arg = {tuple(c[1][x] for x in lam) for c in cands if c[0] == gmin}
    gradt = sp.Matrix([-t[1], -t[0], 1])
    print('eps=%g (rationalized): q(t*) = %s, grad.(v2-t*) = %.3e > 0, grad.(v3-t*) = %.3e, grad.(sbar-t*) = %.3e; min_T* q = %s at %s'
          % (eps, q(t), float(gradt.dot(Vq[1] - t)), float(gradt.dot(Vq[2] - t)), float(gradt.dot(sbq - t)), gmin, arg))
    sbar = np.array([float(z) for z in sbq]); Vf = [np.array([float(z) for z in v]) for v in Vq]; Pl = [v - sbar for v in Vf]
    res = {}
    for solver in ('CLARABEL', 'SCS'):
        lo, hi, Fb = 0.0, 1.0, None
        for _ in range(28):
            mid = (lo + hi) / 2
            F = cp.Variable((2, 2))
            cons = [on.sym(F.T @ on.M(sbar)) >> np.eye(2)] + [on.sym(F.T @ on.M(sbar + mid * p)) >> 0 for p in Pl]
            pr = cp.Problem(cp.Minimize(cp.norm(F, 'fro')), cons)
            try:
                pr.solve(solver=solver, **({'eps': 1e-9, 'max_iters': 200000} if solver == 'SCS' else {}))
                okk = pr.status == 'optimal'
            except Exception:
                okk = False
            if okk:
                lo, Fb = mid, F.value
            else:
                hi = mid
        res[solver] = (lo, hi, on.exactA(Fb, sbar, Pl)[0], Fb)
    Fc = res['CLARABEL'][3]
    def ex(x):
        F = x.reshape(2, 2)
        if np.linalg.det(F) <= 0 or on.lmin(on.sym(F.T @ on.M(sbar))) <= 0:
            return 0.0
        try:
            return on.exactA(F, sbar, Pl)[0]
        except np.linalg.LinAlgError:
            return 0.0
    rng = np.random.default_rng(1); best = ex(Fc.ravel())
    for x0_ in [Fc.ravel()] + [rng.standard_normal(4) for _ in range(150)]:
        r = minimize(lambda x: -ex(x), x0_, method='Nelder-Mead', options=dict(maxiter=3000, xatol=1e-12, fatol=1e-13))
        best = max(best, -r.fun)
    print('   z_A: Clarabel [%.6f, %.6f] exact %.6f ; SCS [%.6f, %.6f] exact %.6f ; direct search %.6f'
          % (res['CLARABEL'][0], res['CLARABEL'][1], res['CLARABEL'][2], res['SCS'][0], res['SCS'][1], res['SCS'][2], best), flush=True)
