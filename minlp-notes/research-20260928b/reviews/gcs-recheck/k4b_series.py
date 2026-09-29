"""Series check for Prop. B': ratio = 1/2 + theta^4/64 + O(theta^6).
With D = 1, r = sin t, P = e^{2it} (|P| = 1) and a = r e^{i phi}, psi = phi - 2t:
  g(psi) = r cos(psi + 2t) + sqrt(1 + r^2 - 2 r cos psi),   REL_H = 2 (1 + min g),  OPT = 4 cos t.
The minimiser psi* = pi/2 - t + delta(t) is found order by order from g'(psi*) = 0."""
import sympy as sp

t, ps = sp.symbols("t ps")
a1, a2, a3, a4, a5 = sp.symbols("a1 a2 a3 a4 a5")
r = sp.sin(t)
g = r * sp.cos(ps + 2 * t) + sp.sqrt(1 + r ** 2 - 2 * r * sp.cos(ps))
dg = sp.diff(g, ps)
delta = a1 * t + a2 * t ** 2 + a3 * t ** 3 + a4 * t ** 4 + a5 * t ** 5
psi = sp.pi / 2 - t + delta
N = 7
ser = sp.expand(sp.series(dg.subs(ps, psi), t, 0, N).removeO())
sol = {}
for k in range(1, N):
    c = sp.simplify(ser.coeff(t, k).subs(sol))
    free = [s for s in (a1, a2, a3, a4, a5) if s in c.free_symbols and s not in sol]
    if c != 0:
        assert free, f"order t^{k} unmatched: {c}"
        sol[free[0]] = sp.solve(c, free[0])[0]
print("solved:", sol)
dsol = delta.subs(sol).subs({a1: 0, a2: 0, a3: 0, a4: 0, a5: 0})
print("delta(t) =", dsol)
gmin = sp.series(g.subs(ps, sp.pi / 2 - t + dsol), t, 0, 8).removeO()
REL = 2 * (1 + gmin)
ratio = (4 * sp.cos(t) / REL - 1) / (1 / sp.cos(t) - 1)
print("ratio =", sp.series(ratio, t, 0, 6))
