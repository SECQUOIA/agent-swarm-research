"""Review check: a disjunct constraint whose variables are all fixed is
extracted as LinRow(vars=[], lb, ub) without folding the constant, so the
hull/big-M row reads 0 >= lb*lam and forces the disjunct off.
True optimum: d1 (x = 0, objective 0); d2 gives 3."""
import os, sys as _sys, logging
_sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
logging.disable(logging.WARNING)
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from lbesh.solver import LBESH
from lbesh.structure import extract

def build():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 5), initialize=1.0)
    m.p = pe.Var(bounds=(0, 5), initialize=2.0); m.p.fix(2.0)   # fixed parameter-like variable
    m.d1 = Disjunct(); m.d1.c = pe.Constraint(expr=m.p >= 1); m.d1.c2 = pe.Constraint(expr=m.x ** 2 <= 1)
    m.d2 = Disjunct(); m.d2.c = pe.Constraint(expr=m.x >= 3)
    m.dj = Disjunction(expr=[m.d1, m.d2])
    m.obj = pe.Objective(expr=m.x)
    return m

p = extract(build())
for d in p.disjunctions[0].disjuncts:
    print(d.name, [(r.name, r.vars, r.coefs, r.lb, r.ub) for r in d.lin_rows])
for form, st in [("hull", False), ("bigm", False)]:
    m = build()
    s = LBESH(m, formulation=form, nlp_solver="ipopt", verbose=False, time_limit=30, threads=2)
    stats = s.solve(single_tree=st)
    print(f"{form}/multi: status {stats.status} obj {stats.obj} x {pe.value(m.x)} d1 {pe.value(m.d1.binary_indicator_var)}")
m = build(); pe.TransformationFactory("gdp.bigm").apply_to(m)
res = pe.SolverFactory("gams").solve(m, solver="baron", tee=False, add_options=["option optcr=1e-6;"])
print("BARON", pe.value(m.obj))
