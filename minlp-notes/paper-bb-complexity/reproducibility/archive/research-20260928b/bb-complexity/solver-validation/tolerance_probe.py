"""Feasibility-tolerance probe: python3 tolerance_probe.py FILE.cip (see results/tolerance_probe.log)."""
import sys, time, pyscipopt
fn = sys.argv[1]
for ft, ep in [(1e-6, 1e-9), (1e-9, 1e-12), (1e-10, 1e-13)]:
    for eps in [1e-4, 1e-6, 1e-8]:
        m = pyscipopt.Model(); m.hideOutput(); m.readProblem(fn)
        m.setParam('limits/absgap', eps); m.setParam('limits/gap', 0.0); m.setParam('limits/time', 60)
        m.setParam('numerics/feastol', ft); m.setParam('numerics/epsilon', ep)
        m.setParam('numerics/dualfeastol', min(1e-7, ft))
        t0 = time.time(); m.optimize()
        print(f"ft={ft:g} eps={eps:g} {m.getStatus()} nodes={m.getNNodes()} primal={m.getPrimalbound():.3e} dual={m.getDualbound():.3e} time={time.time()-t0:.1f}", flush=True)
