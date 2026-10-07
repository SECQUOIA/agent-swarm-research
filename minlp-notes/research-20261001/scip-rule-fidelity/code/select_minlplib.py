"""Select a random sample of MINLPLib instances with nonconvex quadratic constraints.

Filter (from sources/minlplib_instancedata.csv): nquadcons >= 1, conscurvature not in
{linear, convex, concave}, no general nonlinear, polynomial or signomial constraints, nvars <= 1000,
OSiL file present.  Sample size and seed from the command line.
Usage: python3 select_minlplib.py SEED N OUT.txt"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import csv, os, sys, random
seed, n, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
here = os.path.dirname(os.path.abspath(__file__))
r = list(csv.DictReader(open(os.path.join(here, '../sources/minlplib_instancedata.csv')), delimiter=';'))
osil = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil')
iv = lambda x, k: int(x[k] or 0)
sel = [x['name'] for x in r if iv(x, 'nquadcons') >= 1 and x['conscurvature'] not in ('linear', 'convex', 'concave')
       and iv(x, 'ngennlcons') == 0 and iv(x, 'npolynomcons') == 0 and iv(x, 'nsignomcons') == 0
       and iv(x, 'nvars') <= 1000 and os.path.exists(os.path.join(osil, x['name'] + '.osil'))]
sel.sort()
random.Random(seed).shuffle(sel)
open(out, 'w').write('\n'.join(sorted(sel[:n])) + '\n')
print(len(sel), 'eligible;', min(n, len(sel)), 'selected ->', out)
