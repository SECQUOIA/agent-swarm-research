"""LP test: can a chain of pruned-R_min nodes containing a breakpoint s = 0 have many splits
inside K = [0, 1] (class ii: node does not contain 1) when K and K- = [-1, 0] are valid at
budget b = beta + kappa*tau, nodes are invalid at beta and have w >= tau?
Only values of m at split points enter (non-convex m allowed).  Geometry random; maximize slack."""
import sys, random
import numpy as np
from scipy.optimize import linprog

def test(ys_side, rng, kappa, tau=1.0, beta=0.0):
    # build chain: start N = [l,u] with -1 < l < 0 < u < 1
    l, u = -rng.uniform(0.05, 1.0), rng.uniform(0.05, 1.0)
    nodes = []
    for side in ys_side:
        if side == 'R':
            y = rng.uniform(0, u) ** rng.choice([1, 1, 2, 4]) if rng.random() < 0.5 else u * (1 - rng.uniform(0, 1) ** 3)
            y = min(max(y, 1e-9), u * (1 - 1e-9))
        else:
            y = -rng.uniform(0, -l) if rng.random() < 0.5 else l * (1 - rng.uniform(0, 1) ** 3)
            y = max(min(y, -1e-9), l * (1 - 1e-9))
        nodes.append((l, u, y))
        if side == 'R':
            u = y
        else:
            l = y
    # scale tau: set tau = min w (so w >= tau holds); variables m_k
    ws = [(y - l_) * (u_ - y) for l_, u_, y in nodes]
    tau = min(ws)
    b = beta + kappa * tau
    r = len(nodes)
    A, B = [], []
    # variables: m_1..m_r, s (slack); maximize s
    def row():
        return [0.0] * (r + 1)
    for k, (lk, uk, yk) in enumerate(nodes):
        # invalid: m_k - w_k + s <= -beta
        a = row(); a[k] = 1; a[r] = 1; A.append(a); B.append(-beta + ws[k])
        for j, (lj, uj, yj) in enumerate(nodes):
            if j != k and lk < yj < uk:
                # m_j - aN(yj) >= m_k - w_k  ->  m_k - m_j + s <= w_k - aN(yj)
                a = row(); a[k] += 1; a[j] -= 1; a[r] = 1; A.append(a); B.append(ws[k] - (yj - lk) * (uk - yj))
        # validity of K or K-: m_k >= aK(y) - b  ->  -m_k + s <= b - aK
        aK = yk * (1 - yk) if yk > 0 else (yk + 1) * (-yk)
        a = row(); a[k] = -1; a[r] = 1; A.append(a); B.append(b - aK)
        # m >= 0
        a = row(); a[k] = -1; a[r] = 0; A.append(a); B.append(0.0)
    c = [0.0] * r + [-1.0]
    res = linprog(c, A_ub=A, b_ub=B, bounds=[(None, None)] * r + [(None, 1.0)], method="highs")
    if res.status != 0:
        return None
    return -res.fun, nodes

if __name__ == "__main__":
    kappa = float(sys.argv[1]); trials = int(sys.argv[2]); seed = int(sys.argv[3])
    rng = random.Random(seed)
    best = {}
    for t in range(trials):
        L = rng.randint(2, 9)
        pat = ''.join(rng.choice('RRL') for _ in range(L))
        out = test(pat, rng, kappa)
        if out is None:
            continue
        s, nodes = out
        nR = pat.count('R')
        if s > 1e-6 and nR > best.get('nR', 0):
            best = dict(nR=nR, pat=pat, slack=s, nodes=nodes)
            print(f"feasible with {nR} right-splits in K, pattern {pat}, slack {s:.3g}", flush=True)
    print("best", best.get('nR'), best.get('pat'))
