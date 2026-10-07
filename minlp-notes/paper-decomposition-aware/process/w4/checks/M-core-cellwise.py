"""M-core: exact checks of Prop prop:cellwise (a)-(c), Prop prop:filter and
Theorem thm:certificate (soundness of (C1)/(C2) with both alternatives) on
random nonconvex mixed-integer box QPs with n<=3; the exact global optimum is
computed by enumerating faces (free/lower/upper for continuous coordinates,
all values for integer coordinates).
usage: python3 M-core-cellwise.py SEED NINST"""
from fractions import Fraction as Fr
import itertools, random, sys, math

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NINST = int(sys.argv[2]) if len(sys.argv) > 2 else 100
rng = random.Random(seed)
fails = []
def check(c, msg):
    if not c:
        fails.append(msg)
        if len(fails) < 20:
            print("FAIL", msg)

def solve(A, b):
    n = len(A); M = [A[i][:] + [b[i]] for i in range(n)]
    for k in range(n):
        piv = next((r for r in range(k, n) if M[r][k] != 0), None)
        if piv is None:
            return None
        M[k], M[piv] = M[piv], M[k]
        for r in range(n):
            if r != k and M[r][k] != 0:
                f = M[r][k] / M[k][k]
                M[r] = [M[r][c] - f * M[k][c] for c in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]

def F(I, x):
    n = len(x)
    return sum(I['H'][i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2 + sum(I['b'][i] * x[i] for i in range(n))

def opt(I):
    n = I['n']; best = None
    choices = []
    for i in range(n):
        if I['int'][i]:
            choices.append([('fix', Fr(v)) for v in range(int(I['lo'][i]), int(I['hi'][i]) + 1)])
        else:
            choices.append([('fix', I['lo'][i]), ('fix', I['hi'][i]), ('free', None)])
    for ch in itertools.product(*choices):
        free = [i for i in range(n) if ch[i][0] == 'free']
        x = [ch[i][1] for i in range(n)]
        if free:
            A = [[I['H'][i][j] for j in free] for i in free]
            rhs = [-(I['b'][i] + sum(I['H'][i][k] * x[k] for k in range(n) if k not in free)) for i in free]
            sol = solve(A, rhs)
            if sol is None:
                continue
            ok = True
            for t, i in enumerate(free):
                if not (I['lo'][i] <= sol[t] <= I['hi'][i]):
                    ok = False
                x[i] = sol[t]
            if not ok:
                continue
        v = F(I, x)
        if best is None or v < best:
            best = v
    return best

def rand_grid(lo, hi, integer, k):
    pts = {lo, hi}
    for _ in range(k):
        if integer:
            pts.add(Fr(rng.randint(int(lo), int(hi))))
        else:
            pts.add(lo + (hi - lo) * Fr(rng.randint(0, 60), 60))
    return sorted(pts)

def eff(a, b, integer):
    return 0 if (integer and b - a == 1) else b - a

def stage(I, G):
    n = I['n']; L = I['L']
    w = []
    for i in range(n):
        wi = {v: Fr(0) for v in G[i]}
        for a, b in zip(G[i], G[i][1:]):
            e = eff(a, b, I['int'][i]); wi[a] = max(wi[a], e); wi[b] = max(wi[b], e)
        w.append(wi)
    d = [{v: L[i] * w[i][v] ** 2 / 8 for v in G[i]} for i in range(n)]
    Q = {}
    for y in itertools.product(*G):
        Q[y] = F(I, list(y)) - sum(d[i][y[i]] for i in range(n))
    beta = min(Q.values())
    mm = []
    for i in range(n):
        m = {}
        for y, val in Q.items():
            m[y[i]] = min(m.get(y[i], val), val)
        mm.append(m)
    ymin = min(Q, key=Q.get)
    return beta, mm, d, ymin

def rand_point(I, box):
    x = []
    for i in range(I['n']):
        lo, hi = box[i]
        if I['int'][i]:
            x.append(Fr(rng.randint(int(lo), int(hi))))
        else:
            x.append(lo + (hi - lo) * Fr(rng.randint(0, 997), 997))
    return x

for inst in range(NINST):
    n = rng.randint(1, 3)
    I = dict(n=n, int=[rng.random() < 0.4 for _ in range(n)])
    I['lo'] = [Fr(rng.randint(-3, 0)) for _ in range(n)]
    I['hi'] = [I['lo'][i] + (Fr(rng.randint(1, 6)) if I['int'][i] else Fr(rng.randint(1, 12), rng.choice([1, 2, 3]))) for i in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            H[i][j] = H[j][i] = Fr(rng.randint(-6, 6), rng.choice([1, 2]))
    I['H'] = H; I['b'] = [Fr(rng.randint(-6, 6), rng.choice([1, 2])) for _ in range(n)]
    I['L'] = [max(H[i][i], Fr(0)) for i in range(n)]
    OPT = opt(I)
    # one grid: cellwise checks
    box = [(I['lo'][i], I['hi'][i]) for i in range(n)]
    G = [rand_grid(box[i][0], box[i][1], I['int'][i], rng.randint(0, 5)) for i in range(n)]
    beta, mm, d, ymin = stage(I, G)
    check(beta <= OPT, "cellwise(b)")
    for _ in range(60):
        x = rand_point(I, box)
        Fx = F(I, x)
        for i in range(n):
            for a, b in zip(G[i], G[i][1:]):
                if a <= x[i] <= b:
                    check(Fx >= min(mm[i][a], mm[i][b]), "cellwise(c) interval")
                    wJ = eff(a, b, I['int'][i])
                    bi = min(mm[i][v] + d[i][v] for v in (a, b)) - I['L'][i] * wJ ** 2 / 8
                    check(Fx >= bi, "cellwise(c) beta_i")
            if x[i] in mm[i]:
                check(Fx >= mm[i][x[i]] + d[i][x[i]], "cellwise(c) node")
    # path certificates by repeated filtering with a feasible threshold, plus random
    # integer-node removals (second alternative of (C1))
    U = F(I, rand_point(I, box))
    grids = []
    cur = box
    for j in range(rng.randint(1, 4)):
        G = [rand_grid(cur[i][0], cur[i][1], I['int'][i], rng.randint(0, 6)) for i in range(n)]
        beta, mm, d, ymin = stage(I, G)
        U = min(U, F(I, list(ymin)))
        grids.append((G, mm, beta))
        new = []
        for i in range(n):
            ret = [(a, b) for a, b in zip(G[i], G[i][1:]) if min(mm[i][a], mm[i][b]) <= U]
            if len(G[i]) == 1:
                ret = [(G[i][0], G[i][0])]
            lo = min(a for a, _ in ret); hi = max(b for _, b in ret)
            new.append((lo, hi))
        cur = new
        check(all(cur[i][0] <= ymin[i] <= cur[i][1] for i in range(n)), "filter keeps corrected minimizer")
    G = [rand_grid(cur[i][0], cur[i][1], I['int'][i], rng.randint(0, 6)) for i in range(n)]
    betaK, mmK, dK, yK = stage(I, G)
    grids.append((G, mmK, betaK))
    # verify (C1)/(C2) with beta = betaK and soundness
    beta = betaK
    valid = True
    for j in range(len(grids) - 1):
        Gj, mmj, _ = grids[j]; Gn = grids[j + 1][0]
        for i in range(n):
            lo, hi = Gn[i][0], Gn[i][-1]
            ivs = list(zip(Gj[i], Gj[i][1:])) or [(Gj[i][0], Gj[i][0])]
            for a, b in ivs:
                if lo <= a and b <= hi:
                    continue
                alt1 = min(mmj[i][a], mmj[i][b]) >= beta
                alt2 = eff(a, b, I['int'][i]) == 0 and all(mmj[i][v] >= beta for v in (a, b) if not (lo <= v <= hi))
                if not (alt1 or alt2):
                    valid = False
    valid = valid and min(mmK[0].values()) >= beta if n else valid
    check(valid, "filtered record is a valid certificate")
    if valid:
        check(beta <= OPT, "certificate soundness")
print("failures:", len(fails))
print("ALL OK" if not fails else "SOME FAILURES")
