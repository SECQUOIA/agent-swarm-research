from pyscipopt import Model
import sys
def run(params, label):
    m = Model(); m.hideOutput(True)
    x = m.addVar("x", lb=0, ub=1); y = m.addVar("y", lb=0, ub=1); z = m.addVar("z", lb=0, ub=1)
    t = m.addVar("t", lb=-10, ub=10)
    D = 1.25*x - 0.5*y + 1.0*z - 0.75*x*x + 2.0*y*y - 0.609375*z*z - 1.0*x*y - 1.25*y*z + 0.0625
    m.addCons(t >= D); m.setObjective(t, "minimize")
    m.setParam("limits/nodes", 1); m.setParam("parallel/maxnthreads", 1)
    for k,v in params.items(): m.setParam(k, v)
    m.presolve()
    types = [(v.name, v.vtype()) for v in m.getVars(transformed=True)]
    m.optimize()
    print(label, "status", m.getStatus(), "dual", m.getDualbound(), "types", types)
print("SCIP", Model().version())
run({}, "default")
run({"branching/fullstrong/priority": -1000000, "branching/relpscost/sbiterquot": 0.0, "branching/relpscost/initcand": 0}, "nostrong")
run({"constraints/nonlinear/linearizeheursol": "o"}, "x")
