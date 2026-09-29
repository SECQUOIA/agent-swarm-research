"""Item (6), tolerance sentence of Section 7: largest stored relaxation values above OPT (relative).
usage: python3 rc_exceed.py > rc_exceed.log"""
import json, os
from rc_common import DATA

def load(fn):
    return [json.loads(l) for l in open(os.path.join(DATA, fn))]

out = []
for fn, ofn in [("mech_n20_k3.jsonl", "opt_mech_n20_k3.jsonl"), ("mech_n40_k3.jsonl", "opt_mech_n40_k3.jsonl"),
                ("cmp_p100_k3.jsonl", "opt_cmp_p100_k3.jsonl")]:
    opt = {(o["p"], o["seed"], o["n"]): o for o in load(ofn)}
    for r in load(fn):
        o = opt.get((r["p"], r["seed"], r["n"]))
        if not o or "OPT" not in o:
            continue
        OPT = min(r["fS"], o["OPT"])
        for m in ("sdp1", "sdp2", "zb"):
            if r.get(m) is not None and r[m] > OPT:
                out.append(((r[m] - OPT) / OPT, fn, m, r["p"], r["seed"], r.get("alpha"), r.get("zb_solver")))
for r in load("hardzb.jsonl"):
    for m in ("sdp1", "zb"):
        if r[m] > r["opt"]:
            out.append(((r[m] - r["opt"]) / r["opt"], "hardzb", m, r["p"], r["seed"], r["alpha"], r["k"]))
for t in sorted(out, reverse=True)[:8]:
    print("%.2e %s %s p=%s seed=%s alpha=%s %s" % t)
print("rows above OPT by > 1e-6 relative:", sum(t[0] > 1e-6 for t in out))
