"""Exact verification of the random corners where the orbit family numerically misses z_K
(note, Section 7.1).  Regenerates the corners of exp_random.py from (seed, idx), rescales the rays
to w = 1 (p_j / w_j), rounds apex and rays to rationals (denominator 10^6), and certifies
z_K >= z_lo (det > 0 on T_{z_lo}) and z_orbit <= z_up (rational PD dual certificate) exactly.
Usage: python3 verify_misses.py LOG.jsonl [LOG2.jsonl ...]
"""
import sys
import json
from fractions import Fraction as Fr
import numpy as np
import exact_tools as ex
from minor_core import zK, FamilySolver, precondition, det4

ATTAIN = 1 - 1e-5
DEN = 10 ** 6
for path in sys.argv[1:]:
    recs = [json.loads(l) for l in open(path)]
    miss = {r['idx']: r for r in recs if r.get('zK') is not None and r['ratios']['orbit'] < ATTAIN}
    if not miss:
        continue
    seed, N = recs[0]['seed'], next(r['N'] for r in recs if r.get('zK') is not None)
    rng = np.random.default_rng(seed)
    tries = 0
    while miss and tries < 100000:
        tries += 1
        s = rng.normal(size=4)
        if det4(s) <= 0:
            continue
        P = rng.normal(size=(4, N))
        w = rng.uniform(0.2, 2.0, N)
        if tries not in miss:
            continue
        r = miss.pop(tries)
        sb = tuple(Fr(x).limit_denominator(DEN) for x in s)
        Pq = [tuple(Fr(x).limit_denominator(DEN) for x in P[:, j] / w[j]) for j in range(N)]
        sbn = np.array([float(x) for x in sb])
        Pn = np.array([[float(Pq[j][i]) for j in range(N)] for i in range(4)])
        zk = zK(sbn, Pn, np.ones(N))
        zlo = Fr(int(np.floor(zk * (1 - 1e-7) * 10 ** 9)), 10 ** 9)
        Tz = [sb] + [tuple(sb[c] + zlo * Pq[j][c] for c in range(4)) for j in range(N)]
        m, _ = ex.min_det_over_simplex(Tz)   # valid for any polytope: every point lies in a sub-simplex
        okL = (m is not None and m > 0)
        sI, PI = precondition(sbn, Pn)
        c_, h_, _ = FamilySolver('orbit', sI, PI, np.ones(N)).best(zk, iters=40)
        zup = None
        for du in (1e-7, 1e-6, 1e-5, 1e-4):
            z = Fr(int(np.ceil((c_ + du * zk) * 10 ** 9)), 10 ** 9)
            if ex.upper_certificate(ex.ORBIT_BASIS, sb, [list(p) for p in Pq], [Fr(1)] * N, z)[0]:
                zup = z
                break
        print(json.dumps(dict(log=path, idx=r['idx'], support=r['support'], logged_ratio=r['ratios']['orbit'],
                              zK_lower_ok=bool(okL), orbit_numeric=c_ / zk,
                              ratio_upper_exact=float(zup / zlo) if (zup is not None and okL) else None,
                              orbit_upper_over_zK_numeric=float(zup) / zk if zup is not None else None)), flush=True)
