"""Filter MINLPLib metadata to screening candidates; write candidates.csv and screen_jobs.txt.

Criteria (all from instancedata.csv, MINLPLib metadata of the local OSiL set):
- OSiL file present;
- convex flag False, or empty (convexity undetermined by MINLPLib);
- MINLPLib reports the instance solved: finite primal bound and gap <= 1e-4;
- at least one continuous variable appears in a nonlinear term;
- at most 1000 variables and 1000 constraints.
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
META = os.path.join(HERE, "../../../code/minlp_solver_lab/instances/instancedata.csv")
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
SCREEN_TLIM = 20

KEEP = ["name", "probtype", "convex", "nvars", "ncons", "nbinvars", "nintvars", "nnlvars", "nnlbinvars",
        "nnlintvars", "nquadcons", "npolynomcons", "nsignomcons", "nquadfunc", "nlincons", "objsense",
        "objtype", "objcurvature", "conscurvature", "primalbound", "dualbound", "gap",
        "opabs", "opmin", "opsignpower", "opexp", "oplog", "opsin", "opcos", "opdiv", "opsqrt",
        "oppower", "opvcpower", "opcvpower", "opmul"]


def fl(x):
    try:
        return float(x)
    except ValueError:
        return math.nan


def main():
    rows = list(csv.DictReader(open(META), delimiter=";"))
    have = {f[:-5] for f in os.listdir(OSIL) if f.endswith(".osil")}
    reasons = {}
    cands = []
    for r in rows:
        nm = r["name"]
        if nm not in have:
            reasons.setdefault("no osil", []).append(nm)
        elif r["convex"] == "True":
            reasons.setdefault("convex", []).append(nm)
        elif not (math.isfinite(fl(r["primalbound"])) and fl(r["gap"]) <= 1e-4):
            reasons.setdefault("not solved in MINLPLib", []).append(nm)
        elif int(r["nnlvars"]) - int(r["nnlbinvars"]) - int(r["nnlintvars"]) <= 0:
            reasons.setdefault("no continuous nonlinear variable", []).append(nm)
        elif int(r["nvars"]) > 1000 or int(r["ncons"]) > 1000:
            reasons.setdefault("more than 1000 variables or constraints", []).append(nm)
        else:
            cands.append(r)
    with open(os.path.join(HERE, "candidates.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=KEEP, extrasaction="ignore")
        w.writeheader()
        for r in cands:
            w.writerow(r)
    with open(os.path.join(HERE, "screen_jobs.txt"), "w") as fh:
        for r in cands:
            fh.write(f"{r['name']} default 0 {SCREEN_TLIM}\n")
    print(f"{len(rows)} metadata rows, {len(have)} OSiL files, {len(cands)} candidates")
    for k, v in reasons.items():
        print(f"  excluded ({k}): {len(v)}")


if __name__ == "__main__":
    main()
