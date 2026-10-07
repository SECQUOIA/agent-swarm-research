"""Dossier check (camshape): the omitted COPS curvature row |r_2 - r_1| <= alpha at the optimum E and at the
'hi' corner envelope used by robust.py (c + eta, ub1 - eta, alpha - eta), exact Fractions."""
import sys, json
from fractions import Fraction as Fr
sys.set_int_max_str_digits(0)
from check_exact import read_osil, structure, certificate
eta = Fr(1, 10**14)
out = []
for n in map(int, sys.argv[1:]):
    K = structure(read_osil(f'camshape{n}.osil'), n)
    hi = dict(c=K['c'] + eta, ub1=K['ub1'] - eta, alpha=K['alpha'] - eta)
    E = certificate(hi, n)['E']
    d = abs(E[2] - E[1])
    rec = dict(n=n, hi_E2_minus_E1=float(d), alpha_minus=float(hi['alpha']), ok=bool(d <= hi['alpha']),
               E1_ge_1_minus_alpha=bool(E[1] >= 1 - hi['alpha']))
    print(json.dumps(rec), flush=True); out.append(rec)
json.dump(out, open('omitted_row_hi.json', 'w'), indent=1)
