"""Minor cuts at McCormick LP vertices of random bipartite bilinear programs (note, Section 7.2).

Instance: x in [lx, ux]^p, y in [ly, uy]^q, X_ik for every product x_i y_k with its McCormick
envelope, NLIN random linear rows over (x, y), random objective over (x, y, X).  At an optimal
HiGHS basis take the most violated 2x2 minor M = [[X_i1k1, X_i1k2], [X_i2k1, X_i2k2]] (largest
|det|; columns swapped if det < 0, as SCIP does) and the projected basis cone.  Report
  * z_K and the one-cut ratios z_family / z_K for scip, bcm, pr, orbit (corner increments);
  * the LP bound after adding each family's best cut, and the corner-optimal cut w^T lam >= z_K,
    as fractions of the single-minor gap z_1 - z_LP, z_1 = min{c^T x : x in P, det M = 0} (SCIP).
LP helpers (solve_lp, basis_cone, lp_with_cut) are reused from the sfree note's exp_mccormick.py.
Usage: python3 exp_lp.py SEED NTRIALS P Q NLIN OUT.jsonl
"""
import sys
import json
import warnings
import numpy as np
import pyscipopt as ps
warnings.filterwarnings('ignore')
from minor_core import (zK, family_bounds, mat, vec, polar_rotation, step, precondition, FamilySolver,
                        bcm_best, nearest_orbit, I2, J2, SFREE)  # noqa: F401
sys.path.insert(0, SFREE)
from exp_mccormick import solve_lp, basis_cone, lp_with_cut  # noqa: E402


def make_instance(rng, p, q, nlin):
    n = p + q + p * q
    lo = np.concatenate([rng.uniform(-1, 0.5, p + q), np.zeros(p * q)])
    hi = np.concatenate([lo[:p + q] + rng.uniform(0.5, 2, p + q), np.zeros(p * q)])
    idx = {}
    A, b = [], []
    for i in range(p):
        for k in range(q):
            e = p + q + i * q + k
            idx[(i, k)] = e
            xi, yk = i, p + k
            c = [lo[xi] * lo[yk], lo[xi] * hi[yk], hi[xi] * lo[yk], hi[xi] * hi[yk]]
            lo[e], hi[e] = min(c), max(c)
            for (a_, b_, s) in [(lo[xi], lo[yk], -1), (hi[xi], hi[yk], -1), (lo[xi], hi[yk], 1), (hi[xi], lo[yk], 1)]:
                row = np.zeros(n)
                if s == -1:     # X >= b_ x + a_ y - a_ b_
                    row[xi], row[yk], row[e] = b_, a_, -1.0
                    A.append(row); b.append(a_ * b_)
                else:           # X <= b_ x + a_ y - a_ b_
                    row[xi], row[yk], row[e] = -b_, -a_, 1.0
                    A.append(row); b.append(-a_ * b_)
    for _ in range(nlin):
        row = np.zeros(n)
        row[:p + q] = rng.normal(size=p + q)
        mid = (lo + hi) / 2
        A.append(row); b.append(row @ mid + abs(row) @ (hi - lo) * 0.15)
    c = rng.normal(size=n)
    return dict(p=p, q=q, n=n, lo=lo, hi=hi, A=np.array(A), b=np.array(b), c=c, idx=idx)


def single_minor_bound(I, vars4, timelimit=60):
    m = ps.Model()
    m.hideOutput()
    m.setParam('limits/time', timelimit)
    n = I['n']
    xs = [m.addVar(lb=I['lo'][v], ub=I['hi'][v]) for v in range(n)]
    for k_ in range(len(I['b'])):
        m.addCons(ps.quicksum(I['A'][k_, v] * xs[v] for v in range(n) if I['A'][k_, v] != 0) <= I['b'][k_])
    a, b_, c_, d = (xs[v] for v in vars4)
    m.addCons(a * d - b_ * c_ == 0)
    m.setObjective(ps.quicksum(I['c'][v] * xs[v] for v in range(n)))
    m.optimize()
    return m.getDualbound(), m.getStatus()


def alphas_of(FT, sbar, P):
    return np.array([step(FT, sbar, P[:, j]) for j in range(P.shape[1])])


if __name__ == '__main__':
    seed, T, p, q, nlin, out = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                                int(sys.argv[5]), sys.argv[6])
    rng = np.random.default_rng(seed)
    f = open(out, 'w')
    for trial in range(T):
        I = make_instance(rng, p, q, nlin)
        o = solve_lp(I)
        if o is None:
            continue
        h, A, bb = o
        bc = basis_cone(I, h, A, bb)
        if bc is None:
            continue
        x, R, w, Ab, rhs, zlp = bc
        best = None
        nviol = 0
        for i1 in range(p):
            for i2 in range(i1 + 1, p):
                for k1 in range(q):
                    for k2 in range(k1 + 1, q):
                        v4 = [I['idx'][(i1, k1)], I['idx'][(i1, k2)], I['idx'][(i2, k1)], I['idx'][(i2, k2)]]
                        s = x[v4]
                        dt = s[0] * s[3] - s[1] * s[2]
                        if abs(dt) > 1e-6:
                            nviol += 1
                            if best is None or abs(dt) > abs(best[0]):
                                best = (dt, v4)
        if best is None or abs(best[0]) < 1e-4:
            continue
        dt, v4 = best
        v4s = v4 if dt > 0 else [v4[1], v4[0], v4[3], v4[2]]
        sbar = x[v4s]
        P = R[v4s, :]
        keep = np.abs(P).max(axis=0) > 1e-12          # rays that move the minor
        nz = int(np.sum(w[keep] < 1e-9))
        wpos = np.maximum(w, 1e-9 * max(1.0, w.max()))
        zk = zK(sbar, P[:, keep], wpos[keep])
        if not np.isfinite(zk) or zk <= 1e-9:
            f.write(json.dumps(dict(trial=trial, skipped='zK=%r' % zk, nzero_w=nz)) + '\n')
            continue
        z1, st = single_minor_bound(I, v4)
        gap = z1 - zlp
        fb = family_bounds(sbar, P[:, keep], wpos[keep], zk, iters=36)
        # explicit sets for the LP re-solve
        al = {}
        al['scip'] = alphas_of(polar_rotation(mat(sbar)).T, sbar, P)
        v_b, phi = bcm_best(sbar, P[:, keep], wpos[keep])
        al['bcm'] = alphas_of(np.cos(phi) * I2 + np.sin(phi) * J2, sbar, P) if phi is not None else None
        sbI, PI = precondition(sbar, P)
        for fam in ('pr', 'orbit'):
            c_, h_, FT = FamilySolver(fam, sbI, PI[:, keep], wpos[keep]).best(zk, iters=36)
            al[fam] = alphas_of(FT, sbI, PI) if FT is not None else None
        # tie-break variant: the orbit set nearest to SCIP's set among those attaining the orbit bound
        zo = min(fb['orbit']['ratio'], 1.0) * zk * (1 - 1e-6)
        Ptar = polar_rotation(mat(sbar)).T @ mat(sbar)          # SCIP's set in preconditioned coordinates
        FTn = nearest_orbit(sbI, PI[:, keep], wpos[keep], zo, Ptar)
        al['orbit_near_scip'] = alphas_of(FTn, sbI, PI) if FTn is not None else None
        near_ratio = None
        if FTn is not None:
            near_ratio = float(min(np.min([wpos[j] * a for j, a in enumerate(al['orbit_near_scip']) if keep[j]]), zk) / zk)
        lp = {}
        for fam, a_ in al.items():
            if a_ is None:
                lp[fam] = None
                continue
            coef = np.array([0.0 if not np.isfinite(t) else 1.0 / t for t in a_])
            v = lp_with_cut(I, Ab, rhs, coef)
            lp[fam] = None if v is None else v - zlp
        vcor = lp_with_cut(I, Ab, rhs, wpos * keep / zk)
        lp['corner'] = None if vcor is None else vcor - zlp
        fr = (lambda v: None if (v is None or gap <= 1e-7) else float(min(max(v, 0.0), gap) / gap))
        rec = dict(trial=trial, nviol=nviol, det=float(dt), zK=float(zk), z1_status=st, gap=float(gap),
                   nzero_w=nz, ratios={k: v['ratio'] for k, v in fb.items()},
                   incr={k: fr(v['ratio'] * zk) for k, v in fb.items()},
                   lp={k: fr(v) for k, v in lp.items()}, zK_over_gap=fr(zk), near_ratio=near_ratio)
        f.write(json.dumps(rec) + '\n')
        f.flush()
    f.close()
