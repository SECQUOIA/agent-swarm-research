"""Lifted certificate on extension-n2.md's two-state example A- (kappa_tau = -0.3), FLOAT screening.

The Euler transcription of A- is nonconvex in u in hundreds of directions (run_identity.py), so the
kappa-split convexification does not apply.  Here: the transferred tangential family of window-exactness.md
Section 7.5 (eps = 0.02, delta_1 = 0.1; imported read-only from window/n2win.py) fails only at the switching
stage n.  Branch on u_n:
  * central node: lifted family (slopes = costates of z(v), v = u_n), interval V of v on which every stage
    t != n has zero loss over the reachable box (found by bisection on each side; the zero-loss set is an
    interval when the box constraint on d is inactive, kappa-negative.md Lemma 3.2); bound
    min_{v in V} J(z(v)) = J(zbar) + H_nn (v - ubar_n)^2 / 2 >= J(zbar);
  * outer nodes {u_n in [l, r]}: node KKT point (active-set Newton on the exact quadratic J with the node
    bounds), transferred curvatures with the node costates as slopes, stage losses over the reachable box.
usage: OMP_NUM_THREADS=1 python3 run_n2lift.py   ->  logs/n2lift.json
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "window"))
sys.path.insert(0, os.path.join(HERE, "..", "n2"))
sys.path.insert(0, HERE)
from n2win import EXAMPLES, dz, transferred  # noqa: E402
from run_identity import hess2  # noqa: E402


def data_of(p, N, u):
    x, J = dz.simulate(p, N, u)
    P, sig = dz.adjoint(p, N, x, u)
    return dict(N=N, h=p.T / N, u=u, x=x, J=J, p=P, sig=sig)


def losses(p, D, Ps, lo_u, hi_u, skip=()):
    """Stage losses over the reachable box with per-stage control ranges [lo_u, hi_u]."""
    N, x, u = D["N"], D["x"], D["u"]
    lo_b, hi_b = dz.reach_box(p, N, D["h"])
    quads = dz.stage_quadratics(p, D, Ps)
    out = np.zeros(N)
    for t, (g, hs, K, hb, hk) in enumerate(quads):
        if t in skip:
            continue
        gg = np.array([g[0], g[1], hs])
        Hm = np.zeros((3, 3))
        Hm[:2, :2] = K
        Hm[:2, 2] = Hm[2, :2] = hb
        Hm[2, 2] = hk
        if t == 0:
            lo = np.array([0.0, 0.0, lo_u[0] - u[0]])
            hi = np.array([0.0, 0.0, hi_u[0] - u[0]])
        else:
            lo = np.array([lo_b[t, 0] - x[t, 0], lo_b[t, 1] - x[t, 1], lo_u[t] - u[t]])
            hi = np.array([hi_b[t, 0] - x[t, 0], hi_b[t, 1] - x[t, 1], hi_u[t] - u[t]])
        out[t] = -dz.box_min_quadratic(0.0, gg, Hm, lo, hi)
    gN = p.dPhi(*x[N]) - D["p"][N]
    HN = p.Phixx(*x[N]) - Ps[N]
    lossN = -dz.box_min_quadratic(0.0, gN, HN, lo_b[N] - x[N], hi_b[N] - x[N])
    return out, lossN


def node_kkt(p, N, u0, H, lo_u, hi_u, maxit=200, tol=1e-13):
    """Active-set Newton for min J over the box (J exact quadratic, Hessian H)."""
    h = p.T / N
    u = np.clip(u0.copy(), lo_u, hi_u)
    for _ in range(maxit):
        D = data_of(p, N, u)
        sig = D["sig"]
        inter = [t for t in range(N) if lo_u[t] + 1e-15 < u[t] < hi_u[t] - 1e-15]
        viol = [t for t in range(N) if (u[t] >= hi_u[t] - 1e-15 and sig[t] > tol) or (u[t] <= lo_u[t] + 1e-15 and sig[t] < -tol)]
        F = sorted(set(inter) | set(viol))
        if not viol and (not inter or np.abs(sig[inter]).max() < tol):
            break
        step = np.linalg.solve(H[np.ix_(F, F)], -h * sig[F])
        u[F] = np.clip(u[F] + step, lo_u[F], hi_u[F])
    return data_of(p, N, u)


def main():
    p = EXAMPLES["Aminus"]
    out = []
    for N in (500, 1000, 2000, 4000):
        t0 = time.time()
        kk = dz.solve_kkt(p, N)
        h = kk["h"]
        Ps, _ = transferred(p, kk, 0.02, 0.1)
        D0 = data_of(p, N, kk["u"].copy())
        one = np.ones(N)
        L0, LN0 = losses(p, D0, Ps, -one, one)
        tol = 1e-12 * h * h
        fail = [int(t) for t in np.where(L0 > tol)[0]]
        rec = dict(N=N, frac=sorted(kk["fracset"]), failing=[(t, L0[t] / h ** 2) for t in fail], terminal_loss=LN0)
        if not fail:
            rec["certificate"] = "transferred family alone"
            out.append(rec)
            print(json.dumps(rec), flush=True)
            continue
        assert len(fail) == 1
        n = fail[0]
        H = hess2(dict(rho=p.rho, k1=p.k1, k2=p.k2, q=p.q, c=p.c), N)
        ub = kk["u"][n]

        def lifted_ok(v):
            u = kk["u"].copy()
            u[n] = v
            D = data_of(p, N, u)
            L, LN = losses(p, D, Ps, -one, one, skip=(n,))
            # stage n has no control in the lifted problem: its state part only
            lo_n, hi_n = one.copy() * -1, one.copy()
            lo_n[n] = hi_n[n] = v
            Ln, _ = losses(p, D, Ps, lo_n, hi_n)
            return max(L.max(), Ln[n], LN) <= tol

        V = []
        for end in (-1.0, 1.0):
            if lifted_ok(end):
                V.append(end)
                continue
            a, b = ub, end                      # lifted_ok(a) holds (anchor), lifted_ok(b) fails
            assert lifted_ok(a)
            for _ in range(50):
                m = (a + b) / 2
                if lifted_ok(m):
                    a = m
                else:
                    b = m
            V.append(a)
        Hnn = H[n, n]
        rec.update(n=n, u_n=ub, Hnn_over_h2=Hnn / h ** 2, V=V, lifted_bound_minus_J=0.0)
        # outer nodes
        outer = []
        for (l, r) in ((-1.0, V[0]), (V[1], 1.0)):
            if r - l <= 1e-12:
                continue
            lo_u, hi_u = -one.copy(), one.copy()
            lo_u[n], hi_u[n] = l, r
            A = node_kkt(p, N, kk["u"], H, lo_u, hi_u)
            LA, LNA = losses(p, A, Ps, lo_u, hi_u)
            B = A["J"] - LA.sum() - LNA
            outer.append(dict(l=l, r=r, anchor_u_n=A["u"][n], J_anchor_minus_J_over_h2=(A["J"] - kk["J"]) / h ** 2,
                              bound_minus_J_over_h2=(B - kk["J"]) / h ** 2,
                              worst=[(int(t), LA[t] / h ** 2) for t in np.argsort(-LA)[:2] if LA[t] > tol]))
        rec.update(outer=outer, certified=all(o["bound_minus_J_over_h2"] >= 0 for o in outer), time=time.time() - t0)
        out.append(rec)
        print(json.dumps(rec, default=float), flush=True)
    with open(os.path.join(HERE, "logs", "n2lift.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
