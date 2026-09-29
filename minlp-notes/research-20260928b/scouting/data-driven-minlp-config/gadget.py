# Disjunctive gadget: y in [a2,b2] (convex), -(y-a)(y-b) <= 0 (reverse convex; y<=a or y>=b),
# a < a2 < b2 < b => infeasible. Secant relaxation of the concave function on [l,u].
# Root relaxation is feasible; after one split at theta both children are relaxation-infeasible
# iff theta lies in the "good" set G computed below. Also computes the full gadget tree size
# (branch always on y at l + alpha (u - l)) as a function of alpha.
import numpy as np, sys
def g(y, a, b): return -(y - a)*(y - b)
def relax_infeasible(l, u, a, b, a2, b2):
    lo, hi = max(l, a2), min(u, b2)
    if lo > hi: return True
    sl, su = g(l, a, b), g(u, a, b)
    s = lambda y: sl + (su - sl)*(y - l)/(u - l)
    return min(s(lo), s(hi)) > 0            # linear: positive on [lo,hi] iff at both ends
def good_set(a, b, a2, b2, N=200001):
    th = np.linspace(1e-6, 1 - 1e-6, N)
    ok = np.array([relax_infeasible(0, t, a, b, a2, b2) and relax_infeasible(t, 1, a, b, a2, b2) for t in th])
    idx = np.nonzero(ok)[0]
    return (th[idx[0]], th[idx[-1]], ok.sum()) if len(idx) else None
def tree(alpha, a, b, a2, b2, cap=10**6):
    stack, n = [(0.0, 1.0)], 0
    while stack:
        l, u = stack.pop(); n += 1
        if n > cap: return cap
        if relax_infeasible(l, u, a, b, a2, b2): continue
        p = l + alpha*(u - l); stack += [(l, p), (p, u)]
    return n
for (a, b, a2, b2) in [(0.3, 0.7, 0.45, 0.55), (0.3, 0.7, 0.49, 0.51), (0.1, 0.9, 0.2, 0.25), (0.6, 0.95, 0.8, 0.81)]:
    G = good_set(a, b, a2, b2)
    al = np.linspace(0.05, 0.95, 9001)
    T = np.array([tree(x, a, b, a2, b2) for x in al])
    print((a, b, a2, b2), 'good one-split theta interval', G, '| gadget tree size over alpha in [.05,.95]: min', T.min(), 'max', T.max(), 'pieces', 1 + int(np.sum(T[1:] != T[:-1])), 'alpha with size 3:', (al[T == 3].min(), al[T == 3].max()) if (T == 3).any() else None)
