# Symbolic check of the second-order implicit-differentiation step used in Psi (pindyck):
# s = a + b*exp(-K s)  =>  Hess s = iota*Hess a + kappa*Hess b - K*kappa*(gb gs^T + gs gb^T) + K^2*b*kappa*gs gs^T,
# phi = exp(-K s), iota = 1/(1+K b phi), kappa = phi*iota.
import sympy as sp
p1, p2, K = sp.symbols("p1 p2 K", positive=True)
a = sp.Function("a")(p1, p2); b = sp.Function("b")(p1, p2); s = sp.Function("s")(p1, p2)
G = s - a - b * sp.exp(-K * s)
P = (p1, p2)
# first derivatives from the identity
ds = {}
for v in P:
    eq = sp.diff(G, v)
    ds[v] = sp.solve(eq, sp.diff(s, v))[0]
# second derivatives from the identity
ok = True
phi = sp.exp(-K * s); iota = 1 / (1 + K * b * phi); kap = phi * iota
for i, u in enumerate(P):
    for v in P[i:]:
        eq = sp.diff(G, u, v)
        d2 = sp.solve(eq, sp.diff(s, u, v))[0]
        d2 = d2.subs({sp.diff(s, u): ds[u], sp.diff(s, v): ds[v]})
        gs_u, gs_v = ds[u], ds[v]
        gb_u, gb_v = sp.diff(b, u), sp.diff(b, v)
        formula = iota * sp.diff(a, u, v) + kap * sp.diff(b, u, v) - K * kap * (gb_u * gs_v + gs_u * gb_v) \
            + K**2 * b * kap * gs_u * gs_v
        diff = sp.simplify(d2 - formula)
        print(u, v, "difference:", diff)
        ok = ok and diff == 0
# first-order formula
for v in P:
    print(v, "first-order difference:", sp.simplify(ds[v] - (iota * sp.diff(a, v) + kap * sp.diff(b, v))))
print("all zero:", ok)
