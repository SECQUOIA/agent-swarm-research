"""Referee SCIP probe (model identical to theory-face-exact/scip_runs.py build()).
1. seed0, kappa=0.1, n=4, absgap 1e-4: node count, primal vs true f*, constraint violations of the incumbent.
2. kappa=0, c=0, n=4/8: node counts with default settings and with the minor / RLT separators disabled.
Usage: python3 scip_probe.py
"""
import sys
import numpy as np
sys.path.insert(0, "../../theory-face-exact")
from scip_runs import build
from adversarial_boxes import Inst


def solve(n, cmode, kappa, eps, tl=60, off=()):
    m = build(n, cmode, kappa)
    m.setParam("limits/time", tl); m.setParam("limits/absgap", eps); m.setParam("limits/gap", 0.0)
    m.setParam("parallel/maxnthreads", 1)
    for p in off:
        m.setParam(p, -1)
    m.optimize()
    return m


def main():
    n = 4
    c0 = np.random.default_rng(0).uniform(-0.3, 0.3, n)
    I = Inst(n, [0.8] * (n - 1), 0.1, c0, 1e-4, 0.5, "seed0")
    m = solve(n, "seed0", 0.1, 1e-4)
    sol = m.getBestSol()
    xs = [v for v in m.getVars() if v.name.startswith("x")]
    ts = [v for v in m.getVars() if v.name.startswith("t")]
    x = np.array([m.getSolVal(sol, v) for v in sorted(xs, key=lambda v: int(v.name[1:]))])
    t = np.array([m.getSolVal(sol, v) for v in sorted(ts, key=lambda v: int(v.name[1:]))])
    expr = x * x - 0.1 * x ** 4
    expr[:-1] += 0.8 * x[:-1] * x[1:]
    print(f"seed0 kappa=0.1 n=4 absgap=1e-4: nodes={m.getNNodes()} status={m.getStatus()} primal={m.getPrimalbound():.9f} "
          f"dual={m.getDualbound():.9f}; true f*={I.fs:.9f}; primal - f* = {m.getPrimalbound() - I.fs:.2e}; "
          f"f(x_incumbent) - f* = {I.f(x) - I.fs:.2e}; t_i - expr_i = {np.round(t - expr, 9)}")
    for n in (4, 8):
        for off in ((), ("separating/minor/freq",), ("separating/rlt/freq",), ("separating/minor/freq", "separating/rlt/freq")):
            m = solve(n, "zero", 0.0, 1e-4, off=off)
            print(f"kappa=0 c=0 n={n} off={list(off) or 'none'}: nodes={m.getNNodes()} status={m.getStatus()} "
                  f"primal={m.getPrimalbound():.2e} dual={m.getDualbound():.2e} time={m.getSolvingTime():.1f}s", flush=True)


if __name__ == "__main__":
    main()
