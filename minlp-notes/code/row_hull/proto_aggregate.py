"""Prototype: row hulls of aggregated rows (node-set cut rows) on transportation instances.
Root bounds only.  Aggregations: single nodes (the model rows), pairs of sources, pairs of sinks,
source-sink pairs, optionally triples of sources."""
import sys, itertools, time
from pathlib import Path
import numpy as np
import gurobipy as gp

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
from instances import transport
from rowhull.rows import normalize_row
from rowhull.closedform import closed_form_rows
from rowhull.strengthen import root_lp, is_concave, cut_loop


def agg_row(p, m, n, S, D):
    """Row of the node set (sources S, sinks D): sum_{i in S, j notin D} x_ij - sum_{i notin S, j in D} x_ij = s(S) - d(D)."""
    entries, rhs = [], sum(p.b[i] for i in S) - sum(p.b[m + j] for j in D)
    for i in range(m):
        for j in range(n):
            a = (1.0 if i in S else 0.0) - (1.0 if j in D else 0.0)
            if a != 0.0:
                f = p.funcs[i * n + j]
                entries.append((f"x{i*n+j}", a, f.lo, f.hi, f"w{i*n+j}", f._f))
    return normalize_row(entries, "==", rhs)


def bound_with(p, m, n, sets):
    M, v = root_lp(p)
    used = 0
    for q, (S, D) in enumerate(sets):
        row = agg_row(p, m, n, set(S), set(D))
        if row is None:
            continue
        out = closed_form_rows(row, f"a{q}")
        if out is None:
            continue
        used += 1
        for k, (lb, ub, _t) in out[0].items():
            v[k] = M.addVar(lb=lb, ub=ub)
        M.update()
        for rowd, sn, rhs in out[1]:
            lhs = gp.quicksum(c * v[k] for k, c in rowd.items())
            M.addConstr(lhs <= rhs if sn == "<=" else lhs >= rhs if sn == ">=" else lhs == rhs)
    M.optimize()
    return M.ObjVal, used


if __name__ == "__main__":
    m, n, cost = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    best_known = {}
    for seed in range(int(sys.argv[4])):
        p = transport(m, n, seed, "uniform", cost)
        singles = [((i,), ()) for i in range(m)] + [((), (j,)) for j in range(n)]
        pairs = [(c, ()) for c in itertools.combinations(range(m), 2)] + \
                [((), c) for c in itertools.combinations(range(n), 2)] + \
                [((i,), (j,)) for i in range(m) for j in range(n)]
        triples = [(c, ()) for c in itertools.combinations(range(m), 3)] + [((), c) for c in itertools.combinations(range(n), 3)]
        M0, _ = root_lp(p); M0.optimize()
        t0 = time.time(); b1, u1 = bound_with(p, m, n, singles)
        b2, u2 = bound_with(p, m, n, singles + pairs); t2 = time.time() - t0
        b3, u3 = bound_with(p, m, n, singles + pairs + triples)
        print(f"{p.name}: termwise {M0.ObjVal:.4f} | rows {b1:.4f} ({u1}) | +pairs {b2:.4f} ({u2}) | +triples {b3:.4f} ({u3})", flush=True)
