"""R3 exact checks for optsets.tex.

1. prop:twocenters growth constant 1/20 on a rational sample.
2. Algorithm UC (thm:cells) on F_M = x^2 - 2xz + Mz, [0,M]^2, both coordinates
   continuous, L = (L_x, L_z) = (2, 0): node counts against K_S, brackets.
3. CT-style stage on F_M: z has L_z = 0, so G_z = {0, M} (Algorithm 1, i not in P);
   count of x-nodes for theta ~ sqrt(eps)/M, h ~ sqrt(eps) (float count only,
   used to illustrate the table-size claim of prop:twocenters).
4. rem:shor example and prop:sshard multiplier identity on a small instance.
Run: python3 -B r3_optsets.py
"""
from fractions import Fraction as Fr
from math import log, sqrt, isqrt


def report(name, ok):
    print(("PASS " if ok else "FAIL ") + name)


def growth_twocenters():
    M = Fr(8)
    N = 48
    worst = None
    for i in range(N + 1):
        for k in range(N + 1):
            x, z = M * i / N, M * k / N
            F = x * x - 2 * x * z + M * z
            d2 = min(x * x + z * z, (x - M) ** 2 + (z - M) ** 2)
            if d2 > 0:
                r = F / d2
                worst = r if worst is None or r < worst else worst
    report(f"twocenters growth: min F/dist^2 on sample = {worst} >= 1/20", worst >= Fr(1, 20))


def uc_twocenters(M=Fr(4), stages=11):
    L = {0: Fr(2), 1: Fr(0)}
    n, Lmax = 2, Fr(2)
    s = M
    F = lambda x, z: x * x - 2 * x * z + M * z
    cells = {0: [(Fr(0), M)], 1: [(Fr(0), M)]}
    U = F(Fr(0), Fr(0))
    gS, r = Fr(1, 20), 2
    kS = max(1, Lmax / gS)
    KS = 12 * r * (2 * sqrt(n * kS) + 1)
    ok = True
    maxnodes = 0
    for j in range(stages + 1):
        h = s / 2 ** j
        stage = {}
        nodes = {}
        for i in (0, 1):
            sc = []
            for (a, b) in cells[i]:
                pts = [a]
                k = int(a / h) + 1
                while k * h < b:
                    pts.append(k * h)
                    k += 1
                pts.append(b)
                sc += list(zip(pts[:-1], pts[1:]))
            stage[i] = sc
            nodes[i] = sorted({p for c in sc for p in c})
        d = {}
        for i in (0, 1):
            w = {v: Fr(0) for v in nodes[i]}
            for (a, b) in stage[i]:
                w[a] = max(w[a], b - a)
                w[b] = max(w[b], b - a)
            d[i] = {v: L[i] * w[v] ** 2 / 8 for v in nodes[i]}
        Q = {(x, z): F(x, z) - d[0][x] - d[1][z] for x in nodes[0] for z in nodes[1]}
        beta = min(Q.values())
        y = min(Q, key=Q.get)
        U = min(U, F(*y))
        ok &= beta <= 0 <= U and U - beta <= Fr(1, 2) * n * Lmax * h * h
        m0 = {x: min(Q[(x, z)] for z in nodes[1]) for x in nodes[0]}
        m1 = {z: min(Q[(x, z)] for x in nodes[0]) for z in nodes[1]}
        cells = {0: [c for c in stage[0] if min(m0[c[0]], m0[c[1]]) <= U],
                 1: [c for c in stage[1] if min(m1[c[0]], m1[c[1]]) <= U]}
        maxnodes = max(maxnodes, len(nodes[0]), len(nodes[1]))
        ok &= len(nodes[0]) <= KS and len(nodes[1]) <= KS
        print(f"   UC stage {j}: |G_x|={len(nodes[0])}, |G_z|={len(nodes[1])}, gap={float(U-beta):.3g}")
    report(f"UC on F_M (M={M}): brackets hold, max nodes {maxnodes} <= K_S={KS:.1f}", ok)


def ct_counts():
    # float count of graded x-nodes on [0,M] from center 0 (one side, worst side)
    for M, eps in [(2.0 ** 20, 1 / 16), (2.0 ** 24, 1 / 16), (2.0 ** 24, 2.0 ** -10)]:
        mu = 2
        while 2.0 ** -mu > sqrt(eps) / M:
            mu += 1
        th = 2.0 ** -mu
        h = sqrt(eps)
        t, k = 0.0, 0
        while t < M:
            t = t + h + th * t
            k += 1
        nx = k + 1
        table = 2 * nx
        claim = M * M / (2304 * eps)
        D = (2 / 8) * (h + th * M) ** 2
        print(f"   M=2^{int(log(M,2))}, eps={eps}: theta=2^-{mu}, h={h:.3g}, |G_x|~{nx},"
              f" stage gap<=D<={D:.3g}, table=2|G_x|={table} vs claimed {claim:.3g}")


def shor_and_sshard():
    a = [Fr(1), Fr(-1), Fr(1, 2)]
    H = [[2 * a[i] * a[k] for k in range(3)] for i in range(3)]
    H[2][2] -= Fr(1, 4)  # t(1-t)/8 contributes -1/4
    diag_ok = [H[i][i] for i in range(3)] == [2, 2, Fr(1, 4)]
    # multiplier at (v,v,0): dF/dt = 2(x-y+t/2)(1/2) + (1-2t)/8 = 1/8 -> lambda_t = 1/4
    lam = [0, 0, 2 * Fr(1, 8)]
    HL = [[H[i][k] + (lam[i] if i == k else 0) for k in range(3)] for i in range(3)]
    ok = diag_ok and all(HL[i][k] == 2 * a[i] * a[k] for i in range(3) for k in range(3))
    report("rem:shor: diagonal (2,2,1/4), Lambda=diag(0,0,1/4), H+Lambda=2aa^T", ok)


if __name__ == "__main__":
    growth_twocenters()
    uc_twocenters()
    ct_counts()
    shor_and_sshard()
