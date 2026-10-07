"""Float screening of the window law on example A (and optionally B): failing stages of several
quadratic calibration families of the Euler transcription, exact box minimization per stage.
A stage fails if its loss rho_t(zbar) - min_{D_t x U} rho_t exceeds 1e-12."""
import json
import sys
import time

import numpy as np

from model import Par, continuous_family
from discrete import solve_kkt, fam_affine, fam_lyap, fam_rmax, stage_losses

EXAMPLES = {
    # A0: hidden-convex (reduced Hessian in u positive definite); A: nonconvex in u
    "A0": Par(T=2.0, a=1.0, rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5),
    "A": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5),
    # C: eta_L = +0.20 > 0 but the maximal solution is tangential only at a very slow logarithmic rate
    "C": Par(T=2.0, a=1.0, rho=0.5, k1=0.5, q=0.3, c=0.2, k2=-0.2),
}
EPS = 0.02
THR = 1e-12


def sampled(Pf, N, h, shift=0.0):
    """P(t_t + shift); beyond T the profile is extended linearly (slope from the last 1e-3)."""
    T = N * h
    PT, dP = Pf(T), (Pf(T) - Pf(T - 1e-3)) / 1e-3
    out = []
    for t in range(N + 1):
        tt = max(t * h + shift, 0.0)
        out.append(Pf(tt) if tt <= T else PT + (tt - T) * dP)
    return np.array(out)


def main(name, Ns):
    p = EXAMPLES[name]
    Pmax, dmax = continuous_family(p, EPS, None)
    Plin, dlin = continuous_family(p, EPS, 0.1)
    Plin2, _ = continuous_family(p, EPS, 0.02) if name in ("A", "A0") else (None, None)
    out = []
    for N in Ns:
        t0 = time.time()
        kk = solve_kkt(p, N)
        h, s = kk["h"], kk["m"]
        fams = {
            "affine": fam_affine(p, kk),
            "lyap": fam_lyap(p, kk, EPS),
            "rmax": fam_rmax(p, kk, EPS)[0],
            "cmax": sampled(Pmax, N, h),
            "clin": sampled(Plin, N, h),
            "clin+3h": sampled(Plin, N, h, 3 * h),
            **({"clin.02": sampled(Plin2, N, h)} if Plin2 is not None else {}),
        }
        rec = dict(example=name, N=N, s=s, frac=kk["frac"], J=kk["J"], kkt_viol=kk["kkt_viol"])
        for fn, Ps in fams.items():
            if np.isnan(Ps).any():
                rec[fn] = "nan"
                continue
            loss, lN = stage_losses(p, kk, Ps)
            bad = np.where(loss > THR)[0]
            rec[fn] = dict(nfail=int(len(bad)),
                           rel_range=[int(bad.min() - s), int(bad.max() - s)] if len(bad) else None,
                           duration=float(len(bad) * h), total_loss=float(loss.sum()),
                           max_loss=float(loss.max()), term_loss=float(lN))
        rec["time"] = time.time() - t0
        print(json.dumps(rec), flush=True)
        out.append(rec)
    return out


if __name__ == "__main__":
    name = sys.argv[1]
    Ns = [int(a) for a in sys.argv[2:]]
    with open("logs/n2_windows.jsonl", "a") as f:
        for rec in main(name, Ns):
            f.write(json.dumps(rec) + "\n")
