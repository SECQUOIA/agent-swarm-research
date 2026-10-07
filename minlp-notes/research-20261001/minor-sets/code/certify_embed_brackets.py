"""Exact brackets for the orbit bound of the three certified bilinear instances of the sfree note,
embedded as minor corners (note, Corollary 7; revision after review round 2).

The sfree note certifies only the strict gap z_A < z_K for its Theorem 14, its second rational
instance (Section 8.5) and its Proposition 16; its values 0.97539, 0.83477, 0.98385 are numerical.
Here each instance is embedded as in Corollary 7 (apex (w, x, y, 1), rays (p_w, p_x, p_y, 0) in the
coordinates (a, b, c, d) of M = [[w, x], [y, h]]), and the following are checked in exact rational
arithmetic:
  - min of det over T* = conv{sbar, v1, v2, v3} is 0, attained only at t*,
    and t* is a convex combination of v1, v2, v3 with ray cost 1, so z_K = 1;
  - lower bound: a rational F^T whose set C_F contains T_{z_lo} (so z_orbit >= z_lo);
  - upper bound: rational positive definite Y_v with sum_v tr(G V Y_v) = 0 for the orbit basis
    (note, Prop. 4), so z_orbit <= z_up.
By Corollary 7 the orbit bound of the embedded corner equals the sfree family-(A) bound z_A.
Finally it checks that the certified orbit upper bounds of the minor instances A and S1
(9/20 and 779/1000, note Theorems 8 and 9) are below every z_lo found here.
Usage: python3 certify_embed_brackets.py
"""
from fractions import Fraction as Fr

import numpy as np

import exact_tools as ex
from cert_lib import Checker
from minor_core import FamilySolver, precondition

# sfree data in its coordinates (x, y, w); S = {w <= xy}; w = (1, 1, 1)
INST = {
    'Thm14': {'sbar': ('-9/2', '0', '3/2'), 'v': [('-1', '-6', '18'), ('-5', '6', '-18'), ('0', '5/2', '5/2')],
              't0': ('-3', '0', '0'), 'lambda': ('1/2', '1/2', '0')},
    'second': {'sbar': ('-1/2', '1/2', '1'), 'v': [('1/2', '-4', '-1/2'), ('-10', '3', '24'), ('9/2', '1/2', '15/2')],
               't0': ('-1', '-3', '3'), 'lambda': ('6/7', '1/7', '0')},
    'Prop16': {'sbar': ('-2', '3', '2'), 'v': [('0', '0', '0'), ('6', '-2', '1/4'), ('1', '-5/2', '1/2')],
               't0': ('0', '0', '0'), 'lambda': ('1', '0', '0')},
}
MINOR_UPPER = {'A (Thm 8)': Fr(9, 20), 'S1 (Thm 9)': Fr(779, 1000)}


def embed(p, h):
    x, y, w = (Fr(t) for t in p)
    return (w, x, y, Fr(h))


chk = Checker()
lows = {}
for name, d in INST.items():
    sb = embed(d['sbar'], 1)
    vs = [embed(v, 1) for v in d['v']]
    t0 = embed(d['t0'], 1)
    P = [ex.add(v, sb, 1, -1) for v in vs]          # last coordinate 0
    w = [Fr(1)] * 3
    print('== %s: sbar = %s, t* = %s' % (name, [str(x) for x in sb], [str(x) for x in t0]), flush=True)
    chk('%s: det(sbar) = %s > 0' % (name, ex.det4(sb)), ex.det4(sb) > 0)
    m, arg = ex.min_det_over_simplex([sb] + vs)
    chk('%s: min over T* of det = %s, attained only at t*' % (name, m),
        m == 0 and len({a[3] for a in arg}) == 1 and arg[0][3] == t0)
    lam = tuple(Fr(x) for x in d['lambda'])
    chk('%s: t* = sbar + P lambda, lambda = %s >= 0, cost = 1 (so z_K = 1)' %
        (name, [str(x) for x in lam]),
        all(x >= 0 for x in lam) and ex.dot(w, lam) == 1
        and tuple(sb[i] + sum(lam[j] * P[j][i] for j in range(3)) for i in range(4)) == t0)
    sbn = np.array([float(x) for x in sb])
    Pn = np.array([[float(P[j][i]) for j in range(3)] for i in range(4)])
    sI, PI = precondition(sbn, Pn)
    c_, h_, _ = FamilySolver('orbit', sI, PI, np.ones(3)).best(1.0, iters=45)
    lo = up = None
    for dl in (1e-7, 1e-6, 1e-5, 1e-4, 1e-3):
        zl = Fr(int(np.floor((c_ - dl) * 10 ** 7)), 10 ** 7)
        ok, FT = ex.lower_certificate(ex.ORBIT_BASIS, sb, P, w, zl)
        if ok:
            lo = zl
            print('   lower F^T at z = %s:' % lo, [[str(x) for x in row] for row in FT], flush=True)
            break
    for du in (1e-7, 1e-6, 1e-5, 1e-4, 1e-3):
        zu = min(Fr(int(np.ceil((h_ + du) * 10 ** 7)), 10 ** 7), Fr(1))
        ok, Ys = ex.upper_certificate(ex.ORBIT_BASIS, sb, P, w, zu) if zu < 1 else (False, None)
        if ok:
            up = zu
            print('   upper Y_v at z = %s (sbar, then vertices of T_z):' % up,
                  [[[str(x) for x in row] for row in Y] for Y in Ys], flush=True)
            break
    print('   orbit numerical %.8f; exact bracket [%s, %s]' % (
        c_, '%.7f' % float(lo) if lo is not None else 'none', '%.7f' % float(up) if up is not None else 'none'),
        flush=True)
    chk('%s: exact orbit bracket found, z_lo = %s, z_up = %s < 1' % (name, lo, up),
        lo is not None and up is not None and lo <= up < 1)
    lows[name] = lo

if all(v is not None for v in lows.values()):
    mlo = min(lows.values())
    mup = max(MINOR_UPPER.values())
    chk('comparison: certified upper bounds for selected minor instances %s are below the smallest bilinear lower bound %.7f'
        % ({k: str(v) for k, v in MINOR_UPPER.items()}, float(mlo)), mup < mlo)
print('ALL PASS' if chk.ok else 'SOME CHECK FAILED')
raise SystemExit(0 if chk.ok else 1)
