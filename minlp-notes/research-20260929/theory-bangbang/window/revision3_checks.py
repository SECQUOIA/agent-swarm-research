"""Targeted checks for the third revision of window-exactness.md (round-3 review; float screening).

usage: python3 revision3_checks.py PART [PART ...]   PART in famBterm aniso anisogrid
  famBterm: [V]'s family B on the verifier toy (P = 1/2, k = -1/2, Phi = 0, box |x| <= 2).  The
            terminal term is Phi - S_N = (Phi'(xbar_N) - p_N) d - d^2/4 = -d^2/4 (p_N = Phi'(xbar_N)),
            so its loss is (2 + |xbar_N|)^2 / 4, whatever the target a(t) is.  Recomputes the KKT
            points and compares with the logged terminal losses (logs/toy_verifier.json); exact
            rational check at N = 1000 (toy.exact_kkt_traj, toy.terminal_loss).
  aniso:    residual R = M - 2 eps I - (Delta / (2|sigma|)) beta beta^T of the anisotropic global-form
            condition (G), M = P' + A^T P + P A + H_xx, outside the linear-rate layer, for the families
            of Section 7.5: [E]'s cmax, clin, clin.02 (eps = 0.02) on [E]'s A and A0, and this report's
            family (clin) on A, A-, A0' (eps = 0.02) and A0' (eps = 0.1).  continuous_family integrates
            P' = G there with equality, so R = 0 up to ODE and differencing error.  P' by three stencils,
            each kept inside its smooth segment: central, step 0.1 dist (revision2_checks.py shE);
            five-point, step 0.05 dist (round-3 reviewer); five-point, step 0.005 dist; dist = distance to
            the nearer segment end, steps capped at 1e-6.  Reports, per stencil, the largest
            |lambda_min(R)|, the largest ||R||_2 (both eigenvalues), both also relative to ||M||_2, and
            inf lambda_min(M).
  anisogrid: the same residual for the families without a logarithmic segment (all but cmax), central
            stencil only, on a finer grid (20000 points per segment instead of 3000), to show how much
            the sampled maximum depends on the grid.
Writes logs/revision3_<part>.json.
"""
import json
import os
import sys
import warnings
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "n2"))
from toy import VERIFIER, kkt, float_data, fam_const, terminal_loss, exact_kkt_traj  # noqa: E402
from model import A, B, continuous_family, find_switch, solve_arcs  # noqa: E402
from n2win import EXAMPLES  # noqa: E402
from revision2_checks import EXAMPLES_E  # noqa: E402

warnings.filterwarnings("ignore")
LOG = os.path.join(HERE, "logs")


def dump(name, obj):
    with open(os.path.join(LOG, f"revision3_{name}.json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)


# ------------------------------------------------------------------------------------------ famBterm
def part_famBterm():
    with open(os.path.join(LOG, "toy_verifier.json")) as f:
        logged = {r["N"]: r for r in json.load(f)}
    out = []
    for N in (500, 1000, 2000, 4000, 8000):
        kk = kkt(VERIFIER, N)
        xN = float(kk["x"][N])
        pred = (VERIFIER.R + abs(xN)) ** 2 / 4
        D = float_data(VERIFIER, kk)
        tl = terminal_loss(VERIFIER, D, fam_const(N, 0.5))
        rec = dict(N=N, xbar_N=xN, p_N=float(kk["p"][N]), formula=pred, terminal_loss_recomputed=float(tl),
                   terminal_loss_logged=logged[N]["famB"]["terminal_loss"],
                   J_recomputed=float(kk["J"]), J_logged=logged[N]["J"])
        if N == 1000:
            De = exact_kkt_traj(VERIFIER, N, kk["u"])
            tle = terminal_loss(VERIFIER, De, [Fr(1, 2)] * (N + 1), exact=True)
            xNe = De["x"][N]
            rec["exact_terminal_loss_equals_formula"] = bool(tle == (Fr(VERIFIER.R) + abs(xNe)) ** 2 / 4)
            rec["exact_terminal_loss"] = float(tle)
        print(json.dumps(rec), flush=True)
        out.append(rec)
    dump("famBterm", out)


# ------------------------------------------------------------------------------------------ aniso
STENCILS = {"c2_0.1": (2, 0.1), "c5_0.05": (5, 0.05), "c5_0.005": (5, 0.005)}


def dP(Pf, t, lo, hi, order, frac):
    hs = min(1e-6, frac * (t - lo), frac * (hi - t))
    if order == 2:
        return (Pf(t + hs) - Pf(t - hs)) / (2 * hs)
    return (-Pf(t + 2 * hs) + 8 * Pf(t + hs) - 8 * Pf(t - hs) + Pf(t - 2 * hs)) / (12 * hs)


def aniso_pair(p, eps, delta1, npts=3000, gap=5e-5, s_min=1e-8, stencils=STENCILS):
    Pf, _ = continuous_family(p, eps, delta1=delta1)
    th = find_switch(p)[0]
    sol = solve_arcs(p, th)
    Delta = abs(p.ub - p.ua)
    lay = th + (delta1 if delta1 is not None else 0.05)
    segs = [(0.0, th), (th, lay), (lay, p.T)]
    pts = [(t, segs[0]) for t in np.linspace(gap, th - gap, npts)]
    if delta1 is None:  # cmax: the segment (tau, tau + 0.05] is also an equality piece
        pts += [(th + s, segs[1]) for s in np.geomspace(s_min, lay - th - gap, npts)]
    pts += [(t, segs[2]) for t in np.linspace(lay + gap, p.T - gap, npts)]
    res = {}
    for name, (order, frac) in stencils.items():
        lmin_R, norm_R, rel_lmin, rel_norm, lmin_M = [], [], [], [], []
        for t, (lo, hi) in pts:
            P = Pf(t)
            M = dP(Pf, t, lo, hi, order, frac) + A.T @ P + P @ A + p.Hxx
            M = (M + M.T) / 2
            beta = P @ B - p.w
            sg = abs((sol["a"]["sig"] if t < th else sol["b"]["sig"])(t))
            ev = np.linalg.eigvalsh(M - 2 * eps * np.eye(2) - (Delta / (2 * sg)) * np.outer(beta, beta))
            nM = float(np.linalg.norm(M, 2))
            lmin_R.append(abs(ev[0]))
            norm_R.append(float(np.abs(ev).max()))
            rel_lmin.append(abs(ev[0]) / nM)
            rel_norm.append(float(np.abs(ev).max()) / nM)
            lmin_M.append(float(np.linalg.eigvalsh(M)[0]))
        i = int(np.argmax(rel_norm))
        res[name] = dict(absmax_lambda_min_R=max(lmin_R), absmax_norm_R=max(norm_R),
                         relmax_lambda_min_R=max(rel_lmin), relmax_norm_R=max(rel_norm),
                         t_minus_tau_at_relmax_norm=float(pts[i][0] - th),
                         inf_lambda_min_M=min(lmin_M), max_dev_lambda_min_M_from_2eps=max(abs(v - 2 * eps) for v in lmin_M)
                         if delta1 is None else None)
    if delta1 is None:  # the point t - tau = 1e-8 quoted by the round-3 reviewer
        t = th + 1e-8
        near = {}
        for name, (order, frac) in STENCILS.items():
            P = Pf(t)
            M = dP(Pf, t, *segs[1], order, frac) + A.T @ P + P @ A + p.Hxx
            M = (M + M.T) / 2
            beta = P @ B - p.w
            sg = abs(sol["b"]["sig"](t))
            ev = np.linalg.eigvalsh(M - 2 * eps * np.eye(2) - (Delta / (2 * sg)) * np.outer(beta, beta))
            near[name] = dict(lambda_min_R=float(ev[0]), lambda_max_R=float(ev[1]), norm_M=float(np.linalg.norm(M, 2)))
        res["at_t_minus_tau_1e-8"] = near
    return res


def aniso_cases():
    cases = [(f"E_{n}_{f}", EXAMPLES_E[n], 0.02, d1) for n in ("A", "A0")
             for f, d1 in (("cmax", None), ("clin", 0.1), ("clin.02", 0.02))]
    cases += [(f"report_{n}_eps{e}", EXAMPLES[n], e, 0.1)
              for n, e in (("A", 0.02), ("Aminus", 0.02), ("Azero", 0.02), ("Azero", 0.1))]
    return cases


def part_aniso():
    out = {}
    for key, p, eps, d1 in aniso_cases():
        out[key] = aniso_pair(p, eps, d1)
        print(key, json.dumps(out[key]), flush=True)
    dump("aniso", out)


def part_anisogrid():
    out = {}
    for key, p, eps, d1 in aniso_cases():
        if d1 is None:
            continue
        out[key] = aniso_pair(p, eps, d1, npts=20000, stencils={"c2_0.1": STENCILS["c2_0.1"]})
        print(key, json.dumps(out[key]), flush=True)
    dump("anisogrid", out)


if __name__ == "__main__":
    parts = dict(famBterm=part_famBterm, aniso=part_aniso, anisogrid=part_anisogrid)
    for q in sys.argv[1:]:
        print("====", q, flush=True)
        parts[q]()
