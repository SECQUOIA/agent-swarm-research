"""Rerun a few SCIP data points of the scaling study and check that the claimed settings
were applied (SCIP 10 via PySCIPOpt).

1. Node counts: run_scip.solve (the study's own runner) for small n, seed 0, eps 1e-4.
2. Settings: for each variant, rebuild the model with the same parameter changes, dump the
   changed parameters, and read the statistics (node selector used, obbt propagator calls).
"""
import sys, os, json, re, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../computation"))
import run_scip as R
import instances as I
from pyscipopt import SCIP_PARAMEMPHASIS

outdir = os.path.join(os.path.dirname(__file__), "logs")
cases = json.loads(sys.argv[1])
for variant, amp, n, seed in cases:
    rec = R.solve(n, seed, 1e-4, variant, 300, amp=amp)
    print(json.dumps({k: rec[k] for k in ("variant", "amp", "n", "seed", "status", "nodes", "time", "primal", "dual")}),
          flush=True)

# settings inspection (n = 6, amp 0.3, seed 0)
for variant in ("default", "bestfirst", "obbt", "emph_opt", "combo"):
    m, x, t, c = I.build_scip(6, 0, "single" if variant == "combo" else variant, amp=0.3)
    m.setParam("timing/clocktype", 1); m.setParam("limits/time", 300)
    m.setParam("limits/absgap", 1e-4); m.setParam("limits/gap", 0.0)
    if variant in ("emph_opt", "combo"):
        m.setEmphasis(SCIP_PARAMEMPHASIS.OPTIMALITY)
    if variant in ("bestfirst", "combo"):
        for k, v in R.VARIANT_PARAMS["bestfirst"].items():
            m.setParam(k, v)
    if variant in ("obbt", "combo"):
        for k, v in R.VARIANT_PARAMS["obbt"].items():
            m.setParam(k, v)
    pf = os.path.join(outdir, f"scip_params_changed_{variant}.set")
    m.writeParams(pf, onlychanged=True)
    m.optimize()
    sf = os.path.join(outdir, f"scip_stats_{variant}_n6_amp0.3_seed0.txt")
    m.writeStatistics(sf)
    txt = open(sf).read()
    obbt = re.search(r"^\s*obbt\s*:\s*(\d+)", txt, re.M)
    print(json.dumps(dict(variant=variant, nodes=m.getNNodes(), status=m.getStatus(),
                          obbt_propagate_calls=int(obbt.group(1)) if obbt else None,
                          nchanged_params=sum(1 for l in open(pf) if "=" in l and not l.startswith("#")))),
          flush=True)
