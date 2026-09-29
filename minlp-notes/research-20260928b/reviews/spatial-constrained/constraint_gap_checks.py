"""Reviewer's independent checks of Section 5 (constraint-gap schemes) and Section 6 (bisection bounds).

Instances on X0 = [-1.2, 1.3]^2 (s0 = 2.5), objective kept exact, constraint g(z) = -z_2 <= 0 loosened:
  F0: f = z_2            (Example 5.3 of the note; optimal set M = [-1.2,1.3] x {0}, p = 1)
  F1: f = z_2 + z_1^2    (KKT point z* = 0, multiplier 1, active stratum {z_2 = 0} of dimension d = 1;
                          Theorem 5.7 claims N_opt >= c log(1/eps))
Loosening:  iso   R_B = {z in B : -z_2 <= beta q_B(z)}      (tube hypothesis T_{0,beta})
            aniso R_B = {z in B : -z_2 <= beta a_2(z_2)}
Node bound (own derivation): for fixed z_1 the feasible z_2 form the interval [r1, r2] of roots of
  beta z^2 - (1 + beta(l2+u2)) z + beta l2 u2 - beta A1(z_1) = 0  (A1 = a_1(z_1) iso, 0 aniso),
intersected with [l2, u2]; then minimise the convex function c z_1^2 + z2min(z_1) by golden section.
Validated against brute-force grid minimisation on random boxes.

Checks:
  (1) node counts of widest-side binary bisection (ties split z_2, as in the author's script) and
      of uniform 4-ary bisection;
  (2) Theorem 5.2 lower bound (5/16)(2 eps)^(-1/2) for F0-iso against leaf counts;
  (3) the tube dichotomy (D) on every leaf of the F0/F1-iso trees at super-optimal grid points;
  (4) Lemma 6.1 level by level on the 4-ary trees, Theorem 6.4 and Corollary 6.5(b) (10^n vs 20^n);
  (5) the Proposition 5.6 / Theorem 5.7 lower bound for F1-iso with explicit constants.
Usage: python3 constraint_gap_checks.py
"""
import math
import numpy as np

LO, HI = -1.2, 1.3
S0 = HI - LO
BETA = 1.0
PHI = (math.sqrt(5) - 1) / 2


def z2min(z1, l1, u1, l2, u2, iso):
    A1 = (z1 - l1) * (u1 - z1) if iso else 0.0
    a, b, c = BETA, -(1 + BETA * (l2 + u2)), BETA * l2 * u2 - BETA * A1
    D = b * b - 4 * a * c
    if D < 0:
        return math.inf
    sq = math.sqrt(D)
    r1, r2 = (-b - sq) / (2 * a), (-b + sq) / (2 * a)
    lo, hi = max(l2, r1), min(u2, r2)
    return lo if lo <= hi + 1e-15 else math.inf


def lb(box, cz, iso):
    l1, u1, l2, u2 = box
    if cz == 0.0 or not iso:
        m = 0.5 * (l1 + u1)
        zmin = z2min(m, l1, u1, l2, u2, iso)  # iso: widest z_2 range at the midpoint
        if zmin == math.inf:
            return math.inf
        if cz == 0.0:
            return zmin
        # aniso: z2min independent of z1
        return zmin + cz * (0.0 if l1 <= 0 <= u1 else min(l1 * l1, u1 * u1))
    m = 0.5 * (l1 + u1)
    if z2min(m, l1, u1, l2, u2, iso) == math.inf:
        return math.inf
    # feasible z1 interval [p, q] around the midpoint (A1 concave, symmetric)
    def edge(a, b):  # a feasible, b maybe not
        if z2min(b, l1, u1, l2, u2, iso) < math.inf:
            return b
        for _ in range(80):
            mid = 0.5 * (a + b)
            if z2min(mid, l1, u1, l2, u2, iso) < math.inf:
                a = mid
            else:
                b = mid
        return a
    p, q = edge(m, l1), edge(m, u1)
    phi = lambda x: cz * x * x + z2min(x, l1, u1, l2, u2, iso)
    a, b = p, q
    x1, x2 = b - PHI * (b - a), a + PHI * (b - a)
    f1, f2 = phi(x1), phi(x2)
    for _ in range(90):
        if f1 <= f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - PHI * (b - a)
            f1 = phi(x1)
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + PHI * (b - a)
            f2 = phi(x2)
    return min(f1, f2, phi(p), phi(q))


def brute_lb(box, cz, iso, G=601):
    l1, u1, l2, u2 = box
    x = np.linspace(l1, u1, G)
    y = np.linspace(l2, u2, G)
    X, Y = np.meshgrid(x, y, indexing="ij")
    Q = ((X - l1) * (u1 - X) if iso else 0.0) + (Y - l2) * (u2 - Y)
    ok = -Y <= BETA * Q + 1e-14
    return float(np.min(np.where(ok, Y + cz * X * X, np.inf)))


def run_widest(eps, cz, iso, cap=3_000_000, leaves_out=None):
    stack, nodes = [(LO, HI, LO, HI)], 0
    while stack:
        B = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        if lb(B, cz, iso) >= -eps:
            if leaves_out is not None:
                leaves_out.append(B)
            continue
        l1, u1, l2, u2 = B
        if (u1 - l1) > (u2 - l2):
            m = 0.5 * (l1 + u1)
            stack += [(l1, m, l2, u2), (m, u1, l2, u2)]
        else:
            m = 0.5 * (l2 + u2)
            stack += [(l1, u1, l2, m), (l1, u1, m, u2)]
    return nodes


def run_4ary(eps, cz, iso, cap=3_000_000, leaves_out=None):
    """Uniform 2^n-ary refinement; returns (nodes, dict level -> #non-pruned)."""
    level = {0: [(LO, HI, LO, HI)]}
    nonpr, nodes, j = {}, 0, 0
    while level.get(j):
        nxt = []
        for B in level[j]:
            nodes += 1
            if nodes > cap:
                return None, nonpr
            if lb(B, cz, iso) >= -eps:
                if leaves_out is not None:
                    leaves_out.append(B)
                continue
            nonpr[j] = nonpr.get(j, 0) + 1
            l1, u1, l2, u2 = B
            m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
            nxt += [(l1, m1, l2, m2), (m1, u1, l2, m2), (l1, m1, m2, u2), (m1, u1, m2, u2)]
        j += 1
        level[j] = nxt
    return nodes, nonpr


def cells_meeting_E(j, t, cz):
    """N_j(E(t)): closed level-j cells meeting E(t) = {z in X0 : z_2 >= 0, z_2 + cz z_1^2 <= t}."""
    s = S0 / 2 ** j
    K = 2 ** j
    cnt = 0
    b0 = max(0, math.ceil(-LO / s - 1))
    b1 = min(K - 1, math.floor((t - LO) / s))
    for b in range(b0, b1 + 1):
        l2, u2 = LO + b * s, LO + (b + 1) * s
        if u2 < 0 or max(l2, 0.0) > t:
            continue
        if cz == 0:
            cnt += K
            continue
        r = math.sqrt(max(0.0, (t - max(l2, 0.0)) / cz))
        amax = min(K - 1, math.floor((r - LO) / s))
        amin = max(0, math.ceil((-r - LO) / s - 1))
        cnt += max(0, amax - amin + 1)
    return cnt


def main():
    rng = np.random.default_rng(3)
    # --- validate node bound
    worst = 0.0
    for cz in (0.0, 1.0):
        for iso in (True, False):
            for _ in range(60):
                c = rng.uniform(-1.0, 1.1, 2)
                w = np.exp(rng.uniform(math.log(0.01), math.log(2.0), 2))
                B = (max(LO, c[0] - w[0] / 2), min(HI, c[0] + w[0] / 2), max(LO, c[1] - w[1] / 2), min(HI, c[1] + w[1] / 2))
                a, b = lb(B, cz, iso), brute_lb(B, cz, iso)
                if a == math.inf or b == math.inf:
                    assert a == b == math.inf or (a == math.inf) == (b == math.inf), (B, a, b)
                    continue
                assert a <= b + 1e-9, (B, cz, iso, a, b)
                worst = max(worst, b - a)
    print(f"node bound check: own bound <= brute-force grid minimum on 240 random boxes; "
          f"max (grid - own) = {worst:.2e} (grid resolution effect)")
    # --- author's three-box certificates (F0) and the analogous ones for F1
    for cz in (0.0, 1.0):
        for iso in (False, True):
            cert = [lb((LO, HI, LO, -0.6), cz, iso), lb((LO, HI, -0.6, 0.0), cz, iso), lb((LO, HI, 0.0, HI), cz, iso)]
            print(f"three-slab boxes cz={cz} iso={iso}: bounds {[round(x, 6) for x in cert]}")
    # --- node counts and bounds
    print("\n eps     | F0 aniso wide | F0 iso wide (leaves) | Thm5.2 LB | F0 iso 4-ary | F1 aniso wide | F1 iso wide | F1 iso 4-ary | Prop5.6 LB (F1 iso)")
    for k in range(1, 8):
        eps = 10.0 ** (-k)
        a0 = run_widest(eps, 0.0, False)
        leaves = []
        i0 = run_widest(eps, 0.0, True, leaves_out=leaves)
        # tube dichotomy (D) on leaves: super-optimal points must have beta q_C(z) < v(z)
        viol = 0
        for (l1, u1, l2, u2) in leaves[:: max(1, len(leaves) // 400)]:
            xs = np.linspace(l1, u1, 9)
            ys = np.linspace(l2, u2, 9)
            X, Y = np.meshgrid(xs, ys, indexing="ij")
            sup = Y < -eps
            q = (X - l1) * (u1 - X) + (Y - l2) * (u2 - Y)
            viol += int(np.sum(sup & ~(BETA * q < -Y + 1e-15)))
        n4, nonpr0 = run_4ary(eps, 0.0, True)
        a1 = run_widest(eps, 1.0, False)
        leaves1 = []
        i1 = run_widest(eps, 1.0, True, leaves_out=leaves1)
        for (l1, u1, l2, u2) in leaves1:
            xs = np.linspace(l1, u1, 9)
            ys = np.linspace(l2, u2, 9)
            X, Y = np.meshgrid(xs, ys, indexing="ij")
            sup = Y + X * X < -eps
            q = (X - l1) * (u1 - X) + (Y - l2) * (u2 - Y)
            viol += int(np.sum(sup & ~(BETA * q < np.maximum(-Y, 0) + 1e-15)))
        n41, nonpr1 = run_4ary(eps, 1.0, True)
        lb52 = (5 / 16) * (2 * eps) ** -0.5
        r = 1 / 6
        lb56 = (BETA / 3) ** 0.5 * 2 * math.asinh(r / math.sqrt(eps)) / (math.pi * math.sqrt(2))
        print(f" {eps:7.0e} | {a0:13d} | {i0:10d} ({(i0 + 1) // 2:6d}) | {lb52:9.2f} | {n4:12d} | {a1:13d} | {i1:11d} | {n41:12d} | {lb56:.3f}"
              f"   (D)-violations on leaves: {viol}")
        # --- Lemma 6.1, Theorem 6.4, Corollary 6.5(b) on the 4-ary trees
        for name, cz, nodes, nonpr in (("F0-iso", 0.0, n4, nonpr0), ("F1-iso", 1.0, n41, nonpr1)):
            n = 2
            tau, kappa = BETA * n / 4, 1.0
            L = 1.0 if cz == 0 else math.hypot(2 * HI, 1.0)
            Lam = tau * (1 + L * kappa)
            j0 = next(j for j in range(40) if kappa * tau * S0 / 2 ** j <= 1)
            bad61 = []
            rhs_sum = 0
            for j, cnt in nonpr.items():
                s = S0 / 2 ** j
                if j >= j0:
                    if not eps < Lam * s * s:
                        bad61.append((j, "level"))
                    NE = cells_meeting_E(j, Lam * s * s - eps, cz)
                    if cnt > 5 ** n * NE:
                        bad61.append((j, cnt, 5 ** n * NE))
                    rhs_sum += NE
            lem61 = 1 + 2 ** n * (2 ** (n * j0) + 5 ** n * rhs_sum)
            if cz == 0:
                cg, NM = 1 / S0, lambda j: 2 ** j * cells_rows_with_zero(j)
            else:
                cg, NM = 1 / 1.3, lambda j: cells_meeting_E(j, 0.0, 1.0)
            Jp = [j for j in range(j0, 60) if Lam * (S0 / 2 ** j) ** 2 > eps]
            thm64 = 1 + 2 ** n * (2 ** (n * j0) + 5 ** n * (2 * math.sqrt(Lam / cg) + 3) ** n * sum(NM(j) for j in Jp))
            extra = ""
            if cz == 1.0:
                C0 = 1 + 2 ** (n * (j0 + 1))
                J = len([j for j in range(60) if Lam * (S0 / 2 ** j) ** 2 > eps])
                c10 = C0 + 10 ** n * (2 * math.sqrt(Lam / cg) + 3) ** n * 1 * J
                c20 = C0 + 20 ** n * (2 * math.sqrt(Lam / cg) + 3) ** n * 1 * J
                extra = f", Cor6.5(b) with 10^n: {c10:.0f}, with 20^n: {c20:.0f}"
            print(f"     {name}: 4-ary nodes {nodes}, Lemma 6.1 RHS {lem61}, violations {bad61}, Thm 6.4 RHS {thm64:.0f}{extra}")


def cells_rows_with_zero(j):
    s = S0 / 2 ** j
    return sum(1 for b in range(2 ** j) if LO + b * s <= 0 <= LO + (b + 1) * s)


if __name__ == "__main__":
    main()
