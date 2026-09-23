"""Concave-cost facility sizing: the concave terms sit on the facility throughputs y_i = sum_j x_ij,
and the only row that links them, sum_i y_i = total demand, is an AGGREGATE of the demand rows that
the model does not contain.  Cuts are separated on that implied row (and on the model rows) and
handed to the solver on the original model.

python facility.py out.jsonl --sizes 10x30 --seeds 0 1 2 --costs log quad --ratios 0.1 0.5 --solver gurobi --tl 300
"""
import argparse, json, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
from sob.functions import X, Univariate, Piece
from sob.model import SeparableProblem, original_ir
from sob.backends import SOLVERS
from rowhull.strengthen import cut_loop, cut_ir


def facility(m, n, seed, cost="log", ratio=0.3, aggregate=False):
    """m facilities (capacity U_i), n customers (demand d_j); variables y_0..y_{m-1}, then x_ij.
    ratio scales the linear transport costs against the concave facility costs."""
    rng = np.random.default_rng(seed)
    d = np.round(rng.uniform(1, 5, n), 2)
    D = float(d.sum())
    U = np.round(rng.uniform(0.15, 0.45, m) * D, 2)            # about a third of the facilities are needed
    assert U.sum() > 1.3 * D
    funcs = []
    for i in range(m):
        a = rng.uniform(5, 10) * U[i] ** 0.5
        if cost == "log":
            expr = sp.Float(a) * sp.log(1 + sp.Float(4.0 / U[i]) * X)
        elif cost == "quad":
            expr = sp.Float(a * 2 / U[i]) * X - sp.Float(a / U[i] ** 2) * X**2
        else:
            expr = sp.Float(a / U[i] ** 0.5) * sp.sqrt(X)
        funcs.append(Univariate(expr, 0.0, float(U[i]), pieces=[Piece(0.0, float(U[i]), True, expr)]))
    pos_f, pos_c = rng.uniform(0, 1, (m, 2)), rng.uniform(0, 1, (n, 2))
    for i in range(m):
        for j in range(n):
            c = ratio * 10 * float(np.linalg.norm(pos_f[i] - pos_c[j]))
            ub = float(min(U[i], d[j]))
            expr = sp.Float(c) * X
            funcs.append(Univariate(expr, 0.0, ub, pieces=[Piece(0.0, ub, False, expr)]))
    N = m + m * n
    rows, sense, b = [], [], []
    for i in range(m):                                        # y_i - sum_j x_ij = 0
        r = np.zeros(N); r[i] = 1.0; r[m + i * n: m + (i + 1) * n] = -1.0
        rows.append(r); sense.append("=="); b.append(0.0)
    for j in range(n):                                        # sum_i x_ij = d_j
        r = np.zeros(N); r[m + j: m + m * n: n] = 1.0
        rows.append(r); sense.append("=="); b.append(float(d[j]))
    if aggregate:                                             # implied: sum_i y_i = D
        r = np.zeros(N); r[:m] = 1.0
        rows.append(r); sense.append("=="); b.append(D)
    return SeparableProblem(f"facility-{cost}-r{ratio}-{m}x{n}-s{seed}", funcs, np.array(rows), sense, np.array(b))


def cell(args):
    m, n, seed, cost, ratio, form, solver, tl = args
    p = facility(m, n, seed, cost, ratio)
    rec = {"name": p.name, "form": form, "solver": solver, "tl": tl}
    t0 = time.time()
    if form == "orig":
        ir = original_ir(p)
    else:
        q = facility(m, n, seed, cost, ratio, aggregate=(form == "cuts_agg"))
        cuts, extra, info = cut_loop(q)
        rec["cutinfo"] = info
        ir = cut_ir(p, cuts, extra)            # cuts on the ORIGINAL model (no extra row)
    res = SOLVERS[solver](ir, max(tl - (time.time() - t0), 1.0), threads=4)
    res.pop("x", None); rec.update(res); rec["total_time"] = time.time() - t0
    return json.dumps(rec)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--sizes", nargs="+", default=["10x30"])
    ap.add_argument("--seeds", nargs="+", type=int, default=[0]); ap.add_argument("--costs", nargs="+", default=["log"])
    ap.add_argument("--ratios", nargs="+", type=float, default=[0.3])
    ap.add_argument("--forms", nargs="+", default=["orig", "cuts_rows", "cuts_agg"])
    ap.add_argument("--solver", default="gurobi"); ap.add_argument("--tl", type=float, default=300)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    cells = [(int(s.split("x")[0]), int(s.split("x")[1]), sd, c, r, f, a.solver, a.tl)
             for s in a.sizes for sd in a.seeds for c in a.costs for r in a.ratios for f in a.forms]
    with ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as fh:
        for line in ex.map(cell, cells):
            fh.write(line + "\n"); fh.flush()
            r = json.loads(line); ci = r.get("cutinfo", {})
            print(r["name"], r["form"], r["status"], "primal %.3f dual %.3f nodes %d time %.1f" % (r["primal"], r["dual"], r["nodes"], r["total_time"]),
                  ("| LP %.3f -> %.3f, %d cuts, %.1fs" % (ci["bound0"], ci["bound"], ci["ncuts"], ci["time"])) if ci else "", flush=True)
