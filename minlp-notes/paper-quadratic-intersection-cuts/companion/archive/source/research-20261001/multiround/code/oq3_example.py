"""OQ3 (iii): a loop of intersection cuts from maximal quadratic-free sets that converges to a
wrong value.  Instance (proposition in note.md, Section 6):
    min eps*x + y + w   s.t.  0 <= x <= X, 0 <= y <= Y, 1 <= w <= W,  w <= x*y   (eps > 0)
z* = 1 + 2 sqrt(eps) (at x = 1/sqrt(eps), y = sqrt(eps), w = 1), z_LP = 1 at (0, 0, 1).
Sets C_a = {w >= (a x + y/a)^2 / 4}: images of SCIP's set at (0,0,1) under (x,y,w) -> (x/a, a y, w),
maximal S-free for S = {w <= x y}.  Adversarial rule: in round r use a_r = 2/xi_{r+1}.

Part A (exact, sympy): the one-round algebra in symbols, then rounds 0..R in exact rationals for
eps = 1/4, xi_r = 2 (1 - 2^-r): LP optimality of v_r = (xi_r, 0, 1) (strict dual feasibility of its
basis, primal feasibility for all constraints), v_r in int C_a, the three step lengths, and the
new cut x/xi' + (xi'/4) y >= 1.
Part B (numerical): the same instance with the natural rules (Python model of SCIP's set, best
orbit set, geo, pertE0.1) for up to 60 rounds; reports LP value / z* per round.
Usage: python3 oq3_example.py R ROUNDS_B"""
import sys, itertools
import numpy as np
import sympy as sp

R, RB = int(sys.argv[1]), int(sys.argv[2])

# ------------------------------------------------------------------ Part A: symbolic one round
xi, xp, eps, t = sp.symbols('xi xip eps t', positive=True)
a = 2 / xp
beta = xi / 4
v = sp.Matrix([xi, 0, 1])
r1 = sp.Matrix([-beta * xi, 1, 0]); rx = sp.Matrix([1, 0, 0]); rw = sp.Matrix([0, 0, 1])
c = sp.Matrix([eps, 1, 1])
inC = lambda p: p[2] - (a * p[0] + p[1] / a) ** 2 / 4          # >= 0 iff p in C_a
print('Part A (symbolic, 0 < xi < xi\'):')
print('  q at v_r = w - x y =', sp.simplify(v[2] - v[0] * v[1]))
print('  C_a value at v_r (> 0 means interior):', sp.factor(inC(v)))
ax = sp.solve(sp.Eq(inC(v + t * rx), 0), t); a1 = sp.solve(sp.Eq(inC(v + t * r1), 0), t)
print('  roots along e_x:', [sp.simplify(z) for z in ax], ' roots along r_1:', [sp.simplify(z) for z in a1])
print('  along e_w: C_a value', sp.simplify(inC(v + t * rw)), '(increasing in t: alpha_w = inf)')
alx = xp - xi; al1 = 4 / (xi + xp)
# check they are the smallest positive roots: value at 0 > 0, and the C_a value along the ray is a
# concave quadratic in t, so the positive root is the exit point
for nm, rr, al in (('e_x', rx, alx), ('r_1', r1, al1)):
    g = sp.expand(inC(v + t * rr))
    print('  %s: C_a(v + t r) = %s ; leading coefficient %s ; value at alpha = %s' % (
        nm, sp.factor(g), sp.factor(sp.Poly(g, t).LC()), sp.simplify(g.subs(t, al))))
# cut lam_x/alpha_x + lam_1/alpha_1 >= 1 in x-coordinates: x = v + lam_x e_x + lam_1 r_1 + lam_w e_w
X, Y, Wv = sp.symbols('X Y W')
lam1 = Y; lamx = X - xi + beta * xi * Y
cut = sp.simplify((lamx / alx + lam1 / al1 - 1) * alx / xp)
print('  cut (as expression >= 0):', sp.factor(cut), ' target: X/xip + xip*Y/4 - 1 ->',
      sp.simplify(cut - (X / xp + xp * Y / 4 - 1)) == 0)
print('  reduced costs at v_r (rays e_x, r_1, e_w):', [sp.simplify((c.T * rr)[0]) for rr in (rx, r1, rw)])
print('  next vertex on e_x iff eps*alpha_x < c^T r_1 * alpha_1, i.e.',
      sp.simplify(eps * alx - (1 - eps * xi ** 2 / 4) * al1), '< 0')

# ------------------------------------------------------------------ Part A: exact rounds
E = sp.Rational(1, 4)
Xb, Yb, Wb = 10, 10, 10
xs = [2 * (1 - sp.Rational(1, 2 ** r)) for r in range(R + 2)]
rows = [([-1, 0, 0], 0), ([1, 0, 0], Xb), ([0, -1, 0], 0), ([0, 1, 0], Yb), ([0, 0, -1], -1), ([0, 0, 1], Wb)]
cvec = sp.Matrix([E, 1, 1])
ok_all = True
print('\nPart A (exact rationals, eps = 1/4, xi_r = 2(1 - 2^-r), box 10):  z* = 2')
for r in range(R + 1):
    vr = sp.Matrix([xs[r], 0, 1])
    act = [k for k, (g, h) in enumerate(rows) if (sp.Matrix([g]) * vr)[0] == h]
    viol = [k for k, (g, h) in enumerate(rows) if (sp.Matrix([g]) * vr)[0] > h]
    Aact = sp.Matrix([rows[k][0] for k in act])
    ok = len(act) == 3 and not viol and Aact.det() != 0
    if ok:
        Rm = -Aact.inv()                       # rays: columns, A_act r_j = -e_j
        wred = [(cvec.T * Rm[:, j])[0] for j in range(3)]
        ok = all(wv > 0 for wv in wred)
        ap = 2 / xs[r + 1]
        Cv = vr[2] - (ap * vr[0] + vr[1] / ap) ** 2 / 4
        ok = ok and Cv > 0
        # steps along the three rays (exact: smallest positive root, or inf)
        al = []
        for j in range(3):
            g = sp.expand((vr + t * Rm[:, j])[2] - (ap * (vr + t * Rm[:, j])[0] + (vr + t * Rm[:, j])[1] / ap) ** 2 / 4)
            roots = [z for z in sp.solve(g, t) if z.is_real and z > 0]
            al.append(min(roots) if roots else sp.oo)
        # cut sum lam_j / al_j >= 1 with lam = b_act - A_act x
        coef = [0 if al[j] == sp.oo else 1 / al[j] for j in range(3)]
        # sum_j coef_j (b_j - A_j x) >= 1  <=>  (sum_j coef_j A_j) x <= sum_j coef_j b_j - 1
        g_cut = sum((coef[j] * sp.Matrix([rows[act[j]][0]]) for j in range(3)), sp.zeros(1, 3))
        h_cut = sum(coef[j] * rows[act[j]][1] for j in range(3)) - 1
        # normalize to the form  -(x/xi' + xi' y / 4) <= -1
        target = sp.Matrix([[-1 / xs[r + 1], -xs[r + 1] / 4, 0]])
        sc = -h_cut
        ok = ok and sc > 0
        ok = ok and sp.simplify(g_cut / sc - target) == sp.zeros(1, 3)
        rows.append(([sp.nsimplify(z) for z in (g_cut / sc)], -1))
        print('  round %2d  v = (%s, 0, 1)  LP value %s  basis rows %s  reduced costs %s  steps %s  ok %s' % (
            r, xs[r], 1 + E * xs[r], act, [str(z) for z in wred], [str(z) for z in al], ok))
    ok_all &= ok
print('  ALL ROUNDS VERIFIED:', ok_all, '; LP values 1 + xi_r/4 -> 3/2 < z* = 2; violation w - xy = 1 at every v_r')

# ------------------------------------------------------------------ Part B: natural rules
import os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mrcore as M
from scipy.optimize import linprog


def loop(rule, eps_=0.25, rounds=RB):
    A = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]]
    b = [0, 10, 0, 10, -1, 10]
    cc = np.array([eps_, 1.0, 1.0]); zstar = 1 + 2 * np.sqrt(eps_)
    vals = []
    for r in range(rounds + 1):
        res = linprog(cc, A_ub=np.array(A, float), b_ub=np.array(b, float), bounds=[(None, None)] * 3, method='highs')
        x = res.x; vals.append(res.fun)
        if abs(x[2] - x[0] * x[1]) < 1e-9 or r == rounds or res.fun >= zstar - 1e-9:
            break
        An = np.array(A, float); bn = np.array(b, float)
        sl = bn - An @ x
        cand = [k for k in range(len(A)) if sl[k] <= 1e-9 * max(1, abs(bn[k]))]
        basis = None
        for comb in itertools.combinations(cand, 3):
            Ab = An[list(comb)]
            if abs(np.linalg.det(Ab)) < 1e-12:
                continue
            Rm = -np.linalg.inv(Ab)
            if np.all(cc @ Rm >= -1e-12):
                basis = comb; break
        if basis is None:
            print('   no dual feasible basis found'); break
        Ab = An[list(basis)]; Rm = -np.linalg.inv(Ab); w = np.maximum(cc @ Rm, 0.0)
        side = '+'                              # w > x y at every LP vertex of this instance
        if x[2] <= x[0] * x[1]:
            side = '-'
        if rule == 'scip':
            al = M.scip_alpha(side, x, Rm)
        else:
            if rule == 'orbit':
                u = w
            elif rule == 'geo':
                u = np.linalg.norm(Rm, axis=0)
            else:  # pertE0.1
                nr = np.linalg.norm(Rm, axis=0); rate = w / nr
                u = nr * (rate / max(rate.max(), 1e-300) + 0.1)
            al, F, zk = M.orbit_alpha(side, x, Rm, u)
            if al is None:
                print('   orbit set failed'); break
        coef = M.inv(al)
        g = coef @ Ab; h = coef @ bn[list(basis)] - 1.0
        sc = np.abs(g).max(); A.append(list(g / sc)); b.append(h / sc)
    return np.array(vals) / zstar


print('\nPart B (numerical): LP value / z* by round, eps = 1/4 (z* = 2)')
for rule in ('scip', 'orbit', 'geo', 'pertE0.1'):
    v = loop(rule)
    show = [0, 1, 2, 3, 5, 10, 20, 40, len(v) - 1]
    print('  %-9s rounds run %3d  ' % (rule, len(v) - 1) + ' '.join('r%d %.6f' % (k, v[k]) for k in show if k < len(v)))
