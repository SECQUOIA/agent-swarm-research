"""When does SCIP 10.0.3 generate minor intersection cuts?  (note, Section 2)

1. Default parameter values (PySCIPOpt 6.2.1, SCIP 10.0).
2. A random 3x3 bipartite bilinear model solved at the root with PySCIPOpt (bundled SCIP has Ipopt):
   separator statistics of interminor/minor with defaults and with separating/interminor/freq = 0.
3. The same model (written as CIP) with the local binary $HOME/build-scip/build-suite/bin/scip
   (built with IPOPT=OFF) and separating/interminor/freq = 0.
Usage: python3 scip_probe.py   (writes probe files to /tmp/minor_probe)
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import os
import re
import subprocess
import numpy as np
import pyscipopt as ps

D = '/tmp/minor_probe'
os.makedirs(D, exist_ok=True)
BIN = (_PUBLIC_HOME + '/build-scip/build-suite/bin/scip')

m = ps.Model()
for p in ('separating/interminor/freq', 'separating/interminor/maxrounds', 'separating/interminor/maxroundsroot',
          'separating/interminor/usestrengthening', 'separating/interminor/usebounds', 'separating/interminor/mincutviol',
          'separating/minor/freq', 'nlhdlr/quadratic/useintersectioncuts', 'nlhdlr/quadratic/usestrengthening'):
    print('default %-45s = %s' % (p, m.getParam(p)))


def build():
    rng = np.random.default_rng(0)
    p, q = 3, 3
    m = ps.Model()
    m.hideOutput()
    x = [m.addVar('x%d' % i, lb=rng.uniform(-2, 0), ub=rng.uniform(0.5, 2)) for i in range(p)]
    y = [m.addVar('y%d' % k, lb=rng.uniform(-2, 0), ub=rng.uniform(0.5, 2)) for k in range(q)]
    E = rng.normal(size=(p, q))
    m.addCons(ps.quicksum(E[i, k] * x[i] * y[k] for i in range(p) for k in range(q))
              + ps.quicksum(rng.normal() * v for v in x + y) <= 0.5)
    m.addCons(ps.quicksum(rng.normal() * x[i] * y[k] for i in range(p) for k in range(q)) >= -1)
    m.setObjective(ps.quicksum(rng.normal() * v for v in x + y))
    return m


def seplines(txt):
    return [l for l in txt.splitlines() if re.match(r'\s*(interminor|minor)\s*:', l)]


hdr = 'Separators: ExecTime SetupTime Calls RootCalls Cutoffs DomReds FoundCuts ViaPoolAdd DirectAdd Applied ...'
for mode in ('default', 'interminor freq 0'):
    m = build()
    if mode != 'default':
        m.setParam('separating/interminor/freq', 0)
    m.setParam('limits/nodes', 1)
    m.optimize()
    f = os.path.join(D, 'stats_%s.txt' % mode.replace(' ', '_'))
    m.printStatistics(f)
    print('PySCIPOpt, %s: dual bound %.8f' % (mode, m.getDualbound()))
    print('  ' + hdr)
    for l in seplines(open(f).read()):
        print('  ' + l)
build().writeProblem(os.path.join(D, 'probe.cip'))
out = subprocess.run([BIN, '-c', 'read %s set separating interminor freq 0 set limits nodes 1 optimize display statistics quit'
                      % os.path.join(D, 'probe.cip')], capture_output=True, text=True).stdout
print('local binary (IPOPT=OFF), interminor freq 0:')
print('  ' + hdr)
for l in seplines(out):
    print('  ' + l)
print('  external libraries line mentioning Ipopt:', [l.strip() for l in out.splitlines() if 'Ipopt' in l] or 'none')
