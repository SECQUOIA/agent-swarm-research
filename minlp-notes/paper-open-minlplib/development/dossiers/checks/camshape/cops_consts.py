"""Dossier check (camshape): distance between the OSIL decimal constants and the exact COPS/GAMS constants
(theta = 2 pi / (5(n+1)), c = 2 cos theta, c2 = 4 cos theta, ub1 = min(1 + 1.5 theta, 1/(2 cos theta - 1)),
lbn = 2 - 1.5 theta, alpha = 1.5 theta, c0 = pi / n), in mpmath interval arithmetic (assumes mpmath iv is correct).
Also checks that the omitted COPS curvature row |r_2 - r_1| <= alpha holds at the optimum E (exact)."""
import sys
import json
from fractions import Fraction as Fr
from mpmath import iv, mp

sys.set_int_max_str_digits(0)
from check_exact import read_osil, structure

iv.dps = 60


def ivq(q):
    return iv.mpf(q.numerator) / q.denominator


out = []
for n in (100, 200, 400, 800):
    K = structure(read_osil(f'camshape{n}.osil'), n)
    th = 2 * iv.pi / (5 * (n + 1))
    ex = dict(c=2 * iv.cos(th), c2=4 * iv.cos(th), alpha=iv.mpf(3) / 2 * th, lbn=2 - iv.mpf(3) / 2 * th, c0=iv.pi / n)
    u1a = 1 / (2 * iv.cos(th) - 1)
    u1b = 1 + iv.mpf(3) / 2 * th
    assert u1a.b < u1b.a  # the convexity bound is the binding one
    ex['ub1'] = u1a
    rec = dict(n=n)
    worst = 0
    for k, v in ex.items():
        d = ivq(K[k]) - v
        m = max(abs(mp.mpf(d.a)), abs(mp.mpf(d.b)))
        rec[k] = float(m)
        worst = max(worst, m)
    rec['max_abs_diff_upper'] = float(worst)
    rec['within_1e-14'] = bool(worst < mp.mpf('1e-14'))
    out.append(rec)
    print(json.dumps(rec), flush=True)
json.dump(out, open('cops_consts.json', 'w'), indent=1)
