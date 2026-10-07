"""Evaluate the cached MINLPLib KAN OSIL models at the input points that SCIP 9.0.1
reported in Zenodo record 14961066 (Karia, Lastrucci, Schweidtmann 2025).

Usage: python3 kan_points.py [perm]
  perm: also test every permutation of the input order at the given points.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])
_PUBLIC_HOME = str(_PublicPath.home())

import itertools
import sys
import time
import mpmath as mp
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/lit-network-r1'))
import osil_eval as oe

OSIL = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/%s.osil')
# (instance, formulation, SCIP status, SCIP primal, inputs x1..xd) from r3/r5-opt-overview.xlsx
PTS = [
    ("kan_r3_h1_n4", "Default", "optimal", "1.08116412047821E-3",
     ["0.99064970236898897", "0.98118960678561296", "0.96330313134142198"]),
    ("kan_r3_h1_n5", "Default", "optimal", "-1.3080995898235401E-2",
     ["0.99412127037819098", "0.98885022716926496", "0.97685176822519004"]),
    ("kan_r3_h1_n4", "ConvexHull", "optimal", "7.9828227535472295E-4",
     ["0.98916229100078301", "0.97813136210032403", "0.95632445269453803"]),
    ("kan_r3_h1_n9", "Default", "time limit", "9.5567809507278998",
     ["-1.08907507967747", "0.97341587029295795", "1.02891179923145"]),
    ("kan_r3_h1_n9", "ExploitSparsity", "time limit", "0.17526978600835699",
     ["1.0523144782999501", "1.1279242456326399", "1.23755796145988"]),
    ("kan_r5_h1_n3", "Default", "time limit", "513.31371069495503",
     ["0.68542730942835595", "-1.372950113236", "0.77871104039959305", "0.20459976324738899", "-0.86717959395975197"]),
    ("kan_r5_h1_n5", "ConvexHull", "time limit", "0.272518773754655",
     ["0.97604682102706297", "0.95449726853420402", "0.91180965630141997", "0.83184225004449197", "0.69343717737729405"]),
    ("kan_r5_h1_n5", "Default", "time limit", "0.880271357196307",
     ["0.96678629645174397", "0.95892040304794002", "0.98326854309470402", "1.00174758113586", "0.99228285719783804"]),
    ("kan_r5_h1_n8", "Default", "time limit", "185.119995647401",
     ["-1.25724838351926", "1.6137453625348199", "1.37310957823276", "1.37339325103637", "1.77221693275157"]),
    ("kan_r5_h1_n8", "ConvexHull", "time limit", "0.214075154166494",
     ["1.04753213484575", "1.09085126100152", "1.1938102834614901", "1.4329832642765801", "2.0372434754086401"]),
]
CERT = {"kan_r3_h1_n4": "0.0027812371525814", "kan_r3_h1_n5": "-0.011042679521782", "kan_r3_h1_n9": "0.012963659963475",
        "kan_r5_h1_n3": "-262.86422590922", "kan_r5_h1_n5": "0.27258325385485", "kan_r5_h1_n8": "0.069327860510525"}

perm = len(sys.argv) > 1 and sys.argv[1] == "perm"
cache = {}
for name, form, st, claim, xs in PTS:
    if name not in cache:
        cache[name] = oe.read(OSIL % name)
    V, obj, C = cache[name]
    inp = [j for j, v in enumerate(V) if v["lb"] == mp.mpf("-2.048") and v["ub"] == mp.mpf("2.048")]
    assert len(inp) == len(xs), (name, [V[j]["name"] for j in inp])
    orders = list(itertools.permutations(range(len(xs)))) if perm else [tuple(range(len(xs)))]
    for o in orders:
        t0 = time.time()
        fixed = {inp[k]: mp.mpf(xs[o[k]]) for k in range(len(xs))}
        x, part, amb = oe.propagate(V, C, fixed)
        f, vp, vo, vb = oe.report(V, obj, C, x, part)
        print(f"{name} {form} ({st}) inputs {[V[j]['name'] for j in inp]} order {o}: OSIL objective {mp.nstr(f, 12)};"
              f" SCIP {claim}; diff {mp.nstr(f - mp.mpf(claim), 4)}; certified min R {CERT[name]};"
              f" max viol partition {mp.nstr(vp[0], 3)} ({vp[1]}), other rows {mp.nstr(vo[0], 3)} ({vo[1]}),"
              f" bounds {mp.nstr(vb[0], 3)} ({vb[1]}); ambiguous binary groups {len(amb)}; {time.time() - t0:.1f}s", flush=True)
