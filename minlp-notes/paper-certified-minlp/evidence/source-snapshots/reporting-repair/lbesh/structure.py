"""Extract a flat convex-GDP structure from a Pyomo model.

Supported: continuous/binary/integer variables with bounds, linear global
constraints, nonlinear global constraints of the form g(x) <= ub or
g(x) >= lb (the latter is stored as -g <= -lb), one level of disjunctions
whose disjuncts contain linear and nonlinear constraints, logical
constraints (converted with core.logical_to_linear beforehand), and a linear
or nonlinear objective (nonlinear objectives get an epigraph variable).
Convexity is *assumed* for nonlinear rows; nonlinear equalities are rejected.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from pyomo.repn import generate_standard_repn
from pyomo.core.expr.visitor import identify_variables

from .nlfunc import NLFunction

INF = float("inf")


@dataclass
class LinRow:
    name: str
    vars: list
    coefs: list
    lb: float  # -inf allowed
    ub: float  # +inf allowed


@dataclass
class NLRow:
    """Row  g(x) + sum(lin_coefs * lin_vars) <= 0 with g convex."""
    name: str
    func: NLFunction  # convex function g over func.vars
    lin_vars: list = field(default_factory=list)
    lin_coefs: list = field(default_factory=list)
    const: float = 0.0  # g(x) + lin + const <= 0

    def all_vars(self):
        seen = {}
        for v in list(self.func.vars) + list(self.lin_vars):
            seen[id(v)] = v
        return list(seen.values())

    def violation(self, xvals: dict):
        """xvals maps id(var)->value. Returns g(x)+lin+const."""
        x = [xvals[id(v)] for v in self.func.vars]
        val = self.func.value(x) + self.const
        for v, c in zip(self.lin_vars, self.lin_coefs):
            val += c * xvals[id(v)]
        return val

    def linearize(self, xvals: dict):
        """Return (coef dict id(var)->coef, constant) of the tangent
        g(z) + grad(z)^T (x - z) + lin + const <= 0, i.e.
        sum coef*x + constant <= 0."""
        z = [xvals[id(v)] for v in self.func.vars]
        gz, grad = self.func.value_grad(z)
        coef = {}
        constant = gz + self.const - float(sum(gi * zi for gi, zi in zip(grad, z)))
        for v, gi in zip(self.func.vars, grad):
            coef[id(v)] = coef.get(id(v), 0.0) + float(gi)
        for v, c in zip(self.lin_vars, self.lin_coefs):
            coef[id(v)] = coef.get(id(v), 0.0) + float(c)
        return coef, constant


@dataclass
class DisjunctInfo:
    name: str
    indicator: object  # binary Pyomo var
    lin_rows: list = field(default_factory=list)
    nl_rows: list = field(default_factory=list)

    def variables(self):
        seen = {}
        for r in self.lin_rows:
            for v in r.vars:
                seen[id(v)] = v
        for r in self.nl_rows:
            for v in r.all_vars():
                seen[id(v)] = v
        return list(seen.values())


@dataclass
class DisjunctionInfo:
    name: str
    disjuncts: list
    xor: bool = True


@dataclass
class Problem:
    variables: list  # all Pyomo vars (including indicator binaries, epigraph)
    lin_rows: list
    nl_rows: list
    disjunctions: list
    obj_vars: list
    obj_coefs: list
    obj_const: float
    sense: int  # 1 min, -1 max (we always convert to min)
    epigraph_var: object = None
    var_by_id: dict = field(default_factory=dict)

    def var(self, v):
        return self.var_by_id[id(v)]


class StructureError(Exception):
    pass


def _bounds(v):
    lb = -INF if v.lb is None else float(v.lb)
    ub = INF if v.ub is None else float(v.ub)
    if v.is_fixed():
        lb = ub = float(v.value)
    return lb, ub


def _classify_constraint(con, name):
    """Return ('lin', LinRow) or ('nl', [NLRow,...])."""
    body = con.body
    lb = -INF if con.lower is None else float(pe.value(con.lower))
    ub = INF if con.upper is None else float(pe.value(con.upper))
    repn = generate_standard_repn(body, compute_values=True, quadratic=False)
    if repn.is_fixed():
        val = float(repn.constant)
        if val < lb - 1e-9 or val > ub + 1e-9:
            raise StructureError(f"constant constraint {name} infeasible")
        # satisfied constant row: represent as 0 in [lb-val, ub+...] i.e. trivially
        # feasible (do not drop the constant; a row 0 >= lb*lambda would be wrong)
        return ("lin", LinRow(name, [], [], lb - val, ub - val))
    if repn.is_linear():
        const = float(repn.constant)
        vars_ = list(repn.linear_vars)
        coefs = [float(c) for c in repn.linear_coefs]
        return ("lin", LinRow(name, vars_, coefs, lb - const, ub - const))
    # nonlinear
    if lb > -INF and ub < INF:
        if lb == ub:
            raise StructureError(f"nonlinear equality {name} is not convex")
        raise StructureError(f"two-sided nonlinear constraint {name}")
    rows = []
    # split body = nonlinear part + linear part + constant so that tangent
    # constants are computed from the nonlinear part only (no cancellation
    # against large linear terms)
    nl_expr = repn.nonlinear_expr
    lin_vars = list(repn.linear_vars)
    lin_coefs = [float(c) for c in repn.linear_coefs]
    const = float(repn.constant)
    if ub < INF:
        # nl(x) + lin + const - ub <= 0
        f = NLFunction(nl_expr, name=name)
        rows.append(NLRow(name + "_ub", f, lin_vars, lin_coefs, const - ub))
    if lb > -INF:
        # lb - body <= 0  -> -nl - lin - const + lb <= 0
        f = NLFunction(-nl_expr, name=name)
        rows.append(NLRow(name + "_lb", f, lin_vars, [-c for c in lin_coefs], lb - const))
    return ("nl", rows)


def extract(model: pe.ConcreteModel) -> Problem:
    """Extract structure from a Pyomo GDP model (not transformed)."""
    # logical constraints -> linear
    if any(True for _ in model.component_data_objects(pe.LogicalConstraint, active=True, descend_into=(pe.Block, Disjunct))):
        pe.TransformationFactory("core.logical_to_linear").apply_to(model)

    disjuncts_in_disjunctions = {}
    disjunctions = []
    for dj in model.component_data_objects(Disjunction, active=True, descend_into=(pe.Block, Disjunct)):
        dinfos = []
        for d in dj.disjuncts:
            if not d.active:
                continue
            if id(d) in disjuncts_in_disjunctions:
                raise StructureError("disjunct in two disjunctions")
            # nested disjunctions not supported
            for sub in d.component_data_objects(Disjunction, active=True, descend_into=(pe.Block,)):
                raise StructureError(f"nested disjunction {sub.name}")
            di = DisjunctInfo(d.name, d.binary_indicator_var)
            for con in d.component_data_objects(pe.Constraint, active=True, descend_into=(pe.Block,)):
                kind, rows = _classify_constraint(con, con.name)
                if kind == "lin":
                    di.lin_rows.append(rows)
                else:
                    di.nl_rows.extend(rows)
            disjuncts_in_disjunctions[id(d)] = di
            dinfos.append(di)
        disjunctions.append(DisjunctionInfo(dj.name, dinfos, xor=bool(dj.xor)))

    lin_rows, nl_rows = [], []
    for con in model.component_data_objects(pe.Constraint, active=True, descend_into=(pe.Block,)):
        # constraints on Disjunct blocks are not reached (descend_into=Block only)
        kind, rows = _classify_constraint(con, con.name)
        if kind == "lin":
            lin_rows.append(rows)
        else:
            nl_rows.extend(rows)

    objs = list(model.component_data_objects(pe.Objective, active=True, descend_into=(pe.Block,)))
    if len(objs) != 1:
        raise StructureError(f"expected one objective, got {len(objs)}")
    obj = objs[0]
    sense = 1 if obj.sense == pe.minimize else -1
    orepn = generate_standard_repn(obj.expr, compute_values=True, quadratic=False)
    epigraph = None
    if orepn.is_linear() or orepn.is_fixed():
        obj_vars = list(orepn.linear_vars)
        obj_coefs = [sense * float(c) for c in orepn.linear_coefs]
        obj_const = sense * float(orepn.constant)
    else:
        # epigraph: t >= sense*f(x)  ->  sense*f(x) - t <= 0
        epigraph = pe.Var(initialize=0.0)
        model.add_component("_lbesh_epigraph", epigraph)
        onl = orepn.nonlinear_expr if sense == 1 else -orepn.nonlinear_expr
        f = NLFunction(onl, name="objective")
        lv = list(orepn.linear_vars) + [epigraph]
        lc = [sense * float(c) for c in orepn.linear_coefs] + [-1.0]
        nl_rows.append(NLRow("objective_epi", f, lv, lc, sense * float(orepn.constant)))
        obj_vars, obj_coefs, obj_const = [epigraph], [1.0], 0.0

    # collect variables
    var_by_id = {}
    def add(v):
        var_by_id.setdefault(id(v), v)
    for r in lin_rows:
        for v in r.vars: add(v)
    for r in nl_rows:
        for v in r.all_vars(): add(v)
    for dj in disjunctions:
        for d in dj.disjuncts:
            add(d.indicator)
            for v in d.variables(): add(v)
    for v in obj_vars: add(v)
    variables = list(var_by_id.values())
    tighten_bounds(lin_rows, variables)
    disjunctive_bounds(lin_rows, disjunctions, variables)
    return Problem(variables, lin_rows, nl_rows, disjunctions, obj_vars, obj_coefs, obj_const, sense, epigraph, var_by_id)


def _propagate_rows(lin_rows, b, rounds=5, tol=1e-9, integer_ids=()):
    """Interval propagation on rows over a dict id(var)->[lb,ub] (in place).
    Infinite contributions are counted so that one unbounded variable can
    still receive a bound from the others."""
    for _ in range(rounds):
        changed = False
        for r in lin_rows:
            if not r.vars:
                continue
            los, his = [], []
            for v, c in zip(r.vars, r.coefs):
                lb, ub = b[id(v)]
                a, d = c * lb, c * ub
                if math.isnan(a): a = -INF if c != 0 else 0.0
                if math.isnan(d): d = INF if c != 0 else 0.0
                los.append(min(a, d)); his.append(max(a, d))
            fin_lo = [x for x in los if x > -INF]; n_inf_lo = len(los) - len(fin_lo); s_lo = sum(fin_lo)
            fin_hi = [x for x in his if x < INF]; n_inf_hi = len(his) - len(fin_hi); s_hi = sum(fin_hi)
            for idx, (v, c) in enumerate(zip(r.vars, r.coefs)):
                if c == 0:
                    continue
                if los[idx] > -INF:
                    rest_lo = -INF if n_inf_lo > 0 else s_lo - los[idx]
                else:
                    rest_lo = -INF if n_inf_lo > 1 else s_lo
                if his[idx] < INF:
                    rest_hi = INF if n_inf_hi > 0 else s_hi - his[idx]
                else:
                    rest_hi = INF if n_inf_hi > 1 else s_hi
                lb, ub = b[id(v)]
                isint = id(v) in integer_ids
                if r.ub < INF and rest_lo > -INF:
                    val = (r.ub - rest_lo) / c
                    if c > 0 and val < ub - tol:
                        b[id(v)][1] = math.floor(val + 1e-9) if isint else val; changed = True
                    elif c < 0 and val > lb + tol:
                        b[id(v)][0] = math.ceil(val - 1e-9) if isint else val; changed = True
                lb, ub = b[id(v)]
                if r.lb > -INF and rest_hi < INF:
                    val = (r.lb - rest_hi) / c
                    if c > 0 and val > lb + tol:
                        b[id(v)][0] = math.ceil(val - 1e-9) if isint else val; changed = True
                    elif c < 0 and val < ub - tol:
                        b[id(v)][1] = math.floor(val + 1e-9) if isint else val; changed = True
        if not changed:
            break
    return b


def tighten_bounds(lin_rows, variables, rounds=5, tol=1e-9):
    """Interval propagation on global linear rows; writes bounds to the vars."""
    b = {id(v): list(_bounds(v)) for v in variables}
    ints = {id(v) for v in variables if v.is_integer()}
    _propagate_rows(lin_rows, b, rounds, tol, ints)
    for v in variables:
        if v.is_fixed():
            continue
        lb, ub = b[id(v)]
        clb, cub = _bounds(v)
        if lb > clb + tol and math.isfinite(lb):
            v.setlb(lb)
        if ub < cub - tol and math.isfinite(ub):
            v.setub(ub)


def disjunctive_bounds(lin_rows, disjunctions, variables, rounds=3):
    """Valid global bounds from disjunctions: the bound implied by every
    disjunct (its linear rows plus the current global bounds, indicator fixed
    to 1) holds globally; take the union over disjuncts. Only linear rows."""
    ints = {id(v) for v in variables if v.is_integer()}
    for _ in range(rounds):
        changed = False
        current = {id(v): list(_bounds(v)) for v in variables}
        for dj in disjunctions:
            union = {}
            for d in dj.disjuncts:
                cur = {k: list(v) for k, v in current.items()}
                cur[id(d.indicator)] = [1.0, 1.0]
                imp = _propagate_rows(d.lin_rows + lin_rows, cur, 5, 1e-9, ints)
                for vid, (lb, ub) in imp.items():
                    if vid == id(d.indicator):
                        continue
                    u = union.setdefault(vid, [INF, -INF])
                    u[0] = min(u[0], lb); u[1] = max(u[1], ub)
            for v in variables:
                if id(v) not in union or v.is_fixed():
                    continue
                lb, ub = union[id(v)]
                clb, cub = _bounds(v)
                if lb > clb + 1e-9 and math.isfinite(lb):
                    v.setlb(lb); changed = True
                if ub < cub - 1e-9 and math.isfinite(ub):
                    v.setub(ub); changed = True
        if changed:
            tighten_bounds(lin_rows, variables)
        else:
            break
