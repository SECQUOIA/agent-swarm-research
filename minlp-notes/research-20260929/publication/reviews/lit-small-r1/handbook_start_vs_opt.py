"""Reviewer check: distance between the handbook GAMS start levels (n.l in the titan files)
and our 50-digit primal points, and objective difference (own OSIL evaluator, 50 digits).
ex6.2.5 sets only phases 1 and 2; phase 3 (vapour) is completed from the mass balance here.
Phases are matched by trying all 6 permutations. Numerical evidence only."""
import os, sys, itertools
from mpmath import mp, mpf
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from osil_eval import Model
mp.dps = 50
OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil')
PRIM = os.path.join(here, '..', '..', '..', 'open-instances-wave2', 'small', 'logs')
hb = {
 'ex6_2_7': {(1,1):'0.00880',(1,2):'0.33595',(1,3):'0.05525',(2,1):'0.00065',(2,2):'0.00193',(2,3):'0.09742',
             (3,1):'0.30803',(3,2):'0.14700',(3,3):'0.04497'},
 'ex6_2_5': {(1,1):'31.459',(1,2):'0.901998',(2,1):'3.10348',(2,2):'0.0000096',(3,1):'26.1669',(3,2):'15.0141'},
}
for name in ['ex6_2_7', 'ex6_2_5']:
    m = Model(os.path.join(OSIL, name + '.osil'))
    ntot = [mpf(m.cons[r]['lb']) for r in range(3)]
    n = {k: mpf(v) for k, v in hb[name].items()}
    for i in (1, 2, 3):
        if (i, 3) not in n:
            n[(i, 3)] = ntot[i - 1] - n[(i, 1)] - n[(i, 2)]
    ours = {}
    for line in open(os.path.join(PRIM, name + '_primal.txt')):
        a, b = line.split(); ours[int(a[1:])] = mpf(b)
    xo = [ours[j] for j in range(2, 11)]
    best = None
    for perm in itertools.permutations(range(3)):
        x = [n[(i, perm[k] + 1)] for i in (1, 2, 3) for k in range(3)]
        d = max(abs(a - b) for a, b in zip(x, xo))
        if best is None or d < best[0]:
            best = (d, perm, x)
    d, perm, x = best
    print(name, 'phase map', perm, ' max|start-ours| =', mp.nstr(d, 4),
          ' f(start) =', mp.nstr(m.objective(x), 16), ' f(ours) =', mp.nstr(m.objective(xo), 20),
          ' f(start)-f(ours) =', mp.nstr(m.objective(x) - m.objective(xo), 3),
          ' viol(start) =', mp.nstr(m.violation(x), 3), ' viol(ours) =', mp.nstr(m.violation(xo), 3))
    print('   per-entry |diff|:', [mp.nstr(abs(a - b), 2) for a, b in zip(x, xo)])
