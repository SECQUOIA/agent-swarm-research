"""Build Delsarte-Yudin lower-bound certificates for elec25/50/100/200 (verified by elec_verify.py).

1. Solve the LP  max (N^2 h_0 - N sum_k h_k)/2  s.t.  sum_k h_k P_k(1 - s^2/2) <= 1/s on an s-grid in (0, 2],
   h_k >= 0 (k >= 1), with Gurobi (floating point; only used to find a candidate).
2. Round h to exact decimals, then lower h_0 by a rational delta until the exact check passes
   (lowering h_0 by delta adds delta*s to g(s) = 1 - s h(1 - s^2/2) and costs N(N-1) delta/2 in the bound).
3. Write certs/<instance>.json. The bound depends only on the stored exact h.
Usage: python elec_yudin.py [K]
"""
import json
import os
import sys
from fractions import Fraction

import gurobipy as gp
import numpy as np
from numpy.polynomial import legendre as L

from elec_model import check as check_model
from elec_verify import g_poly, bernstein_positive

HERE = os.path.dirname(os.path.abspath(__file__))


def solve_lp(N, K, ns=20000):
    s = np.linspace(2e-3, 2, ns)
    P = L.legvander(1 - s * s / 2, K)
    env = gp.Env(empty=True); env.setParam("OutputFlag", 0); env.start()
    m = gp.Model(env=env)
    h = m.addMVar(K + 1, lb=np.r_[-np.inf, np.zeros(K)])
    m.addConstr(P @ h <= 1 / s)
    m.setObjective((N * N * h[0] - N * h.sum()) / 2, gp.GRB.MAXIMIZE)
    m.Params.FeasibilityTol = 1e-9; m.Params.OptimalityTol = 1e-9
    m.optimize()
    return m.ObjVal, h.X


def max_violation(hf):
    s = np.linspace(1e-4, 2, 4_000_001)
    return float(np.max(L.legval(1 - s * s / 2, hf) - 1 / s))


def build(name, K):
    N = check_model(name)
    lpval, hx = solve_lp(N, K)
    h = [Fraction(repr(float(x))) for x in hx]
    h = [h[0]] + [max(x, Fraction(0)) for x in h[1:]]
    viol = max_violation(np.array([float(x) for x in h]))
    delta = Fraction(f"{max(viol, 0) * 2 + 1e-12:.1e}")
    while True:
        hc = [h[0] - delta] + h[1:]
        g = g_poly(hc)
        for sv in [Fraction(k, 20) for k in range(41)]:  # exact g vs float definition (consistency check)
            ge = float(sum(c * sv ** i for i, c in enumerate(g)))
            gf = 1 - float(sv) * L.legval(1 - float(sv) ** 2 / 2, np.array([float(x) for x in hc]))
            assert abs(ge - gf) < 1e-8, (sv, ge, gf)
        ok = bernstein_positive(g)[0]
        print(f"  {name}: delta={float(delta):.1e} exact positivity proof: {ok}", flush=True)
        if ok:
            break
        delta *= 4
    bound = (N * N * hc[0] - N * sum(hc)) / 2
    cert = {
        "instance": name, "N": N, "K": K,
        "claim": "objective >= bound for every feasible point",
        "basis": "Legendre P_k with P_k(1)=1; h(t)=sum_k h[k] P_k(t)",
        "h": [_dec(x) for x in hc],
        "bound": f"{bound.numerator}/{bound.denominator}",
        "bound_float": float(bound), "lp_value_float": lpval, "delta": str(delta),
    }
    with open(os.path.join(HERE, "certs", name + ".json"), "w") as fh:
        json.dump(cert, fh, indent=1)
    return lpval, bound


def _dec(x):
    """Exact decimal string of a Fraction whose denominator divides a power of 10."""
    p = 0
    while 10 ** p % x.denominator:
        p += 1
        assert p < 400
    num = abs(x.numerator) * (10 ** p // x.denominator)
    digits = str(num).rjust(p + 1, "0")
    out = ("-" if x < 0 else "") + (digits[:-p] + "." + digits[-p:] if p else digits)
    assert Fraction(out) == x
    return out


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    for nm in ["elec25", "elec50", "elec100", "elec200"]:
        lpval, bound = build(nm, K)
        print(f"{nm}: LP {lpval:.6f}  certified {float(bound):.6f}", flush=True)
