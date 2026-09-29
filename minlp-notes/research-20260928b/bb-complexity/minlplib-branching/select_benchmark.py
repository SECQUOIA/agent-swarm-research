"""Select the benchmark from the screening runs; write selected.txt and job files.

    python3 select_benchmark.py

Criteria on the screening run (default settings, seed 0, 20 s CPU limit):
status optimal, solving time >= 1 s, at least 50 nodes. At most FAMILY_CAP
instances per family (name prefix, see fam()); larger families are sampled
with random.Random(0) over the sorted names.
"""
import csv
import json
import os
import random
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FAMILY_CAP = 3
MAIN_TLIM = 120
CORE = ["default", "lp", "lp_noclamp", "mix_noclamp", "mid"]
TRACE = ["default", "lp", "lp_noclamp"]
OPTIONAL = ["trig0", "couenne", "lp_c05"]
SWEEP = ["default", "lp", "lp_noclamp", "mid"]
SWEEP_DELTAS = [1e-2, 1e-4, 1e-6]
SWEEP_TLIM = 60
SWEEP_MAXVARS = 20
TRACE_TLIM = 30


def fam(n):
    m = re.match(r"ex(\d+)_", n)
    if m:
        return "ex" + m.group(1)
    if re.match(r"(st_|nvs|mathopt|prob|gear|hs|alan)", n):
        return n  # GLOBALLib/MacMINLP collections of unrelated small problems
    return re.match(r"[a-z]+", n.lower()).group(0)


def main():
    R = [json.loads(ln) for ln in open(os.path.join(HERE, "results/screen.jsonl"))]
    ok = sorted(r["inst"] for r in R if r["status"] == "optimal" and r["time"] >= 1 and r["nodes"] >= 50)
    byfam = defaultdict(list)
    for i in ok:
        byfam[fam(i)].append(i)
    rng = random.Random(0)
    sel, dropped = [], []
    for f in sorted(byfam):
        members = byfam[f]
        keep = members if len(members) <= FAMILY_CAP else sorted(rng.sample(members, FAMILY_CAP))
        sel += keep
        dropped += [i for i in members if i not in keep]
    sel.sort()
    with open(os.path.join(HERE, "selected.txt"), "w") as fh:
        fh.write("\n".join(sel) + "\n")
    with open(os.path.join(HERE, "main_jobs.txt"), "w") as fh:
        # seed 0 of every setting first, so a partial batch is still balanced
        for seed in (0, 1, 2):
            for s in CORE:
                for i in sel:
                    extra = f" --solfile {HERE}/results/sols/{i}.json" if (s == "default" and seed == 0) else ""
                    fh.write(f"{i} {s} {seed} {MAIN_TLIM}{extra}\n")
    with open(os.path.join(HERE, "trace_jobs.txt"), "w") as fh:
        for s in TRACE:
            for i in sel:
                fh.write(f"{i} {s} 0 {TRACE_TLIM} --trace\n")
    with open(os.path.join(HERE, "optional_jobs.txt"), "w") as fh:
        for s in OPTIONAL:
            for i in sel:
                fh.write(f"{i} {s} 0 {MAIN_TLIM}\n")
    # absolute-gap sweep: continuous instances (no binary/integer variables) with at most
    # SWEEP_MAXVARS variables; absgap = delta * max(1, |MINLPLib primal bound|)
    meta = {r["name"]: r for r in csv.DictReader(open(os.path.join(HERE, "candidates.csv")))}
    sweep = [i for i in sel if int(meta[i]["nbinvars"]) + int(meta[i]["nintvars"]) == 0
             and int(meta[i]["nvars"]) <= SWEEP_MAXVARS]
    with open(os.path.join(HERE, "optional_jobs.txt"), "a") as fh:
        for d in SWEEP_DELTAS:
            for s in SWEEP:
                for i in sweep:
                    eps = d * max(1.0, abs(float(meta[i]["primalbound"])))
                    fh.write(f"{i} {s}@abs{eps:.6g} 0 {SWEEP_TLIM}\n")
    print(f"{len(ok)} instances meet the criteria; {len(sel)} selected; dropped by family cap: {dropped}")
    print(f"absolute-gap sweep instances ({len(sweep)}): {' '.join(sweep)}")


if __name__ == "__main__":
    main()
