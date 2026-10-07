"""Targeted checks for the second revision of window-exactness.md (round-2 review; float screening).

usage: python3 revision2_checks.py PART [PART ...]   PART in shE famB rmaxrow
  shE:     isotropic (H3)/(W5) margin of (SH) for the continuous tangential families that
           extension-n2.md, Section 6.2, screened on its examples A and A0: cmax (delta_1 = None,
           logarithmic tangency), clin (delta_1 = 0.1) and clin.02 (delta_1 = 0.02), all eps = 0.02
           (continuous_family of n2/model.py, read only).  (SH) needs one mu > 0 with
           grad_x^2 r >= mu I and |sigma| > Delta |beta|^2 / (2 mu) for t != tau, i.e.
           sup_t Delta |beta|^2 / (2 |sigma|) < inf_t lambda_min(M), M = P' + A^T P + P A + H_xx.
           Reports the sup of the ratio on the whole grid, before the switch (t <= tau - 0.1), on the
           last arc beyond the layers (t >= tau + 0.1) and at t = T, and the ratio at distances
           s = 1e-2 ... 1e-8 after the switch.  Also the anisotropic (global-form) residual
           lambda_min(M - 2 eps I - (Delta / (2|sigma|)) beta beta^T) outside the linear-rate layer.
  famB:    [V]'s family B on the verifier toy (P = 1/2, k = -1/2): the exact stage Hessian in (d, omega)
           from the formula of toy.py, and the logged float stage losses (logs/toy_verifier.json).
  rmaxrow: the eta_hat_1 rows of the Section 7.6 table from logs/toy_rmax.json, rounded to 3 digits.
Writes logs/revision2_<part>.json.
"""
import json
import os
import sys
import warnings
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "n2"))
from model import A, B, Par, continuous_family, find_switch, solve_arcs  # noqa: E402

warnings.filterwarnings("ignore")
LOG = os.path.join(HERE, "logs")

# extension-n2.md, Section 6.1 table and n2/n2_windows.py
EXAMPLES_E = {
    "A": Par(T=2.0, a=1.0, rho=2.0, k1=-0.3, k2=-0.3, q=0.3, c=1.0, x20=0.5),
    "A0": Par(T=2.0, a=1.0, rho=1.0, k1=-0.3, k2=-0.3, q=0.3, c=0.2, x20=0.5),
}
FAMILIES_E = {"cmax": None, "clin": 0.1, "clin.02": 0.02}
EPS = 0.02


def dump(name, obj):
    with open(os.path.join(LOG, f"revision2_{name}.json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)


# ------------------------------------------------------------------------------------------ shE
def margin_terms(p, Pf, sol, th, t, lo, hi):
    """M, beta, |sigma| at t; P' by central differences inside the smooth segment [lo, hi]."""
    step = min(1e-6, 0.1 * (t - lo), 0.1 * (hi - t))
    P = Pf(t)
    dP = (Pf(t + step) - Pf(t - step)) / (2 * step)
    M = dP + A.T @ P + P @ A + p.Hxx
    M = (M + M.T) / 2
    beta = P @ B - p.w
    sg = abs((sol["a"]["sig"] if t < th else sol["b"]["sig"])(t))
    return M, beta, sg


def n2_margin_E(p, delta1, eps=EPS, npts=4000, gap=5e-5, s_min=1e-8):
    Pf, dg = continuous_family(p, eps, delta1=delta1)
    th = find_switch(p)[0]
    sol = solve_arcs(p, th)
    Delta = abs(p.ub - p.ua)
    T = p.T
    # smooth segments of continuous_family (boundaries: 0, th, th + layer end, T)
    lay = th + (delta1 if delta1 is not None else 0.05)
    segs = [(0.0, th), (th, lay), (lay, T)]
    pts = [(t, segs[0]) for t in np.linspace(gap, th - gap, npts)]
    pts += [(th + s, segs[1]) for s in np.geomspace(s_min, lay - th - gap, npts)]
    pts += [(t, segs[2]) for t in np.linspace(lay + gap, T - gap, npts)]
    rows = []
    for t, (lo, hi) in pts:
        M, beta, sg = margin_terms(p, Pf, sol, th, t, lo, hi)
        ev = np.linalg.eigvalsh(M)
        ratio = Delta * beta @ beta / (2 * sg)
        aniso = float(np.linalg.eigvalsh(M - 2 * eps * np.eye(2) - (Delta / (2 * sg)) * np.outer(beta, beta))[0])
        rows.append((t, ev[0], ratio, aniso))
    t_arr = np.array([r[0] for r in rows])
    lmin = np.array([r[1] for r in rows])
    ratio = np.array([r[2] for r in rows])
    aniso = np.array([r[3] for r in rows])
    before = t_arr <= th - 0.1
    last = t_arr >= th + 0.1
    outside_layer = (t_arr < th) | (t_arr > lay) if delta1 is not None else np.ones_like(t_arr, bool)
    MT, bT, sT = margin_terms(p, Pf, sol, th, T - gap, lay, T)
    at_s = {}
    for s in (1e-2, 1e-4, 1e-6, 1e-8):
        Ms, bs, ss = margin_terms(p, Pf, sol, th, th + s, th, lay)
        at_s[f"{s:.0e}"] = dict(ratio=float(Delta * bs @ bs / (2 * ss)), abs_beta=float(np.linalg.norm(bs)),
                                lambda_min_M=float(np.linalg.eigvalsh(Ms)[0]))
    return dict(delta1=delta1, eps=eps, tau=th, pre_blowup=bool(dg["pre_blowup"]),
                inf_lambda_min_M=float(lmin.min()), t_inf_lambda_min_M=float(t_arr[int(lmin.argmin())]),
                sup_ratio=float(ratio.max()), t_sup_ratio=float(t_arr[int(ratio.argmax())]),
                sup_ratio_before_switch=float(ratio[before].max()),
                sup_ratio_last_arc=float(ratio[last].max()),
                ratio_at_T=float(Delta * bT @ bT / (2 * sT)),
                ratio_after_switch_at_s=at_s,
                isotropic_ok=bool(ratio.max() < lmin.min()),
                aniso_absmax_outside_layer=float(np.max(np.abs(aniso[outside_layer]))),
                grid=dict(npts_per_segment=npts, gap=gap, s_min=s_min))


def part_shE():
    out = {}
    for name, p in EXAMPLES_E.items():
        for fam, delta1 in FAMILIES_E.items():
            key = f"{name}_{fam}"
            out[key] = n2_margin_E(p, delta1)
            print(key, json.dumps(out[key]), flush=True)
    dump("shE", out)


# ------------------------------------------------------------------------------------------ famB
def part_famB():
    # toy.py: in (d, omega) the stage residual has Hessian [[h + P_{t+1} - P_t, h (P_{t+1} + k)],
    # [h (P_{t+1} + k), h^2 P_{t+1}]], gradient (0, h sigma_t).  Family B: P = 1/2, k = -1/2.
    h = Fr(1, 500)
    P, k = Fr(1, 2), Fr(-1, 2)
    H = [[h + P - P, h * (P + k)], [h * (P + k), h * h * P]]
    rec = dict(hessian_at_N1000=[[str(v) for v in row] for row in H],
               cross_term_zero=(H[0][1] == 0), H_dd_equals_h=(H[0][0] == h), H_uu_equals_h2_over_2=(H[1][1] == h * h / 2))
    with open(os.path.join(LOG, "toy_verifier.json")) as f:
        rec["logged_max_stage_loss"] = {r["N"]: r["famB"]["max_stage_loss"] for r in json.load(f)}
    print(json.dumps(rec), flush=True)
    dump("famB", rec)


# ------------------------------------------------------------------------------------------ rmaxrow
def part_rmaxrow():
    with open(os.path.join(LOG, "toy_rmax.json")) as f:
        d = json.load(f)
    out = {}
    for k in (0.5, 0.1):
        rows = [r for r in d if r["k"] == k]
        out[str(k)] = {r["N"]: dict(eta_hat_1=r["eta_hat"]["1"], rounded=f"{r['eta_hat']['1']:.3f}",
                                    break_stage=r["break_stage"]) for r in rows}
        print(k, {N: v["rounded"] for N, v in out[str(k)].items()}, flush=True)
    stage = [r["exact_everywhere_float"]["max_stage_loss"] for r in d if "exact_everywhere_float" in r]
    out["max_stage_loss_where_no_break"] = max(stage)
    print("max stage loss where the recursion does not break:", max(stage), flush=True)
    dump("rmaxrow", out)


if __name__ == "__main__":
    parts = dict(shE=part_shE, famB=part_famB, rmaxrow=part_rmaxrow)
    for q in sys.argv[1:]:
        print("====", q, flush=True)
        parts[q]()
