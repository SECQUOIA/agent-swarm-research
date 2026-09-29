"""Right-split chains converging to the breakpoint s=0 from the right, node [-o, u_k], split y_k = u_k * rho,
K=[0,1], K-=[-1,0] valid at beta+kappa*tau.  LP over m-values (uses chainlp.test's constraint set)."""
import sys
import numpy as np
from scipy.optimize import linprog

def lp(nodes, kappa, beta=0.0):
    ws = [(y - l) * (u - y) for l, u, y in nodes]
    tau = min(ws); b = beta + kappa * tau
    r = len(nodes)
    A, B = [], []
    pts = sorted({y for _, _, y in nodes} | {nodes[0][0], nodes[0][1]})
    idx = {p: i for i, p in enumerate(pts)}; P = len(pts)
    def row(): return [0.0] * (P + 1)
    for (l, u, y), w in zip(nodes, ws):
        a = row(); a[idx[y]] = 1; a[P] = 1; A.append(a); B.append(-beta + w)
        for p in pts:
            if l <= p <= u and p != y:
                a = row(); a[idx[y]] += 1; a[idx[p]] -= 1; a[P] = 1; A.append(a); B.append(w - (p - l) * (u - p))
    for p in pts:
        aK = p * (1 - p) if p >= 0 else (p + 1) * (-p)
        a = row(); a[idx[p]] = -1; a[P] = 1; A.append(a); B.append(b - aK)
        a = row(); a[idx[p]] = -1; A.append(a); B.append(0.0)
    res = linprog([0.0] * P + [-1.0], A_ub=A, b_ub=B, bounds=[(None, None)] * P + [(None, 1.0)], method="highs")
    return None if res.status != 0 else -res.fun / tau

if __name__ == "__main__":
    kappa = float(sys.argv[1])
    for r in range(2, 9):
        best = None
        for o in (0.05, 0.2, 0.5, 0.9, 0.999):
            for u0 in (0.05, 0.2, 0.5, 0.9, 0.999):
                for rho in np.geomspace(1e-3, 0.99, 30):
                    nodes = []; u = u0
                    for k in range(r):
                        y = u * rho; nodes.append((-o, u, y)); u = y
                    s = lp(nodes, kappa)
                    if s is not None and (best is None or s > best[0]):
                        best = (round(s, 4), o, u0, round(rho, 4))
        print(kappa, r, best, flush=True)
