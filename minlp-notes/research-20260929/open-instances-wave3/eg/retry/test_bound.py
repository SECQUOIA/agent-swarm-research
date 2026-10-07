"""Sampling soundness test of the full per-box pipeline BB.bound (Taylor/natural models,
row bounds, domain reduction with the objective cut, LP dual, Farkas test).  Not a proof.

For random boxes (near the best point, uniform, integer coordinates fixed or relaxed) and a
cutoff theta (UB + delta, so that many test points qualify), every test point x of the box
that is feasible with margin 1e-9 and has F(x) <= theta must
  (a) lie in the reduced box, and (b) satisfy F(x) >= lb(box) (lb = inf means 'no such point').
Test points: box centre, random points, and local minimizers of F inside the box (SLSQP).
Near-violations (margin < 1e-6) are re-evaluated at 50 digits with mpmath.

    python3 test_bound.py <name> <boxes per family> [seed]
"""
import sys

import mpmath as mp
import numpy as np
from scipy.optimize import minimize

import egbb


def q2mp(q):
    return mp.mpf(q.numerator) / q.denominator


def F_mp(D, x):
    mp.mp.dps = 50
    best = None
    side = []
    for k in range(28):
        s = mp.mpf(0)
        for m in range(D.Mt):
            e = mp.mpf(0)
            for i in range(D.d):
                t = mp.mpf(D.qmu[k][m][i].numerator) / D.qmu[k][m][i].denominator + \
                    mp.mpf(D.qs[i].numerator) / D.qs[i].denominator * mp.mpf(float(x[i]))
                e += mp.mpf(D.qga[k][i].numerator) / D.qga[k][i].denominator * t * t
            s += mp.mpf(D.qa[k][m].numerator) / D.qa[k][m].denominator * mp.exp(e)
        for i in range(D.d):
            s += mp.mpf(D.qlin[k][i].numerator) / D.qlin[k][i].denominator * mp.mpf(float(x[i]))
        if k < 24:
            v = mp.mpf(D.qc[k].numerator) / D.qc[k].denominator + s
            best = v if best is None or v > best else best
        else:
            side.append(s)
    return best, side


def local_in_box(D, lo, hi, x0, isint):
    cont = np.where(~isint)[0]
    if len(cont) == 0:
        return x0

    def full(z):
        x = x0.copy(); x[cont] = z; return x

    def f(z):
        return D.F(full(z)[None])[0][0]
    r = minimize(f, x0[cont], bounds=list(zip(lo[cont], hi[cont])), method="Powell",
                 options=dict(maxiter=400, xtol=1e-9, ftol=1e-12))
    return full(np.clip(r.x, lo[cont], hi[cont]))


def main(name, nb, seed=0):
    bb = egbb.BB(name, 1e-6)
    M = bb.M
    D = M.D
    rng = np.random.default_rng(seed)
    best = {"eg_int_s": [0.5642193457125262, 0.6468471892151673, 1.0, 0.9390699678004698, 2.0, 4.0, 3.0]}
    import explore
    # reference best point: from the exploration log if not listed above
    xs = np.array(best.get(name, (M.lo0 + M.hi0) / 2))
    if name != "eg_int_s":
        import egbb as _e
        pol = _e.make_polish(bb)
        sys.path.insert(0, "../../../open-instances-wave2/small")
        import ev
        vals = ev.read_sol(f"../../sol/{name}.p1.sol")
        x0 = np.array([float(vals.get(n, "0")) for n in D.M["names"]])
        xs = pol(x0)
    UB = float(bb.fpoint(xs[None])[0])
    W = M.hi0 - M.lo0
    fams = []
    for rho in (0.3, 0.1, 0.03, 0.01, 0.001):
        for _ in range(nb):
            c = xs + (rng.random(D.d) - 0.5) * W * rho * 2
            fams.append(("near%g" % rho, c, rho))
    for rho in (0.2, 0.05, 0.01):
        for _ in range(nb):
            c = M.lo0 + rng.random(D.d) * W
            fams.append(("unif%g" % rho, c, rho))
    nviol = 0
    nq = 0
    minmarg = np.inf
    stats = {}
    for fam, c, rho in fams:
        lo = np.clip(c - W * rho / 2, M.lo0, M.hi0)
        hi = np.clip(c + W * rho / 2, M.lo0, M.hi0)
        relax = rng.random() < 0.3
        ci = np.clip(np.round(c[M.isint]), M.lo0[M.isint], M.hi0[M.isint])
        if relax:
            lo[M.isint] = np.clip(ci - 1, M.lo0[M.isint], M.hi0[M.isint])
            hi[M.isint] = np.clip(ci + 1, M.lo0[M.isint], M.hi0[M.isint])
        else:
            lo[M.isint] = ci; hi[M.isint] = ci
        for delta in (0.5, 5.0):
            theta = UB + delta
            lb, nlo, nhi, sc = bb.bound(lo[None], hi[None], theta)
            lb, nlo, nhi = lb[0], nlo[0], nhi[0]
            pts = [0.5 * (lo + hi)]
            for _ in range(60):
                pts.append(lo + rng.random(D.d) * (hi - lo))
            for _ in range(3):
                x0 = lo + rng.random(D.d) * (hi - lo)
                x0[M.isint] = np.round(x0[M.isint])
                pts.append(local_in_box(D, lo, hi, x0, M.isint))
            P = np.array(pts)
            P[:, M.isint] = np.clip(np.round(P[:, M.isint]), lo[M.isint], hi[M.isint])
            f, v, g = D.F(P)
            ok = (v <= -1e-9) & (f <= theta)
            for x, fx in zip(P[ok], f[ok]):
                nq += 1
                inside = np.all(x >= nlo - 1e-12) and np.all(x <= nhi + 1e-12)
                marg = fx - lb
                bad = (not inside) or (marg < 0)
                if np.isfinite(marg):
                    minmarg = min(minmarg, marg)
                if bad or marg < 1e-6:
                    fm, sm = F_mp(D, x)
                    feas = all(sm[j] <= q2mp(D.qghi[24 + j]) if D.qghi[24 + j] is not None else True
                               for j in range(4)) and all(
                        sm[j] >= q2mp(D.qglo[24 + j]) if D.qglo[24 + j] is not None else True
                        for j in range(4))
                    if feas and fm <= theta and ((not inside) or fm < lb):
                        nviol += 1
                        print("VIOLATION", fam, delta, x.tolist(), float(fm), lb, inside)
            stats.setdefault(fam, [0, 0])
            stats[fam][0] += 1
            stats[fam][1] += int(ok.sum())
    print(f"{name}: {len(fams)} boxes x 2 cutoffs, {nq} qualifying feasible points, {nviol} violations, "
          f"smallest margin F - lb = {minmarg:.3e}")
    print("  qualifying points per family:", {k: v[1] for k, v in stats.items()})


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 0)
