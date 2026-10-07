"""Referee: effect of SCIP's minor separator on the kappa = 0.1 runs of Section 7.4.
Usage: python3 scip_minor.py cmode eps n1 n2 ...
"""
import sys
from scip_probe import solve
cmode, eps = sys.argv[1], float(sys.argv[2])
for n in [int(a) for a in sys.argv[3:]]:
    for off in ((), ("separating/minor/freq",)):
        m = solve(n, cmode, 0.1, eps, tl=300, off=off)
        print(f"kappa=0.1 {cmode} absgap={eps:.0e} n={n} minor={'off' if off else 'default'}: nodes={m.getNNodes()} "
              f"status={m.getStatus()} primal={m.getPrimalbound():.8f} dual={m.getDualbound():.8f} t={m.getSolvingTime():.1f}s", flush=True)
