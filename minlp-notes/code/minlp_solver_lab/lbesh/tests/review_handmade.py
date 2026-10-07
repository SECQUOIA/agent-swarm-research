"""Review checks on hand-made convex GDPs.

A. OR-disjunction (xor=False): hull master is not exact for integral lambda
   when two disjuncts are selected (x = nu_1 + nu_2 is a Minkowski sum).
B. Global optimum inside a disjunct with an inequality-only nonlinear row and
   an integer variable that appears only in that nonlinear row.
C. Maximisation with a nonlinear objective (epigraph + sense handling).
D. Solution mapping by name with string indices containing spaces.

Run from code/minlp_solver_lab:
  OMP_NUM_THREADS=1 \
    uv run python lbesh/tests/review_handmade.py
"""
import logging, math
logging.disable(logging.WARNING)
import os, sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from lbesh.solver import LBESH


def baron(build):
    m = build()
    pe.TransformationFactory("gdp.bigm").apply_to(m)
    res = pe.SolverFactory("gams").solve(m, solver="baron", tee=False, add_options=["option optcr=1e-6;", "option reslim=60;"])
    o = next(iter(m.component_data_objects(pe.Objective, active=True)))
    return pe.value(o.expr), str(res.solver.termination_condition), m


def run_all(build, label, forms=(("hull", False), ("hull", True), ("bigm", False), ("bigm", True))):
    ref, tc, _ = baron(build)
    print(f"--- {label}: BARON {ref:.8g} ({tc})")
    for form, st in forms:
        m = build()
        s = LBESH(m, formulation=form, nlp_solver="ipopt", verbose=False, time_limit=60, threads=2)
        stats = s.solve(single_tree=st)
        o = next(iter(m.component_data_objects(pe.Objective, active=True)))
        try:
            mo = pe.value(o.expr)
        except Exception:
            mo = None
        vals = {v.name: pe.value(v, exception=False) for v in m.component_data_objects(pe.Var) if not v.name.startswith("_")}
        print(f"  {form}/{'single' if st else 'multi'}: status {stats.status} obj {stats.obj} lb {stats.lb} "
              f"model-obj {mo} vals {vals}")
    return ref


# ---------------------------------------------------------------- A
def build_or():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(-2, 0), initialize=0.0)
    m.d1 = Disjunct(); m.d1.c = pe.Constraint(expr=m.x**2 <= 1)
    m.d2 = Disjunct(); m.d2.c = pe.Constraint(expr=m.x**2 <= 1)
    m.dj = Disjunction(expr=[m.d1, m.d2], xor=False)
    m.obj = pe.Objective(expr=m.x)
    return m

# ---------------------------------------------------------------- B
def build_intdisj():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 10), initialize=5.0)
    m.n = pe.Var(domain=pe.Integers, bounds=(0, 5), initialize=1)
    m.g = pe.Constraint(expr=pe.exp(m.x / 5) + m.n <= 20)   # inactive global nonlinear row
    m.d1 = Disjunct()
    m.d1.c = pe.Constraint(expr=(m.x - 3) ** 2 + (m.n - 2.5) ** 2 <= 2)  # n appears only here
    m.d2 = Disjunct()
    m.d2.c1 = pe.Constraint(expr=m.x >= 4)
    m.d2.c2 = pe.Constraint(expr=m.n == 0)
    m.dj = Disjunction(expr=[m.d1, m.d2])
    m.obj = pe.Objective(expr=m.x + 0.5 * m.n)
    return m
# optimum: d1 with n=2: x = 3 - sqrt(1.75) = 1.677124, obj = 2.677124; d2 gives 4.

# ---------------------------------------------------------------- C
def build_max():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 4), initialize=1.0)
    m.d1 = Disjunct(); m.d1.c = pe.Constraint(expr=m.x <= 1)
    m.d2 = Disjunct(); m.d2.c = pe.Constraint(expr=m.x >= 3)
    m.dj = Disjunction(expr=[m.d1, m.d2])
    m.obj = pe.Objective(expr=10 - (m.x - 2) ** 2 - 0.5 * m.x, sense=pe.maximize)
    return m
# concave max objective; optimum at x=1 -> 10-1-0.5 = 8.5 (x=3 -> 10-1-1.5=7.5)

# ---------------------------------------------------------------- D
def build_names():
    m = pe.ConcreteModel()
    m.S = pe.Set(initialize=["a b", "c,d"])
    m.x = pe.Var(m.S, bounds=(0, 5), initialize=1.0)
    m.d1 = Disjunct(); m.d1.c = pe.Constraint(expr=m.x["a b"] ** 2 + m.x["c,d"] ** 2 <= 4); m.d1.c2 = pe.Constraint(expr=m.x["a b"] + m.x["c,d"] >= 2)
    m.d2 = Disjunct(); m.d2.c = pe.Constraint(expr=m.x["a b"] >= 3); m.d2.c2 = pe.Constraint(expr=m.x["c,d"] >= 3)
    m.dj = Disjunction(expr=[m.d1, m.d2])
    m.obj = pe.Objective(expr=(m.x["a b"] - 1.5) ** 2 + (m.x["c,d"] - 1.5) ** 2 + m.x["a b"])
    return m


if __name__ == "__main__":
    run_all(build_or, "A: OR-disjunction (true optimum -1)")
    run_all(build_intdisj, "B: integer var inside disjunct (true optimum 2.6771244)")
    run_all(build_max, "C: maximise nonlinear objective (true optimum 8.5)")
    run_all(build_names, "D: names with spaces/commas")
