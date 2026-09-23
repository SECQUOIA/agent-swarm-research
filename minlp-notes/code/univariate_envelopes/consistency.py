"""Soundness check: every mode's [dual, primal] interval must contain the MINLPLib reference optimum (within tolerance)."""
import csv, json, sys
ref = {}
with open("../minlp_solver_lab/instances/instancedata.csv") as fh:
    for row in csv.DictReader(fh, delimiter=";"):
        try: ref[row["name"]] = (float(row["primalbound"]), float(row["dualbound"]))
        except ValueError: pass
bad = 0
for l in open(sys.argv[1]):
    r = json.loads(l)
    if r.get("status") == "error" or r["instance"] not in ref: continue
    pb, db = ref[r["instance"]]
    sgn = 1 if r["sense"] == "min" else -1
    tol = 1e-3 * max(1.0, abs(pb))
    if r.get("dual") is not None and sgn * (r["dual"] - pb) > tol:
        bad += 1; print("DUAL BOUND EXCEEDS REFERENCE PRIMAL:", r["instance"], r["mode"], "dual", r["dual"], "ref primal", pb)
    if r.get("primal") is not None and sgn * (db - r["primal"]) > tol:
        bad += 1; print("PRIMAL BETTER THAN REFERENCE DUAL:", r["instance"], r["mode"], "primal", r["primal"], "ref dual", db)
print("violations:", bad)
