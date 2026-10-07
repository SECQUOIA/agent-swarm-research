"""Round-3 confirmation, item 3: the anisotropic residual R of the two-state families.

R(t) = M - 2 eps I - (Delta / (2|sigma|)) beta beta^T,  M = P' + A^T P + P A + H_xx,  beta = P b - w,
for P = continuous_family(p, eps, delta1) of theory-bangbang/n2/model.py (object under test,
imported read-only).  continuous_family integrates P' = G (equality) outside the linear-rate layer,
so R should be numerical error only.

Own choices (independent of revision3_checks.py):
 * On the logarithmic segment of cmax, (tau, tau + 0.05], P is the dense output of an ODE in
   lam = log(t - tau).  I pull that dense output out of the closure and difference it in lam
   (five-point, step 1e-3), so P' = (dP/dlam) / s has no cancellation in t.  This measures the
   residual of the interpolant itself.
 * For comparison, differences in t: central with step 0.1 s and five-point with step 0.05 s
   (the two schemes quoted in the report), s = distance to the nearer segment end, cap 1e-6.
 * On the other segments: five-point in t with step min(1e-4, 0.1 s) and central with the
   report's step min(1e-6, 0.1 s).
 * Per segment: max ||R||_2, max ||R||_2 / ||M||_2, max |lambda_min(M) - 2 eps| and
   min lambda_min(M) - 2 eps.
Sampling: 4000 points per segment (linspace; geomspace from 1e-8 on the cmax log segment).
"""
import json
import os
import sys
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "theory-bangbang")
sys.path.insert(0, os.path.join(ROOT, "n2"))
from model import A, B, Par, continuous_family, find_switch, solve_arcs  # noqa: E402

warnings.filterwarnings("ignore")

EX = {  # [E] Section 6.1 examples A and A0; this report's variants A-, A0' (window-exactness.md 7.5)
    "A": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5),
    "A0": Par(T=2.0, a=1.0, rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5),
    "Aminus": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=0.3, q=0.3, c=1.0, x20=0.5),
    "Azero": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=0.0, q=0.3, c=1.0, x20=0.5),
}
CASES = [("E_A_cmax", "A", 0.02, None), ("E_A_clin", "A", 0.02, 0.1), ("E_A_clin.02", "A", 0.02, 0.02),
         ("E_A0_cmax", "A0", 0.02, None), ("E_A0_clin", "A0", 0.02, 0.1), ("E_A0_clin.02", "A0", 0.02, 0.02),
         ("rep_Aminus", "Aminus", 0.02, 0.1), ("rep_Azero", "Azero", 0.02, 0.1),
         ("rep_Azero_eps0.1", "Azero", 0.1, 0.1)]


def five(F, x, hs):
    return (-F(x + 2 * hs) + 8 * F(x + hs) - 8 * F(x - hs) + F(x - 2 * hs)) / (12 * hs)


def central(F, x, hs):
    return (F(x + hs) - F(x - hs)) / (2 * hs)


def resid(p, eps, P, dP, t, sig, Delta):
    M = dP + A.T @ P + P @ A + p.Hxx
    M = (M + M.T) / 2
    beta = P @ B - p.w
    Rm = M - 2 * eps * np.eye(2) - (Delta / (2 * abs(sig(t)))) * np.outer(beta, beta)
    ev = np.linalg.eigvalsh(Rm)
    nM = np.linalg.norm(M, 2)
    lm = np.linalg.eigvalsh(M)[0] - 2 * eps
    return float(np.abs(ev).max()), float(np.abs(ev).max() / nM), float(lm), float(ev[0]), float(ev[1]), float(nM)


def run_case(key, ex, eps, d1, npts=4000):
    p = EX[ex]
    Pf, _ = continuous_family(p, eps, delta1=d1)
    th = find_switch(p)[0]
    sol = solve_arcs(p, th)
    Delta = abs(p.ub - p.ua)
    lay = th + (d1 if d1 is not None else 0.05)
    out = {}
    segs = {"pre": (0.0, th, sol["a"]["sig"]), "last": (lay, p.T, sol["b"]["sig"])}
    for name, (lo, hi, sig) in segs.items():
        ts = np.linspace(lo + 5e-5, hi - 5e-5, npts)
        rows = {"five_1e-4": [], "central_rep": []}
        for t in ts:
            s = min(t - lo, hi - t)
            P = Pf(t)
            rows["five_1e-4"].append(resid(p, eps, P, five(Pf, t, min(1e-4, 0.1 * s)), t, sig, Delta))
            rows["central_rep"].append(resid(p, eps, P, central(Pf, t, min(1e-6, 0.1 * s)), t, sig, Delta))
        out[name] = {k: summarize(v) for k, v in rows.items()}
    if d1 is None:
        # log segment: find the lam-dense output inside the closure of Pf
        segs_cl = [c.cell_contents for c in Pf.__closure__ if isinstance(c.cell_contents, list)][0]
        f_log = [f for lo, hi, f in segs_cl if abs(lo - th) < 1e-9 and abs(hi - lay) < 1e-12][0]
        sol2 = f_log.__defaults__[0]
        Q = lambda lam: np.asarray(sol2(lam)).reshape(2, 2)
        sig = sol["b"]["sig"]
        ss = np.geomspace(1e-8, 0.05 - 5e-5, npts)
        rows = {"lam_five_1e-3": [], "t_central_0.1": [], "t_five_0.05": []}
        for s in ss:
            lam = np.log(s)
            t = th + s
            P = Q(lam)
            dP = five(Q, lam, 1e-3) / s
            rows["lam_five_1e-3"].append(resid(p, eps, P, dP, t, sig, Delta))
            lo, hi = th, lay
            d = min(t - lo, hi - t)
            Pt = Pf(t)
            rows["t_central_0.1"].append(resid(p, eps, Pt, central(Pf, t, min(1e-6, 0.1 * d)), t, sig, Delta))
            rows["t_five_0.05"].append(resid(p, eps, Pt, five(Pf, t, min(1e-6, 0.05 * d)), t, sig, Delta))
        out["log"] = {k: summarize(v) for k, v in rows.items()}
        out["log_at_1e-8"] = {k: dict(lmin_R=v[0][3], lmax_R=v[0][4], normM=v[0][5]) for k, v in rows.items()}
    return out


def summarize(rows):
    a = np.array(rows)
    return dict(max_norm_R=float(a[:, 0].max()), max_rel_norm_R=float(a[:, 1].max()),
                max_abs_lminM_dev=float(np.abs(a[:, 2]).max()), min_lminM_dev=float(a[:, 2].min()),
                max_abs_lmin_R=float(np.abs(a[:, 3]).max()))


def main():
    res = {}
    for key, ex, eps, d1 in CASES:
        res[key] = run_case(key, ex, eps, d1)
        print(key, json.dumps(res[key]), flush=True)
    json.dump(res, open(os.path.join(HERE, "logs", "c2_aniso.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
