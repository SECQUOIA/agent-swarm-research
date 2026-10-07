"""Review check: LB-ESH (hull/multi, hull/single, bigm/single, bigm/multi) vs BARON
on small convex GDP instances from gdp_instances.INSTANCES.

Run from code/minlp_solver_lab:
  OMP_NUM_THREADS=1 \
    uv run python lbesh/tests/review_compare_instances.py [names...]
"""
import sys, time, json, logging, math, traceback
logging.disable(logging.WARNING)
import os, sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pyomo.environ as pe
from pyomo.gdp import Disjunct
from gdp_instances import INSTANCES
from lbesh.solver import LBESH

DEFAULT = [
    "pyomo.circles.Circles2D3", "pyomo.circles.Circles2D3_modified", "pyomo.circles.Circles3D4",
    "pyomo.farm_layout.FLay02", "pyomo.farm_layout.FLay03", "pyomo.small_lit.ex1_Lee",
    "pyomo.small_lit.basic_step", "pyomo.constrained_layout.CLay0203.l1",
]
names = sys.argv[1:] or DEFAULT
TL = 60.0
THREADS = 2


def max_violation(model):
    """Max constraint violation at the current variable values, evaluated on
    the original GDP (constraints of disjuncts whose indicator is 1 only)."""
    worst = 0.0
    def check(con):
        nonlocal worst
        b = pe.value(con.body, exception=False)
        if b is None:
            worst = max(worst, float("inf")); return
        if con.lower is not None:
            worst = max(worst, pe.value(con.lower) - b)
        if con.upper is not None:
            worst = max(worst, b - pe.value(con.upper))
    for con in model.component_data_objects(pe.Constraint, active=True, descend_into=(pe.Block,)):
        check(con)
    for d in model.component_data_objects(Disjunct, active=True, descend_into=(pe.Block,)):
        if round(pe.value(d.binary_indicator_var)) == 1:
            for con in d.component_data_objects(pe.Constraint, active=True, descend_into=(pe.Block,)):
                check(con)
    return worst


def obj_value(model):
    o = next(iter(model.component_data_objects(pe.Objective, active=True, descend_into=(pe.Block,))))
    return pe.value(o.expr), (1 if o.sense == pe.minimize else -1)


out = []
for name in names:
    ref = None
    try:
        m = INSTANCES[name]()
        pe.TransformationFactory("gdp.bigm").apply_to(m)
        t = time.time()
        res = pe.SolverFactory("gams").solve(m, solver="baron", tee=False,
                                             add_options=["option optcr=1e-6;", f"option reslim={TL};", f"option threads={THREADS};"])
        ref = obj_value(m)[0]
        print(f"{name:40s} BARON     {ref:.8g} {res.solver.termination_condition} {time.time()-t:.1f}s", flush=True)
    except Exception as e:
        print(name, "BARON error", repr(e)[:200], flush=True)
    for form, st in [("hull", False), ("hull", True), ("bigm", True), ("bigm", False)]:
        tag = f"{form}/{'single' if st else 'multi'}"
        try:
            m = INSTANCES[name]()
            s = LBESH(m, formulation=form, nlp_solver="ipopt", verbose=False, time_limit=TL, threads=THREADS)
            stats = s.solve(single_tree=st)
            viol = max_violation(m) if stats.obj is not None else None
            ov, sense = obj_value(m)
            rec = dict(instance=name, method=tag, status=stats.status, obj=stats.obj, lb=stats.lb,
                       ref=ref, model_obj=ov, viol=viol, cuts=stats.cuts, nlps=stats.nlp_solves,
                       lp=stats.lp_iters, milp=stats.milp_iters, time=stats.time_total)
            flag = ""
            if ref is not None and stats.obj is not None:
                gap = stats.obj - ref
                if abs(gap) > 1e-4 * (1 + abs(ref)):
                    flag += f" OBJ-MISMATCH({gap:+.3g})"
                if stats.lb > ref + 1e-4 * (1 + abs(ref)):
                    flag += f" LB-ABOVE-REF({stats.lb-ref:+.3g})"
            if stats.obj is not None and stats.lb > stats.obj + 1e-6 * (1 + abs(stats.obj)):
                flag += f" LB>UB({stats.lb-stats.obj:+.3g})"
            if viol is not None and viol > 1e-5:
                flag += f" INCUMBENT-VIOL({viol:.3g})"
            if stats.obj is not None and abs(ov * sense - stats.obj) > 1e-6 * (1 + abs(ov)):
                flag += f" MODEL-OBJ-DIFF({ov*sense-stats.obj:+.3g})"
            print(f"{name:40s} {tag:12s} {stats.status:16s} obj {stats.obj} lb {stats.lb} viol {viol} "
                  f"cuts {stats.cuts} nlps {stats.nlp_solves} milp {stats.milp_iters} {stats.time_total:.1f}s{flag}", flush=True)
            rec["flag"] = flag
            out.append(rec)
        except Exception as e:
            print(f"{name:40s} {tag:12s} ERROR {repr(e)[:200]}", flush=True)
            out.append(dict(instance=name, method=tag, error=repr(e)[:300]))
with open("lbesh/tests/review_compare_instances.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r) + "\n")
