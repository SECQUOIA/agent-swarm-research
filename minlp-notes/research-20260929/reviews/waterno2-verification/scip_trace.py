"""Trace the SCIP tree nodes whose local box contains the cheaper point x*.
Reports, for such nodes, the focus-time box membership, the node lower bound
after processing, and how the node ends (branched / infeasible / feasible).
A node whose box contains x* but whose lower bound exceeds value(x*), or that
is declared infeasible, shows an invalid local reduction.
usage: python3 scip_trace.py t setting"""
import sys
import pyscipopt as ps
import scip_check as sc
from scip_diag import load_point

t, name = int(sys.argv[1]), sys.argv[2]
cfg = sc.SETTINGS[name]
x = load_point(t)
E = ps.SCIP_EVENTTYPE


class H(ps.Eventhdlr):
    def eventinit(self):
        for ev in (E.NODEFOCUSED, E.NODEBRANCHED, E.NODEINFEASIBLE, E.NODEFEASIBLE):
            self.model.catchEvent(ev, self)
        self.tv = None
        self.log = []

    def contains(self):
        if self.tv is None:
            self.tv = [(self.model.getTransformedVar(var), x[v], sc.m["names"][v]) for v, var in X.items()]
        out = []
        for tv, val, nm in self.tv:
            if not tv.isInLP() and str(tv.vtype()) == "":
                pass
            try:
                lb, ub = tv.getLbLocal(), tv.getUbLocal()
            except Exception:
                continue
            if val < lb - 1e-6 or val > ub + 1e-6:
                out.append((nm, round(val, 9), lb, ub))
        return out

    def eventexec(self, event):
        et = event.getType()
        node = event.getNode()
        ex = self.contains()
        tag = {E.NODEFOCUSED: "focus", E.NODEBRANCHED: "branched", E.NODEINFEASIBLE: "infeasible/cutoff",
               E.NODEFEASIBLE: "feasible"}.get(et, str(et))
        if et == E.NODEFOCUSED:
            self.focus_ok = not ex
            if not ex:
                print(f"node {node.getNumber()} depth {node.getDepth()} FOCUS contains x*; "
                      f"node lb {node.getLowerbound():.6f} cutoff {self.model.getCutoffbound():.6f}", flush=True)
        elif getattr(self, "focus_ok", False):
            print(f"   node {node.getNumber()} {tag}: lb {node.getLowerbound():.6f} "
                  f"x* still inside: {not ex} {ex[:6]}", flush=True)
            if ex:
                # bound changes stored at this node that exclude x*
                xt = {}
                for tv, val, nm in self.tv:
                    xt[tv.name] = (val, nm)
                dc = node.getDomchg()
                chg = dc.getBoundchgs() if dc is not None else []
                for bc in chg:
                    v = bc.getVar()
                    if v.name in xt:
                        val, nm = xt[v.name]
                        nb = bc.getNewBound()
                        lower = bc.getBoundtype() == 0
                        cut = (val < nb - 1e-6) if lower else (val > nb + 1e-6)
                        print(f"      stored bound change {nm} {'>=' if lower else '<='} {nb!r} "
                              f"type {bc.getBoundchgtype()} excludes x* ({val}): {cut}", flush=True)
            self.focus_ok = False


M, X, obj = sc.build(t, dict(cfg.get("params", {}), **{"limits/time": 300}), cfg.get("emphasis"),
                     cfg.get("presolve_off", False), cfg.get("heur_off", False))
vstar = float(sum(a * sc.F(x[v]) for v, a in obj.items()))
print("value of x*:", vstar)
h = H()
M.includeEventhdlr(h, "trace", "trace x*")
M.optimize()
print("status", M.getStatus(), "dual", M.getDualbound(), "primal", M.getPrimalbound())
bs = M.getBestSol()
off = M.getSolObjVal(bs) - M.getSolObjVal(bs, original=False)
print(f"incumbent original {M.getSolObjVal(bs):.6f} transformed {M.getSolObjVal(bs, original=False):.6f} -> offset {off:.6f}; "
      f"x* transformed value = {vstar - off:.6f}")
