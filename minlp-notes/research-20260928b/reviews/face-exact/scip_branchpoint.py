"""Reviewer check: where does SCIP (via PySCIPOpt) actually branch on the scout's kink instance?

Instance: min 2|x-a| - (x-a)(y-b) on [0,1]^2, a = 1/3, b = sqrt(2)-1 (optimal set {a} x [0,1], f* = 0).
Model: z >= 2 t - x*y + b x + a y - a b,  t >= x-a, t >= a-x;  minimise z.

We record the domains of x and y at every focused node (event NODEFOCUSED).  The first children of the
root reveal SCIP's branching point.  With SCIP's default parameters branching/midpull = 0.75,
branching/midpullreldomtrig = 0.5, branching/clamp = 0.2, a pure relaxation-point rule (alpha = 1)
would split x at xhat = a = 1/3; the midpull rule would split at 0.75*0.5 + 0.25*xhat.

Run 1: SCIP defaults except presolve off (keeps the root domain [0,1]).
Run 2: additionally branching/midpull = 0 (pure LP point, clamped at 0.2).
"""
import math
import sys
import pyscipopt as ps

A = 1.0 / 3.0
B = math.sqrt(2.0) - 1.0


class Rec(ps.Eventhdlr):
    def __init__(self, x, y):
        self.x, self.y, self.rows = x, y, []

    def eventinit(self):
        self.model.catchEvent(ps.SCIP_EVENTTYPE.NODEFOCUSED, self)

    def eventexit(self):
        self.model.dropEvent(ps.SCIP_EVENTTYPE.NODEFOCUSED, self)

    def eventexec(self, event):
        node = self.model.getCurrentNode()
        par = node.getParent()
        self.rows.append((node.getNumber(), par.getNumber() if par is not None else 0, node.getDepth(),
                          self.x.getLbLocal(), self.x.getUbLocal(), self.y.getLbLocal(), self.y.getUbLocal()))


def run(extra, eps_abs=1e-4, label=""):
    m = ps.Model()
    m.hideOutput()
    x = m.addVar("x", lb=0, ub=1)
    y = m.addVar("y", lb=0, ub=1)
    t = m.addVar("t", lb=0, ub=1)
    z = m.addVar("z", lb=-10, ub=10)
    m.addCons(t >= x - A)
    m.addCons(t >= A - x)
    m.addCons(z >= 2 * t - x * y + B * x + A * y - A * B)
    m.setObjective(z, "minimize")
    m.setPresolve(ps.SCIP_PARAMSETTING.OFF)
    m.setParam("limits/absgap", eps_abs)
    m.setParam("limits/gap", 0.0)
    m.setParam("limits/nodes", 400)
    for k, v in extra.items():
        m.setParam(k, v)
    rec = Rec(x, y)
    m.includeEventhdlr(rec, "rec", "record node domains")
    m.optimize()
    print(f"== {label}: status={m.getStatus()} nodes={m.getNNodes()} obj={m.getObjVal():.3e} "
          f"dual={m.getDualbound():.3e}")
    print("   first 12 focused nodes (num, parent, depth, x-domain, y-domain):")
    for r in rec.rows[:12]:
        print(f"   {r[0]:4d} {r[1]:4d} d={r[2]:2d}  x=[{r[3]:.6f},{r[4]:.6f}]  y=[{r[5]:.6f},{r[6]:.6f}]")
    xs = sorted({round(v, 9) for r in rec.rows for v in (r[3], r[4])})
    print("   distinct x-bounds seen (first 12):", xs[:12])
    return m.getNNodes()


def main():
    print("PySCIPOpt", ps.__version__)
    m0 = ps.Model()
    print("SCIP defaults: branching/midpull =", m0.getParam("branching/midpull"),
          " midpullreldomtrig =", m0.getParam("branching/midpullreldomtrig"),
          " clamp =", m0.getParam("branching/clamp"))
    print("prediction for the first x split with defaults: 0.75*0.5 + 0.25*(1/3) =", 0.75 * 0.5 + 0.25 / 3)
    for eps in (1e-3, 1e-4, 1e-5):
        n1 = run({}, eps, f"defaults (presolve off), abs gap {eps:g}")
        n2 = run({"branching/midpull": 0.0}, eps, f"midpull=0 (alpha=1, clamp .2), abs gap {eps:g}")


def small_gaps():
    """Second part: smaller absolute gaps (SCIP's feasibility tolerance is 1e-6, so read with care)."""
    for eps in (1e-6, 1e-7):
        run({}, eps, f"defaults (presolve off), abs gap {eps:g}")
        run({"branching/midpull": 0.0}, eps, f"midpull=0, abs gap {eps:g}")
        run({"propagating/maxrounds": 0, "propagating/maxroundsroot": 0, "separating/maxrounds": 0,
             "separating/maxroundsroot": 0}, eps, f"defaults, propagation+separation off, abs gap {eps:g}")


if __name__ == "__main__":
    main()
    small_gaps()
