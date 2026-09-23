import sys, time, logging
logging.disable(logging.WARNING)
import pyomo.environ as pe
from lbesh.solver import LBESH
import importlib
name = sys.argv[1]
M = importlib.import_module('gdplib.'+name)
def build():
    return M.build_model()
for form, st in [('hull', False), ('hull', True), ('bigm', True)]:
    m = build()
    try:
        s = LBESH(m, formulation=form, nlp_solver='ipopt', verbose=False, time_limit=300)
        stats = s.solve(single_tree=st)
        print(name, form, 'single' if st else 'multi', stats.status, 'obj', stats.obj, 'lb', stats.lb, 'cuts', stats.cuts, 'nlps', stats.nlp_solves, 'lp', stats.lp_iters, 'milp', stats.milp_iters, f"time {stats.time_total:.2f}", flush=True)
    except Exception as e:
        print(name, form, st, 'ERROR', repr(e)[:300], flush=True)
m = build()
t=time.time()
res = pe.SolverFactory('gdpopt.loa').solve(m, nlp_solver='ipopt', mip_solver='gurobi', time_limit=300, tee=False)
print('GDPopt LOA', pe.value(m.obj) if hasattr(m,'obj') else [pe.value(o) for o in m.component_data_objects(pe.Objective, active=True)], res.solver.termination_condition, f"{time.time()-t:.1f}s", flush=True)
m = build()
pe.TransformationFactory('gdp.bigm').apply_to(m)
t=time.time()
res = pe.SolverFactory('gams').solve(m, solver='baron', tee=False, add_options=['option optcr=1e-4; option reslim=300;'])
print('BARON bigm', [pe.value(o) for o in m.component_data_objects(pe.Objective, active=True)], res.solver.termination_condition, f"{time.time()-t:.1f}s", flush=True)
