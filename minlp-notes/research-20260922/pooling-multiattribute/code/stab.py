"""Dantzig-Wolfe with Wentges dual smoothing and explicit Lagrangian bounds.

L(pi) = LP_PQ(c - sum_b pi_b E_b) + sum_b min_{p in S_b} pi_b . p is a valid lower bound for
any pi (|pi| <= M, the penalty on the linking slacks). Pricing is exact (Block.minimize), so
every reported bound is valid up to floating-point LP tolerances."""
import sys, json, time
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import instance as I
import gridrelax as GR


def coef_rows(b, nvar):
    rows = []
    for c in b.coords:
        e = gp.LinExpr(c); idx = np.array([e.getVar(k).index for k in range(e.size())], int)
        val = np.array([e.getCoeff(k) for k in range(e.size())]); rows.append((idx, val))
    return rows


def run(P, mode, grid_pts=None, tlim=3600, M=1e3, alpha=0.7, rtol=1e-4, log=True):
    vars_ = I.build_pq(P); m = vars_[0]
    m.optimize(); zpq = m.ObjVal
    pq2 = I.build_pq(P)[0]; v2 = pq2.getVars(); c0 = np.array(pq2.getAttr("Obj", v2)); nvar = len(v2)
    blocks = []
    for (l, j) in P.LJ:
        if mode in ("L1", "D1"):
            for a in P.attrs[j]: blocks.append(I.Block(P, vars_, l, j, mode, a))
        else:
            blocks.append(I.Block(P, vars_, l, j, mode))
    rows = [coef_rows(b, nvar) for b in blocks]
    sol = I.feasible_solution(P, tlim=30)
    for bi, b in enumerate(blocks):
        for r in b.link:
            m.addVar(lb=0, obj=M, column=gp.Column([1.0], [r])); m.addVar(lb=0, obj=M, column=gp.Column([-1.0], [r]))
        b.seed_points(m, sol)
        if grid_pts is not None:
            for p in grid_pts[bi]: b.add_col(m, p)
    t0 = time.time(); best = -np.inf; center = None; it = 0
    while time.time() - t0 < tlim:
        it += 1
        m.optimize(); zm = m.ObjVal
        pim = [np.array([c.Pi for c in b.link]) for b in blocks]
        pis = pim if center is None else [alpha * cc + (1 - alpha) * pp for cc, pp in zip(center, pim)]
        pis = [np.clip(p, -M, M) for p in pis]
        # Lagrangian at the smoothed duals
        mod = np.zeros(nvar); pricesum = 0.0; nadd = 0
        for b, rw, pi, pm_ in zip(blocks, rows, pis, pim):
            for (idx, val), pr in zip(rw, pi):
                np.add.at(mod, idx, pr * val)
            sc = max(1e-12, np.abs(pi).max())
            ub, lb, p = b.minimize(list(pi / sc))
            pricesum += sc * lb
            if p is not None and float(pm_ @ np.array(p)) - b.conv.Pi < -1e-6 * max(1.0, abs(zm)):
                b.add_col(m, p); nadd += 1
        pq2.setAttr("Obj", v2, list(c0 - mod)); pq2.optimize()
        L = pq2.ObjVal + pricesum
        if L > best:
            best, center = L, pis
        if log:
            print(f"  [{mode}] it {it} master {zm:.6f} lagr {L:.6f} best {best:.6f} cols+ {nadd}", flush=True)
        if zm - best <= rtol * max(1.0, abs(zm)):
            break
        if nadd == 0:  # misprice at smoothed point: fall back to master duals once
            center = pim
    m.optimize()
    return dict(mode=mode, lb=best, ub=m.ObjVal, it=it, blocks=len(blocks), time=time.time() - t0, zpq=zpq)


if __name__ == "__main__":
    path = sys.argv[1]; mode = sys.argv[2]; G = int(sys.argv[3]); tlim = float(sys.argv[4])
    if path.endswith(".osil"):
        import spp; P = spp.SppInst(path)
    else:
        P = I.Inst(path)
    pts = None
    if G > 0:
        grid = np.unique(np.concatenate([np.linspace(0, 1, G), np.geomspace(1e-3, 0.05, 6)]))
        gm, gb = GR.build(P, mode, grid); gm.Params.Threads = 4; gm.Params.Method = 2; gm.Params.Crossover = 0
        gm.optimize(); print(json.dumps(dict(grid_value=gm.ObjVal)), flush=True)
        pts = GR.grid_points(gb)
    r = run(P, mode, pts, tlim=tlim)
    print("STABRESULT", json.dumps({"name": P.name, **r}), flush=True)
