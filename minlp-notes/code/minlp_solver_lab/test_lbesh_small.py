import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from lbesh.solver import LBESH

def build():
    m = pe.ConcreteModel()
    m.x = pe.Var([1,2,3], bounds=(0, 8), initialize=1.0)
    m.c = pe.Constraint(expr=m.x[1] + m.x[2] + m.x[3] >= 6)
    # global convex constraint
    m.g = pe.Constraint(expr=pe.exp(0.3*m.x[1]) + m.x[2]**2 * 0.1 <= 12)
    m.units = pe.Set(initialize=[1,2])
    def d_rule(d, u, mode):
        if mode == 'on':
            if u == 1:
                d.c1 = pe.Constraint(expr=(m.x[1]-2)**2 + (m.x[2]-3)**2 <= 4)
                d.c2 = pe.Constraint(expr=m.x[3] <= 5)
            else:
                d.c1 = pe.Constraint(expr=pe.exp(m.x[3]/3) + m.x[1] <= 7)
        else:
            if u == 1:
                d.c1 = pe.Constraint(expr=m.x[1] + m.x[2] <= 3)
            else:
                d.c1 = pe.Constraint(expr=m.x[3] <= 1.5)
    m.D = Disjunct(m.units, ['on','off'], rule=d_rule)
    m.dj = Disjunction(m.units, rule=lambda m,u: [m.D[u,'on'], m.D[u,'off']])
    m.obj = pe.Objective(expr=3*m.D[1,'on'].binary_indicator_var + 2*m.D[2,'on'].binary_indicator_var + m.x[1] + 0.5*m.x[2] + 2*m.x[3] + 0.2*(m.x[1]-1)**2)
    return m

for form in ['hull','bigm']:
    for st in [False, True]:
        m = build()
        s = LBESH(m, formulation=form, nlp_solver='ipopt', verbose=False, time_limit=60)
        stats = s.solve(single_tree=st)
        print(form, 'single' if st else 'multi', stats.status, 'obj', stats.obj, 'lb', stats.lb, 'cuts', stats.cuts, 'nlps', stats.nlp_solves, 'lp', stats.lp_iters, 'milp', stats.milp_iters, f"time {stats.time_total:.2f}")
# reference with BARON via gams on bigm
m = build()
pe.TransformationFactory('gdp.bigm').apply_to(m)
res = pe.SolverFactory('gams').solve(m, solver='baron', tee=False, add_options=['option optcr=1e-6;'])
print('BARON ref', pe.value(m.obj), res.solver.termination_condition)
