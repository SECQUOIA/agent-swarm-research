"""Targeted validity checks for the prototype's bounding routines.

1. quad_box_min: compare against a dense grid on random boxes and random
   (including indefinite) quadratics; the bound must not exceed the grid
   minimum and should be close to it (it is meant to be exact).
2. Probe3Chain.unary_lb / pair_lb with random transfers: the bound must not
   exceed the piece value at any sampled point in the cell.
3. Reparametrization identity: sum of all pieces (with transfers) equals F(x).
4. quad_band_min against a grid on random polygons (box intersected with a band).
5. LotSizingChain.pair_lb with random transfers against sampled feasible points.
"""
import numpy as np
import instances as I
import chain_bb as CB

rng = np.random.default_rng(12345)

# 1. quad_box_min vs grid
worst_viol, worst_slack = -np.inf, 0.0
for trial in range(3000):
    A, Bc, C, D, E = rng.normal(size=5)
    if trial % 3 == 0:
        A, C = abs(A), abs(C)
    p, q = np.sort(rng.uniform(-1.5, 1.5, 2)); s, t = np.sort(rng.uniform(-1.5, 1.5, 2))
    lb = CB.quad_box_min(*(np.array([v]) for v in (A, Bc, C, D, E, p, q, s, t)))[0]
    xs, ys = np.meshgrid(np.linspace(p, q, 401), np.linspace(s, t, 401))
    gmin = (A * xs**2 + Bc * xs * ys + C * ys**2 + D * xs + E * ys).min()
    worst_viol = max(worst_viol, lb - gmin)
    worst_slack = max(worst_slack, gmin - lb)
print(f"quad_box_min: max(LB - gridmin) = {worst_viol:.3e} (must be <= 0); "
      f"max(gridmin - LB) = {worst_slack:.3e} (grid resolution error)")
assert worst_viol <= 0

# 2. piece bounds of the probe3 chain on random cells with random transfers
for n in (3, 7):
    pr = I.Probe3Chain(I.coeffs(n, 7))
    worst_u = worst_p = -np.inf
    for trial in range(2000):
        i = int(rng.integers(n)); e = int(rng.integers(n - 1))
        p, q = np.sort(rng.uniform(-1, 1, 2)); s, t = np.sort(rng.uniform(-1, 1, 2))
        if trial % 2:  # small cells as well
            q = p + (q - p) * 1e-3; t = s + (t - s) * 1e-3
        Qt, Lt = rng.uniform(-1, 1), rng.uniform(-1, 1)
        rhoL, rhoR, al, be = rng.uniform(0, 0.6), rng.uniform(0, 0.6), rng.normal(), rng.normal()
        ulb = pr.unary_lb(np.array([i]), np.array([p]), np.array([q]), np.array([Qt]), np.array([Lt]))[0]
        xs = np.linspace(p, q, 2001)
        uval = xs**2 - pr.kappa * xs**4 + pr.c[i] * xs - Qt * xs**2 + Lt * xs
        worst_u = max(worst_u, ulb - uval.min())
        plb = pr.pair_lb(np.array([e]), *(np.array([v]) for v in (p, q, s, t, rhoL, al, rhoR, be)))[0]
        X, Y = np.meshgrid(np.linspace(p, q, 201), np.linspace(s, t, 201))
        pval = pr.bval * X * Y + rhoL * X**2 - al * X + rhoR * Y**2 - be * Y
        worst_p = max(worst_p, plb - pval.min())
    print(f"n={n}: unary max(LB - sampled min) = {worst_u:.3e}; pair max(LB - sampled min) = {worst_p:.3e}")
    assert worst_u <= 0 and worst_p <= 0

# 3. reparametrization identity
n = 9
pr = I.Probe3Chain(I.coeffs(n, 3))
xhat = rng.uniform(-1, 1, n)
for mode in ("plain", "affine", "quad"):
    rhoL, al, rhoR, be = CB.transfers(pr, xhat, mode)
    Q = np.zeros(n); L = np.zeros(n); Q[:-1] += rhoL; Q[1:] += rhoR; L[:-1] += al; L[1:] += be
    x = rng.uniform(-1, 1, n)
    uni = x**2 - pr.kappa * x**4 + pr.c * x - Q * x**2 + L * x
    pair = pr.bval * x[:-1] * x[1:] + rhoL * x[:-1]**2 - al * x[:-1] + rhoR * x[1:]**2 - be * x[1:]
    err = abs(uni.sum() + pair.sum() - pr.F(x))
    print(f"identity {mode}: |sum pieces - F| = {err:.2e}")
    assert err < 1e-12
# 4. quad_band_min vs grid
worst = -np.inf
for trial in range(2000):
    A, Bc, C, D, E = rng.normal(size=5)
    p, q = np.sort(rng.uniform(-1, 1, 2)); s, t = np.sort(rng.uniform(-1, 1, 2))
    dl, dh = np.sort(rng.uniform(-1.5, 1.5, 2))
    X, Y = np.meshgrid(np.linspace(p, q, 301), np.linspace(s, t, 301))
    ok = (Y - X >= dl) & (Y - X <= dh)
    lb = CB.quad_band_min(*(np.array([v]) for v in (A, Bc, C, D, E, p, q, s, t, dl, dh)))[0]
    if ok.any():
        worst = max(worst, lb - (A * X * X + Bc * X * Y + C * Y * Y + D * X + E * Y)[ok].min())
print(f"quad_band_min: max(LB - grid min) = {worst:.3e} (must be <= 0)")
assert worst <= 0

# 5. lot-sizing pair bound vs sampled feasible points
import lotsizing as LS
pr = LS.LotSizingChain(LS.demands(5, 0))
worst = -np.inf
for k in range(3000):
    e = int(rng.integers(5)); p, q = np.sort(rng.uniform(-3, 3, 2)); s, t = np.sort(rng.uniform(-3, 3, 2))
    if k % 2:
        q = p + (q - p) * 0.01; t = s + (t - s) * 0.01
    rl, rr, al, be = rng.normal(size=4) * 0.5
    lb = pr.pair_lb(np.array([e]), *(np.array([v]) for v in (p, q, s, t, rl, al, rr, be)))[0]
    X, Y = np.meshgrid(np.linspace(p, q, 201), np.linspace(s, t, 201)); P = Y - X + pr.d[e]
    ok = (P >= 0) & (P <= LS.PCAP)
    if ok.any():
        worst = max(worst, lb - (LS.g(P) + rl * X**2 - al * X + rr * Y**2 - be * Y)[ok].min())
print(f"lot-sizing pair bound: max(LB - sampled feasible min) = {worst:.3e} (must be <= 0)")
assert worst <= 0
print("all bound checks passed")
