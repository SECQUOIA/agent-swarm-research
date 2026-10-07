"""Independent recheck of Remarks 5.2(d)-(f) on scalar LQ problems (floating point).

Problem: xdot = alpha x + u, l = (u^2 + q x^2)/2, Phi = phiT x^2/2, x0 = 1, T = 1,
U = [-UMAX, UMAX], D_t = interval enclosure of the Euler-feasible states at stage t.
Continuous value function V = P x^2/2 (a field; not strict in x).  Tilted
S = V - eps e^{-lam t} (x - x*(t))^2.

Families on the Euler transcription, all of the form S_t(y) = s2_t y^2/2 + s1_t y:
  * transferred (Theorem 5.2): S(t_t, .) + a_t y, a_t = p_t - S_x(t_t, x_t);
  * uncorrected (Proposition 5.1): S(t_t, .).
Every stage residual is a quadratic in (y, v); it is minimized exactly over the box
D_t x U by enumerating the interior stationary point, the edge critical points and the
corners (own implementation, not the review's).  The gap J - B(S) is computed as the sum
over stages of rho_t(z_t) - min rho_t (telescoping), so no constants are needed.

Outputs:
  A. field versus tilted versus uncorrected gaps for alpha = -2 (compare review c4/c4b);
  B. the smallest N from which the tilted transferred family is exact, as a function of
     eps and lam (the note says h_0 scales like the strictness constant eps e^{-lam T});
  C. uncorrected-family losses: Theta(h) for the non-strict field, O(h^2) for the tilted
     (strict) calibration (Remark 5.2(f)).
"""
import functools
import json

import numpy as np
from scipy.integrate import solve_ivp

T, X0, UMAX = 1.0, 1.0, 5.0


def box_min_quad(Hyy, Hyv, Hvv, gy, gv, ylo, yhi, vlo, vhi):
    """Vectorized exact min of 0.5[Hyy y^2 + 2Hyv y v + Hvv v^2] + gy y + gv v on boxes."""
    f = lambda y, v: 0.5 * (Hyy * y * y + 2 * Hyv * y * v + Hvv * v * v) + gy * y + gv * v
    cands = [f(y, v) for y in (ylo, yhi) for v in (vlo, vhi)]
    for yb in (ylo, yhi):  # edges y = const: 1-D in v
        with np.errstate(divide="ignore", invalid="ignore"):
            vc = -(gv + Hyv * yb) / Hvv
        ok = (Hvv > 0) & (vc >= vlo) & (vc <= vhi)
        cands.append(np.where(ok, f(yb, np.where(ok, vc, vlo)), np.inf))
    for vb in (vlo, vhi):  # edges v = const: 1-D in y
        with np.errstate(divide="ignore", invalid="ignore"):
            yc = -(gy + Hyv * vb) / Hyy
        ok = (Hyy > 0) & (yc >= ylo) & (yc <= yhi)
        cands.append(np.where(ok, f(np.where(ok, yc, ylo), vb), np.inf))
    det = Hyy * Hvv - Hyv * Hyv
    with np.errstate(divide="ignore", invalid="ignore"):
        ys = (-Hvv * gy + Hyv * gv) / det
        vs = (Hyv * gy - Hyy * gv) / det
    ok = (det > 0) & (Hyy > 0) & (ys >= ylo) & (ys <= yhi) & (vs >= vlo) & (vs <= vhi)
    cands.append(np.where(ok, f(np.where(ok, ys, ylo), np.where(ok, vs, vlo)), np.inf))
    return np.min(np.vstack(cands), axis=0), f


def setup(alpha, q, phiT):
    solP = solve_ivp(lambda t, P: [P[0] ** 2 - 2 * alpha * P[0] - q], [T, 0.0], [phiT],
                     rtol=1e-12, atol=1e-14, dense_output=True)
    Pf = lambda t: solP.sol(t)[0]
    solx = solve_ivp(lambda t, x: [(alpha - Pf(t)) * x[0]], [0.0, T], [X0],
                     rtol=1e-12, atol=1e-14, dense_output=True)
    xs = lambda t: solx.sol(t)[0]
    return Pf, xs


@functools.lru_cache(maxsize=None)
def discrete_kkt(alpha, q, phiT, N):
    h = T / N
    A = 1 + h * alpha
    Pd = np.empty(N + 1)
    Pd[N] = phiT
    K = np.empty(N)
    for t in range(N - 1, -1, -1):
        K[t] = A * Pd[t + 1] / (1 + h * Pd[t + 1])
        Pd[t] = h * q + A * A * Pd[t + 1] / (1 + h * Pd[t + 1])
    x = np.empty(N + 1)
    x[0] = X0
    u = np.empty(N)
    for t in range(N):
        u[t] = -K[t] * x[t]
        x[t + 1] = A * x[t] + h * u[t]
    p = Pd * x
    lo = np.empty(N + 1)
    hi = np.empty(N + 1)
    lo[0] = hi[0] = X0
    for t in range(N):
        c = (A * lo[t], A * hi[t])
        lo[t + 1] = min(c) - h * UMAX
        hi[t + 1] = max(c) + h * UMAX
    assert np.max(np.abs(u)) < UMAX
    return h, A, x, u, p, lo, hi


def family_gap(alpha, q, phiT, N, eps, lam, kind, Pf, xs):
    h, A, x, u, p, lo, hi = discrete_kkt(alpha, q, phiT, N)
    tt = h * np.arange(N + 1)
    ep = eps * np.exp(-lam * tt)
    s2 = Pf(tt) - 2 * ep
    if kind == "transferred":
        s1 = p - s2 * x
    else:
        s1 = 2 * ep * xs(tt)
    # stage residual coefficients for t = 0..N-1
    Hyy = h * q + s2[1:] * A * A - s2[:-1]
    Hyv = s2[1:] * A * h
    Hvv = h + s2[1:] * h * h
    gy = s1[1:] * A - s1[:-1]
    gv = s1[1:] * h
    ylo, yhi = lo[:-1].copy(), hi[:-1].copy()
    mins, f = box_min_quad(Hyy, Hyv, Hvv, gy, gv, ylo, yhi, -UMAX, UMAX)
    at = f(x[:-1], u)
    stage_def = at - np.minimum(mins, at)
    # terminal residual Phi - S_N on [lo_N, hi_N]
    cN = phiT - s2[N]
    fN = lambda y: 0.5 * cN * y * y - s1[N] * y
    cand = [fN(lo[N]), fN(hi[N]), fN(x[N])]
    if cN > 0:
        yc = s1[N] / cN
        if lo[N] <= yc <= hi[N]:
            cand.append(fN(yc))
    term_def = fN(x[N]) - min(cand)
    det = Hyy[1:] * Hvv[1:] - Hyv[1:] ** 2
    scale = np.abs(Hyy[1:] * Hvv[1:]) + Hyv[1:] ** 2
    psd = bool(np.all(Hvv > 0) and np.all(det >= -1e-12 * scale) and cN > 0)
    return float(np.sum(stage_def) + term_def), psd


out = {}
# ------------------------------------------------------------------ A
rowsA = []
Pf, xs = setup(-2.0, 0.0, 1.0)
for N in (10, 20, 40, 80, 160, 320, 640, 2560):
    rec = {"N": N}
    rec["field_transferred"], _ = family_gap(-2.0, 0.0, 1.0, N, 0.0, 0.0, "transferred", Pf, xs)
    rec["tilt_lam1_transferred"], rec["tilt_lam1_psd"] = family_gap(-2.0, 0.0, 1.0, N, 0.5, 1.0, "transferred", Pf, xs)
    rec["tilt_lam8_transferred"], rec["tilt_lam8_psd"] = family_gap(-2.0, 0.0, 1.0, N, 0.5, 8.0, "transferred", Pf, xs)
    rowsA.append(rec)
    print("A", json.dumps(rec))
out["A"] = rowsA

# ------------------------------------------------------------------ B
def first_exact_N(alpha, q, phiT, eps, lam, Pf, xs, tol=1e-12, Nmax=200000):
    """Smallest N on a fine geometric grid from which the transferred family is exact
    (gap <= tol * max(1,|J|)) at every larger grid N up to Nmax."""
    Ns = np.unique(np.round(np.geomspace(4, Nmax, 160)).astype(int))
    ex = []
    for N in Ns:
        g, psd = family_gap(alpha, q, phiT, int(N), eps, lam, "transferred", Pf, xs)
        ex.append((int(N), g <= tol, psd, g))
    # exactness is decided by the exact PSD test of the stage Hessians; the computed
    # gap is a consistency check (gap <= tol whenever PSD; gap > tol when not PSD,
    # except within rounding very close to the threshold)
    last_bad = max([N for N, _, psd, _ in ex if not psd], default=0)
    firstN = min([N for N, _, psd, _ in ex if psd and N > last_bad], default=None)
    agree = sum(e == psd for _, e, psd, _ in ex) / len(ex)
    return firstN, last_bad, agree


rowsB = []
for (alpha, q, phiT) in ((-2.0, 0.0, 1.0), (1.0, 1.0, 0.0)):
    Pf, xs = setup(alpha, q, phiT)
    for lam in ((1.0, 2.0, 4.0, 8.0) if alpha < 0 else (4.0, 6.0, 8.0)):
        for eps in (0.5, 0.1, 0.02):
            firstN, last_bad, agree = first_exact_N(alpha, q, phiT, eps, lam, Pf, xs)
            c_T = eps * np.exp(-lam * T)
            rec = {"alpha": alpha, "q": q, "phiT": phiT, "lam": lam, "eps": eps,
                   "eps_exp_minus_lamT": c_T, "first_exact_N": firstN, "last_inexact_N": last_bad,
                   "h0_estimate": (T / last_bad) if last_bad else None,
                   "h0_over_epsexp": (T / last_bad / c_T) if last_bad else None,
                   "fraction_grid_N_gap_test_agrees_with_psd": agree}
            rowsB.append(rec)
            print("B", json.dumps(rec))
out["B"] = rowsB

# ------------------------------------------------------------------ C
rowsC = []
Pf, xs = setup(-2.0, 0.0, 1.0)
for N in (10, 20, 40, 80, 160, 320, 640):
    g_field, _ = family_gap(-2.0, 0.0, 1.0, N, 0.0, 0.0, "uncorrected", Pf, xs)
    g_tilt, _ = family_gap(-2.0, 0.0, 1.0, N, 0.5, 1.0, "uncorrected", Pf, xs)
    rec = {"N": N, "uncorrected_field_gap": g_field, "uncorrected_field_gap_over_h": g_field * N,
           "uncorrected_tilted_gap": g_tilt, "uncorrected_tilted_gap_over_h2": g_tilt * N * N}
    rowsC.append(rec)
    print("C", json.dumps(rec))
out["C"] = rowsC

with open("logs/r2_tilted_lq.json", "w") as fh:
    json.dump(out, fh, indent=1)
