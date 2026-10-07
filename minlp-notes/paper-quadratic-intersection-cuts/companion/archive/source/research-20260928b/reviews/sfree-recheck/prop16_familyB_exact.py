"""Attempt an exact certificate that family (B) (upward closures) also misses T* in Proposition 16.

T* lies in the (B) set of F iff for each vertex v some tau_v in [0, q(v)] has sym(F^T (M(v) - tau_v E)) >= 0
(E = e1 e1^T; tau = 0 at t* = v1 because q(t*) = 0).  Look for Y_v(tau) = Y_v^0 + sum_u tau_u Z_v^u, affine in
tau = (tau_sbar, tau_v2, tau_v3), with
    sum_v (M(v) - tau_v E) Y_v(tau) = 0   identically in tau   (coefficients of 1, tau_u, tau_u tau_w vanish)
and Y_v(tau) positive definite at the 8 corners of the box prod [0, q(v)] (hence on the whole box, by
convexity).  Then for every lowering no nonzero F works (Proposition 16(2) argument), and the compactness
argument of Theorem 14(3) (with limits of the lowering parameters) gives z_B < 1.
Found numerically by an SDP, then rounded in an exact rational kernel basis and verified exactly.
"""
import itertools
from fractions import Fraction as Fr
import numpy as np, sympy as sp, cvxpy as cp
R = sp.Rational
V = {'s': sp.Matrix([-2, 3, 2]), '1': sp.Matrix([0, 0, 0]), '2': sp.Matrix([6, -2, R(1, 4)]), '3': sp.Matrix([1, R(-5, 2), R(1, 2)])}
q = lambda s: s[2] - s[0] * s[1]
M = lambda s: sp.Matrix([[s[2], s[0]], [s[1], 1]])
E = sp.Matrix([[1, 0], [0, 0]])
verts = ['s', '1', '2', '3']; low = ['s', '2', '3']            # lowered vertices (tau at v1 is 0)
box = {u: q(V[u]) for u in low}
print('box:', box)
tau = {u: sp.Symbol('tau_' + u) for u in low}
# unknown symmetric matrices: Y0_v and Z_v^u
unk = []
def symm(name):
    a, b, c = sp.symbols(name + '_a ' + name + '_b ' + name + '_c'); unk.extend([a, b, c])
    return sp.Matrix([[a, b], [b, c]])
Y0 = {v: symm('Y0' + v) for v in verts}
Z = {(v, u): symm('Z' + v + u) for v in verts for u in low}
Yt = {v: Y0[v] + sum((tau[u] * Z[(v, u)] for u in low), sp.zeros(2, 2)) for v in verts}
expr = sum(((M(V[v]) - (tau[v] if v in tau else 0) * E) * Yt[v] for v in verts), sp.zeros(2, 2))
eqs = []
for e in expr:
    P = sp.Poly(sp.expand(e), *[tau[u] for u in low])
    eqs += list(P.coeffs())
A, _ = sp.linear_eq_to_matrix(eqs, unk)
K = A.nullspace()
print('unknowns %d, independent equations %d, kernel dimension %d' % (len(unk), A.rank(), len(K)), flush=True)
Kn = np.array([[float(x) for x in k] for k in K]).T
c = cp.Variable(len(K)); t = cp.Variable(); y = Kn @ c
idx = {s: i for i, s in enumerate(unk)}
def mat_at(v, corner):   # Y_v(tau) at a corner, as cvxpy expression
    def ent(name):
        e = y[idx[sp.Symbol('Y0' + v + '_' + name)]]
        for u in low:
            e = e + float(corner[u]) * y[idx[sp.Symbol('Z' + v + u + '_' + name)]]
        return e
    return cp.bmat([[ent('a'), ent('b')], [ent('b'), ent('c')]])
corners = [dict(zip(low, cs)) for cs in itertools.product(*[(0, box[u]) for u in low])]
cons = [mat_at(v, cn) - t * np.eye(2) >> 0 for v in verts for cn in corners] + [cp.norm(y, 'inf') <= 1]
cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
print('SDP margin (min eigenvalue over the 32 corner matrices, entries <= 1): %.3e' % t.value, flush=True)
ok = False
if t.value > 0:
    cn = c.value / np.max(np.abs(c.value))
    for D in (10, 100, 1000, 10 ** 4, 10 ** 6, 10 ** 8):
        cr = [R(Fr(float(x)).limit_denominator(D).numerator, Fr(float(x)).limit_denominator(D).denominator) for x in cn]
        sol = dict(zip(unk, list(sum((cr[k] * K[k] for k in range(len(K))), sp.zeros(len(unk), 1)))))
        Yex = {v: Yt[v].subs(sol) for v in verts}
        ident = sum(((M(V[v]) - (tau[v] if v in tau else 0) * E) * Yex[v] for v in verts), sp.zeros(2, 2)).applyfunc(sp.expand)
        pd = all((lambda Ym: Ym[0, 0] > 0 and Ym.det() > 0)(Yex[v].subs({tau[u]: cn_[u] for u in low}))
                 for v in verts for cn_ in corners)
        if ident == sp.zeros(2, 2) and pd:
            ok = True
            print('exact certificate found (coefficient denominators <= %d):' % D)
            for v in verts:
                print('  Y_%s(tau) = %s' % (v, Yex[v].applyfunc(sp.nsimplify).tolist()))
            print('  identity sum_v (M(v) - tau_v E) Y_v(tau) = 0 holds exactly; all 32 corner matrices PD (exact)')
            break
print('RESULT: family (B) excluded exactly' if ok else 'RESULT: no exact affine certificate found')
