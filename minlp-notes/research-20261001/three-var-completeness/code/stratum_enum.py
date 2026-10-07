"""Systematic enumeration of point-contact strata of extreme rays of P3
(note.md, Section 2.8).  Numerical.

A zero type is (s, T): s in {0,1,-1}^3 is the face carrying the zero (-1 =
free coordinate, value generic in (0,1)); T is a set of fixed coordinates in
which the first derivative also vanishes (tangential contact).  Facet zeros
carry no tangency (that forces a convex quadratic).  A zero of type (s, T)
imposes 1 + |free(s)| + |T| linear conditions on the 10 coefficients.

We enumerate all sets of zero types, one per face, with
  * total number of conditions 9 ("generic strata": the conditions determine
    p up to scale at generic positions), or
  * total 10 ("determinantal strata": one position is solved from the
    determinant condition, the others are random),
subject to necessary conditions for a nonnegative quadratic with positive
square coefficients and isolated zeros:
  * no two zeros on a common axis-parallel line (strict convexity),
  * no other zero in the closure of a facet carrying an interior zero,
  * a vertex zero is not on an edge that carries a zero.
Types are reduced modulo the 48 cube symmetries.  For each type and each
sample of positions we compute the kernel p (rank 9 required), keep +-p if it
is nonnegative on the cube (face enumeration), and record its sign class.
Quadratics with positive square coefficients and an indefinite Hessian are
tested against the D3 relaxation and against R (D3 + 24 family LMIs).

usage: python stratum_enum.py PART NPARTS SAMPLES9 SAMPLES10 SEED [TAG]
Writes ../logs/stratum_enumTAG_PART.jsonl (one line per type, checkpointed).
"""
import json
import os
import sys
import time
import warnings
from itertools import combinations, permutations, product

import numpy as np

warnings.filterwarnings("ignore")
from cube3 import QKEYS, face_minimizers, quad_from_vector  # noqa: E402
from face_explore import lin_deriv, lin_value  # noqa: E402

FACES = [s for s in product((0, 1, -1), repeat=3) if s != (-1, -1, -1)]


def free(s):
    return tuple(i for i in range(3) if s[i] == -1)


def zero_types():
    out = []
    for s in FACES:
        fixed = [i for i in range(3) if s[i] != -1]
        if len(free(s)) == 2:
            out.append((s, ()))
            continue
        for k in range(len(fixed) + 1):
            for T in combinations(fixed, k):
                out.append((s, T))
    return out


ZT = zero_types()


def ncond(z):
    s, T = z
    return 1 + len(free(s)) + len(T)


def contains(big, small):
    """Face `small` lies in the closure of face `big`."""
    return all(big[i] == -1 or big[i] == small[i] for i in range(3))


def realizable(config):
    faces = [s for s, _ in config]
    if len(set(faces)) < len(faces):
        return False
    for a, b in combinations(faces, 2):
        # common axis-parallel line: two fixed coordinates agree
        if len([j for j in range(3) if a[j] != -1 and a[j] == b[j]]) >= 2:
            return False
        # facet zero excludes other zeros in its closure
        for f, o in ((a, b), (b, a)):
            if len(free(f)) == 2 and contains(f, o):
                return False
    return True


def act_zero(z, g):
    s, T = z
    perm, flips = g
    ns = []
    for i in range(3):
        c = s[perm[i]]
        if c != -1 and flips[i]:
            c = 1 - c
        ns.append(c)
    inv = {perm[i]: i for i in range(3)}
    nT = tuple(sorted(inv[t] for t in T))
    return (tuple(ns), nT)


GROUP = [(perm, flips) for perm in permutations(range(3)) for flips in product((0, 1), repeat=3)]


def canon(config):
    return min(tuple(sorted(act_zero(z, g) for z in config)) for g in GROUP)


def enumerate_types(total):
    seen = set()
    out = []
    zt = sorted(ZT, key=ncond)

    def rec(start, chosen, cnt):
        if cnt == total:
            key = canon(chosen)
            if key not in seen:
                seen.add(key)
                out.append(key)
            return
        for idx in range(start, len(zt)):
            z = zt[idx]
            c = ncond(z)
            if cnt + c > total:
                continue
            new = chosen + [z]
            if not realizable(new):
                continue
            rec(idx + 1, new, cnt + c)
    rec(0, [], 0)
    return out


def rows(config, pos):
    """pos: list of points (one per zero)."""
    R = []
    for (s, T), p in zip(config, pos):
        R.append(lin_value(p))
        for i in sorted(set(free(s)) | set(T)):
            R.append(lin_deriv(p, i))
    return np.array(R)


def random_positions(config, rng):
    return [[rng.uniform(0.05, 0.95) if c == -1 else float(c) for c in s] for s, _ in config]


def kernel(M):
    U, sv, Vt = np.linalg.svd(M)
    if len(sv) < 9 or sv[8] < 1e-9 * sv[0]:
        return None   # rank < 9
    if M.shape[0] >= 10 and sv[9] > 1e-9 * sv[0]:
        return None   # rank 10 (no nonzero kernel)
    return Vt[-1]


def cubemin(p):
    q = quad_from_vector(p)
    return min(v for (_, _, v) in face_minimizers(q, tol=-1e-12))


def classify(p):
    sc = np.abs(p).max()
    p = p / sc
    sq = p[4:7]
    Q = np.array([[p[4], p[7] / 2, p[8] / 2], [p[7] / 2, p[5], p[9] / 2], [p[8] / 2, p[9] / 2, p[6]]])
    ev = np.linalg.eigvalsh(Q)
    prod = p[7] * p[8] * p[9]
    return p, dict(min_square=float(sq.min()), min_eig=float(ev[0]), cross_product=float(prod))


def solve_det_roots(config, pos, zi, ci):
    """Positions pos; vary coordinate ci of zero zi in (0.02, 0.98); return
    roots of det(rows) (10 x 10)."""
    def f(t):
        pp = [list(p) for p in pos]
        pp[zi][ci] = t
        M = rows(config, pp)
        return np.linalg.det(M)
    ts = np.cos(np.linspace(0, np.pi, 13)) * 0.5 + 0.5
    vals = np.array([f(t) for t in ts])
    if not np.all(np.isfinite(vals)) or np.abs(vals).max() == 0:
        return []
    coef = np.polynomial.chebyshev.chebfit(2 * ts - 1, vals / np.abs(vals).max(), 7)
    roots = np.polynomial.chebyshev.chebroots(coef)
    out = []
    for r in roots:
        if abs(r.imag) < 1e-9:
            t = (r.real + 1) / 2
            if 0.02 < t < 0.98:
                # refine by secant on f
                a, b = t - 1e-4, t + 1e-4
                fa, fb = f(a), f(b)
                for _ in range(40):
                    if fb == fa:
                        break
                    c = b - fb * (b - a) / (fb - fa)
                    a, fa, b, fb = b, fb, c, f(c)
                    if abs(b - a) < 1e-14:
                        break
                if 0.02 < b < 0.98:
                    out.append(b)
    return out


def candidates_for(config, total, rng, samples):
    cands = []
    for _ in range(samples):
        pos = random_positions(config, rng)
        if total == 9:
            M = rows(config, pos)
            v = kernel(M)
            if v is not None:
                cands.append((v, pos))
        else:
            params = [(zi, ci) for zi, (s, _) in enumerate(config) for ci in range(3) if s[ci] == -1]
            if not params:
                return cands
            zi, ci = params[rng.integers(len(params))]
            for t in solve_det_roots(config, pos, zi, ci):
                pp = [list(p) for p in pos]
                pp[zi][ci] = t
                v = kernel(rows(config, pp))
                if v is not None:
                    cands.append((v, pp))
    return cands


def main():
    part, nparts, s9, s10, seed = (int(a) for a in sys.argv[1:6])
    tag = sys.argv[6] if len(sys.argv) > 6 else ''
    order = sys.argv[7] if len(sys.argv) > 7 else 'fwd'
    rng = np.random.default_rng(seed + 1000 * part)
    t0 = time.time()
    cache = '../logs/stratum_types.json'
    if os.path.exists(cache):
        raw = json.load(open(cache))
        types = [(t, tuple((tuple(s), tuple(T)) for s, T in c)) for t, c in raw]
    else:
        types = [(9, c) for c in enumerate_types(9)] + [(10, c) for c in enumerate_types(10)]
        json.dump(types, open(cache, 'w'))
    if part == 0:
        print('types: 9 conditions %d, 10 conditions %d' % (
            sum(1 for t, _ in types if t == 9), sum(1 for t, _ in types if t == 10)), flush=True)
    mine = types[part::nparts]
    if order == 'rev':
        mine = mine[::-1]
    out_path = f'../logs/stratum_enum{tag}_{part}.jsonl'
    base = tag.rstrip('R')   # reverse shards ('_denseR') also skip types done by '_dense' shards

    def done_keys():
        keys = set()
        import glob as _glob
        for fn in _glob.glob(f'../logs/stratum_enum{base}*_*.jsonl'):
            for ln in open(fn):
                keys.add(json.loads(ln)['key'])
        return keys
    done = done_keys()
    from sdp3 import Relaxation
    R1 = Relaxation(use_family=True)
    R0 = Relaxation(use_family=False)
    for total, config in mine:
        key = repr((total, config))
        if order == 'rev':
            done = done_keys()
        if key in done:
            continue
        cands = candidates_for(list(config), total, rng, s9 if total == 9 else s10)
        rec = dict(key=key, total=total, config=[list(map(list, z)) for z in config] if False else repr(config),
                   kernels=len(cands), nonneg=0, interesting=0, tested_d3=0, notd3=0, missing=0,
                   min_r_d3=None, min_r_R=None, signclass_counts={}, examples=[])
        for v, pos in cands:
            for sgn in (1, -1):
                p = sgn * v
                p = p / np.abs(p).max()
                if cubemin(p) < -1e-9:
                    continue
                rec['nonneg'] += 1
                p, info = classify(p)
                interesting = info['min_square'] > 1e-7 and info['min_eig'] < -1e-9
                cls = 'sup' if info['cross_product'] > 1e-12 else ('sub' if info['cross_product'] < -1e-12 else 'zero')
                rec['signclass_counts'][cls] = rec['signclass_counts'].get(cls, 0) + 1
                if not interesting:
                    continue
                rec['interesting'] += 1
                # D3 test for every interesting ray; R test when outside D3
                try:
                    r0 = R0.solve(p)[0]
                except BaseException as e:
                    if isinstance(e, KeyboardInterrupt):
                        raise
                    continue
                rec['tested_d3'] += 1
                rec['min_r_d3'] = r0 if rec['min_r_d3'] is None else min(rec['min_r_d3'], r0)
                if r0 < -1e-6:
                    rec['notd3'] += 1
                    try:
                        r1 = R1.solve(p)[0]
                    except BaseException as e:
                        if isinstance(e, KeyboardInterrupt):
                            raise
                        continue
                    rec['min_r_R'] = r1 if rec['min_r_R'] is None else min(rec['min_r_R'], r1)
                    if r1 < -1e-6:
                        rec['missing'] += 1
                    if len(rec['examples']) < 3 or r1 < -1e-6:
                        rec['examples'].append(dict(p=p.tolist(), pos=pos, r_d3=r0, r_R=r1, cls=cls))
        with open(out_path, 'a') as fh:
            fh.write(json.dumps(rec, default=float) + '\n')
    print('part', part, 'done', len(mine), 'types, time %.0f' % (time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
