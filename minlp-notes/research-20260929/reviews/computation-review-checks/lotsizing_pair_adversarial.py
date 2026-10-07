"""Adversarial sampling of LotSizingChain.pair_lb (study 4.1-4.2): boxes that straddle the band
lines (box centre outside the band), thin boxes, and singular quadratic models (rho = 0, so
A = C = Hlo/2, B = -Hlo, det = 0). The bound must not exceed the piece minimum over
box ∩ band; the minimum is approximated from below-dense sampling that includes the polygon
vertices (box corners inside the band and band-line/box-edge intersections)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../computation"))
import lotsizing as LS

rng = np.random.default_rng(7)
pr = LS.LotSizingChain(LS.demands(6, 3))
worst = -np.inf; ntest = 0
for k in range(20000):
    e = int(rng.integers(6)); dd = pr.d[e]
    # choose a box around a band line y - x + dd = 0 or = P
    c0 = 0.0 if k % 2 else LS.PCAP
    xc = rng.uniform(-3, 3); yc = xc - dd + c0 + rng.normal() * 0.3
    wx, wy = 10 ** rng.uniform(-4, 0.5, 2)
    p, q, s, t = xc - wx, xc + wx, yc - wy, yc + wy
    if k % 3 == 0:
        rl = rr = al = be = 0.0
    else:
        rl, rr = rng.normal(size=2) * 0.6; al, be = rng.normal(size=2)
    lb = pr.pair_lb(np.array([e]), *(np.array([v]) for v in (p, q, s, t, rl, al, rr, be)))[0]
    X, Y = np.meshgrid(np.linspace(p, q, 121), np.linspace(s, t, 121))
    X, Y = X.ravel(), Y.ravel()
    # add polygon vertices
    vx, vy = [], []
    for cc in (0.0, LS.PCAP):
        off = cc - dd
        vx += [p, q, s - off, t - off]; vy += [p + off, q + off, s, t]
    X = np.concatenate([X, vx]); Y = np.concatenate([Y, vy])
    P = Y - X + dd
    ok = (P >= 0) & (P <= LS.PCAP) & (X >= p) & (X <= q) & (Y >= s) & (Y <= t)
    if not ok.any():
        continue
    ntest += 1
    vals = LS.g(P[ok]) + rl * X[ok]**2 - al * X[ok] + rr * Y[ok]**2 - be * Y[ok]
    worst = max(worst, lb - vals.min())
print(f"tested {ntest} feasible boxes; max(LB - sampled feasible min) = {worst:.3e} (must be <= 0)")
