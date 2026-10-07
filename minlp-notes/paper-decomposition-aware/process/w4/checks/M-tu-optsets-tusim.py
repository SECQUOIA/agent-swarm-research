"""Exact simulation of TU-GRID (union and hull variants) and TU-EXACT on a
mixed-integer instance with an integer column in the coupling row.

X = {(x1,x2,z): x in [0,2]^2, z in {0,1,2}, x1 - x2 + z <= 1}, eta = 1.
F = x1^2 + x2^2 - x1 x2 - c1 x1 - z x2 + z^2/2 + c0 z  (PD in x).
Checks: prop:tu-sound (b),(d),(e) (beta_j <= OPT <= U_j <= OPT+E_j, S in D^(j)),
lem:tu-snap whenever its distance hypothesis holds, thm:tu-exact (a),(b).
"""
from fractions import Fraction as Fr
import itertools, math

def solve(Aeq, beq):
    # exact Gaussian elimination; returns unique solution or None (inconsistent) or 'many'
    rows = [list(a) + [b] for a, b in zip(Aeq, beq)]
    n = len(Aeq[0])
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    for i in range(r, len(rows)):
        if rows[i][-1] != 0: return None
    if r < n: return 'many'
    x = [Fr(0)] * n
    for i, c in enumerate(piv):
        x[c] = rows[i][-1] / rows[i][c]
    return x

def kernel(Ar, n):
    if not Ar: return [[Fr(int(i == k)) for i in range(n)] for k in range(n)]
    # basis of null space of Ar (exact)
    rows = [list(a) for a in Ar]
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [a / rows[r][c] for a in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * n; v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -rows[i][f]
        basis.append(v)
    return basis

def run(c1, c0, hull):
    ok = True
    Zs = [0, 1, 2]
    lo, hi = Fr(0), Fr(2)
    F = lambda x1, x2, z: x1 * x1 + x2 * x2 - x1 * x2 - c1 * x1 - z * x2 + Fr(z * z, 2) + c0 * z
    feas = lambda x1, x2, z: lo <= x1 <= hi and lo <= x2 <= hi and x1 - x2 + z <= 1
    # Ahat rows: A row, x<=u, -x<=-l
    Ahat = [[1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]
    bhat = lambda z: [Fr(1 - z), hi, hi, -lo, -lo]
    # exact OPT per z: strictly convex in x -> enumerate active sets
    cands = []
    for z in Zs:
        grad = lambda x: [2 * x[0] - x[1] - c1, 2 * x[1] - x[0] - z]
        for k in range(0, 3):
            for act in itertools.combinations(range(5), k):
                Aa = [Ahat[r] for r in act]
                ba = [bhat(z)[r] for r in act]
                Xi = kernel([[Fr(a) for a in row] for row in Aa], 2)
                # stationarity on kernel: Xi^T (Hx - g0) = 0 with H=[[2,-1],[-1,2]], g0=(c1,z)
                eqA = [[Fr(a) for a in row] for row in Aa] + [[2 * v[0] - v[1], -v[0] + 2 * v[1]] for v in Xi]
                eqb = ba + [v[0] * c1 + v[1] * z for v in Xi]
                x = solve(eqA, eqb)
                if x is None or x == 'many': continue
                if feas(x[0], x[1], z):
                    cands.append((F(x[0], x[1], z), (x[0], x[1], z)))
    OPT = min(c[0] for c in cands)
    S = sorted({c[1] for c in cands if c[0] == OPT})
    # Ghat constants: Delta clears 1,1,-1,c1,1,1/2,c0 (z coefficient), F(0)=0
    Delta = 1
    for q in (Fr(1), Fr(-1), c1, Fr(1, 2), c0):
        Delta = Delta * q.denominator // math.gcd(Delta, q.denominator)
    Hhat = [[Delta * 2, -Delta], [-Delta, Delta * 2]]
    C = max(1, max(abs(a) for r in Hhat for a in r))
    nc = 2
    R = (2 * nc * C) ** nc
    Omega = Delta * R * R
    mprime = 5
    tau = Fr(1, 4 * mprime * R)
    Lbar = Fr(3)
    D = {0: (lo, hi), 1: (lo, hi)}
    Dsets = [[(lo, hi)], [(lo, hi)]]
    Lam = set(Zs)
    returned = None
    snaps = 0
    for j in range(0, 22):
        h = Fr(1, 2 ** j)
        E = nc * Lbar * h * h / 8
        nodes = []
        for i in range(2):
            ns = set()
            for (a, b) in Dsets[i]:
                k = a / h
                while a + 0 <= hi and k * h <= b:
                    ns.add(k * h); k += 1
            nodes.append(sorted(ns))
        pts = [(x1, x2, z) for x1 in nodes[0] for x2 in nodes[1] for z in sorted(Lam) if feas(x1, x2, z)]
        vals = {p: F(*p) for p in pts}
        mu = min(vals.values())
        y = min(vals, key=vals.get)
        U, beta = mu, mu - E
        if not (beta <= OPT <= U <= OPT + E):
            print("FAIL bounds at level", j); ok = False
        for s in S:
            ins = all(any(a <= s[i] <= b for (a, b) in Dsets[i]) for i in range(2)) and s[2] in Lam
            if not ins:
                print("FAIL S not in D at", j); ok = False
        # TU-EXACT steps (i)-(iii) at y
        yz = y[2]
        bz = bhat(yz)
        Jrows = [r for r in range(5) if bz[r] - (Ahat[r][0] * y[0] + Ahat[r][1] * y[1]) <= tau]
        AJ = [[Fr(a) for a in Ahat[r]] for r in Jrows]
        Xi = kernel(AJ, 2)
        eqA = AJ + [[2 * v[0] - v[1], -v[0] + 2 * v[1]] for v in Xi]
        eqb = [bz[r] for r in Jrows] + [v[0] * c1 + v[1] * yz for v in Xi]
        xh = solve(eqA, eqb)
        dist = min(math.sqrt(float((y[0] - s[0]) ** 2 + (y[1] - s[1]) ** 2 + (y[2] - s[2]) ** 2)) for s in S)
        if dist <= float(tau) / (2 * math.sqrt(nc)):
            snaps += 1
            if xh is None or xh == 'many' or not feas(xh[0], xh[1], yz) or F(xh[0], xh[1], yz) != OPT:
                print("FAIL snap lemma at level", j, xh); ok = False
        if xh is not None and xh != 'many' and feas(xh[0], xh[1], yz) and returned is None:
            val = F(xh[0], xh[1], yz)
            W = val.denominator
            if val - beta < Fr(1, Omega * W):
                returned = (j, (xh[0], xh[1], yz), val)
                if val != OPT:
                    print("FAIL returned nonoptimal"); ok = False
        # filter (min-marginals in one pass)
        mm = [{}, {}, {}]
        for p, v in vals.items():
            for i in range(3):
                if p[i] not in mm[i] or v < mm[i][p[i]]:
                    mm[i][p[i]] = v
        def m_coord(i, t):
            return (mm[i][t] - E) if t in mm[i] else None
        newD = []
        for i in range(2):
            keep = []
            for (a, b) in Dsets[i]:
                if a == b:
                    mv = m_coord(i, a)
                    if mv is not None and mv <= U: keep.append((a, a))
                    continue
                k = a / h
                while k * h + h <= b:
                    t = k * h
                    ms = [m for m in (m_coord(i, t), m_coord(i, t + h)) if m is not None]
                    if ms and min(ms) <= U: keep.append((t, t + h))
                    k += 1
            # merge
            keep.sort()
            merged = []
            for (a, b) in keep:
                if merged and a <= merged[-1][1]:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], b))
                else:
                    merged.append((a, b))
            if hull:
                merged = [(merged[0][0], merged[-1][1])]
            newD.append(merged)
        Dsets = newD
        Lam = {t for t in Lam if t in mm[2] and mm[2][t] - E <= U}
        maxn = max(len(nodes[0]), len(nodes[1]))
        if j == 21:
            print("   level 21 nodes per coordinate:", len(nodes[0]), len(nodes[1]), "values:", sorted(Lam))
    return ok, OPT, S, returned, snaps

allok = True
for c1, c0 in ((Fr(1, 3), Fr(-1, 5)), (Fr(2), Fr(0)), (Fr(5, 7), Fr(1, 4)), (Fr(1), Fr(-1, 2))):
    for hull in (False, True):
        ok, OPT, S, ret, snaps = run(c1, c0, hull)
        allok = allok and ok  # early return is not required: the guaranteed level is far larger
        print("c1=%s c0=%s hull=%d: OPT=%s S=%s returned=%s snap-levels=%d ok=%s"
              % (c1, c0, hull, OPT, [tuple(str(a) for a in s) for s in S], ret and (ret[0], tuple(str(a) for a in ret[1])), snaps, ok))
print("ALL PASS" if allok else "SOME FAIL")
