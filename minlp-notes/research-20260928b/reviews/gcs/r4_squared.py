"""Corollary C audit: squared lengths.

For a polytope D = conv(V) in R^2 with 0 not in D:
  kappa_true = sup_w cav_D(q)(w)/q(w), q = ||.||^2, computed by bisection on
               kappa with the concave inner problem max_p sum p_i q(v_i) - kappa q(Vp);
  product    = sec^2(theta) (M+m)^2/(4Mm)   (scout / Kantorovich bound);
  ball_best  = inf over enclosing balls B(c, rho), rho < |c|, of |c|^2/(|c|^2 - rho^2).
               With u = c/|c|^2 this is 1/(1 - min_u max_i (|v_i|^2 |u|^2 - 2 v_i.u + 1)),
               a convex problem;
  ball_min   = the same with the smallest enclosing ball only.
Checks kappa_true <= min(product, ball_best) and compares the bounds on
balls, radial segments, circular segments (conv of an arc), and random polygons.
"""
import numpy as np
import cvxpy as cp


def kappa_true(V, hi=1e3, it=60):
    V = np.asarray(V, float)
    qv = np.sum(V ** 2, 1)
    p = cp.Variable(len(V), nonneg=True)
    kap = cp.Parameter(nonneg=True)
    prob = cp.Problem(cp.Maximize(qv @ p - kap * cp.sum_squares(V.T @ p)), [cp.sum(p) == 1])
    lo = 1.0
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        kap.value = mid
        prob.solve(solver="CLARABEL")
        if prob.value > 1e-10 * max(1, qv.max()):
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-9 * hi:
            break
    return hi


def aperture_cos(V):
    U = V / np.linalg.norm(V, axis=1, keepdims=True)
    a = cp.Variable(2)
    t = cp.Variable()
    prob = cp.Problem(cp.Maximize(t), [U @ a >= t, cp.norm(a, 2) <= 1])
    prob.solve(solver="CLARABEL")
    return prob.value


def min_norm(V):
    p = cp.Variable(len(V), nonneg=True)
    prob = cp.Problem(cp.Minimize(cp.sum_squares(V.T @ p)), [cp.sum(p) == 1])
    prob.solve(solver="CLARABEL")
    return np.sqrt(max(prob.value, 0))


def product_bound(V):
    c = aperture_cos(V)
    if c <= 0:
        return np.inf
    M = np.max(np.linalg.norm(V, axis=1))
    m = min_norm(V)
    return (M + m) ** 2 / (4 * M * m) / c ** 2


def ball_best(V):
    qv = np.sum(V ** 2, 1)
    u = cp.Variable(2)
    t = cp.Variable()
    cons = [qv[i] * cp.sum_squares(u) - 2 * V[i] @ u + 1 <= t for i in range(len(V))]
    prob = cp.Problem(cp.Minimize(t), cons)
    prob.solve(solver="CLARABEL")
    return 1.0 / (1.0 - prob.value) if prob.value < 1 else np.inf


def ball_min(V):
    c = cp.Variable(2)
    r = cp.Variable()
    prob = cp.Problem(cp.Minimize(r), [cp.norm(V[i] - c, 2) <= r for i in range(len(V))])
    prob.solve(solver="CLARABEL")
    d = np.linalg.norm(c.value)
    return d * d / (d * d - r.value ** 2) if d > r.value else np.inf


def report(name, V, extra=""):
    V = np.asarray(V, float)
    kt, pb, bb, bm = kappa_true(V), product_bound(V), ball_best(V), ball_min(V)
    ok = kt <= min(pb, bb) * (1 + 1e-6)
    print(f"{name:34s} kappa_true={kt:.6f} product={pb:.6f} ball_best={bb:.6f} ball_min={bm:.6f} "
          f"{'OK' if ok else 'VIOLATION'} {extra}")
    return kt, pb, bb, bm


print("-- balls (polygon with 400 vertices), center (1,0), radius rho")
for rho in [0.1, 0.3, 0.6]:
    ang = np.linspace(0, 2 * np.pi, 400, endpoint=False)
    V = np.c_[1 + rho * np.cos(ang), rho * np.sin(ang)]
    report(f"ball rho={rho}", V, f"sec^2={1/(1-rho*rho):.6f} sec^4={1/(1-rho*rho)**2:.6f}")

print("-- radial segments [m, M] on the x-axis (tiny width)")
for m, M in [(1, 2), (1, 5)]:
    V = np.array([[m, -1e-7], [M, -1e-7], [M, 1e-7], [m, 1e-7]])
    report(f"segment [{m},{M}]", V, f"(M+m)^2/4Mm={(M+m)**2/(4*M*m):.6f}")

print("-- circular segments conv(arc of radius 1, half-angle phi)")
for phi_deg in [5, 15, 30, 45]:
    phi = np.radians(phi_deg)
    ang = np.linspace(-phi, phi, 60)
    V = np.c_[np.cos(ang), np.sin(ang)]
    report(f"conv(arc) phi={phi_deg}", V, f"sec^2(phi)={1/np.cos(phi)**2:.6f}")

print("-- thin annular-sector hulls conv(arc r=1 U arc r=1+eps), half-angle phi")
for phi_deg, eps in [(15, 0.05), (30, 0.05), (30, 0.3)]:
    phi = np.radians(phi_deg)
    ang = np.linspace(-phi, phi, 60)
    V = np.r_[np.c_[np.cos(ang), np.sin(ang)], (1 + eps) * np.c_[np.cos(ang), np.sin(ang)]]
    report(f"sector phi={phi_deg} eps={eps}", V)

print("-- random polygons (5-8 random points in a cone of half-angle <= 60 deg)")
rng = np.random.default_rng(0)
cnt = dict(prod_better=0, ball_better=0, viol=0, n=0)
examples = {}
for k in range(60):
    npts = int(rng.integers(3, 9))
    half = np.radians(rng.uniform(5, 60))
    ang = rng.uniform(-half, half, npts)
    rad = rng.uniform(1, rng.uniform(1.05, 6), npts)
    V = np.c_[rad * np.cos(ang), rad * np.sin(ang)]
    kt, pb, bb, bm = kappa_true(V), product_bound(V), ball_best(V), ball_min(V)
    cnt["n"] += 1
    cnt["viol"] += kt > min(pb, bb) * (1 + 1e-6)
    if pb < bb * (1 - 1e-6):
        cnt["prod_better"] += 1
        examples.setdefault("prod_better", (V, kt, pb, bb))
    elif bb < pb * (1 - 1e-6):
        cnt["ball_better"] += 1
print(cnt)
if "prod_better" in examples:
    V, kt, pb, bb = examples["prod_better"]
    print("example where the product bound beats the best ball:", np.round(V, 4).tolist(),
          f"kappa_true={kt:.6f} product={pb:.6f} ball_best={bb:.6f}")
