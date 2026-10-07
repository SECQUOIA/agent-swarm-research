"""Exact certificate: support one does not save the orbit family for minors (note, Theorem 9).

Full-dimensional rational corner (w = 1, four rays) whose unique corner minimizer is the vertex
t0 = v1 (support one), with every edge of T* at t0 transversal to the null cone and strictly
positive KKT multipliers of the other rays; a rational positive definite dual certificate shows
that no orbit set contains T_z for some z < 1.  Usage: python3 certify_supp1_full.py [JSON]
"""
import json
import sys
from fractions import Fraction as Fr

import numpy as np

import exact_tools as ex
from cert_lib import Checker, load, corner_checks, orbit_upper, brackets, scip_value
from minor_core import FamilySolver, precondition

INSTANCE = {"sbar": [-4, -1, "-1/2", -2], "v1": [3, 3, -3, -3], "v2": ["95/24", 4, -4, -4],
            "v3": ["17/3", 6, "-3/2", "-3/2"], "v4": ["41/6", 3, -6, -2], "t0": [3, 3, -3, -3]}
if len(sys.argv) > 1:
    INSTANCE = json.loads(sys.argv[1])
chk = Checker()
V = load(INSTANCE)
P, g, sigma, nu = corner_checks(chk, V)
t0 = V['t0']
chk('(3) support one: t0 = v1', t0 == V['v1'])
chk('(3) strict complementarity: nu_1 = 0 and nu_2, nu_3, nu_4 > 0 (%s)' % [str(x) for x in nu],
    nu[0] == 0 and all(x > 0 for x in nu[1:]))
tr = [ex.dot(g, ex.add(V[k], t0, 1, -1)) for k in ('sbar', 'v2', 'v3', 'v4')]
chk('(3) every edge of T* at t0 is transversal: grad det(t0) . (v - t0) = %s > 0' % [str(x) for x in tr],
    all(x > 0 for x in tr))
sbn = np.array([float(x) for x in V['sbar']])
Pn = np.array([[float(P[j][i]) for j in range(4)] for i in range(4)])
sI, PI = precondition(sbn, Pn)
c_, h_, _ = FamilySolver('orbit', sI, PI, np.ones(4)).best(1.0, iters=40)
print('   numerical orbit bound %.8f (upper %.8f)' % (c_, h_))
orbit_upper(chk, V, P, Fr(1))
orbit_upper(chk, V, P, Fr(int(np.ceil(h_ * 1000)), 1000))
br = brackets(chk, V, P)
zs = scip_value(V, P)
print('SUMMARY z_K = 1 (support one); orbit in [%.7f, %.7f]; pr in [%.7f, %.7f]; bcm in [%.7f, %.7f]; scip = %.10f'
      % (float(br['orbit'][0]), float(br['orbit'][1]), float(br['pr'][0]), float(br['pr'][1]),
         float(br['bcm'][0]), float(br['bcm'][1]), float(zs)))
print('ALL PASS' if chk.ok else 'SOME CHECK FAILED')
