"""Sampling soundness test of the affine models: the independent ones (indep_cert.Model) and the
retry's production models (egfast.Fast.taylor, natural enclosure).  Not a proof.

Reference values: g_k(x) in numpy long double (64-bit significand; data parsed from the exact
decimal strings), whose error (about 1e-17 sum|w|) is far below the slack of either model.
Test points: box centre, all corners (up to 128), random points, and local minimizers /
maximizers of g_k(x) - beta_k . (x - c) found by L-BFGS-B (float) for every row.

Reports per box family the smallest normalised margins
  (g - minorant) / (1 + sum|w|)   and   (majorant - g) / (1 + sum|w|)
(negative = model violated) and the median of (retry aL - independent aL) for the
objective rows.

    python3 test_models_indep.py <name> <boxes per family> [seed]
"""
import itertools
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "open-instances-wave3", "eg", "retry"))
import egfast  # noqa: E402
from gms_model import GmsModel  # noqa: E402
from indep_cert import Model  # noqa: E402

LD = np.longdouble


class LDEval:
    def __init__(self, name, M):
        T = GmsModel(name).terms()
        dv = M.vars
        self.A = np.array([[LD(str(a.numerator)) / LD(str(a.denominator)) for a, _ in t["terms"]] for t in T])
        self.MU = np.array([[[LD(str(f[v][1].numerator)) / LD(str(f[v][1].denominator)) for v in dv]
                             for _, f in t["terms"]] for t in T])
        self.GA = np.array([[LD(str(t["terms"][0][1][v][2].numerator)) / LD(str(t["terms"][0][1][v][2].denominator))
                             for v in dv] for t in T])
        sc = T[0]["terms"][0][1]
        self.S = np.array([LD(str(sc[v][0].numerator)) / LD(str(sc[v][0].denominator)) for v in dv])
        self.LIN = np.array([[LD(str(t["lin"].get(v, 0).numerator)) / LD(str(t["lin"].get(v, 0).denominator))
                              if v in t["lin"] else LD(0) for v in dv] for t in T])

    def g(self, x):
        x = np.asarray(x, dtype=LD)
        t = self.MU[None] + (self.S * x)[:, None, None, :]
        E = (self.GA[None, :, None, :] * t * t).sum(-1)
        W = self.A[None] * np.exp(E)
        return W.sum(-1) + (x[:, None, :] * self.LIN[None]).sum(-1), np.abs(W).sum(-1)


def boxes(M, rng, n, rel, around, fix_int):
    lo0, hi0 = M.lb, M.ub
    out = []
    for _ in range(n):
        if around is not None:
            cen = around + rng.normal(0, 1, M.d) * rel * (hi0 - lo0) * 0.5
        else:
            cen = rng.uniform(lo0, hi0)
        cen = np.clip(cen, lo0, hi0)
        half = rel * (hi0 - lo0) * rng.uniform(0.2, 1.0, M.d)
        lo = np.clip(cen - half, lo0, hi0); hi = np.clip(cen + half, lo0, hi0)
        if fix_int:
            v = np.round(cen)
            lo = np.where(M.isint, v, lo); hi = np.where(M.isint, v, hi)
        else:
            lo = np.where(M.isint, np.floor(lo), lo); hi = np.where(M.isint, np.ceil(hi), hi)
        out.append((lo, hi))
    return np.array([b[0] for b in out]), np.array([b[1] for b in out])


def main(name, nb, seed=0):
    rng = np.random.default_rng(seed)
    M = Model(name)
    E = LDEval(name, M)
    Fm = egfast.Fast(name)
    best = {"eg_int_s": [0.564219345763436, 0.6468471890552644, 1.0, 0.9390699678023392, 2, 4, 3],
            "eg_disc_s": [3, 10, 8, 12, 1.0800209145804143, 3.485358811359775, 2.2415838244871797],
            "eg_disc2_s": [0.339986187975027, 1.0, 0.7526242429543005, 1.2370734367691458, 11, 34, 24]}[name]
    best = np.array(best, float)
    fams = [(rel, around, fi) for rel in (0.3, 0.03, 1e-3, 1e-5, 1e-7) for around in (best, None) for fi in (True, False)
            if not (around is None and rel < 1e-3)]
    print(f"{name}: {len(fams)} box families x {nb} boxes")
    worst_all = (np.inf, np.inf, np.inf, np.inf)
    for rel, around, fi in fams:
        lo, hi = boxes(M, rng, nb, rel, around, fi)
        c, r, beta, aL, aU = M.taylor(lo, hi)
        nl, nh = M.natural(lo, hi)
        T = Fm.taylor(lo, hi)
        fl, fh = Fm.natural(lo, hi).lo, Fm.natural(lo, hi).hi
        mL = mU = fL = fU = np.inf
        diffs = []
        for n in range(nb):
            pts = [c[n]]
            cont = np.where(hi[n] > lo[n])[0]
            corners = list(itertools.product(*[(lo[n][i], hi[n][i]) for i in cont]))
            for cc in corners[:128]:
                p = c[n].copy(); p[cont] = cc; pts.append(p)
            pts += list(lo[n] + rng.uniform(0, 1, (40, M.d)) * (hi[n] - lo[n]))
            # adversarial: extremes of g_k - beta_k.(x - c) per row (float local search)
            if len(cont):
                for k in rng.choice(28, 6, replace=False):
                    for sgn in (1.0, -1.0):
                        def f(z, k=k, sgn=sgn):
                            x = c[n].copy(); x[cont] = z
                            t = M.MU[k] + M.S * x
                            w = M.A[k] * np.exp((M.GA[k] * t * t).sum(-1))
                            val = w.sum() + M.LIN[k] @ x - beta[n, k] @ (x - c[n])
                            gr = (w[:, None] * 2 * M.GA[k] * M.S * t).sum(0) + M.LIN[k] - beta[n, k]
                            return sgn * val, sgn * gr[cont]
                        z0 = lo[n][cont] + rng.uniform(0, 1, len(cont)) * (hi[n][cont] - lo[n][cont])
                        res = minimize(f, z0, jac=True, method="L-BFGS-B",
                                       bounds=list(zip(lo[n][cont], hi[n][cont])), options=dict(maxiter=60))
                        p = c[n].copy(); p[cont] = np.clip(res.x, lo[n][cont], hi[n][cont]); pts.append(p)
            pts = np.array(pts)
            pts = np.where(M.isint & (hi[n] > lo[n]), np.round(pts), pts)
            g, sw = E.g(pts)
            g = g.astype(np.float64); sw = sw.astype(np.float64)
            dd = pts - c[n]
            minor = aL[n][None] + (dd[:, None, :] * beta[n][None]).sum(-1)
            major = aU[n][None] + (dd[:, None, :] * beta[n][None]).sum(-1)
            fminor = T["aL"][n][None] + ((pts - T["c"][n])[:, None, :] * T["beta"][n][None]).sum(-1)
            fmajor = T["aU"][n][None] + ((pts - T["c"][n])[:, None, :] * T["beta"][n][None]).sum(-1)
            den = 1 + sw
            with np.errstate(invalid="ignore"):
                mL = min(mL, np.nanmin(np.where(np.isfinite(minor), (g - minor) / den, np.inf)), np.min((g - nl[n]) / den))
                mU = min(mU, np.nanmin(np.where(np.isfinite(major), (major - g) / den, np.inf)), np.min((nh[n] - g) / den))
                fL = min(fL, np.nanmin(np.where(np.isfinite(fminor), (g - fminor) / den, np.inf)), np.min((g - fl[n]) / den))
                fU = min(fU, np.nanmin(np.where(np.isfinite(fmajor), (fmajor - g) / den, np.inf)), np.min((fh[n] - g) / den))
            ok = np.isfinite(aL[n, :24]) & np.isfinite(T["aL"][n, :24])
            if ok.any():
                # compare at the common centre: minorant values at c
                diffs += list((T["aL"][n, :24] - aL[n, :24])[ok])
        med = np.median(diffs) if diffs else np.nan
        tag = f"rel {rel:g} {'near best' if around is not None else 'uniform  '} {'int fixed' if fi else 'int relax'}"
        print(f"  {tag}: min margins indep (lower {mL:.2e}, upper {mU:.2e}); retry (lower {fL:.2e}, upper {fU:.2e}); "
              f"median(retry aL - indep aL) obj rows {med:.2e}")
        worst_all = tuple(min(a, b) for a, b in zip(worst_all, (mL, mU, fL, fU)))
    print(f"  overall min margins: indep lower {worst_all[0]:.2e} upper {worst_all[1]:.2e}; "
          f"retry lower {worst_all[2]:.2e} upper {worst_all[3]:.2e}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 0)
