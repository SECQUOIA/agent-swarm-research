"""R2-math referee checks (single-threaded, short).

1. Witness of Prop 6.1: PSD completion of the dense moment matrix exists (p_xz = 3/5)
   and is unique; it violates p_xz <= m_x.
2. Cut (6.3) and witness arithmetic.
3. k = 3 gluing on A={0,2}, C={1,3}, y in [0,3]: no zero witness (alt = 3 = k),
   but an exact feasible pair of measures gives a glued value < 1/2 = true min.
4. Example 4.5 envelope value and Corollary 6.5 pairwise-intersection remark.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
from fractions import Fraction as Fr
import sympy as sp
import numpy as np
from scipy.optimize import linprog

# ---- 1. PSD completion at the witness
mx, my, mz, sx, sy, sz, pxy, pyz = [sp.Rational(*t) for t in
    [(1,2),(1,2),(4,5),(1,2),(5,16),(4,5),(3,8),(1,2)]]
w = sp.symbols('w')
M = sp.Matrix([[1, mx, my, mz],[mx, sx, pxy, w],[my, pxy, sy, pyz],[mz, w, pyz, sz]])
det = sp.factor(M.det())
print("det M(w) =", det)
sols = sp.solve(sp.Eq(M.det(), 0), w)
print("roots of det:", sols)
M35 = M.subs(w, sp.Rational(3,5))
print("eigenvalues at w=3/5:", [sp.nsimplify(e) for e in M35.eigenvals()])
# leading principal minors of the two clique blocks
print("block (1,x,y) det:", sp.Matrix([[1,mx,my],[mx,sx,pxy],[my,pxy,sy]]).det(),
      " block (1,y,z) det:", sp.Matrix([[1,my,mz],[my,sy,pyz],[mz,pyz,sz]]).det())
# check for which w M is PSD: sample
ok = [float(t) for t in np.linspace(0.4, 0.8, 4001) if min(np.linalg.eigvalsh(np.array(M.subs(w, t), dtype=float))) > -1e-12]
print("PSD w-range (numeric):", (min(ok), max(ok)) if ok else None)

# ---- 2. cut arithmetic
x, y, z = sp.symbols('x y z')
D = (y - sp.Rational(1,4) - x/2)**2 + (y - sp.Rational(5,8)*z)**2 + x*(1-x) + z*(1-z)
print("expanded D:", sp.expand(D))
lin = {x: mx, y: my, z: mz}
Dexp = sp.Poly(sp.expand(D), x, y, z)
val = 0
mom = {(1,0,0): mx, (0,1,0): my, (0,0,1): mz, (2,0,0): sx, (0,2,0): sy, (0,0,2): sz,
       (1,1,0): pxy, (0,1,1): pyz, (0,0,0): 1}
for mon, c in Dexp.terms():
    val += c * mom[mon]
print("linearized D at witness:", val)

# ---- 3. k = 3 gluing, A={0,2}, C={1,3} on [0,3]
A = [0, 2]; C = [1, 3]; lo, hi = 0, 3; k = 3
grid = [Fr(i, 32) for i in range(lo*32, hi*32 + 1)]
dA = [min((g - a)**2 for a in A) for g in grid]
dC = [min((g - c)**2 for c in C) for g in grid]
n = len(grid)
cvec = np.array([float(v) for v in dA + dC])
Aeq = []; beq = []
Aeq.append([1.0]*n + [0.0]*n); beq.append(1.0)
Aeq.append([0.0]*n + [1.0]*n); beq.append(1.0)
for j in range(1, k+1):
    Aeq.append([float(g**j) for g in grid] + [-float(g**j) for g in grid]); beq.append(0.0)
res = linprog(cvec, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method="highs")
print("k=3 grid LP value (float):", res.fun)
supp = [i for i in range(2*n) if res.x[i] > 1e-9]
print("support:", [("A" if i < n else "C", str(grid[i % n]), round(res.x[i], 6)) for i in supp])
# exact re-solve on the support
lam = sp.symbols('l0:%d' % len(supp))
eqs = []
eqs.append(sum(lam[t] for t, i in enumerate(supp) if i < n) - 1)
eqs.append(sum(lam[t] for t, i in enumerate(supp) if i >= n) - 1)
for j in range(1, k+1):
    eqs.append(sum((1 if i < n else -1) * lam[t] * sp.Rational(grid[i % n].numerator, grid[i % n].denominator)**j
                   for t, i in enumerate(supp)))
sol = sp.solve(eqs, lam, dict=True)
print("exact solutions:", sol)
if sol:
    s = sol[0]
    if all(sym in s for sym in lam):
        weights = [s[l] for l in lam]
        objv = sum(weights[t] * sp.Rational((dA + dC)[i].numerator, (dA + dC)[i].denominator) for t, i in enumerate(supp))
        print("exact weights nonneg:", all(wt >= 0 for wt in weights), " exact glued value:", objv, "=", float(objv))

# ---- 4. misc
u = sp.symbols('u')
print("min_{[-1,1]} u^2-u^3 candidates:", [ (t, (t**2 - t**3)) for t in [-1, 0, sp.Rational(2,3), 1]])
