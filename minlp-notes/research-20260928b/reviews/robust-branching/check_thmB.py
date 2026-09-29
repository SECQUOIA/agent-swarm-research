"""Independent checks of Theorem B (robust-branching.md, Section 3). Review code only.

Chain: kink at relative distance d from the nearer end; draw theta ~ U[t0, t1]; theta <= d splits at
the kink; otherwise r = d/theta and d' = min(r, 1-r). S = number of splits (including the last).

[B1] constants delta, A, B, 1/mu for [0.1, 0.3]; both upper bounds and the lower bound of Theorem B.
[B2] E[S] by a Nystrom discretisation of E(d) = 1 + (1/D) int_{max(d,t0)}^{t1} E(d'(theta)) dtheta:
     log grid in d, Gauss-Legendre in theta with the substitution theta = d (1 + t^2) on (d, 2d) to
     absorb the log singularity, linear interpolation in log d, direct linear solve.
[B3] Monte Carlo (numpy, 10^7 chains per entry): E[S], quantiles; windows [0.1,0.3], [0.15,0.25],
     [0.19,0.21].
[B4] supersolution slack g(d) - 1 - E[g(d'); theta > d] in closed form (mpmath), fine grid of d.
[B5] 1D node counts E[T] with eps > 0 (exact open test (a-l)(u-a) > eps, alpha = 1), 10^6 runs.
"""
import math
import sys

import mpmath as mp
import numpy as np


def consts(t0, t1):
    D = t1 - t0
    delta = math.log(1 / t1) - t0 / D
    A = 1 + t1 / (D * delta)
    B = 1 / delta
    mu = ((t1 - t1 * math.log(t1)) - (t0 - t0 * math.log(t0))) / D   # E[log(1/theta)]
    return D, delta, A, B, mu


def part_B1():
    print("[B1] constants and bounds of Theorem B, window [0.1, 0.3]")
    t0, t1 = 0.1, 0.3
    D, delta, A, B, mu = consts(t0, t1)
    print(f"  delta = {delta:.5f}, A = {A:.5f}, B = {B:.5f}, mu = {mu:.5f}, 1/mu = {1 / mu:.5f}")
    for name, a in (("1/6", 1 / 6), ("3/238", 3 / 238), ("0.1999", 0.1999), ("1e-4", 1e-4), ("1e-8", 1e-8)):
        d0 = min(a, 1 - a)
        b1 = A + B * math.log(1 / d0)
        b2 = (math.log(1 / d0) - math.log(2)) / mu + A + B * math.log(2 / t0) if d0 < t0 / 2 else float("nan")
        lb = (math.log(1 / d0) - math.log(2 / t0)) / mu
        print(f"  a = {name}: first bound {b1:.3f}; second bound (d0 < t0/2) {b2:.3f}; lower bound {lb:.3f}")


def nystrom(t0, t1, N=6000, dmin=1e-18, nq=48):
    D = t1 - t0
    # grid: log-spaced plus the breakpoints where E has kinks
    brk = [t0 / 2, t1 / 2, t0, t1, 0.5]
    g = np.unique(np.concatenate([np.geomspace(dmin, 0.5, N), brk]))
    lg = np.log(g)
    n = g.size
    M = np.zeros((n, n))
    xg, wg = np.polynomial.legendre.leggauss(nq)

    def add(i, th, w):
        # contribution sum_j w_j E(d'(th_j)) / D into row i
        r = g[i] / th
        dn = np.minimum(r, 1 - r)
        dn = np.clip(dn, g[0], 0.5)
        x = np.log(dn)
        k = np.clip(np.searchsorted(lg, x) - 1, 0, n - 2)
        lam = (x - lg[k]) / (lg[k + 1] - lg[k])
        np.add.at(M[i], k, w * (1 - lam) / D)
        np.add.at(M[i], k + 1, w * lam / D)

    for i, d in enumerate(g):
        lo = max(d, t0)
        if lo >= t1:
            continue
        # piece 1: theta in (d, 2d) intersected with [lo, t1]; theta = d (1 + t^2), t in [ta, tb]
        p, q = lo, min(2 * d, t1)
        if q > p:
            ta, tb = math.sqrt(p / d - 1), math.sqrt(q / d - 1)
            # split in a few panels for accuracy
            edges = np.linspace(ta, tb, 5)
            for e0, e1 in zip(edges[:-1], edges[1:]):
                t = 0.5 * (e1 - e0) * xg + 0.5 * (e1 + e0)
                th = d * (1 + t * t)
                w = 0.5 * (e1 - e0) * wg * 2 * d * t
                add(i, th, w)
        p, q = max(lo, 2 * d), t1
        if q > p:
            edges = np.geomspace(p, q, 9)
            for e0, e1 in zip(edges[:-1], edges[1:]):
                th = 0.5 * (e1 - e0) * xg + 0.5 * (e1 + e0)
                w = 0.5 * (e1 - e0) * wg
                add(i, th, w)
    E = np.linalg.solve(np.eye(n) - M, np.ones(n))
    return g, E


def part_B2():
    print("[B2] Nystrom solution of the E[S] equation")
    for (t0, t1) in ((0.1, 0.3), (0.15, 0.25), (0.19, 0.21)):
        for N in (3000, 6000):
            g, E = nystrom(t0, t1, N=N)
            f = lambda d: float(np.interp(math.log(d), np.log(g), E))  # noqa: E731
            vals = {name: f(min(a, 1 - a)) for name, a in (("1/6", 1 / 6), ("3/238", 3 / 238), ("0.1999", 0.1999),
                                                          ("1e-4", 1e-4), ("1e-8", 1e-8), ("1e-12", 1e-12))}
            slope = (f(1e-14) - f(1e-8)) / math.log(1e6)
            print(f"  [{t0}, {t1}] N={N}: " + ", ".join(f"E[S]({k}) = {v:.4f}" for k, v in vals.items())
                  + f"; slope in log(1/d) on [1e-14, 1e-8]: {slope:.5f}; 1/mu = {1 / consts(t0, t1)[4]:.5f}")
            sys.stdout.flush()


def mc(d0, t0, t1, n, rng, batch=2_000_000):
    Ss = []
    left = n
    while left > 0:
        m = min(batch, left)
        d = np.full(m, d0)
        S = np.zeros(m, dtype=np.int64)
        alive = np.arange(m)
        while alive.size:
            th = rng.uniform(t0, t1, alive.size)
            S[alive] += 1
            fail = th > d[alive]
            idx = alive[fail]
            r = d[idx] / th[fail]
            d[idx] = np.minimum(r, 1 - r)
            alive = idx
        Ss.append(S)
        left -= m
    return np.concatenate(Ss)


def part_B3():
    print("[B3] Monte Carlo, 10^7 chains per entry")
    rng = np.random.default_rng(987654321)
    for (t0, t1), As in (((0.1, 0.3), (1 / 6, 3 / 238, 0.1999, 1e-4, 1e-8)),
                         ((0.15, 0.25), (1 / 6,)), ((0.19, 0.21), (1 / 6,))):
        for a in As:
            S = mc(min(a, 1 - a), t0, t1, 10 ** 7, rng)
            q = np.quantile(S, [0.5, 0.99, 0.9999])
            print(f"  [{t0}, {t1}] a = {a:.6g}: E[S] = {S.mean():.4f} +- {S.std() / math.sqrt(S.size):.4f}; "
                  f"median/99%/99.99% = {q[0]:.0f}/{q[1]:.0f}/{q[2]:.0f}; max {S.max()}")
            sys.stdout.flush()


def slack_curve(t0, t1, ds):
    mp.mp.dps = 30
    D, delta, A, B, mu = consts(t0, t1)
    A, B, D, t0m, t1m = mp.mpf(A), mp.mpf(B), mp.mpf(D), mp.mpf(t0), mp.mpf(t1)
    F1 = lambda th: th * mp.log(th) - th  # noqa: E731
    out = []
    for d in ds:
        d = mp.mpf(d)
        g = A + B * mp.log(1 / d)
        lo = max(d, t0m)
        if lo >= t1m:
            out.append(float(g - 1))
            continue
        tot = (t1m - lo) * A
        p, q = lo, min(2 * d, t1m)
        if q > p:
            F2 = lambda th: (th - d) * mp.log(th - d) - (th - d) if th > d else mp.mpf(0)  # noqa: E731
            tot += B * ((F1(q) - F1(p)) - (F2(q) - F2(p)))
        p, q = max(lo, 2 * d), t1m
        if q > p:
            tot += B * ((F1(q) - F1(p)) - mp.log(d) * (q - p))
        out.append(float(g - 1 - tot / D))
    return np.array(out)


def part_B4():
    print("[B4] supersolution slack of Theorem B, closed form, 20,000-point grid per window")
    for t0, t1 in ((0.1, 0.3), (0.05, 0.35), (0.1, 0.5), (0.01, 0.2), (0.2, 0.5), (0.25, 0.5), (0.05, 0.1)):
        D, delta, A, B, mu = consts(t0, t1)
        if delta <= 0:
            print(f"  [{t0}, {t1}]: delta = {delta:.4f} <= 0, theorem does not apply")
            continue
        ds = np.unique(np.concatenate([np.geomspace(1e-12, 0.5, 10000), np.linspace(t0 * 0.9, min(0.5, t1 * 1.1), 10000)]))
        s = slack_curve(t0, t1, ds)
        i = int(np.argmin(s))
        print(f"  [{t0}, {t1}]: delta = {delta:.4f}; min slack {s[i]:.4f} at d = {ds[i]:.5g}; "
              f"limit d->0 (mu/delta - 1) = {mu / delta - 1:.4f}")
        sys.stdout.flush()


def T1d_mc(a, eps, t0, t1, n, rng):
    """1D exact-gap kink, alpha = 1; returns array of T."""
    dl = np.full(n, a)
    du = np.full(n, 1 - a)
    T = np.ones(n, dtype=np.int64)
    alive = np.nonzero(dl * du > eps)[0]
    while alive.size:
        th = rng.uniform(t0, t1, alive.size)
        T[alive] += 2
        w = dl[alive] + du[alive]
        cut = th * w
        left = dl[alive] < cut
        right = (~left) & (du[alive] < cut)
        hit = ~(left | right)
        il, ir = alive[left], alive[right]
        du[il] = cut[left] - dl[il]
        dl[ir] = cut[right] - du[ir]
        keep = alive[~hit]
        alive = keep[dl[keep] * du[keep] > eps]
    return T


def part_B5():
    print("[B5] 1D node counts of the randomized clamp [0.1, 0.3], 10^6 runs")
    rng = np.random.default_rng(13579)
    for a in (1 / 6, 3 / 238):
        for k in (2, 4, 8, 16, 32):
            T = T1d_mc(a, 10.0 ** -k, 0.1, 0.3, 10 ** 6, rng)
            print(f"  a = {a:.6g}, eps = 1e-{k}: E[T] = {T.mean():.3f} +- {T.std() / 1e3:.3f}")
            sys.stdout.flush()


if __name__ == "__main__":
    parts = sys.argv[1:] or ["B1", "B2", "B3", "B4", "B5"]
    for p in parts:
        {"B1": part_B1, "B2": part_B2, "B3": part_B3, "B4": part_B4, "B5": part_B5}[p]()
