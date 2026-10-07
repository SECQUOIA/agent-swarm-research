"""Re-solve a few probe3 instances with SCIP (default, eps 1e-4) and compare SCIP's
reported primal value with F evaluated at SCIP's x and with the prototype's
certified bounds at eps 1e-6."""
import json, sys
import numpy as np
import instances as I
import chain_bb as CB
out = []
for amp, n, seed in [(0.3, 8, 4), (0.2, 8, 1), (0.3, 6, 1), (0.2, 6, 3)]:
    m, x, t, c = I.build_scip(n, seed, amp=amp)
    m.setParam("timing/clocktype", 1); m.setParam("limits/time", 300)
    m.setParam("limits/absgap", 1e-4); m.setParam("limits/gap", 0.0)
    m.optimize()
    sol = m.getBestSol()
    xs = np.array([m.getSolVal(sol, v) for v in x]); ts = np.array([m.getSolVal(sol, v) for v in t])
    g = xs**2 - I.KAPPA * xs**4; g[:-1] += I.B * xs[:-1] * xs[1:]
    viol = g - ts  # > 0 means t_i below its right-hand side
    r = CB.chain_bb(I.Probe3Chain(c), 1e-6, mode="quad", unary_sub=16)
    rec = dict(amp=amp, n=n, seed=seed, scip_primal=m.getPrimalbound(), F_at_scip_x=I.F(xs, c),
               max_t_violation=float(viol.max()), sum_t_violation=float(viol.sum()),
               proto_LB=r["LB"], proto_UB=r["UB"])
    out.append(rec); print(json.dumps(rec), flush=True)
