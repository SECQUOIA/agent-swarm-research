"""Inner (grid) approximation of PQ + block hulls by disjunctive (Balas) extended formulations.

For a block S = {p : x in [0, XU], p satisfies the pricing constraints with P = x*s}, fixing
x = x_g makes the block a polytope F(x_g). conv(union_g F(x_g)) is an inner approximation of
conv(S) that converges as the grid refines. The block LP rows at x = x_g are read from
Block.pm and homogenized with a weight lambda_g. The resulting LP value is an upper estimate
of the relaxation value (it restricts the hull); the DW Lagrangian bounds in instance.py give
valid lower estimates."""
import sys, json, time
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB
import instance as I


def block_matrices(b, lo, hi):
    pm = b.pm
    b.set_interval(lo, hi); pm.update()
    A = pm.getA().tocsr(); rhs = np.array(pm.getAttr("RHS", pm.getConstrs())); sense = pm.getAttr("Sense", pm.getConstrs())
    lb = np.array(pm.getAttr("LB", pm.getVars())); ub = np.array(pm.getAttr("UB", pm.getVars()))
    return A, rhs, sense, lb, ub


def coord_matrix(b):
    vs = b.pm.getVars(); idx = {v.index: k for k, v in enumerate(vs)}
    C = np.zeros((len(b.pvars), len(vs)))
    for r, e in enumerate(b.pvars):
        if isinstance(e, gp.Var):
            C[r, e.index] = 1.0
        else:
            e = gp.LinExpr(e)
            for k in range(e.size()): C[r, e.getVar(k).index] += e.getCoeff(k)
    return C


def build(P, mode, grid, outer=False):
    """outer=False: slices at the grid points (inner approximation of the hull).
    outer=True: McCormick pieces on consecutive grid intervals; their union covers the whole
    block, so the LP is a valid relaxation (outer approximation of the hull)."""
    vars_ = I.build_pq(P); m = vars_[0]
    blocks = []
    for (l, j) in P.LJ:
        if mode in ("L1", "D1"):
            for a in P.attrs[j]: blocks.append(I.Block(P, vars_, l, j, mode, a, link=False))
        else:
            blocks.append(I.Block(P, vars_, l, j, mode, link=False))
    for b in blocks:
        C = coord_matrix(b)
        xs = b.XU * np.asarray(grid)
        pieces = list(zip(xs[:-1], xs[1:])) if outer else [(x, x) for x in xs]
        lam = m.addMVar(len(pieces), lb=0); m.addConstr(lam.sum() == 1)
        b._grid = (lam, [], C)
        acc = [gp.LinExpr() for _ in range(C.shape[0])]
        tot = None
        for g, (lo, hi) in enumerate(pieces):
            A, rhs, sense, lb, ub = block_matrices(b, lo, hi)
            n = A.shape[1]
            p = m.addMVar(n, lb=-GRB.INFINITY); b._grid[1].append(p)
            # homogenized bounds: lb*lam <= p <= ub*lam (skip infinite)
            fl = np.isfinite(lb); fu = np.isfinite(ub)
            if fl.any(): m.addConstr(p[np.where(fl)[0]] >= lb[fl] * lam[g])
            if fu.any(): m.addConstr(p[np.where(fu)[0]] <= ub[fu] * lam[g])
            for s, op in (("<", "<="), (">", ">="), ("=", "==")):
                rows = [r for r in range(A.shape[0]) if sense[r] == s]
                if not rows: continue
                As = A[rows]; rs = rhs[rows]
                expr = As @ p - rs[:, None] @ lam[g:g+1].reshape(1) if False else None
                lhs = As @ p
                if s == "<": m.addConstr(lhs - lam[g] * rs <= 0)
                elif s == ">": m.addConstr(lhs - lam[g] * rs >= 0)
                else: m.addConstr(lhs - lam[g] * rs == 0)
            Cp = C @ np.eye(n) if False else C
            contrib = Cp @ p
            tot = contrib if tot is None else tot + contrib
        coords = b.coords
        for r in range(C.shape[0]):
            m.addConstr(tot[r] == coords[r])
    return m, blocks


def grid_points(blocks, tol=1e-9):
    """Block points (C p_g / lambda_g) used by the grid LP solution; each is a feasible block point."""
    out = []
    for b in blocks:
        lam, ps, C = b._grid
        L = lam.X; pts = []; agg = np.zeros(C.shape[0])
        for g, p in enumerate(ps):
            agg += C @ p.X
            if L[g] > tol:
                pts.append(list(C @ (p.X / L[g])))
        pts.append(list(agg))  # the block's point in the grid solution: a point of conv(S) up to LP tolerance
        out.append(pts)
    return out


if __name__ == "__main__":
    path = sys.argv[1]; modes = sys.argv[2].split(","); G = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    outer = len(sys.argv) > 4 and sys.argv[4] == "outer"
    if path.endswith(".osil"):
        import spp; P = spp.SppInst(path)
    else:
        P = I.Inst(path)
    # grid: uniform plus refinement near 0
    grid = np.unique(np.concatenate([np.linspace(0, 1, G), np.geomspace(1e-3, 0.05, 6)]))
    for mode in modes:
        t0 = time.time()
        m, blocks = build(P, mode, grid, outer=outer); nb = len(blocks)
        m.Params.Threads = 4; m.Params.Method = 2; m.Params.Crossover = 0
        m.optimize()
        print("GRIDRESULT", json.dumps(dict(name=P.name, mode=mode, grid=len(grid), outer=outer, value=m.ObjVal if m.Status == 2 else None,
                                              status=m.Status, blocks=nb, time=time.time() - t0)), flush=True)
