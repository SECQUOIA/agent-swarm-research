"""Random nonconvex QCQP instances: standard alphaBB versus alphaBB-on-augmented-Lagrangian node counts.

Instances: n variables on [-1,1]^n, indefinite quadratic objective, two indefinite quadratic inequalities,
one quadratic equality.  Box bounds are included as linear inequality constraints so that the
augmented Lagrangian carries their multipliers when a bound is active at the minimizer.

Reference solve: the standard scheme at eps_ref, then SLSQP polish of the best feasible relaxation point;
KKT multipliers by least squares on the active set; instances are kept only if the polished point is
feasible within 1e-9, KKT residual < 1e-7, LICQ (active gradients full rank), strict complementarity
(all active multipliers > 1e-3) and second-order sufficiency (projected Lagrangian Hessian minimum
eigenvalue > 1e-3) hold numerically, and the reference lower bound certifies global optimality within eps_ref.
Everything is floating point and uncertified.

Run: conda run -n minlp-notes python code/augmented_lagrangian_bb/random_instances.py [n_inst] [n] [seed]
"""
import math
import sys
import time

import numpy as np
import sympy as sp
from scipy.optimize import minimize

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from albb import Problem, branch_and_bound, standard_bound, choose_rho, convexity_radius  # noqa: E402


def make_instance(n, rng):
    def symq(scale):
        A = rng.normal(size=(n, n))
        return scale * (A + A.T) / 2

    Q = symq(1.0)
    c = rng.normal(size=n)
    P1, p1 = symq(1.0), rng.normal(size=n)
    P2, p2 = symq(1.0), rng.normal(size=n)
    R, r = symq(1.0), rng.normal(size=n)
    # choose right-hand sides so that a random point x0 is feasible with g1 active-ish
    x0 = rng.uniform(-0.6, 0.6, size=n)
    b1 = x0 @ P1 @ x0 + p1 @ x0 + 0.0
    b2 = x0 @ P2 @ x0 + p2 @ x0 + 0.3
    b = x0 @ R @ x0 + r @ x0

    def quad(M, v, x):
        return sum(M[i, j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(v[i] * x[i] for i in range(n))

    def f(x):
        return quad(Q, c, x)

    def gs(x):
        out = [quad(P1, p1, x) - b1, quad(P2, p2, x) - b2]
        for i in range(n):
            out.append(x[i] - 1)
            out.append(-1 - x[i])
        return out

    def hs(x):
        return [quad(R, r, x) - b]

    data = dict(Q=Q, c=c, P1=P1, p1=p1, b1=b1, P2=P2, p2=p2, b2=b2, R=R, r=r, b=b)
    return f, gs, hs, data


def kkt_analysis(P, x):
    """Least-squares multipliers on the active set; returns (mu, lam, info)."""
    n = P.n
    gvals = np.array([g.v(x) for g in P.gs])
    active = [j for j, gv in enumerate(gvals) if gv > -1e-6]
    G = np.array([P.gs[j].g(x) for j in active], float).reshape(len(active), n)
    Hh = np.array([h.g(x) for h in P.hs], float).reshape(len(P.hs), n)
    A = np.vstack([G, Hh]) if len(active) + len(P.hs) > 0 else np.zeros((0, n))
    gradf = np.array(P.f.g(x), float)
    sol, *_ = np.linalg.lstsq(A.T, -gradf, rcond=None) if A.shape[0] > 0 else (np.zeros(0),)
    mu = np.zeros(len(P.gs))
    for idx, j in enumerate(active):
        mu[j] = sol[idx]
    lam = sol[len(active):] if len(P.hs) > 0 else np.zeros(0)
    resid = np.linalg.norm(gradf + A.T @ sol) if A.shape[0] > 0 else np.linalg.norm(gradf)
    licq = (np.linalg.matrix_rank(A, tol=1e-8) == A.shape[0]) if A.shape[0] > 0 else True
    sc = all(mu[j] > 1e-3 for j in active)
    # projected Hessian of the Lagrangian on the null space of A
    HL = np.array(P.f.H(x), float)
    for j, m in enumerate(mu):
        HL += m * np.array(P.gs[j].H(x), float)
    for k, l in enumerate(lam):
        HL += l * np.array(P.hs[k].H(x), float)
    if A.shape[0] > 0:
        _, s, vt = np.linalg.svd(A)
        rank = int((s > 1e-8).sum())
        N = vt[rank:].T
    else:
        N = np.eye(n)
    if N.shape[1] == 0:
        sosc_eig = math.inf
    else:
        sosc_eig = float(np.linalg.eigvalsh(N.T @ HL @ N).min())
    hl_eig = float(np.linalg.eigvalsh(HL).min())
    return mu, lam, dict(active=active, resid=resid, licq=licq, sc=sc, sosc_eig=sosc_eig,
                         hl_min_eig=hl_eig, viol=float(max([0.0] + [gv for gv in gvals] + [abs(h.v(x)) for h in P.hs])))


def reference_solve(P, eps_ref=1e-7, max_nodes=20000):
    """Standard-scheme B&B with incumbent updates from polished relaxation points (numerical)."""
    import heapq
    lo = np.array([l for l, _ in P.root]); hi = np.array([u for _, u in P.root])

    def polish(x0):
        cons = [{"type": "ineq", "fun": (lambda x, g=g: -g.v(x)), "jac": (lambda x, g=g: -np.array(g.g(x), float))} for g in P.gs]
        cons += [{"type": "eq", "fun": (lambda x, h=h: h.v(x)), "jac": (lambda x, h=h: np.array(h.g(x), float))} for h in P.hs]
        r = minimize(lambda x: P.f.v(x), x0, jac=lambda x: np.array(P.f.g(x), float), bounds=list(zip(lo, hi)),
                     constraints=cons, method="SLSQP", options={"ftol": 1e-15, "maxiter": 500})
        viol = max([0.0] + [g.v(r.x) for g in P.gs] + [abs(h.v(r.x)) for h in P.hs])
        return (r.x, float(r.fun)) if viol <= 1e-9 else (None, math.inf)

    UB, xbest = math.inf, None
    # multistart polish for an initial incumbent
    rng = np.random.default_rng(1)
    for _ in range(20):
        x, v = polish(lo + rng.random(P.n) * (hi - lo))
        if v < UB:
            UB, xbest = v, x
    heap = [(standard_bound(P, P.root), 0, P.root)]
    cnt, nodes = 1, 0
    while heap:
        L, _, box = heapq.heappop(heap)
        nodes += 1
        if L >= UB - eps_ref:
            continue
        if nodes > max_nodes:
            return None
        widths = [u - l for (l, u) in box]
        i = int(np.argmax(widths)); l, u = box[i]; mid = 0.5 * (l + u)
        for child in ((l, mid), (mid, u)):
            nb = list(box); nb[i] = child; nb = tuple(nb)
            Lc = standard_bound(P, nb)
            if Lc < UB - eps_ref:
                # try to improve the incumbent from the child's center
                x, v = polish(np.array([0.5 * (a + b) for a, b in nb]))
                if v < UB:
                    UB, xbest = v, x
                heapq.heappush(heap, (Lc, cnt, nb)); cnt += 1
    LB = min([UB] + [t[0] for t in heap]) if heap else UB
    return xbest, UB, nodes


def main():
    n_inst = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = np.random.default_rng(seed)
    eps_list = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
    kept = 0
    tried = 0
    print(f"n={n}, seed={seed}, eps_ref=1e-7; rho = 2*rho_min+1 (choose_rho)")
    while kept < n_inst and tried < 10 * n_inst:
        tried += 1
        f, gs, hs, data = make_instance(n, rng)
        P = Problem(f"R{tried}", n, f, gs, hs, [(-1.0, 1.0)] * n, [0.0] * n, 0.0, [0.0] * (2 + 2 * n), [0.0])
        t0 = time.time()
        ref = reference_solve(P)
        if ref is None:
            print(f"  instance {tried}: reference node limit; skipped")
            continue
        xbest, UB, nodes_ref = ref
        if xbest is None:
            print(f"  instance {tried}: no feasible point; skipped")
            continue
        mu, lam, info = kkt_analysis(P, xbest)
        ok = info["resid"] < 1e-6 and info["licq"] and info["sc"] and info["sosc_eig"] > 1e-3 and info["viol"] <= 1e-9
        print(f"  instance {tried}: f*={UB:.10f} ref_nodes={nodes_ref} active={info['active']} "
              f"resid={info['resid']:.1e} LICQ={info['licq']} SC={info['sc']} SOSC_eig={info['sosc_eig']:.3g} "
              f"HessL_min={info['hl_min_eig']:.3g} ({time.time()-t0:.0f}s) -> {'kept' if ok else 'rejected'}")
        if not ok:
            continue
        kept += 1
        P.zstar, P.fstar, P.mu, P.lam = np.array(xbest), UB, mu, lam
        rho = choose_rho(P)
        print(f"   rho_auto = {rho:.4g}; convexity radius: " + ", ".join(f"rho={r_:g}: {convexity_radius(P, r_):.4g}" for r_ in (rho, 10.0)))
        print("   eps      std:nodes depth | std+AL:nodes depth AL_exact | AL only:nodes depth")
        for eps in eps_list:
            s1 = branch_and_bound(P, eps, use_std=True, use_al=False, rho=rho)
            s2 = branch_and_bound(P, eps, use_std=True, use_al=True, rho=rho)
            s3 = branch_and_bound(P, eps, use_std=False, use_al=True, rho=rho)
            fmt = lambda s: (f"{s['nodes']:6d} {s['max_depth']:4d}" if s['nodes'] is not None else "  limit    ")
            print(f"  {eps:7.0e}  {fmt(s1)}   |  {fmt(s2)} {s2['al_exact_boxes'] if s2['nodes'] else 0:5d}    |  {fmt(s3)}")
    print("done")


if __name__ == "__main__":
    main()
