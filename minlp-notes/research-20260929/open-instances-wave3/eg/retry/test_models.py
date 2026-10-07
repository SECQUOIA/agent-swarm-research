"""Sampling check (not a proof) of the per-box models: for random boxes of several sizes
(integer coordinates fixed or relaxed), the affine minorant/majorant of egfast.Fast.taylor
and egtm.Model.taylor (interval version) and both natural enclosures must contain the float
row values at 300 random points per box.  Also reports timings and the differences between
the fast and the interval versions.

    python3 test_models.py [names...]
"""
import sys
import time

import numpy as np

import egfast
import egtm

names = sys.argv[1:] or ["eg_int_s", "eg_disc_s", "eg_disc2_s"]
for name in names:
    M = egtm.Model(name); F = egfast.Fast(name); D = M.D
    rng = np.random.default_rng(0)
    for rho in [0.3, 0.03, 0.001, 1e-5]:
        N = 128
        w = (M.hi0 - M.lo0) * rho
        c = M.lo0 + rng.random((N, 7)) * (M.hi0 - M.lo0)
        lo = np.clip(c - w / 2, M.lo0, M.hi0); hi = np.clip(c + w / 2, M.lo0, M.hi0)
        isi = M.isint
        lo[:N // 2, isi] = np.round(c[:N // 2, isi]); hi[:N // 2, isi] = lo[:N // 2, isi]
        lo[N // 2:, isi] = np.floor(lo[N // 2:, isi]); hi[N // 2:, isi] = np.ceil(hi[N // 2:, isi])
        lo = np.clip(lo, M.lo0, M.hi0); hi = np.clip(hi, M.lo0, M.hi0)
        t0 = time.time(); T = M.taylor(lo, hi); t1 = time.time() - t0
        t0 = time.time(); Tf = F.taylor(lo, hi); t2 = time.time() - t0
        t0 = time.time(); Nn = M.natural(lo, hi); t3 = time.time() - t0
        t0 = time.time(); Nf = F.natural(lo, hi); t4 = time.time() - t0
        S = 300
        X = lo[:, None, :] + rng.random((N, S, 7)) * (hi - lo)[:, None, :]
        g, _ = D.g(X.reshape(-1, 7)); g = g.reshape(N, S, 28)
        viol = -np.inf
        for TT in (T, Tf):
            dX = X - TT['c'][:, None, :]
            lowm = TT['aL'][:, None, :] + np.einsum('nrd,nsd->nsr', TT['beta'], dX)
            upm = TT['aU'][:, None, :] + np.einsum('nrd,nsd->nsr', TT['beta'], dX)
            viol = max(viol, np.nanmax(lowm - g), np.nanmax(g - upm))
        for NN in (Nn, Nf):
            viol = max(viol, (NN.lo[:, None, :] - g).max(), (g - NN.hi[:, None, :]).max())
        fix = np.all(lo[:, isi] == hi[:, isi], axis=1)
        fin = np.isfinite(T['aL']) & np.isfinite(Tf['aL']) & fix[:, None]
        d_aL = (Tf['aL'] - T['aL'])[fin]
        print(f"{name} rho {rho:g}: taylor NI {t1/N*1e3:.2f} ms/box, fast {t2/N*1e3:.2f}; natural NI {t3/N*1e3:.2f}, "
              f"fast {t4/N*1e3:.2f}; max(model - value) {viol:.2e} (must be <= 0); integer-fixed boxes: "
              f"aL(fast) - aL(NI) in [{d_aL.min():.2e}, {d_aL.max():.2e}]; width of fast G {np.median(Tf['G'].hi - Tf['G'].lo):.1e}")
