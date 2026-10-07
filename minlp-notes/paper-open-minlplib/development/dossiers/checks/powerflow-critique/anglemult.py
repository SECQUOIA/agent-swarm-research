# Critic (run from /tmp/pfcrit/rev): largest stored angle-row multiplier per 0039p leaf
import json, sys
sys.path.insert(0, "/tmp/pfcrit/rev")
import pf_model as pm
M = pm.decode("powerflow0039p")
D = json.load(open("/tmp/pfcrit/rev/logs/powerflow0039p.bb3t.json"))
idx = [i for i, r in enumerate(M["rows"]) if r["kind"] == "angle"]
print("angle rows", len(idx), "M rows", len(M["rows"]), "raw", len(D["leaves"][0]["raw"]))
for k, lf in enumerate(D["leaves"]):
    vals = [abs(v or 0) for i in idx for v in lf["raw"][i][1:]]
    print("leaf", k, "max angle multiplier %.3e" % max(vals), "sum %.3e" % sum(vals))
