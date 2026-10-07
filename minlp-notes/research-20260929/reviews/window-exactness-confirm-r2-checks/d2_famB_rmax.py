"""Confirmation round 2, items 3 and 6 (and the Summary rewording of item 4).

famB: derive the family-B stage residual of [V]'s toy symbolically from the definitions
  (x_{t+1} = x_t + h u_t, L_t = h [(x - a)^2/2 + k x u], S_t = p_t x + P (x - xbar_t)^2 / 2,
  discrete adjoint p_t = p_{t+1} + h (xbar_t - a + k ubar_t)), with P = 1/2, k = -1/2,
  and show rho_t(xbar + d, ubar + omega) - rho_t(xbar, ubar) = h d^2/2 + h sigma omega + h^2 omega^2/4,
  sigma = k xbar_t + p_{t+1}.  Independent of toy.py.
rmax: read logs/toy_rmax.json of the report (read-only) and print the eta_hat_1 rows,
  break patterns and the largest float stage loss where the recursion does not break.
"""
import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "..", "..", "theory-bangbang", "window", "logs")


def famB():
    h, a, xb, ub, p1, d, om = sp.symbols("h a xbar ubar p_next d omega", real=True)
    P, k = sp.Rational(1, 2), sp.Rational(-1, 2)
    p0 = p1 + h * (xb - a + k * ub)
    xb1 = xb + h * ub

    def rho(x, u):
        L = h * ((x - a) ** 2 / 2 + k * x * u)
        S1 = p1 * (x + h * u) + P * (x + h * u - xb1) ** 2 / 2
        S0 = p0 * x + P * (x - xb) ** 2 / 2
        return L + S1 - S0
    diff = sp.expand(rho(xb + d, ub + om) - rho(xb, ub))
    sigma = k * xb + p1
    target = sp.expand(h * d ** 2 / 2 + h * sigma * om + h ** 2 * om ** 2 / 4)
    return dict(difference=str(diff), identity_holds=bool(sp.simplify(diff - target) == 0))


def rmax():
    with open(os.path.join(LOG, "toy_rmax.json")) as f:
        d = json.load(f)
    rows = {}
    for r in d:
        rows.setdefault(str(r["k"]), []).append(
            dict(N=r["N"], interior=bool(r["frac"]), eta_hat_1=round(r["eta_hat"]["1"], 6),
                 break_stage=r["break_stage"]))
    losses = [(r["k"], r["N"], r["exact_everywhere_float"]["max_stage_loss"]) for r in d
              if r.get("exact_everywhere_float")]
    worst = max(losses, key=lambda z: z[2])
    k05 = rows["0.5"]
    return dict(rows=rows, worst_stage_loss_where_no_break=worst,
                k05_breaks_exactly_on_interior_grids=all((r["break_stage"] is not None) == r["interior"] for r in k05),
                k01_k005_never_break=all(r["break_stage"] is None for kk in ("0.1", "0.05") for r in rows[kk]),
                all_eta_hat_1_positive=all(r["eta_hat_1"] > 0 for v in rows.values() for r in v))


if __name__ == "__main__":
    out = dict(famB=famB(), rmax=rmax())
    print(json.dumps(out, indent=1))
    with open(os.path.join(HERE, "logs", "d2_famB_rmax.json"), "w") as f:
        json.dump(out, f, indent=1)
