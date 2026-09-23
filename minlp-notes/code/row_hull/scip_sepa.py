"""SCIP separator for row-hull cuts on local boxes (prototype, PySCIPOpt).

The model is the native SCIP model of the solver-neutral IR (w_i == f_i(x_i), linear rows).  At
every separation call the separator rebuilds the normalized rows on the current local bounds,
separates the LP solution (closed form for equal widths, column generation otherwise) and adds the
cuts as local rows whenever a bound differs from its global value.

python scip_sepa.py <m> <n> <seed> <cap> <cost> {native|root|tree} [--tl 300] [--maxdepth 1000]
"""
from __future__ import annotations

import argparse, json, math, sys, time
from pathlib import Path

import numpy as np
import pyscipopt as ps
from pyscipopt import Sepa, SCIP_RESULT

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
from sob.model import original_ir
from sob.backends import _walk
from rowhull.rows import normalize_row
from rowhull.separate import RowSeparator, cut_to_model
from rowhull.strengthen import clean_cut, is_concave


def equal_width_cut(row, zhat, tp):
    """Most violated linearization of (RH); None if the row is not an equal-width equality row."""
    w = row.widths
    if row.slack is not None or w.max() - w.min() > 1e-9 * w.max():
        return False, None
    w = float(w.mean())
    k = math.floor(row.B / w + 1e-9)
    r = row.B - k * w
    if r <= 1e-7 * w or r >= (1 - 1e-7) * w:
        return True, None
    pi, omega, lhs, pi0 = np.zeros(row.n), np.zeros(row.n), 0.0, 1.0
    for i, it in enumerate(row.items):
        e1, e2 = zhat[i] / r, (w - zhat[i]) / (w - r)
        d = float(it.gap(np.array([r]))[0]) if it.f is not None else 0.0
        e3 = tp[i] / d if d > 1e-12 else math.inf
        e = min(e1, e2, e3)
        lhs += e
        if e == e3:
            omega[i] = 1.0 / d
        elif e == e1:
            pi[i] = -1.0 / r               # cut: omega.tau >= pi.z + pi0  with  pi0 = 1 - ...
        else:
            pi[i] = 1.0 / (w - r); pi0 -= w / (w - r)
    if lhs >= 1 - 1e-6:
        return True, None
    return True, {"pi": pi, "pi0": pi0, "omega": omega, "viol": 1 - lhs}


class RowHullSepa(Sepa):
    def __init__(self, p, svars, maxdepth, tol=1e-4):
        self.p, self.svars, self.maxdepth, self.tol = p, svars, maxdepth, tol
        self.tvars = None
        self.ncuts = self.ncalls = 0
        self.time = 0.0
        self.cache = {}

    def sepaexeclp(self):
        m, p = self.model, self.p
        if m.getDepth() > self.maxdepth:
            return {"result": SCIP_RESULT.DIDNOTRUN}
        t0 = time.time()
        self.ncalls += 1
        if self.tvars is None:
            self.tvars = {k: m.getTransformedVar(v) for k, v in self.svars.items()}
        tv = self.tvars
        lo = np.array([max(tv[f"x{i}"].getLbLocal(), p.funcs[i].lo) for i in range(p.n)])
        hi = np.array([min(tv[f"x{i}"].getUbLocal(), p.funcs[i].hi) for i in range(p.n)])
        glo = np.array([tv[f"x{i}"].getLbGlobal() for i in range(p.n)])
        ghi = np.array([tv[f"x{i}"].getUbGlobal() for i in range(p.n)])
        val = {k: m.getSolVal(None, v) for k, v in tv.items()}
        added, cutoff = 0, False
        for r in range(p.A.shape[0]):
            idx = np.flatnonzero(p.A[r])
            if (hi[idx] < lo[idx] - 1e-9).any():
                continue
            key = (r, tuple(lo[idx]), tuple(hi[idx]))
            if key not in self.cache:
                entries = [(f"x{i}", p.A[r, i], lo[i], max(hi[i], lo[i]),
                            f"w{i}" if is_concave(p.funcs[i]) else None,
                            p.funcs[i]._f if is_concave(p.funcs[i]) else None) for i in idx]
                row = normalize_row(entries, p.sense[r], float(p.b[r]))
                if len(self.cache) > 4000:
                    self.cache.clear()
                self.cache[key] = (row, None)
            row, sep = self.cache[key]
            if row is None or row.n > 63 or row.B < -1e-9 or row.B > row.widths.sum() + 1e-9:
                continue
            zhat = np.clip(np.array([it.z_of_v(val[it.var]) if it.var else 0.0 for it in row.items]), 0, row.widths)
            if row.slack is not None:
                zhat[row.slack] = min(max(row.B - zhat.sum() + zhat[row.slack], 0.0), row.widths[row.slack])
            tp = {k: max(sum(c * val[t] for t, c in row.items[k].tvar.items())
                         - row.items[k].chord[0] - row.items[k].chord[1] * val[row.items[k].var], 0.0)
                  for k in row.concave}
            tpv = np.array([tp.get(k, 0.0) for k in range(row.n)])
            handled, cut = equal_width_cut(row, zhat, tpv)
            if not handled:
                if sep is None:
                    sep = RowSeparator(row, 2000)
                    self.cache[key] = (row, sep)
                cut = sep.separate(zhat, tp, self.tol)
            if cut is None:
                continue
            bounds_of = {}
            for it in row.items:
                if it.var:
                    bounds_of[it.var] = (it.lo, it.hi)
                    for t in (it.tvar or {}):
                        bounds_of[t] = (tv[t].getLbLocal(), tv[t].getUbLocal())
            cc = clean_cut(*cut_to_model(row, cut), bounds_of)
            if cc is None:
                continue
            coefs, rhs = cc
            local = bool(((lo[idx] > glo[idx] + 1e-12) | (hi[idx] < ghi[idx] - 1e-12)).any())
            srow = m.createEmptyRowSepa(self, f"rh{self.ncuts}", lhs=rhs, rhs=None, local=local, removable=True)
            m.cacheRowExtensions(srow)
            for k, c in coefs.items():
                m.addVarToRow(srow, tv[k], float(c))
            m.flushRowExtensions(srow)
            if m.isCutEfficacious(srow):
                cutoff |= bool(m.addCut(srow, forcecut=False))
                added += 1
                self.ncuts += 1
            m.releaseRow(srow)
        self.time += time.time() - t0
        if cutoff:
            return {"result": SCIP_RESULT.CUTOFF}
        return {"result": SCIP_RESULT.SEPARATED if added else SCIP_RESULT.DIDNOTFIND}


def solve(p, mode, tl, maxdepth=1000, log=False, freq=1):
    t0 = time.time()
    ir = original_ir(p)
    m = ps.Model(ir.name)
    if not log:
        m.hideOutput()
    m.setParam("limits/time", tl); m.setParam("limits/gap", 1e-4)
    v = {k: m.addVar(lb=lb, ub=ub, vtype=t, name=k) for k, (lb, ub, t) in ir.vars.items()}
    for row, sense, rhs in ir.lin:
        lhs = ps.quicksum(c * v[k] for k, c in row.items())
        m.addCons(lhs <= rhs if sense == "<=" else lhs >= rhs if sense == ">=" else lhs == rhs)
    fn = {"exp": ps.exp, "log": ps.log, "sin": ps.sin, "cos": ps.cos, "sqrt": ps.sqrt, "Abs": abs}
    for w, g, arg in ir.nl:
        m.addCons(v[w] == _walk(g, v[arg], fn))
    m.setObjective(ps.quicksum(c * v[k] for k, c in ir.obj.items()) + ir.obj_const, "minimize")
    sepa = None
    if mode != "native":
        sepa = RowHullSepa(p, v, 0 if mode == "root" else maxdepth)
        m.includeSepa(sepa, "rowhull", "row-hull cuts for separable concave terms", priority=100000,
                      freq=freq, maxbounddist=1.0, delay=False)
    m.optimize()
    has = m.getNSols() > 0
    return {"name": p.name, "mode": mode, "status": m.getStatus(), "primal": m.getObjVal() if has else math.inf,
            "dual": m.getDualbound(), "nodes": m.getNTotalNodes(), "total_time": time.time() - t0,
            "sepa_cuts": sepa.ncuts if sepa else 0, "sepa_calls": sepa.ncalls if sepa else 0,
            "sepa_time": sepa.time if sepa else 0.0}


if __name__ == "__main__":
    from instances import transport, netflow
    ap = argparse.ArgumentParser()
    ap.add_argument("m"); ap.add_argument("n", type=int); ap.add_argument("seed", type=int)
    ap.add_argument("cap"); ap.add_argument("cost"); ap.add_argument("mode")
    ap.add_argument("--tl", type=float, default=300); ap.add_argument("--maxdepth", type=int, default=1000)
    ap.add_argument("--log", action="store_true")
    a = ap.parse_args()
    p = netflow(int(a.m[1:]), a.n, a.seed, a.cap, a.cost) if a.m.startswith("g") else transport(int(a.m), a.n, a.seed, a.cap, a.cost)
    print(json.dumps(solve(p, a.mode, a.tl, a.maxdepth, a.log)))
