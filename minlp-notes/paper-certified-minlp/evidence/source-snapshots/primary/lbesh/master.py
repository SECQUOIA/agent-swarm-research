"""Gurobi master problem for LB-ESH: hull (exact affine perspective of
polyhedral disjuncts) or big-M relaxation of the linearized GDP."""
from __future__ import annotations

import math
import gurobipy as gp
from gurobipy import GRB

from .structure import Problem, LinRow, INF


class Master:
    def __init__(self, prob: Problem, formulation="hull", threads=4, output=False,
                 bigm_default=1e4, env=None):
        self.prob = prob
        self.formulation = formulation
        self.m = gp.Model("lbesh_master", env=env)
        self.m.Params.OutputFlag = 1 if output else 0
        self.m.Params.Threads = threads
        self.gx = {}       # id(var) -> gurobi var
        self.nu = {}       # (disjunction idx, disjunct idx, id(var)) -> gurobi var
        self.lam = {}      # (i,k) -> gurobi var (the indicator binary)
        self.ncuts = 0
        self.bigm_default = bigm_default
        self._build()

    # ------------------------------------------------------------------
    def _build(self):
        p, m = self.prob, self.m
        for v in p.variables:
            lb, ub = v.lb, v.ub
            lb = -GRB.INFINITY if lb is None else float(lb)
            ub = GRB.INFINITY if ub is None else float(ub)
            if v.is_fixed():
                lb = ub = float(v.value)
            if v.is_binary():
                vt = GRB.BINARY
            elif v.is_integer():
                vt = GRB.INTEGER
            else:
                vt = GRB.CONTINUOUS
            self.gx[id(v)] = m.addVar(lb=lb, ub=ub, vtype=vt, name=v.name[:200])
        m.update()
        for r in p.lin_rows:
            self._add_linrow_global(r)
        for i, dj in enumerate(p.disjunctions):
            self._add_disjunction(i, dj)
        obj = gp.LinExpr(p.obj_const)
        for v, c in zip(p.obj_vars, p.obj_coefs):
            obj += c * self.gx[id(v)]
        m.setObjective(obj, GRB.MINIMIZE)
        m.update()

    def _add_linrow_global(self, r: LinRow):
        e = gp.LinExpr()
        for v, c in zip(r.vars, r.coefs):
            e += c * self.gx[id(v)]
        if r.lb > -INF:
            self.m.addLConstr(e >= r.lb, name=r.name + "_lb")
        if r.ub < INF:
            self.m.addLConstr(e <= r.ub, name=r.name + "_ub")

    def _bounds_of(self, v):
        lb, ub = v.lb, v.ub
        if v.is_fixed():
            return float(v.value), float(v.value)
        return (-INF if lb is None else float(lb), INF if ub is None else float(ub))

    def _add_disjunction(self, i, dj):
        m, p = self.m, self.prob
        lams = []
        for k, d in enumerate(dj.disjuncts):
            lam = self.gx[id(d.indicator)]
            self.lam[(i, k)] = lam
            lams.append(lam)
        if dj.xor:
            m.addLConstr(gp.quicksum(lams) == 1, name=f"xor_{i}")
        else:
            # An OR disjunction (several disjuncts may be selected) is not a
            # union of the disjunct sets; the Balas hull with x = sum nu would
            # be a Minkowski sum. Not supported (Pyomo's gdp.hull refuses it too).
            raise ValueError(f"disjunction {dj.name} is OR (xor=False); only exclusive disjunctions are supported")
        if self.formulation == "hull":
            # variables appearing in the disjunction
            vset = {}
            for d in dj.disjuncts:
                for v in d.variables():
                    if v is d.indicator:
                        continue
                    vset[id(v)] = v
            for vid, v in vset.items():
                lb, ub = self._bounds_of(v)
                if lb == -INF or ub == INF:
                    raise ValueError(f"hull needs bounds on {v.name}")
                agg = gp.LinExpr()
                for k, d in enumerate(dj.disjuncts):
                    nu = m.addVar(lb=min(lb, 0.0), ub=max(ub, 0.0), name=f"nu_{i}_{k}_{v.name[:60]}")
                    self.nu[(i, k, vid)] = nu
                    lam = self.lam[(i, k)]
                    m.addLConstr(nu >= lb * lam, name=f"nulb_{i}_{k}_{v.name[:60]}")
                    m.addLConstr(nu <= ub * lam, name=f"nuub_{i}_{k}_{v.name[:60]}")
                    agg += nu
                m.addLConstr(agg == self.gx[vid], name=f"agg_{i}_{v.name[:60]}")
            for k, d in enumerate(dj.disjuncts):
                lam = self.lam[(i, k)]
                for r in d.lin_rows:
                    e = gp.LinExpr()
                    for v, c in zip(r.vars, r.coefs):
                        if v is d.indicator:
                            e += c * lam
                        else:
                            e += c * self.nu[(i, k, id(v))]
                    if r.lb > -INF:
                        m.addLConstr(e >= r.lb * lam, name=f"{r.name}_lb")
                    if r.ub < INF:
                        m.addLConstr(e <= r.ub * lam, name=f"{r.name}_ub")
        else:  # big-M
            for k, d in enumerate(dj.disjuncts):
                lam = self.lam[(i, k)]
                for r in d.lin_rows:
                    e = gp.LinExpr()
                    lo, hi = 0.0, 0.0
                    for v, c in zip(r.vars, r.coefs):
                        e += c * self.gx[id(v)]
                        lb, ub = self._bounds_of(v)
                        if v is d.indicator:
                            lb, ub = 0.0, 1.0
                        a, b = c * lb, c * ub
                        lo += min(a, b)
                        hi += max(a, b)
                    if r.ub < INF:
                        if not math.isfinite(hi):
                            raise ValueError(f"big-M needs bounds for row {r.name}")
                        M = max(hi - r.ub, 0.0)
                        m.addLConstr(e <= r.ub + M * (1 - lam), name=f"{r.name}_ub")
                    if r.lb > -INF:
                        if not math.isfinite(lo):
                            raise ValueError(f"big-M needs bounds for row {r.name}")
                        M = max(r.lb - lo, 0.0)
                        m.addLConstr(e >= r.lb - M * (1 - lam), name=f"{r.name}_lb")

    # ------------------------------------------------------------------
    def cut_expr_global(self, coef: dict, const: float):
        e = gp.LinExpr(const)
        for vid, c in coef.items():
            e += c * self.gx[vid]
        return e

    def cut_expr_disjunct(self, i, k, coef: dict, const: float):
        """Return (expr, rhs_expr) meaning expr <= rhs_expr for cut
        sum coef*x + const <= 0 valid inside disjunct (i,k)."""
        lam = self.lam[(i, k)]
        d = self.prob.disjunctions[i].disjuncts[k]
        if self.formulation == "hull":
            e = gp.LinExpr()
            for vid, c in coef.items():
                if vid == id(d.indicator):
                    e += c * lam
                else:
                    e += c * self.nu[(i, k, vid)]
            e += const * lam
            return e, 0.0
        else:
            e = gp.LinExpr(const)
            hi = const
            for vid, c in coef.items():
                v = self.prob.var_by_id[vid]
                e += c * self.gx[vid]
                lb, ub = self._bounds_of(v)
                if vid == id(d.indicator):
                    lb, ub = 0.0, 1.0
                hi += max(c * lb, c * ub)
            if not math.isfinite(hi):
                raise ValueError(f"big-M cut in disjunct {d.name} needs finite bounds on all cut variables")
            M = max(hi, 0.0)
            return e, M * (1 - lam)

    def add_global_cut(self, coef, const, name=None):
        self.ncuts += 1
        return self.m.addLConstr(self.cut_expr_global(coef, const) <= 0, name=name or f"gcut{self.ncuts}")

    def add_disjunct_cut(self, i, k, coef, const, name=None):
        e, rhs = self.cut_expr_disjunct(i, k, coef, const)
        if e is None:
            return None
        self.ncuts += 1
        return self.m.addLConstr(e <= rhs, name=name or f"dcut{self.ncuts}")

    # ------------------------------------------------------------------
    def relax_integrality(self):
        self._saved = []
        for v in self.m.getVars():
            if v.VType != GRB.CONTINUOUS:
                self._saved.append((v, v.VType))
                v.VType = GRB.CONTINUOUS
        self.m.update()

    def restore_integrality(self):
        for v, t in self._saved:
            v.VType = t
        self._saved = []
        self.m.update()

    def values(self):
        return {vid: gv.X for vid, gv in self.gx.items()}

    def nu_values(self):
        return {key: gv.X for key, gv in self.nu.items()}
