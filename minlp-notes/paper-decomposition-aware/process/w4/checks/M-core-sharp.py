"""M-core: exact checks of Prop prop:sharp, Cor cor:uniformgrid (uniform and
graded rules), Example ex:family (a)-(c) and Example ex:chain constants.
usage: python3 M-core-sharp.py SEED"""
from fractions import Fraction as Fr
import math, random, sys, itertools

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rng = random.Random(seed)
fails = []
counts = {}
def cnt(k): counts[k]=counts.get(k,0)+1
def check(c, msg):
    if not c:
        fails.append(msg)
        if len(fails) < 20:
            print("FAIL", msg)

def widths(G):
    w = {v: Fr(0) for v in G}
    for a, b in zip(G, G[1:]):
        w[a] = max(w[a], b - a); w[b] = max(w[b], b - a)
    return w

# ---------------- Prop sharp on random grids
for trial in range(300):
    m = rng.randint(1, 4); n = 2 * m
    Lam = Fr(rng.randint(1, 40), rng.randint(1, 5))
    g = Lam / 2 * Fr(rng.randint(1, 100), 100)
    kap = Lam / g
    lo = [-Fr(rng.randint(1, 20), 20) for _ in range(n)]
    hi = [Fr(rng.randint(1, 20), 20) for _ in range(n)]
    rho = min(min(-l for l in lo), min(hi))
    G = []
    for i in range(n):
        pts = {lo[i], hi[i], Fr(0)}
        for _ in range(rng.randint(0, 25)):
            pts.add(lo[i] + (hi[i] - lo[i]) * Fr(rng.randint(0, 400), 400))
        G.append(sorted(pts))
    W = [widths(Gi) for Gi in G]
    h = min(W[i][Fr(0)] for i in range(n))
    def Qk(k, u, v):
        return Lam / 2 * (u * u + v * v) + (Lam - 2 * g) * u * v - Lam / 8 * (W[2 * k][u] ** 2 + W[2 * k + 1][v] ** 2)
    minQ = [min(Qk(k, u, v) for u in G[2 * k] for v in G[2 * k + 1]) for k in range(m)]
    tot = sum(minQ)
    for k in range(m):
        for which in (0, 1):
            i = 2 * k + which
            for a in G[i]:
                if a * a <= rho * rho and a * a <= h * h * (n - 2) * kap / 16:
                    if which == 0:
                        mm = min(Qk(k, a, v) for v in G[2 * k + 1])
                    else:
                        mm = min(Qk(k, u, a) for u in G[2 * k])
                    mm += tot - minQ[k]
                    counts["sharp"]=counts.get("sharp",0)+1
                    check(mm <= 0, "sharp m_i(a)<=0: n=%d kap=%s a=%s" % (n, kap, a))

# ---------------- Cor uniformgrid: simulate TRIAL stages, common mesh, center 0
def grid_graded(lo, hi, c, h, th):
    nodes = {c}
    for sgn, end in [(1, hi - c), (-1, c - lo)]:
        t = Fr(0)
        while t < end:
            t = min(t + h + th * t, end)
            nodes.add(c + sgn * t)
    return sorted(nodes)

def simulate(n, Lam, g, th, stages, center0=True):
    m = n // 2; kap = Lam / g
    box = [(Fr(-1), Fr(1))] * n
    c = [Fr(0)] * n
    U = Fr(0) if center0 else None
    out = []
    for j in range(stages):
        h = Fr(2) / 2 ** j
        G = [grid_graded(box[i][0], box[i][1], c[i], h, th) for i in range(n)]
        W = [widths(Gi) for Gi in G]
        def Qk(k, u, v):
            return Lam / 2 * (u * u + v * v) + (Lam - 2 * g) * u * v - Lam / 8 * (W[2 * k][u] ** 2 + W[2 * k + 1][v] ** 2)
        best = []
        for k in range(m):
            vals = {(u, v): Qk(k, u, v) for u in G[2 * k] for v in G[2 * k + 1]}
            mn = min(vals.values()); best.append((mn, [uv for uv, val in vals.items() if val == mn], vals))
        tot = sum(b[0] for b in best)
        y = []
        for k in range(m):
            y.extend(best[k][1][0])
        Fy = sum(Lam / 2 * (y[2 * k] ** 2 + y[2 * k + 1] ** 2) + (Lam - 2 * g) * y[2 * k] * y[2 * k + 1] for k in range(m))
        U = Fy if U is None else min(U, Fy)
        # min-marginals
        newbox = []
        for i in range(n):
            k, wh = divmod(i, 2)
            vals = best[k][2]
            mm = {}
            for (u, v), val in vals.items():
                key = u if wh == 0 else v
                mm[key] = min(mm.get(key, val), val)
            mm = {a: val + tot - best[k][0] for a, val in mm.items()}
            ret = [(a, b) for a, b in zip(G[i], G[i][1:]) if min(mm[a], mm[b]) <= U]
            newbox.append((min(a for a, _ in ret), max(b for _, b in ret)))
        out.append(dict(j=j, G=G, y=y, box=box, newbox=newbox, uniq=[len(b[1]) for b in best], W=W, beta=tot, U=U))
        box = newbox; c = y
    return out

for (n, kapint) in [(4, 2), (4, 9), (4, 37), (6, 5), (6, 50), (8, 17), (4, 200), (6, 2)]:
    Lam = Fr(kapint); g = Fr(1); kap = Lam / g
    nu = math.isqrt(int((n - 2) * kapint // 16)) if False else int(math.floor(math.sqrt((n - 2) * kapint / 16)))
    # exact floor of sqrt((n-2)kap/16)
    nu = max(t for t in range(0, 1000) if t * t * 16 <= (n - 2) * kapint)
    out = simulate(n, Lam, g, Fr(0), 9)
    for st in out:
        j = st['j']; h = Fr(2) / 2 ** j
        check(all(v == 0 for v in st['y']) and all(u == 1 for u in st['uniq']), "uniform: corrected minimizer 0 unique (n=%d kap=%d j=%d)" % (n, kapint, j))
        if j >= 1 and (nu + 1) * h <= 1:
            R = (nu + 1) * h
            check(all(nb[0] <= -R and nb[1] >= R for nb in st['newbox']), "uniform: filtered box (n=%d kap=%d j=%d)" % (n, kapint, j))
            if j + 1 < len(out):
                cnt = min(len(Gi) for Gi in out[j + 1]['G'])
                counts["uniform-count"]=counts.get("uniform-count",0)+1
                check(cnt >= 4 * nu + 5, "uniform: nodes %d < 4nu+5=%d" % (cnt, 4 * nu + 5))
                check((4 * nu + 4) ** 2 >= (n - 2) * kapint, "4nu+5 >= sqrt((n-2)kappa)+1")
    # graded rule
    for th in [Fr(1, 4), Fr(1, 8), Fr(1, 16)]:
        out = simulate(n, Lam, g, th, 8)
        for st in out[:-1]:
            j = st['j']; h = Fr(2) / 2 ** j
            R2 = h * h * (n - 2) * kap / 16   # R^2
            hyp = all(-b[0] >= 0 and b[0] ** 2 >= R2 and b[1] ** 2 >= R2 for b in st['box']) and \
                all(Fr(0) in Gi for Gi in st['G']) and all(st['W'][i][Fr(0)] >= h for i in range(n))
            if hyp and st['U'] - st['beta'] > 0:
                R = math.sqrt(float(R2))
                lb = 1 + math.log(1 + 2 * float(th) * R / float(h)) / math.log(1 + float(th))
                cnt = min(len(Gi) for Gi in out[j + 1]['G'])
                cnt_ = None; counts["graded-lb"]=counts.get("graded-lb",0)+1
                check(cnt + 1e-9 >= lb, "graded lower bound n=%d kap=%d th=%s j=%d cnt=%d lb=%.2f" % (n, kapint, th, j, cnt, lb))
                check(all(nb[0] ** 2 >= R2 and nb[1] ** 2 >= R2 and nb[0] <= 0 <= nb[1] for nb in st['newbox']), "graded: filtered box contains [-R,R]")

# ---------------- Example ex:family
def fam_F(blocks, edges, Delta, x):
    val = Fr(0)
    for b in range(blocks):
        u, v, r = x[3 * b:3 * b + 3]
        val += u * u + v * v - 4 * u * v + (u + v) / 4 + (r - u / 2) ** 2
    for (b, c) in edges:
        val += (x[3 * b] - x[3 * c]) ** 2 / (16 * Delta)
    return val

for (blocks, edges) in [(2, [(0, 1)]), (3, [(0, 1), (1, 2)]), (4, [(0, 1), (1, 2), (2, 3), (3, 0)]), (3, [(0, 1), (0, 2)])]:
    deg = [0] * blocks
    for b, c in edges:
        deg[b] += 1; deg[c] += 1
    Delta = max(deg)
    xstar = []
    for b in range(blocks):
        xstar += [Fr(1), Fr(1), Fr(1, 2)]
    Fs = fam_F(blocks, edges, Delta, xstar)
    check(Fs == Fr(-3, 2) * blocks, "family OPT")
    for _ in range(3000):
        x = [Fr(rng.randint(0, 24), 24) for _ in range(3 * blocks)]
        d2 = sum((x[i] - xstar[i]) ** 2 for i in range(3 * blocks))
        check(fam_F(blocks, edges, Delta, x) - Fs >= d2 / 2, "family (a)")
    # (b) diagonal entries
    for b in range(blocks):
        check(Fr(5, 2) + Fr(2 * deg[b], 16 * Delta) <= Fr(21, 8), "family (b)")
    # (a) 9/8 per block at (0,0,0)
    for pattern in itertools.product([0, 1], repeat=blocks):
        xb = []
        for b in range(blocks):
            xb += [Fr(0), Fr(0), Fr(0)] if pattern[b] == 0 else [Fr(1), Fr(1), Fr(1, 2)]
        Fb = fam_F(blocks, edges, Delta, xb)
        check(Fb - Fs >= Fr(9, 8) * pattern.count(0), "family 9/8")
        # (c) strict local min: random small feasible perturbations
        for _ in range(400):
            d = []
            for b in range(blocks):
                for t in range(3):
                    base = xb[3 * b + t]
                    step = Fr(rng.randint(0, 40), 4000)
                    if t == 2:
                        step = Fr(rng.randint(-40, 40), 4000)
                        if base == 0:
                            step = abs(step)
                    elif base == 1:
                        step = -step
                    d.append(step)
            if all(t == 0 for t in d):
                continue
            x = [xb[i] + d[i] for i in range(3 * blocks)]
            delta = sum(abs(d[3 * b]) + abs(d[3 * b + 1]) for b in range(blocks))
            diff = fam_F(blocks, edges, Delta, x) - Fb
            rhs = delta / 8 - delta * delta + sum((d[3 * b + 2] - d[3 * b] / 2) ** 2 for b in range(blocks))
            check(diff >= rhs, "family (c) inequality")
            if delta < Fr(1, 8):
                check(diff > 0, "family (c) strict")

# ---------------- Example ex:chain: curvatures and the 20 delta^2 point
for m in range(2, 7):
    # Psi_m quadratic: compute Hessian diagonal exactly by finite differences of a quadratic
    def Psi(xi, z):
        val = xi[m - 1] ** 2
        prev = Fr(0)
        for t in range(m):
            val += (xi[t] - 2 * prev - z[t]) ** 2 + z[t] * (1 - z[t]) / 8
            prev = xi[t]
        return val
    zero = [Fr(0)] * m
    for t in range(m):
        e = [Fr(0)] * m; e[t] = Fr(1)
        d2 = Psi(e, zero) + Psi([-x for x in e], zero) - 2 * Psi(zero, zero)
        check(d2 == (4 if t == m - 1 else 10), "chain xi curvature")
        d2 = Psi(zero, e) + Psi(zero, [-x for x in e]) - 2 * Psi(zero, zero)
        check(d2 == Fr(7, 4), "chain z curvature")
    for dl in [Fr(1, 2), Fr(1, 7), Fr(1, 1000)]:
        xi = [Fr(0)] * m; xi[0] = 2 * dl
        check(Psi(xi, zero) == 20 * dl * dl, "chain 20 delta^2")
    check(Fr(4) ** (m + 1) / 20 == Fr(4) ** m / 5 and 8 * Fr(4) ** (m + 1) == 32 * Fr(4) ** m, "chain kappa bracket")

print("counts:", counts)
print("failures:", len(fails))
print("ALL OK" if not fails else "SOME FAILURES")
