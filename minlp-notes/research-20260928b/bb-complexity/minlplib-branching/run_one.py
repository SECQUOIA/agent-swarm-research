"""One SCIP run on a MINLPLib OSiL instance.

    python3 run_one.py INSTANCE SETTING SEED TIMELIMIT [--trace] [--solfile FILE]

SETTING is a key of SETTINGS, optionally followed by "@abs<value>" to set
limits/absgap (for example "lp@abs0.01").

Prints one compact JSON line on stdout (the last line). --trace adds a
histogram of spatial branching points (continuous variables only), recorded
by a NODEBRANCHED event handler; use it only for diagnostic runs, because the
Python callback adds time. --solfile writes the best solution's values of the
original variables (in file order) as JSON.
"""
import json
import math
import os
import re
import sys
import tempfile

import pyscipopt
from pyscipopt import Eventhdlr, SCIP_EVENTTYPE

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
MEMLIMIT_MB = 4000

# Branching-point parameters (SCIP 10 defaults: midpull 0.75,
# midpullreldomtrig 0.5, clamp 0.2). Split point for a continuous variable
# with LP value x on the local domain [l, u], global domain [L, U]:
#   m = midpull * ((u-l)/(U-L) if (u-l)/(U-L) < midpullreldomtrig else 1)
#   p = m*(l+u)/2 + (1-m)*x, then projected onto [l + clamp*(u-l), u - clamp*(u-l)].
SETTINGS = {
    "default": {},
    "lp": {"branching/midpull": 0.0},
    "lp_noclamp": {"branching/midpull": 0.0, "branching/clamp": 0.0},
    "mix_noclamp": {"branching/clamp": 0.0},
    "mid": {"branching/midpull": 1.0, "branching/midpullreldomtrig": 0.0},
    # optional variants
    # Couenne's default point (branch_midpoint_alpha = 0.25 on the LP value, clamp 0.05),
    # without Couenne's increase of alpha at small relative gaps
    "couenne": {"branching/midpull": 0.75, "branching/midpullreldomtrig": 0.0, "branching/clamp": 0.05},
    "lp_c05": {"branching/midpull": 0.0, "branching/clamp": 0.05},
    "trig0": {"branching/midpullreldomtrig": 0.0},
}


def seed_params(seed):
    """Seed 0 is SCIP's default. Seed k > 0 permutes constraints and variables
    with permutation seed k and shifts all random seeds by k."""
    if seed == 0:
        return {}
    return {"randomization/permutationseed": seed, "randomization/permutevars": True,
            "randomization/randomseedshift": seed}


def _i(tok):
    try:
        return int(tok)
    except ValueError:
        return 0


def parse_stats(txt):
    """Branching counts by origin from the SCIP statistics text."""
    out = {}
    sec = None
    for line in txt.splitlines():
        m = re.match(r"^(\S[^:]*?)\s*:", line)
        if m and not line.startswith(" "):
            sec = m.group(1).strip()
            continue
        if ":" not in line:
            continue
        name, rest = line.split(":", 1)
        name = name.strip()
        f = rest.split()
        if sec == "Constraints" and name in ("nonlinear", "integral") and len(f) >= 14:
            # columns: Number MaxNumber #Separate #Propagate #EnfoLP #EnfoRelax #EnfoPS
            #          #Check #ResProp Cutoffs DomReds Cuts Applied Conss Children
            out[f"{name}_enfolp"] = _i(f[4])
            out[f"{name}_enfops"] = _i(f[6])
            out[f"{name}_children"] = _i(f[-1])
        elif sec == "Branching Rules" and len(f) == 10:
            # ExecTime SetupTime BranchLP BranchExt BranchPS Cutoffs DomReds Cuts Conss Children
            lp_, ext, ps, ch = _i(f[2]), _i(f[3]), _i(f[4]), _i(f[9])
            if lp_ + ext + ps > 0:
                out[f"br_{name}"] = [lp_, ext, ps, ch]
        elif sec == "B&B Tree":
            if name == "number of runs":
                out["nruns"] = _i(f[0])
            elif name == "max depth (total)":
                out["max_depth"] = _i(f[0])
        elif sec == "Solution" and name == "Primal Bound":
            m2 = re.search(r"found by <(\w+)>", rest)
            if m2:
                out["best_sol_by"] = m2.group(1)
    return out


class BranchTrace(Eventhdlr):
    """Histogram of relative split positions for continuous branching variables."""

    def __init__(self):
        super().__init__()
        self.n = 0
        self.nint = 0
        self.hist = [0] * 20          # split position (bp-l)/(u-l) in 20 bins
        self.lp_hist = [0] * 20       # LP value position (x-l)/(u-l) in 20 bins
        self.lp_at_bound = 0          # LP value within 1e-6 (relative) of a bound
        self.split_at_clamp = 0       # split within 1e-6 of 0.2 or 0.8
        self.split_degenerate = 0     # split within 1e-6 of a bound
        self.split_degenerate_wide = 0  # ... on a domain wider than 1e-6 * max(1, |l|, |u|)
        self.split_mid = 0            # split within 1e-6 of 0.5
        self.relwidth_small = 0       # local/global width < 0.5 (midpull scaled)
        self.n_infbound = 0           # continuous branchings on a variable with an infinite local bound

    def eventinit(self):
        self.model.catchEvent(SCIP_EVENTTYPE.NODEBRANCHED, self)

    def eventexit(self):
        self.model.dropEvent(SCIP_EVENTTYPE.NODEBRANCHED, self)

    def eventexec(self, event):
        m = self.model
        children = m.getChildren()
        if not children:
            return
        vars_, bounds, _types = children[0].getParentBranchings()
        if not vars_:
            return
        var, bp = vars_[0], bounds[0]
        if var.vtype() != "CONTINUOUS":
            self.nint += 1
            return
        lb, ub = var.getLbLocal(), var.getUbLocal()
        if not (ub - lb > 0 and abs(lb) < 1e19 and abs(ub) < 1e19):
            self.n_infbound += 1
            return
        self.n += 1
        w = ub - lb
        p = (bp - lb) / w
        x = m.getSolVal(None, var)
        t = min(max((x - lb) / w, 0.0), 1.0)
        self.hist[min(int(p * 20), 19)] += 1
        self.lp_hist[min(int(t * 20), 19)] += 1
        if t < 1e-6 or t > 1 - 1e-6:
            self.lp_at_bound += 1
        if abs(p - 0.2) < 1e-6 or abs(p - 0.8) < 1e-6:
            self.split_at_clamp += 1
        if p < 1e-6 or p > 1 - 1e-6:
            self.split_degenerate += 1
            if w > 1e-6 * max(1.0, abs(lb), abs(ub)):
                self.split_degenerate_wide += 1
        if abs(p - 0.5) < 1e-6:
            self.split_mid += 1
        glb, gub = var.getLbGlobal(), var.getUbGlobal()
        if math.isfinite(glb) and math.isfinite(gub) and gub > glb and w / (gub - glb) < 0.5:
            self.relwidth_small += 1

    def summary(self):
        return dict(n=self.n, nint=self.nint, hist=self.hist, lp_hist=self.lp_hist,
                    lp_at_bound=self.lp_at_bound, split_at_clamp=self.split_at_clamp,
                    split_degenerate=self.split_degenerate,
                    split_degenerate_wide=self.split_degenerate_wide, split_mid=self.split_mid,
                    relwidth_small=self.relwidth_small, n_infbound=self.n_infbound)


def fnum(x):
    if x is None or not math.isfinite(x) or abs(x) >= 1e20:
        return None
    return x


def main():
    args = sys.argv[1:]
    trace = "--trace" in args
    solfile = None
    if "--solfile" in args:
        solfile = args[args.index("--solfile") + 1]
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--solfile")]
    inst, setting, seed, tlim = pos[0], pos[1], int(pos[2]), float(pos[3])

    rec = dict(inst=inst, setting=setting, seed=seed, tlim=tlim, traced=trace)
    m = pyscipopt.Model()
    m.hideOutput()
    m.readProblem(os.path.join(OSIL_DIR, inst + ".osil"))
    params = {"limits/time": tlim, "limits/memory": MEMLIMIT_MB, "display/verblevel": 0,
              "timing/clocktype": 1}
    base, _, absgap = setting.partition("@abs")  # "lp@abs0.01": setting lp with limits/absgap 0.01
    params.update(SETTINGS[base])
    if absgap:
        params["limits/absgap"] = float(absgap)
    params.update(seed_params(seed))
    for k, v in params.items():
        m.setParam(k, v)
    tr = None
    if trace:
        tr = BranchTrace()
        m.includeEventhdlr(tr, "brtrace", "branching point trace")
    m.optimize()

    rec.update(status=m.getStatus(), nodes=m.getNTotalNodes(), nodes_lastrun=m.getNNodes(),
               time=round(m.getSolvingTime(), 3), primal=fnum(m.getPrimalbound()),
               dual=fnum(m.getDualbound()), gap=fnum(m.getGap()), lpiter=m.getNLPIterations(),
               nsols=m.getNSols(), sense=m.getObjectiveSense())
    fd, path = tempfile.mkstemp(suffix=".stats")
    os.close(fd)
    try:
        m.writeStatistics(path)
        with open(path) as fh:
            rec.update(parse_stats(fh.read()))
    finally:
        os.unlink(path)
    if tr is not None:
        rec["trace"] = tr.summary()
    if solfile and m.getNSols() > 0:
        sol = m.getBestSol()
        vals = [m.getSolVal(sol, v) for v in m.getVars(transformed=False)]
        with open(solfile, "w") as fh:
            json.dump(dict(inst=inst, names=[v.name for v in m.getVars(transformed=False)], vals=vals), fh)
    sys.stdout.flush()
    print(json.dumps(rec, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
