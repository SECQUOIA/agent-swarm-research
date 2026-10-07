"""R1-math: numeric checks of Lemma 7.1 (distance duality with cone coordinates),
Theorem 7.2 call bound for column generation, and the grid fallback bound."""
import numpy as np, random, math, itertools
from scipy.optimize import linprog
rng = np.random.default_rng(5)

def dist_primal(Fp, zb, J):
    n, k = Fp.shape
    # vars: lam (n), q (k), t (k)
    c = np.concatenate([np.zeros(n), np.zeros(k), np.ones(k)])
    A_ub = []; b_ub = []
    for j in range(k):
        row = np.zeros(n+2*k); row[:n] = Fp[:, j]; row[n+j] = 1; row[n+k+j] = -1; A_ub.append(row); b_ub.append(zb[j])
        row = np.zeros(n+2*k); row[:n] = -Fp[:, j]; row[n+j] = -1; row[n+k+j] = -1; A_ub.append(row); b_ub.append(-zb[j])
    A_eq = [np.concatenate([np.ones(n), np.zeros(2*k)])]; b_eq = [1]
    bounds = [(0, None)]*n + [((0, None) if j in J else (0, 0)) for j in range(k)] + [(None, None)]*k
    r = linprog(c, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=bounds, method='highs')
    return r.fun

def dist_dual(Fp, zb, J):
    n, k = Fp.shape
    W = Fp - zb
    # max tau s.t. tau <= c^T w_i, c in C_J
    c = np.concatenate([np.zeros(k), [-1]])
    A_ub = np.hstack([-W, np.ones((n, 1))]); b_ub = np.zeros(n)
    bounds = [((0, 1) if j in J else (-1, 1)) for j in range(k)] + [(None, None)]
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    return -r.fun, r.x[:k]

worst = 0
for trial in range(300):
    k = rng.integers(1, 5); n = rng.integers(1, 8)
    Fp = rng.normal(size=(n, k)); zb = rng.normal(size=k)*1.5
    J = set(j for j in range(k) if rng.random() < 0.4)
    p = dist_primal(Fp, zb, J); d, _ = dist_dual(Fp, zb, J)
    worst = max(worst, abs(p-d))
print("Lemma 7.1 duality max |primal-dual|:", worst)

# Column generation with an exact finite oracle (P finite set of points -> F(P) finite)
def cg(Fp, zb, J, eps, delta=0.0):
    n, k = Fp.shape
    W = [Fp[0] - zb]; calls = 0; dirs = []
    while True:
        Wm = np.array(W)
        UB, cbar = dist_dual(Wm + zb, zb, J)
        if UB <= eps: return 'within', calls, dirs
        calls += 1; dirs.append(cbar.copy())
        vals = Fp @ cbar
        i = int(np.argmin(vals)); L = vals[i]
        if L > cbar @ zb + 1e-12: return 'cut', calls, dirs
        W.append(Fp[i] - zb)

maxratio = 0; okdist = True
for trial in range(200):
    k = int(rng.integers(1, 4)); n = int(rng.integers(2, 30))
    Fp = rng.uniform(-1, 1, size=(n, k)); zb = rng.uniform(-1, 1, size=k)
    J = set(j for j in range(k) if rng.random() < 0.4)
    R = max(np.abs(Fp - zb).sum(axis=1))
    eps = 0.05
    out, calls, dirs = cg(Fp, zb, J, eps)
    bound = 2*k*math.ceil(2*R/eps)**(k-1)
    maxratio = max(maxratio, calls/bound)
    # pairwise separation of directions
    for s, t in itertools.combinations(range(len(dirs)), 2):
        if np.max(np.abs(dirs[s]-dirs[t])) <= eps/R - 1e-9: okdist = False
    dist = dist_primal(Fp, zb, J)
    if dist > eps + 1e-9 and out != 'cut': print("missed cut!")
    if dist < 1e-12 and out == 'cut': print("cut at member!")
    for c in dirs:
        if abs(np.max(np.abs(c)) - 1) > 1e-7 and out == 'within': pass
print("Thm 7.2: max calls/bound:", maxratio, " pairwise separation ok:", okdist)
