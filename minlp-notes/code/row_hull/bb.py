"""A minimal spatial branch-and-bound to compare node counts (not times) of three relaxations:

  T  term-wise chords on the node box,
  R  T plus the row-hull cuts generated once at the root,
  L  T plus row-hull separation on the node box at every node (children inherit the cuts).

Best-bound search; branch on the variable with the largest chord gap at the node solution, at that
solution value (kept 10% away from the node bounds).  Relative gap 1e-4.
"""
import heapq, itertools, sys, time
from pathlib import Path

import numpy as np
import gurobipy as gp
from gurobipy import GRB

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
from instances import transport, netflow
from rowhull.rows import normalize_row
from rowhull.separate import RowSeparator, cut_to_model
from rowhull.strengthen import _row_point, clean_cut
from rowhull.closedform import closed_form_rows


class Node:
    __slots__ = ("lo", "hi", "cuts", "bound")

    def __init__(self, lo, hi, cuts, bound):
        self.lo, self.hi, self.cuts, self.bound = lo, hi, cuts, bound


def node_rows(p, lo, hi):
    rows = []
    for r in range(p.A.shape[0]):
        entries = [(f"x{i}", p.A[r, i], lo[i], hi[i], f"w{i}", p.funcs[i]._f)
                   for i in range(p.n) if p.A[r, i] != 0.0]
        row = normalize_row(entries, p.sense[r], float(p.b[r]))
        if row is not None and row.n <= 63:
            rows.append(row)
    return rows


def solve_node(p, node, mode, max_rounds=30):
    n = p.n
    m = gp.Model(); m.Params.OutputFlag = 0
    x = [m.addVar(lb=node.lo[i], ub=node.hi[i]) for i in range(n)]
    w = [m.addVar(lb=-GRB.INFINITY, obj=1.0) for _ in range(n)]
    v = {**{f"x{i}": x[i] for i in range(n)}, **{f"w{i}": w[i] for i in range(n)}}
    for i, f in enumerate(p.funcs):
        a, b = node.lo[i], node.hi[i]
        if b - a > 1e-12:
            m.addConstr(w[i] >= f(a) + (f(b) - f(a)) / (b - a) * (x[i] - a))
        else:
            m.addConstr(w[i] >= f(a))
    for r in range(p.A.shape[0]):
        m.addConstr(gp.quicksum(p.A[r, i] * x[i] for i in range(n) if p.A[r, i] != 0.0) == p.b[r])
    for coefs, rhs in node.cuts:
        m.addConstr(gp.quicksum(c * v[k] for k, c in coefs.items()) >= rhs)
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        return None, None, node.cuts
    cuts = list(node.cuts)
    if mode == "L":
        rows = node_rows(p, node.lo, node.hi)
        seps = [RowSeparator(row, 2000) for row in rows]
        bounds_of = {k: (var.LB, var.UB) for k, var in v.items()}
        for _ in range(max_rounds):
            val = {k: var.X for k, var in v.items()}
            new = 0
            for row, sep in zip(rows, seps):
                zhat, tp = _row_point(row, val)
                cut = sep.separate(zhat, tp, 1e-5)
                if cut is None:
                    continue
                cc = clean_cut(*cut_to_model(row, cut), bounds_of)
                if cc is None:
                    continue
                m.addConstr(gp.quicksum(c * v[k] for k, c in cc[0].items()) >= cc[1])
                cuts.append(cc); new += 1
            if new == 0:
                break
            m.optimize()
            if m.Status != GRB.OPTIMAL:
                return None, None, cuts
    xs = np.array([xi.X for xi in x])
    # keep only cuts that are tight at the node optimum (children re-separate anyway)
    return m.ObjVal, xs, cuts


def bb(p, mode, gap=1e-4, max_nodes=200000, tl=1800):
    t0 = time.time()
    lo = np.array([f.lo for f in p.funcs]); hi = np.array([f.hi for f in p.funcs])
    root = Node(lo, hi, [], -np.inf)
    rootmode = "L" if mode in ("R", "L") else mode        # modes other than T/R/L are handled by wrappers
    ub, nodes, cnt = np.inf, 0, itertools.count()
    heap = []
    bound, xs, cuts = solve_node(p, root, rootmode)
    root.bound, root.cuts = bound, cuts
    heapq.heappush(heap, (bound, next(cnt), root, xs))
    rootbound = bound
    while heap and nodes < max_nodes and time.time() - t0 < tl:
        bound, _, node, xs = heapq.heappop(heap)
        if bound >= ub - gap * max(1.0, abs(ub)):
            break
        nodes += 1
        true = np.array([p.funcs[i](xs[i]) for i in range(p.n)])
        val = true.sum()
        ub = min(ub, val)
        a, b = node.lo, node.hi
        chord = np.array([p.funcs[i](a[i]) + (p.funcs[i](b[i]) - p.funcs[i](a[i])) / (b[i] - a[i]) * (xs[i] - a[i])
                          if b[i] - a[i] > 1e-12 else true[i] for i in range(p.n)])
        i = int(np.argmax(true - chord))
        if true[i] - chord[i] <= 1e-9:
            continue
        theta = min(max(xs[i], a[i] + 0.1 * (b[i] - a[i])), b[i] - 0.1 * (b[i] - a[i]))
        for side in (0, 1):
            lo2, hi2 = a.copy(), b.copy()
            if side == 0: hi2[i] = theta
            else: lo2[i] = theta
            child = Node(lo2, hi2, node.cuts, bound)
            cb, cx, ccuts = solve_node(p, child, "T" if mode in ("T", "R") else mode)
            if cb is None or cb >= ub - gap * max(1.0, abs(ub)):
                if cb is not None:
                    ub = min(ub, sum(p.funcs[k](cx[k]) for k in range(p.n)))
                continue
            child.bound, child.cuts = cb, ccuts
            heapq.heappush(heap, (cb, next(cnt), child, cx))
    lb = min([ub] + [h[0] for h in heap])
    return {"mode": mode, "nodes": nodes, "ub": ub, "lb": lb, "root": rootbound, "time": time.time() - t0,
            "done": not heap or heap[0][0] >= ub - gap * max(1.0, abs(ub))}


if __name__ == "__main__":
    m, n, cap, cost, seeds = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5])
    for seed in range(seeds):
        p = transport(m, n, seed, cap, cost)
        out = [bb(p, mode) for mode in ("T", "R", "L")]
        print(p.name, " | ".join(f"{o['mode']}: nodes {o['nodes']} root {o['root']:.4f} ub {o['ub']:.4f} "
                                 f"{'done' if o['done'] else 'LIMIT'} {o['time']:.0f}s" for o in out), flush=True)
