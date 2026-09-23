"""Gurobi 13 on a MINLPLib instance: original model, or curve-hull strengthened model.

python run.py <instance> <mode> [--tl 1800] [--threads 1] [--pbounds] [--kmin 2] [--root-only]
modes
  orig  the OSiL model as read (model.build mode "orig")
  sub   univariate atoms of selected variables replaced by auxiliary variables, no cuts (control)
  (orig and sub first run the root only (NodeLimit 1) to record the root bound, then a fresh full run)
  cuts  phase 1: the "sub" model is solved at the root only (NodeLimit 1) with a MIPNODE callback that
        separates Gurobi's root relaxation point from the hull of each selected curve and adds the cut
        (cbCut); phase 2: fresh "sub" model + all phase-1 cuts as static linear constraints, full run with time limit tl minus the phase-1 time.
  dyn   as cuts, and phase 2 keeps separating (globally valid cuts) at every node.
  soc   "sub" model plus the exact hull of (x, x^2, x^3) on [l, u] as two rotated second-order cones for
        every selected variable with both x^2 and x^3 atoms (no cuts); reference for the cut approach.
--pbounds  use variable bounds from Gurobi presolve with DualReductions=0 (primal reductions only)
           for the curve intervals, where they are tighter than the model bounds.
Prints one JSON line; phase-1 cuts are saved in cuts/<instance>[_pb]_<mode>_s<seed>.json.  Each cut records
the auxiliary variables it acts on: t_j = funcs[j](x) and the model term keys[j](x) = factors[j] * t_j.
"""
import argparse
import json
import math
import os
import time

import numpy as np
import sympy as sp
import gurobipy as gp
from gurobipy import GRB

import model

HERE = os.path.dirname(os.path.abspath(__file__))


def presolve_bounds(name):
    B = model.build(name, "orig")
    B.m.Params.DualReductions = 0
    p = B.m.presolve()
    pb = {v.VarName: (v.LB, v.UB) for v in p.getVars()}
    lb, ub = list(B.inst.var_lb), list(B.inst.var_ub)
    for j in range(len(lb)):
        if f"x{j}" in pb:
            lb[j] = max(lb[j], pb[f"x{j}"][0])
            ub[j] = min(ub[j], pb[f"x{j}"][1])
    return lb, ub


class Separator:
    def __init__(self, B, min_viol=1e-5):
        self.B, self.min_viol = B, min_viol
        self.items = []  # (v, curve, [x var, aux vars...], numeric functions)
        for v, keep in B.det.sel.items():
            C = B.det.curves[v]
            vs = [B.x[v]] + [B.aux[(v, sk)][0] for sk, _, _ in keep]
            self.items.append((v, C, vs))
        self.allvars = [w for _, _, vs in self.items for w in vs]
        self.cuts = []
        self.sep_time = 0.0
        self.calls = 0

    def separate(self, vals):
        """vals: values of self.allvars.  Returns list of (v, cut)."""
        t0 = time.time()
        out, i = [], 0
        for v, C, vs in self.items:
            p = np.array(vals[i:i + len(vs)])
            i += len(vs)
            p[0] = min(max(p[0], C.l), C.u)
            # a point on the curve is in the hull: skip cheaply
            f = C.phi(p[0])[:, 0]
            if np.all(np.abs(f[1:] - p[1:]) <= 1e-7 * C.wid[1:]):
                continue
            cut = C.separate(p, min_viol=self.min_viol)
            if cut is not None:
                out.append((v, cut, vs))
        self.sep_time += time.time() - t0
        self.calls += 1
        return out

    def callback(self, root_only):
        def cb(m, where):
            if where != GRB.Callback.MIPNODE or m.cbGet(GRB.Callback.MIPNODE_STATUS) != GRB.OPTIMAL:
                return
            if root_only and m.cbGet(GRB.Callback.MIPNODE_NODCNT) > 0:
                return
            if root_only and self.calls >= 60:
                return
            vals = m.cbGetNodeRel(self.allvars)
            for v, cut, vs in self.separate(vals):
                m.cbCut(gp.LinExpr(list(cut["c"]), vs) >= -cut["c0"])
                self.cuts.append((v, cut))
        return cb


def add_static(B, cuts):
    for v, cut in cuts:
        keep = B.det.sel[v]
        vs = [B.x[v]] + [B.aux[(v, sk)][0] for sk, _, _ in keep]
        B.m.addLConstr(gp.LinExpr(list(cut["c"]), vs), GRB.GREATER_EQUAL, -cut["c0"])


def add_moment_cones(B):
    """(x-l)(z-l y) >= (y-l x)^2, (u-x)(u y-z) >= (u x-y)^2 with nonnegative factors, y = x^2, z = x^3."""
    m, n = B.m, 0
    for v, keep in B.det.sel.items():
        d = {sk: B.aux[(v, sk)] for sk, _, _ in keep}
        k2, k3 = model.sp.srepr(model.T**2), model.sp.srepr(model.T**3)
        if k2 not in d or k3 not in d:
            continue
        (t2, f2), (t3, f3) = d[k2], d[k3]
        x, C = B.x[v], B.det.curves[v]
        l, u = C.l, C.u
        y, z = f2 * t2, f3 * t3
        for a, b, c in [(x - l, z - l * y, y - l * x), (u - x, u * y - z, u * x - y)]:
            av, bv, cv = m.addVar(lb=0), m.addVar(lb=0), m.addVar(lb=-GRB.INFINITY)
            m.addConstr(av == a); m.addConstr(bv == b); m.addConstr(cv == c)
            m.addQConstr(cv * cv <= av * bv)
        n += 1
    return n


def result(B, t0):
    m = B.m
    if m.SolCount:  # incumbent in the original variables, checked in the original model
        import check_point
        xs = [v.X for v in B.x]
        B.incumbent = xs
        chk = check_point.check(B.inst, xs)
    else:
        chk = None
    return {"incumbent_check": chk,"status": m.Status, "primal": m.ObjVal if m.SolCount else None, "dual": m.ObjBound,
            "nodes": m.NodeCount, "time": time.time() - t0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("mode", choices=["orig", "sub", "cuts", "dyn", "soc"])
    ap.add_argument("--tl", type=float, default=1800)
    ap.add_argument("--root-tl", type=float, default=300)
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--kmin", type=int, default=2)
    ap.add_argument("--pbounds", action="store_true")
    ap.add_argument("--root-only", action="store_true", help="stop after phase 1")
    ap.add_argument("--seed", type=int, default=0, help="Gurobi Seed (performance variability checks)")
    a = ap.parse_args()
    out = {"name": a.name, "mode": a.mode, "tl": a.tl, "threads": a.threads, "pbounds": a.pbounds, "seed": a.seed}
    inst = model.read_osil(model.OSIL.format(a.name))
    out["sense"] = inst.obj_sense
    det = None
    if a.mode != "orig":
        if a.pbounds:
            inst.var_lb, inst.var_ub = presolve_bounds(a.name)
        det = model.Detected(inst, kmin=a.kmin)
        out["nsel"] = len(det.sel)
        out["curves"] = model.summary(det)

    def fresh():
        B = model.build(a.name, "orig" if a.mode == "orig" else "sub", threads=a.threads, det=det)
        B.m.Params.Seed = a.seed
        return B

    if a.mode in ("orig", "sub", "soc"):
        B = fresh()  # root bound first (NodeLimit 1), for comparison with phase 1 of "cuts"
        if a.mode == "soc":
            out["cones"] = add_moment_cones(B)
        B.m.Params.NodeLimit = 1
        B.m.Params.TimeLimit = a.root_tl
        t0 = time.time()
        B.m.optimize()
        out["root"] = {"dual": B.m.ObjBound, "primal": B.m.ObjVal if B.m.SolCount else None, "time": time.time() - t0}
        B = fresh()
        if a.mode == "soc":
            add_moment_cones(B)
        B.m.Params.TimeLimit = a.tl
        t0 = time.time()
        B.m.optimize()
        out.update(result(B, t0))
        save_point(a, B)
        print(json.dumps(out), flush=True)
        return
    # phase 1: root separation
    B = fresh()
    S = Separator(B)
    B.m.Params.PreCrush = 1
    B.m.Params.NodeLimit = 1
    B.m.Params.TimeLimit = a.root_tl
    t0 = time.time()
    B.m.optimize(S.callback(root_only=True))
    out["root"] = {"dual": B.m.ObjBound, "primal": B.m.ObjVal if B.m.SolCount else None, "time": time.time() - t0,
                   "sep_calls": S.calls, "sep_time": S.sep_time}
    cuts = S.cuts
    out["ncuts"] = len(cuts)
    out["cuts_per_var"] = len({v for v, _ in cuts})
    os.makedirs(os.path.join(HERE, "cuts"), exist_ok=True)
    with open(os.path.join(HERE, "cuts", f"{a.name}{'_pb' if a.pbounds else ''}_{a.mode}_s{a.seed}.json"), "w") as f:
        json.dump([{"v": v, "funcs": [str(sc.g) for _, _, sc in det.sel[v]], "keys": [str(key) for _, key, _ in det.sel[v]],
                    "factors": [sc.factor for _, _, sc in det.sel[v]], "l": det.curves[v].l, "u": det.curves[v].u,
                    "c0": c["c0"], "c": list(c["c"]), "viol_scaled": c["viol_scaled"]} for v, c in cuts], f)
    if a.root_only:
        print(json.dumps(out), flush=True)
        return
    # phase 2
    B = fresh()
    add_static(B, cuts)
    B.m.Params.TimeLimit = max(a.tl - out["root"]["time"], 1.0)  # phase 1 time counts against the limit
    t0 = time.time()
    if a.mode == "dyn":
        S2 = Separator(B)
        B.m.Params.PreCrush = 1
        B.m.optimize(S2.callback(root_only=False))
        out["tree_cuts"] = len(S2.cuts)
        out["tree_sep_time"] = S2.sep_time
    else:
        B.m.optimize()
    out.update(result(B, t0))
    save_point(a, B)
    print(json.dumps(out), flush=True)


def save_point(a, B):
    if getattr(B, "incumbent", None) is not None:
        os.makedirs(os.path.join(HERE, "points"), exist_ok=True)
        tag = f"{a.name}_{a.mode}{'_pb' if a.pbounds else ''}_s{a.seed}_{int(a.tl)}"
        json.dump(B.incumbent, open(os.path.join(HERE, "points", tag + ".json"), "w"))


if __name__ == "__main__":
    main()
