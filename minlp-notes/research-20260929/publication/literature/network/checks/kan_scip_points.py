"""Evaluate the MINLPLib KAN models at the input points that SCIP 9.0.1 reported
as optimal in Karia, Lastrucci, Schweidtmann (2025), Zenodo record 14961066.

For each point x (Rosenbrock coordinates), the input roots u of the decoded OSIL
model are obtained from the exact scaling rows (the class member with bounds
[-2.048, 2.048]); all other variables are then propagated at 60 digits with the
wave-3 code (kan_check.full_point), which satisfies every non-partition row to
~1e-60. The printed objective is therefore the value of the network relaxation R
(and of the intended network) at that input, to be compared with SCIP's claim and
with the certified minimum of R.  Floating-point inputs are used as given.

    python3 kan_scip_points.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import sys
from fractions import Fraction

import mpmath as mp

sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/open-instances-wave3/kan'))
import kan_check as kc  # noqa: E402
import kan_model as km  # noqa: E402

# (instance, configuration, SCIP status, SCIP primal = dual (or primal), x reported by SCIP)
CASES = [
    ("kan_r3_h1_n4", "Default", "optimal", "1.08116412047821e-3",
     ["0.9906497023689892", "0.9811896067856135", "0.9633031313414224"]),
    ("kan_r3_h1_n5", "Default", "optimal", "-1.30809958982354e-2",
     ["0.99412127037819098", "0.98885022716926496", "0.97685176822519004"]),
    ("kan_r5_h1_n5", "ConvexHull", "time limit (primal)", "0.272518773754655",
     ["0.97604682102706297", "0.95449726853420402", "0.91180965630141997",
      "0.83184225004449197", "0.69343717737729405"]),
]
CERT = {"kan_r3_h1_n4": "0.0027812371525814", "kan_r3_h1_n5": "-0.011042679521782",
        "kan_r5_h1_n5": "0.27258325385485"}


def scaled_members(M):
    out = []
    for R in M["inputs"]:
        mem = [(v, a, b) for (v, a, b) in M["classes"][R]
               if M["lb"][v] == Fraction(-2048, 1000) and M["ub"][v] == Fraction(2048, 1000)]
        assert len(mem) == 1, (R, mem)
        out.append(mem[0])
    return out


mp.mp.dps = 60
for name, conf, status, claim, xs in CASES:
    M = km.decode(name)
    mem = scaled_members(M)
    names = [M["I"]["names"][v] for v, _, _ in mem]
    # order the inputs by the index of their scaled member (Pyomo order x1, x2, ...)
    order = sorted(range(len(mem)), key=lambda i: mem[i][0])
    u = [None] * len(mem)
    for k, i in enumerate(order):
        v, a, b = mem[i]
        u[i] = (mp.mpf(xs[k]) - mp.mpf(b.numerator) / b.denominator) / (mp.mpf(a.numerator) / a.denominator)
    x, r = kc.point_report(M, u, f"{name} at SCIP {conf} point (scaled vars {[names[i] for i in order]}):")
    print(f"   SCIP claim ({status}): {claim};  certified min of R: {CERT[name]};"
          f"  value at SCIP input minus SCIP claim: {mp.nstr(r['obj'] - mp.mpf(claim), 6)}")
