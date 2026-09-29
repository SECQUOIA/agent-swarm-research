"""LP test for type-0 chains: nodes D^1 = [0,1] > D^2 > ... (each the child of the previous),
all split (m(y_k) - w_k < -beta, w_k >= tau), inside l = [0,1] valid at b = beta + kappa*tau.
Values of m at all split points and at 0, 1 are LP variables (non-convex m allowed).
Pattern: alternating slivers.  Reports feasibility (positive slack) for chain length r."""
import sys
import numpy as np
from scipy.optimize import linprog

def lp(nodes, kappa, beta=0.0):
    pts = sorted({0.0, 1.0} | {y for (_, _, y) in nodes})
    idx = {p: i for i, p in enumerate(pts)}
    P = len(pts)
    ws = [(y - l) * (u - y) for l, u, y in nodes]
    tau = min(ws)
    b = beta + kappa * tau
    A, B = [], []
    def row():
        return [0.0] * (P + 1)
    for (l, u, y), w in zip(nodes, ws):
        a = row(); a[idx[y]] = 1; a[P] = 1; A.append(a); B.append(-beta + w)  # invalid
        for p in pts:
            if l <= p <= u and p != y:
                ap = (p - l) * (u - p)
                a = row(); a[idx[y]] += 1; a[idx[p]] -= 1; a[P] = 1; A.append(a); B.append(w - ap)  # y minimizer
    for p in pts:
        a = row(); a[idx[p]] = -1; a[P] = 1; A.append(a); B.append(b - p * (1 - p))  # l valid at b
        a = row(); a[idx[p]] = -1; A.append(a); B.append(0.0)  # m >= 0
    res = linprog([0.0] * P + [-1.0], A_ub=A, b_ub=B, bounds=[(None, None)] * P + [(None, 1.0)], method="highs")
    if res.status != 0 or tau <= 0:
        return None
    return -res.fun / tau

def alt_chain(r, delta, small):
    l, u = 0.0, 1.0
    nodes = []
    side = 'R'   # first split near the right end
    for k in range(r):
        L = u - l
        if k == 0:
            y = u - delta * L
        elif side == 'R':
            y = u - small * L    # near the old right end
        else:
            y = l + small * L
        nodes.append((l, u, y))
        if k == 0:
            u = y; side = 'L'
        elif side == 'R':
            u = y; side = 'L'
        else:
            l = y; side = 'R'
    return nodes

if __name__ == "__main__":
    kappa = float(sys.argv[1])
    for r in range(2, 12):
        best = None
        for delta in np.geomspace(1e-4, 0.5, 25):
            for small in np.geomspace(1e-4, 0.5, 25):
                s = lp(alt_chain(r, delta, small), kappa)
                if s is not None and (best is None or s > best[0]):
                    best = (s, delta, small)
        print(r, best, flush=True)
