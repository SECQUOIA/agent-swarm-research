"""Single-center graded grids cannot certify two separated optima quickly.

Instance F_M(x,z) = x^2 - 2 x z + M z on [0,M]^2 (both continuous):
S = {(0,0),(M,M)}, F* = 0, Hessian [[2,-2],[-2,0]], L_x = 2, L_z = 0,
set growth with g = 1/20.

Claim checked: for every center c in the box, theta in (0,1/4], mesh
h in (0,M], the corrected-grid minimum satisfies
    beta <= -max(theta^2 M^2 / 379, h^2 / 20)
(with corrections L_x w^2/8 on x and any L_z >= 0 on z).
Also runs the filtered algorithm FG(theta, J) and confirms the hull stays
[0,M]^2 and the certified gap never drops below theta^2 M^2/379.
Finally checks the set-growth constant g = 1/20 on a rational sample.
"""
import random
from fractions import Fraction as Fr

random.seed(11)


def graded(lo, hi, c, h, theta):
    nodes = [c]
    t = Fr(0)
    while True:
        t2 = t + h + theta * t
        if c + t2 >= hi:
            if nodes[-1] != hi:
                nodes.append(hi)
            break
        nodes.append(c + t2)
        t = t2
    left = []
    t = Fr(0)
    while c > lo:
        t2 = t + h + theta * t
        if c - t2 <= lo:
            left.append(lo)
            break
        left.append(c - t2)
        t = t2
    return sorted(set(nodes + left))


def widths(nodes):
    w = {}
    for k, v in enumerate(nodes):
        cand = []
        if k > 0:
            cand.append(v - nodes[k - 1])
        if k + 1 < len(nodes):
            cand.append(nodes[k + 1] - v)
        w[v] = max(cand) if cand else Fr(0)
    return w


def F(M, x, z):
    return x * x - 2 * x * z + M * z


def stage(M, box, c, h, theta, Lz):
    gx = graded(box[0][0], box[0][1], c[0], h, theta)
    gz = graded(box[1][0], box[1][1], c[1], h, theta)
    wx, wz = widths(gx), widths(gz)
    best, arg = None, None
    mx = {v: None for v in gx}
    mz = {v: None for v in gz}
    for x in gx:
        dx = 2 * wx[x] ** 2 / 8
        for z in gz:
            q = F(M, x, z) - dx - Lz * wz[z] ** 2 / 8
            if best is None or q < best:
                best, arg = q, (x, z)
            if mx[x] is None or q < mx[x]:
                mx[x] = q
            if mz[z] is None or q < mz[z]:
                mz[z] = q
    return best, arg, gx, gz, mx, mz


def check_bound():
    count = 0
    for M in (16, 40, 100):
        for theta in (Fr(1, 4), Fr(1, 8), Fr(1, 16)):
            for h in (Fr(M), Fr(M, 4), Fr(M, 16), Fr(M, 64)):
                for _ in range(4):
                    c = (Fr(random.randint(0, 64 * M), 64), Fr(random.randint(0, 64 * M), 64))
                    for Lz in (Fr(0), Fr(2)):
                        beta, *_ = stage(M, ((Fr(0), Fr(M)),) * 2, c, h, theta, Lz)
                        bound = max(theta ** 2 * M ** 2 / 379, h ** 2 / 20)
                        assert beta <= -bound, (M, theta, h, c, beta, -bound)
                        count += 1
    return count


def run_fg(M, theta, J):
    box = [(Fr(0), Fr(M)), (Fr(0), Fr(M))]
    c = (Fr(0), Fr(0))
    U = F(M, *c)
    s = Fr(M)
    gaps = []
    for j in range(J + 1):
        h = s / 2 ** j
        beta, y, gx, gz, mx, mz = stage(M, box, c, h, theta, Fr(0))
        U = min(U, F(M, *y))
        gaps.append(U - beta)
        # filter: keep interval [a,b] iff min(m(a), m(b)) <= U; take hull
        newbox = []
        for g, m in ((gx, mx), (gz, mz)):
            kept = [(a, b2) for a, b2 in zip(g, g[1:]) if min(m[a], m[b2]) <= U]
            newbox.append((min(a for a, _ in kept), max(b2 for _, b2 in kept)))
        assert newbox == [(Fr(0), Fr(M)), (Fr(0), Fr(M))], newbox
        box = newbox
        c = y
    return gaps


def check_growth():
    M = 20
    worst = None
    for _ in range(4000):
        x = Fr(random.randint(0, 400 * M), 400)
        z = Fr(random.randint(0, 400 * M), 400)
        d2 = min(x * x + z * z, (M - x) ** 2 + (M - z) ** 2)
        if d2 == 0:
            continue
        r = F(M, x, z) / d2
        worst = r if worst is None or r < worst else worst
    assert worst >= Fr(1, 20)
    return worst


n = check_bound()
print("stage bound checks:", n)
for M, theta in ((16, Fr(1, 4)), (64, Fr(1, 8))):
    gaps = run_fg(M, theta, 9)
    floor = theta ** 2 * M ** 2 / 379
    assert min(gaps) >= floor
    print(f"FG M={M} theta={theta}: min gap {float(min(gaps)):.4f} >= {float(floor):.4f};"
          f" last gaps {[round(float(g), 3) for g in gaps[-3:]]}")
print("sampled min ratio (F-F*)/dist^2 =", float(check_growth()))
