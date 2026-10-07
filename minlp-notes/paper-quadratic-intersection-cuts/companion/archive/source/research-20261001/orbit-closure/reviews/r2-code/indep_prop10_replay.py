"""Review r2: independent exact replay of the 60 saved Proposition 10 cuts.

Imports no stream code. Reads logs/revision-r1/closure_lower_prop16_cuts.json and
  1. rebuilds the corner of sfree Proposition 16 from the note's numbers (not from the file)
     and checks that the file's instance is the same;
  2. for every cut i: X_i has sym(X_i) positive definite (so det X_i > 0, det F > 0, and sbar is
     interior to C_F), and sym(X_i (I + mu_ij N_j)) is PSD, so sbar + mu_ij p_j lies in C_F and
     alpha_j >= mu_ij (convexity), hence a_j <= 1/mu_ij;
  3. solves min{1^T lam : lam >= 0, sum_j lam_j / mu_ij >= 1} exactly by its own enumeration of
     all basic solutions, then gives an exact dual vector y >= 0 on tight rows with G^T y <= 1 and
     1^T y = value. The dual alone proves the lower bound: 1^T lam >= y^T G lam >= 1^T y for every
     feasible lam. (A floating HiGHS solve was tried first; it returns a point infeasible by 3e-8,
     so it was not used.)
  4. compares with the saved value and lam, and with the note's bounds 0.9953611 and 0.9839.
"""
import json
import sys
from fractions import Fraction as Fr
from itertools import combinations


path = sys.argv[1]
d = json.load(open(path))

# corner of sfree Proposition 16 as written in note Section 5
sb = [Fr(-2), Fr(3), Fr(2)]
V = [[Fr(0), Fr(0), Fr(0)], [Fr(6), Fr(-2), Fr(1, 4)], [Fr(1), Fr(-5, 2), Fr(1, 2)]]
P = [[V[j][i] - sb[i] for i in range(3)] for j in range(3)]
ok = True


def check(msg, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)


inst = d['instance']
check('file instance equals the note corner',
      [Fr(x) for x in inst['sbar']] == sb and [[Fr(x) for x in r] for r in inst['verts']] == V)


def mul(A, B):
    return [[A[i][0] * B[0][k] + A[i][1] * B[1][k] for k in range(2)] for i in range(2)]


def symm(A):
    return [[A[0][0], (A[0][1] + A[1][0]) / 2], [(A[0][1] + A[1][0]) / 2, A[1][1]]]


# M(s) = [[w, x], [y, 1]], M0(p) = [[p_w, p_x], [p_y, 0]]
M = [[sb[2], sb[0]], [sb[1], Fr(1)]]
dm = M[0][0] * M[1][1] - M[0][1] * M[1][0]
check('q(sbar) = det M(sbar) = %s > 0' % dm, dm > 0)
Minv = [[M[1][1] / dm, -M[0][1] / dm], [-M[1][0] / dm, M[0][0] / dm]]
Nj = [mul(Minv, [[p[2], p[0]], [p[1], Fr(0)]]) for p in P]


def is_pd(S):
    return S[0][0] > 0 and S[0][0] * S[1][1] - S[0][1] ** 2 > 0


def is_psd(S):
    return S[0][0] >= 0 and S[1][1] >= 0 and S[0][0] * S[1][1] - S[0][1] ** 2 >= 0


cuts = d['cuts']
check('60 saved cuts', len(cuts) == 60)
G = []
nfail = 0
for rec in cuts:
    X = [[Fr(v) for v in row] for row in rec['X']]
    mus = [Fr(v) for v in rec['mu']]
    good = len(mus) == 3 and is_pd(symm(X))
    for j in range(3):
        good &= mus[j] > 0
        A = symm(mul(X, [[(1 if r == k else 0) + mus[j] * Nj[j][r][k] for k in range(2)] for r in range(2)]))
        good &= is_psd(A)
    nfail += not good
    G.append([1 / mu for mu in mus])
check('every cut: sym(X) PD and every step certified (%d failures)' % nfail, nfail == 0)

# exact LP by my own enumeration of all basic solutions (63 constraints incl. lam_k >= 0)
def det3(B):
    return (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1]) - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
            + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0]))


def solve3(A, b):
    D = det3(A)
    if D == 0:
        return None
    out = []
    for c in range(3):
        B = [[(b[r] if k == c else A[r][k]) for k in range(3)] for r in range(3)]
        out.append(det3(B) / D)
    return out


rows = [(g, Fr(1)) for g in G] + [([Fr(1) if k == j else Fr(0) for k in range(3)], Fr(0)) for j in range(3)]
best = None
nvert = 0
for trip in combinations(range(len(rows)), 3):
    lamc = solve3([rows[i][0] for i in trip], [rows[i][1] for i in trip])
    if lamc is None or any(x < 0 for x in lamc):
        continue
    if any(sum(g[k] * lamc[k] for k in range(3)) < 1 for g in G):
        continue
    nvert += 1
    v = sum(lamc)
    if best is None or v < best[0]:
        best = (v, lamc)
val, lam = best
print('feasible basic solutions: %d; exact minimum %s ~ %.12f at lam ~ %s' % (nvert, val, float(val), [float(x) for x in lam]))
# dual certificate on the tight rows: find y >= 0 on three tight rows with A^T y = 1
tight = [i for i in range(len(G)) if sum(G[i][k] * lam[k] for k in range(3)) == 1]
print('tight cut rows at the minimizer:', tight)
dual = None
for trip in combinations(tight, 3):
    At = [[G[trip[r]][c] for r in range(3)] for c in range(3)]
    y = solve3(At, [Fr(1)] * 3)
    if y is not None and all(v >= 0 for v in y):
        dual = (trip, y)
        break
check('nonnegative exact dual on three tight rows exists', dual is not None)
trip, y = dual
colsum = [sum(y[t] * G[trip[t]][k] for t in range(3)) for k in range(3)]
check('dual feasible (y >= 0, G^T y <= 1)', all(v >= 0 for v in y) and all(c <= 1 for c in colsum))
check('dual value 1^T y = primal value', sum(y) == val)
print('dual rows %s, y ~ %s' % (list(trip), [float(v) for v in y]))
check('value equals the saved value', val == Fr(d['value']))
check('minimizer equals the saved lam', lam == [Fr(v) for v in d['lam']])
check('0.9953611 <= value < 0.9953612 (note: bound written 0.9953611)', Fr('0.9953611') <= val < Fr('0.9953612'))
check('value > 9839/10000 (single-cut upper bound)', val > Fr(9839, 10000))
check('value <= 999/1000 (closure upper bound of Proposition 10)', val <= Fr(999, 1000))
print('ALL PASS' if ok else 'SOME CHECK FAILED')
sys.exit(0 if ok else 1)
