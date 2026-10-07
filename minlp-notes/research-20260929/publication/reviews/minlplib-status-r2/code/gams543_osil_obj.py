"""Review r2: does GAMS 54.3's OSiL rendering of methanol50.gms carry the exact .gms objective? (own code)"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import sys, sympy as sp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import exactcmp as X
G = (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl/gms/methanol50.gms')
for O in [(_PUBLIC_REPO + '/research-20260929/publication/minlplib-status/pages/canon/methanol50/current/methanol50.osil'),
          (_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/conv/methanol50.cur/out.osil')]:
    eqs, ov, _ = X.read_gms(G)
    _, og = X.gms_objective(eqs, ov)
    rows, oo, _, _, _ = X.read_osil(O)
    d = sp.expand(og - oo)
    print(O.split('research-20260929/')[1], 'objective difference .gms - GAMS54.3 OSiL expands to', d if d == 0 else ('nonzero, terms: %d' % len(d.as_ordered_terms())))
