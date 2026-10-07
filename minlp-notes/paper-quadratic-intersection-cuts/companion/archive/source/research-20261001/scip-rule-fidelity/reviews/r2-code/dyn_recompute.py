"""Review r2: independent recomputation of the dynamism-abort statistics (M1).

Does not import any stream code. Reads the raw SCIP dumps (logs/runs_minlplib/*.jsonl.gz)
and, only to identify the sampled attempts, the analysis files (logs/an_minlplib*/).

For every dynamism abort ("fail":"numerics" with nbadray increment) in the dumps:
  * the failing piece (1-3/4a if the dumped c1234a has min_nonzero/max <= 1e-15, else 4b),
    the ratio and dumped (A, B, C) of that piece, and the largest |ray entry| on quadratic vars;
For the sampled aborts additionally:
  * A, B, C recomputed from the dumped eigen data and the failing ray, in SCIP's order
    (computeRestrictionToRay), compared with the dumped values;
  * which entry is the tiny one (A, B or C) and a forward-error consistency test: the tiny
    entry is "consistent with a rounded zero at level K" if it is within K*u times the
    absolute-value evaluation of its formula (u = 2^-53). This is a heuristic, not an
    exact zero test (eigenvectors and LP values are themselves rounded).

Usage: python3 -B dyn_recompute.py OUT.jsonl  (4 worker processes)
"""
import gzip
import json
import math
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / 'logs'
U = 2.0 ** -53
EPS = 1e-9  # SCIP numerics/epsilon, used by SCIPisZero


def ratio3(c):
    v = [abs(x) for x in c[:3]]
    nz = [x for x in v if x != 0.0]
    return (min(nz) / max(v)) if nz else 1.0


def sampled_rows():
    rows = defaultdict(dict)
    for d in ('an_minlplib', 'an_minlplib2'):
        for p in sorted((LOGS / d).glob('*.jsonl')):
            for line in p.open():
                r = json.loads(line)
                if 'k' in r and r.get('fail') == 'numerics':
                    rows[r['inst']][r['k']] = r
    return rows


def restriction(rec, ray):
    """A,B,C (piece 1-3 or 4a) and 4b, with absolute-value evaluations, following SCIP."""
    nq = rec['nquad']
    sf = rec['sidefactor']
    ev = rec['eigval']
    V = rec['eigvec']
    vzlp, vb = rec['vzlp'], rec['vb']
    zlp = rec['zlp']
    kappa = rec['kappa']
    case4 = bool(rec['case4'])
    idx = [k for k, _ in ray]
    val = [v for _, v in ray]
    a = b = c = d = e = 0.0
    Sa = Sb = Sc = 0.0           # absolute-value evaluations
    wray = 0.0
    Sw = 0.0
    neg_small = []               # per negative eigenvalue: |v.r| / S(v.r)
    for i in range(nq):
        th = sf * ev[i]
        zero = abs(ev[i]) <= EPS
        if zero and not case4:
            continue
        dot = 0.0 if zero else vzlp[i] + vb[i] / (2.0 * th)
        vr = 0.0
        Svr = 0.0
        for k, v in ray:
            if k >= nq:
                break
            vr += V[i * nq + k] * v
            Svr += abs(V[i * nq + k] * v)
        Sdot = 0.0
        if not zero:
            Sdot = sum(abs(V[i * nq + k] * zlp[k]) for k in range(nq)) + abs(vb[i] / (2.0 * th))
        if zero:
            wray += vb[i] * vr
            Sw += abs(vb[i]) * Svr
        elif th > 0:
            d += th * dot * vr
            e += th * dot * dot
        else:
            a -= th * vr * vr
            b -= 2.0 * th * dot * vr
            c -= th * dot * dot
            # absolute evaluations: vr may be noise of size u*Svr
            Sa += -th * Svr * Svr
            Sb += -2.0 * th * (abs(dot) + Sdot) * Svr
            Sc += -th * (abs(dot) + Sdot) ** 2
            neg_small.append(abs(vr) / Svr if Svr > 0 else 0.0)
    out = {}
    if not case4:
        e += max(kappa, 0.0)
        c -= min(kappa, 0.0)
        Sc += abs(min(kappa, 0.0))
        out['p1'] = (a, b, c)
        out['S1'] = (Sa, Sb, Sc)
        out['neg_small'] = neg_small
        return out
    # Case 4: linear part of w(ray)
    lin = rec['lincoefs']
    nl = rec['nlin']
    ray_d = dict(ray)
    if idx[-1] == nq + nl:
        wray += -sf * val[-1]
        Sw += abs(val[-1])
    # SCIP adds the linear entries from the back; order matters only at rounding level
    for k in reversed(idx):
        if k < nq:
            break
        if k == nq + nl:
            continue
        wray += sf * lin[k - nq] * ray_d[k]
        Sw += abs(lin[k - nq] * ray_d[k])
    b4 = (a * e, b * e, c * e) if e <= 100 else (a, b, c)
    norm = math.sqrt(1.0 + kappa * kappa)
    wzlp = rec['wzlp']
    yextra = wzlp + kappa - norm
    Sy = abs(wzlp) + abs(kappa) + norm
    a4 = a + wray * wray / (4.0 * norm)
    b4a = b + 2.0 * yextra * wray / (4.0 * norm)
    c4 = c + yextra * yextra / (4.0 * norm)
    out['p1'] = (a4, b4a, c4)
    out['S1'] = (Sa + Sw * Sw / (4 * norm),
                 Sb + 2.0 * (abs(yextra) + Sy) * Sw / (4 * norm),
                 Sc + (abs(yextra) + Sy) ** 2 / (4 * norm))
    out['p4b'] = b4
    out['neg_small'] = neg_small
    out['w_small'] = abs(wray) / Sw if Sw > 0 else 0.0
    return out


def work(inst_and_rows):
    inst, rows = inst_and_rows
    res = []
    k = -1
    with gzip.open(LOGS / 'runs_minlplib' / (inst + '.jsonl.gz'), 'rt') as f:
        for line in f:
            if not line.startswith('{"v":'):
                continue
            k += 1
            if '"fail":"numerics"' not in line:
                continue
            rec = json.loads(line)
            if rec['nbadray1'] - rec['nbadray0'] != 1:
                res.append({'inst': inst, 'k': k, 'kind': 'not_dynamism'})
                continue
            fe = [x for x in rec['perray'] if x.get('fail')]
            assert len(fe) == 1
            fe = fe[0]
            r1 = ratio3(fe['c1234a'])
            if r1 <= 1e-15:
                piece, ratio, coefs = '1-3/4a', r1, fe['c1234a']
            else:
                piece, ratio, coefs = '4b', ratio3(fe['c4b']), fe['c4b']
            row = {'inst': inst, 'k': k, 'kind': 'dyn', 'piece': piece, 'ratio': ratio,
                   'case4': rec['case4'], 'sampled': k in rows, 'coefs': coefs[:3],
                   'rayqmax': max([abs(v) for i, v in rec['rays'][fe['i']] if i < rec['nquad']] or [0.0])}
            if k in rows:
                ar = rows[k]
                row['match_lp_cons'] = (ar['lp'] == rec['lp'] and ar['cons'] == rec['cons']
                                        and ar['fail_ray'] == fe['i'])
                r = restriction(rec, rec['rays'][fe['i']])
                key = 'p1' if piece == '1-3/4a' else 'p4b'
                mine = r[key]
                row['recomp_maxrel'] = max(abs(x - y) / max(abs(y), 1e-300)
                                           for x, y in zip(mine, coefs[:3]) if y != 0 or x != 0) \
                    if any(coefs[:3]) else 0.0
                row['recomp_tiny_same'] = all((abs(x) <= 1e-15 * max(map(abs, mine))) ==
                                              (abs(y) <= 1e-15 * max(map(abs, coefs[:3])))
                                              for x, y in zip(mine, coefs[:3]))
                mx = max(abs(x) for x in coefs[:3])
                tiny = [j for j in range(3) if coefs[j] != 0 and abs(coefs[j]) <= 1e-15 * mx]
                row['tiny'] = ''.join('ABC'[j] for j in tiny)
                if piece == '1-3/4a':
                    S = r['S1']
                    # level K at which each tiny entry is within K*u*S
                    row['K_needed'] = max(abs(coefs[j]) / (U * S[j]) if S[j] > 0 else math.inf
                                          for j in tiny)
                    row['neg_max_rel'] = max(r['neg_small']) if r['neg_small'] else 0.0
                    if 'w_small' in r:
                        row['w_rel'] = r['w_small']
            res.append(row)
    return res


def main():
    out = sys.argv[1]
    rows = sampled_rows()
    insts = sorted(p.name[:-len('.jsonl.gz')] for p in (LOGS / 'runs_minlplib').glob('*.jsonl.gz'))
    jobs = [(i, rows.get(i, {})) for i in insts]
    jobs.sort(key=lambda j: -(LOGS / 'runs_minlplib' / (j[0] + '.jsonl.gz')).stat().st_size)
    with Pool(4) as pool, open(out, 'w') as fo:
        for res in pool.imap_unordered(work, jobs):
            for r in res:
                fo.write(json.dumps(r) + '\n')
            if res:
                print('done', res[0]['inst'], len(res), flush=True)


if __name__ == '__main__':
    main()
