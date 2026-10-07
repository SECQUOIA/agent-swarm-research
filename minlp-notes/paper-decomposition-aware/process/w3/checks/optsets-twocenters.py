"""Exact checks for Proposition prop:twocenters (optsets.tex, W3 revision).

F_M(x,z) = x^2 - 2xz + Mz on [0,M]^2, L_x = 2, L_z = 0.

1. Set growth F_M >= dist(.,S)^2/20 on a rational sample.
2. The bound beta <= -max{theta^2 M^2/379, h^2/20} for graded x-grids with
   theta in (0,1/4], h in (0,M], any center, G_z = {0,M} (the worst case:
   more z-nodes or d_z > 0 only lower beta), d_x = 2 w^2/8.
3. The constants used in the proof and in the consequences.
4. Exact runs of TRIAL and CT (growth.tex, Algorithms 1 and 2) on F_M:
   every stage obeys the bound, stage 0 has G_x = {0,M}, and the stage that
   certifies eps has an x-grid with > M/(48 sqrt eps) nodes and a bag table
   with > M/(24 sqrt eps) entries.
Run: python3 -B optsets-twocenters.py
"""
from fractions import Fraction as Fr
from math import isqrt, sqrt


def F(M, x, z):
    return x * x - 2 * x * z + M * z


def graded(c, lo, hi, h, th):
    nodes = {c}
    t = Fr(0)
    while t < hi - c:
        t = min(t + h + th * t, hi - c)
        nodes.add(c + t)
    t = Fr(0)
    while t < c - lo:
        t = min(t + h + th * t, c - lo)
        nodes.add(c - t)
    return sorted(nodes)


def widths(nodes):
    w = {}
    for k, v in enumerate(nodes):
        a = nodes[k] - nodes[k - 1] if k > 0 else Fr(0)
        b = nodes[k + 1] - nodes[k] if k + 1 < len(nodes) else Fr(0)
        w[v] = max(a, b)
    return w


def beta_and_marginals(M, Gx, Gz, Lx=Fr(2)):
    wx = widths(Gx)
    best, arg = None, None
    mx = {}
    for v in Gx:
        dx = Lx * wx[v] ** 2 / 8
        m = None
        for z in Gz:
            q = F(M, v, z) - dx  # d_z = 0 (L_z = 0)
            if m is None or q < m:
                m = q
            if best is None or q < best:
                best, arg = q, (v, z)
        mx[v] = m
    return best, arg, mx


def check_growth():
    worst = None
    for M in [Fr(1), Fr(7, 3), Fr(16)]:
        N = 40
        for a in range(N + 1):
            for b in range(N + 1):
                x, z = M * a / N, M * b / N
                d2 = min(x * x + z * z, (M - x) ** 2 + (M - z) ** 2)
                if d2 == 0:
                    continue
                r = F(M, x, z) / d2
                worst = r if worst is None else min(worst, r)
    print("growth: min F/dist^2 on sample =", worst, ">= 1/20:", worst >= Fr(1, 20))
    return worst >= Fr(1, 20)


def check_bound():
    ok = True
    tight = None
    count = 0
    for M in [Fr(1), Fr(7, 3), Fr(16), Fr(1000)]:
        for th in [Fr(1, 4), Fr(3, 16), Fr(1, 8), Fr(1, 16), Fr(1, 32), Fr(1, 64), Fr(1, 128)]:
            for hf in [Fr(1), Fr(1, 2), Fr(1, 7), Fr(1, 16), Fr(1, 17), Fr(1, 100), Fr(1, 1000)]:
                h = M * hf
                for cf in [Fr(0), Fr(1, 10), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(9, 10), Fr(1)]:
                    c = M * cf
                    Gx = graded(c, Fr(0), M, h, th)
                    if len(Gx) > 4000:
                        continue
                    b, _, _ = beta_and_marginals(M, Gx, [Fr(0), M])
                    bound = -max(th * th * M * M / 379, h * h / 20)
                    count += 1
                    if not b <= bound:
                        ok = False
                        print("FAIL", M, th, h, c, b, bound)
                    r = b / bound
                    tight = r if tight is None else min(tight, r)
    print(f"bound (9.1): {count} cases, all hold: {ok}; min beta/bound = {float(tight):.4f}")
    return ok


def check_constants():
    ok = True
    ok &= Fr(23, 100) ** 2 / 20 > Fr(1, 379)
    ok &= (Fr(1, 2) - Fr(9, 64)) * Fr(16, 25) == Fr(23, 100)
    ok &= Fr(9, 4) * Fr(1, 16) == Fr(9, 64)
    ok &= sqrt(20) + sqrt(379) < 24
    # stage 0: h in [M,2M): M^2/4 >= max{theta^2 M^2/379, h^2/20} with h < 2M
    ok &= Fr(1, 4) >= Fr(4, 20) and Fr(1, 4) >= Fr(1, 16 * 379)
    # K = 1 case: M^2/16 >= max{theta^2M^2/379, h^2/20} for theta <= 1/4, h <= M
    ok &= Fr(1, 16) >= Fr(1, 20) and Fr(1, 16) >= Fr(1, 16 * 379)
    print("constants:", ok, "; sqrt20+sqrt379 =", sqrt(20) + sqrt(379))
    return ok


def trial(M, mu, eps, Jmax, cap):
    """Algorithm 1 (TRIAL) on F_M; P = {x}; returns list of stage records."""
    # L_x = 2: e_x = 1, r_x = 1/2; E least with 2^E r_x >= M
    E = 0
    while Fr(2 ** E, 2) < M:
        E += 1
    th = Fr(1, 2 ** mu)
    Bx = (Fr(0), M)
    c = Fr(0)
    U = F(M, Fr(0), Fr(0))
    recs = []
    for j in range(Jmax + 1):
        h = Fr(2 ** E, 2 ** (j + 1)) if E - j - 1 >= 0 else Fr(1, 2 ** (j + 1 - E))
        Gx = graded(c, Bx[0], Bx[1], h, th)
        if len(Gx) > cap:
            return recs, "abort"
        Gz = [Fr(0), M]
        b, arg, mx = beta_and_marginals(M, Gx, Gz)
        U = min(U, F(M, *arg))
        bound = -max(th * th * M * M / 379, h * h / 20)
        recs.append(dict(j=j, h=h, th=th, beta=b, U=U, nx=len(Gx), table=len(Gx) * len(Gz),
                         ok=b <= bound, Gx0=(Gx if j == 0 else None)))
        if U - b <= eps:
            return recs, "success"
        # filter x with threshold U; z not in P is not filtered
        keep = [k for k in range(len(Gx) - 1) if min(mx[Gx[k]], mx[Gx[k + 1]]) <= U]
        Bx = (Gx[keep[0]], Gx[keep[-1] + 1])
        c = arg[0]
    return recs, "limit"


def check_ct(M, eps):
    E = 0
    while Fr(2 ** E, 2) < M:
        E += 1
    eta0 = Fr(2 ** E)
    J = 0
    while Fr(9, 16) * eta0 ** 2 / 4 ** J > eps:
        J += 1
    ok = True
    mu = 2
    while True:
        cap = 10 * 2 ** mu * 2  # K(theta, n_P=1) = 10 theta^-1 ceil(log2 3)
        recs, status = trial(M, mu, eps, J, cap)
        for r in recs:
            ok &= r["ok"]
            if r["j"] == 0:
                ok &= r["Gx0"] == [Fr(0), M] and r["beta"] <= -M * M / 4
            # consequence (b) for every stage, with eps_stage = -beta
            epsb = -r["beta"]
            ok &= r["nx"] > M / (48 * sqrt(epsb))
        if status == "success":
            last = recs[-1]
            lb_x = float(M) / (48 * sqrt(eps))
            lb_t = float(M) / (24 * sqrt(eps))
            print(f"CT on F_M, M={M}, eps={eps}: success at mu={mu}, stage {last['j']},"
                  f" x-nodes {last['nx']} > {lb_x:.1f}: {last['nx'] > lb_x};"
                  f" table {last['table']} > {lb_t:.1f}: {last['table'] > lb_t}")
            ok &= last["nx"] > lb_x and last["table"] > lb_t
            return ok
        mu += 1


if __name__ == "__main__":
    res = [check_growth(), check_bound(), check_constants()]
    for M, eps in [(Fr(64), Fr(1, 4)), (Fr(1024), Fr(1)), (Fr(4096), Fr(1, 4))]:
        res.append(check_ct(M, eps))
    print("ALL PASS" if all(res) else "SOME FAIL")
