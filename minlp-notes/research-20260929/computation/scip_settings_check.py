"""After review: which propagators/separators actually ran (probe3, amp 0.3,
n = 6, seed 0, eps 1e-4) under default, obbt, and emph_opt. Writes SCIP
statistics to logs/settings_check_<variant>_n6.txt and prints the relevant lines."""
import re
import run_scip as R
from pyscipopt import SCIP_PARAMEMPHASIS
import instances as I
for v in ("default", "obbt", "emph_opt"):
    m, x, t, c = I.build_scip(6, 0, amp=0.3)
    m.setParam("timing/clocktype", 1); m.setParam("limits/time", 300)
    m.setParam("limits/absgap", 1e-4); m.setParam("limits/gap", 0.0)
    if v == "obbt":
        m.setParam("propagating/obbt/freq", 1)
    if v == "emph_opt":
        m.setEmphasis(SCIP_PARAMEMPHASIS.OPTIMALITY)
    m.optimize()
    fn = f"logs/settings_check_{v}_n6.txt"
    m.writeStatistics(fn)
    txt = open(fn).read().split("\n")
    print(f"== {v}: nodes {m.getNNodes()}")
    sec = None
    for l in txt:
        if l and not l.startswith(" "):
            sec = l.split(":")[0].strip()
        if sec in ("Propagators", "Separators") and re.match(r"\s+(obbt|minor|interminor|rlt|intobj|convexproj|gauge|eccuts)\s*:", l):
            print(sec, "|", l.strip())
