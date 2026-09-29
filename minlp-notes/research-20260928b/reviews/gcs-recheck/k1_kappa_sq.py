"""Recheck of Corollary C (exact squared-length constant).

For a polytope D (0 not in D) with vertex rows W:
  kappa_mix  = sup_{p in simplex} (sum p_i |w_i|^2) / |sum p_i w_i|^2   (= sup_D cav(q)/q; the true constant)
      (a) convex program: max geo_mean(1'p, a'p) s.t. |W'p| <= 1, p >= 0  (degree-0 homogenization)
      (b) SLSQP over the simplex (ratio is quasiconcave: linear / convex-positive), non-cvxpy
      (c) best 2-point mixture (lower bound)
  kappa_ball = 1/(1 - tau*),  tau* = min_u max_i | |w_i| u - w_i/|w_i| |^2   (SOCP form, own derivation)
      also the note's linear-row form, whose duals give the Danskin mixture certificate.
Checks: kappa_ball == kappa_mix; best ball contains D; kappa^sq >= sec^2(theta_e); product
bound >= kappa^sq; special sets (balls, radial segment, circular segment, chord segment)."""
import sys
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize, minimize_scalar
from scipy.spatial import ConvexHull
from rc import sec_aperture, SOLVER


def hull_pts(P):
    P = np.asarray(P, float)
    if P.shape[1] == 1 or len(P) <= P.shape[1] + 1:
        return P
    try:
        return P[ConvexHull(P).vertices]
    except Exception:
        return P


def kappa_ball_socp(W):
    n2 = np.linalg.norm(W, axis=1)
    Wh = W / n2[:, None]
    u, r = cp.Variable(W.shape[1]), cp.Variable()
    cons = [cp.norm(n2[i] * u - Wh[i]) <= r for i in range(len(W))]
    cp.Problem(cp.Minimize(r), cons).solve(solver=SOLVER)
    tau = float(r.value) ** 2
    u = np.array(u.value, float)
    return tau, u


def kappa_ball_rows(W):
    """the note's form (linear rows + |u|^2 <= s); duals give the Danskin weights."""
    n2 = np.sum(W ** 2, axis=1)
    u, t, s = cp.Variable(W.shape[1]), cp.Variable(), cp.Variable(nonneg=True)
    rows = [n2[i] * s - 2 * W[i] @ u + 1 <= t for i in range(len(W))]
    cp.Problem(cp.Minimize(t), rows + [cp.sum_squares(u) <= s]).solve(solver=SOLVER)
    mu = np.array([max(0.0, float(c.dual_value)) for c in rows])
    return float(t.value), np.array(u.value, float), mu / mu.sum()


def kappa_mix_geo(W):
    a = np.sum(W ** 2, axis=1)
    p = cp.Variable(len(W), nonneg=True)
    pr = cp.Problem(cp.Maximize(cp.geo_mean(cp.hstack([cp.sum(p), a @ p]))), [cp.norm(W.T @ p) <= 1])
    pr.solve(solver=SOLVER)
    pv = np.maximum(np.array(p.value, float), 0)
    pv /= pv.sum()
    exact_ratio = float(a @ pv / np.sum((W.T @ pv) ** 2))  # exact evaluation of the recovered mixture
    return float(pr.value) ** 2, exact_ratio


def ratio(p, W, a):
    p = np.maximum(p, 0)
    p = p / p.sum()
    return a @ p / np.sum((W.T @ p) ** 2)


def kappa_mix_slsqp(W, rng, starts=4):
    a = np.sum(W ** 2, axis=1)
    k = len(W)
    best = 0.0
    for _ in range(starts):
        x0 = rng.dirichlet(np.ones(k))
        r = minimize(lambda p: -ratio(p, W, a), x0, method="SLSQP", bounds=[(0, 1)] * k,
                     constraints=[{"type": "eq", "fun": lambda p: p.sum() - 1}],
                     options=dict(ftol=1e-14, maxiter=500))
        best = max(best, ratio(r.x, W, a))
    return best


def kappa_pairs(W):
    a = np.sum(W ** 2, axis=1)
    best = 1.0
    for i in range(len(W)):
        for j in range(i + 1, len(W)):
            f = lambda l: -(l * a[i] + (1 - l) * a[j]) / np.sum((l * W[i] + (1 - l) * W[j]) ** 2)
            r = minimize_scalar(f, bounds=(0, 1), method="bounded", options=dict(xatol=1e-12))
            best = max(best, -r.fun, -f(0.0), -f(1.0))
    return best


def min_norm(W):
    p = cp.Variable(len(W), nonneg=True)
    pr = cp.Problem(cp.Minimize(cp.norm(W.T @ p)), [cp.sum(p) == 1])
    pr.solve(solver=SOLVER)
    return float(pr.value)


def analyse(W, rng, tag, rows):
    W = hull_pts(W)
    mnorm = min_norm(W)
    if mnorm < 1e-3:
        return None
    n2 = np.sum(W ** 2, axis=1)
    F = lambda uu: float(np.max(n2 * (uu @ uu) - 2 * W @ uu + 1))   # exact max_i f_{w_i}(u)
    tau_s, u = kappa_ball_socp(W)
    tau2, u2, mu = kappa_ball_rows(W)
    kb_s, kb2 = 1 / (1 - F(u)), 1 / (1 - F(u2))    # each a rigorous upper bound (exact evaluation)
    kb = min(kb_s, kb2)
    if kb2 < kb_s:
        u = u2
    tau = 1 - 1 / kb
    # best ball and its containment
    c = u / np.sum(u ** 2)
    rho = np.sqrt(tau) * np.linalg.norm(c)
    contain = np.max(np.linalg.norm(W - c, axis=1)) - rho
    secB2 = np.sum(c ** 2) / (np.sum(c ** 2) - rho ** 2)
    # Danskin certificate from duals
    wbar = mu @ W
    cert = float(mu @ np.sum(W ** 2, axis=1) / np.sum(wbar ** 2))
    kg, kg_exact = kappa_mix_geo(W)
    ks = kappa_mix_slsqp(W, rng)
    kp = kappa_pairs(W)
    sec = sec_aperture(W)
    M = np.max(np.linalg.norm(W, axis=1))
    prod = sec ** 2 * (M + mnorm) ** 2 / (4 * M * mnorm)
    kmix = max(kg_exact, ks, kp, cert)  # best exact-evaluated mixture (valid lower bound on kappa^sq)
    rec = dict(tag=tag, nv=len(W), kb=kb, kb2=abs(kb2 - kb_s) + kb, secB2=secB2, contain=contain, rho_lt_c=rho < np.linalg.norm(c),
               cert=cert, kg=kg, kg_exact=kg_exact, ks=ks, kp=kp, kmix=kmix, sec2=sec ** 2, prod=prod)
    rows.append(rec)
    return rec


def rand_poly(rng, dim):
    d = rng.uniform(1, 5)
    dirn = rng.normal(size=dim)
    dirn /= np.linalg.norm(dirn)
    c = d * dirn
    k = rng.integers(3, 10)
    A = rng.normal(size=(dim, dim)) * rng.uniform(0.05, 0.9) * d / 2
    P = c + rng.normal(size=(k, dim)) @ A.T
    return P


def rand_arc(rng):
    phi = rng.uniform(0.05, 1.2)
    rad = rng.uniform(0.5, 3)
    k = rng.integers(3, 12)
    ang = np.sort(rng.uniform(-phi, phi, size=k))
    ang[0], ang[-1] = -phi, phi
    P = rad * np.c_[np.cos(ang), np.sin(ang)]
    if rng.random() < 0.5:
        P = P + rng.normal(size=2) * 0.2 * rad
    rot = rng.uniform(0, 2 * np.pi)
    R = np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
    return P @ R.T


def main(n2d=200, npair=100, n3d=60, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n2d):
        analyse(rand_poly(rng, 2), rng, "poly2d", rows)
    for _ in range(60):
        analyse(rand_arc(rng), rng, "arc2d", rows)
    for _ in range(npair):  # D_e = X_v - X_u from two random polygons
        Xu, Xv = rand_poly(rng, 2) * 0.4, rand_poly(rng, 2) * 0.4 + rng.normal(size=2) * 3
        W = np.array([b - a for a in hull_pts(Xu) for b in hull_pts(Xv)])
        analyse(W, rng, "diff2d", rows)
    for _ in range(n3d):
        Xu, Xv = rand_poly(rng, 3) * 0.4, rand_poly(rng, 3) * 0.4 + rng.normal(size=3) * 3
        W = np.array([b - a for a in hull_pts(Xu) for b in hull_pts(Xv)])
        analyse(W, rng, "diff3d", rows)

    def rel(a, b):
        return abs(a - b) / b

    for tag in ["poly2d", "arc2d", "diff2d", "diff3d"]:
        R = [r for r in rows if r["tag"] == tag]
        if not R:
            continue
        print(f"[{tag}] n={len(R)}")
        print(f"  max rel |F(u_SOCP) vs F(u_rows) ball values|       = {max(rel(r['kb2'], r['kb']) for r in R):.2e}")
        print(f"  max rel gap upper(ball) - lower(mixture)            = {max(rel(r['kmix'], r['kb']) for r in R):.2e}")
        print(f"  max (lower - upper)/upper (exact evaluations)       = {max((r['kmix'] - r['kb']) / r['kb'] for r in R):.2e}  (>0 would refute the upper bound)")
        print(f"  max rel |geo-mean value - SLSQP|                     = {max(rel(r['kg'], r['ks']) for r in R):.2e}")
        print(f"  max rel |Danskin certificate - kappa_ball|          = {max(rel(r['cert'], r['kb']) for r in R):.2e}")
        print(f"  best ball: max containment excess {max(r['contain'] for r in R):.1e}, rho<|c| always: {all(r['rho_lt_c'] for r in R)},"
              f" max rel |sec^2 theta_B - kappa_ball| {max(rel(r['secB2'], r['kb']) for r in R):.1e}")
        print(f"  pairs-only mixture strictly below kappa (rel > 1e-6): {sum(rel(r['kp'], r['kb']) > 1e-6 for r in R)} of {len(R)}")
        v1 = sum(r['kb'] < r['sec2'] * (1 - 1e-7) for r in R)
        v2 = sum(r['prod'] < r['kb'] * (1 - 1e-7) for r in R)
        print(f"  kappa^sq < sec^2(theta_e): {v1};  product bound < kappa^sq: {v2};"
              f"  min kappa^sq/sec^2 = {min(r['kb'] / r['sec2'] for r in R):.6f};  min product/kappa^sq = {min(r['prod'] / r['kb'] for r in R):.6f}")

    print("\nspecial sets")
    # balls: inscribed regular k-gons converge to d^2/(d^2 - rho^2) from below
    for d, rho in [(1.0, 0.1), (1.0, 0.3), (2.0, 1.2)]:
        exact = d * d / (d * d - rho * rho)
        for k in [16, 400]:
            ang = np.linspace(0, 2 * np.pi, k, endpoint=False)
            W = np.c_[d + rho * np.cos(ang), rho * np.sin(ang)]
            tau, _ = kappa_ball_socp(W)
            print(f"  ball d={d} rho={rho} {k}-gon: kappa={1/(1-tau):.6f}  sec^2={exact:.6f}  sec^4={exact**2:.6f}")
    # radial segment
    for m, M in [(2, 8), (1, 1.5)]:
        W = np.array([[m, 0.0], [M, 0.0]])
        tau, u = kappa_ball_socp(W)
        c = u / (u @ u)
        print(f"  radial [{m},{M}]: kappa={1/(1-tau):.6f}  (M+m)^2/(4Mm)={(M+m)**2/(4*M*m):.6f}  ball centre={c.round(6)}")
    # circular segment of radius 1, half-angle 30 deg
    phi = np.pi / 6
    ang = np.linspace(-phi, phi, 301)
    W = np.c_[np.cos(ang), np.sin(ang)]
    tau, u = kappa_ball_socp(W)
    c = u / (u @ u)
    mn = min_norm(W)
    prod = sec_aperture(W) ** 2 * (1 + mn) ** 2 / (4 * mn)
    minrad = np.cos(phi) ** 2 / (np.cos(phi) ** 2 - np.sin(phi) ** 2)
    print(f"  circular segment phi=30: kappa={1/(1-tau):.6f} (4/3={4/3:.6f}), ball centre {c.round(6)} (1/cos phi={1/np.cos(phi):.6f}),"
          f" product={prod:.6f}, min-radius ball={minrad:.6f}")
    # chord between the two tangent points of a ball: not a ball, yet kappa^sq = sec^2(theta_e)
    d, rho = 1.0, 0.5
    th = np.arcsin(rho / d)
    T = np.sqrt(d * d - rho * rho) * np.array([[np.cos(th), np.sin(th)], [np.cos(th), -np.sin(th)]])
    tau, _ = kappa_ball_socp(T)
    print(f"  chord of tangent points (d=1, rho=0.5): kappa={1/(1-tau):.6f}  sec^2(theta_e)={sec_aperture(T)**2:.6f}  -> equality without D being a ball")


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    main(*a)
