"""Choose certification records of cert3 to re-bound (own code).

For every record: 'crit' = min over the leaf pairs it certifies of
(best path value through the pair - V), and 'required' = max over those leaf
pairs of (V - best prefix - best suffix): the smallest bound of this record
that leaves the DP value V unchanged (the other periods fixed).

Groups:
  crit   all records with crit <= CRIT (near-minimal paths)
  rand   random finite-bound records (seed below)
  inf    random records with rbb bound +inf (FBBT proved the box empty)
  obbt0  random records certified at the root by rbb's cutoff OBBT (0 nodes)
  retry  records produced by the rc=False retry
usage: python3 select_records.py cert.pkl out.json CRIT NRAND NINF NOBBT SEED
"""
import json
import random
import sys

import numpy as np

import load_cert

T = 6


def main():
    pkl, out = sys.argv[1], sys.argv[2]
    crit_max, nrand, ninf, nobbt, seed = float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(
        sys.argv[6]), int(sys.argv[7])
    P = load_cert.load(pkl).__dict__
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
        th = rest + B[t]
        for (r, c), v in np.ndenumerate(th):
            rid = int(CS[t][r, c])
            crit[rid] = min(crit.get(rid, np.inf), v - V)
            req[rid] = max(req.get(rid, -np.inf), V - rest[r, c])
    used = sorted(crit)
    sel = {}

    def add(rid, group):
        if rid not in sel:
            rq = req[rid]
            sel[rid] = dict(rid=rid, group=group, crit=float(crit[rid]),
                            required=float(rq) + 1e-6 if np.isfinite(rq) else -1e30)
    for rid in used:
        if crit[rid] <= crit_max:
            add(rid, "crit")
    for i, r in enumerate(cr):
        if r["retry"] is not None and i in crit:
            add(i, "retry")
    rng = random.Random(seed)
    fin_ = [i for i in used if np.isfinite(cr[i]["bound"]) and cr[i]["nodes"] > 0 and i not in sel]
    inf_ = [i for i in used if not np.isfinite(cr[i]["bound"]) and np.isfinite(req[i]) and i not in sel]
    ob_ = [i for i in used if np.isfinite(cr[i]["bound"]) and cr[i]["nodes"] == 0 and i not in sel]
    for i in rng.sample(fin_, min(nrand, len(fin_))):
        add(i, "rand")
    for i in rng.sample(inf_, min(ninf, len(inf_))):
        add(i, "inf")
    for i in rng.sample(ob_, min(nobbt, len(ob_))):
        add(i, "obbt0")
    items = sorted(sel.values(), key=lambda s: s["rid"])
    json.dump(items, open(out, "w"), indent=0)
    from collections import Counter
    print("V", V, "selected", len(items), Counter(s["group"] for s in items))
    print("inf records with finite 'required':", len(inf_) + sum(1 for s in items if s["group"] == "inf"),
          "of", sum(1 for i in used if not np.isfinite(cr[i]["bound"])))


if __name__ == "__main__":
    main()
