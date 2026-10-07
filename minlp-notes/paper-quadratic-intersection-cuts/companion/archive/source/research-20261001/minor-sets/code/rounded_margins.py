"""Non-degeneracy margins of the adversarial corners that certify_ratio.py certifies (note, Section 7.3).

certify_ratio.py rounds the vertices sbar, v_1..v_4 of each final adversarial corner to rationals with
denominator <= DEN and certifies the rounded corner.  This script recomputes, independently of
adversarial.py, the margins defined in its docstring (w = 1, rays p_j = v_j - sbar, B the polar form
of det, d = v_1 - v_2):
  ray non-grazing  |B(sbar,p)^2 - det(sbar) det(p)| / (B(sbar,p)^2 + |det(sbar) det(p)|), each ray;
  multipliers      nu_3, nu_4 of the KKT system at the corner minimizer t0 (numerical: t0 is computed
                   with minor_core.zK on the rounded corner);
  second order     det(d) det(sbar) / (B(d,sbar)^2 + det(d) det(sbar))   (-1 if det(d) <= 0);
  apex             det(sbar) / max_j (|det p_j| + |B(sbar,p_j)|).
All margins except the multipliers are computed exactly in rational arithmetic for the rounded corner.
For the float corner the same formulas are compared with the margins logged by adversarial.py.
Usage: python3 rounded_margins.py RECORDS.jsonl [DEN]
"""
import sys
import json
from fractions import Fraction as Fr
import numpy as np
from minor_core import zK


def det(s):
    return s[0] * s[3] - s[1] * s[2]


def polar(s, t):
    # B(s, t) = (det(s + t) - det(s) - det(t)) / 2
    return (det([x + y for x, y in zip(s, t)]) - det(s) - det(t)) / 2


def margins(sb, V, t0):
    P = [[v[i] - sb[i] for i in range(4)] for v in V]
    ds = det(sb)
    m = []
    for p in P:
        B, dp = polar(sb, p), det(p)
        m.append(abs(B * B - ds * dp) / (B * B + abs(ds * dp)))
    g = [float(t0[3]), -float(t0[2]), -float(t0[1]), float(t0[0])]  # gradient of det at t0
    gp = [sum(gi * float(pi) for gi, pi in zip(g, p)) for p in P]
    sig = -1.0 / gp[0]
    m += [1 + sig * gp[2], 1 + sig * gp[3]]
    d = [V[0][i] - V[1][i] for i in range(4)]
    dd, Bd = det(d), polar(d, sb)
    m.append(dd * ds / (Bd * Bd + dd * ds) if dd > 0 else -1)
    m.append(ds / max(abs(det(p)) + abs(polar(sb, p)) for p in P))
    return m


NAMES = ['graze1', 'graze2', 'graze3', 'graze4', 'nu3', 'nu4', 'second', 'apex']
src = sys.argv[1]
DEN = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 4
for line in open(src):
    r = json.loads(line)
    if 'V' not in r:
        continue
    mf = margins(r['sbar'], r['V'], r['t0'])
    dev = max(abs(a - b) for a, b in zip(mf, r['margins']))
    sb = [Fr(x).limit_denominator(DEN) for x in r['sbar']]
    V = [[Fr(x).limit_denominator(DEN) for x in v] for v in r['V']]
    sbn = np.array([float(x) for x in sb])
    Pn = np.array([[float(V[j][i] - sb[i]) for j in range(4)] for i in range(4)])
    zk, lam = zK(sbn, Pn, np.ones(4), return_point=True)
    t0 = sbn + Pn @ lam
    mq = margins(sb, V, t0)
    k = int(np.argmin([float(x) for x in mq]))
    print(json.dumps(dict(start=r['start'], float_vs_logged_maxdiff=float(dev),
                          rounded_support=[int(j) for j in np.nonzero(lam > 1e-9)[0]],
                          rounded_min_margin=float(mq[k]), rounded_argmin=NAMES[k],
                          rounded_margins=[round(float(x), 6) for x in mq])), flush=True)
