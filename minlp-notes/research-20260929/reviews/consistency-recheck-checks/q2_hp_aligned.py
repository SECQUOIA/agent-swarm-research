"""Recheck Q2: aligned hp value in Section 7.5 (two cells split at c0).

psi(s) = -|s - c0| + 0.3 sin(3s) + 0.2 s^2, c0 = 1/sqrt(7). On each cell psi
is analytic; the zero-width band gives gap = 2 max_D E_p(psi|D)
(Proposition 2.3 + Corollary 2.2(2)). Degree p >= 2 absorbs the linear and
quadratic parts, so E_p(psi|D) = 0.3 E_p(sin(3s)|D) for p >= 2.

Remez exchange in 40-digit arithmetic (mpmath), extrema refined by
golden-section search; returns the levelled error (de la Vallee Poussin
lower bound) and the max error (upper bound)."""
import mpmath as mp

mp.mp.dps = 40
c0 = 1 / mp.sqrt(7)


def psi(s):
    return -abs(s - c0) + mp.mpf("0.3") * mp.sin(3 * s) + mp.mpf("0.2") * s ** 2


def remez_cell(f, a, b, p, iters=40):
    # Chebyshev basis on the cell via t in [-1, 1]
    tof = lambda t: (a + b) / 2 + (b - a) / 2 * t
    basis = lambda t: [mp.chebyt(k, t) for k in range(p + 1)]
    ref = [mp.cos(mp.pi * (p + 1 - i) / (p + 1)) for i in range(p + 2)]
    for it in range(iters):
        A = mp.matrix([basis(t) + [(-1) ** i] for i, t in enumerate(ref)])
        rhs = mp.matrix([f(tof(t)) for t in ref])
        sol = mp.lu_solve(A, rhs)
        c = [sol[k] for k in range(p + 1)]
        err = lambda t: f(tof(t)) - mp.fsum(ck * mp.chebyt(k, t) for k, ck in enumerate(c))
        # locate extrema: sample, then golden-section refine
        M = 40 * (p + 2)
        ts = [mp.cos(mp.pi * (M - j) / M) for j in range(M + 1)]
        es = [err(t) for t in ts]
        cand = [0] + [j for j in range(1, M) if (es[j] - es[j - 1]) * (es[j + 1] - es[j]) <= 0] + [M]
        pts = []
        for j in cand:
            s = 1 if es[j] >= 0 else -1
            lo, hi = ts[max(j - 1, 0)], ts[min(j + 1, M)]
            g = lambda t: -s * err(t)
            # golden section
            gr = (mp.sqrt(5) - 1) / 2
            x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
            f1, f2 = g(x1), g(x2)
            for _ in range(120):
                if f1 < f2:
                    hi, x2, f2 = x2, x1, f1
                    x1 = hi - gr * (hi - lo); f1 = g(x1)
                else:
                    lo, x1, f1 = x1, x2, f2
                    x2 = lo + gr * (hi - lo); f2 = g(x2)
            best = min([(g(ts[j]), ts[j]), (f1, x1)], key=lambda z: z[0])
            pts.append((best[1], err(best[1])))
        pts.sort(key=lambda z: z[0])
        grp = []
        for t, e in pts:
            if grp and mp.sign(grp[-1][1]) == mp.sign(e):
                if abs(e) > abs(grp[-1][1]):
                    grp[-1] = (t, e)
            else:
                grp.append((t, e))
        emax = max(abs(e) for _, e in grp)
        while len(grp) > p + 2:
            if abs(grp[0][1]) < abs(grp[-1][1]):
                grp.pop(0)
            else:
                grp.pop()
        assert len(grp) == p + 2, len(grp)
        lev = min(abs(e) for _, e in grp)
        ref = [t for t, _ in grp]
        if emax - lev < mp.mpf("1e-25") * emax:
            break
    return lev, emax


if __name__ == "__main__":
    for p in [4, 8, 12]:
        res = [remez_cell(psi, a, b, p) for a, b in [(mp.mpf(-1), c0), (c0, mp.mpf(1))]]
        gl = 2 * max(r[0] for r in res)
        gu = 2 * max(r[1] for r in res)
        print(f"p={p:2d} N={2 * (p + 1)}: per-cell E_p = {mp.nstr(res[0][0], 8)}, {mp.nstr(res[1][0], 8)};"
              f" gap in [{mp.nstr(gl, 8)}, {mp.nstr(gu, 8)}]")
