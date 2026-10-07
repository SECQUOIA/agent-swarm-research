"""'bad' one-clique assignment plus Lasserre's (2006) redundant ball constraint 2 - x^2 - y^2 >= 0 in every pair
clique (order-1 localizing matrix). Floating point (Clarabel)."""
import cvxpy as cp
src = open("c4_sdp_variants.py").read().split("\nfor n in (5, 8):")[0]
ns = {}; exec(src, ns)
orig = cp.Problem.solve
def patched(self, *a, **k):
    # add ball localizing matrices: find the scalar moment variables per clique from the module-level Y is not exposed,
    # so rebuild: constraints are kept and we append the ball condition via the moment matrices' entries.
    return orig(self, *a, **k)
# simpler: re-implement with the ball constraint
b, g, ev = 0.6, 0.3, 0.05; a = b + ev
def solve(n, ball=True):
    mons = [(i, d - i) for d in range(5) for i in range(d + 1)]
    Y = [dict((m, cp.Variable()) for m in mons if m != (0, 0)) for _ in range(n - 1)]
    y = lambda e, m: 1.0 if m == (0, 0) else Y[e][m]
    cons = []
    b2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]; b1 = [(0, 0), (1, 0), (0, 1)]
    loc = lambda e, lin: cp.bmat([[sum(cf * y(e, (p[0] + q[0] + sh[0], p[1] + q[1] + sh[1])) for cf, sh in lin) for q in b1] for p in b1]) >> 0
    PX, MX, PY, MY = [(1, (0, 0)), (1, (1, 0))], [(1, (0, 0)), (-1, (1, 0))], [(1, (0, 0)), (1, (0, 1))], [(1, (0, 0)), (-1, (0, 1))]
    BALL = [(2, (0, 0)), (-1, (2, 0)), (-1, (0, 2))]
    for e in range(n - 1):
        cons.append(cp.bmat([[y(e, (p[0] + q[0], p[1] + q[1])) for q in b2] for p in b2]) >> 0)
        if e < n - 2:
            for d in range(1, 5):
                cons.append(Y[e][(0, d)] == Y[e + 1][(d, 0)])
        use = [MY, PX] + ([MX] if e == 0 else []) + ([PY] if e == n - 2 else []) + ([BALL] if ball else [])
        for lin in use:
            cons.append(loc(e, lin))
    obj = sum(a / 2 * (y(e, (2, 0)) + y(e, (0, 2))) + b * y(e, (1, 1)) + g / 2 * (y(e, (1, 2)) - y(e, (2, 1))) for e in range(n - 1))
    obj = obj + a / 2 * y(0, (2, 0)) + a / 2 * y(n - 2, (0, 2))
    pr = cp.Problem(cp.Minimize(obj), cons); pr.solve(solver="CLARABEL")
    return pr.value, pr.status
for n in (5, 8):
    for ball in (False, True):
        v, s = solve(n, ball)
        print(f"n={n} bad assignment, ball constraint {ball}: value {v:+.4e} ({s})", flush=True)
