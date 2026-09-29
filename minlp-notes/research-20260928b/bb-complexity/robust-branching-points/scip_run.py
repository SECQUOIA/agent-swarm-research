"""One SCIP run with a branching-point rule.

    python3 scip_run.py INSTANCE SETTING SEED TIMELIMIT [--eps EPS]

INSTANCE is a MINLPLib name (OSiL file) or a synthetic kink instance:
  k1:A     min t s.t. 2|x - A| - (x - A)^2 <= t, x in [0,1]         (1D exact-gap kink, alpha = 1)
  mc:A     min t s.t. 2|x - A| - (x - A)(y - B) <= t, [0,1]^2, B = sqrt(2) - 1   (McCormick kink)
Synthetic instances run in the theory's model (best-first order, propagation and heuristics off,
the optimum x = A, t = 0 given as incumbent, limits/absgap = EPS, feastol 1e-9).

SETTING (see SETTINGS): two arms.
  Arm P (parameter only; SCIP's own variable selection): the branching-point parameters are set
  once, and for 'r' settings branching/clamp is redrawn uniformly from [0.1, 0.3] when each node
  is focused, so every SCIPgetBranchingPoint call at that node (pseudocost scoring and the split)
  uses the same random clamp.
  Arm X (plugin): constraints/nonlinear/branching/external = TRUE and a branching rule with
  branchexecext that re-implements cons_nonlinear's variable selection on the external
  candidates (scoreBranchingCandidates/selectBranchingCandidate in cons_nonlinear.c of SCIP
  10.0.3: weighted violation, fractionality, pseudocost and variable-type scores, uniform
  random choice among candidates within 0.9 of the best weighted score; the pseudocost score is
  evaluated at the rule's own point, as SCIP does with its point). Only the point rule differs
  between X settings. Integer candidates always use SCIPgetBranchingPoint.

Prints one JSON line (the last line of stdout).
"""
import ctypes
import glob
import json
import math
import os
import random
import sys
import tempfile

import pyscipopt
from pyscipopt import Branchrule, Eventhdlr, SCIP_EVENTTYPE, SCIP_PARAMSETTING, SCIP_RESULT

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "minlplib-branching"))
from run_one import OSIL_DIR, MEMLIMIT_MB, parse_stats, seed_params, fnum  # noqa: E402

# ---------------------------------------------------------------- C access
_LIB = ctypes.CDLL(glob.glob(os.path.join(os.path.dirname(pyscipopt.__file__), "..",
                                          "pyscipopt.libs", "libscip-*.so*"))[0])
_P, _D, _I, _B = ctypes.c_void_p, ctypes.c_double, ctypes.c_int, ctypes.c_uint


def _fn(name, res, *args):
    f = getattr(_LIB, name)
    f.restype = res
    f.argtypes = list(args)
    return f


C_getExternCands = _fn("SCIPgetExternBranchCands", _I, _P, ctypes.POINTER(ctypes.POINTER(_P)),
                       ctypes.POINTER(ctypes.POINTER(_D)), ctypes.POINTER(ctypes.POINTER(_D)),
                       ctypes.POINTER(_I), ctypes.POINTER(_I), ctypes.POINTER(_I), ctypes.POINTER(_I),
                       ctypes.POINTER(_I))
C_getBranchingPoint = _fn("SCIPgetBranchingPoint", _D, _P, _P, _D)
C_branchVarVal = _fn("SCIPbranchVarVal", _I, _P, _P, _D, _P, _P, _P)
C_lbLocal = _fn("SCIPvarGetLbLocal", _D, _P)
C_ubLocal = _fn("SCIPvarGetUbLocal", _D, _P)
C_isIntegral = _fn("SCIPvarIsIntegral", _B, _P)
C_varIndex = _fn("SCIPvarGetIndex", _I, _P)
C_getVarSol = _fn("SCIPgetVarSol", _D, _P, _P)
C_hasNodeLP = _fn("SCIPhasCurrentNodeLP", _B, _P)
C_getBestSol = _fn("SCIPgetBestSol", _P, _P)
C_getSolVal = _fn("SCIPgetSolVal", _D, _P, _P, _P)
C_infinity = _fn("SCIPinfinity", _D, _P)
C_nVars = _fn("SCIPgetNVars", _I, _P)
C_vars = _fn("SCIPgetVars", ctypes.POINTER(_P), _P)
C_setReal = _fn("SCIPsetRealParam", _I, _P, ctypes.c_char_p, _D)
C_varType = _fn("SCIPvarGetType", _I, _P)
C_isImplInt = _fn("SCIPvarIsImpliedIntegral", _B, _P)
C_pscostCount = _fn("SCIPgetVarPseudocostCountCurrentRun", _D, _P, _P, _I)
C_pscostVal = _fn("SCIPgetVarPseudocostVal", _D, _P, _P, _D)
C_branchScore = _fn("SCIPgetBranchScore", _D, _P, _P, _D, _D)
C_adjLb = _fn("SCIPadjustedVarLb", _D, _P, _P, _D)
C_adjUb = _fn("SCIPadjustedVarUb", _D, _P, _P, _D)
C_nObjVars = _fn("SCIPgetNObjVars", _I, _P)
C_nLPBranchCands = _fn("SCIPgetNLPBranchCands", _I, _P)
SCIP_INVALID = 1e99


def scip_ptr(model):
    cap = model.to_ptr(False)
    get = ctypes.pythonapi.PyCapsule_GetPointer
    get.restype = ctypes.c_void_p
    get.argtypes = [ctypes.py_object, ctypes.c_char_p]
    return get(cap, b"scip")


# ---------------------------------------------------------------- settings
RCLAMP = (0.1, 0.3)
# name -> (SCIP parameters, point rule for the plugin or None, redraw clamp per node)
SETTINGS = {
    # Arm P: SCIP's own selection and point formula
    "default": ({}, None, False),
    "rclamp": ({}, None, True),
    "lp": ({"branching/midpull": 0.0}, None, False),
    "lp_rclamp": ({"branching/midpull": 0.0}, None, True),
    "c10": ({"branching/clamp": 0.1}, None, False),       # control: fixed clamp at the lower end
    # Arm X: plugin selection (max violation score), point rule varies
    "x_default": ({}, "scip", False),
    "x_rclamp": ({}, "scip", True),          # SCIP's pulled point, random clamp
    "x_lp": ({"branching/midpull": 0.0}, "scip", False),
    "x_lp_rclamp": ({"branching/midpull": 0.0}, "scip", True),
    "x_recenter": ({"branching/midpull": 0.0}, "recenter", False),
    "x_inc": ({"branching/midpull": 0.0}, "inc", False),
    "x_noclamp": ({"branching/midpull": 0.0, "branching/clamp": 0.0}, "scip", False),
}
EXTERNAL = {"constraints/nonlinear/branching/external": True}

# theory model for the synthetic instances (as in ../solver-validation/run_one.py, setting 'modelnoprop')
MODEL = {"nodeselection/bfs/stdpriority": 1000000, "nodeselection/bfs/maxplungedepth": 0,
         "nodeselection/bfs/minplungedepth": 0, "limits/gap": 0.0, "numerics/feastol": 1e-9,
         "numerics/epsilon": 1e-12, "numerics/sumepsilon": 1e-10, "numerics/dualfeastol": 1e-9,
         "constraints/nonlinear/checkvarlocks": "d", "limits/nodes": 2_000_000,
         "misc/allowweakdualreds": False}
MODEL.update({"propagating/%s/freq" % p: -1 for p in
              ["dualfix", "genvbounds", "nlobbt", "obbt", "probing", "pseudoobj", "redcost",
               "rootredcost", "symmetry", "vbounds"]})
MODEL.update({"constraints/nonlinear/propfreq": -1, "constraints/linear/propfreq": -1,
              "constraints/varbound/propfreq": -1})
BSTAR = math.sqrt(2.0) - 1.0


def synthetic_cip(name):
    kind, a = name.split(":")
    a = float(a)
    if kind == "k1":
        xs = {"x": (0.0, 1.0)}
        expr = f"2*abs(<x> - ({a:.17g})) - (<x> - ({a:.17g}))^2"
    elif kind == "mc":
        xs = {"x": (0.0, 1.0), "y": (0.0, 1.0)}
        expr = f"2*abs(<x> - ({a:.17g})) - (<x> - ({a:.17g}))*(<y> - ({BSTAR:.17g}))"
    else:
        raise ValueError(name)
    lines = ["STATISTICS", f"  Problem name     : {name}",
             f"  Variables        : {len(xs) + 1} (0 binary, 0 integer, 0 implicit integer, {len(xs) + 1} continuous)",
             "  Constraints      : 1 initial, 1 maximal", "OBJECTIVE", "  Sense            : minimize",
             "VARIABLES"]
    for v, (lb, ub) in xs.items():
        lines.append(f"  [continuous] <{v}>: obj=0, original bounds=[{lb:.17g},{ub:.17g}]")
    lines += ["  [continuous] <t>: obj=1, original bounds=[-1000,1000]", "CONSTRAINTS",
              f"  [nonlinear] <fobj>: {expr} - <t> <= 0;", "END"]
    opt = {"x": a, "y": 0.5, "t": 1e-15}
    return "\n".join(lines) + "\n", {v: opt[v] for v in list(xs) + ["t"]}


# ---------------------------------------------------------------- plugins
class ClampRedraw(Eventhdlr):
    """Redraw branching/clamp uniformly from RCLAMP whenever a node is focused."""

    def __init__(self, ptr, rng):
        super().__init__()
        self.ptr, self.rng, self.n = ptr, rng, 0

    def eventinit(self):
        self.model.catchEvent(SCIP_EVENTTYPE.NODEFOCUSED, self)

    def eventexit(self):
        self.model.dropEvent(SCIP_EVENTTYPE.NODEFOCUSED, self)

    def eventexec(self, event):
        self.n += 1
        assert C_setReal(self.ptr, b"branching/clamp", self.rng.uniform(*RCLAMP)) == 1


class PointRule(Branchrule):
    """cons_nonlinear's variable selection on the external candidates, with a rule-specific point."""

    def __init__(self, ptr, rule, clamp, rng):
        super().__init__()
        self.ptr, self.rule, self.clamp, self.rng = ptr, rule, clamp, rng
        self.cnt = dict(ext=0, cont=0, int=0, nolp=0, lp_at_bound=0, clamped=0, recentred=0, inc=0,
                        small_child=0)

    def branchexeclp(self, allowaddcons):  # integer (LP) branching stays with SCIP's rules
        return {"result": SCIP_RESULT.DIDNOTRUN}

    def branchexecps(self, allowaddcons):
        return {"result": SCIP_RESULT.DIDNOTRUN}

    @staticmethod
    def _guess_bounds(lb, ub, inf):
        # SCIP's guess of a missing bound (branch.c, SCIPbranchGetBranchingPoint)
        if ub >= inf:
            ub = lb + min(max(0.5 * abs(lb), 1000.0), 0.9 * (inf - lb))
        elif lb <= -inf:
            lb = ub - min(max(0.5 * abs(ub), 1000.0), 0.9 * (inf + ub))
        return lb, ub

    def _incumbent_inside(self, var, lb, ub):
        sol = C_getBestSol(self.ptr)
        if not sol:
            return None
        xv = C_getSolVal(self.ptr, sol, var)
        w = ub - lb
        if not (lb + 1e-6 * w < xv < ub - 1e-6 * w):
            return None
        if self._incbox is None:  # the incumbent point must lie in the node box (once per node)
            n, vs = C_nVars(self.ptr), C_vars(self.ptr)
            self._incbox = True
            for i in range(n):
                v = vs[i]
                s = C_getSolVal(self.ptr, sol, v)
                if s < C_lbLocal(v) - 1e-9 or s > C_ubLocal(v) + 1e-9:
                    self._incbox = False
                    break
        return xv if self._incbox else None

    def _point(self, var):
        """Branching point of the rule; returns (point, kind)."""
        ptr = self.ptr
        if C_isIntegral(var) or self.rule == "scip":
            return C_getBranchingPoint(ptr, var, SCIP_INVALID), "scip"
        lb, ub = C_lbLocal(var), C_ubLocal(var)
        glb, gub = self._guess_bounds(lb, ub, C_infinity(ptr))
        w, th = gub - glb, 0.2
        x = min(max(C_getVarSol(ptr, var), glb), gub)
        if self.rule == "inc":
            s = self._incumbent_inside(var, lb, ub)
            if s is not None:
                return C_getBranchingPoint(ptr, var, s), "inc"
        kind = "lp"
        if x < glb + th * w:
            s = glb + th * w
            if self.rule == "recenter" and 2 * (x - glb) > th * w:
                s, kind = glb + 2 * (x - glb), "recentred"
        elif x > gub - th * w:
            s = gub - th * w
            if self.rule == "recenter" and 2 * (gub - x) > th * w:
                s, kind = gub - 2 * (gub - x), "recentred"
        else:
            s = x
        return C_getBranchingPoint(ptr, var, s), kind

    def _pscost(self, var, brpoint):
        """cons_nonlinear's pseudocost score (scoreBranchingCandidates), or None if unavailable."""
        ptr = self.ptr
        lb, ub = C_lbLocal(var), C_ubLocal(var)
        inf = C_infinity(ptr)
        if lb <= -inf or ub >= inf:
            return None
        integral = C_isIntegral(var)
        down = up = None
        if C_pscostCount(ptr, var, 0) >= 2.0:
            if not integral:   # strategy 's' (branching/lpgainnormalize)
                down = C_pscostVal(ptr, var, -(ub - C_adjLb(ptr, var, brpoint)))
            else:              # strategy 'l'
                x = C_getSolVal(ptr, None, var)
                ab = C_adjUb(ptr, var, brpoint)
                down = C_pscostVal(ptr, var, 0.0 if x <= ab else -(x - ab))
        if C_pscostCount(ptr, var, 1) >= 2.0:
            if not integral:
                up = C_pscostVal(ptr, var, C_adjUb(ptr, var, brpoint) - lb)
            else:
                x = C_getSolVal(ptr, None, var)
                ab = C_adjLb(ptr, var, brpoint)
                up = C_pscostVal(ptr, var, 0.0 if x >= ab else ab - x)
        if down is None and up is None:
            return None
        if down is None:
            return up
        if up is None:
            return down
        return C_branchScore(ptr, None, down, up)

    def branchexecext(self, allowaddcons):
        ptr = self.ptr
        cands, sols, scores = ctypes.POINTER(_P)(), ctypes.POINTER(_D)(), ctypes.POINTER(_D)()
        n, a1, a2, a3, a4 = _I(), _I(), _I(), _I(), _I()
        C_getExternCands(ptr, ctypes.byref(cands), ctypes.byref(sols), ctypes.byref(scores),
                         ctypes.byref(n), ctypes.byref(a1), ctypes.byref(a2), ctypes.byref(a3),
                         ctypes.byref(a4))
        if n.value == 0:
            return {"result": SCIP_RESULT.DIDNOTRUN}
        self._incbox = None
        if self.clamp:
            assert C_setReal(ptr, b"branching/clamp", self.clamp.uniform(*RCLAMP)) == 1
        # ---- candidate scores (weights: viol 1, frac 1, pscost 1, vartype 0.5; domain, dual 0)
        C = []
        usefrac = C_nLPBranchCands(ptr) > 0
        usepscost = C_nObjVars(ptr) > 0
        for i in range(n.value):
            v = cands[i]
            pt, kind = self._point(v)
            integral = bool(C_isIntegral(v))
            frac = 0.0
            if usefrac and integral:
                x = C_getSolVal(ptr, None, v)
                frac = abs(x - round(x))
            t = C_varType(v)
            vt = 1.0 if t == 0 else 0.1 if t == 1 else (0.01 if C_isImplInt(v) else 0.0)
            ps = self._pscost(v, pt) if usepscost else None
            C.append(dict(var=v, viol=scores[i], frac=frac, vt=vt, ps=ps, pt=pt, kind=kind,
                          idx=C_varIndex(v)))
        if len(C) == 1:
            sel = C[0]
        else:
            mx = {k: max((c[k] for c in C if c[k] is not None), default=0.0)
                  for k in ("viol", "frac", "vt", "ps")}
            for c in C:
                s = ws = 0.0
                for k, wgt in (("viol", 1.0), ("frac", 1.0), ("vt", 0.5)):
                    if mx[k] > 0:
                        s += wgt * c[k] / mx[k]
                        ws += wgt
                if mx["ps"] > 0 and c["ps"] is not None:
                    s += c["ps"] / mx["ps"]
                    ws += 1.0
                c["w"] = s / ws if ws > 0 else 0.0
            C.sort(key=lambda c: (c["w"], c["idx"]), reverse=True)
            thr = 0.9 * C[0]["w"]
            top = [c for c in C if c["w"] >= thr]
            sel = top[self.rng.randrange(len(top))] if len(top) > 1 else top[0]
        var, val = sel["var"], sel["pt"]
        self.cnt["ext"] += 1
        if not C_hasNodeLP(ptr):
            self.cnt["nolp"] += 1
        if C_isIntegral(var):
            self.cnt["int"] += 1
        else:
            self.cnt["cont"] += 1
            if sel["kind"] in ("inc", "recentred"):
                self.cnt[sel["kind"]] += 1
            lb, ub = C_lbLocal(var), C_ubLocal(var)
            if ub - lb > 0 and ub < 1e19 and lb > -1e19:
                x = C_getVarSol(ptr, var)
                w = ub - lb
                if min(x - lb, ub - x) <= 1e-6 * w:
                    self.cnt["lp_at_bound"] += 1
                if abs(val - x) > 1e-9 * max(1.0, abs(x)):
                    self.cnt["clamped"] += 1
                if min(val - lb, ub - val) < 0.01 * w:
                    self.cnt["small_child"] += 1
        C_branchVarVal(ptr, var, val, None, None, None)
        return {"result": SCIP_RESULT.BRANCHED}


# ---------------------------------------------------------------- run
def main():
    args = sys.argv[1:]
    eps = None
    if "--eps" in args:
        eps = float(args[args.index("--eps") + 1])
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--eps")]
    inst, setting, seed, tlim = pos[0], pos[1], int(pos[2]), float(pos[3])
    params, rule, redraw = SETTINGS[setting]
    synthetic = ":" in inst
    rec = dict(inst=inst, setting=setting, seed=seed, tlim=tlim, eps=eps)

    m = pyscipopt.Model()
    m.hideOutput()
    tmp = None
    if synthetic:
        cip, opt = synthetic_cip(inst)
        fd, tmp = tempfile.mkstemp(suffix=".cip")
        with os.fdopen(fd, "w") as fh:
            fh.write(cip)
        m.readProblem(tmp)
    else:
        m.readProblem(os.path.join(OSIL_DIR, inst + ".osil"))
    allp = {"limits/time": tlim, "limits/memory": MEMLIMIT_MB, "display/verblevel": 0,
            "timing/clocktype": 1}
    if synthetic:
        allp.update(MODEL)
        allp["limits/absgap"] = eps
    allp.update(params)
    if rule is not None:
        allp.update(EXTERNAL)
    allp.update(seed_params(seed))
    for k, v in allp.items():
        m.setParam(k, v)
    ptr = scip_ptr(m)
    rng = random.Random(1_000_003 * seed + 12_345)
    ev = br = None
    if rule is not None:
        br = PointRule(ptr, rule, rng if redraw else None, random.Random(7_919 * seed + 1))
        m.includeBranchrule(br, "pointrule", "point-rule plugin", priority=1_000_000, maxdepth=-1,
                            maxbounddist=1.0)
    elif redraw:
        ev = ClampRedraw(ptr, rng)
        m.includeEventhdlr(ev, "clampredraw", "redraw branching/clamp per node")
    if synthetic:
        m.setHeuristics(SCIP_PARAMSETTING.OFF)
        vs = {v.name: v for v in m.getVars()}
        sol = m.createSol()
        for k, v in opt.items():
            m.setSolVal(sol, vs[k], v)
        rec["knownopt_accepted"] = m.addSol(sol, free=True)
    m.optimize()
    rec.update(status=m.getStatus(), nodes=m.getNTotalNodes(), nodes_lastrun=m.getNNodes(),
               time=round(m.getSolvingTime(), 3), primal=fnum(m.getPrimalbound()),
               dual=fnum(m.getDualbound()), gap=fnum(m.getGap()), lpiter=m.getNLPIterations(),
               nsols=m.getNSols())
    fd, path = tempfile.mkstemp(suffix=".stats")
    os.close(fd)
    try:
        m.writeStatistics(path)
        with open(path) as fh:
            rec.update(parse_stats(fh.read()))
    finally:
        os.unlink(path)
        if tmp:
            os.unlink(tmp)
    if br is not None:
        rec["plugin"] = br.cnt
    if ev is not None:
        rec["redraws"] = ev.n
    rec["versions"] = dict(scip=m.version(), pyscipopt=pyscipopt.__version__)
    print(json.dumps(rec, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
