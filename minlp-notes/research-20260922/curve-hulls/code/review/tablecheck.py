"""Print dual bounds, root bounds and cut counts from the author's raw results files.
python tablecheck.py"""
import glob, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ["results", "results_seed"]:
    for f in sorted(glob.glob(os.path.join(HERE, "..", d, "*.out"))):
        recs = []
        for line in open(f):
            line = line.strip()
            if line.startswith("{"):
                recs.append(json.loads(line))
        for r in recs:
            print(d, os.path.basename(f), r.get("mode"), "seed", r.get("seed"), "tl", r.get("tl"), "status", r.get("status"),
                  "root", None if "root" not in r else round(r["root"]["dual"], 4),
                  "dual", r.get("dual"), "primal", r.get("primal"), "ncuts", r.get("ncuts"), "time", round(r.get("time", 0)),
                  "chk", None if not r.get("incumbent_check") else r["incumbent_check"].get("max_viol", r["incumbent_check"]))
        if not recs:
            print(d, os.path.basename(f), "NO JSON RECORD")
