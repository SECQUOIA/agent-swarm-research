"""Checks for the one-dimensional kink chain (robust-branching.md, Sections 2-4).

Chain model: kink at relative position rho in the node [0,1]; d = min(rho, 1 - rho).
A clip rule with clamp th splits at rho if th <= d, else at the clamp point; the child that
contains the kink has the kink at rho/th (left zone) or 1 - (1-rho)/th (right zone).
S = number of splits until the split lands on the kink (epsilon = 0; a positive eps only stops
the chain earlier).

[A] Theorem A: deterministic clamp schedules have trap points. For several schedules th(l, u),
    build the alternating itinerary in 200-digit arithmetic (mpmath; exact rationals would grow
    doubly exponentially for width-dependent schedules), take a point of the final interval and
    replay the rule: no split lands on the point within the depth checked, and the 1D
    node count at tolerance eps obeys T >= 2 K + 1, K = ceil(log(th0/(4 eps))/(2 log(1/th0))).
[B] Theorem B: randomized clamp th ~ U[t0, t1]. Monte Carlo E[S] for several kink positions
    and windows against the bound 1 + t1/(D delta) + log(1/d)/delta,
    delta = log(1/t1) - t0/D, D = t1 - t0. Also the exact E[S](d) by value iteration.
[C] Proposition C (price of safety): the lower bound ceil(log(th0/a)/log(1/th0)) against the
    randomized clamp, the recentring rule and the fixed clamp, for kinks near the boundary.
Added in the revision after review:
[A2] Theorem A(ii) as corrected: the old parenthetical fails for itineraries with a run of
    length 2 (fixed clamp 1/5); itineraries with runs of length at most 2 satisfy the bound with
    theta0/4 replaced by theta0^2/4; the McCormick x-only chain obeys the bound with w_k (not w_k^2).
[D] Proposition D(i) as corrected: the recentring clamp uses exactly S = J(theta) + 1 splits
    (exact rational arithmetic).
[A3] (closing audit) the McCormick x-only bound at points with runs of length at most 2 is
    T >= 2K' - 1; T >= 2K' + 1 holds only at the alternating points.
"""
import math
import random
import mpmath as mp

import numpy as np


# ------------------------------------------------------------------ [A]
def clip_split(l, u, a, th):
    w = u - l
    lo, hi = l + th * w, u - th * w
    return min(max(a, lo), hi)


mp.mp.dps = 200
Fr = lambda p, q=1: mp.mpf(p) / q  # noqa: E731
SCHEDULES = {
    "fixed 1/5": lambda l, u, k: Fr(1, 5),
    "depth: 1/5, 1/4 alternating": lambda l, u, k: Fr(1, 5) if k % 2 == 0 else Fr(1, 4),
    "width: 1/10 + w/5": lambda l, u, k: Fr(1, 10) + (u - l) / 5,
    "position: 1/8 + l/4": lambda l, u, k: Fr(1, 8) + l / 4,
}


def trap_point(sched, depth, pattern="LR"):
    """Point of the nested interval of the given itinerary (repeated pattern) after `depth` steps."""
    l, u = Fr(0), Fr(1)
    for k in range(depth):
        th = sched(l, u, k)
        w = u - l
        if pattern[k % len(pattern)] == "L":
            u = l + th * w
        else:
            l = u - th * w
    return (l + u) / 2


def replay(sched, a, depth):
    """Exact replay of the clip rule; returns list of (l, u, split) along the kink's chain."""
    l, u = Fr(0), Fr(1)
    out = []
    for k in range(depth):
        s = clip_split(l, u, a, sched(l, u, k))
        out.append((l, u, s))
        if s == a:
            break
        if a < s:
            u = s
        else:
            l = s
    return out


def theta0_of(name):
    return {"fixed 1/5": 0.2, "depth: 1/5, 1/4 alternating": 0.2, "width: 1/10 + w/5": 0.1,
            "position: 1/8 + l/4": 0.125}[name]


def count_1d(chain, a, eps, xonly=False):
    """1D (or McCormick x-only, full-height boxes) node count along a replayed chain."""
    T = 1
    for l, u, s in chain:
        w = u - l
        val = (a - l) * (u - a) / (w if xonly else 1)
        if val <= eps:
            break
        T += 2
    return T


def check_A2():
    import random as _r
    mp.mp.dps = 300
    print("[A2] Theorem A(ii), corrected (300-digit arithmetic)")
    # (a) counterexample to "(in fact uncountably many)" with the stated K: one run of length 2
    sched = SCHEDULES["fixed 1/5"]
    for k0 in (0, 1, 3, 5):
        run = "RR" if k0 % 2 else "LL"
        pat = "".join("LR"[j % 2] for j in range(k0)) + run
        nxt = "LR" if run == "RR" else "RL"
        pat += "".join(nxt[j % 2] for j in range(120))
        a = trap_point(sched, 120, pat)
        chain = replay(sched, a, 100)
        first = None
        for e10 in [x / 100 for x in range(100, 2500)]:  # eps = 10^-1 ... 10^-25 on a fine grid
            eps = 10 ** (-e10)
            K = math.ceil(math.log(0.2 / (4 * eps)) / (2 * math.log(5)))
            if count_1d(chain, a, mp.mpf(eps)) < 2 * K + 1:
                first = eps
                break
        print(f"  fixed 1/5, run of length 2 at step {k0}: a ~ {float(a):.10f}; first eps with T < 2K+1: "
              f"{first:.3g}" if first else f"  fixed 1/5, run at step {k0}: no violation found")
    # (b) itineraries with runs of length <= 2: bound with theta0^2/4
    rng = _r.Random(11)
    for name, sched in SCHEDULES.items():
        th0 = theta0_of(name)
        worst = math.inf
        hit = False
        for _ in range(20):
            pat, last, run = "", "", 0
            while len(pat) < 120:
                c = rng.choice("LR")
                if c == last and run == 2:
                    c = "L" if last == "R" else "R"
                run = run + 1 if c == last else 1
                last = c
                pat += c
            a = trap_point(sched, 120, pat)
            chain = replay(sched, a, 90)
            hit |= any(s == a for _, _, s in chain)
            for k in range(2, 49):
                eps = 10.0 ** -k
                K2 = math.ceil(math.log(th0 ** 2 / (4 * eps)) / (2 * math.log(1 / th0)))
                if K2 >= 1:
                    worst = min(worst, count_1d(chain, a, mp.mpf(eps)) - (2 * K2 + 1))
        print(f"  {name:30s} runs <= 2, 20 itineraries, eps = 1e-2..1e-48: min (T - (2 K2 + 1)) = {worst}; "
              f"split at a: {hit}")
    # (c) McCormick x-only: bound |c| rho(1-rho) w_k, K' = ceil(log(theta0/(4 eps))/log(1/theta0))
    for name, sched in SCHEDULES.items():
        th0 = theta0_of(name)
        a = trap_point(sched, 120)
        chain = replay(sched, a, 110)
        rows = []
        for k in (4, 8, 16, 24, 32, 48):
            eps = 10.0 ** -k
            K1 = math.ceil(math.log(th0 / (4 * eps)) / (2 * math.log(1 / th0)))
            Kx = math.ceil(math.log(th0 / (4 * eps)) / math.log(1 / th0))
            T = count_1d(chain, a, mp.mpf(eps), xonly=True)
            rows.append(f"1e-{k}: {T} (2K'+1 = {2 * Kx + 1}; old 2K+1 = {2 * K1 + 1})")
        print(f"  {name:30s} McCormick x-only: " + "; ".join(rows))
    mp.mp.dps = 200


def check_A3():
    """[A3] (closing audit) McCormick x-only bound at points whose runs have length <= 2:
    T >= 2K' + 1 can fail there; T >= 2K' - 1 (constant theta0^2/4) holds."""
    import random as _r
    mp.mp.dps = 300
    print("[A3] McCormick x-only, runs <= 2: T against 2K'+1 and 2K'-1 (300-digit arithmetic)")
    sched = SCHEDULES["fixed 1/5"]
    a = trap_point(sched, 150, "LL" + "RL" * 80)
    chain = replay(sched, a, 100)
    eps = mp.mpf(1) / 25
    Kx = math.ceil(math.log(0.2 / (4 * float(eps))) / math.log(5))
    print(f"  fixed 1/5, itinerary L,L,R,L,R,...: a = {mp.nstr(a, 12)}, eps = 1/25: "
          f"T = {count_1d(chain, a, eps, xonly=True)}, 2K'+1 = {2 * Kx + 1}")
    rng = _r.Random(23)
    for name, sched in SCHEDULES.items():
        th0 = theta0_of(name)
        n = fail_plus = fail_minus = 0
        for _ in range(20):
            pat, last, run = "", "", 0
            while len(pat) < 150:
                c = rng.choice("LR")
                if c == last and run == 2:
                    c = "L" if last == "R" else "R"
                run = run + 1 if c == last else 1
                last = c
                pat += c
            a = trap_point(sched, 150, pat)
            chain = replay(sched, a, 120)
            for k in range(2, 49, 2):
                eps = 10.0 ** -k
                if eps >= th0 / 4:
                    continue
                Kx = math.ceil(math.log(th0 / (4 * eps)) / math.log(1 / th0))
                T = count_1d(chain, a, mp.mpf(eps), xonly=True)
                n += 1
                fail_plus += T < 2 * Kx + 1
                fail_minus += T < 2 * Kx - 1
        print(f"  {name:30s} {n} cases: T < 2K'+1 in {fail_plus}; T < 2K'-1 in {fail_minus}")
    mp.mp.dps = 200


def check_D():
    """[D] exact S of the recentring clamp against J + 1."""
    from fractions import Fraction as F
    import random as _r
    print("[D] recentring clamp: S = J(theta) + 1 (exact rationals)")
    rng = _r.Random(5)
    for th in (F(1, 10), F(1, 5), F(1, 4), F(3, 10), F(1, 3)):
        ds = []
        for j in range(0, 9):
            for base in (th ** (j + 1), th ** (j + 1) / 2):
                for dlt in (F(0), F(1, 10 ** 6), -F(1, 10 ** 6), F(1, 100), -F(1, 100)):
                    d = base * (1 + dlt)
                    if 0 < d < F(1, 2):
                        ds.append(d)
        for _ in range(3000):
            ds.append(F(round(10 ** (-12 * rng.random()) * 10 ** 15), 2 * 10 ** 15))
        bad, maxclip, trapped = 0, 0, 0
        for d in ds:
            J = 0
            while not d >= th ** (J + 1):
                J += 1
            # recentring, kink at distance d from the left end of [0,1]
            l, u, S = F(0), F(1), 0
            while True:
                w = u - l
                S += 1
                if d < l + th * w:
                    s = l + max(th * w, 2 * (d - l))
                elif d > u - th * w:
                    s = u - max(th * w, 2 * (u - d))
                else:
                    s = d
                if s == d:
                    break
                l, u = (l, s) if d < s else (s, u)
            bad += S != J + 1
            # clip, for comparison
            l, u, Sc = F(0), F(1), 0
            while Sc < 60:
                w = u - l
                Sc += 1
                s = min(max(d, l + th * w), u - th * w)
                if s == d:
                    break
                l, u = (l, s) if d < s else (s, u)
            if s != d:
                trapped += 1
            else:
                maxclip = max(maxclip, Sc - (J + 1))
        print(f"  theta = {th}: {len(ds)} kinks, S_RC != J+1 in {bad}; clip exceeds J+1 by up to "
              f"{maxclip} splits; clip not at the kink within 60 splits: {trapped}")


def check_A():
    print("[A] deterministic clamp schedules: alternating-itinerary trap points (200-digit arithmetic)")
    for name, sched in SCHEDULES.items():
        th0 = min(Fr(1, 10), Fr(1, 5))  # all schedules above take values >= 1/10
        a = trap_point(sched, 80)
        chain = replay(sched, a, 60)
        hit = any(s == a for _, _, s in chain)
        rel = [float(min(a - l, u - a) / (u - l)) for l, u, _ in chain]
        print(f"  {name:30s} a ~ {float(a):.12f}  splits at a within 60 steps: {hit}; "
              f"min relative distance of a to the node ends along the chain: {min(rel):.4f}")
        for eps in (Fr(1, 10 ** 4), Fr(1, 10 ** 8), Fr(1, 10 ** 16), Fr(1, 10 ** 24)):
            T = 1
            for l, u, s in chain:
                if (a - l) * (u - a) <= eps:
                    break
                T += 2
            K = math.ceil(math.log(float(th0) / (4 * float(eps))) / (2 * math.log(1 / float(th0))))
            print(f"      eps=1e-{round(-math.log10(float(eps)))}: T = {T}  (bound 2K+1 = {2 * K + 1})")


# ------------------------------------------------------------------ [B]
def mc_S(rho, t0, t1, n, rng):
    """Vectorized Monte Carlo of S for the randomized clamp, from relative position rho."""
    d = np.full(n, min(rho, 1 - rho))
    S = np.zeros(n)
    alive = np.ones(n, dtype=bool)
    while alive.any():
        idx = np.nonzero(alive)[0]
        th = rng.uniform(t0, t1, size=idx.size)
        S[idx] += 1
        ok = th <= d[idx]
        alive[idx[ok]] = False
        f = idx[~ok]
        r = d[f] / th[~ok]
        d[f] = np.minimum(r, 1 - r)
    return S


def bound_B(d, t0, t1):
    D = t1 - t0
    delta = math.log(1 / t1) - t0 / D
    if delta <= 0:
        return None
    return 1 + t1 / (D * delta) + math.log(1 / d) / delta


def value_iteration(t0, t1, nq=4000, tol=1e-10):
    """E[S](d) on a grid (log-spaced below t0/4, uniform above); quadrature in theta."""
    grid = np.unique(np.concatenate([np.geomspace(1e-14, t0 / 4, 400), np.linspace(t0 / 4, 0.5, 2000)]))
    lg = np.log(grid)
    E = np.ones_like(grid)
    th = np.linspace(t0, t1, nq + 1)
    wq = np.full(nq + 1, (t1 - t0) / nq)
    wq[0] = wq[-1] = 0.5 * (t1 - t0) / nq
    for it in range(10000):
        Enew = np.empty_like(E)
        for i, d in enumerate(grid):
            fail = th > d
            r = d / th[fail]
            dn = np.minimum(r, 1 - r)
            dn = np.maximum(dn, grid[0])
            val = np.interp(np.log(dn), lg, E)
            Enew[i] = 1 + np.sum(wq[fail] * val) / (t1 - t0)
        diff = np.max(np.abs(Enew - E))
        E = Enew
        if diff < tol:
            break
    return grid, E, it


def check_B():
    print("[B] randomized clamp: E[S] (Monte Carlo, 10^6 chains) against the bound of Theorem B")
    rng = np.random.default_rng(20260929)
    for t0, t1 in ((0.1, 0.3), (0.05, 0.35), (0.1, 0.5), (0.15, 0.25), (0.19, 0.21)):
        D = t1 - t0
        delta = math.log(1 / t1) - t0 / D
        print(f"  window [{t0}, {t1}]: delta = {delta:.4f}")
        for a in (1 / 6, 3 / 238, 1 / 3, 0.1999, 0.25, 1e-2, 1e-4, 1e-8):
            S = mc_S(a, t0, t1, 10 ** 6, rng)
            b = bound_B(min(a, 1 - a), t0, t1)
            q = np.quantile(S, [0.5, 0.99, 0.9999])
            print(f"    a={a:.6g}: E[S] = {S.mean():.4f} +- {S.std() / 1e3:.4f}; median/99%/99.99%: "
                  f"{q[0]:.0f}/{q[1]:.0f}/{q[2]:.0f}; max {S.max():.0f}; bound "
                  + (f"{b:.3f}" if b else "n/a (delta <= 0)"))
    print("  value iteration of E[S](d), window [0.1, 0.3]:")
    grid, E, it = value_iteration(0.1, 0.3)
    B = [bound_B(d, 0.1, 0.3) for d in grid]
    gap = min(b - e for b, e in zip(B, E))
    print(f"    converged after {it} iterations; sup_d E[S](d) over d >= 0.1: {E[grid >= 0.1].max():.4f}; "
          f"min over the grid of (bound - E): {gap:.4f} (>= 0 means the bound holds)")
    for d in (1 / 6, 0.1, 0.05, 1e-2, 1e-4, 1e-8, 1e-12):
        print(f"    d={d:.3g}: E[S] = {np.interp(math.log(d), np.log(grid), E):.4f}")
    slope = (np.interp(math.log(1e-12), np.log(grid), E) - np.interp(math.log(1e-6), np.log(grid), E)) / math.log(1e6)
    ES = (0.3 * math.log(0.3) - 0.1 * math.log(0.1)) / 0.2 - 1  # E[log(theta)]
    print(f"    growth per unit log(1/d): {slope:.4f}; 1/E[log(1/theta)] = {1 / -ES:.4f}; 1/delta = "
          f"{1 / (math.log(1 / 0.3) - 0.5):.4f}")


# ------------------------------------------------------------------ [C]
def S_det(a, rule, th=0.2, cap=10 ** 4):
    l, u = 0.0, 1.0
    for k in range(1, cap):
        w = u - l
        if rule == "clip":
            s = min(max(a, l + th * w), u - th * w)
        else:  # recenter
            if a < l + th * w:
                s = l + max(th * w, 2 * (a - l))
            elif a > u - th * w:
                s = u - max(th * w, 2 * (u - a))
            else:
                s = a
        if s == a or abs(s - a) < 1e-15 * max(1.0, abs(a)):
            return k
        if a < s:
            u = s
        else:
            l = s
    return None


def check_C():
    print("[C] price of safety: splits until the kink is split, kink at distance a from the boundary")
    rng = np.random.default_rng(7)
    print("    lower bounds on S for every th0-safe rule that ends by splitting at the kink: J + 1")
    print("    a        LB(th0=0.1)  LB(th0=0.2)  E[S] rclip[.1,.3]  S recenter(.2)  S clip(.2)")
    for a in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 1e-12):
        lb1 = max(0, math.ceil(math.log(0.1 / a) / math.log(1 / 0.1))) + 1
        lb2 = max(0, math.ceil(math.log(0.2 / a) / math.log(1 / 0.2))) + 1
        S = mc_S(a, 0.1, 0.3, 200000, rng).mean()
        print(f"    {a:<8.0e} {lb1:^11d} {lb2:^12d} {S:^18.3f} {S_det(a, 'recenter')!s:^15} {S_det(a, 'clip')!s:^10}")


def check_S():
    """[S] the supersolution inequality of Theorem B, g(d) >= 1 + E[g(d'); theta > d], checked by
    quadrature (theta split at d and 2d, 200k points per piece) on a grid of d."""
    import sys
    print("[S] supersolution inequality of Theorem B (min over d of the slack; must be >= 0)")
    for t0, t1 in ((0.1, 0.3), (0.05, 0.35), (0.1, 0.5), (0.01, 0.2)):
        D = t1 - t0
        delta = math.log(1 / t1) - t0 / D
        A, B = 1 + t1 / (D * delta), 1 / delta
        g = lambda d: A + B * np.log(1 / d)  # noqa: E731
        worst = (math.inf, None)
        for d in np.concatenate([np.geomspace(1e-9, t0, 300), np.linspace(t0, 0.5, 600)]):
            lo = max(d, t0)
            total = 0.0
            for a_, b_ in ((lo, min(max(2 * d, lo), t1)), (min(max(2 * d, lo), t1), t1)):
                if b_ <= a_:
                    continue
                # midpoint rule (avoids the integrable log singularity at theta = d)
                n = 200000
                th = a_ + (np.arange(n) + 0.5) * (b_ - a_) / n
                r = d / th
                total += np.sum(g(np.minimum(r, 1 - r))) * (b_ - a_) / n
            slack = g(d) - 1 - total / D
            if slack < worst[0]:
                worst = (slack, d)
        print(f"  window [{t0}, {t1}]: delta = {delta:.4f}, min slack {worst[0]:.4f} at d = {worst[1]:.4g}")
        sys.stdout.flush()


if __name__ == "__main__":
    import sys
    parts = sys.argv[1:] or ["A", "B", "C"]
    for p in parts:
        {"A": check_A, "A2": check_A2, "A3": check_A3, "B": check_B, "C": check_C, "S": check_S,
         "D": check_D}[p]()
