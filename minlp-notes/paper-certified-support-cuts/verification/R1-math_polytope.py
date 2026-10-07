"""R1-math: Theorem 5.1 candidate enumeration vs brute force; Appendix A.1 size bound."""
from fractions import Fraction as Fr
import itertools, random, math
import sympy as sp
random.seed(11)

def solve_exact(M, rhs):
    Ms = sp.Matrix(M); 
    if Ms.det() == 0: return None
    return list(Ms.LUsolve(sp.Matrix(rhs)))

def candidates(H, c, A, b, d, indep_only=False):
    out = []
    m = len(A)
    for kk in range(0, d+1):
        for S in itertools.combinations(range(m), kk):
            AS = [A[i] for i in S]
            K = [[H[i][j] for j in range(d)] + [AS[r][i] for r in range(kk)] for i in range(d)] + \
                [[AS[r][j] for j in range(d)] + [0]*kk for r in range(kk)]
            rhs = [-ci for ci in c] + [b[i] for i in S]
            sol = solve_exact(K, rhs)
            if sol is None: continue
            x = sol[:d]
            if all(sum(A[i][j]*x[j] for j in range(d)) <= b[i] for i in range(m)):
                out.append((x, S))
    return out

def q(H, c, x):
    d = len(x)
    return sp.Rational(1,2)*sum(x[i]*H[i][j]*x[j] for i in range(d) for j in range(d)) + sum(c[i]*x[i] for i in range(d))

bad = 0; tot = 0
for trial in range(60):
    d = random.choice([2, 2, 3])
    H = [[0]*d for _ in range(d)]
    for i in range(d):
        for j in range(i, d):
            H[i][j] = H[j][i] = random.randint(-4, 4)
    c = [random.randint(-4, 4) for _ in range(d)]
    A = []; b = []
    for i in range(d):
        e = [0]*d; e[i] = 1; A.append(e); b.append(1)
        e = [0]*d; e[i] = -1; A.append(e); b.append(0)
    for _ in range(random.randint(0, 2)):
        A.append([random.randint(-2, 2) for _ in range(d)]); b.append(random.randint(0, 2))
    if random.random() < 0.3:  # an implied equality via two rows
        row = [random.randint(-2, 2) for _ in range(d)]
        if any(row):
            rhs = sum(row)//2 if d == 2 else 0
            A.append(row); b.append(Fr(sum(abs(v) for v in row if v > 0), 2))
            A.append([-v for v in row]); b.append(-Fr(sum(abs(v) for v in row if v > 0), 2))
    cands = candidates(H, c, A, b, d)
    # brute force: grid of feasible points + edges
    N = 24 if d == 2 else 10
    gridmin = None
    for pt in itertools.product(range(N+1), repeat=d):
        x = [Fr(p, N) for p in pt]
        if all(sum(A[i][j]*x[j] for j in range(d)) <= b[i] for i in range(len(A))):
            v = q(H, c, x)
            gridmin = v if gridmin is None or v < gridmin else gridmin
    tot += 1
    if not cands:
        if gridmin is not None: bad += 1; print("no candidates but feasible grid point")
        continue
    cmin = min(q(H, c, x) for x, S in cands)
    if gridmin is not None and cmin > gridmin: bad += 1; print("candidate min above a feasible value!", cmin, gridmin)
print("Theorem 5.1 instances:", tot, " failures:", bad)

# Hadamard bound check of Appendix A.1 on integer data
viol = 0
for trial in range(200):
    d = random.randint(1, 3); kk = random.randint(0, d)
    eta = random.randint(1, 4); alpha = random.randint(1, 4)
    H = [[random.randint(-2**eta, 2**eta) for _ in range(d)] for _ in range(d)]
    H = [[H[i][j] if i <= j else H[j][i] for j in range(d)] for i in range(d)]
    cc = [random.randint(-2**eta, 2**eta) for _ in range(d)]
    AS = [[random.randint(-2**alpha, 2**alpha) for _ in range(d)] for _ in range(kk)]
    bS = [random.randint(-2**alpha, 2**alpha) for _ in range(kk)]
    n = d + kk
    aug = [H[i] + [AS[r][i] for r in range(kk)] + [-cc[i]] for i in range(d)] + [AS[r] + [0]*kk + [bS[r]] for r in range(kk)]
    B = (2*d)**d * 2**(d*(eta + 2*alpha))
    Ms = sp.Matrix(aug)
    for s in range(1, n+1):
        for rows in itertools.combinations(range(n), s):
            for cols in itertools.combinations(range(n+1), s):
                if abs(Ms.extract(list(rows), list(cols)).det()) > B: viol += 1
print("Appendix A.1 Hadamard bound violations:", viol)
