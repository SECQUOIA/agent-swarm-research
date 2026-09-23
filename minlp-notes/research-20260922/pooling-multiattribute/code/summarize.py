"""Summarize root-bound gap closure per relaxation from out/*.log."""
import json, glob, os
ref = json.load(open("random_haverly_reference.json"))
glob_opt = {}
for f in ["out/rh_global.jsonl"]:
    if os.path.exists(f):
        for l in open(f):
            if l.startswith("{"):
                r = json.loads(l)
                if r["status"] == 2: glob_opt[r["name"]] = r["primal"]
MODES = ["pq", "L1", "D1", "Abox", "Apoly", "D"]
rows = []
for f in sorted(glob.glob("out/*.log")):
    res = [l for l in open(f) if l.startswith("RESULT")]
    if not res: continue
    r = json.loads(res[-1][7:])
    name = r["name"]
    opt = r["opt"] if r["opt"] is not None else glob_opt.get(name, (ref.get(name) or {}).get("zstar"))
    if opt is None: continue
    zpq = r["pq"]["lb"]; gap = opt - zpq
    row = dict(name=name, K=r["K"], opt=opt, pq=zpq, gap_pct=100 * gap / abs(opt))
    for m in MODES[1:]:
        if m in r:
            row[m + "_lb"] = r[m]["lb"]; row[m + "_ub"] = r[m]["ub"]
            row[m] = 100 * (r[m]["lb"] - zpq) / gap if gap > 1e-6 else None
            row[m + "_ubc"] = 100 * (r[m]["ub"] - zpq) / gap if gap > 1e-6 else None
    rows.append(row)
print(f"{'instance':38s} K  gap%   closed% by (valid lower bound; [master value])")
print(f"{'':38s}       " + "  ".join(f"{m:>15s}" for m in MODES[1:]))
for r in rows:
    if r["gap_pct"] < 1e-4:
        print(f"{r['name']:38s} {r['K']}  {r['gap_pct']:5.2f}  (pq exact)"); continue
    print(f"{r['name']:38s} {r['K']}  {r['gap_pct']:5.2f}  " + "  ".join(
        (f"{r[m]:6.1f} [{r[m+'_ubc']:6.1f}]" if r.get(m) is not None else f"{'-':>15s}") for m in MODES[1:]))
json.dump(rows, open("summary.json", "w"), indent=1)
