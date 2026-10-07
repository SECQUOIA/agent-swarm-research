"""Review r2: are the large coefficients at non-root rational neighbours inherent?

For each non-root record of logs/thm3_r1.jsonl with a returned vector:
  1. rebuild the pivot-row rational neighbour (own copy of the procedure described
     in Section 8 / exp_separate.rationalize_rank; no stream import) and check that
     the logged vector has the logged exact value there;
  2. compute the integer kernel of the factor P independently (sympy LLL of an
     embedded graph lattice), its dimension and covolume;
  3. shorten the logged representative inside its kernel coset with sympy LLL
     (delta 0.99) on an affine embedding, which leaves the exact neighbour value
     unchanged, and evaluate the shortened vector at the stored point;
  4. split u^T Y u (u = 2v + e0) at the stored point into the part along the
     top-r eigenvectors and the discarded tail, to locate the stored-point value.
Usage from split-practice/: python3 reviews/r2-code/r2_nonroot.py
"""
import json
import math
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from sympy import QQ, ZZ
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[2]
opn = set(open(ROOT / 'logs/open_gap.txt').read().split())
only = sys.argv[1:]


def neighbour(Y, r, den=10**6):
    w, V = np.linalg.eigh(Y)
    idx = np.argsort(w)[::-1][:r]
    Yr = (V[:, idx] * w[idx]) @ V[:, idx].T
    N = Y.shape[0]; d = np.diag(Yr).copy(); K = []; Lf = np.zeros((N, r))
    for j in range(r):
        p = int(np.argmax(d)); K.append(p)
        Lf[:, j] = (Yr[:, p] - Lf[:, :j] @ Lf[p, :j]) / np.sqrt(d[p])
        d -= Lf[:, j] ** 2; d[K] = -np.inf
    P = [[F(int(round(Yr[k, j] * den)), den) for j in range(N)] for k in K]
    for a in range(r):
        for b in range(r):
            P[a][K[b]] = P[b][K[a]] if b < a else P[a][K[b]]
    C = [[P[a][K[b]] for b in range(r)] for a in range(r)]
    Ci = inv_frac(C)
    s = sum(P[a][0] * Ci[a][b] * P[b][0] for a in range(r) for b in range(r))
    G = [[x / s for x in row] for row in Ci]
    return P, G, w[np.argsort(w)[::-1]]


def inv_frac(A):
    n = len(A)
    M = [[F(x) for x in A[i]] + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return [row[n:] for row in M]


def q_factor(P, G, v):
    Pv = [sum(P[k][i] * v[i] for i in range(len(v)) if v[i]) for k in range(len(P))]
    p0 = [P[k][0] for k in range(len(P))]
    r = len(P)
    return sum(Pv[a] * G[a][b] * Pv[b] for a in range(r) for b in range(r)) + \
        sum(Pv[a] * G[a][b] * p0[b] for a in range(r) for b in range(r))


def q_stored(Y, v):
    YF = [[F(float(a)) for a in row] for row in Y]
    N = len(v); nz = [i for i in range(N) if v[i]]
    return sum(F(v[i]) * YF[i][j] * v[j] for i in nz for j in nz) + sum(F(v[i]) * YF[i][0] for i in nz)


def lll(rows, delta=None):
    m = DomainMatrix([[ZZ(int(a)) for a in row] for row in rows], (len(rows), len(rows[0])), ZZ)
    return [[int(a) for a in row] for row in m.lll(delta=QQ(99, 100)).to_list()]


out = open(ROOT / 'reviews/r2-logs/r2_nonroot.jsonl', 'w')
for line in open(ROOT / 'logs/thm3_r1.jsonl'):
    d = json.loads(line); f = d['file']
    if f.endswith('root.npz') or d['thm3']['v'] is None or (only and f not in only):
        continue
    t0 = time.time()
    t = d['thm3']; r = d['rank']
    n = f.split('_n')[1].split('_')[0]
    Y = np.load(ROOT / f'data/points_{"BT" if f.startswith("bt") else "DM"}{n}/{f}')['Y']
    Y = (Y + Y.T) / 2
    N = Y.shape[0]
    P, G, eig = neighbour(Y, r)
    v = t['v']
    q_mine = q_factor(P, G, v)
    match = q_mine == F(t['q_exact'])
    # integer kernel of P: P = content * M
    den = 1
    for row in P:
        for x in row:
            den = den * x.denominator // math.gcd(den, x.denominator)
    M = [[int(x * den) for x in row] for row in P]
    g = 0
    for row in M:
        for x in row:
            g = math.gcd(g, x)
    M = [[x // g for x in row] for row in M]
    W = 10**40
    emb = lll([[int(i == j) for j in range(N)] + [W * M[k][i] for k in range(r)] for i in range(N)])
    kern = [row[:N] for row in emb if not any(row[N:])]
    assert len(kern) == N - r, (len(kern), N - r)
    assert all(sum(M[k][i] * row[i] for i in range(N)) == 0 for row in kern for k in range(r))
    gram = DomainMatrix([[ZZ(sum(a * b for a, b in zip(x, y))) for y in kern] for x in kern], (len(kern), len(kern)), ZZ)
    covol = math.sqrt(float(gram.det()))
    gh = math.sqrt(len(kern) / (2 * math.pi * math.e)) * covol ** (1 / len(kern))
    # shorten the logged representative within its kernel coset
    best = list(v)
    for scale in (1, 2, 4, 8, 16):
        red = lll([row + [0] for row in kern] + [list(v) + [scale]])
        for row in red:
            if abs(row[-1]) == scale:
                cand = [a * (row[-1] // scale) for a in row[:N]]
                if sum(a * a for a in cand) < sum(a * a for a in best):
                    best = cand
    assert all(sum(M[k][i] * (best[i] - v[i]) for i in range(N)) == 0 for k in range(r))
    q_best_nb = q_factor(P, G, best)
    assert q_best_nb == q_mine
    qY_logged = q_stored(Y, v); qY_best = q_stored(Y, best)
    # Gram-Schmidt profile of the reduced kernel basis and a rigorous lower bound on
    # the norm of every coset member: project orthogonally to the first d-1 basis
    # vectors; the image is the 1-D lattice spanned by b*_d.
    kred = lll(kern)
    bs, gs = [], []
    for row in kred:
        b = [F(a) for a in row]
        for bj, nj in zip(bs, gs):
            c = sum(x * y for x, y in zip(row, bj)) / nj
            b = [x - c * y for x, y in zip(b, bj)]
        bs.append(b); gs.append(sum(x * x for x in b))
    tproj = sum(F(a) * y for a, y in zip(v, bs[-1])) / gs[-1]
    frac = abs(tproj - round(tproj))
    lb2 = frac * frac * gs[-1]          # squared lower bound on ||v + k||^2
    lb_inf = math.sqrt(float(lb2) / N)  # implied lower bound on max |coefficient|
    # stored-point decomposition along top-r eigenvectors and the tail
    w, V = np.linalg.eigh(Y); order = np.argsort(w)[::-1]
    u = 2 * np.array(best, float); u[0] += 1
    proj = V.T @ u
    top = float(np.sum(w[order[:r]] * proj[order[:r]] ** 2))
    tail = float(np.sum(w[order[r:]] * proj[order[r:]] ** 2))
    rec = dict(file=f, rank=r, N=N, matches_logged_q=match, q_neighbour=str(q_mine),
               logged_vmax=max(map(abs, v)), logged_norm2=sum(a * a for a in v), logged_q_at_Y=float(qY_logged),
               kernel_dim=len(kern), kernel_covolume_log10=math.log10(covol), gaussian_heuristic=gh,
               gso_norms=[float(math.sqrt(x)) for x in gs[:2]] + ['...'] + [float(math.sqrt(x)) for x in gs[-3:]],
               coset_norm_lower_bound=math.sqrt(float(lb2)), coset_vmax_lower_bound=lb_inf,
               short_vmax=max(map(abs, best)), short_norm2=sum(a * a for a in best),
               short_support=sum(a != 0 for a in best[1:]), short_q_at_Y=float(qY_best),
               short_ratio_at_Y=float(-qY_best / sum(a * a for a in best[1:])),
               lambda_r=float(eig[r - 1]), lambda_r1=float(eig[r]), top_part=top / 4 - 0.25, tail_part=tail / 4,
               time=time.time() - t0)
    out.write(json.dumps(rec) + '\n'); out.flush()
    print(json.dumps(rec), flush=True)
