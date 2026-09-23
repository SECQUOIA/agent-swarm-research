"""Root cut loop for a SeparableProblem (code/vertex_binarization/sob) and export to the solver IR."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import gurobipy as gp
from gurobipy import GRB

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "vertex_binarization"))
from sob.model import SeparableProblem, original_ir, _range  # noqa: E402

from .rows import normalize_row
from .separate import RowSeparator, cut_to_model


def is_concave(f) -> bool:
    return len(f.pieces) == 1 and f.pieces[0].concave


def problem_rows(p: SeparableProblem):
    """Normalized rows of p that contain at least one concave term."""
    rows = []
    fixed = getattr(p, "fixed_charge", {})        # i -> (j, c): cost c*y_j, x_i <= u_i y_j, f_i(0) = 0
    for r in range(p.A.shape[0]):
        entries = []
        for i, f in enumerate(p.funcs):
            if p.A[r, i] != 0.0:
                conc = is_concave(f)
                if conc and i in fixed:
                    j, c = fixed[i]
                    assert f.lo == 0.0 and abs(f(0.0)) < 1e-12
                    # c*1[x>0] + f(x) is concave and lower semicontinuous on [0,u]; c*y_j + w_i >= it
                    entries.append((f"x{i}", p.A[r, i], f.lo, f.hi, {f"w{i}": 1.0, f"y{j}": float(c)},
                                    lambda v, g=f._f, c=c, u=f.hi: np.asarray(g(v), float) + c * (np.asarray(v) > 1e-9 * u)))
                    continue
                entries.append((f"x{i}", p.A[r, i], f.lo, f.hi, f"w{i}" if conc else None,
                                f._f if conc else None))
        if p.B is not None:
            for j in range(p.B.shape[1]):
                if p.B[r, j] != 0.0:
                    entries.append((f"y{j}", p.B[r, j], p.y_lb[j], p.y_ub[j], None, None))
        if len(entries) < 2:
            continue
        if fixed and any(v.startswith("y") for v, *_ in entries) and sum(v.startswith("x") for v, *_ in entries) == 1:
            continue                              # variable upper bound row x_i <= u_i y_j
        row = normalize_row(entries, p.sense[r], float(p.b[r]), name=f"row{r}")
        if row is not None:
            rows.append(row)
    return rows


def root_lp(p: SeparableProblem):
    """Term-wise relaxation: chords for concave f_i, range lower bound otherwise."""
    m = gp.Model()
    m.Params.OutputFlag = 0
    v = {}
    for i, f in enumerate(p.funcs):
        v[f"x{i}"] = m.addVar(lb=f.lo, ub=f.hi, name=f"x{i}")
        wlo, whi = _range(f, f.expr, f.lo, f.hi)
        v[f"w{i}"] = m.addVar(lb=wlo, ub=whi, obj=1.0, name=f"w{i}")
        if is_concave(f):
            flo, fhi = f(f.lo), f(f.hi)
            c1 = (fhi - flo) / (f.hi - f.lo)
            m.addConstr(v[f"w{i}"] >= flo + c1 * (v[f"x{i}"] - f.lo))
    if p.B is not None:
        for j in range(p.B.shape[1]):
            v[f"y{j}"] = m.addVar(lb=p.y_lb[j], ub=p.y_ub[j], obj=float(p.c_y[j]) if p.c_y is not None else 0.0)
    for r in range(p.A.shape[0]):
        lhs = gp.quicksum(p.A[r, i] * v[f"x{i}"] for i in range(p.n) if p.A[r, i] != 0.0)
        if p.B is not None:
            lhs += gp.quicksum(p.B[r, j] * v[f"y{j}"] for j in range(p.B.shape[1]) if p.B[r, j] != 0.0)
        s = p.sense[r]
        m.addConstr(lhs <= p.b[r] if s == "<=" else lhs >= p.b[r] if s == ">=" else lhs == p.b[r])
    m.update()
    return m, v


def _row_point(row, val):
    zhat = np.array([it.z_of_v(val[it.var]) if it.var is not None else 0.0 for it in row.items])
    zhat = np.clip(zhat, 0.0, row.widths)
    if row.slack is not None:
        zhat[row.slack] = min(max(row.B - zhat.sum() + zhat[row.slack], 0.0), row.widths[row.slack])
    tp = {k: sum(tc * val[tv] for tv, tc in row.items[k].tvar.items())
             - (row.items[k].chord[0] + row.items[k].chord[1] * val[row.items[k].var]) for k in row.concave}
    return zhat, tp


def clean_cut(coefs, rhs, bounds, drop=1e-9, max_range=1e7):
    """Drop tiny coefficients conservatively; reject badly scaled cuts.  sum coefs*var >= rhs."""
    big = max(abs(c) for c in coefs.values())
    out = {}
    for k, c in coefs.items():
        if abs(c) < drop * big:
            lb, ub = bounds[k]
            rhs -= max(c * lb, c * ub)          # the dropped term is at most this
        else:
            out[k] = c
    small = min(abs(c) for c in out.values())
    if big / small > max_range:
        return None
    return {k: c / big for k, c in out.items()}, rhs / big      # largest coefficient one


def cut_loop(p: SeparableProblem, max_rounds=200, tol=1e-5, kmax=4000, time_limit=600.0, log=False,
             keep="binding", closed_form=True, in_out=True):
    """Root cut loop.  Returns (cuts, extra, info).

    cuts: list of (coefs, rhs) meaning sum coefs*var >= rhs.
    extra: (new_vars, lin_rows) of the closed-form extended rows used for equal-width rows
    (exact there by Theorem 2); the other rows are separated by column generation.
    """
    from .closedform import closed_form_rows
    t0 = time.time()
    rows = problem_rows(p)
    m, v = root_lp(p)
    m.optimize()
    bound0 = m.ObjVal if m.Status == GRB.OPTIMAL else None
    bounds_of = {k: (var.LB, var.UB) for k, var in v.items()}
    extra_vars, extra_lin, sep_rows = {}, [], []
    for r, row in enumerate(rows):
        w = row.widths[[k for k in range(row.n) if k != row.slack]]
        if closed_form and w.max() - w.min() <= 1e-9 * w.max():
            out = closed_form_rows(row, f"r{r}", kmax)
            if out is not None:
                extra_vars.update(out[0]); extra_lin.extend(out[1])
            continue                      # equal widths: closed form is the hull (or the row is degenerate)
        if row.n <= 63:
            sep_rows.append(row)
    for k, (lb, ub, _t) in extra_vars.items():
        v[k] = m.addVar(lb=lb, ub=ub, name=k)
    m.update()
    for rowd, sense, rhs in extra_lin:
        lhs = gp.quicksum(c * v[k] for k, c in rowd.items())
        m.addConstr(lhs <= rhs if sense == "<=" else lhs >= rhs if sense == ">=" else lhs == rhs)
    seps = [RowSeparator(row, kmax) for row in sep_rows]
    cuts, bounds = [], []
    core = None
    for rnd in range(max_rounds):
        m.optimize()
        if m.Status != GRB.OPTIMAL:
            break
        bounds.append(m.ObjVal)
        if len(bounds) > 10 and bounds[-1] - bounds[-11] <= 1e-6 * max(1.0, abs(bounds[-1])):
            break
        val = {k: var.X for k, var in v.items()}
        core = dict(val) if core is None else {k: 0.5 * (core[k] + val[k]) for k in val}
        new = 0
        for row, sep in zip(sep_rows, seps):
            zhat, tp = _row_point(row, val)
            cut = None
            if in_out and rnd > 0:
                mid = {k: 0.5 * (core[k] + val[k]) for k in val}
                zmid, tmid = _row_point(row, mid)
                cand = sep.separate(zmid, tmid, tol)
                if cand is not None:
                    viol = float(cand["pi"] @ zhat + cand["pi0"] - sum(cand["omega"][k] * tp[k] for k in row.concave))
                    if viol > tol:
                        cut = cand
            if cut is None:
                cut = sep.separate(zhat, tp, tol)
            if cut is None:
                continue
            cc = clean_cut(*cut_to_model(row, cut), bounds_of)
            if cc is None:
                continue
            coefs, rhs = cc
            con = m.addConstr(gp.quicksum(c * v[k] for k, c in coefs.items()) >= rhs)
            cuts.append((coefs, rhs, con))
            new += 1
        if log:
            print(f"round {rnd}: bound {m.ObjVal:.6f}, {new} cuts, {time.time()-t0:.1f}s", flush=True)
        if new == 0 or time.time() - t0 > time_limit:
            break
    m.optimize()
    if m.Status == GRB.OPTIMAL:
        bounds.append(m.ObjVal)
    ntotal = len(cuts)
    if keep == "binding" and m.Status == GRB.OPTIMAL:
        cuts = [c for c in cuts if c[2].Slack >= -1e-7 * max(1.0, abs(c[1]))]
    cuts = [(c[0], c[1]) for c in cuts]
    info = {"time": time.time() - t0, "rounds": len(bounds) - 1, "bound0": bound0,
            "bound": bounds[-1] if bounds else None, "ncuts": len(cuts), "ncuts_generated": ntotal,
            "nrows": len(rows), "rows_closed_form": len(rows) - len(sep_rows),
            "ncols": sum(s.ncols for s in seps)}
    return cuts, (extra_vars, extra_lin), info


def cut_ir(p: SeparableProblem, cuts, extra=None):
    ir = original_ir(p)
    ir.name = p.name + "-rowhull"
    if extra is not None:
        for k, (lb, ub, t) in extra[0].items():
            ir.var(k, lb, ub, t)
        ir.lin.extend(({k: float(c) for k, c in row.items()}, sense, float(rhs)) for row, sense, rhs in extra[1])
    for coefs, rhs in cuts:
        ir.lin.append(({k: float(c) for k, c in coefs.items()}, ">=", float(rhs)))
    return ir


def closed_form_ir(p: SeparableProblem, kmax=4000):
    """original_ir plus the closed-form row inequality (extended form) for every applicable row."""
    from .closedform import closed_form_rows
    t0 = time.time()
    ir = original_ir(p)
    ir.name = p.name + "-rowcf"
    used = 0
    for r, row in enumerate(problem_rows(p)):
        out = closed_form_rows(row, f"r{r}", kmax)
        if out is None:
            continue
        used += 1
        for k, (lb, ub, t) in out[0].items():
            ir.var(k, lb, ub, t)
        ir.lin.extend(out[1])
    info = {"time": time.time() - t0, "rows_used": used}
    info["bound0"], info["bound"] = ir_root_bound(p, original_ir(p)), ir_root_bound(p, ir)
    return ir, info


def ir_root_bound(p: SeparableProblem, ir):
    """LP bound of an IR whose nonlinear definitions are relaxed to chords (concave f_i only)."""
    m = gp.Model()
    m.Params.OutputFlag = 0
    v = {k: m.addVar(lb=lb, ub=ub, name=k) for k, (lb, ub, _t) in ir.vars.items()}
    for row, sense, rhs in ir.lin:
        lhs = gp.quicksum(c * v[k] for k, c in row.items())
        m.addConstr(lhs <= rhs if sense == "<=" else lhs >= rhs if sense == ">=" else lhs == rhs)
    for i, f in enumerate(p.funcs):
        if is_concave(f):
            flo, fhi = f(f.lo), f(f.hi)
            m.addConstr(v[f"w{i}"] >= flo + (fhi - flo) / (f.hi - f.lo) * (v[f"x{i}"] - f.lo))
    m.setObjective(gp.quicksum(c * v[k] for k, c in ir.obj.items()) + ir.obj_const)
    m.optimize()
    return m.ObjVal if m.Status == GRB.OPTIMAL else None
