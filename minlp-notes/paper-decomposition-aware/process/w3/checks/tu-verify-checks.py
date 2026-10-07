"""Independent exact checks for Section 8 and Appendix D (verifier for group tu).

Run: python3 -B tu-verify-checks.py
Every check uses Fractions (exact) except the random Hadamard test, which
uses exact integer determinants.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
import math
import random

ok = True


def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok = ok and bool(cond)


# ---------------------------------------------------------------- graded grids
def graded(lo, hi, c, h, theta):
    """Graded grid of Definition def:graded (continuous coordinate)."""
    nodes = {c}
    for side, end in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        while t < end:
            t = min(t + h + theta * t, end)
            nodes.add(c + side * t)
    return sorted(nodes)


def widths(G):
    """w(v): largest length of a grid interval with endpoint v."""
    w = {}
    for k, v in enumerate(G):
        adj = []
        if k > 0:
            adj.append(v - G[k - 1])
        if k + 1 < len(G):
            adj.append(G[k + 1] - v)
        w[v] = max(adj)
    return w


L = Fr(1)
# misaligned graded grids (paragraph after prop:tu-misaligned, App D.4)
G1 = graded(Fr(0), Fr(1), Fr(3, 10), Fr(1, 16), Fr(1, 4))
G2 = graded(Fr(0), Fr(1), Fr(7, 10), Fr(1, 16), Fr(1, 4))
listed = [Fr(0), Fr(79, 1280), Fr(51, 320), Fr(19, 80), Fr(3, 10), Fr(29, 80),
          Fr(141, 320), Fr(689, 1280), Fr(3381, 5120), Fr(16649, 20480), Fr(1)]
check(G1 == listed, "graded grid with center 3/10 equals the printed node list")
check(G2 == sorted(1 - t for t in G1), "center 7/10 grid is the reflection")
check(len(G1) == 11 and len(G2) == 11, "eleven nodes each")
check(set(G1) & set(G2) == {Fr(0), Fr(1)}, "common nodes are 0 and 1 only")
maxw = max(max(b - a for a, b in zip(G, G[1:])) for G in (G1, G2))
check(maxw == Fr(3831, 20480) and maxw < Fr(1, 5), "largest interval 3831/20480 < 1/5")
w1, w2 = widths(G1), widths(G2)
m = Fr(1, 2)
gap_ok = all(L * (nu - m) ** 2 > L / 8 * (w1[nu] ** 2 + w2[nu] ** 2) for nu in (0, 1))
check(gap_ok, "(8.5) holds with m=1/2 and d_i = L w_i^2/8")
delta = min(y2 - y1 for y1 in G1 for y2 in G2 if y2 > y1)
check(delta == Fr(27, 1280), "delta = 27/1280")
# corrected minimum above the threshold is positive
d1max = max(L / 8 * w1[v] ** 2 for v in G1)
d2max = max(L / 8 * w2[v] ** 2 for v in G2)
lam = (d1max + d2max) / delta + Fr(1, 10 ** 6)
cmin = min(L / 2 * ((y1 - m) ** 2 + (y2 - m) ** 2) + lam * (y2 - y1)
           - L / 8 * w1[y1] ** 2 - L / 8 * w2[y2] ** 2
           for y1 in G1 for y2 in G2 if y1 <= y2)
check(cmin > 0, "graded misaligned: corrected grid minimum > OPT = 0 above threshold")

# simple misaligned instance
H1, H2 = [Fr(0), Fr(1, 2), Fr(1)], [Fr(0), Fr(1, 3), Fr(1)]
u1, u2 = widths(H1), widths(H2)
m = Fr(2, 5)
check(all(L * (nu - m) ** 2 > L / 8 * (u1[nu] ** 2 + u2[nu] ** 2) for nu in (0, 1)),
      "simple instance satisfies (8.5) with m=2/5")
check(Fr(4, 25) > Fr(1, 32) + Fr(1, 72) and Fr(9, 25) > Fr(1, 32) + Fr(1, 18),
      "printed inequalities")
dl = min(y2 - y1 for y1 in H1 for y2 in H2 if y2 > y1)
thr = (max(L / 8 * u1[v] ** 2 for v in H1) + max(L / 8 * u2[v] ** 2 for v in H2)) / dl
check(dl == Fr(1, 3) and thr == Fr(75, 288), "delta=1/3 and threshold 75L/288")
lam = thr + Fr(1, 1000)
cmin = min(L / 2 * ((y1 - m) ** 2 + (y2 - m) ** 2) + lam * (y2 - y1)
           - L / 8 * u1[y1] ** 2 - L / 8 * u2[y2] ** 2
           for y1 in H1 for y2 in H2 if y1 <= y2)
check(cmin > 0, "simple instance: corrected minimum > 0 just above threshold")
# aligned uniform grids: (8.5) fails at the common node nearest m
for hh in (Fr(1, 2), Fr(1, 3), Fr(1, 8)):
    U = [k * hh for k in range(int(1 / hh) + 1)]
    w = widths(U)
    for m in (Fr(2, 5), Fr(1, 7), Fr(5, 9)):
        nu = min(U, key=lambda t: abs(t - m))
        check(L * (nu - m) ** 2 <= 2 * L / 8 * w[nu] ** 2,
              f"aligned uniform h={hh}, m={m}: (8.5) fails at nearest node")

# ---------------------------------------------------------------- ex:tu-sum
G = graded(Fr(0), Fr(3), Fr(0), Fr(1), Fr(1, 4))
check(G == [0, 1, Fr(9, 4), 3], "ex:tu-sum grid {0,1,9/4,3}")
w = widths(G)
d = {v: L / 8 * w[v] ** 2 for v in G}
check(d == {0: L / 8, 1: 25 * L / 128, Fr(9, 4): 25 * L / 128, 3: 9 * L / 128},
      "ex:tu-sum corrections")
star = (1, 1, 2)
F = lambda x: L / 2 * sum((a - b) ** 2 for a, b in zip(x, star))
feas = [x for x in product(G, repeat=3) if x[0] + x[1] == x[2]]
check(len(feas) == 7, "seven feasible grid points")
vals = sorted(F(x) - sum(d[t] for t in x) for x in feas)
check(vals == sorted([Fr(21, 8), Fr(31, 64), Fr(31, 64), Fr(51, 64), Fr(51, 64),
                      Fr(175, 64), Fr(175, 64)]), "corrected values as printed")
check(min(vals) == Fr(31, 64) > 0, "corrected minimum 31L/64 > OPT")
allow = 3 * L * Fr(5, 4) ** 2 / 8
check(allow == Fr(75, 128) and min(F(x) for x in feas) - allow == Fr(53, 128),
      "constant allowance 75L/128 gives 53L/128 > OPT")

# ---------------------------------------------------------------- ex:tu-fullcurv
for hh in (Fr(1, 2), Fr(1, 3), Fr(1, 8)):
    Ff = lambda t: 2 * t * t - 2 * hh * t
    opt = Ff(hh / 2)
    grid_min = min(Ff(k * hh) for k in range(int(1 / hh) + 1))
    check(opt == -hh ** 2 / 2 and grid_min == 0 and grid_min - 2 * 2 * hh ** 2 / 8 == opt,
          f"ex:tu-fullcurv h={hh}")

# ---------------------------------------------------------------- ex:tu-union
S = [(Fr(0), Fr(0), Fr(0)), (Fr(1, 2), Fr(1, 2), Fr(1))]
worst = None
N = 60
for a in range(N + 1):
    for c in range(N + 1):
        x1, x3 = Fr(a, N), Fr(c, N)
        x2 = x3 - x1
        if not (0 <= x2 <= 1):
            continue
        Fb = (2 * x1 - x3) ** 2 + Fr(1, 4) * x3 * (1 - x3)
        dist2 = min((x1 - s[0]) ** 2 + (x2 - s[1]) ** 2 + (x3 - s[2]) ** 2 for s in S)
        if dist2 > 0:
            r = Fb / dist2
            worst = r if worst is None or r < worst else worst
check(worst is not None and worst >= Fr(1, 6), f"ex:tu-union growth ratio >= 1/6 (min {worst})")
Hb = [[8, 0, -4], [0, 0, 0], [-4, 0, Fr(3, 2)]]
check(max(sum(abs(v) for v in row) for row in Hb) == 12, "ex:tu-union row-sum bound 12")
nb = 7
check(2 * (5 + math.isqrt(4 * 216 * nb)) == 2 * (5 + math.floor(2 * math.sqrt(216 * nb))),
      "ex:tu-union bound arithmetic")


# ---------------------------------------------------------------- lem:tu-uniform
def simulate(nc, p, eps, hull):
    """Exact TU-GRID on X={x in [-1,1]^nc: x_1+..+x_p<=p}, F=Lbar/2|x|^2, eta=1.

    The row is redundant on the box and F is separable, so the min-marginal of
    coordinate i at t is Lbar t^2/2 + sum_{k != i} min_{G_k} Lbar y^2/2 - E_j.
    All coordinates evolve identically; one interval list is tracked.
    Returns list of (j, intervals of D^(j), node count at level j).
    """
    Lb = Fr(1)
    D = [(Fr(-1), Fr(1))]
    out = []
    j = 0
    while True:
        h = Fr(1, 2 ** j)
        nodes = sorted({k * h for (a, b) in D for k in range(int(a / h), int(b / h) + 1)})
        E = nc * Lb * h * h / 8
        mn = min(Lb * t * t / 2 for t in nodes)
        U = (nc) * mn  # mu_j: minimum of F on the product grid (box)
        out.append((j, list(D), len(nodes)))
        if E <= eps:
            return out, j
        mm = {t: Lb * t * t / 2 + (nc - 1) * mn - E for t in nodes}
        cells = []
        for (a, b) in D:
            if a == b:
                if mm[a] <= U:
                    cells.append((a, b))
                continue
            k = a
            while k < b:
                if min(mm[k], mm[k + h]) <= U:
                    cells.append((k, k + h))
                k += h
        cells.sort()
        merged = []
        for a, b in cells:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        if hull:
            merged = [(merged[0][0], merged[-1][1])]
        D = merged
        j += 1


for nc in (4, 6, 8, 10, 18, 50, 202):
    # exact floor of sqrt((nc-2)/8)
    nu = max(k for k in range(0, nc) if 8 * k * k <= nc - 2)
    for hull in (False, True):
        for p in (1, 2, 3):
            eps = Fr(1, 64)
            levels, J = simulate(nc, p, eps, hull)
            good = True
            for (j, D, cnt) in levels:
                if j + 1 >= len(levels):
                    break
                h = Fr(1, 2 ** j)
                if (nu + 1) * h <= 1:
                    Dn = levels[j + 1][1]
                    cover = any(a <= -(nu + 1) * h and (nu + 1) * h <= b for a, b in Dn)
                    good = good and cover and levels[j + 1][2] >= 4 * nu + 5
            ub = 5 + math.floor(2 * math.sqrt(2 * nc))
            within = all(cnt <= ub for (j, D, cnt) in levels if j >= 1)
            lastcnt = levels[-1][2]
            hJm1 = Fr(1, 2 ** (J - 1)) if J >= 1 else None
            reach = J >= 1 and (nu + 1) * hJm1 <= 1
            check(good and within and reach and lastcnt ** p >= nc ** (p / 2)
                  and 4 * nu + 5 >= math.sqrt(2 * (nc - 2)) + 1,
                  f"lem:tu-uniform nc={nc} p={p} hull={hull}: J={J}, last nodes={lastcnt}, 4nu+5={4*nu+5}, ub={ub}")
for nc in range(4, 2000, 2):
    nu = max(k for k in range(0, nc) if 8 * k * k <= nc - 2)
    assert 4 * nu + 5 >= math.sqrt(2 * (nc - 2)) + 1
    assert (math.sqrt(2 * (nc - 2)) + 1) ** 2 >= nc
    assert nu + 1 <= math.sqrt(2 * nc)
check(True, "lem:tu-uniform inequalities for even nc < 2000")


# ---------------------------------------------------------------- Hadamard bound
def det(M):
    M = [[Fr(v) for v in row] for row in M]
    n = len(M)
    s = Fr(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            s = -s
        s *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n):
                M[r][k] -= f * M[c][k]
    return s


def rank(rows):
    M = [[Fr(v) for v in row] for row in rows]
    rk = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = next((r for r in range(rk, len(M)) if M[r][c] != 0), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk


random.seed(5)
worst_ratio = 0.0
tested = 0
for trial in range(400):
    nc = random.randint(1, 4)
    C = random.randint(1, 4)
    Hh = [[0] * nc for _ in range(nc)]
    for i in range(nc):
        for k in range(i, nc):
            Hh[i][k] = Hh[k][i] = random.randint(-C, C)
    Cmax = max(1, max(abs(v) for row in Hh for v in row))
    # interval (consecutive-ones) rows: TU
    rows = []
    for a in range(nc):
        for b in range(a, nc):
            r = [1 if a <= i <= b else 0 for i in range(nc)]
            rows.append(r)
            rows.append([-v for v in r])
    for i in range(nc):
        e = [0] * nc
        e[i] = 1
        rows.append(e)
        rows.append([-v for v in e])
    k = random.randint(0, nc)
    cand = random.sample(rows, min(len(rows), k))
    if cand and rank(cand) < len(cand):
        continue
    K = [Hh[i] + [cand[r][i] for r in range(len(cand))] for i in range(nc)]
    K += [cand[r] + [0] * len(cand) for r in range(len(cand))]
    dK = abs(det(K))
    if dK == 0:
        continue
    tested += 1
    R = (2 * nc * Cmax) ** nc
    worst_ratio = max(worst_ratio, float(dK) / R)
    if dK > R or float(dK) > (math.sqrt(2) * nc * Cmax) ** nc + 1e-9:
        check(False, f"Hadamard bound violated nc={nc}")
check(tested > 50, f"Hadamard row bound |det K| <= (sqrt2 nc C)^nc <= R_TU on {tested} random cases (max ratio to R_TU {worst_ratio:.3g})")

# ---------------------------------------------------------------- snapping example
# F = x1 - x1^2 on {x in [0,1]^2: x1 = x2}, y = (1/2,1/2): J = the equality rows,
# ker = span(1,1), stationarity 1 - 2 x1 = 0, so P_z(J) = {(1/2,1/2)}.
x1 = Fr(1, 2)
check(1 - 2 * x1 == 0 and x1 - x1 ** 2 == Fr(1, 4), "snapping example returns (1/2,1/2), value 1/4")

# ---------------------------------------------------------------- tu-states(b) counting
for _ in range(2000):
    h = Fr(1, 2 ** random.randint(0, 6))
    a = Fr(random.randint(0, 400), random.randint(1, 50))
    nu = Fr(random.randint(-200, 200), random.randint(1, 30))
    lo, hi = nu - a - h, nu + a + h
    hh = h / 2
    cnt = math.floor(hi / hh) - math.ceil(lo / hh) + 1
    assert cnt <= math.floor(4 * a / h) + 5
check(True, "thm:tu-states(b): interval of length 2a+2h has <= floor(4a/h)+5 points of h/2 Z")

# ---------------------------------------------------------------- last-level size without growth
for _ in range(2000):
    nc = random.randint(1, 50)
    Lb = Fr(random.randint(1, 100), random.randint(1, 10))
    eta = Fr(1, random.randint(1, 8))
    eps = Fr(1, random.randint(1, 10 ** 6))
    J = 0
    while nc * Lb * eta ** 2 / (8 * 4 ** J) > eps:
        J += 1
    if J >= 1:
        assert (2 ** J) ** 2 < eta ** 2 * nc * Lb / (2 * eps)
check(True, "J>=1 minimal => 2^J < eta sqrt(nc Lbar/(2 eps))")

print("ALL PASS" if ok else "SOME CHECKS FAILED")
