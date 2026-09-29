"""Verify the two apparent Conjecture-16 failures (instances 13, 14 of rv_conj16.py).
(i)  exact z_K check after rationalizing the data so the construction holds exactly
     (t* on dS, d tangent): min of q over T* = 0 only at t* = v1 (face enumeration, sympy);
(ii) orbit (A) bisection with SCS as a second solver;
(iii) direct maximization of the exact orbit bound (generalized eigenvalues, no SDP) by Nelder-Mead
     from the Clarabel optimum and 200 random starts;
(iv) best (B) bound found (reviewer's membership routine)."""
import json, sys, numpy as np, sympy as sp, warnings
warnings.filterwarnings('ignore')
from scipy.optimize import minimize
import cvxpy as cp
import rv_orbit_numeric as on
from rv_thm14_exact import face_min

R = lambda x: sp.Rational(x).limit_denominator(1000)
recs = {json.loads(l)['n']: json.loads(l) for l in open('rv_conj16_instances.jsonl')}
for n in (int(a) for a in sys.argv[1:]):
    d = recs[n]
    sb = np.array(d['sbar']); V = [np.array(v) for v in d['V']]
    # rationalize: t* = (x0, y0, x0 y0) exactly; d tangent exactly; r, p rounded
    x0, y0 = R(V[0][0]), R(V[0][1]); t = sp.Matrix([x0, y0, x0 * y0])
    dd = V[1] - V[0]; dx, dy = R(dd[0]), R(dd[1]); dvec = sp.Matrix([dx, dy, y0 * dx + x0 * dy])
    rv_ = sp.Matrix([R(z) for z in V[2] - V[0]]); pv = sp.Matrix([R(z) for z in V[0] - sb])
    sbq = t - pv; Vq = [t, t + dvec, t + rv_]
    q = lambda s: s[2] - s[0] * s[1]
    P = sp.Matrix.hstack(*[v - sbq for v in Vq])
    lam = sp.symbols('l1:4', real=True)
    g = sp.expand(q(sbq + P * sp.Matrix(lam)))
    cands, singular = face_min(g, lam)
    gmin = min(c[0] for c in cands); arg = {tuple(c[1][x] for x in lam) for c in cands if c[0] == gmin}
    print('inst %d (rationalized): q(sbar)=%s  min_T* q = %s at %s ; singular faces %s' % (n, sp.N(q(sbq), 6), gmin, arg, singular))
    sbar = np.array([float(z) for z in sbq]); Vf = [np.array([float(z) for z in v]) for v in Vq]
    Pl = [v - sbar for v in Vf]
    for solver in ('CLARABEL', 'SCS'):
        lo, hi, Fb = 0.0, 1.0, None
        for _ in range(30):
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
        cert = on.exactA(Fb, sbar, Pl)[0] if Fb is not None else 0
        print('   %s bisection: feasible %.6f / infeasible %.6f ; exact bound of returned F %.6f' % (solver, lo, hi, cert))
        if solver == 'CLARABEL':
            Fc = Fb
    def ex(x):
        F = x.reshape(2, 2)
        if np.linalg.det(F) <= 0 or on.lmin(on.sym(F.T @ on.M(sbar))) <= 0:
            return 0.0
        try:
            return on.exactA(F, sbar, Pl)[0]
        except np.linalg.LinAlgError:
            return 0.0
    rng = np.random.default_rng(0); best = ex(Fc.ravel())
    starts = [Fc.ravel()] + [rng.standard_normal(4) for _ in range(200)]
    for x0_ in starts:
        r = minimize(lambda x: -ex(x), x0_, method='Nelder-Mead', options=dict(maxiter=3000, xatol=1e-12, fatol=1e-13))
        best = max(best, -r.fun)
    print('   direct max of exact (A) bound over F: %.6f' % best)
    bb = on.boundB(Fc, sbar, Pl, 3.0)
    for x0_ in [Fc.ravel() / np.linalg.norm(Fc)] + [rng.standard_normal(4) for _ in range(12)]:
        r = minimize(lambda x: -on.boundB(x.reshape(2, 2) / max(1e-12, np.linalg.norm(x)), sbar, Pl, 3.0), x0_, method='Nelder-Mead', options=dict(maxiter=600))
        bb = max(bb, -r.fun)
    print('   best (B) bound found: %.6f' % bb, flush=True)
