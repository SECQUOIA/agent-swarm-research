"""Certified relaxation bounds: grid LP (inner estimate) seeds Dantzig-Wolfe with exact pricing,
whose Lagrangian bound is a valid lower bound on the relaxation value and hence on the optimum."""
import sys, json, time
import numpy as np
import instance as I
import gridrelax as GR

if __name__ == "__main__":
    path = sys.argv[1]; modes = sys.argv[2].split(","); G = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    tlim = float(sys.argv[4]) if len(sys.argv) > 4 else 3600
    if path.endswith(".osil"):
        import spp; P = spp.SppInst(path)
    else:
        P = I.Inst(path)
    grid = np.unique(np.concatenate([np.linspace(0, 1, G), np.geomspace(1e-3, 0.05, 6)]))
    for mode in modes:
        t0 = time.time()
        m, blocks = GR.build(P, mode, grid)
        m.Params.Threads = 4; m.Params.Method = 2; m.Params.Crossover = 0
        m.optimize(); gval = m.ObjVal
        pts = GR.grid_points(blocks)
        print(json.dumps(dict(name=P.name, mode=mode, grid_value=gval, grid_time=time.time() - t0)), flush=True)
        r = I.solve_relax(P, mode, tlim=tlim, extra=pts, maxit=100000)
        r["grid_value"] = gval
        print("CERTRESULT", json.dumps({"name": P.name, **r}), flush=True)
