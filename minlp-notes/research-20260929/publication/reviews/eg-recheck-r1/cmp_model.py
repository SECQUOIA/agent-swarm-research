"""Compare the model data that the eg-recheck certification used (indep_cert.Model, read from the
MINLPLib GAMS file) with the verifier's own decoding of the cached OSIL file (own_model.py).

indep_cert is imported ONLY to read its data arrays; nothing it computes is used for a claim.
Checks, per row: objective/side role, constant (exact Fraction), side bounds (exact), linear
coefficients, and the multiset of terms (a, mu_1..7) plus per-variable gamma and scale, with the
float data of indep_cert compared to float(Fraction) of the OSIL decimal strings (exact equality).
Also the variable bounds and integrality.
"""
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from own_model import OsilModel  # noqa: E402

sys.path.insert(1, os.path.join(HERE, "..", "..", "..", "reviews", "eg-retry-review-checks"))
import indep_cert  # noqa: E402

O = OsilModel()
M = indep_cert.Model("eg_disc2_s")
bad = 0
assert M.vars == O.names[:7], (M.vars, O.names)
for i in range(7):
    ok = (Fr(M.qlb[i]) == O.vlb[i] and Fr(M.qub[i]) == O.vub[i] and bool(M.isint[i]) == O.vint[i])
    bad += not ok
    print("var", O.names[i], "osil", O.vlb[i], O.vub[i], O.vint[i], "gms", M.qlb[i], M.qub[i], bool(M.isint[i]), "OK" if ok else "MISMATCH")
for k in range(28):
    r = O.rows[k]
    # role and constants
    if k < 24:
        assert O.objcoef[k] == 1 and O.cub[k] is None
        ok_c = Fr(M.qc[k]) == O.clb[k]
    else:
        j = k - 24
        # -h in [lb, ub]  <=>  h in [-ub, -lb]
        want_hi = None if O.clb[k] is None else -O.clb[k]
        want_lo = None if O.cub[k] is None else -O.cub[k]
        ok_c = (M.qghi[j] == want_hi) and (M.qglo[j] == want_lo)
    # linear
    lin_osil = [float(r["lin"].get(i, Fr(0))) for i in range(7)]
    ok_l = list(M.LIN[k]) == lin_osil and [Fr(v) for v in M.qLIN[k]] == [r["lin"].get(i, Fr(0)) for i in range(7)]
    # gamma and scale per variable, shared by all terms of the row
    gam = {i: set(f[i][2] for _, f in r["terms"]) for i in range(7)}
    sca = {i: set(f[i][0] for _, f in r["terms"]) for i in range(7)}
    ok_g = all(len(gam[i]) == 1 and float(next(iter(gam[i]))) == M.GA[k, i] for i in range(7))
    ok_s = all(len(sca[i]) == 1 and float(next(iter(sca[i]))) == M.S[i] for i in range(7))
    # terms as multisets
    to = sorted((float(a),) + tuple(float(f[i][1]) for i in range(7)) for a, f in r["terms"])
    tg = sorted((M.A[k, m],) + tuple(M.MU[k, m, :]) for m in range(M.Mt))
    ok_t = to == tg
    ok = ok_c and ok_l and ok_g and ok_s and ok_t
    bad += not ok
    print(f"row {k:2d} ({'obj' if k < 24 else 'side'}): const {ok_c} lin {ok_l} gamma {ok_g} scale {ok_s} "
          f"terms {ok_t} ({len(to)} vs {len(tg)})")
print("MODEL DATA IDENTICAL (OSIL vs data used by indep_cert)" if bad == 0 else f"MISMATCHES: {bad}")
