"""Benchmark harness: LB-ESH variants vs GDPopt, MindtPy and GAMS solvers on
convex GDP instances from gdp_instances.INSTANCES.

usage: uv run python bench_gdp.py --instances a,b --methods m1,m2 --timelimit 300 --out results.jsonl --par 4
Each (instance, method) runs in a separate subprocess (fresh Python state).
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, itertools, traceback

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
# Solver executables are discovered through the caller's PATH.

GAMS_SOLVERS = ["shot", "dicopt", "sbb", "baron", "scip", "gurobi", "antigone", "knitro"]
METHODS = (["lbesh-hull-multi", "lbesh-hull-single", "lbesh-hull-single-uc", "lbesh-bigm-single", "lbesh-bigm-multi",
            "gdpopt-loa", "gdpopt-lbb", "gdpopt-ric",
            "mindtpy-oa-bigm", "mindtpy-oa-hull", "mindtpy-lpnlp-bigm", "mindtpy-lpnlp-hull", "mindtpy-ecp-bigm", "mindtpy-ecp-hull"]
           + [f"gams-{s}-{f}" for s in GAMS_SOLVERS for f in ("bigm", "hull")])


def run_one(name, method, timelimit, threads):
    import logging
    logging.disable(logging.WARNING)
    import pyomo.environ as pe
    from gdp_instances import INSTANCES
    t0 = time.time()
    m = INSTANCES[name]()
    rec = dict(instance=name, method=method, timelimit=timelimit)
    objs = list(m.component_data_objects(pe.Objective, active=True))
    sense = 1 if objs[0].sense == pe.minimize else -1
    try:
        if method.startswith("lbesh"):
            from lbesh.solver import LBESH
            parts = method.split("-")
            form = parts[1]; single = parts[2] == "single"; uc = len(parts) > 3 and parts[3] == "uc"
            s = LBESH(m, formulation=form, nlp_solver="ipopt", threads=threads, time_limit=timelimit,
                      verbose=False, user_cuts=uc)
            st = s.solve(single_tree=single)
            rec.update(status=st.status, obj=(sense * st.obj if st.obj is not None else None),
                       lb=(sense * st.lb if st.lb > -1e300 else None), cuts=st.cuts, nlps=st.nlp_solves,
                       lp_iters=st.lp_iters, milp_iters=st.milp_iters, nodes=st.nodes,
                       time_master=st.time_master, time_nlp=st.time_nlp, time_cuts=st.time_cuts)
        elif method.startswith("gdpopt"):
            alg = method.split("-")[1]
            opt = pe.SolverFactory(f"gdpopt.{alg}")
            kw = dict(nlp_solver="ipopt", mip_solver="gurobi", mip_solver_args=dict(options=dict(Threads=threads)),
                      time_limit=timelimit, tee=False)
            if alg == "lbb":
                kw = dict(minlp_solver="gams", minlp_solver_args=dict(solver="baron"), time_limit=timelimit, tee=False)
            res = opt.solve(m, **kw)
            rec.update(status=str(res.solver.termination_condition),
                       obj=_objval(m, res), lb=_bound(res, sense))
        elif method.startswith("mindtpy"):
            _, strat, form = method.split("-")
            pe.TransformationFactory(f"gdp.{form}").apply_to(m)
            opt = pe.SolverFactory("mindtpy")
            kw = dict(strategy={"oa": "OA", "ecp": "ECP", "lpnlp": "OA"}[strat], nlp_solver="ipopt",
                      mip_solver="gurobi_persistent" if strat == "lpnlp" else "gurobi",
                      mip_solver_args=dict(options=dict(Threads=threads)), time_limit=timelimit, tee=False)
            if strat == "lpnlp":
                kw["single_tree"] = True
            res = opt.solve(m, **kw)
            rec.update(status=str(res.solver.termination_condition), obj=_objval(m, res), lb=_bound(res, sense))
        elif method.startswith("gams"):
            _, solver, form = method.split("-")
            pe.TransformationFactory(f"gdp.{form}").apply_to(m)
            # Pyomo's GAMS plugin evaluates every constraint body at the current
            # values before writing (check_expr_evaluation); a variable at 0 in a
            # denominator raises ZeroDivisionError. Give such variables an
            # interior starting value (this only affects the initial point).
            for v in m.component_data_objects(pe.Var, active=True, descend_into=True):
                if v.is_fixed():
                    continue
                if v.value is None or v.value == 0:
                    lb, ub = v.lb, v.ub
                    if lb is not None and ub is not None and lb < ub:
                        v.set_value(0.5 * (lb + ub), skip_validation=True)
                    elif lb is not None and lb > 0:
                        v.set_value(lb, skip_validation=True)
                    elif ub is not None and ub < 0:
                        v.set_value(ub, skip_validation=True)
                    elif lb is None and ub is None:
                        v.set_value(1.0, skip_validation=True)
            opt = pe.SolverFactory("gams")
            res = opt.solve(m, solver=solver, tee=False, load_solutions=False,
                            add_options=[f"option reslim={timelimit};", "option optcr=1e-4;", "option optca=1e-6;", f"option threads={threads};"])
            rec.update(status=str(res.solver.termination_condition))
            try:
                m.solutions.load_from(res)
                rec["obj"] = float(pe.value(objs[0], exception=False))
            except Exception as ex:
                rec["obj"] = None
                rec["obj_error"] = repr(ex)[:200]
            if rec.get("obj") is None:
                # objective value reported by GAMS (results.problem) as a fallback
                try:
                    rec["obj"] = float(res.problem.upper_bound if sense == 1 else res.problem.lower_bound)
                    if abs(rec["obj"]) > 1e300: rec["obj"] = None
                except Exception:
                    pass
            rec["lb"] = _bound(res, sense)
        else:
            raise ValueError(method)
    except Exception as e:
        rec.update(status="error", error=repr(e)[:400], trace=traceback.format_exc()[-1500:])
    rec["time"] = time.time() - t0
    return rec


def _objval(m, res):
    import pyomo.environ as pe
    try:
        objs = list(m.component_data_objects(pe.Objective, active=True))
        return float(pe.value(objs[0]))
    except Exception:
        return None


def _bound(res, sense):
    try:
        p = res.problem
        b = p.lower_bound if sense == 1 else p.upper_bound
        b = float(b)
        return b if abs(b) < 1e300 else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", required=True)
    ap.add_argument("--methods", required=True)
    ap.add_argument("--timelimit", type=float, default=300)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--par", type=int, default=4)
    ap.add_argument("--out", required=True)
    ap.add_argument("--worker", nargs=2, default=None)
    a = ap.parse_args()
    if a.worker:
        rec = run_one(a.worker[0], a.worker[1], a.timelimit, a.threads)
        print("RESULT " + json.dumps(rec))
        return
    insts = a.instances.split(",")
    meths = METHODS if a.methods == "all" else a.methods.split(",")
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            try:
                r = json.loads(line); done.add((r["instance"], r["method"]))
            except Exception:
                pass
    jobs = [(i, mth) for i in insts for mth in meths if (i, mth) not in done]
    print(f"{len(jobs)} jobs", flush=True)
    running = []
    out = open(a.out, "a")
    def launch(job):
        cmd = [sys.executable, __file__, "--instances", "x", "--methods", "x", "--out", "/dev/null",
               "--timelimit", str(a.timelimit), "--threads", str(a.threads), "--worker", job[0], job[1]]
        return (job, subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True), time.time())
    while jobs or running:
        while jobs and len(running) < a.par:
            running.append(launch(jobs.pop(0)))
        time.sleep(1)
        still = []
        for job, p, t0 in running:
            if p.poll() is None:
                if time.time() - t0 > a.timelimit + 240:
                    p.kill(); rec = dict(instance=job[0], method=job[1], status="killed", time=time.time()-t0)
                    out.write(json.dumps(rec) + "\n"); out.flush(); print("KILLED", job, flush=True)
                else:
                    still.append((job, p, t0))
                continue
            so, se = p.communicate()
            rec = None
            for line in so.splitlines():
                if line.startswith("RESULT "):
                    rec = json.loads(line[7:])
            if rec is None:
                rec = dict(instance=job[0], method=job[1], status="crash", time=time.time()-t0, stderr=se[-1500:])
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(f"{job[0]:28s} {job[1]:22s} {rec.get('status'):16s} obj={rec.get('obj')} lb={rec.get('lb')} t={rec.get('time', 0):.1f}", flush=True)
        running = still
    out.close()


if __name__ == "__main__":
    main()
