"""Sample rerun of the coupling-row census heuristics (recheck of
theory-coupling/coupling.md, Section 7.3).

1. Reruns the author's per-instance functions census_k.work (densest first),
   census_k2.work (bag rule) and census_k3.work (restricted eligibility) on a
   sample of instances, in one process, and compares every field except the
   timing with the saved JSONL records.
2. For the rows removed by the unrestricted bag rule, classifies each row
   (linear equality / linear inequality / nonlinear) with a separate raw XML
   parse of the OSIL file (not the author's osil.read), and compares with the
   labels in logs/census_k_rows.log.

Usage: python3 r2_census_sample.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET

CP = (_PUBLIC_REPO + '/research-20260929/theory-coupling')
sys.dont_write_bytecode = True  # do not leave __pycache__ in the author's folder
sys.path.insert(0, CP)
import census_k  # noqa: E402
import census_k2  # noqa: E402
import census_k3  # noqa: E402
from census_k import rowdata, fac_graph, read, OSIL_DIR, TARGET  # noqa: E402
from census_k2 import width_and_bag, ROWBASE, MAXR, TCAP  # noqa: E402

SAMPLE = ["casctanks", "powerflow0030r", "powerflow0057r", "wastepaper6", "tln12",
          "kall_ellipsoids_tc03c", "waterno1_03", "sfacloc1_4_95", "ann_cumene_tanh",
          "waternd_pescara", "waterno2_03", "kriging_peaks-full100"]
NS = "{os.optimizationservices.org}"


def load(path):
    return {json.loads(l)["name"]: json.loads(l) for l in open(path)}


def same(a, b):
    a = {k: v for k, v in a.items() if k != "secs"}
    b = {k: v for k, v in b.items() if k != "secs"}
    return json.loads(json.dumps(a)) == json.loads(json.dumps(b))


def raw_row_classes(path):
    """Row index -> 'L=', 'L<>' or 'NL' from the raw OSIL XML."""
    root = ET.parse(path).getroot()
    data = root.find(f"{NS}instanceData")
    cons = data.find(f"{NS}constraints")
    bounds = []
    for c in cons:
        mult = int(c.get("mult", "1"))
        for _ in range(mult):
            bounds.append((c.get("lb"), c.get("ub")))
    nonlin = set()
    q = data.find(f"{NS}quadraticCoefficients")
    if q is not None:
        for t in q:
            nonlin.add(int(t.get("idx")))
    nle = data.find(f"{NS}nonlinearExpressions")
    if nle is not None:
        for e in nle:
            nonlin.add(int(e.get("idx")))
    out = {}
    for i, (lb, ub) in enumerate(bounds):
        if i in nonlin:
            out[i] = "NL"
        else:
            eq = lb is not None and ub is not None and float(lb) == float(ub)
            out[i] = "L=" if eq else "L<>"
    return out


def bag_rule_rows(name):
    I = read(os.path.join(OSIL_DIR, name + ".osil"))
    rows = rowdata(I)
    free = census_k3.free_rows(I, rows)
    removed, order, t0 = set(), [], time.time()
    while True:
        adj = fac_graph(rows, free | removed)
        w, bag = width_and_bag(adj)
        if w is None or w <= TARGET or len(removed) >= MAXR or time.time() - t0 > TCAP:
            break
        rn = [v for v in bag if isinstance(v, int) and v >= ROWBASE]
        if not rn:
            break
        best = max(rn, key=lambda v: len(adj[v]))
        removed.add(best - ROWBASE - 1)
        order.append(best - ROWBASE - 1)
    return order


def main():
    L = CP + "/logs/"
    ref = {"census_k": load(L + "census_k.jsonl"), "census_k2": load(L + "census_k2.jsonl"),
           "census_k3": load(L + "census_k3.jsonl")}
    labels_log = {}
    for line in open(L + "census_k_rows.log"):
        m = re.match(r"^(\S+): k=\d+ .*: (\[.*\])$", line.strip())
        if m:
            labels_log[m.group(1)] = eval(m.group(2))
    n_ok = n_all = 0
    for name in SAMPLE:
        for mod, fn in (("census_k", census_k.work), ("census_k2", census_k2.work),
                        ("census_k3", census_k3.work)):
            if name not in ref[mod]:
                continue
            t0 = time.time()
            rec = fn(name)
            ok = same(rec, ref[mod][name])
            n_all += 1
            n_ok += ok
            keys = {"census_k": ("w_full", "w_free", "k_heur"), "census_k2": ("k_bag",),
                    "census_k3": ("w0", "k_dense_lin", "k_bag_lin", "k_dense_lineq", "k_bag_lineq")}[mod]
            print(f"{name:24s} {mod:9s} identical={ok} " +
                  " ".join(f"{k}={rec.get(k)}" for k in keys) + f" ({time.time() - t0:.1f}s)")
        if name in labels_log:
            order = bag_rule_rows(name)
            cls = raw_row_classes(os.path.join(OSIL_DIR, name + ".osil"))
            mine = [cls[r] for r in order]
            print(f"{name:24s} row classes (raw XML) {mine}; log agrees={mine == labels_log[name]}")
    print(f"\nrecords identical (ignoring secs): {n_ok}/{n_all}")


if __name__ == "__main__":
    main()
