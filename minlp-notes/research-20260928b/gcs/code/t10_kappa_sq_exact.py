"""T10 (after review): Corollary C in exact form.

kappa^sq(D) = sup_{w in D} cav_D(|.|^2)(w)/|w|^2 equals the best enclosing-ball bound
1/(1 - tau*), tau* = min_u max_{w in ext D} (|w|^2|u|^2 - 2 w.u + 1).
For each random polygon D (0 not in D) this script computes
  k_ball : 1/(1 - tau*) (upper bound on kappa^sq, convex program),
  k_cert : sum mu|w|^2/|sum mu w|^2 for the dual weights mu (a mixture in D, lower bound),
  k_prod : the scout's product bound sec^2(theta) (M+m)^2/(4Mm),
  k_cent : the ball centred at the vertex centroid (the note's first-version code),
  sec2   : sec^2(theta), theta = cone aperture (so kappa^sq >= kappa_l2^2),
and checks k_cert = k_ball (exactness), k_prod >= k_ball, k_cent >= k_ball, k_ball >= sec2.
Usage: python3 t10_kappa_sq_exact.py [n] [seed]
"""
import sys
import numpy as np
import cvxpy as cp
from gcslib import point, poly_from_vertices2d, kappa_sq, kappa_l2, SOLVER

N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
O = point([0.0, 0.0])


def product_bound(V):
    th_sec = kappa_l2(O, poly_from_vertices2d(V))
    x = cp.Variable(2)
    P = poly_from_vertices2d(V)
    cp.Problem(cp.Minimize(cp.norm(x)), [P.A @ x <= P.b]).solve(solver=SOLVER)
    m = float(np.linalg.norm(x.value))
    M = float(np.max(np.linalg.norm(V, axis=1)))
    return th_sec ** 2 * (M + m) ** 2 / (4 * M * m), th_sec ** 2


def centroid_ball(V):
    c = V.mean(0)
    rho = np.max(np.linalg.norm(V - c, axis=1))
    d2 = c @ c
    return np.inf if rho ** 2 >= d2 else d2 / (d2 - rho ** 2)


worst_cert, bad, n = 0.0, 0, 0
prod_better = cent_better = 0
for k in range(N):
    npts = int(rng.integers(3, 9))
    half = np.radians(rng.uniform(2, 75))
    ang = rng.uniform(-half, half, npts) + rng.uniform(0, 2 * np.pi)
    rad = rng.uniform(0.2, rng.uniform(0.3, 10), npts)
    V = np.c_[rad * np.cos(ang), rad * np.sin(ang)]
    try:
        P = poly_from_vertices2d(V)
    except Exception:
        continue
    V = P.V
    if np.all(P.b >= -1e-9):  # 0 in D
        continue
    kb, (mu, W) = kappa_sq(O, P, return_cert=True)
    if not np.isfinite(kb):
        continue
    wb = mu @ W
    kc = (mu @ np.sum(W ** 2, axis=1)) / (wb @ wb)
    kp, s2 = product_bound(V)
    kce = centroid_ball(V)
    n += 1
    worst_cert = max(worst_cert, abs(kc - kb) / kb)
    bad += (kp < kb * (1 - 1e-6)) or (kce < kb * (1 - 1e-6)) or (kb < s2 * (1 - 1e-6)) or (kc > kb * (1 + 1e-6))
    prod_better += kp < kb * (1 - 1e-6)
    cent_better += kce < kb * (1 - 1e-6)
print(f"random polygons: n={n} max|k_cert-k_ball|/k_ball={worst_cert:.2e} violations={bad} "
      f"(product strictly better: {prod_better}, centroid ball strictly better: {cent_better})")

# special sets
phi = np.radians(30)
arc = np.array([[np.cos(a), np.sin(a)] for a in np.linspace(-phi, phi, 61)])
Parc = poly_from_vertices2d(arc)
kb = kappa_sq(O, Parc)
kp, s2 = product_bound(Parc.V)
# minimum-radius ball of the circular segment: centre (cos phi, 0), radius sin phi
cmr, rmr = np.array([np.cos(phi), 0.0]), np.sin(phi)
kmr = (cmr @ cmr) / (cmr @ cmr - rmr ** 2)
print(f"circular segment phi=30deg: best ball={kb:.6f} (sec^2 phi={1/np.cos(phi)**2:.6f}) product={kp:.6f} "
      f"min-radius ball={kmr:.6f} centroid ball={centroid_ball(Parc.V):.6f}")
seg = np.array([[2.0, 0.0], [8.0, 0.0], [8.0, 1e-9], [2.0, 1e-9]])
print(f"radial segment [2,8]: best ball={kappa_sq(O, poly_from_vertices2d(seg)):.6f} (M+m)^2/(4Mm)={100/64:.6f}")
