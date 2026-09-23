"""Solve an IR with Gurobi, SCIP, or BARON (through GAMS).

Every backend returns the same record: status, primal value, dual bound,
node count, and wall-clock time including model construction.
"""
from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import sympy as sp

from .functions import X
from .model import IR


def _walk(e: sp.Expr, x, fn: dict):
    """Evaluate the sympy expression ``e`` with X := x using backend functions."""
    if e == X:
        return x
    if e.is_Number or e.is_NumberSymbol:
        return float(e)
    if e.is_Add:
        out = _walk(e.args[0], x, fn)
        for a in e.args[1:]:
            out = out + _walk(a, x, fn)
        return out
    if e.is_Mul:
        out = _walk(e.args[0], x, fn)
        for a in e.args[1:]:
            out = out * _walk(a, x, fn)
        return out
    if e.is_Pow:
        base, ex = e.args
        if ex.is_Number:
            if ex == sp.Rational(1, 2):
                return fn["sqrt"](_walk(base, x, fn))
            if float(ex) < 0:
                return 1.0 / _walk(sp.Pow(base, -ex), x, fn)
            return _walk(base, x, fn) ** (int(ex) if ex.is_Integer else float(ex))
        raise ValueError(f"unsupported exponent in {e}")
    name = type(e).__name__
    if name in fn:
        return fn[name](_walk(e.args[0], x, fn))
    raise ValueError(f"unsupported function {name}")


def _recover_x(ir: IR, val) -> dict[str, float]:
    if ir.x_affine is None:
        return {k: val(k) for k in ir.vars if k.startswith("x")}
    return {f"x{i}": const + sum(c * val(k) for k, c in terms.items())
            for i, (const, terms) in enumerate(ir.x_affine)}


def solve_gurobi(ir: IR, time_limit: float, threads: int = 4, gap: float = 1e-4, log: bool = False):
    import gurobipy as gp
    from gurobipy import GRB, nlfunc

    t0 = time.time()
    m = gp.Model(ir.name)
    m.Params.OutputFlag = int(log)
    m.Params.TimeLimit = time_limit
    m.Params.Threads = threads
    m.Params.MIPGap = gap
    m.Params.NonConvex = 2
    v = {k: m.addVar(lb=lb, ub=ub, vtype={"C": GRB.CONTINUOUS, "B": GRB.BINARY, "I": GRB.INTEGER}[t], name=k)
         for k, (lb, ub, t) in ir.vars.items()}
    for row, sense, rhs in ir.lin:
        lhs = gp.quicksum(c * v[k] for k, c in row.items())
        m.addConstr(lhs <= rhs if sense == "<=" else lhs >= rhs if sense == ">=" else lhs == rhs)

    def gabs(arg):
        inner = m.addVar(lb=-GRB.INFINITY)
        m.addGenConstrNL(inner, arg)
        out = m.addVar()
        m.addGenConstrAbs(out, inner)
        return out

    fn = {"exp": nlfunc.exp, "log": nlfunc.log, "sin": nlfunc.sin, "cos": nlfunc.cos,
          "sqrt": nlfunc.sqrt, "Abs": gabs}
    for w, g, arg in ir.nl:
        if g.is_polynomial(X) and sp.degree(g, X) <= 2:   # use Gurobi's quadratic machinery
            coeffs = [float(c) for c in sp.Poly(g, X).all_coeffs()]
            c2, c1, c0 = [0.0] * (3 - len(coeffs)) + coeffs
            m.addConstr(v[w] == c2 * v[arg] * v[arg] + c1 * v[arg] + c0)
        else:
            m.addGenConstrNL(v[w], _walk(g, v[arg], fn))
    m.setObjective(gp.quicksum(c * v[k] for k, c in ir.obj.items()) + ir.obj_const, GRB.MINIMIZE)
    m.optimize()
    has_sol = m.SolCount > 0
    return {"status": {2: "optimal", 9: "timelimit", 3: "infeasible"}.get(m.Status, str(m.Status)),
            "primal": m.ObjVal if has_sol else math.inf, "dual": m.ObjBound,
            "nodes": m.NodeCount, "time": time.time() - t0,
            "x": _recover_x(ir, lambda k: v[k].X) if has_sol else {}}


def solve_scip(ir: IR, time_limit: float, gap: float = 1e-4, log: bool = False, **_):
    import pyscipopt as ps

    t0 = time.time()
    m = ps.Model(ir.name)
    if not log:
        m.hideOutput()
    m.setParam("limits/time", time_limit)
    m.setParam("limits/gap", gap)
    v = {k: m.addVar(lb=lb, ub=ub, vtype=t, name=k) for k, (lb, ub, t) in ir.vars.items()}
    for row, sense, rhs in ir.lin:
        lhs = ps.quicksum(c * v[k] for k, c in row.items())
        m.addCons(lhs <= rhs if sense == "<=" else lhs >= rhs if sense == ">=" else lhs == rhs)
    fn = {"exp": ps.exp, "log": ps.log, "sin": ps.sin, "cos": ps.cos, "sqrt": ps.sqrt, "Abs": abs}
    for w, g, arg in ir.nl:
        m.addCons(v[w] == _walk(g, v[arg], fn))
    m.setObjective(ps.quicksum(c * v[k] for k, c in ir.obj.items()) + ir.obj_const, "minimize")
    m.optimize()
    has_sol = m.getNSols() > 0
    return {"status": m.getStatus(), "primal": m.getObjVal() if has_sol else math.inf,
            "dual": m.getDualbound(), "nodes": m.getNTotalNodes(), "time": time.time() - t0,
            "x": _recover_x(ir, lambda k: m.getVal(v[k])) if has_sol else {}}


class _GamsPrinter(sp.printing.str.StrPrinter):
    def _print_Pow(self, e):
        base, ex = e.args
        if ex == sp.Rational(1, 2):
            return f"sqrt({self._print(base)})"
        if ex.is_Integer:
            return f"power({self._print(base)},{int(ex)})"
        return f"(({self._print(base)})**({float(ex)!r}))"

    def _print_Abs(self, e):
        return f"abs({self._print(e.args[0])})"

    def _print_Float(self, e):
        return repr(float(e))

    def _print_Rational(self, e):
        return repr(float(e))


def gams_text(ir: IR, time_limit: float, gap: float, solver: str = "baron") -> str:
    pr = _GamsPrinter()
    lines = ["Variables " + ", ".join(ir.vars) + ", objvar;"]
    for kind, word in (("B", "Binary Variables"), ("I", "Integer Variables")):
        names = [k for k, (_, _, t) in ir.vars.items() if t == kind]
        if names:
            lines.append(f"{word} " + ", ".join(names) + ";")
    for k, (lb, ub, t) in ir.vars.items():
        if t != "B":
            lines.append(f"{k}.lo = {lb!r}; {k}.up = {ub!r};")
    eqs = []
    for r, (row, sense, rhs) in enumerate(ir.lin):
        op = {"<=": "=l=", ">=": "=g=", "==": "=e="}[sense]
        lhs = " + ".join(f"({c!r})*{k}" for k, c in row.items())
        eqs.append((f"lin{r}", f"{lhs} {op} {rhs!r}"))
    for r, (w, g, arg) in enumerate(ir.nl):
        eqs.append((f"nl{r}", f"{w} =e= {pr.doprint(g.subs(X, sp.Symbol(arg)))}"))
    obj = " + ".join(f"({c!r})*{k}" for k, c in ir.obj.items())
    eqs.append(("defobj", f"objvar =e= {obj} + ({ir.obj_const!r})"))
    lines.append("Equations " + ", ".join(n for n, _ in eqs) + ";")
    lines += [f"{n}.. {body};" for n, body in eqs]
    # Start nonlinear arguments inside their domains.
    for _, _, arg in ir.nl:
        lb, ub, _t = ir.vars[arg]
        lines.append(f"{arg}.l = {0.5 * (lb + ub)!r};")
    lines += ["Model m /all/;", f"option minlp={solver}, reslim={time_limit!r}, optcr={gap!r}, optca=0, threads=1;",
              "solve m using minlp minimizing objvar;",
              "file res /res.txt/; put res; res.nd=10; res.nw=24;",
              "put m.modelstat, m.solvestat, m.objval, m.objest, m.nodusd, m.resusd /;"]
    lines += [f"put '{k}', {k}.l /;" for k in ir.vars]
    return "\n".join(lines) + "\n"


def solve_baron(ir: IR, time_limit: float, gap: float = 1e-4, log: bool = False, **_):
    """Run BARON through GAMS in a temporary directory that is always removed.

    GAMS is allowed to exit normally so that it deletes its own scratch data.
    """
    t0 = time.time()
    work = Path(tempfile.mkdtemp(prefix="sob-gams-"))
    try:
        (work / "model.gms").write_text(gams_text(ir, time_limit, gap))
        subprocess.run(["gams", "model.gms", "lo=0" if not log else "lo=3"], cwd=work,
                       check=False, timeout=time_limit + 120, capture_output=not log)
        lines = (work / "res.txt").read_text().split("\n")
        ms, ss, objval, objest, nodes, _res = (float(t) for t in lines[0].split())
        has_sol = ms in (1, 2, 8)
        xs = {ln.split()[0]: float(ln.split()[1]) for ln in lines[1:] if ln.strip()}
        status = "optimal" if ms == 1 and ss == 1 else "timelimit" if ss == 3 else f"ms{ms:.0f}ss{ss:.0f}"
        return {"status": status, "primal": objval if has_sol else math.inf, "dual": objest,
                "nodes": nodes, "time": time.time() - t0, "x": _recover_x(ir, xs.__getitem__) if has_sol else {}}
    finally:
        shutil.rmtree(work, ignore_errors=True)


SOLVERS = {"gurobi": solve_gurobi, "scip": solve_scip, "baron": solve_baron}
