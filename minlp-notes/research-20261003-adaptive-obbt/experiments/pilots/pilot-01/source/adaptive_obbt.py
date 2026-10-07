"""Budgeted, local SCIP OBBT for bounded QCQPs.

Import ``solve_problem`` with a historical ``qcqp.QCQP`` or an object with the
same fields.  SciPy solves a separate LP; only validated dual lower bounds can
change SCIP's current-node domains.  An LP infeasibility report never prunes.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import math
import time
import warnings

import numpy as np
from scipy.optimize import linprog, OptimizeWarning
from scipy.sparse import csr_matrix
from pyscipopt import Model, Prop, SCIP_PROPTIMING, SCIP_RESULT, quicksum


@dataclass(frozen=True)
class Config:
    total_lp_budget: int = 64
    root_lp_per_call: int = 12
    node_lp_per_call: int = 4
    max_calls: int = 24
    max_calls_per_node: int = 3
    max_depth: int = 64
    time_fraction: float = 0.10
    lp_time_limit: float = 0.25
    pilot_directions: int = 2
    min_pilot_gain: float = 1e-3
    min_relative_tightening: float = 1e-4
    cutoff_improvement: float = 0.01
    box_change: float = 0.10
    endpoint_tolerance: float = 1e-7
    bound_margin: float = 1e-7
    witness_cache_size: int = 24
    retained_tangents_per_square: int = 25

    def __post_init__(self):
        for key in ("total_lp_budget", "root_lp_per_call", "node_lp_per_call",
                    "max_calls", "max_calls_per_node", "max_depth",
                    "pilot_directions", "witness_cache_size"):
            if getattr(self, key) < 0:
                raise ValueError(f"{key} must be nonnegative")
        if self.retained_tangents_per_square < 5:
            raise ValueError("retain at least five initial square tangents")
        if not 0 <= self.time_fraction <= 1 or self.lp_time_limit <= 0:
            raise ValueError("invalid time budget")
        for key in ("min_pilot_gain", "min_relative_tightening", "cutoff_improvement",
                    "box_change", "endpoint_tolerance", "bound_margin"):
            if getattr(self, key) < 0:
                raise ValueError(f"{key} must be nonnegative")


def _down(x):
    return math.nextafter(float(x), -math.inf)


def _up(x):
    return math.nextafter(float(x), math.inf)


def _fraction(x):
    return x if isinstance(x, Fraction) else Fraction(float(x))


def _float_up(x):
    value = float(x)
    return _up(value) if Fraction(value) < x else value


def dual_box_bound(c, A, b, bounds, marginals):
    """Lower bound min c*x over A*x<=b and a finite box, with directed rounding.

    Any finite y<=0 is allowed; dual feasibility is unnecessary.  Compute
    y*b + min_box (c-A.T*y)*x, enclosing residual arithmetic outwards.  This
    validates the LP's *stored binary floating-point coefficients*.  The LP
    builder separately rounds its rows outwards from their exact dyadic model.
    Return None on overflow or nonfinite input, never an optimistic bound.
    """
    y = np.minimum(np.asarray(marginals, dtype=float), 0.0)
    if len(y) != len(b) or not np.isfinite(y).all():
        return None
    rlo, rhi = np.array(c, dtype=float), np.array(c, dtype=float)
    value = 0.0
    for row, yi in enumerate(y):
        if yi == 0.0:
            continue
        value = _down(value + _down(yi * b[row]))
        for pos in range(A.indptr[row], A.indptr[row + 1]):
            col, a = A.indices[pos], A.data[pos]
            prod = float(a) * float(yi)
            rlo[col] = _down(rlo[col] - _up(prod))
            rhi[col] = _up(rhi[col] - _down(prod))
    for lo, hi, (lb, ub) in zip(rlo, rhi, bounds):
        products = (lo * lb, lo * ub, hi * lb, hi * ub)
        if not all(math.isfinite(z) for z in products):
            return None
        value = _down(value + _down(min(products)))
    return value if math.isfinite(value) else None


class Relaxation:
    """One frozen local McCormick LP, with exact row construction and finite box."""

    def __init__(self, P, lb, ub, cutoff=math.inf, tangents=None):
        self.P = P
        self.lb, self.ub = np.array(lb, dtype=float), np.array(ub, dtype=float)
        if not np.isfinite(self.lb).all() or not np.isfinite(self.ub).all():
            raise ValueError("sidecar requires a finite current box")
        if np.any(self.lb > self.ub):
            raise ValueError("empty current box")
        self.terms = list(P.terms)
        self.aux = {term: P.n + k for k, term in enumerate(self.terms)}
        self.bounds = list(zip(self.lb, self.ub))
        for i, j in self.terms:
            li, ui, lj, uj = self.lb[i], self.ub[i], self.lb[j], self.ub[j]
            if i == j:
                lo = 0.0 if li <= 0 <= ui else _down(min(li * li, ui * ui))
                hi = _up(max(li * li, ui * ui))
            else:
                values = [li * lj, li * uj, ui * lj, ui * uj]
                lo, hi = _down(min(values)), _up(max(values))
            if not math.isfinite(lo) or not math.isfinite(hi):
                raise ValueError("auxiliary interval overflow")
            self.bounds.append((lo, hi))
        self.rows, self.rhs = [], []
        for (i, j), aux in self.aux.items():
            l, u = _fraction(self.lb[i]), _fraction(self.ub[i])
            if i == j:
                knots = set(np.linspace(self.lb[i], self.ub[i], 5))
                knots.update((tangents or {}).get(i, ()))
                for p in sorted(knots):
                    p = _fraction(p)
                    self.add_row({i: 2 * p, aux: -1}, p * p)
                self.add_row({aux: 1, i: -(l + u)}, -l * u)
            else:
                a, b = _fraction(self.lb[j]), _fraction(self.ub[j])
                self.add_row({i: a, j: l, aux: -1}, l * a)
                self.add_row({i: b, j: u, aux: -1}, u * b)
                self.add_row({aux: 1, i: -a, j: -u}, -u * a)
                self.add_row({aux: 1, i: -b, j: -l}, -l * b)
        for r in range(P.m):
            row = {int(k): float(a) for k, a in zip(
                P.A.indices[P.A.indptr[r]:P.A.indptr[r + 1]],
                P.A.data[P.A.indptr[r]:P.A.indptr[r + 1]])}
            row.update({self.aux[t]: q for t, q in P.rq.get(r, {}).items()})
            if math.isfinite(P.rhi[r]):
                self.add_row(row, P.rhi[r])
            if math.isfinite(P.rlo[r]):
                self.add_row({k: -v for k, v in row.items()}, -P.rlo[r])
        if math.isfinite(cutoff):
            row = {i: P.sense * v for i, v in enumerate(P.c) if v}
            row.update({self.aux[t]: P.sense * q for t, q in P.oq.items()})
            self.add_row(row, _fraction(cutoff) - _fraction(P.sense * P.c0))
        rr, cc, vv = [], [], []
        for r, row in enumerate(self.rows):
            for k, v in row.items():
                rr.append(r); cc.append(k); vv.append(v)
        self.A = csr_matrix((vv, (rr, cc)), shape=(len(self.rows), len(self.bounds)))
        self.b = np.array(self.rhs)

    def add_row(self, row, rhs):
        """Round exact dyadic coefficients into an outward valid floating row."""
        b = _fraction(rhs)
        rounded = {}
        for k, coeff in row.items():
            exact = _fraction(coeff)
            value = float(exact)
            if not math.isfinite(value):
                raise ValueError("row coefficient overflow")
            error = _fraction(value) - exact
            lo, hi = self.bounds[k]
            b += max(error * _fraction(lo), error * _fraction(hi))
            if value:
                rounded[k] = value
        value = _float_up(b)
        if not math.isfinite(value):
            raise ValueError("row right-hand side overflow")
        self.rows.append(rounded)
        self.rhs.append(value)

    def bound(self, variable, lower, time_limit):
        c = np.zeros(len(self.bounds)); c[variable] = 1.0 if lower else -1.0
        started = time.perf_counter()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=OptimizeWarning,
                                    message="Unrecognized options detected.*")
            result = linprog(c, A_ub=self.A if len(self.b) else None,
                             b_ub=self.b if len(self.b) else None,
                             bounds=self.bounds, method="highs-ds",
                             options={"time_limit": max(0.001, time_limit),
                                      "threads": 1, "presolve": True})
        value = None
        if result.status == 0 and result.ineqlin.marginals is not None:
            value = dual_box_bound(c, self.A, self.b, self.bounds, result.ineqlin.marginals)
        return value, result.x, int(result.status), time.perf_counter() - started

    def witness_feasible(self, point):
        """Exact dyadic feasibility of a stored point in this frozen LP only."""
        if point is None or len(point) != len(self.bounds) or not np.isfinite(point).all():
            return False
        if any(v < l or v > u for v, (l, u) in zip(point, self.bounds)):
            return False
        for row, rhs in zip(self.rows, self.rhs):
            # Cheap outward test; exact arithmetic resolves boundary ambiguity.
            lo = hi = 0.0
            for k, a in row.items():
                product = a * point[k]
                lo, hi = _down(lo + _down(product)), _up(hi + _up(product))
            if hi <= rhs:
                continue
            if lo > rhs:
                return False
            if sum((_fraction(a) * _fraction(point[k]) for k, a in row.items()), Fraction(0)) > _fraction(rhs):
                return False
        return True


class TriggerState:
    """Node-scoped scheduling state; never carries bounds between siblings."""
    def __init__(self, config):
        self.config, self.nodes = config, {}

    def reason(self, node, lb, ub, cutoff):
        previous = self.nodes.get(node)
        if previous is None:
            return "first_visit"
        old_lb, old_ub, old_cutoff, calls = previous
        if calls >= self.config.max_calls_per_node:
            return None
        if math.isfinite(cutoff) and (not math.isfinite(old_cutoff) or
                old_cutoff - cutoff >= self.config.cutoff_improvement * max(1.0, abs(old_cutoff))):
            return "incumbent_improvement"
        widths = old_ub - old_lb
        changed = np.divide((lb - old_lb) + (old_ub - ub), widths,
                            out=np.zeros_like(widths), where=widths > 1e-12)
        if np.max(changed, initial=0.0) >= self.config.box_change:
            return "domain_reduction"
        return None

    def record(self, node, lb, ub, cutoff):
        count = self.nodes[node][3] + 1 if node in self.nodes else 1
        self.nodes[node] = (lb.copy(), ub.copy(), cutoff, count)


def _candidate_order(P, lb, ub, policy):
    candidates = [i for i in P.nlvars if ub[i] - lb[i] > 1e-9]
    if policy == "adaptive":
        scores = np.zeros(P.n)
        for i, j in P.terms:
            # Constraint and objective coefficients are used only to order work.
            weight = abs(P.oq.get((i, j), 0.0)) + sum(abs(q.get((i, j), 0.0)) for q in P.rq.values())
            score = weight * (ub[i] - lb[i]) * (ub[j] - lb[j])
            scores[i] += score
            if j != i:
                scores[j] += score
        candidates.sort(key=lambda i: (-scores[i], i))
    return [(i, lower) for i in candidates for lower in (True, False)]


class AdaptiveOBBT(Prop):
    def __init__(self, P, original_vars, policy, config, time_limit, deadline=math.inf):
        self.P, self.original_vars, self.policy, self.config = P, original_vars, policy, config
        self.time_budget = config.time_fraction * time_limit
        self.deadline = deadline
        self.state = TriggerState(config)
        self.witnesses, self.tangents = [], {}
        self.stats = dict(calls=0, lp_calls=0, time=0.0, lp_time=0.0,
                          proposed=0, tightened=0, screened=0, no_incumbent_calls=0,
                          nonroot_calls=0, incumbent_retriggers=0, unsupported=0,
                          lp_failures=0, errors=[], events=[])

    def _cutoff(self):
        best = self.model.getBestSol()
        if best is None:
            return math.inf
        point = np.array([self.model.getSolVal(best, v) for v in self.original_vars])
        value = self.P.fmin(point)
        if not math.isfinite(value):
            return math.inf
        # Preserve SCIP's accepted incumbent under its ordinary numerical tolerance.
        return _up(value + 1e-6 * max(1.0, abs(value)))

    def propexec(self, proptiming):
        result = {"result": SCIP_RESULT.DIDNOTRUN}
        C, S = self.config, self.stats
        if (S["lp_calls"] >= C.total_lp_budget or S["calls"] >= C.max_calls or
                S["time"] >= self.time_budget or self.model.getDepth() > C.max_depth):
            return result
        node = self.model.getCurrentNode()
        if node is None:
            return result
        started = time.perf_counter()
        event = None
        try:
            variables = [self.model.getTransformedVar(v) for v in self.original_vars]
            lb = np.array([max(self.P.lb[i], v.getLbLocal()) for i, v in enumerate(variables)])
            ub = np.array([min(self.P.ub[i], v.getUbLocal()) for i, v in enumerate(variables)])
            cutoff = self._cutoff()
            reason = self.state.reason(node.getNumber(), lb, ub, cutoff)
            if reason is None:
                return result
            self.state.record(node.getNumber(), lb, ub, cutoff)
            S["calls"] += 1
            depth = self.model.getDepth()
            S["nonroot_calls"] += int(depth > 0)
            S["incumbent_retriggers"] += int(reason == "incumbent_improvement")
            S["no_incumbent_calls"] += int(not math.isfinite(cutoff))
            event = dict(node=int(node.getNumber()), depth=depth, reason=reason,
                         cutoff=cutoff if math.isfinite(cutoff) else None,
                         lp_calls=0, tightened=0, proposed=0, screened=0,
                         gain=0.0, applications=[], stop="directions_exhausted")
            S["events"].append(event)
            if (not np.isfinite(lb).all() or not np.isfinite(ub).all() or
                    any(self.model.isInfinity(abs(float(v))) for v in np.r_[lb, ub])):
                S["unsupported"] += 1; event["stop"] = "unbounded_current_box"
                return result
            for i, j in self.P.terms:
                if i == j:
                    retained = self.tangents.setdefault(i, set())
                    for p in np.linspace(lb[i], ub[i], 5):
                        if len(retained) < C.retained_tangents_per_square:
                            retained.add(float(p))
            relaxation = Relaxation(self.P, lb, ub, cutoff, self.tangents)
            directions = _candidate_order(self.P, lb, ub, self.policy)
            limit = min(C.root_lp_per_call if depth == 0 else C.node_lp_per_call,
                        C.total_lp_budget - S["lp_calls"])
            screened = set()

            def screen(point):
                if self.policy != "adaptive" or not relaxation.witness_feasible(point):
                    return
                for i, lower in directions:
                    endpoint = lb[i] if lower else ub[i]
                    tol = C.endpoint_tolerance * max(1.0, ub[i] - lb[i])
                    if abs(point[i] - endpoint) <= tol:
                        screened.add((i, lower))

            for witness in self.witnesses:
                screen(witness)
            changed = 0
            for i, lower in directions:
                if (i, lower) in screened:
                    S["screened"] += 1; event["screened"] += 1
                    continue
                now = time.perf_counter()
                remaining = min(self.time_budget - S["time"] - (now - started), self.deadline - now)
                if remaining <= 0:
                    event["stop"] = "time_budget"; break
                if event["lp_calls"] >= limit:
                    event["stop"] = "lp_budget"; break
                bound, point, status, duration = relaxation.bound(i, lower, min(remaining, C.lp_time_limit))
                S["lp_calls"] += 1; event["lp_calls"] += 1; S["lp_time"] += duration
                if status != 0 or bound is None:
                    S["lp_failures"] += 1
                else:
                    screen(point)
                    if point is not None and C.witness_cache_size:
                        self.witnesses.append(point.copy())
                        self.witnesses = self.witnesses[-C.witness_cache_size:]
                    candidate = bound if lower else -bound
                    margin = C.bound_margin * max(1.0, abs(candidate))
                    candidate = _down(candidate - margin) if lower else _up(candidate + margin)
                    # Reject contradictory proposals; never turn an LP status into a cutoff.
                    current_l, current_u = variables[i].getLbLocal(), variables[i].getUbLocal()
                    gain = candidate - current_l if lower else current_u - candidate
                    if (current_l <= candidate <= current_u and
                            gain > max(1e-9, C.min_relative_tightening * (ub[i] - lb[i]))):
                        # SCIP rounds integer domains. Check the rounded proposal first.
                        rounded = math.ceil(candidate) if lower else math.floor(candidate)
                        compatible = (not self.P.isint[i] or current_l <= rounded <= current_u)
                        if compatible:
                            S["proposed"] += 1; event["proposed"] += 1
                            fn = self.model.tightenVarLb if lower else self.model.tightenVarUb
                            infeasible, accepted = fn(variables[i], candidate)
                            if infeasible:
                                raise RuntimeError("SCIP rejected a domain-compatible bound as infeasible")
                            if accepted:
                                changed += 1; S["tightened"] += 1; event["tightened"] += 1
                                event["gain"] += gain / max(1e-12, ub[i] - lb[i])
                                event["applications"].append(dict(variable=i, lower=lower,
                                    old_lower=float(current_l), old_upper=float(current_u),
                                    dual_bound=float(bound), proposed=float(candidate),
                                    actual_lower=float(variables[i].getLbLocal()),
                                    actual_upper=float(variables[i].getUbLocal())))
                if (self.policy == "adaptive" and event["lp_calls"] >= C.pilot_directions and
                        event["gain"] < C.min_pilot_gain):
                    event["stop"] = "unproductive_pilot"; break
            result["result"] = SCIP_RESULT.REDUCEDDOM if changed else SCIP_RESULT.DIDNOTFIND
            return result
        except (ValueError, OverflowError) as exc:
            S["unsupported"] += 1
            S["errors"].append(str(exc))
            if event is not None:
                event["stop"] = "unsupported_relaxation"
            return result
        finally:
            duration = time.perf_counter() - started
            S["time"] += duration
            if event is not None:
                event["time"] = duration


def build_model(P, time_limit=10.0, seed=0, parameters=None, log_path=None, show_output=False):
    model = Model(P.name)
    if not show_output:
        model.hideOutput()
    if log_path is not None:
        model.setLogfile(str(log_path))
    model.setRealParam("limits/time", float(time_limit))
    model.setIntParam("parallel/maxnthreads", 1)
    model.setIntParam("lp/threads", 1)
    model.setIntParam("randomization/randomseedshift", int(seed))
    if parameters:
        for name, value in parameters.items():
            model.setParam(name, value)
    inf = model.infinity()
    variables = [model.addVar(P.names[i], vtype=str(P.vtype[i]),
                             lb=float(P.lb[i]) if math.isfinite(P.lb[i]) else -inf,
                             ub=float(P.ub[i]) if math.isfinite(P.ub[i]) else inf)
                 for i in range(P.n)]
    for r in range(P.m):
        expression = quicksum(float(a) * variables[int(i)] for i, a in zip(
            P.A.indices[P.A.indptr[r]:P.A.indptr[r + 1]],
            P.A.data[P.A.indptr[r]:P.A.indptr[r + 1]]))
        expression += quicksum(float(q) * variables[i] * variables[j]
                               for (i, j), q in P.rq.get(r, {}).items())
        if P.rlo[r] == P.rhi[r]:
            model.addCons(expression == float(P.rlo[r]))
        else:
            if math.isfinite(P.rlo[r]):
                model.addCons(expression >= float(P.rlo[r]))
            if math.isfinite(P.rhi[r]):
                model.addCons(expression <= float(P.rhi[r]))
    objective = P.sense * (quicksum(float(c) * variables[i] for i, c in enumerate(P.c) if c) + float(P.c0))
    if P.oq:
        expression = objective + quicksum(P.sense * float(q) * variables[i] * variables[j]
                                          for (i, j), q in P.oq.items())
        epigraph = model.addVar("adaptive_obbt_objective", lb=-inf, ub=inf)
        model.addCons(expression <= epigraph)
        model.setObjective(epigraph, "minimize")
    else:
        model.setObjective(objective, "minimize")
    return model, variables


def solve_problem(P, policy="native", time_limit=10.0, seed=0, config=None,
                  initial_point=None, parameters=None, log_path=None, show_output=False):
    """Run one solver arm; no reference objective or known optimum is accepted.

    ``initial_point`` is optional explicit experimental data and must be
    feasible.  Public experiments should omit it. ``parameters`` exists for
    targeted callback tests; experiments must apply identical settings to arms.
    Objective and dual bound are in the data model's minimization convention.
    """
    if policy not in ("native", "fixed", "adaptive"):
        raise ValueError("policy must be native, fixed, or adaptive")
    if not math.isfinite(time_limit) or time_limit <= 0:
        raise ValueError("time_limit must be positive and finite")
    config = Config(**config) if isinstance(config, dict) else config or Config()
    wall_start = time.perf_counter()
    deadline = wall_start + time_limit
    model, variables = build_model(P, time_limit, seed, parameters, log_path, show_output)
    plugin = None
    if policy != "native":
        plugin = AdaptiveOBBT(P, variables, policy, config, time_limit, deadline)
        model.includeProp(plugin, "budgeted_obbt", "budgeted local QCQP OBBT",
                          presolpriority=0, presolmaxrounds=0,
                          proptiming=SCIP_PROPTIMING.BEFORELP, priority=-1000000,
                          freq=1, delay=False)
    if initial_point is not None:
        point = np.array(initial_point, dtype=float)
        if len(point) != P.n or not np.isfinite(point).all() or P.violation(point) > 1e-7:
            raise ValueError("initial_point is not feasible for the original model")
        solution = model.createSol()
        for variable, value in zip(variables, point):
            model.setSolVal(solution, variable, float(value))
        for variable in model.getVars():
            if variable.name == "adaptive_obbt_objective":
                model.setSolVal(solution, variable, float(P.fmin(point)))
        if not model.addSol(solution, free=True):
            raise ValueError("SCIP rejected the explicit initial point")
    remaining = deadline - time.perf_counter()
    if remaining > 0:
        model.setRealParam("limits/time", remaining)
        model.optimize()
    else:
        result = dict(name=P.name, policy=policy, seed=int(seed), time_limit=float(time_limit),
                      status="setup_time_limit", wall_time=time.perf_counter() - wall_start,
                      solving_time=0.0, objective=None, dual_bound=None, gap=None, nodes=0,
                      solution=None, violation=None, config=asdict(config),
                      obbt=plugin.stats if plugin is not None else dict(calls=0, lp_calls=0,
                      time=0.0, lp_time=0.0, proposed=0, tightened=0, screened=0,
                      no_incumbent_calls=0, nonroot_calls=0, incumbent_retriggers=0,
                      unsupported=0, lp_failures=0, errors=[], events=[]))
        model.freeProb()
        return result
    solution = model.getBestSol()
    point = np.array([model.getSolVal(solution, v) for v in variables]) if solution is not None else None

    def finite(value):
        value = float(value)
        return value if math.isfinite(value) and not model.isInfinity(abs(value)) else None

    result = dict(name=P.name, policy=policy, seed=int(seed), time_limit=float(time_limit),
                  status=str(model.getStatus()), wall_time=time.perf_counter() - wall_start,
                  solving_time=float(model.getSolvingTime()), objective=finite(P.fmin(point)) if point is not None else None,
                  dual_bound=finite(model.getDualbound()), gap=finite(model.getGap()), nodes=int(model.getNNodes()),
                  solution=point.tolist() if point is not None else None,
                  violation=float(P.violation(point)) if point is not None else None,
                  config=asdict(config), obbt=plugin.stats if plugin is not None else
                  dict(calls=0, lp_calls=0, time=0.0, lp_time=0.0, proposed=0, tightened=0,
                       screened=0, no_incumbent_calls=0, nonroot_calls=0,
                       incumbent_retriggers=0, unsupported=0, lp_failures=0, errors=[], events=[]))
    model.freeProb()
    return result
