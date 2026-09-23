"""LB-ESH: logic-based extended supporting hyperplane algorithm for convex GDP.

Multi-tree variant:
  1. interior (Slater) points per disjunct and for the global nonlinear rows;
  2. LP phase: cuts from supporting hyperplanes at boundary points found by
     bisection between the interior point and the disaggregated LP point;
  3. MILP phase: same with the MILP master; reduced NLPs at integer
     assignments give incumbents and extra supporting cuts.
Single-tree variant: one Gurobi branch-and-cut with lazy ESH cuts at
integer-feasible nodes (and optional user cuts at fractional nodes).
"""
from __future__ import annotations

import math
import time
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import pyomo.environ as pe
from pyomo.gdp import Disjunct

from .structure import Problem, extract, NLRow, INF
from .master import Master


def _finite(coef, const):
    return math.isfinite(const) and all(math.isfinite(c) for c in coef.values())


class Stats:
    def __init__(self):
        self.lp_iters = 0
        self.milp_iters = 0
        self.nlp_solves = 0
        self.cuts = 0
        self.interior_nlps = 0
        self.time_master = 0.0
        self.time_nlp = 0.0
        self.time_interior = 0.0
        self.time_cuts = 0.0
        self.time_total = 0.0
        self.time_setup = 0.0
        self.lazy_calls = 0
        self.user_cuts = 0
        self.nodes = 0
        self.status = "unknown"
        self.lb = -INF
        self.ub = INF
        self.obj = None
        self.lp_bound = None
        self.lp_end_reason = "not_run"
        self.last_lp_max_perspective_violation = None

    def as_dict(self):
        return dict(self.__dict__)


class LBESH:
    def __init__(self, model, formulation="hull", nlp_solver="ipopt", nlp_options=None,
                 threads=4, time_limit=600.0, abs_tol=1e-6, rel_tol=1e-4,
                 feas_tol=1e-6, esh=True, lp_phase=True, lp_max_iters=200,
                 milp_max_iters=500, nlp_at_integer=True, output=False, verbose=True,
                 user_cuts=False, bigm_default=1e4, cut_tol=1e-6, lp_stall_tol=1e-5):
        if any(not math.isfinite(value) or value < 0 for value in (abs_tol, rel_tol, feas_tol, cut_tol)):
            raise ValueError("solver tolerances must be finite and nonnegative")
        self.t0 = time.time()
        self.lp_stall_tol = lp_stall_tol
        self._since_nlp = 0
        self._max_viol = 0.0
        self.nlp_viol_tol = 1e-3
        self.nlp_every = 25
        self.model = model
        self._objective = next(model.component_data_objects(pe.Objective, active=True))
        self.prob: Problem = extract(model)
        self.formulation = formulation
        self.nlp_solver = nlp_solver
        self.nlp_options = nlp_options or {}
        self.threads = threads
        self.time_limit = time_limit
        self.abs_tol, self.rel_tol = abs_tol, rel_tol
        self.feas_tol = feas_tol
        self.cut_tol = cut_tol
        self.esh = esh
        self.lp_phase = lp_phase
        self.lp_max_iters = lp_max_iters
        self.milp_max_iters = milp_max_iters
        self.nlp_at_integer = nlp_at_integer
        self.output = output
        self.verbose = verbose
        self.user_cuts = user_cuts
        self.stats = Stats()
        self.stats.feasibility_tolerance = feas_tol
        self.stats.incumbent_validation = "none"
        self.stats.max_primal_violation = None
        self.stats.rigorous_certificate = False
        self._obbt_missing_bounds(threads)
        self.master = Master(self.prob, formulation, threads=threads, output=output, bigm_default=bigm_default)
        self.master.m.Params.MIPGap = min(1e-6, rel_tol / 10)
        self.master.m.Params.MIPGapAbs = min(1e-8, abs_tol / 10)
        self.interior = {}   # (i,k) -> dict id(var)->value ; ('g',) global
        self.stats.time_setup = time.time() - self.t0
        self.incumbent = None  # dict id(var)->value (original vars)
        self.ub = INF
        self.lb = -INF
        self._nlp_cache = {}
        self._nlp_fail = {}
        self.cut_log = []  # (kind, i, k, row, coef, const, z)

    # ------------------------------------------------------------------
    def _obbt_missing_bounds(self, threads):
        """LP-based bound tightening on the global linear rows for variables
        without a bound that appear in nonlinear rows or disjunctions."""
        p = self.prob
        need = {}
        for r in p.nl_rows:
            for v in r.all_vars():
                need[id(v)] = v
        for dj in p.disjunctions:
            for d in dj.disjuncts:
                for v in d.variables():
                    need[id(v)] = v
        targets = [v for v in need.values() if v is not p.epigraph_var and (v.lb is None or v.ub is None)]
        if not targets:
            return
        lp = gp.Model("obbt")
        lp.Params.OutputFlag = 0
        lp.Params.Threads = threads
        gx = {}
        for v in p.variables:
            if v is p.epigraph_var:
                continue
            lb = -GRB.INFINITY if v.lb is None else float(v.lb)
            ub = GRB.INFINITY if v.ub is None else float(v.ub)
            if v.is_fixed():
                lb = ub = float(v.value)
            gx[id(v)] = lp.addVar(lb=lb, ub=ub)
        for r in p.lin_rows:
            e = gp.LinExpr()
            for v, c in zip(r.vars, r.coefs):
                e += c * gx[id(v)]
            if r.lb > -INF:
                lp.addLConstr(e >= r.lb)
            if r.ub < INF:
                lp.addLConstr(e <= r.ub)
        n = 0
        for v in targets:
            for sense, attr in ((GRB.MINIMIZE, "lb"), (GRB.MAXIMIZE, "ub")):
                if self.remaining() <= 0:
                    return
                lp.Params.TimeLimit = max(0.001, self.remaining())
                lp.setObjective(gx[id(v)], sense)
                lp.optimize()
                if lp.Status == GRB.OPTIMAL:
                    val = lp.ObjVal
                    if attr == "lb":
                        val = val - 1e-9 * (1 + abs(val))
                        if v.lb is None or val > v.lb:
                            v.setlb(val); n += 1
                    else:
                        val = val + 1e-9 * (1 + abs(val))
                        if v.ub is None or val < v.ub:
                            v.setub(val); n += 1
        if n:
            self.log(f"OBBT derived {n} missing bounds from the global LP")

    def log(self, *a):
        if self.verbose:
            print(f"[LB-ESH {time.time()-self.t0:7.2f}s]", *a, flush=True)

    def remaining(self):
        return self.time_limit - (time.time() - self.t0)

    # ------------------------------------------------------------------
    # interior points
    def _interior_point(self, nl_rows, lin_rows, extra_lin_rows, key):
        """min t s.t. g_j(x) + lin + const <= t, linear rows, bounds."""
        if not nl_rows:
            return None
        vars_ = {}
        for r in nl_rows:
            for v in r.all_vars():
                vars_[id(v)] = v
        for r in lin_rows + extra_lin_rows:
            for v in r.vars:
                vars_[id(v)] = v
        m = pe.ConcreteModel()
        m.t = pe.Var(initialize=0.0)
        m.vs = pe.VarList()
        vmap = {}
        for vid, v in vars_.items():
            nv = m.vs.add()
            lb, ub = v.lb, v.ub
            if v.is_fixed():
                lb = ub = v.value
            # artificial box for unbounded variables: the interior point only
            # needs strict feasibility, any bounded region is admissible
            x0 = v.value if v.value is not None else 0.0
            if lb is None:
                lb = min(x0, ub if ub is not None else x0) - 1e3
            if ub is None:
                ub = max(x0, lb) + 1e3
            nv.setlb(lb); nv.setub(ub)
            x0 = v.value
            if x0 is None or (lb is not None and x0 < lb) or (ub is not None and x0 > ub):
                if lb is not None and ub is not None:
                    x0 = 0.5 * (lb + ub)
                elif lb is not None:
                    x0 = lb
                elif ub is not None:
                    x0 = ub
                else:
                    x0 = 0.0
            nv.set_value(float(x0))
            vmap[vid] = nv
        m.cons = pe.ConstraintList()
        from pyomo.core.expr.visitor import replace_expressions
        subs = {vid: vmap[vid] for vid in vars_}
        for r in nl_rows:
            e = replace_expressions(r.func.expr, substitution_map=subs)
            lin = sum(c * vmap[id(v)] for v, c in zip(r.lin_vars, r.lin_coefs))
            m.cons.add(e + lin + r.const <= m.t)
        for r in lin_rows + extra_lin_rows:
            e = sum(c * vmap[id(v)] for v, c in zip(r.vars, r.coefs))
            if isinstance(e, (int, float)):
                continue
            if r.lb > -INF:
                m.cons.add(e >= r.lb)
            if r.ub < INF:
                m.cons.add(e <= r.ub)
        m.t.setlb(-1e6)
        m.obj = pe.Objective(expr=m.t)
        ok = False
        rng = np.random.default_rng(7)
        for attempt in range(4):
            if self.remaining() <= 0:
                break
            if attempt > 0:
                for nv in m.vs.values():
                    lb, ub = nv.lb, nv.ub
                    if lb is None: lb = (ub - 10.0) if ub is not None else -10.0
                    if ub is None: ub = lb + 10.0
                    nv.set_value(float(lb + (ub - lb) * rng.uniform(0.1, 0.9)))
                m.t.set_value(1.0)
            try:
                self.stats.interior_nlps += 1
                res = self._solve_nlp_model(m)
                ok = res is not None and pe.value(m.t) < -1e-6
            except Exception as ex:
                self.log("interior NLP failed", key, str(ex)[:80])
                ok = False
            if ok:
                break
        if not ok:
            return None
        return {vid: float(pe.value(nv)) for vid, nv in vmap.items()}

    def _solve_nlp_model(self, m):
        if self.remaining() <= 0:
            return None
        opt = pe.SolverFactory(self.nlp_solver)
        for k, v in self.nlp_options.items():
            opt.options[k] = v
        if self.nlp_solver == "ipopt":
            opt.options["max_cpu_time"] = min(float(opt.options.get("max_cpu_time", INF)),
                                              max(0.001, self.remaining()))
        res = opt.solve(m, tee=False, load_solutions=False)
        tc = str(res.solver.termination_condition)
        if tc in ("optimal", "locallyOptimal", "globallyOptimal", "feasible"):
            m.solutions.load_from(res)
            return res
        if "nfeasible" in tc or tc in ("unbounded",):
            return None
        # try loading anyway
        try:
            m.solutions.load_from(res)
            return res
        except Exception:
            return None

    def compute_interior_points(self):
        p = self.prob
        rows = [r for r in p.nl_rows if p.epigraph_var is None or not any(v is p.epigraph_var for v in r.lin_vars)]
        if rows:
            self.interior[("g",)] = self._interior_point(rows, p.lin_rows, [], ("g",))
            if self.interior[("g",)] is None:
                self.log("no global interior point; using ECP cuts for global rows")
        for i, dj in enumerate(p.disjunctions):
            for k, d in enumerate(dj.disjuncts):
                if d.nl_rows:
                    pt = self._interior_point(d.nl_rows, d.lin_rows, p.lin_rows, (i, k))
                    self.interior[(i, k)] = pt
                    if pt is None:
                        self.log(f"no interior point for disjunct {d.name}; ECP cuts")

    # ------------------------------------------------------------------
    # cut generation
    def _max_violation(self, nl_rows, x):
        worst, wr = -INF, None
        vals = []
        for r in nl_rows:
            v = r.violation(x)
            vals.append(v)
            if v > worst:
                worst, wr = v, r
        return worst, vals

    def _esh_cuts(self, nl_rows, xhat, interior, tag):
        """Return list of (row, coef, const) supporting cuts separating xhat.
        For every row violated at xhat: bisection between the interior point
        and xhat on that row alone (ESH, one supporting hyperplane per violated
        row); if no interior point is available, linearize at xhat (ECP)."""
        t0 = time.time()
        cuts = []
        keys = list(xhat.keys())
        for r in nl_rows:
            v = r.violation(xhat)
            if not math.isfinite(v):
                raise ValueError(f"nonfinite violation for {r.name}")
            if v <= min(self.cut_tol, self.feas_tol):
                continue
            if self.esh and interior is not None and all(id(v) in interior for v in r.all_vars()) and r.violation(interior) < -1e-9:
                base = {kk: interior.get(kk, xhat[kk]) for kk in keys}
                def point(a):
                    return {kk: base[kk] + a * (xhat[kk] - base[kk]) for kk in keys}
                lo, hi = 0.0, 1.0
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    if r.violation(point(mid)) > 0:
                        hi = mid
                    else:
                        lo = mid
                    if hi - lo < 1e-10:
                        break
                z = point(hi)
                coef, const = r.linearize(z)
                if _finite(coef, const):
                    viol = const + sum(c * xhat[k] for k, c in coef.items())
                    if viol > self.cut_tol * 0.1:
                        cuts.append((r, coef, const, z))
                        continue
            coef, const = r.linearize(xhat)
            if not _finite(coef, const):
                raise ValueError(f"nonfinite separating cut for {r.name}")
            cuts.append((r, coef, const, dict(xhat)))
        self.stats.time_cuts += time.time() - t0
        return cuts

    def _separate_point(self, xvals, nuvals, lamtol=1e-6, add=True, lazy_cb=None, user_cb=None):
        """Generate cuts at a master point. Returns number of cuts added."""
        p = self.prob
        n = 0
        self._max_viol = 0.0
        # global rows
        if p.nl_rows:
            self._max_viol = max(self._max_viol, max(r.violation(xvals) for r in p.nl_rows))
            cuts = self._esh_cuts(p.nl_rows, xvals, self.interior.get(("g",)), "g")
            for r, coef, const, z in cuts:
                self.cut_log.append(("g", None, None, r, coef, const, z))
                if lazy_cb is not None:
                    lazy_cb(self.master.cut_expr_global(coef, const) <= 0)
                elif user_cb is not None:
                    user_cb(self.master.cut_expr_global(coef, const) <= 0)
                elif add:
                    self.master.add_global_cut(coef, const)
                n += 1
        for i, dj in enumerate(p.disjunctions):
            for k, d in enumerate(dj.disjuncts):
                if not d.nl_rows:
                    continue
                lam = xvals[id(d.indicator)]
                if lam <= lamtol:
                    continue
                if self.formulation == "hull":
                    pt = {}
                    for v in d.variables():
                        if v is d.indicator:
                            pt[id(v)] = 1.0
                        else:
                            pt[id(v)] = nuvals[(i, k, id(v))] / lam
                else:
                    pt = {id(v): (1.0 if v is d.indicator else xvals[id(v)]) for v in d.variables()}
                self._max_viol = max(self._max_viol, max(r.violation(pt) for r in d.nl_rows))
                cuts = self._esh_cuts(d.nl_rows, pt, self.interior.get((i, k)), (i, k))
                for r, coef, const, z in cuts:
                    self.cut_log.append(("d", i, k, r, coef, const, z))
                    e, rhs = self.master.cut_expr_disjunct(i, k, coef, const)
                    if e is None:
                        continue
                    if lazy_cb is not None:
                        lazy_cb(e <= rhs)
                    elif user_cb is not None:
                        user_cb(e <= rhs)
                    elif add:
                        self.master.add_disjunct_cut(i, k, coef, const)
                    n += 1
        self.stats.cuts += n
        return n

    # ------------------------------------------------------------------
    # reduced NLP at an integer assignment
    def _integer_key(self, xvals):
        key = []
        for v in self.prob.variables:
            if v.is_binary() or v.is_integer():
                key.append(int(round(xvals[id(v)])))
        return tuple(key)

    def solve_reduced_nlp(self, xvals):
        """Fix discrete variables to xvals, solve the NLP on a clone of the
        model with fixed disjuncts. Returns (obj, solution dict) or (None, None)."""
        key = self._integer_key(xvals)
        if key in self._nlp_cache:
            return self._nlp_cache[key]
        t0 = time.time()
        self.stats.nlp_solves += 1
        p = self.prob
        # set values on the original model and clone
        for v in p.variables:
            val = xvals.get(id(v))
            if val is not None and v is not p.epigraph_var and not v.is_fixed():
                if v.is_binary() or v.is_integer():
                    v.set_value(int(round(val)), skip_validation=True)
                else:
                    lb, ub = v.lb, v.ub
                    if lb is not None: val = max(val, lb)
                    if ub is not None: val = min(val, ub)
                    v.set_value(float(val), skip_validation=True)
        m = self.model.clone()
        # fix discrete vars
        for v in m.component_data_objects(pe.Var, descend_into=(pe.Block, Disjunct)):
            if (v.is_binary() or v.is_integer()) and not v.is_fixed():
                v.fix(int(round(v.value if v.value is not None else (v.lb or 0))))
        for d in m.component_data_objects(Disjunct, descend_into=(pe.Block, Disjunct)):
            d.indicator_var.fix(bool(round(d.binary_indicator_var.value)))
        if p.epigraph_var is not None:
            m.del_component(m._lbesh_epigraph)
        pe.TransformationFactory("gdp.fix_disjuncts").apply_to(m)
        # deactivate logical linear constraints on binaries (all fixed) : fine
        try:
            res = self._solve_nlp_model(m)
        except Exception as ex:
            self.log("reduced NLP error", ex)
            res = None
        self.stats.time_nlp += time.time() - t0
        if res is None:
            self._nlp_fail[key] = self._nlp_fail.get(key, 0) + 1
            if self._nlp_fail[key] >= 2:
                self._nlp_cache[key] = (None, None)
            return None, None
        # map back solution to original var ids by name
        sol = {}
        # clone preserves component names; build name map
        for v in p.variables:
            if v is p.epigraph_var:
                continue
            cv = m.find_component(v.name)
            if cv is None:
                continue
            val = pe.value(cv, exception=False)
            if val is None:
                val = xvals.get(id(v), 0.0)
            sol[id(v)] = float(val)
        objs = list(m.component_data_objects(pe.Objective, active=True, descend_into=(pe.Block,)))
        obj = float(pe.value(objs[0].expr)) * (1 if objs[0].sense == pe.minimize else -1)
        if p.epigraph_var is not None:
            sol[id(p.epigraph_var)] = obj  # t = f(x)
        validated = self._validate_primal(sol)
        if validated is None:
            return None, None
        obj, sol, _ = validated
        self._nlp_cache[key] = (obj, sol)
        return obj, sol

    def _validate_primal(self, sol):
        """Check an original GDP point numerically; never certify exact feasibility.

        Integer values are rounded only within feas_tol, then every relevant
        row is checked again. The objective is evaluated from the original
        expression, not from a relaxed epigraph or an NLP termination code.
        """
        if sol is None:
            return None
        p, tol = self.prob, self.feas_tol
        clean, worst = dict(sol), 0.0
        try:
            for v in p.variables:
                if v is p.epigraph_var:
                    continue
                value = float(clean[id(v)])
                if not math.isfinite(value):
                    return None
                if v.is_integer():
                    if abs(value - round(value)) > tol:
                        return None
                    value = float(round(value))
                    clean[id(v)] = value
                if v.is_fixed():
                    if abs(value - float(v.value)) > tol:
                        return None
                    value = clean[id(v)] = float(v.value)
                if v.lb is not None:
                    worst = max(worst, float(v.lb) - value)
                if v.ub is not None:
                    worst = max(worst, value - float(v.ub))
            active_rows = list(p.lin_rows)
            nonlinear = list(p.nl_rows)
            for dj in p.disjunctions:
                chosen = [d for d in dj.disjuncts if clean[id(d.indicator)] == 1]
                if len(chosen) != 1:
                    return None
                active_rows.extend(chosen[0].lin_rows)
                nonlinear.extend(chosen[0].nl_rows)
            # Restore variable values after evaluating the original objective.
            old = [(v, v.value) for v in p.variables if v is not p.epigraph_var]
            try:
                for v, _ in old:
                    v.set_value(clean[id(v)], skip_validation=True)
                obj = p.sense * float(pe.value(self._objective.expr))
            finally:
                for v, value in old:
                    v.set_value(value, skip_validation=True)
            if not math.isfinite(obj):
                return None
            if p.epigraph_var is not None:
                clean[id(p.epigraph_var)] = obj
            for r in active_rows:
                value = sum(c * clean[id(v)] for v, c in zip(r.vars, r.coefs))
                if not math.isfinite(value):
                    return None
                worst = max(worst, r.lb - value, value - r.ub)
            for r in nonlinear:
                value = r.violation(clean)
                if not math.isfinite(value):
                    return None
                worst = max(worst, value)
            if worst > tol:
                return None
            return obj, clean, worst
        except (KeyError, ValueError, ArithmeticError):
            return None

    def _update_incumbent(self, obj, sol):
        validated = self._validate_primal(sol)
        if validated is None:
            return False
        obj, sol, violation = validated
        if obj < self.ub - 1e-12:
            self.ub = obj
            self.incumbent = sol
            self.stats.incumbent_validation = "numerical_within_tolerance"
            self.stats.max_primal_violation = violation
            return True
        return False

    def _cuts_at_solution(self, sol):
        """Supporting cuts at an NLP solution (always valid, sharpen master)."""
        p = self.prob
        n = 0
        for r in p.nl_rows:
            coef, const = r.linearize(sol)
            if not _finite(coef, const):
                continue
            self.cut_log.append(("g", None, None, r, coef, const, dict(sol)))
            self.master.add_global_cut(coef, const)
            n += 1
        for i, dj in enumerate(p.disjunctions):
            for k, d in enumerate(dj.disjuncts):
                if not d.nl_rows or round(sol[id(d.indicator)]) != 1:
                    continue
                pt = {id(v): sol[id(v)] for v in d.variables()}
                for r in d.nl_rows:
                    coef, const = r.linearize(pt)
                    if not _finite(coef, const):
                        continue
                    self.cut_log.append(("d", i, k, r, coef, const, pt))
                    self.master.add_disjunct_cut(i, k, coef, const)
                    n += 1
        self.stats.cuts += n
        return n

    def _converged(self):
        if not math.isfinite(self.ub) or not math.isfinite(self.lb):
            return False
        tolerance = self.abs_tol + self.rel_tol * abs(self.ub)
        return -tolerance <= self.ub - self.lb <= tolerance

    # ------------------------------------------------------------------
    def _initial_cuts(self):
        """Linearize every nonlinear row at its starting point (ECP-style)
        so that the master is bounded before the first solve."""
        p = self.prob
        n = 0
        rng = np.random.default_rng(12345)
        def random_point(rows, pt):
            out = dict(pt)
            for r in rows:
                for v in r.all_vars():
                    if v is p.epigraph_var:
                        continue
                    lb, ub = v.lb, v.ub
                    if lb is None: lb = (ub - 10.0) if ub is not None else -10.0
                    if ub is None: ub = lb + 10.0
                    out[id(v)] = float(lb + (ub - lb) * rng.uniform(0.05, 0.95))
            return out
        def finite_linearization(r, pt, rows):
            for attempt in range(31):
                try:
                    coef, const = r.linearize(pt)
                    if _finite(coef, const):
                        return coef, const, pt
                except (ValueError, ArithmeticError):
                    pass
                pt = random_point(rows, pt)
            raise ValueError(f"unable to initialize a finite supporting cut for {r.name}")
        def start_point(rows):
            pt = {}
            for r in rows:
                for v in r.all_vars():
                    if id(v) in pt:
                        continue
                    if v is p.epigraph_var:
                        pt[id(v)] = 0.0
                        continue
                    val = v.value
                    lb, ub = v.lb, v.ub
                    if val is None or (lb is not None and val < lb) or (ub is not None and val > ub):
                        if lb is not None and ub is not None:
                            val = 0.5 * (lb + ub)
                        elif lb is not None:
                            val = float(lb) + 1.0
                        elif ub is not None:
                            val = float(ub) - 1.0
                        else:
                            val = 0.0
                    pt[id(v)] = float(val)
            return pt
        if p.nl_rows:
            pt = start_point(p.nl_rows)
            ip = self.interior.get(("g",))
            if ip:
                pt.update({kk: vv for kk, vv in ip.items() if kk in pt})
            for r in p.nl_rows:
                coef, const, pt2 = finite_linearization(r, pt, p.nl_rows)
                if not _finite(coef, const):
                    continue
                self.cut_log.append(("g", None, None, r, coef, const, dict(pt2)))
                self.master.add_global_cut(coef, const)
                n += 1
        for i, dj in enumerate(p.disjunctions):
            for k, d in enumerate(dj.disjuncts):
                if not d.nl_rows:
                    continue
                pt = start_point(d.nl_rows)
                ip = self.interior.get((i, k))
                if ip:
                    pt.update({kk: vv for kk, vv in ip.items() if kk in pt})
                pt[id(d.indicator)] = 1.0
                for r in d.nl_rows:
                    coef, const, pt2 = finite_linearization(r, pt, d.nl_rows)
                    if not _finite(coef, const):
                        continue
                    pt2[id(d.indicator)] = 1.0
                    self.cut_log.append(("d", i, k, r, coef, const, dict(pt2)))
                    self.master.add_disjunct_cut(i, k, coef, const)
                    n += 1
        self.stats.cuts += n
        return n

    def solve(self, single_tree=False):
        self.t0 = time.time() - self.stats.time_setup
        interior_start = time.time()
        self.compute_interior_points()
        self.stats.time_interior = time.time() - interior_start
        self._initial_cuts()
        if self.lp_phase:
            self._lp_phase()
        if single_tree:
            self._single_tree()
        else:
            self._multi_tree()
        self.stats.time_total = time.time() - self.t0
        sg = self.prob.sense  # internal values are for the minimisation form
        self.stats.lb, self.stats.ub = self.lb, self.ub
        if sg == -1:
            # original problem is a maximisation: report obj = -ub, bound = -lb
            self.stats.lb, self.stats.ub = (-self.ub if self.ub < INF else -INF), (-self.lb if self.lb > -INF else INF)
        if self.stats.lp_bound is not None:
            self.stats.lp_bound *= sg
        self.stats.obj = (sg * self.ub) if self.ub < INF else None
        self.stats.bound = (sg * self.lb) if self.lb > -INF else None
        # write incumbent to model
        if self.incumbent is not None:
            for v in self.prob.variables:
                if id(v) in self.incumbent and not v.is_fixed():
                    v.set_value(self.incumbent[id(v)], skip_validation=True)
        return self.stats

    def _perspective_violation(self, xvals, nuvals):
        """Diagnostic max λ[g(ν/λ)]_+ over every positive-weight hull branch.

        Includes branches below the separation threshold. Returns infinity
        when numerical evaluation is undefined, and None for big-M masters.
        This is a floating-point diagnostic, not an interval certificate.
        """
        if self.formulation != "hull":
            return None
        worst = 0.0
        try:
            for i, dj in enumerate(self.prob.disjunctions):
                for k, d in enumerate(dj.disjuncts):
                    lam = xvals[id(d.indicator)]
                    if lam <= 0:
                        continue
                    pt = {id(v): (1.0 if v is d.indicator else nuvals[(i, k, id(v))] / lam)
                          for v in d.variables()}
                    for r in d.nl_rows:
                        value = lam * r.violation(pt)
                        if not math.isfinite(value):
                            return INF
                        worst = max(worst, value)
        except (ValueError, ArithmeticError):
            return INF
        return worst

    def _lp_phase(self):
        M = self.master
        M.relax_integrality()
        self.stats.lp_end_reason = "iteration_limit"
        hist = []
        for it in range(self.lp_max_iters):
            if self.remaining() <= 0:
                self.stats.lp_end_reason = "time_limit"
                break
            t0 = time.time()
            M.m.Params.TimeLimit = max(0.001, self.remaining())
            M.m.optimize()
            self.stats.time_master += time.time() - t0
            self.stats.lp_iters += 1
            if M.m.Status in (GRB.INF_OR_UNBD, GRB.UNBOUNDED):
                M.m.Params.DualReductions = 0
                M.m.optimize()
            if M.m.Status not in (GRB.OPTIMAL, GRB.SUBOPTIMAL):
                self.log("LP phase status", M.m.Status)
                self.stats.lp_end_reason = f"master_status_{M.m.Status}"
                break
            x, nu = M.values(), M.nu_values()
            if M.m.Status == GRB.OPTIMAL:
                old = self.stats.lp_bound
                self.stats.lp_bound = M.m.ObjVal if old is None else max(old, M.m.ObjVal)
            self.stats.last_lp_max_perspective_violation = self._perspective_violation(x, nu)
            n = self._separate_point(x, nu)
            obj = M.m.ObjVal
            if it % 10 == 0 or n == 0:
                self.log(f"LP it {it}: obj {obj:.6g} cuts +{n} total {self.stats.cuts}")
            if n == 0:
                self.stats.lp_end_reason = "no_separating_cuts"
                break
            hist.append(obj)
            if len(hist) > 5 and abs(hist[-1] - hist[-6]) <= self.lp_stall_tol * (1 + abs(hist[-1])):
                self.log(f"LP phase stalled at {obj:.6g} after {it+1} iterations")
                self.stats.lp_end_reason = "stalled"
                break
        M.restore_integrality()

    def _multi_tree(self):
        M = self.master
        for it in range(self.milp_max_iters):
            if self.remaining() <= 0:
                self.stats.status = "time_limit"
                break
            t0 = time.time()
            M.m.Params.TimeLimit = max(0.001, self.remaining())
            M.m.optimize()
            if M.m.Status in (GRB.INF_OR_UNBD, GRB.UNBOUNDED):
                M.m.Params.DualReductions = 0
                M.m.optimize()
            self.stats.time_master += time.time() - t0
            self.stats.milp_iters += 1
            self.stats.nodes += int(M.m.NodeCount)
            st = M.m.Status
            if st == GRB.INFEASIBLE:
                self.stats.status = "numerical_error" if self.incumbent is not None else "infeasible"
                break
            if st == GRB.CUTOFF:
                self.stats.status = "cutoff"
                break
            if st not in (GRB.OPTIMAL, GRB.SUBOPTIMAL, GRB.TIME_LIMIT):
                self.stats.status = f"master_status_{st}"
                break
            if st == GRB.TIME_LIMIT and M.m.SolCount == 0:
                self.stats.status = "time_limit"
                break
            self.lb = max(self.lb, M.m.ObjBound)
            x, nu = M.values(), M.nu_values()
            n = self._separate_point(x, nu)
            # reduced NLP for incumbent
            if self.nlp_at_integer:
                obj, sol = self.solve_reduced_nlp(x)
                if obj is not None:
                    improved = self._update_incumbent(obj, sol)
                    self._cuts_at_solution(sol)
                    if improved:
                        self.log(f"  new incumbent {obj:.8g}")
            self.log(f"MILP it {it}: LB {self.lb:.8g} UB {self.ub:.8g} cuts +{n} total {self.stats.cuts}")
            if n == 0:
                # master point (integral lambda) is eps-feasible for all
                # nonlinear rows => it is an eps-feasible GDP point with
                # objective ObjVal (hull and big-M alike)
                if self.ub > M.m.ObjVal:
                    obj = M.m.ObjVal
                    self._update_incumbent(obj, x)
            if self._converged():
                self.stats.status = "optimal"
                break
            if n == 0 and (self.incumbent is None):
                # feasible master point but NLP failed: stop
                self.stats.status = "stalled"
                break
        else:
            self.stats.status = "iteration_limit"

    # ------------------------------------------------------------------
    def _single_tree(self):
        if self.remaining() <= 0:
            self.stats.status = "time_limit"
            return
        M = self.master
        M.m.Params.LazyConstraints = 1
        if self.user_cuts:
            M.m.Params.PreCrush = 1
        M.m.Params.TimeLimit = max(0.001, self.remaining())
        solver = self
        p = self.prob
        gvars = [M.gx[id(v)] for v in p.variables]
        nu_keys = list(M.nu.keys())
        nu_vars = [M.nu[k] for k in nu_keys]

        self._callback_error = None

        def callback_body(model, where):
            if where == GRB.Callback.MIPSOL:
                solver.stats.lazy_calls += 1
                xv = model.cbGetSolution(gvars)
                x = {id(v): val for v, val in zip(p.variables, xv)}
                nu = dict(zip(nu_keys, model.cbGetSolution(nu_vars))) if nu_vars else {}
                cuts = []
                n = solver._separate_point(x, nu, lazy_cb=lambda c: cuts.append(c))
                for c in cuts:
                    model.cbLazy(c)
                if n == 0:
                    solver._update_incumbent(None, x)
                solver._since_nlp += 1
                do_nlp = False
                if solver.nlp_at_integer in (True, "always"):
                    do_nlp = True
                elif solver.nlp_at_integer == "adaptive":
                    key = solver._integer_key(x)
                    if key not in solver._nlp_cache:
                        do_nlp = (n == 0) or solver._max_viol <= solver.nlp_viol_tol or solver._since_nlp >= solver.nlp_every
                if do_nlp:
                    solver._since_nlp = 0
                    obj, sol = solver.solve_reduced_nlp(x)
                    if obj is not None and obj < solver.ub - 1e-9:
                        accepted = solver._update_incumbent(obj, sol)
                        if not accepted:
                            return
                        sol = solver.incumbent
                        # pass solution to gurobi
                        vals = [sol.get(id(v), x[id(v)]) for v in p.variables]
                        model.cbSetSolution(gvars, vals)
                        if nu_vars:
                            nuv = []
                            for (i, k, vid) in nu_keys:
                                d = p.disjunctions[i].disjuncts[k]
                                lam = round(sol.get(id(d.indicator), x[id(d.indicator)]))
                                nuv.append(sol.get(vid, x[vid]) if lam == 1 else 0.0)
                            model.cbSetSolution(nu_vars, nuv)
                        model.cbUseSolution()
            elif where == GRB.Callback.MIPNODE and solver.user_cuts:
                if model.cbGet(GRB.Callback.MIPNODE_STATUS) != GRB.OPTIMAL:
                    return
                nodecnt = model.cbGet(GRB.Callback.MIPNODE_NODCNT)
                if nodecnt > 0 and nodecnt % 50 != 0:
                    return
                xv = model.cbGetNodeRel(gvars)
                x = {id(v): val for v, val in zip(p.variables, xv)}
                nu = dict(zip(nu_keys, model.cbGetNodeRel(nu_vars))) if nu_vars else {}
                cuts = []
                solver._separate_point(x, nu, lamtol=0.05, user_cb=lambda c: cuts.append(c))
                for c in cuts:
                    model.cbCut(c)
                solver.stats.user_cuts += len(cuts)

        def callback(model, where):
            try:
                callback_body(model, where)
            except Exception as ex:
                solver._callback_error = f"{type(ex).__name__}: {ex}"
                model.terminate()

        t0 = time.time()
        M.m.optimize(callback)
        self.stats.time_master += time.time() - t0
        self.stats.nodes = int(M.m.NodeCount)
        st = M.m.Status
        if self._callback_error is not None:
            self.stats.status = "numerical_error"
            self.stats.error = self._callback_error
            return
        if st in (GRB.OPTIMAL, GRB.TIME_LIMIT, GRB.SUBOPTIMAL, GRB.INTERRUPTED):
            self.lb = M.m.ObjBound
            if M.m.SolCount > 0:
                self._update_incumbent(None, M.values())
            if self._converged():
                self.stats.status = "optimal"
            elif st == GRB.TIME_LIMIT:
                self.stats.status = "time_limit"
            else:
                self.stats.status = "stalled" if st == GRB.OPTIMAL else f"master_status_{st}"
        elif st == GRB.INFEASIBLE:
            self.stats.status = "numerical_error" if self.incumbent is not None else "infeasible"
        else:
            self.stats.status = f"master_status_{st}"
