"""LP feasibility of a long minimizer-rule chain around one certificate breakpoint.

Given a breakpoint s and a sequence of split points y_1..y_K (the chain: node
B^1 = [0,1], B^{k+1} = child of B^k at y_k containing s), decide whether some
polyhedral instance (knots = {0, s, 1, y_k, extra}) has
  * [0,s] and [s,1] valid (so N_opt <= 2),
  * every B^k invalid with margin delta and y_k a minimizer of phi_{B^k}.
Maximize delta.  alpha = 1.
"""
import sys
import numpy as np
from scipy.optimize import linprog


def chain_nodes(s, ys):
    l, u = 0.0, 1.0
    nodes = []
    for y in ys:
        if not (l < y < u):
            return None
        nodes.append((l, u, y))
        if y > s:
            u = y
        elif y < s:
            l = y
        else:
            return None
    return nodes


def solve(s, ys, extra=()):
    nodes = chain_nodes(s, ys)
    if nodes is None:
        return None
    xs = np.array(sorted(set([0.0, 1.0, s] + list(ys) + list(extra))))
    n = len(xs)
    idx = {x: i for i, x in enumerate(xs)}
    # variables: m_0..m_{n-1}, delta ; maximize delta
    A, b = [], []
    # convexity of H = m + x^2: slope_j <= slope_{j+1}
    for j in range(1, n - 1):
        h1, h2 = xs[j] - xs[j - 1], xs[j + 1] - xs[j]
        row = np.zeros(n + 1)
        # (H_j - H_{j-1})/h1 - (H_{j+1} - H_j)/h2 <= 0
        row[j] += 1 / h1 + 1 / h2
        row[j - 1] -= 1 / h1
        row[j + 1] -= 1 / h2
        rhs = -(xs[j] ** 2 - xs[j - 1] ** 2) / h1 + (xs[j + 1] ** 2 - xs[j] ** 2) / h2
        A.append(row); b.append(rhs)
    # validity of [0,s] and [s,1]: -m_j <= -(x-l)(u-x)
    for j, x in enumerate(xs):
        row = np.zeros(n + 1); row[j] = -1
        if 0 < x < s:
            A.append(row); b.append(-(x) * (s - x))
        elif s < x < 1:
            A.append(row); b.append(-(x - s) * (1 - x))
    # chain nodes
    for (l, u, y) in nodes:
        jy = idx[y]
        qy = (y - l) * (u - y)
        row = np.zeros(n + 1); row[jy] = 1; row[n] = 1   # m_y - qy + delta <= 0
        A.append(row); b.append(qy)
        for j, x in enumerate(xs):
            if l < x < u and j != jy:
                row = np.zeros(n + 1); row[jy] = 1; row[j] = -1
                A.append(row); b.append(qy - (x - l) * (u - x))
    c = np.zeros(n + 1); c[n] = -1
    bounds = [(0, None)] * n + [(None, 1.0)]
    r = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
    if r.status != 0:
        return None
    return r.x[n], xs, r.x[:n]


if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    s = 1.0 / 3.0
    for K in range(1, 9):
        best = None
        for trial in range(3000):
            # random chain: sides and log-distances
            ys = []
            l, u = 0.0, 1.0
            ok = True
            for k in range(K):
                side = rng.integers(2)
                frac = np.exp(rng.uniform(-12, 0))
                if side:
                    y = s + frac * (u - s) * rng.uniform(0.01, 0.99)
                    u = y
                else:
                    y = s - frac * (s - l) * rng.uniform(0.01, 0.99)
                    l = y
                ys.append(y)
            r = solve(s, ys)
            if r is not None and (best is None or r[0] > best[0]):
                best = (r[0], ys)
        print(K, "best delta", None if best is None else best[0],
              None if best is None else ["%.3g" % (y - s) for y in best[1]], flush=True)
