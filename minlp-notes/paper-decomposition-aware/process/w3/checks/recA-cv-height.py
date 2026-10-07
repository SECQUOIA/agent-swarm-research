"""recA check: Lemma lem:cv-height without uniqueness (2D, exact arithmetic).

For random integer QPs over bounded integer polygons (including singular and
indefinite Hessians with non-unique minimizers), compute OPT exactly by face
enumeration, pick a global minimizer with a maximal active set, and verify:
  * the saddle matrix of a maximal independent subset of its active rows is
    nonsingular (the key step of the proof);
  * x* = z/q with q = |det S| <= Lambda_0 = (2n' beta_H^2)^{n'};
  * OPT has reduced denominator <= 2 D_f Lambda_0^2, and divides 2 D_f q^2.
"""
from fractions import Fraction as Fr
import itertools, random

random.seed(7)

def det(M):
    n = len(M)
    if n == 0:
        return Fr(1)
    M = [row[:] for row in M]
    d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n):
                M[r][k] -= f * M[c][k]
    return d

def solve(M, b):
    n = len(M)
    A = [[Fr(x) for x in row] + [Fr(bb)] for row, bb in zip(M, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None:
            return None
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                for k in range(c, n + 1):
                    A[r][k] -= f * A[c][k]
    return [A[i][n] / A[i][i] for i in range(n)]

def rank(rows):
    rows = [[Fr(x) for x in r] for r in rows]
    rk, ncol = 0, len(rows[0]) if rows else 0
    for c in range(ncol):
        p = next((r for r in range(rk, len(rows)) if rows[r][c] != 0), None)
        if p is None:
            continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for r in range(len(rows)):
            if r != rk and rows[r][c] != 0:
                f = rows[r][c] / rows[rk][c]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[rk])]
        rk += 1
    return rk

def f(H, h, h0, Df, x):
    q = sum(Fr(H[i][j]) * x[i] * x[j] for i in range(2) for j in range(2)) / 2
    return (q + sum(h[i] * x[i] for i in range(2)) + h0) / Df

def feasible(A, a, x):
    return all(sum(A[s][j] * x[j] for j in range(2)) <= a[s] for s in range(len(A)))

def instance():
    H0 = random.choice([None, [[1, 1], [1, 1]], [[0, 0], [0, 0]], [[2, 0], [0, 0]],
                        [[1, -1], [-1, 1]], [[-2, 1], [1, 0]]])
    if H0 is None:
        a, b, c = (random.randint(-3, 3) for _ in range(3))
        H0 = [[a, b], [b, c]]
    A = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    a = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
    for _ in range(random.randint(0, 2)):
        A.append([random.randint(-3, 3), random.randint(-3, 3)])
        a.append(random.randint(-1, 4))
    h = [random.randint(-5, 5), random.randint(-5, 5)]
    if random.random() < 0.3:
        h = [0, 0]
    return H0, h, random.randint(-3, 3), random.randint(1, 3), A, a

def candidates(H, h, h0, Df, A, a):
    m = len(A)
    verts = set()
    for s, t in itertools.combinations(range(m), 2):
        x = solve([A[s], A[t]], [a[s], a[t]])
        if x is not None and feasible(A, a, x):
            verts.add(tuple(x))
    cands = set(verts)
    for s in range(m):
        on = [v for v in verts if sum(A[s][j] * v[j] for j in range(2)) == a[s]]
        if len(on) < 2:
            continue
        on.sort()
        p, q = on[0], on[-1]
        d = [q[0] - p[0], q[1] - p[1]]
        quad = sum(Fr(H[i][j]) * d[i] * d[j] for i in range(2) for j in range(2)) / 2
        g = [sum(Fr(H[i][j]) * p[j] for j in range(2)) + h[i] for i in range(2)]
        lin = g[0] * d[0] + g[1] * d[1]
        if quad > 0:
            t = -lin / (2 * quad)
            if 0 < t < 1:
                cands.add((p[0] + t * d[0], p[1] + t * d[1]))
    if det([[Fr(x) for x in r] for r in H]) != 0:
        x = solve(H, [-hh for hh in h])
        if feasible(A, a, x):
            cands.add(tuple(x))
    return verts, cands

checked = degenerate = 0
for trial in range(4000):
    H, h, h0, Df, A, a = instance()
    verts, cands = candidates(H, h, h0, Df, A, a)
    if len(verts) < 3:
        continue
    vals = {x: f(H, h, h0, Df, x) for x in cands}
    OPT = min(vals.values())
    mins = [x for x in cands if vals[x] == OPT]
    if len(mins) > 1:
        degenerate += 1
    act = lambda x: [s for s in range(len(A)) if sum(A[s][j] * x[j] for j in range(2)) == a[s]]
    xs = max(mins, key=lambda x: len(act(x)))
    E = act(xs)
    Ep = []
    for s in E:
        if rank([A[t] for t in Ep + [s]]) == len(Ep) + 1:
            Ep.append(s)
    k = len(Ep)
    S = [[Fr(H[i][j]) for j in range(2)] + [Fr(A[s][i]) for s in Ep] for i in range(2)]
    S += [[Fr(A[s][j]) for j in range(2)] + [Fr(0)] * k for s in Ep]
    dS = det(S)
    assert dS != 0, (H, h, A, a, xs, E)
    sol = solve(S, [-hh for hh in h] + [a[s] for s in Ep])
    assert tuple(sol[:2]) == xs
    beta = max([1] + [abs(x) for r in H for x in r] + [abs(x) for r in A for x in r])
    Lam0 = (2 * 2 * beta ** 2) ** 2
    q = abs(dS)
    assert q <= Lam0 and all((q * c).denominator == 1 for c in xs)
    assert OPT.denominator <= 2 * Df * Lam0 ** 2
    assert (2 * Df * q * q) % OPT.denominator == 0
    checked += 1
print(f"checked {checked} instances, {degenerate} with several minimizers: PASS")
