"""Fairness control for Gurobi on quadratic costs: state the concave quadratic directly in the
objective (nonconvex QP) instead of through epigraph variables.
python run_objform.py out.jsonl --sizes 8x12 10x15 --caps uniform random uncap --seeds 0 1 2 3 4 --tl 300 --workers 8"""
import argparse, json, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))


def cell(args):
    size, cap, seed, tl = args
    import gurobipy as gp
    import sympy as sp
    from instances import transport, netflow
    from sob.functions import X
    t0 = time.time()
    if size.startswith("g"):
        a, b = size[1:].split("d")[0].split("n"); p = netflow(int(a), int(b), seed, cap, "quad")
    else:
        a, b = size.split("x"); p = transport(int(a), int(b), seed, cap, "quad")
    m = gp.Model(); m.Params.OutputFlag = 0; m.Params.TimeLimit = tl; m.Params.Threads = 4
    m.Params.MIPGap = 1e-4; m.Params.NonConvex = 2
    x = [m.addVar(lb=f.lo, ub=f.hi) for f in p.funcs]
    obj = gp.QuadExpr()
    for xi, f in zip(x, p.funcs):
        c2, c1, c0 = [float(c) for c in sp.Poly(f.expr, X).all_coeffs()]
        obj += c2 * xi * xi + c1 * xi + c0
    m.setObjective(obj)
    for r in range(p.A.shape[0]):
        m.addConstr(gp.quicksum(p.A[r, i] * x[i] for i in range(p.n) if p.A[r, i] != 0.0) == p.b[r])
    m.optimize()
    return json.dumps({"name": p.name, "form": "objform", "solver": "gurobi", "tl": tl,
                       "status": {2: "optimal", 9: "timelimit"}.get(m.Status, str(m.Status)),
                       "primal": m.ObjVal if m.SolCount else float("inf"), "dual": m.ObjBound,
                       "nodes": m.NodeCount, "total_time": time.time() - t0})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--sizes", nargs="+"); ap.add_argument("--caps", nargs="+")
    ap.add_argument("--seeds", nargs="+", type=int); ap.add_argument("--tl", type=float, default=300)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    cells = [(s, c, sd, a.tl) for s in a.sizes for c in a.caps for sd in a.seeds
             if not (s.startswith("g") and c == "uncap")]
    with ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as fh:
        for line in ex.map(cell, cells):
            fh.write(line + "\n"); fh.flush()
