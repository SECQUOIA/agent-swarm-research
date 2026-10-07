"""Selection file for the full re-bounding run: every record used by the cert3
DP, with the group labels of logs/sel_cert3.json (others: 'other'), its
criticality and 'required' value (see select_records.py), ordered by
descending rbb run time (long runs first).
usage: python3 make_full_selection.py cert.pkl sel_cert3.json out.json"""
import json
import sys

import numpy as np

import load_cert

T = 6
P = load_cert.load(sys.argv[1]).__dict__
B, CS, cr = P["tables"]["CB"], P["tables"]["CSRC"], P["crecs"]
f = [None] * T
f[0] = B[0][0, :].astype(float)
for t in range(1, T - 1):
    f[t] = (f[t - 1][:, None] + B[t]).min(axis=0)
V = float((f[T - 2] + B[T - 1][:, 0]).min())
g = [None] * T
g[T - 2] = B[T - 1][:, 0].astype(float)
for t in range(T - 2, 0, -1):
    g[t - 1] = (B[t] + g[t][None, :]).min(axis=1)
crit, req = {}, {}
for t in range(T):
    fin = np.zeros(1) if t == 0 else f[t - 1]
    go = np.zeros(1) if t == T - 1 else g[t]
    rest = fin[:, None] + go[None, :] + np.zeros_like(B[t])
    for (r, c), v in np.ndenumerate(rest + B[t]):
        rid = int(CS[t][r, c])
        crit[rid] = min(crit.get(rid, np.inf), v - V)
        req[rid] = max(req.get(rid, -np.inf), V - rest[r, c])
sel = {s["rid"]: s for s in json.load(open(sys.argv[2]))}
items = []
for rid in crit:
    if rid in sel:
        it = dict(sel[rid])
    else:
        rq = req[rid]
        it = dict(rid=rid, group="other", crit=float(crit[rid]),
                  required=float(rq) + 1e-6 if np.isfinite(rq) else -1e30)
    items.append(it)
items.sort(key=lambda s: -cr[s["rid"]]["time"])
json.dump(items, open(sys.argv[3], "w"))
print(len(items), "records; V", V)
