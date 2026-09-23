"""Review check: big-M cut silently skipped when a variable in a disjunct's
nonlinear row has no finite bound in the direction needed for M.
y is bounded only through a global *nonlinear* row, so OBBT (linear rows
only) cannot bound it.  True optimum: d1 selected, y = ln(10) = 2.302585,
objective -2.302585.
"""
import os, sys as _sys, logging
_sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
logging.disable(logging.WARNING)
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from lbesh.solver import LBESH

def build():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(1, 10), initialize=2.0)
    m.y = pe.Var(bounds=(0, None), initialize=0.5)
    m.gy = pe.Constraint(expr=m.y ** 2 <= 25)          # only bound on y (nonlinear)
    m.d1 = Disjunct(); m.d1.c = pe.Constraint(expr=pe.exp(m.y) - m.x <= 0)   # y <= ln x
    m.d2 = Disjunct(); m.d2.c = pe.Constraint(expr=m.y ** 2 <= 1)
    m.dj = Disjunction(expr=[m.d1, m.d2])
    m.obj = pe.Objective(expr=-m.y)
    return m

for form, st in [("bigm", True), ("bigm", False), ("hull", True)]:
    m = build()
    try:
        s = LBESH(m, formulation=form, nlp_solver="ipopt", verbose=False, time_limit=30, threads=2, milp_max_iters=50)
        stats = s.solve(single_tree=st)
        print(f"{form}/{'single' if st else 'multi'}: status {stats.status} obj {stats.obj} lb {stats.lb} milp_iters {stats.milp_iters} "
              f"x {pe.value(m.x)} y {pe.value(m.y)} d1 {pe.value(m.d1.binary_indicator_var)} bounds y {m.y.bounds}")
    except Exception as e:
        print(f"{form}/{'single' if st else 'multi'}: ERROR {repr(e)[:200]}")
