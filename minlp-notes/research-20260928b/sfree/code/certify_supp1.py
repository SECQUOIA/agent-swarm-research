"""Exact certificate refuting Conjecture 16 (support-1 minimizer => orbit family (A) attains z_K).

Instance (side '+', S = {w <= xy}, w = (1,1,1)):  sbar = (-2, 3, 2),  rays p_j = v_j - sbar to
v1 = t* = (0, 0, 0),  v2 = (6, -2, 1/4),  v3 = (1, -5/2, 1/2).
Checks (exact, sympy):
 (1) min over T* = conv{sbar, v1, v2, v3} of q = w - xy is 0, attained only at t* = v1, so z_K = 1 with
     the unique minimizer lambda = e1 (support 1); every edge of T* at t* is transversal:
     grad q(t*).(v - t*) > 0 for v in {sbar, v2, v3}; KKT multipliers of rays 2, 3 are positive.
 (2) Rational Y_v > 0 (positive definite) with sum_v M(v) Y_v = 0 exactly.  For every F,
     sum_v <sym(F^T M(v)), Y_v> = tr(F^T sum_v M(v) Y_v) = 0, so if sym(F^T M(v)) >= 0 at all four
     vertices then every sym(F^T M(v)) = 0; the linear system sym(F^T M(v)) = 0 (all v) has only F = 0.
     Hence no nonzero F has C_F containing T*.
 (3) Compactness (as in Theorem 14(3)): if z_A = 1, a normalized limit F != 0 would satisfy (2)'s
     closed conditions.  So z_A < z_K.
The PD certificate is found numerically (SDP) and then rounded and projected exactly onto the linear
constraints; positive definiteness of the exact rational matrices is checked exactly.
"""
import itertools
import numpy as np
import sympy as sp
import cvxpy as cp

R = sp.Rational
sb = sp.Matrix([-2, 3, 2]); v1 = sp.Matrix([0, 0, 0]); v2 = sp.Matrix([6, -2, R(1, 4)]); v3 = sp.Matrix([1, R(-5, 2), R(1, 2)])
verts = [sb, v1, v2, v3]
q = lambda s: s[2] - s[0] * s[1]
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)


# ---------------------------------------------------------------- (1)
L = sp.symbols('l0:4')
pt = sum((L[i] * verts[i] for i in range(4)), sp.zeros(3, 1))
cands = []
for r in range(1, 5):
    for Fc in itertools.combinations(range(4), r):
        sub = {L[i]: 0 for i in range(4) if i not in Fc}
        free = [L[i] for i in Fc]
        expr = sp.expand(q(pt).subs(sub))
        mu = sp.Symbol('mu')
        eqs = [sp.diff(expr, x) - mu for x in free] + [sum(free) - 1]
        sols = sp.solve(eqs, free + [mu], dict=True) if r > 1 else [{free[0]: 1}]
        for so in sols:
            vals = [None if so.get(x) is None else sp.sympify(so.get(x)) for x in free]
            if any(v is None for v in vals):
                # singular face: a continuum of stationary points; q is constant on it, so its minimum
                # value is attained at the endpoints on the relative boundary (enumerated), and a
                # continuum of minimizers would show up there as extra boundary minimizers)
                continue
            if all(v.is_real and v >= 0 for v in vals):
                cands.append((sp.nsimplify(q(pt.subs(sub).subs(dict(zip(free, vals))))), Fc, tuple(vals)))
qmin = min(c[0] for c in cands)
arg = [c for c in cands if c[0] == qmin]
check('(1) q(sbar) = %s > 0' % q(sb), q(sb) > 0)
check('(1) min over T* of q = %s' % qmin, qmin == 0)
check('(1) unique minimizer is the vertex t* = v1: %s' % [(c[1], c[2]) for c in arg],
      all(c[1] == (1,) for c in arg))
gt = sp.Matrix([-v1[1], -v1[0], 1])
for name, v in (('sbar', sb), ('v2', v2), ('v3', v3)):
    check('(1) transversal edge at t*: grad q(t*).(%s - t*) = %s > 0' % (name, gt.dot(v - v1)), gt.dot(v - v1) > 0)
# KKT at lambda = e1:  w + sigma * P^T grad q(t*) - nu = 0, nu_1 = 0
P = sp.Matrix.hstack(*[v - sb for v in (v1, v2, v3)])
g = P.T * gt
sigma = -1 / g[0]
nu = [1 + sigma * g[j] for j in range(3)]
check('(1) KKT: sigma = %s > 0, multipliers of rays 2, 3 = %s > 0 (strict complementarity)' % (sigma, nu[1:]),
      sigma > 0 and nu[0] == 0 and nu[1] > 0 and nu[2] > 0)
check('(1) det P = %s != 0' % P.det(), P.det() != 0)

# ---------------------------------------------------------------- (2)
M = lambda s: sp.Matrix([[s[2], s[0]], [s[1], 1]])
Ms = [M(v) for v in verts]
Mf = [np.array(m.tolist(), dtype=float) for m in Ms]
Y = [cp.Variable((2, 2), symmetric=True) for _ in range(4)]
t = cp.Variable()
cons = [Y[i] - t * np.eye(2) >> 0 for i in range(4)] + [sum(Mf[i] @ Y[i] for i in range(4)) == 0,
                                                       sum(cp.trace(Y[i]) for i in range(4)) == 1]
pr = cp.Problem(cp.Maximize(t), cons); pr.solve(solver='CLARABEL')
print('   SDP: max min-eigenvalue of a certificate = %.3e (status %s)' % (t.value, pr.status))
# round to rationals and project exactly: unknowns = 12 entries (a_i, b_i, c_i); 4 linear equations.
syms = sp.symbols('y0:12')
Ysym = [sp.Matrix([[syms[3 * i], syms[3 * i + 1]], [syms[3 * i + 1], syms[3 * i + 2]]]) for i in range(4)]
eqs = list(sum((Ms[i] * Ysym[i] for i in range(4)), sp.zeros(2, 2)))
num = {}
for i in range(4):
    Yv = Y[i].value
    for k, (a, bb) in enumerate(((0, 0), (0, 1), (1, 1))):
        num[syms[3 * i + k]] = sp.Rational(Yv[a, bb]).limit_denominator(10 ** 12)
# solve the 4 equations for 4 pivot unknowns, keep the other 8 at their rounded values
A_, b_ = sp.linear_eq_to_matrix(eqs, syms)
piv = A_.rref()[1]
pivots = [syms[j] for j in piv]
others = {s: num[s] for s in syms if s not in pivots}
sol = sp.solve([e.subs(others) for e in eqs], pivots, dict=True)[0]
full = {**others, **sol}
Yex = [Yi.subs(full) for Yi in Ysym]
check('(2) sum_v M(v) Y_v = 0 exactly', sum((Ms[i] * Yex[i] for i in range(4)), sp.zeros(2, 2)) == sp.zeros(2, 2))
pd = all(Yi[0, 0] > 0 and Yi.det() > 0 for Yi in Yex)
check('(2) all Y_v positive definite (exact)', pd)
print('   min eigenvalue (float) of the exact certificate: %.3e' % min(np.linalg.eigvalsh(np.array(Yi.tolist(), dtype=float))[0] for Yi in Yex))
F = sp.Matrix(2, 2, sp.symbols('f0:4'))
lin = []
for m in Ms:
    X = F.T * m
    lin += list(X + X.T)
sol0 = sp.solve(lin, list(F), dict=True)
check('(2) sym(F^T M(v)) = 0 for all v forces F = 0', sol0 == [{s: 0 for s in F}] or all(all(v == 0 for v in s_.values()) for s_ in sol0))
print('ALL PASS' if ok else 'SOME CHECK FAILED')
